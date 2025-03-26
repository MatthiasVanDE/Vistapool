import logging
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    numbers = []

    numbers.append(VistapoolPhSetpointNumber(coordinator))
    numbers.append(VistapoolRedoxSetpointNumber(coordinator))
    numbers.append(VistapoolWaterTempSetpointNumber(coordinator))

    async_add_entities(numbers)

class VistapoolPhSetpointNumber(CoordinatorEntity, NumberEntity):
    """pH-doelwaarde (modules.ph.status.high_value). Typisch 6.0 tot 8.0."""

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
        val_str = data.get("modules", {}).get("ph", {}).get("status", {}).get("high_value", "700")
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


class VistapoolRedoxSetpointNumber(CoordinatorEntity, NumberEntity):
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
        val_str = data.get("modules", {}).get("rx", {}).get("status", {}).get("value", "650")
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


class VistapoolWaterTempSetpointNumber(CoordinatorEntity, NumberEntity):
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
        changes = {
            "filtration": {
                "intel": {
                    "temp": int(value)
                }
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()
