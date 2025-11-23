"""Helper functions en base classes voor Vistapool sensors."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    get_device_info,
    FILTRATION_MODE_NAMES,
    BACKWASH_MODE_NAMES,
    FILTRATION_STATUS_MAP,
    BACKWASH_STATUS_MAP,
    TRUE_FALSE_NAMES,
)
from .coordinator import VistapoolDataUpdateCoordinator


def get_nested_value(data: Dict[str, Any], path: list[str], default: Any = None) -> Any:
    """Haal een geneste waarde op uit een dictionary."""
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def intervalTime(value: int) -> str:
    """Convert seconden naar HH:MM:SS formaat."""
    if value is None:
        return "00:00:00"
    return datetime.fromtimestamp(value, tz=timezone.utc).strftime("%H:%M:%S")


class VistapoolSensorBase(CoordinatorEntity, SensorEntity):
    """Base class voor Vistapool sensors."""

    def __init__(
        self,
        coordinator: VistapoolDataUpdateCoordinator,
        name: str,
        key: str,
        device_type: str,
        icon: str = "mdi:information",
    ) -> None:
        """Initialiseer de sensor."""
        super().__init__(coordinator)
        
        self._attr_name = name
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_{key}"
        self._attr_icon = icon
        self._device_type = device_type

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device info."""
        return get_device_info(self.coordinator.api._pool_id, self._device_type)


class VistapoolSensor(VistapoolSensorBase):
    """
    Generieke Vistapool sensor.
    
    Ondersteunt verschillende data paths, value transformations en mappings.
    """

    def __init__(
        self,
        coordinator: VistapoolDataUpdateCoordinator,
        name: str,
        key: str,
        device_type: str,
        data_path: list[str],
        icon: str = "mdi:information",
        unit: Optional[str] = None,
        device_class: Optional[SensorDeviceClass] = None,
        value_map: Optional[Dict[Any, str]] = None,
        value_transform: Optional[Callable[[Any], Any]] = None,
        available_check: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> None:
        """
        Initialiseer de sensor.
        
        Args:
            coordinator: De data coordinator
            name: Weergave naam
            key: Unieke key
            device_type: Type apparaat
            data_path: Pad naar waarde in data dict
            icon: MDI icon
            unit: Meeteenheid
            device_class: Home Assistant device class
            value_map: Mapping van waarde naar leesbare string
            value_transform: Functie om waarde te transformeren
            available_check: Functie om beschikbaarheid te checken
        """
        super().__init__(coordinator, name, key, device_type, icon)
        
        self._data_path = data_path
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._value_map = value_map
        self._value_transform = value_transform
        self._available_check = available_check

    @property
    def native_value(self) -> Any:
        """Return de native waarde."""
        value = get_nested_value(self.coordinator.data, self._data_path)
        
        if value is None:
            return None
        
        # Transform de waarde indien nodig
        if self._value_transform:
            value = self._value_transform(value)
        
        # Map naar leesbare string indien nodig
        if self._value_map:
            return self._value_map.get(value, f"unknown ({value})")
        
        return value

    @property
    def available(self) -> bool:
        """Return True als de entity beschikbaar is."""
        if not super().available:
            return False
            
        if self._available_check:
            return self._available_check(self.coordinator.data)
            
        return True


# Veelgebruikte value transformers
def timestamp_to_datetime(value: int) -> datetime:
    """Convert UNIX timestamp naar datetime object."""
    if value is None:
        return None
    return datetime.fromtimestamp(value)


def seconds_to_time(value: int) -> str:
    """Convert seconden sinds middernacht naar HH:MM:SS."""
    if value is None:
        return "00:00:00"
    return intervalTime(value)


def string_to_float(value: str) -> Optional[float]:
    """Convert string naar float, return None bij fout."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def ph_value_to_float(value: str) -> Optional[float]:
    """Convert pH string waarde naar float (710 -> 7.10)."""
    if value is None:
        return None
    try:
        return float(value) / 100.0
    except (ValueError, TypeError):
        return None


# Status mappings die nog ontbreken in const.py
FILTRATION_STATUS_MAP = {
    "Off": 0,
    "On": 1,
}

BACKWASH_STATUS_MAP = {
    "Off": 0,
    "On": 1,
}

FILTRATION_STATUS_NAMES = {v: k for k, v in FILTRATION_STATUS_MAP.items()}
BACKWASH_STATUS_NAMES = {v: k for k, v in BACKWASH_STATUS_MAP.items()}
