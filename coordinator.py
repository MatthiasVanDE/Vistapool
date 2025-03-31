"""DataUpdateCoordinator voor vistapool (niet-blokkerend)."""
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .api import VistapoolApiClient
from .firestore_parser import parse_firestore_doc

_LOGGER = logging.getLogger(__name__)

class VistapoolDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator om periodiek alle Zwembad-data op te halen, niet-blokkerend."""

    def __init__(self, hass: HomeAssistant, config_data: dict):
        """Init zonder blokkerende call."""
        self.hass = hass
        self.api = VistapoolApiClient(
            api_key=config_data["api_key"],
            email=config_data["email"],
            password=config_data["password"],
            project=config_data["project"],
            gateway=config_data["gateway"],
            pool_id=config_data["pool_id"]
        )

        # NIET meer self.api.login() hier!
        update_interval = timedelta(seconds=30)

        super().__init__(
            hass,
            _LOGGER,
            name="VistapoolDataUpdateCoordinator",
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Deze methode draait elke update_interval (bvb. 30s)."""
        try:
            # 1. Inloggen via threadpool
            await self.hass.async_add_executor_job(self.api.login)
            # 2. Pool document ophalen
            doc = await self.hass.async_add_executor_job(self.api.get_pool_document)
            parsed = parse_firestore_doc(doc)
            return parsed
        except Exception as err:
            raise UpdateFailed(f"Error updating data from Vistapool: {err}") from err