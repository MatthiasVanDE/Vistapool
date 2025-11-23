"""Constanten voor de Vistapool integratie."""
from __future__ import annotations

# Domain
DOMAIN = "vistapool"

# Mapping tables voor enum waarden
FILTRATION_MODE_MAP = {
    "Manual": 0,
    "Auto": 1,
    "Smart": 3,
}

BACKWASH_MODE_MAP = {
    "Manual": 0,
    "Automatic": 1,
}

PUMP_SPEED_MAP = {
    "Slow": 0,
    "Medium": 1,
    "High": 2,
}

# Backwash frequenties in minuten
BACKWASH_FREQ_MAP = {
    "Elke dag": 1440,
    "Elke twee dagen": 2880,
    "Elke drie dagen": 4320,
    "Elke vier dagen": 5760,
    "Elke vijf dagen": 7200,
    "Elke week": 10080,
    "Elke twee weken": 20160,
    "Elke drie weken": 30240,
    "Elke vier weken": 40320,
}

# True/False mapping
TRUE_FALSE_MAP = {
    "False": 0,
    "True": 1,
}

# Reversed mappings (voor display)
FILTRATION_MODE_NAMES = {v: k for k, v in FILTRATION_MODE_MAP.items()}
BACKWASH_MODE_NAMES = {v: k for k, v in BACKWASH_MODE_MAP.items()}
PUMP_SPEED_NAMES = {v: k for k, v in PUMP_SPEED_MAP.items()}
BACKWASH_FREQ_NAMES = {v: k for k, v in BACKWASH_FREQ_MAP.items()}
TRUE_FALSE_NAMES = {v: k for k, v in TRUE_FALSE_MAP.items()}

# Device types
DEVICE_TYPE_FILTRATIE = "filtratie"
DEVICE_TYPE_HYDROLYSE = "hydrolyse"
DEVICE_TYPE_SETPOINTS = "setpoints"
DEVICE_TYPE_GLOBAL = "global"
DEVICE_TYPE_MAIN = "main"
DEVICE_TYPE_MODULES = "modules"
DEVICE_TYPE_RELAYS = "relays"
DEVICE_TYPE_FORM = "form"

# Device info templates
DEVICE_INFO = {
    DEVICE_TYPE_FILTRATIE: {
        "name": "Filtratie",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
    DEVICE_TYPE_HYDROLYSE: {
        "name": "Hydrolyse",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
    DEVICE_TYPE_SETPOINTS: {
        "name": "Set points",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
    DEVICE_TYPE_GLOBAL: {
        "name": "Algemeen (Global)",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
    DEVICE_TYPE_MAIN: {
        "name": "Algemeen (Main)",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
    DEVICE_TYPE_MODULES: {
        "name": "Modules",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
    DEVICE_TYPE_RELAYS: {
        "name": "Relays",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
    DEVICE_TYPE_FORM: {
        "name": "Form",
        "manufacturer": "Vistapool",
        "model": "Vistapool Controller",
    },
}


def get_device_info(pool_id: str, device_type: str) -> dict:
    """
    Genereer device info voor een gegeven device type.
    
    Args:
        pool_id: Het pool ID
        device_type: Het type device
        
    Returns:
        Dictionary met device info
    """
    info = DEVICE_INFO.get(device_type, {})
    return {
        "identifiers": {(DOMAIN, f"{pool_id}_{device_type}")},
        **info,
    }