import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    switches = []
    switches.append(VistapoolPumpSwitch(coordinator))
    switches.append(VistapoolLightSwitch(coordinator))
    switches.append(VistapoolChlorShockSwitch(coordinator))

    async_add_entities(switches)

class VistapoolPumpSwitch(CoordinatorEntity, SwitchEntity):
    """Aan/uit via filtration.status (0=uit,1=aan)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembadpomp"
        self._attr_unique_id = f"{coordinator.api._pool_id}_pump"

    @property
    def is_on(self):
        data = self.coordinator.data
        status = data.get("filtration", {}).get("status", 0)
        return (status == 1)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "pool_device")},
            "name": "Pool",
            "manufacturer": "Sugar Valley",
            "model": "Oxilife",
        }

    async def async_turn_on(self, **kwargs):
        changes = {
            "filtration": {
                "status": 1
            }
        }
        # Let op: via thread
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        changes = {
            "filtration": {
                "status": 0
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolLightSwitch(CoordinatorEntity, SwitchEntity):
    """Aan/uit via light.status (0=uit,1=aan)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembadlicht"
        self._attr_unique_id = f"{coordinator.api._pool_id}_light"

    @property
    def is_on(self):
        data = self.coordinator.data
        status = data.get("light", {}).get("status", 0)
        return (status == 1)

    async def async_turn_on(self, **kwargs):
        changes = {
            "light": {
                "status": 1
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        changes = {
            "light": {
                "status": 0
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()


class VistapoolChlorShockSwitch(CoordinatorEntity, SwitchEntity):
    """Aan/uit via hidro.cloration_enabled (0=uit,1=aan)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Chloorshock"
        self._attr_unique_id = f"{coordinator.api._pool_id}_chlor_shock"

    @property
    def is_on(self):
        data = self.coordinator.data
        enabled = data.get("hidro", {}).get("cloration_enabled", 0)
        return (enabled == 1)

    async def async_turn_on(self, **kwargs):
        changes = {
            "hidro": {
                "cloration_enabled": 1
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        changes = {
            "hidro": {
                "cloration_enabled": 0
            }
        }
        await self.hass.async_add_executor_job(
            self.coordinator.api.send_pool_command,
            "WRP",
            changes
        )
        await self.coordinator.async_request_refresh()
