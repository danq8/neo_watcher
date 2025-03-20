"""Config flow for NEO Watcher integration."""

import logging
from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_NEO_ID, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

class NeoWatcherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for NEO Watcher."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="NEO Watcher", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NEO_ID): str,
                    vol.Required(CONF_API_KEY): str,
                }
            ),
            errors=errors,
        )
