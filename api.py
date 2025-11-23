"""API-client voor Vistapool/Oxilife."""
from __future__ import annotations

import time
import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

import requests
from requests.exceptions import RequestException, Timeout

_LOGGER = logging.getLogger(__name__)

# API endpoints
LOGIN_URL = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
REFRESH_URL = "https://securetoken.googleapis.com/v1/token"
FIRESTORE_URL = "https://firestore.googleapis.com/v1"
SENDCMD_URL = "https://europe-west1-hayward-europe.cloudfunctions.net/sendCommand"
SENDPOOL_URL = "https://europe-west1-hayward-europe.cloudfunctions.net/sendPoolCommand"

# Constanten
TOKEN_EXPIRY_BUFFER = 300  # 5 minuten voor expiratie
REQUEST_TIMEOUT = 15


class VistapoolApiError(Exception):
    """Base exception voor Vistapool API errors."""


class VistapoolAuthError(VistapoolApiError):
    """Authentication error."""


class VistapoolConnectionError(VistapoolApiError):
    """Connection error."""


class VistapoolApiClient:
    """API client voor Vistapool/Oxilife zwembadbesturing."""

    def __init__(
        self,
        api_key: str,
        email: str,
        password: str,
        project: str,
        gateway: str,
        pool_id: str,
    ) -> None:
        """Initialiseer de API client."""
        self._api_key = api_key
        self._email = email
        self._password = password
        self._project = project
        self._gateway = gateway
        self._pool_id = pool_id

        self._id_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_acquired_at: float = 0

        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})

    @property
    def is_token_valid(self) -> bool:
        """Check of het huidige token nog geldig is."""
        if not self._id_token:
            return False
        
        time_since_acquired = time.time() - self._token_acquired_at
        # Token is 1 uur geldig, vernieuw 5 min voor expiratie
        return time_since_acquired < (3600 - TOKEN_EXPIRY_BUFFER)

    def login(self) -> None:
        """
        Login met email/wachtwoord.
        
        Raises:
            VistapoolAuthError: Bij authenticatie fouten
            VistapoolConnectionError: Bij netwerk fouten
        """
        if self.is_token_valid:
            _LOGGER.debug("Token is nog geldig, skip login")
            return

        _LOGGER.info("Vistapool login voor %s", self._email)
        
        url = f"{LOGIN_URL}?key={self._api_key}"
        payload = {
            "email": self._email,
            "password": self._password,
            "returnSecureToken": True,
        }

        try:
            resp = self._session.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()

            self._id_token = data["idToken"]
            self._refresh_token = data["refreshToken"]
            self._token_acquired_at = time.time()
            
            _LOGGER.info("Vistapool login succesvol")

        except requests.HTTPError as err:
            if err.response.status_code in (400, 401):
                raise VistapoolAuthError(
                    f"Authenticatie gefaald: {err.response.text}"
                ) from err
            raise VistapoolConnectionError(f"HTTP error tijdens login: {err}") from err
        except Timeout as err:
            raise VistapoolConnectionError("Login timeout") from err
        except RequestException as err:
            raise VistapoolConnectionError(f"Netwerk fout tijdens login: {err}") from err

    def refresh_id_token(self) -> None:
        """
        Vernieuw het ID token met de refresh token.
        
        Raises:
            VistapoolAuthError: Bij authenticatie fouten
            VistapoolConnectionError: Bij netwerk fouten
        """
        if not self._refresh_token:
            _LOGGER.warning("Geen refresh token beschikbaar, voer volledige login uit")
            self.login()
            return

        _LOGGER.debug("Vernieuw Vistapool token")
        
        url = f"{REFRESH_URL}?key={self._api_key}"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }

        try:
            resp = self._session.post(url, data=payload, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()

            self._id_token = data["id_token"]
            self._refresh_token = data["refresh_token"]
            self._token_acquired_at = time.time()
            
            _LOGGER.debug("Token succesvol vernieuwd")

        except requests.HTTPError as err:
            _LOGGER.warning("Token refresh gefaald, voer volledige login uit")
            self.login()
        except (Timeout, RequestException) as err:
            raise VistapoolConnectionError(f"Fout bij token refresh: {err}") from err

    def _ensure_authenticated(self) -> None:
        """Zorg ervoor dat we een geldig token hebben."""
        if not self.is_token_valid:
            if self._refresh_token:
                self.refresh_id_token()
            else:
                self.login()

    def get_pool_document(self) -> Dict[str, Any]:
        """
        Haal het Firestore pool document op.
        
        Returns:
            Dict met pool data in Firestore formaat
            
        Raises:
            VistapoolApiError: Bij API fouten
        """
        self._ensure_authenticated()

        url = (
            f"{FIRESTORE_URL}/projects/{self._project}/databases/(default)/"
            f"documents/pools/{self._pool_id}"
        )
        headers = {"Authorization": f"Bearer {self._id_token}"}

        try:
            resp = self._session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.json()

        except requests.HTTPError as err:
            raise VistapoolApiError(
                f"Fout bij ophalen pool document: {err.response.status_code}"
            ) from err
        except (Timeout, RequestException) as err:
            raise VistapoolConnectionError(
                f"Netwerk fout bij ophalen pool document: {err}"
            ) from err

    def send_command(
        self, operation: str, changes: str = "10"
    ) -> None:
        """
        Stuur een simpel commando naar de pool.
        
        Args:
            operation: Het uit te voeren commando
            changes: De wijzigingen (meestal "10")
            
        Raises:
            VistapoolApiError: Bij API fouten
        """
        self._ensure_authenticated()

        headers = {"Authorization": f"Bearer {self._id_token}"}
        payload = {
            "gateway": self._gateway,
            "poolId": self._pool_id,
            "operation": operation,
            "operationId": None,
            "changes": changes,
            "pool": None,
            "source": "homeassistant",
        }

        try:
            resp = self._session.post(
                SENDCMD_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            _LOGGER.debug("Commando %s succesvol verzonden", operation)

        except requests.HTTPError as err:
            raise VistapoolApiError(
                f"Fout bij verzenden commando {operation}: {err.response.text}"
            ) from err
        except (Timeout, RequestException) as err:
            raise VistapoolConnectionError(
                f"Netwerk fout bij verzenden commando: {err}"
            ) from err

    def send_pool_command(
        self, operation: str, changes: Dict[str, Any]
    ) -> None:
        """
        Stuur een pool configuratie commando.
        
        Args:
            operation: Het uit te voeren commando (meestal "WRP")
            changes: Dictionary met wijzigingen
            
        Raises:
            VistapoolApiError: Bij API fouten
        """
        self._ensure_authenticated()

        headers = {"Authorization": f"Bearer {self._id_token}"}
        payload = {
            "gateway": self._gateway,
            "poolId": self._pool_id,
            "operation": operation,
            "operationId": None,
            "changes": json.dumps(changes),
            "pool": None,
            "source": "homeassistant",
        }

        _LOGGER.debug(
            "Verzend pool commando %s met changes: %s", 
            operation, 
            json.dumps(changes, indent=2)
        )

        try:
            resp = self._session.post(
                SENDPOOL_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            _LOGGER.info("Pool commando %s succesvol verzonden", operation)

        except requests.HTTPError as err:
            _LOGGER.error(
                "Fout bij pool commando %s: %s", 
                operation, 
                err.response.text
            )
            raise VistapoolApiError(
                f"Fout bij pool commando {operation}: {err.response.text}"
            ) from err
        except (Timeout, RequestException) as err:
            raise VistapoolConnectionError(
                f"Netwerk fout bij pool commando: {err}"
            ) from err

    def close(self) -> None:
        """Sluit de HTTP sessie."""
        self._session.close()
