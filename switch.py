import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up all switch entities for this integration."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    switches = []

    #
    # ============== FILTRATIE SWITCHES ==============
    #
    switches.append(VistapoolPumpSwitch(coordinator))
    switches.append(VistapoolLightSwitch(coordinator))

    #
    # ============== HYDROLYSE SWITCHES ==============
    #
    switches.append(VistapoolChlorShockSwitch(coordinator))

    #
    # ============== SET POINTS SWITCHES (if any) ====
    #
    # In je huidige use-case zijn er geen toggles bij "Set points",
    # maar hier zou je ze toevoegen als die ooit nodig zijn.

    async_add_entities(switches)


#
# --------------------------------------------------------------------------
# BASE CLASSES: 1) FiltrationSwitchBase, 2) HydrolyseSwitchBase, 3) SetPointsSwitchBase
# --------------------------------------------------------------------------
#

class FiltrationSwitchBase(CoordinatorEntity, SwitchEntity):
    """Alle 'Filtratie' gerelateerde switches onder hetzelfde device_info."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class HydrolyseSwitchBase(CoordinatorEntity, SwitchEntity):
    """Alle 'Hydrolyse' gerelateerde switches onder hetzelfde device_info."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_hydrolyse")},
            "name": "Hydrolyse",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class SetPointsSwitchBase(CoordinatorEntity, SwitchEntity):
    """Voor als er ooit 'Set points' toggles komen."""

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_setpoints")},
            "name": "Set points",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }


#
# ======================= FILTRATIE SWITCHES =======================
#

class VistapoolPumpSwitch(FiltrationSwitchBase):
    """Aan/uit via filtration.status (0=uit,1=aan)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembadpomp"
        self._attr_unique_id = f"{coordinator.api._pool_id}_pump"

    @property
    def is_on(self):
        data = self.coordinator.data
        status = data.get("filtration", {}).get("status", 0)
        return status == 1

    async def async_turn_on(self, **kwargs):
        # Guard: Filtratie modus moet MANUAL (0) zijn om direct ON/OFF te zetten?
        # Alleen als je dat wilt afdwingen. Anders laten we 'm gaan.
        changes = {
            "filtration": {
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


class VistapoolLightSwitch(FiltrationSwitchBase):
    """Aan/uit via light.status (0=uit,1=aan). Verdeel deze onder 'Filtratie'."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Zwembadlicht"
        self._attr_unique_id = f"{coordinator.api._pool_id}_light"

    @property
    def is_on(self):
        data = self.coordinator.data
        status = data.get("light", {}).get("status", 0)
        return status == 1

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


#
# ======================= HYDROLYSE SWITCHES =======================
#

class VistapoolChlorShockSwitch(HydrolyseSwitchBase):
    """Aan/uit via hidro.cloration_enabled (0=uit,1=aan)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Chloorshock"
        self._attr_unique_id = f"{coordinator.api._pool_id}_chlor_shock"

    @property
    def is_on(self):
        data = self.coordinator.data
        enabled = data.get("hidro", {}).get("cloration_enabled", 0)
        return enabled == 1

    @property
    def available(self):
        """Bijv. alleen tonen als 'disable=0'? Keuze."""
        hidro = self.coordinator.data.get("hidro", {})
        return (hidro.get("disable", 1) == 0)

    async def async_turn_on(self, **kwargs):
        # Guard: Hydrolyse niet disabled?
        hidro = self.coordinator.data.get("hidro", {})
        if hidro.get("disable", 1) == 1:
            _LOGGER.warning("Cannot enable chloorshock if hydrolyse is disabled.")
            return

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


#
# ============== SET POINTS SWITCHES (if needed) =================
#
# Currently you have no known toggles in the setpoints section (pH/rX).
# If needed, create them by inheriting from SetPointsSwitchBase.
#
