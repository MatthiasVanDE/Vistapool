"""API-client voor Vistapool/Oxilife."""
import time
import json
import requests
import logging

_LOGGER = logging.getLogger(__name__)

LOGIN_URL = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
REFRESH_URL = "https://securetoken.googleapis.com/v1/token"
FIRESTORE_URL = "https://firestore.googleapis.com/v1"
SENDCMD_URL = "https://europe-west1-hayward-europe.cloudfunctions.net/sendCommand"
SENDPOOL_URL = "https://europe-west1-hayward-europe.cloudfunctions.net/sendPoolCommand"

class VistapoolApiClient:
    """Simpel Python-client om de Vistapool/Oxilife API te raadplegen."""

    def __init__(self, api_key, email, password, project, gateway, pool_id):
        self._api_key = api_key
        self._email = email
        self._password = password
        self._project = project
        self._gateway = gateway
        self._pool_id = pool_id

        self._id_token = None
        self._refresh_token = None
        self._token_acquired_at = 0

        # NIET direct login() hier!
        # Gewoon constructor zonder blokkerend call.

    def login(self):
        """Login met email/wachtwoord, haal id_token en refresh_token op (blokkerend)."""
        # Als we al een token hebben dat niet (bijna) verlopen is, kun je skippen.
        if time.time() - self._token_acquired_at < 3500 and self._id_token:
            return  # token is nog geldig genoeg

        url = f"{LOGIN_URL}?key={self._api_key}"
        payload = {
            "email": self._email,
            "password": self._password,
            "returnSecureToken": True
        }
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        self._id_token = data["idToken"]
        self._refresh_token = data["refreshToken"]
        self._token_acquired_at = time.time()
        _LOGGER.debug("Vistapool ingelogd, id_token verkregen.")

    def refresh_id_token_if_needed(self):
        """Vernieuw token als deze (bijna) is verlopen."""
        if time.time() - self._token_acquired_at > 3500:
            _LOGGER.debug("Vistapool token verversen...")
            url = f"{REFRESH_URL}?key={self._api_key}"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            }
            resp = requests.post(url, data=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            self._id_token = data["id_token"]
            self._refresh_token = data["refresh_token"]
            self._token_acquired_at = time.time()
            _LOGGER.debug("Vistapool token vernieuwd.")

    def get_pool_document(self):
        """Firestore-document ophalen (blokkerend)."""
        self.refresh_id_token_if_needed()
        headers = {"Authorization": f"Bearer {self._id_token}"}
        url = (
            f"{FIRESTORE_URL}/projects/{self._project}/databases/(default)/"
            f"documents/pools/{self._pool_id}"
        )
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def send_command(self, operation, changes="10"):
        """Simpele sendCommand call (blokkerend)."""
        self.refresh_id_token_if_needed()
        headers = {
            "Authorization": f"Bearer {self._id_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "gateway": self._gateway,
            "poolId": self._pool_id,
            "operation": operation,
            "operationId": None,
            "changes": changes,
            "pool": None,
            "source": "homeassistant"
        }
        resp = requests.post(SENDCMD_URL, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()

    def send_pool_command(self, operation, changes: dict):
        """Volledige poolinstellingen wijzigen (blokkerend)."""
        self.refresh_id_token_if_needed()
        headers = {
            "Authorization": f"Bearer {self._id_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "gateway": self._gateway,
            "poolId": self._pool_id,
            "operation": operation,
            "operationId": None,
            "changes": json.dumps(changes),
            "pool": None,
            "source": "homeassistant"
        }
        resp = requests.post(SENDPOOL_URL, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()