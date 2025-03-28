import logging
import copy
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

#
# Hulpfuncties om HH:MM ←→ seconden te converteren
#

def hhmm_to_seconds(hhmm: str) -> int:
    """Parse 'HH:MM' naar integer seconden."""
    parts = hhmm.split(":")
    if len(parts) != 2:
        return 0
    h = int(parts[0])
    m = int(parts[1])
    return h * 3600 + m * 60


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up all number entities for this integration."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    numbers = []

    #
    # ================== SET POINTS ==================
    #
    numbers.append(VistapoolPhSetpointNumber(coordinator))
    numbers.append(VistapoolRedoxSetpointNumber(coordinator))

    #
    # ================== HYDROLYSE ===================
    #
    numbers.append(VistapoolHydrolyseLevelNumber(coordinator))
    numbers.append(VistapoolHydrolyseReductionNumber(coordinator))

    #
    # ================== FILTRATIE (incl. BACKWASH) ==
    #
    # - WaterTemp + Smart temps
    numbers.append(VistapoolWaterTempSetpointNumber(coordinator))
    numbers.append(VistapoolSmartTempMinNumber(coordinator))
    numbers.append(VistapoolSmartTempHighNumber(coordinator))

    # - All intervals (1..3)
    numbers.append(VistapoolFiltrationInterval1FromNumber(coordinator))
    numbers.append(VistapoolFiltrationInterval1ToNumber(coordinator))
    numbers.append(VistapoolFiltrationInterval2FromNumber(coordinator))
    numbers.append(VistapoolFiltrationInterval2ToNumber(coordinator))
    numbers.append(VistapoolFiltrationInterval3FromNumber(coordinator))
    numbers.append(VistapoolFiltrationInterval3ToNumber(coordinator))

    # - Backwash
    numbers.append(VistapoolBackwashIntervalNumber(coordinator))
    numbers.append(VistapoolBackwashFrequencyNumber(coordinator))
    numbers.append(VistapoolBackwashStartAtNumber(coordinator))

    async_add_entities(numbers)


#
# --------------------------------------------------------------------------
#  DEVICE BASE CLASSES
# --------------------------------------------------------------------------
#

class SetPointsNumberBase(CoordinatorEntity, NumberEntity):
    """Alle 'Set Points' getallen komen onder hetzelfde device_info."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_setpoints")},
            "name": "Set points",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class HydrolyseNumberBase(CoordinatorEntity, NumberEntity):
    """Alle 'Hydrolyse' getallen komen onder hetzelfde device_info."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_hydrolyse")},
            "name": "Hydrolyse",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class FiltrationNumberBase(CoordinatorEntity, NumberEntity):
    """Alle 'Filtratie' (en Backwash) getallen komen onder hetzelfde device_info."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }


#
# ========================== SET POINTS ==========================
#

class VistapoolPhSetpointNumber(SetPointsNumberBase):
    """pH-doelwaarde (modules.ph.status.high_value)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "pH Setpoint"
        self._attr_unique_id = f"{coordinator.api._pool_id}_ph_setpoint"
        self._attr_min_value = 6.0
        self._attr_max_value = 8.0
        self._attr_step = 0.01

    @property
    def native_value(self):
        data = self.coordinator.data
        val_str = (
            data.get("modules", {})
                .get("ph", {})
                .get("status", {})
                .get("high_value", "700")
        )
        try:
            return float(val_str) / 100.0
        except:
            return 7.0

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value * 100))
        changes = {
            "modules": {
                "ph": {
                    "status": {
                        "high_value": str(val_int)
                    }
                }
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolRedoxSetpointNumber(SetPointsNumberBase):
    """Redox-doelwaarde (modules.rx.status.value)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Redox Setpoint"
        self._attr_unique_id = f"{coordinator.api._pool_id}_redox_setpoint"
        self._attr_min_value = 300
        self._attr_max_value = 900
        self._attr_step = 1

    @property
    def native_value(self):
        data = self.coordinator.data
        val_str = (
            data.get("modules", {})
                .get("rx", {})
                .get("status", {})
                .get("value", "650")
        )
        try:
            return float(val_str)
        except:
            return 650

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        changes = {
            "modules": {
                "rx": {
                    "status": {
                        "value": str(val_int)
                    }
                }
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


#
# ========================== HYDROLYSE ==========================
#

class VistapoolHydrolyseLevelNumber(HydrolyseNumberBase):
    """Hydrolyse (hidro.level) UI range: 0..100, internal: 0..1000."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hydrolyse Level"
        self._attr_unique_id = f"{coordinator.api._pool_id}_hydrolyse_level"
        self._attr_min_value = 0
        self._attr_max_value = 100
        self._attr_step = 1

    @property
    def native_value(self):
        data = self.coordinator.data
        level = data.get("hidro", {}).get("level", 1000)
        return float(level) / 10.0

    async def async_set_native_value(self, value: float) -> None:
        hidro = self.coordinator.data.get("hidro", {})
        if hidro.get("disable", 1) == 1:
            _LOGGER.warning("Hydrolyse is disabled; ignoring level change.")
            return

        val_int = int(round(value * 10))
        changes = {
            "hidro": {
                "level": val_int
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolHydrolyseReductionNumber(HydrolyseNumberBase):
    """Hydrolyse (hidro.reduction) 0..100% (relevant if cover_enabled=1)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hydrolyse Reduction"
        self._attr_unique_id = f"{coordinator.api._pool_id}_hydrolyse_reduction"
        self._attr_min_value = 0
        self._attr_max_value = 100
        self._attr_step = 1

    @property
    def native_value(self):
        data = self.coordinator.data
        return float(data.get("hidro", {}).get("reduction", 10))

    @property
    def available(self):
        cover_enabled = self.coordinator.data.get("hidro", {}).get("cover_enabled", 0)
        return cover_enabled == 1

    async def async_set_native_value(self, value: float) -> None:
        hidro = self.coordinator.data.get("hidro", {})
        if hidro.get("cover_enabled", 0) != 1:
            _LOGGER.warning("Reduction only valid when cover_enabled=1.")
            return

        val_int = int(round(value))
        changes = {
            "hidro": {
                "reduction": val_int
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


#
# ========================== FILTRATIE (incl. BACKWASH) =========
#

class VistapoolWaterTempSetpointNumber(FiltrationNumberBase):
    """Gewenste watertemperatuur (filtration.intel.temp)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembadtemp Setpoint"
        self._attr_unique_id = f"{coordinator.api._pool_id}_water_temp_setpoint"
        self._attr_min_value = 0
        self._attr_max_value = 40
        self._attr_step = 1

    @property
    def native_value(self):
        data = self.coordinator.data
        val = data.get("filtration", {}).get("intel", {}).get("temp", 28)
        return float(val)

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        changes = {
            "filtration": {
                "intel": {
                    "temp": val_int
                }
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolSmartTempMinNumber(FiltrationNumberBase):
    """Smart modus min. temp (filtration.smart.tempMin)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Smart Temp Min"
        self._attr_unique_id = f"{coordinator.api._pool_id}_smart_temp_min"
        self._attr_min_value = 0
        self._attr_max_value = 40
        self._attr_step = 1

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {})
                .get("smart", {})
                .get("tempMin", 10)
        )

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode == 3

    async def async_set_native_value(self, value: float) -> None:
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode != 3:
            _LOGGER.warning("tempMin only relevant in SMART mode (3).")
            return

        val_int = int(round(value))
        changes = {
            "filtration": {
                "smart": {
                    "tempMin": val_int
                }
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolSmartTempHighNumber(FiltrationNumberBase):
    """Smart modus max. temp (filtration.smart.tempHigh)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Smart Temp Max"
        self._attr_unique_id = f"{coordinator.api._pool_id}_smart_temp_high"
        self._attr_min_value = 0
        self._attr_max_value = 40
        self._attr_step = 1

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {})
                .get("smart", {})
                .get("tempHigh", 25)
        )

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode == 3

    async def async_set_native_value(self, value: float) -> None:
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode != 3:
            _LOGGER.warning("tempHigh only relevant in SMART mode (3).")
            return

        val_int = int(round(value))
        changes = {
            "filtration": {
                "smart": {
                    "tempHigh": val_int
                }
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


#
#  Intervals 1..3 (from/to) – bewaard in seconden
#
class VistapoolFiltrationInterval1FromNumber(FiltrationNumberBase):
    """filtration.interval1.from in seconds (0..86400). Displayed as a plain integer in HA."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Interval1 From (sec)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_interval1_from"
        self._attr_min_value = 0
        self._attr_max_value = 86400
        self._attr_step = 60

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {})
                .get("interval1", {})
                .get("from", 0)
        )

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode in [1, 3]

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode not in [1, 3]:
            _LOGGER.warning("Interval1.from only relevant if mode=Auto(1) or Smart(3).")
            return

        # Kopieer de bestaande filtration.interval1
        base = copy.deepcopy(self.coordinator.data.get("filtration", {}).get("interval1", {}))
        base["from"] = val_int
        changes = {
            "filtration": {
                "interval1": base
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolFiltrationInterval1ToNumber(FiltrationNumberBase):
    """filtration.interval1.to in seconds (0..86400)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Interval1 To (sec)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_interval1_to"
        self._attr_min_value = 0
        self._attr_max_value = 86400
        self._attr_step = 60

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {})
                .get("interval1", {})
                .get("to", 0)
        )

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode in [1, 3]

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode not in [1, 3]:
            _LOGGER.warning("Interval1.to only relevant if mode=Auto(1) or Smart(3).")
            return

        base = copy.deepcopy(self.coordinator.data.get("filtration", {}).get("interval1", {}))
        base["to"] = val_int

        changes = {
            "filtration": {
                "interval1": base
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()

# Interval2From, Interval2To, Interval3From, Interval3To werken identiek, alleen index verschilt

class VistapoolFiltrationInterval2FromNumber(FiltrationNumberBase):
    """filtration.interval2.from in seconds (0..86400)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Interval2 From (sec)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_interval2_from"
        self._attr_min_value = 0
        self._attr_max_value = 86400
        self._attr_step = 60

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {}).get("interval2", {}).get("from", 0)
        )

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode in [1, 3]

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode not in [1, 3]:
            _LOGGER.warning("Interval2.from only relevant if mode=Auto(1) or Smart(3).")
            return

        base = copy.deepcopy(self.coordinator.data.get("filtration", {}).get("interval2", {}))
        base["from"] = val_int

        changes = {
            "filtration": {
                "interval2": base
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolFiltrationInterval2ToNumber(FiltrationNumberBase):
    """filtration.interval2.to in seconds (0..86400)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Interval2 To (sec)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_interval2_to"
        self._attr_min_value = 0
        self._attr_max_value = 86400
        self._attr_step = 60

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {}).get("interval2", {}).get("to", 0)
        )

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode in [1, 3]

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode not in [1, 3]:
            _LOGGER.warning("Interval2.to only relevant if mode=Auto(1) or Smart(3).")
            return

        base = copy.deepcopy(self.coordinator.data.get("filtration", {}).get("interval2", {}))
        base["to"] = val_int

        changes = {
            "filtration": {
                "interval2": base
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolFiltrationInterval3FromNumber(FiltrationNumberBase):
    """filtration.interval3.from in seconds (0..86400)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Interval3 From (sec)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_interval3_from"
        self._attr_min_value = 0
        self._attr_max_value = 86400
        self._attr_step = 60

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {}).get("interval3", {}).get("from", 0)
        )

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode in [1, 3]

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode not in [1, 3]:
            _LOGGER.warning("Interval3.from only relevant if mode=Auto(1) or Smart(3).")
            return

        base = copy.deepcopy(self.coordinator.data.get("filtration", {}).get("interval3", {}))
        base["from"] = val_int

        changes = {
            "filtration": {
                "interval3": base
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolFiltrationInterval3ToNumber(FiltrationNumberBase):
    """filtration.interval3.to in seconds (0..86400)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Interval3 To (sec)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_interval3_to"
        self._attr_min_value = 0
        self._attr_max_value = 86400
        self._attr_step = 60

    @property
    def available(self):
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        return mode in [1, 3]

    @property
    def native_value(self):
        return float(
            self.coordinator.data.get("filtration", {}).get("interval3", {}).get("to", 0)
        )

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        mode = self.coordinator.data.get("filtration", {}).get("mode", 0)
        if mode not in [1, 3]:
            _LOGGER.warning("Interval3.to only relevant if mode=Auto(1) or Smart(3).")
            return

        base = copy.deepcopy(self.coordinator.data.get("filtration", {}).get("interval3", {}))
        base["to"] = val_int

        changes = {
            "filtration": {
                "interval3": base
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


#
#  BACKWASH: also under Filtratie device
#
class VistapoolBackwashIntervalNumber(FiltrationNumberBase):
    """backwash.interval in minutes (both MANUAL & AUTO)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Interval (min)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_interval"
        self._attr_min_value = 1
        self._attr_max_value = 1440
        self._attr_step = 1

    @property
    def native_value(self):
        data = self.coordinator.data
        return float(data.get("backwash", {}).get("interval", 180))

    async def async_set_native_value(self, value: float) -> None:
        val_int = int(round(value))
        changes = {
            "backwash": {
                "interval": val_int
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolBackwashFrequencyNumber(FiltrationNumberBase):
    """backwash.frequency in minutes (AUTO only, e.g. 40320=4 weeks)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Frequency (min)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_frequency"
        self._attr_min_value = 1440
        self._attr_max_value = 999999
        self._attr_step = 60

    @property
    def native_value(self):
        data = self.coordinator.data
        return float(data.get("backwash", {}).get("frequency", 40320))

    @property
    def available(self):
        return self.coordinator.data.get("backwash", {}).get("mode", 0) == 1

    async def async_set_native_value(self, value: float) -> None:
        mode = self.coordinator.data.get("backwash", {}).get("mode", 0)
        if mode != 1:
            _LOGGER.warning("Backwash frequency only relevant if backwash.mode=1 (auto).")
            return

        val_int = int(round(value))
        changes = {
            "backwash": {
                "frequency": val_int
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolBackwashStartAtNumber(FiltrationNumberBase):
    """backwash.startAt in epoch seconds (AUTO mode)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash StartAt (epoch)"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_startAt"
        self._attr_min_value = 0
        self._attr_max_value = 9999999999
        self._attr_step = 60

    @property
    def native_value(self):
        data = self.coordinator.data
        return float(data.get("backwash", {}).get("startAt", 0))

    @property
    def available(self):
        return self.coordinator.data.get("backwash", {}).get("mode", 0) == 1

    async def async_set_native_value(self, value: float) -> None:
        mode = self.coordinator.data.get("backwash", {}).get("mode", 0)
        if mode != 1:
            _LOGGER.warning("Backwash startAt only relevant in backwash.mode=1 (auto).")
            return

        val_int = int(round(value))
        changes = {
            "backwash": {
                "startAt": val_int
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()
