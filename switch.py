"""Switch platform voor Vistapool - COMPLETE versie."""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, get_device_info
from .coordinator import VistapoolDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


def get_nested_value(data: Dict[str, Any], path: list[str], default: Any = None) -> Any:
    """Haal een geneste waarde op uit een dictionary."""
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def set_nested_value(data: Dict[str, Any], path: list[str], value: Any) -> Dict[str, Any]:
    """Zet een geneste waarde in een dictionary."""
    import copy
    result = copy.deepcopy(data)
    
    current = result
    for key in path[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[path[-1]] = value
    
    return result


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ALLE Vistapool switches."""
    coordinator: VistapoolDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    switches = [
        # ========== FILTRATIE ==========
        VistapoolSwitch(
            coordinator=coordinator,
            name="Zwembadpomp",
            key="pump",
            device_type="filtratie",
            data_path=["filtration", "status"],
            command_path={"filtration": {"status": None}},
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Zwembadlicht",
            key="light",
            device_type="filtratie",
            data_path=["light", "status"],
            command_path={"light": {"status": None}},
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Licht Automatische Modus",
            key="light_auto_mode",
            device_type="filtratie",
            data_path=["light", "mode"],
            command_path={"light": {"mode": None}},
            icon="mdi:lightbulb-auto",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Backwash Actief",
            key="backwash_status",
            device_type="filtratie",
            data_path=["backwash", "status"],
            command_path={"backwash": {"status": None}},
            icon="mdi:washing-machine",
        ),
        
        # ========== HYDROLYSE ==========
        VistapoolSwitch(
            coordinator=coordinator,
            name="Chloorshock",
            key="chlor_shock",
            device_type="hydrolyse",
            data_path=["hidro", "cloration_enabled"],
            command_path={"hidro": {"cloration_enabled": None}},
            available_check=lambda data: data.get("hidro", {}).get("disable", 1) == 0,
            icon="mdi:water-plus",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Hydrolyse Ingeschakeld",
            key="hydro_enabled",
            device_type="hydrolyse",
            data_path=["hidro", "disable"],
            command_path={"hidro": {"disable": None}},
            inverted=True,  # disable=0 betekent enabled
            icon="mdi:water-pump",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Hydrolyse Temperatuur Sensor",
            key="hydro_temp_enabled",
            device_type="hydrolyse",
            data_path=["hidro", "temperature_enabled"],
            command_path={"hidro": {"temperature_enabled": None}},
            icon="mdi:thermometer",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Hydrolyse Dekzeil Detectie",
            key="hydro_cover_enabled",
            device_type="hydrolyse",
            data_path=["hidro", "cover_enabled"],
            command_path={"hidro": {"cover_enabled": None}},
            icon="mdi:shield-check",
        ),
        
        # ========== RELAYS ==========
        VistapoolSwitch(
            coordinator=coordinator,
            name="Relay 1",
            key="relay1_onoff",
            device_type="relays",
            data_path=["relays", "relay1", "info", "onoff"],
            command_path={"relays": {"relay1": {"info": {"onoff": None}}}},
            icon="mdi:electric-switch",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Relay 2",
            key="relay2_onoff",
            device_type="relays",
            data_path=["relays", "relay2", "info", "onoff"],
            command_path={"relays": {"relay2": {"info": {"onoff": None}}}},
            icon="mdi:electric-switch",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Relay 3",
            key="relay3_onoff",
            device_type="relays",
            data_path=["relays", "relay3", "info", "onoff"],
            command_path={"relays": {"relay3": {"info": {"onoff": None}}}},
            icon="mdi:electric-switch",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Relay 4",
            key="relay4_onoff",
            device_type="relays",
            data_path=["relays", "relay4", "info", "onoff"],
            command_path={"relays": {"relay4": {"info": {"onoff": None}}}},
            icon="mdi:electric-switch",
        ),
        VistapoolSwitch(
            coordinator=coordinator,
            name="Verwarming",
            key="heating_status",
            device_type="filtratie",
            data_path=["relays", "filtration", "heating", "status"],
            command_path={"relays": {"filtration": {"heating": {"status": None}}}},
            icon="mdi:radiator",
        ),
        
        # ========== FILTRATION ADVANCED ==========
        VistapoolSwitch(
            coordinator=coordinator,
            name="Smart Mode Vorstbeveiliging",
            key="smart_freeze",
            device_type="filtratie",
            data_path=["filtration", "smart", "freeze"],
            command_path={"filtration": {"smart": {"freeze": None}}},
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) == 3,
            icon="mdi:snowflake-alert",
        ),
    ]

    async_add_entities(switches)


class VistapoolSwitchBase(CoordinatorEntity, SwitchEntity):
    """Base class voor Vistapool switches."""

    def __init__(
        self,
        coordinator: VistapoolDataUpdateCoordinator,
        name: str,
        key: str,
        device_type: str,
        icon: str = "mdi:toggle-switch",
    ) -> None:
        """Initialiseer de switch."""
        super().__init__(coordinator)
        
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.api._pool_id}_{key}"
        self._attr_icon = icon
        self._device_type = device_type
        self._key = key

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device info."""
        return get_device_info(self.coordinator.api._pool_id, self._device_type)


class VistapoolSwitch(VistapoolSwitchBase):
    """Generieke Vistapool switch."""

    def __init__(
        self,
        coordinator: VistapoolDataUpdateCoordinator,
        name: str,
        key: str,
        device_type: str,
        data_path: list[str],
        command_path: Dict[str, Any],
        available_check: Optional[Callable[[Dict[str, Any]], bool]] = None,
        inverted: bool = False,
        icon: str = "mdi:toggle-switch",
    ) -> None:
        """
        Initialiseer de switch.
        
        Args:
            inverted: Als True, wordt 0=aan en 1=uit (voor 'disable' velden)
        """
        super().__init__(coordinator, name, key, device_type, icon)
        
        self._data_path = data_path
        self._command_path = command_path
        self._available_check = available_check
        self._inverted = inverted

    @property
    def is_on(self) -> bool:
        """Return True als de switch aan staat."""
        value = get_nested_value(self.coordinator.data, self._data_path, 0)
        
        if self._inverted:
            return value == 0  # disable=0 betekent enabled
        return value == 1

    @property
    def available(self) -> bool:
        """Return True als de entity beschikbaar is."""
        if not super().available:
            return False
            
        if self._available_check:
            return self._available_check(self.coordinator.data)
            
        return True

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Zet de switch aan."""
        if self._available_check and not self._available_check(self.coordinator.data):
            _LOGGER.warning("Kan %s niet inschakelen: niet beschikbaar", self._attr_name)
            return

        # Bij inverted switches: aan = 0, anders 1
        value = 0 if self._inverted else 1
        changes = set_nested_value(self._command_path, self._data_path, value)
        
        _LOGGER.debug("Zet %s aan met changes: %s", self._attr_name, changes)
        
        try:
            await self.coordinator.async_send_pool_command("WRP", changes)
        except Exception as err:
            _LOGGER.error("Fout bij inschakelen %s: %s", self._attr_name, err)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Zet de switch uit."""
        # Bij inverted switches: uit = 1, anders 0
        value = 1 if self._inverted else 0
        changes = set_nested_value(self._command_path, self._data_path, value)
        
        _LOGGER.debug("Zet %s uit met changes: %s", self._attr_name, changes)
        
        try:
            await self.coordinator.async_send_pool_command("WRP", changes)
        except Exception as err:
            _LOGGER.error("Fout bij uitschakelen %s: %s", self._attr_name, err)
