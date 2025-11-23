"""Select platform voor Vistapool - COMPLETE versie."""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    get_device_info,
    FILTRATION_MODE_MAP,
    FILTRATION_MODE_NAMES,
    BACKWASH_MODE_MAP,
    BACKWASH_MODE_NAMES,
    PUMP_SPEED_MAP,
    PUMP_SPEED_NAMES,
    BACKWASH_FREQ_MAP,
    BACKWASH_FREQ_NAMES,
)
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
    """Set up ALLE Vistapool selects."""
    coordinator: VistapoolDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    selects = [
        # ========== FILTRATIE ==========
        VistapoolSelect(
            coordinator=coordinator,
            name="Filtratie Modus",
            key="filtration_mode",
            device_type="filtratie",
            data_path=["filtration", "mode"],
            command_path={"filtration": {"mode": None}},
            options_map=FILTRATION_MODE_MAP,
            names_map=FILTRATION_MODE_NAMES,
            icon="mdi:cog",
        ),
        VistapoolSelect(
            coordinator=coordinator,
            name="Pomp Snelheid (Manueel)",
            key="pump_speed_manual",
            device_type="filtratie",
            data_path=["filtration", "manVel"],
            command_path={"filtration": {"manVel": None}},
            options_map=PUMP_SPEED_MAP,
            names_map=PUMP_SPEED_NAMES,
            icon="mdi:speedometer",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) == 0,
        ),
        VistapoolSelect(
            coordinator=coordinator,
            name="Pomp Snelheid Interval 1",
            key="pump_speed_timer1",
            device_type="filtratie",
            data_path=["filtration", "timerVel1"],
            command_path={"filtration": {"timerVel1": None}},
            options_map=PUMP_SPEED_MAP,
            names_map=PUMP_SPEED_NAMES,
            icon="mdi:speedometer",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolSelect(
            coordinator=coordinator,
            name="Pomp Snelheid Interval 2",
            key="pump_speed_timer2",
            device_type="filtratie",
            data_path=["filtration", "timerVel2"],
            command_path={"filtration": {"timerVel2": None}},
            options_map=PUMP_SPEED_MAP,
            names_map=PUMP_SPEED_NAMES,
            icon="mdi:speedometer",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolSelect(
            coordinator=coordinator,
            name="Pomp Snelheid Interval 3",
            key="pump_speed_timer3",
            device_type="filtratie",
            data_path=["filtration", "timerVel3"],
            command_path={"filtration": {"timerVel3": None}},
            options_map=PUMP_SPEED_MAP,
            names_map=PUMP_SPEED_NAMES,
            icon="mdi:speedometer",
            available_check=lambda data: data.get("filtration", {}).get("mode", 0) in [1, 3],
        ),
        VistapoolSelect(
            coordinator=coordinator,
            name="Pomp Type",
            key="pump_type",
            device_type="filtratie",
            data_path=["filtration", "pumpType"],
            command_path={"filtration": {"pumpType": None}},
            options_map={"Enkel-snelheid": 0, "Variabel": 1},
            names_map={0: "Enkel-snelheid", 1: "Variabel"},
            icon="mdi:pump",
        ),
        
        # ========== BACKWASH ==========
        VistapoolSelect(
            coordinator=coordinator,
            name="Backwash Modus",
            key="backwash_mode",
            device_type="filtratie",
            data_path=["backwash", "mode"],
            command_path={"backwash": {"mode": None}},
            options_map=BACKWASH_MODE_MAP,
            names_map=BACKWASH_MODE_NAMES,
            icon="mdi:washing-machine",
        ),
        VistapoolSelect(
            coordinator=coordinator,
            name="Backwash Frequentie",
            key="backwash_frequency_select",
            device_type="filtratie",
            data_path=["backwash", "frequency"],
            command_path={"backwash": {"frequency": None}},
            options_map=BACKWASH_FREQ_MAP,
            names_map=BACKWASH_FREQ_NAMES,
            icon="mdi:calendar-clock",
            available_check=lambda data: data.get("backwash", {}).get("mode", 0) == 1,
        ),
        
        # ========== MODULES (pH type) ==========
        VistapoolSelect(
            coordinator=coordinator,
            name="pH Dosering Type",
            key="ph_type",
            device_type="setpoints",
            data_path=["modules", "ph", "type"],
            command_path={"modules": {"ph": {"type": None}}},
            options_map={"ACID": "ACID", "BASE": "BASE"},
            names_map={"ACID": "ACID", "BASE": "BASE"},
            icon="mdi:ph",
        ),
    ]

    async_add_entities(selects)


class VistapoolSelect(CoordinatorEntity, SelectEntity):
    """Generieke Vistapool select."""

    def __init__(
        self,
        coordinator: VistapoolDataUpdateCoordinator,
        name: str,
        key: str,
        device_type: str,
        data_path: list[str],
        command_path: Dict[str, Any],
        options_map: Dict[str, Any],
        names_map: Dict[Any, str],
        icon: str = "mdi:format-list-bulleted",
        available_check: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> None:
        """Initialiseer de select."""
        super().__init__(coordinator)
        
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.api._pool_id}_{key}"
        self._attr_icon = icon
        self._attr_options = list(options_map.keys())
        
        self._device_type = device_type
        self._data_path = data_path
        self._command_path = command_path
        self._options_map = options_map
        self._names_map = names_map
        self._available_check = available_check

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device info."""
        return get_device_info(self.coordinator.api._pool_id, self._device_type)

    @property
    def current_option(self) -> Optional[str]:
        """Return de huidige optie."""
        value = get_nested_value(self.coordinator.data, self._data_path)
        
        if value is None:
            return None
        
        # Convert string naar int indien nodig
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                # Als het een string moet blijven (zoals "ACID")
                return self._names_map.get(value)
        
        return self._names_map.get(value)

    @property
    def available(self) -> bool:
        """Return True als de entity beschikbaar is."""
        if not super().available:
            return False
            
        if self._available_check:
            return self._available_check(self.coordinator.data)
            
        return True

    async def async_select_option(self, option: str) -> None:
        """Selecteer een nieuwe optie."""
        # Haal de API waarde op
        api_value = self._options_map.get(option)
        
        if api_value is None:
            _LOGGER.error("Ongeldige optie %s voor %s", option, self._attr_name)
            return
        
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
        
        _LOGGER.debug("Selecteer %s voor %s", option, self._attr_name)
        
        try:
            await self.coordinator.async_send_pool_command("WRP", changes)
        except Exception as err:
            _LOGGER.error("Fout bij selecteren %s: %s", self._attr_name, err)
