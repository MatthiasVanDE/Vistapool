from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .api import VistapoolApi
from .coordinator import VistapoolDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Vistapool component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vistapool from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    # Haal config uit entry.data
    email = entry.data["email"]
    password = entry.data["password"]
    api_key = entry.data["api_key"]
    project = entry.data["project"]
    gateway = entry.data["gateway"]
    pool_id = entry.data["pool_id"]

    # Initialiseer de API op jouw manier (zoals jij het vroeger deed)
    api = VistapoolApi(email, password, api_key, project, gateway, pool_id)
    await api.async_initialize()  # ← als je asynchrone init gebruikt

    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
    }

    coordinator = VistapoolDataUpdateCoordinator(hass, api, pool_id)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok