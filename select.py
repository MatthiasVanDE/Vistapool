import logging
import copy
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

#
# =================== Mapping Tables ===================
#
FILTRATION_MODE_MAP = {
    "Manual": 0,
    "Auto": 1,
    "Smart": 3
}
FILTRATION_MODE_NAMES = {v: k for k, v in FILTRATION_MODE_MAP.items()}

BACKWASH_MODE_MAP = {
    "Manual": 0,
    "Automatic": 1
}
BACKWASH_MODE_NAMES = {v: k for k, v in BACKWASH_MODE_MAP.items()}

#
# Pomp-snelheid: "langzaam"=0, "medium"=1, "hoog"=2 (voor filtration.manVel)
#
PUMP_SPEED_MAP = {
    "Slow": 0,
    "Medium": 1,
    "High": 2
}
PUMP_SPEED_NAMES = {v: k for k, v in PUMP_SPEED_MAP.items()}

#
# Backwash-frequentie:
#   "Elke dag" => 1440
#   "Elke twee dagen" => 2880
#   ...
#   "Elke vier weken" => 40320
# etc.
#
BACKWASH_FREQ_MAP = {
    "Elke dag": 1440,
    "Elke twee dagen": 2880,
    "Elke drie dagen": 4320,
    "Elke vier dagen": 5760,
    "Elke vijf dagen": 7200,
    "Elke week": 10080,
    "Elke twee weken": 20160,
    "Elke drie weken": 30240,
    "Elke vier weken": 40320
}
BACKWASH_FREQ_NAMES = {v: k for k, v in BACKWASH_FREQ_MAP.items()}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up all select entities for this integration."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    selects = []

    #
    # ========== FILTRATIE SELECTS ==========
    #
    selects.append(VistapoolFiltrationModeSelect(coordinator))
    selects.append(VistapoolPumpSpeedSelect(coordinator))  # pomp-snelheid

    #
    # ========== BACKWASH SELECTS ==========
    #
    selects.append(VistapoolBackwashModeSelect(coordinator))
    selects.append(VistapoolBackwashFrequencySelect(coordinator))  # backwash-frequentie

    async_add_entities(selects)


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
        """Lees de hele filtration-subdict, overschrijf 'mode', en stuur alles."""
        mode_val = FILTRATION_MODE_MAP.get(option, 0)
        filtration_data = copy.deepcopy(self.coordinator.data.get("filtration", {}))
        filtration_data["mode"] = mode_val

        changes = {
            "filtration": filtration_data
        }

        _LOGGER.debug("Setting filtration mode -> %s (%s). Full 'filtration':\n%s",
                      option, mode_val, changes)

        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()

#
# ================== POMP-SNELHEID ==================
#
class VistapoolPumpSpeedSelect(FiltrationSelectBase):
    """
    Kies pomp-snelheid: 'langzaam'(0), 'medium'(1), 'hoog'(2).
    Dit gaat naar 'filtration.manVel' in de JSON.
    """

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Pomp Snelheid"
        self._attr_unique_id = f"{coordinator.api._pool_id}_pump_speed"
        self._attr_options = list(PUMP_SPEED_MAP.keys())  # ["langzaam", "medium", "hoog"]

    @property
    def current_option(self):
        data = self.coordinator.data
        manvel_val = data.get("filtration", {}).get("manVel", 0)
        return PUMP_SPEED_NAMES.get(manvel_val, "langzaam")

    async def async_select_option(self, option: str):
        """Lees de hele filtration-subdict, overschrijf manVel, en stuur alles."""
        speed_val = PUMP_SPEED_MAP.get(option, 0)
        filtration_data = copy.deepcopy(self.coordinator.data.get("filtration", {}))
        filtration_data["manVel"] = speed_val

        changes = {
            "filtration": filtration_data
        }

        _LOGGER.debug("Setting pump speed -> %s (%s). Full 'filtration':\n%s",
                      option, speed_val, changes)

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
        """Lees de hele backwash-subdict, overschrijf 'mode', en stuur alles."""
        mode_val = BACKWASH_MODE_MAP.get(option, 0)
        backwash_data = copy.deepcopy(self.coordinator.data.get("backwash", {}))
        backwash_data["mode"] = mode_val

        changes = {
            "backwash": backwash_data
        }

        _LOGGER.debug("Setting backwash mode -> %s (%s). Full 'backwash':\n%s",
                      option, mode_val, changes)

        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


#
# ================== BACKWASH FREQUENTIE ==================
#
class VistapoolBackwashFrequencySelect(FiltrationSelectBase):
    """
    Kies backwash frequentie (in minuten) via BACKWASH_FREQ_MAP.
    UI-opties: 'Elke dag', 'Elke twee dagen', ..., 'Elke vier weken'.
    """

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Frequentie"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_frequency"
        self._attr_options = list(BACKWASH_FREQ_MAP.keys())

    @property
    def current_option(self):
        data = self.coordinator.data
        freq_val = data.get("backwash", {}).get("frequency", 40320)
        # Zoek de bijbehorende tekst, of None
        return BACKWASH_FREQ_NAMES.get(freq_val, None)

    async def async_select_option(self, option: str):
        """Lees de hele backwash-subdict, overschrijf 'frequency', en stuur alles."""
        freq_val = BACKWASH_FREQ_MAP.get(option, 40320)
        backwash_data = copy.deepcopy(self.coordinator.data.get("backwash", {}))
        backwash_data["frequency"] = freq_val

        changes = {
            "backwash": backwash_data
        }

        _LOGGER.debug("Setting backwash frequency -> %s (%s minutes). Full 'backwash':\n%s",
                      option, freq_val, changes)

        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()
