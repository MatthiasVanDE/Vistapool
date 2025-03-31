"""Config flow for vistapool integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class VistapoolConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Vistapool config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Setup door de gebruiker in de UI."""
        if user_input is not None:
            # Creëer de config entry en ga door
            return self.async_create_entry(
                title="Vistapool Zwembad",
                data={
                    "email": user_input[CONF_EMAIL],
                    "password": user_input[CONF_PASSWORD],
                    "api_key": user_input["api_key"],
                    "project": user_input["project"],
                    "gateway": user_input["gateway"],
                    "pool_id": user_input["pool_id"],
                }
            )

        schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required("api_key", default=""): str,
            vol.Required("project", default="hayward-europe"): str,
            vol.Required("gateway"): str,
            vol.Required("pool_id"): str
        })

        return self.async_show_form(step_id="user", data_schema=schema)