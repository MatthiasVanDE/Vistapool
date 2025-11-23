"""Config flow voor Vistapool integratie."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .api import (
    VistapoolApiClient,
    VistapoolAuthError,
    VistapoolConnectionError,
    VistapoolApiError,
)

_LOGGER = logging.getLogger(__name__)

# Config velden
CONF_API_KEY = "api_key"
CONF_PROJECT = "project"
CONF_GATEWAY = "gateway"
CONF_POOL_ID = "pool_id"

# Defaults
DEFAULT_PROJECT = "hayward-europe"


async def validate_input(hass: HomeAssistant, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valideer de gebruikersinput door een test API call te maken.
    
    Args:
        hass: Home Assistant instance
        data: User input dictionary
        
    Returns:
        Dictionary met info voor de entry
        
    Raises:
        VistapoolAuthError: Bij authenticatie fouten
        VistapoolConnectionError: Bij verbindingsfouten
    """
    # Maak een test API client
    api = VistapoolApiClient(
        api_key=data[CONF_API_KEY],
        email=data[CONF_EMAIL],
        password=data[CONF_PASSWORD],
        project=data[CONF_PROJECT],
        gateway=data[CONF_GATEWAY],
        pool_id=data[CONF_POOL_ID],
    )

    # Test de verbinding
    await hass.async_add_executor_job(api.login)
    
    # Test of we het pool document kunnen ophalen
    doc = await hass.async_add_executor_job(api.get_pool_document)
    
    if not doc:
        raise VistapoolApiError("Kon pool document niet ophalen")

    # Sluit de sessie
    api.close()

    # Return info voor de entry
    return {
        "title": f"Vistapool {data[CONF_POOL_ID][:8]}...",
        "pool_id": data[CONF_POOL_ID],
    }


class VistapoolConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow voor Vistapool."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle de initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                # Valideer de input
                info = await validate_input(self.hass, user_input)

                # Check of deze pool al geconfigureerd is
                await self.async_set_unique_id(user_input[CONF_POOL_ID])
                self._abort_if_unique_id_configured()

                # Maak de entry
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

            except VistapoolAuthError:
                _LOGGER.warning("Authenticatie gefaald voor Vistapool")
                errors["base"] = "invalid_auth"
            
            except VistapoolConnectionError:
                _LOGGER.warning("Kan geen verbinding maken met Vistapool")
                errors["base"] = "cannot_connect"
            
            except VistapoolApiError as err:
                _LOGGER.error("API fout bij Vistapool configuratie: %s", err)
                errors["base"] = "unknown"
            
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Onverwachte fout bij Vistapool configuratie")
                errors["base"] = "unknown"

        # Toon het formulier
        data_schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(
                    CONF_API_KEY,
                    description="Firebase API Key (zie documentatie)",
                ): str,
                vol.Required(
                    CONF_PROJECT,
                    default=DEFAULT_PROJECT,
                    description="Firebase project (meestal hayward-europe)",
                ): str,
                vol.Required(
                    CONF_GATEWAY,
                    description="Gateway ID (bijv. P32202209190043)",
                ): str,
                vol.Required(
                    CONF_POOL_ID,
                    description="Pool ID (24 tekens hexadecimaal)",
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "docs_url": "https://github.com/MatthiasVanDE/Vistapool"
            },
        )

    async def async_step_import(self, import_config: Dict[str, Any]) -> FlowResult:
        """Handle import van YAML configuratie."""
        return await self.async_step_user(import_config)


class VistapoolOptionsFlow(config_entries.OptionsFlow):
    """Handle options voor Vistapool."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialiseer de options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Toon options formulier (bijv. scan interval)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "scan_interval",
                        default=self.config_entry.options.get("scan_interval", 30),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                }
            ),
        )
