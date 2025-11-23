"""Vistapool (Sugar Valley Oxilife) integratie voor Home Assistant."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
import voluptuous as vol

from .const import DOMAIN
from .coordinator import VistapoolDataUpdateCoordinator
from .api import VistapoolApiError, VistapoolConnectionError

_LOGGER = logging.getLogger(__name__)

# Ondersteunde platforms
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SELECT,
]

# Service schemas
SERVICE_SET_TIMER_INTERVALS_SCHEMA = vol.Schema(
    {
        vol.Required("interval1_from"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=86400)
        ),
        vol.Required("interval1_to"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=86400)
        ),
        vol.Optional("interval2_from"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=86400)
        ),
        vol.Optional("interval2_to"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=86400)
        ),
        vol.Optional("interval3_from"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=86400)
        ),
        vol.Optional("interval3_to"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=86400)
        ),
    }
)


async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    """Set up de Vistapool integratie via YAML (optioneel)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up Vistapool vanuit een config entry.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry van UI
        
    Returns:
        True bij succes
        
    Raises:
        ConfigEntryNotReady: Bij tijdelijke fouten
    """
    hass.data.setdefault(DOMAIN, {})

    # Haal scan interval uit options (of gebruik default)
    scan_interval = entry.options.get("scan_interval", 30)
    
    # Maak coordinator
    coordinator = VistapoolDataUpdateCoordinator(
        hass=hass,
        config_data=entry.data,
        update_interval=timedelta(seconds=scan_interval),
    )

    # Doe eerste refresh
    try:
        await coordinator.async_config_entry_first_refresh()
    except VistapoolConnectionError as err:
        # Tijdelijke netwerk fouten
        raise ConfigEntryNotReady(
            f"Kan geen verbinding maken met Vistapool: {err}"
        ) from err
    except VistapoolApiError as err:
        # Structurele API fouten
        _LOGGER.error("Fout bij initialiseren Vistapool integratie: %s", err)
        return False

    # Sla coordinator op
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Registreer services
    async def handle_set_timer_intervals(call: ServiceCall) -> None:
        """Handle de set_timer_intervals service."""
        # Bouw de changes dictionary
        changes: Dict[str, Any] = {"filtration": {}}
        
        # Interval 1
        if "interval1_from" in call.data:
            changes["filtration"]["interval1"] = {
                "from": call.data["interval1_from"],
                "to": call.data["interval1_to"],
            }
        
        # Interval 2 (optioneel)
        if "interval2_from" in call.data:
            changes["filtration"]["interval2"] = {
                "from": call.data["interval2_from"],
                "to": call.data["interval2_to"],
            }
        
        # Interval 3 (optioneel)
        if "interval3_from" in call.data:
            changes["filtration"]["interval3"] = {
                "from": call.data["interval3_from"],
                "to": call.data["interval3_to"],
            }

        _LOGGER.info("Service set_timer_intervals aangeroepen met: %s", changes)
        
        try:
            await coordinator.async_send_pool_command("WRP", changes)
        except VistapoolApiError as err:
            _LOGGER.error("Fout bij instellen timer intervals: %s", err)

    # Registreer de service (indien nog niet geregistreerd)
    if not hass.services.has_service(DOMAIN, "set_timer_intervals"):
        hass.services.async_register(
            DOMAIN,
            "set_timer_intervals",
            handle_set_timer_intervals,
            schema=SERVICE_SET_TIMER_INTERVALS_SCHEMA,
        )

    # Registreer entry update listener voor options
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Unload een config entry.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry
        
    Returns:
        True bij succes
    """
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Verwijder coordinator
        coordinator: VistapoolDataUpdateCoordinator = hass.data[DOMAIN].pop(
            entry.entry_id
        )
        
        # Sluit API sessie
        coordinator.api.close()

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """
    Reload een config entry wanneer options wijzigen.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry
    """
    await hass.config_entries.async_reload(entry.entry_id)
