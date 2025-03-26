import logging
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

FILTRATION_MODE_MAP = {
    "manual": 0,
    "auto": 1,
    "smart_freeze": 3
}
FILTRATION_MODE_NAMES = {v: k for k, v in FILTRATION_MODE_MAP.items()}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    selects = []
    selects.append(VistapoolFiltrationModeSelect(coordinator))

    async_add_entities(selects)

class VistapoolFiltrationModeSelect(CoordinatorEntity, SelectEntity):
    """Kies filtratiemodus: manual(0), auto(1), smart/freeze(3)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtratie Modus"
        self._attr_unique_id = f"{coordinator.api._pool_id}_filtration_mode"
        self._attr_options = list(FILTRATION_MODE_MAP.keys())  # ["manual", "auto", "smart_freeze"]

    @property
    def current_option(self):
        data = self.coordinator.data
        mode_val = data.get("filtration", {}).get("mode", 0)
        return FILTRATION_MODE_NAMES.get(mode_val, "unknown")

    async def async_select_option(self, option: str):
        mode_val = FILTRATION_MODE_MAP[option]
        changes = {
            "filtration": {
                "mode": mode_val
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()
