import logging
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Filtratie modus mapping
FILTRATION_MODE_MAP = {
    "manual": 0,
    "auto": 1,
    "smart": 3
}
FILTRATION_MODE_NAMES = {v: k for k, v in FILTRATION_MODE_MAP.items()}

# Backwash modus mapping
BACKWASH_MODE_MAP = {
    "manual": 0,
    "automatic": 1
}
BACKWASH_MODE_NAMES = {v: k for k, v in BACKWASH_MODE_MAP.items()}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up all select entities for this integration."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    selects = []

    #
    # ================== FILTRATIE SELECTS ==================
    #
    selects.append(VistapoolFiltrationModeSelect(coordinator))

    #
    # ================== BACKWASH SELECTS ===================
    #
    selects.append(VistapoolBackwashModeSelect(coordinator))

    #
    # ================== HYDROLYSE SELECTS ==================
    # (Bijv. disable=0/1, if you prefer a select instead of a switch,
    #  but typically you'd use a switch for booleans.)

    #
    # ================== SET POINTS SELECTS =================
    # (Geen specifieke toggles in de setpoints, dus niks hier.
    #  Als je ooit een select maakt voor pH-min of zo, kun je die hier toevoegen.)

    async_add_entities(selects)


#
# --------------------------------------------------------------------------
#  DEVICE BASE CLASSES
# --------------------------------------------------------------------------
#

class FiltrationSelectBase(CoordinatorEntity, SelectEntity):
    """Alle 'Filtratie' (incl. Backwash) gerelateerde selects in hetzelfde apparaat."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class HydrolyseSelectBase(CoordinatorEntity, SelectEntity):
    """Als je toggles/selects voor Hydrolyse wilt, plaats je die hier."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_hydrolyse")},
            "name": "Hydrolyse",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class SetPointsSelectBase(CoordinatorEntity, SelectEntity):
    """Select-based entiteiten voor setpoints (indien nodig)."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_setpoints")},
            "name": "Set points",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }


#
# ================== FILTRATIE MODUS ==================
#
class VistapoolFiltrationModeSelect(FiltrationSelectBase):
    """
    Kies filtratiemodus: manual (0), auto (1), smart (3).
    UI-opties: 'manual', 'auto', 'smart'.
    """

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtratie Modus"
        self._attr_unique_id = f"{coordinator.api._pool_id}_filtration_mode"
        self._attr_options = list(FILTRATION_MODE_MAP.keys())  # ["manual", "auto", "smart"]

    @property
    def current_option(self):
        data = self.coordinator.data
        mode_val = data.get("filtration", {}).get("mode", 0)
        return FILTRATION_MODE_NAMES.get(mode_val, "manual")

    async def async_select_option(self, option: str):
        mode_val = FILTRATION_MODE_MAP.get(option, 0)
        # Je kunt een guard toevoegen als je bepaalde transitions wil blokkeren
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


#
# ================== BACKWASH MODUS ==================
#
class VistapoolBackwashModeSelect(FiltrationSelectBase):
    """
    Kies backwash mode: manual(0), automatic(1).
    UI-opties: 'manual', 'automatic'.
    """

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Modus"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_mode"
        self._attr_options = list(BACKWASH_MODE_MAP.keys())  # ["manual", "automatic"]

    @property
    def current_option(self):
        data = self.coordinator.data
        mode_val = data.get("backwash", {}).get("mode", 0)
        return BACKWASH_MODE_NAMES.get(mode_val, "manual")

    async def async_select_option(self, option: str):
        mode_val = BACKWASH_MODE_MAP.get(option, 0)
        changes = {
            "backwash": {
                "mode": mode_val
            }
        }
        # Mogelijk guard: check of manual/auto past bij scenario?
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()
