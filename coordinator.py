"""DataUpdateCoordinator voor Vistapool."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import VistapoolApiClient, VistapoolApiError, VistapoolConnectionError
from .firestore_parser import parse_firestore_doc

_LOGGER = logging.getLogger(__name__)

# Update interval
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)


class VistapoolDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """
    Coordinator om periodiek pool data op te halen.
    
    Gebruikt de DataUpdateCoordinator van Home Assistant voor
    efficiënte en gecoördineerde updates van alle entities.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        config_data: Dict[str, str],
        update_interval: timedelta = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """
        Initialiseer de coordinator.
        
        Args:
            hass: Home Assistant instance
            config_data: Configuratie data met API credentials
            update_interval: Interval tussen updates
        """
        self.api = VistapoolApiClient(
            api_key=config_data["api_key"],
            email=config_data["email"],
            password=config_data["password"],
            project=config_data["project"],
            gateway=config_data["gateway"],
            pool_id=config_data["pool_id"],
        )

        super().__init__(
            hass,
            _LOGGER,
            name="Vistapool Data Update Coordinator",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """
        Haal de laatste pool data op.
        
        Deze methode wordt automatisch aangeroepen door de coordinator
        op basis van het update_interval.
        
        Returns:
            Dictionary met geparste pool data
            
        Raises:
            UpdateFailed: Bij fouten tijdens het ophalen van data
        """
        try:
            # Login indien nodig (draait in executor)
            await self.hass.async_add_executor_job(self.api.login)

            # Haal pool document op
            _LOGGER.debug("Haal pool document op voor %s", self.api._pool_id)
            raw_doc = await self.hass.async_add_executor_job(
                self.api.get_pool_document
            )

            # Parse Firestore document naar normale dict
            parsed_data = parse_firestore_doc(raw_doc)

            if not parsed_data:
                raise UpdateFailed("Ontvangen lege data van Vistapool API")

            _LOGGER.debug("Pool data succesvol opgehaald en geparst")
            return parsed_data

        except VistapoolConnectionError as err:
            # Netwerk fouten zijn vaak tijdelijk
            _LOGGER.warning("Verbindingsfout met Vistapool API: %s", err)
            raise UpdateFailed(f"Kan geen verbinding maken met Vistapool: {err}") from err

        except VistapoolApiError as err:
            # API fouten kunnen structureel zijn
            _LOGGER.error("Vistapool API fout: %s", err)
            raise UpdateFailed(f"Fout bij ophalen Vistapool data: {err}") from err

        except Exception as err:
            # Onverwachte fouten
            _LOGGER.exception("Onverwachte fout bij updaten van Vistapool data")
            raise UpdateFailed(
                f"Onverwachte fout bij Vistapool data update: {err}"
            ) from err

    async def async_send_command(
        self, operation: str, changes: str = "10"
    ) -> None:
        """
        Stuur een commando naar de pool en refresh data.
        
        Args:
            operation: Het uit te voeren commando
            changes: De wijzigingen
        """
        try:
            await self.hass.async_add_executor_job(
                self.api.send_command, operation, changes
            )
            # Wacht even voordat we refreshen
            await self.async_request_refresh()
        except VistapoolApiError as err:
            _LOGGER.error("Fout bij verzenden commando: %s", err)
            raise

    async def async_send_pool_command(
        self, operation: str, changes: Dict[str, Any]
    ) -> None:
        """
        Stuur een pool configuratie commando en refresh data.
        
        Args:
            operation: Het uit te voeren commando
            changes: Dictionary met wijzigingen
        """
        try:
            await self.hass.async_add_executor_job(
                self.api.send_pool_command, operation, changes
            )
            # Wacht even voordat we refreshen
            await self.async_request_refresh()
        except VistapoolApiError as err:
            _LOGGER.error("Fout bij verzenden pool commando: %s", err)
            raise
