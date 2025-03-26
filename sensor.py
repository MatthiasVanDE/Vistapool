import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []
    sensors.append(VistapoolTemperatureSensor(coordinator))
    sensors.append(VistapoolPhSensor(coordinator))
    sensors.append(VistapoolRedoxSensor(coordinator))
    # eventueel meer sensoren...

    async_add_entities(sensors)

class VistapoolTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Toont de watertemperatuur (main.temperature)."""
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembadtemperatuur"
        self._attr_unique_id = f"{coordinator.api._pool_id}_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        data = self.coordinator.data
        # bijv. data["main"]["temperature"] = 14.7
        return data.get("main", {}).get("temperature", None)


class VistapoolPhSensor(CoordinatorEntity, SensorEntity):
    """Toont pH (modules.ph.current)."""
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembad pH"
        self._attr_unique_id = f"{coordinator.api._pool_id}_ph"

    @property
    def native_value(self):
        data = self.coordinator.data
        ph_str = data.get("modules", {}).get("ph", {}).get("current", "700")
        try:
            return round(float(ph_str) / 100.0, 2)
        except ValueError:
            return None


class VistapoolRedoxSensor(CoordinatorEntity, SensorEntity):
    """Toont Redox (modules.rx.current)."""
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembad Redox"
        self._attr_unique_id = f"{coordinator.api._pool_id}_redox"

    @property
    def native_value(self):
        data = self.coordinator.data
        rx_str = data.get("modules", {}).get("rx", {}).get("current", 0)
        try:
            return float(rx_str)
        except ValueError:
            return None
