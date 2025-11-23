"""Number platform voor Vistapool - COMPLETE versie."""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

from homeassistant.components.number import NumberEntity, NumberMode
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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ALLE Vistapool numbers."""
    coordinator: VistapoolDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    numbers = [
        # ========== SET POINTS ==========
        VistapoolNumber(
            coordinator=coordinator,
            name="pH Setpoint Hoog",
            key="ph_setpoint_high",
            device_type="setpoints",
            data_path=["modules", "ph", "status", "high_value"],
            command_path={"modules": {"ph": {"status": {"high_value": None}}}},
            min_value=6.0,
            max_value=8.5,
            step=0.01,
            multiplier=100,  # 710 -> 7.10
            mode=NumberMode.BOX,
            icon="mdi:ph",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="pH Setpoint Laag",
            key="ph_setpoint_low",
            device_type="setpoints",
            data_path=["modules", "ph", "status", "low_value"],
            command_path={"modules": {"ph": {"status": {"low_value": None}}}},
            min_value=6.0,
            max_value=8.5,
            step=0.01,
            multiplier=100,
            mode=NumberMode.BOX,
            icon="mdi:ph",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Redox Setpoint",
            key="redox_setpoint",
            device_type="setpoints",
            data_path=["modules", "rx", "status", "value"],
            command_path={"modules": {"rx": {"status": {"value": None}}}},
            min_value=300,
            max_value=900,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:flash",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Chloor Setpoint",
            key="cl_setpoint",
            device_type="setpoints",
            data_path=["modules", "cl", "status", "value"],
            command_path={"modules": {"cl": {"status": {"value": None}}}},
            min_value=0,
            max_value=300,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:water-percent",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="CD Setpoint",
            key="cd_setpoint",
            device_type="setpoints",
            data_path=["modules", "cd", "status", "value"],
            command_path={"modules": {"cd": {"status": {"value": None}}}},
            min_value=0,
            max_value=10000,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:water-circle",
        ),
        
        # ========== HYDROLYSE ==========
        VistapoolNumber(
            coordinator=coordinator,
            name="Hydrolyse Level",
            key="hydrolyse_level",
            device_type="hydrolyse",
            data_path=["hidro", "level"],
            command_path={"hidro": {"level": None}},
            min_value=0,
            max_value=100,
            step=1,
            multiplier=10,  # UI: 0-100, API: 0-1000
            mode=NumberMode.SLIDER,
            icon="mdi:gauge",
            available_check=lambda data: data.get("hidro", {}).get("disable", 1) == 0,
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Hydrolyse Reductie",
            key="hydrolyse_reduction",
            device_type="hydrolyse",
            data_path=["hidro", "reduction"],
            command_path={"hidro": {"reduction": None}},
            min_value=0,
            max_value=100,
            step=1,
            mode=NumberMode.SLIDER,
            icon="mdi:percent",
            available_check=lambda data: data.get("hidro", {}).get("cover_enabled", 0) == 1,
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Hydrolyse Max Toegestane Waarde",
            key="hydrolyse_max_allowed",
            device_type="hydrolyse",
            data_path=["hidro", "maxAllowedValue"],
            command_path={"hidro": {"maxAllowedValue": None}},
            min_value=0,
            max_value=1000,
            step=10,
            mode=NumberMode.BOX,
            icon="mdi:gauge-full",
        ),
        
        # ========== FILTRATIE ==========
        VistapoolNumber(
            coordinator=coordinator,
            name="Watertemperatuur Setpoint",
            key="water_temp_setpoint",
            device_type="filtratie",
            data_path=["filtration", "intel", "temp"],
            command_path={"filtration": {"intel": {"temp": None}}},
            min_value=0,
            max_value=40,
            step=0.5,
            mode=NumberMode.BOX,
            icon="mdi:thermometer",
            unit="°C",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Verwarming Temperatuur",
            key="heating_temp",
            device_type="filtratie",
            data_path=["filtration", "heating", "temp"],
            command_path={"filtration": {"heating": {"temp": None}}},
            min_value=0,
            max_value=40,
            step=0.5,
            mode=NumberMode.BOX,
            icon="mdi:radiator",
            unit="°C",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Verwarming Max Temperatuur",
            key="heating_temp_hi",
            device_type="filtratie",
            data_path=["filtration", "heating", "tempHi"],
            command_path={"filtration": {"heating": {"tempHi": None}}},
            min_value=0,
            max_value=45,
            step=0.5,
            mode=NumberMode.BOX,
            icon="mdi:thermometer-high",
            unit="°C",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Smart Mode Min Temperatuur",
            key="smart_temp_min",
            device_type="filtratie",
            data_path=["filtration", "smart", "tempMin"],
            command_path={"filtration": {"smart": {"tempMin": None}}},
            min_value=0,
            max_value=30,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:thermometer-low",
            unit="°C",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) == 3,
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Smart Mode Max Temperatuur",
            key="smart_temp_high",
            device_type="filtratie",
            data_path=["filtration", "smart", "tempHigh"],
            command_path={"filtration": {"smart": {"tempHigh": None}}},
            min_value=15,
            max_value=40,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:thermometer-high",
            unit="°C",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) == 3,
        ),
        
        # ========== FILTRATIE INTERVALS (seconden sinds middernacht) ==========
        VistapoolNumber(
            coordinator=coordinator,
            name="Interval 1 Start",
            key="interval1_from",
            device_type="filtratie",
            data_path=["filtration", "interval1", "from"],
            command_path={"filtration": {"interval1": {"from": None}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-start",
            unit="sec",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Interval 1 Einde",
            key="interval1_to",
            device_type="filtratie",
            data_path=["filtration", "interval1", "to"],
            command_path={"filtration": {"interval1": {"to": None}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-end",
            unit="sec",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Interval 2 Start",
            key="interval2_from",
            device_type="filtratie",
            data_path=["filtration", "interval2", "from"],
            command_path={"filtration": {"interval2": {"from": None}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-start",
            unit="sec",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Interval 2 Einde",
            key="interval2_to",
            device_type="filtratie",
            data_path=["filtration", "interval2", "to"],
            command_path={"filtration": {"interval2": {"to": None}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-end",
            unit="sec",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Interval 3 Start",
            key="interval3_from",
            device_type="filtratie",
            data_path=["filtration", "interval3", "from"],
            command_path={"filtration": {"interval3": {"from": None}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-start",
            unit="sec",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Interval 3 Einde",
            key="interval3_to",
            device_type="filtratie",
            data_path=["filtration", "interval3", "to"],
            command_path={"filtration": {"interval3": {"to": None}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-end",
            unit="sec",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        
        # ========== BACKWASH ==========
        VistapoolNumber(
            coordinator=coordinator,
            name="Backwash Interval",
            key="backwash_interval",
            device_type="filtratie",
            data_path=["backwash", "interval"],
            command_path={"backwash": {"interval": None}},
            min_value=1,
            max_value=1440,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:timer",
            unit="min",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Backwash Frequentie",
            key="backwash_frequency",
            device_type="filtratie",
            data_path=["backwash", "frequency"],
            command_path={"backwash": {"frequency": None}},
            min_value=1440,
            max_value=43200,
            step=1440,
            mode=NumberMode.BOX,
            icon="mdi:calendar-clock",
            unit="min",
            available_check=lambda data: data.get("backwash", {}).get("mode", 0) == 1,
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Backwash StartAt",
            key="backwash_startat",
            device_type="filtratie",
            data_path=["backwash", "startAt"],
            command_path={"backwash": {"startAt": None}},
            min_value=0,
            max_value=9999999999,
            step=3600,
            mode=NumberMode.BOX,
            icon="mdi:clock-start",
            unit="epoch",
            available_check=lambda data: data.get("backwash", {}).get("mode", 0) == 1,
        ),
        
        # ========== LIGHT ==========
        VistapoolNumber(
            coordinator=coordinator,
            name="Licht Start Tijd",
            key="light_from",
            device_type="filtratie",
            data_path=["light", "from"],
            command_path={"light": {"from": None}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-start",
            unit="sec",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Licht Eind Tijd",
            key="light_to",
            device_type="filtratie",
            data_path=["light", "to"],
            command_path={"light": {"to": None}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-end",
            unit="sec",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Licht Frequentie",
            key="light_freq",
            device_type="filtratie",
            data_path=["light", "freq"],
            command_path={"light": {"freq": None}},
            min_value=3600,
            max_value=604800,
            step=3600,
            mode=NumberMode.BOX,
            icon="mdi:clock-fast",
            unit="sec",
        ),
        
        # ========== RELAYS ==========
        # Relay 1
        VistapoolNumber(
            coordinator=coordinator,
            name="Relay 1 Vertraging",
            key="relay1_delay",
            device_type="relays",
            data_path=["relays", "relay1", "info", "delay"],
            command_path={"relays": {"relay1": {"info": {"delay": None}}}},
            min_value=0,
            max_value=3600,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:timer",
            unit="sec",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Relay 1 Start Tijd",
            key="relay1_from",
            device_type="relays",
            data_path=["relays", "relay1", "info", "from"],
            command_path={"relays": {"relay1": {"info": {"from": None}}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-start",
            unit="sec",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name="Relay 1 Eind Tijd",
            key="relay1_to",
            device_type="relays",
            data_path=["relays", "relay1", "info", "to"],
            command_path={"relays": {"relay1": {"info": {"to": None}}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-end",
            unit="sec",
        ),
        # Relay 2-4 (identiek aan Relay 1)
        *create_relay_numbers(coordinator, 2),
        *create_relay_numbers(coordinator, 3),
        *create_relay_numbers(coordinator, 4),
    ]

    async_add_entities(numbers)


def create_relay_numbers(coordinator, relay_num: int) -> list:
    """Helper om relay numbers te maken voor relay 2, 3, 4."""
    return [
        VistapoolNumber(
            coordinator=coordinator,
            name=f"Relay {relay_num} Vertraging",
            key=f"relay{relay_num}_delay",
            device_type="relays",
            data_path=["relays", f"relay{relay_num}", "info", "delay"],
            command_path={"relays": {f"relay{relay_num}": {"info": {"delay": None}}}},
            min_value=0,
            max_value=3600,
            step=1,
            mode=NumberMode.BOX,
            icon="mdi:timer",
            unit="sec",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name=f"Relay {relay_num} Start Tijd",
            key=f"relay{relay_num}_from",
            device_type="relays",
            data_path=["relays", f"relay{relay_num}", "info", "from"],
            command_path={"relays": {f"relay{relay_num}": {"info": {"from": None}}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-start",
            unit="sec",
        ),
        VistapoolNumber(
            coordinator=coordinator,
            name=f"Relay {relay_num} Eind Tijd",
            key=f"relay{relay_num}_to",
            device_type="relays",
            data_path=["relays", f"relay{relay_num}", "info", "to"],
            command_path={"relays": {f"relay{relay_num}": {"info": {"to": None}}}},
            min_value=0,
            max_value=86400,
            step=60,
            mode=NumberMode.BOX,
            icon="mdi:clock-end",
            unit="sec",
        ),
    ]


class VistapoolNumber(CoordinatorEntity, NumberEntity):
    """Generieke Vistapool number."""

    def __init__(
        self,
        coordinator: VistapoolDataUpdateCoordinator,
        name: str,
        key: str,
        device_type: str,
        data_path: list[str],
        command_path: Dict[str, Any],
        min_value: float,
        max_value: float,
        step: float,
        mode: NumberMode = NumberMode.AUTO,
        multiplier: float = 1.0,
        icon: str = "mdi:numeric",
        unit: Optional[str] = None,
        available_check: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> None:
        """Initialiseer de number."""
        super().__init__(coordinator)
        
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.api._pool_id}_{key}"
        self._attr_icon = icon
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_mode = mode
        self._attr_native_unit_of_measurement = unit
        
        self._device_type = device_type
        self._data_path = data_path
        self._command_path = command_path
        self._multiplier = multiplier
        self._available_check = available_check

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device info."""
        return get_device_info(self.coordinator.api._pool_id, self._device_type)

    @property
    def native_value(self) -> Optional[float]:
        """Return de huidige waarde."""
        value = get_nested_value(self.coordinator.data, self._data_path)
        
        if value is None:
            return None
            
        # Convert string naar float indien nodig
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return None
        
        # Apply multiplier (bijv. 710 / 100 = 7.10)
        return float(value) / self._multiplier

    @property
    def available(self) -> bool:
        """Return True als de entity beschikbaar is."""
        if not super().available:
            return False
            
        if self._available_check:
            return self._available_check(self.coordinator.data)
            
        return True

    async def async_set_native_value(self, value: float) -> None:
        """Set de nieuwe waarde."""
        # Apply multiplier (bijv. 7.10 * 100 = 710)
        api_value = int(round(value * self._multiplier))
        
        # Bouw nested command
        import copy
        changes = copy.deepcopy(self._command_path)
        
        # Zet de waarde op de juiste plek
        current = changes
        for key in self._data_path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[self._data_path[-1]] = api_value
        
        _LOGGER.debug("Set %s naar %s (API: %s)", self._attr_name, value, api_value)
        
        try:
            await self.coordinator.async_send_pool_command("WRP", changes)
        except Exception as err:
            _LOGGER.error("Fout bij instellen %s: %s", self._attr_name, err)
