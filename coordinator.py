from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import VistapoolApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class VistapoolDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, api: VistapoolApi, user_id: str):
        """Initialize my coordinator."""
        self.api = api
        self.user_id = user_id

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),  # ← je kan dit verlagen voor test bv. 15 sec
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Firestore asynchronously."""
        raw_data = await self.api.async_get_document_data(f"config/{self.user_id}")
        parsed_data = self.api.parse_firestore_data(raw_data)
        _LOGGER.debug("Firestore data updated: %s", parsed_data)
        return parsed_data