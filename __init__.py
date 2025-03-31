"""Vistapool (Sugar Valley Oxilife) integratie."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import VistapoolDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up via YAML (als je dat wilt).
       Als je alleen de UI-config-flow gebruikt, kun je dit leeg laten."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up vistapool vanuit config flow (UI)."""
    hass.data.setdefault(DOMAIN, {})

    # Maak DataUpdateCoordinator aan
    coordinator = VistapoolDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()

    # Sla op zodat andere platformen hem kunnen gebruiken
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward naar de platformen (sensor, switch, etc.)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_set_timer_intervals(call):
        interval1_from = call.data["interval1_from"]
        interval1_to = call.data["interval1_to"]
        # ...
        changes = {
            "filtration": {
                "interval1": {
                    "from": interval1_from,
                    "to": interval1_to
                }
            }
        }
        await hass.async_add_executor_job(
            coordinator.api.send_pool_command, "WRP", changes
        )
        await coordinator.async_request_refresh()

    hass.services.async_register(DOMAIN, "set_timer_intervals", handle_set_timer_intervals)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Verwijder integratie."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok