"""Config flow for NEO Watcher integration."""
from __future__ import annotations

import logging
from typing import Any, Mapping

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig, NumberSelectorMode

from .const import DOMAIN, CONF_API_KEY, CONF_WEEKS_AHEAD, DEFAULT_WEEKS_AHEAD

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NEO Watcher."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_API_KEY): str,
                        vol.Required(
                            CONF_WEEKS_AHEAD,
                            default=DEFAULT_WEEKS_AHEAD,
                        ): vol.All(vol.Coerce(int), vol.Range(min=1, max=104)),
                    }
                ),
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
            return self.async_show_form(step_id="user", errors=errors)
        except InvalidAuth:
            errors["base"] = "invalid_auth"
            return self.async_show_form(step_id="user", errors=errors)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
            return self.async_show_form(step_id="user", errors=errors)
        else:
            return self.async_create_entry(title="Neo_Watcher", data=user_input)




async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # You could add API validation here if needed.
    # For example, try to make a request to the API with the provided key.
    # If the request fails, raise an exception.
    # If the request succeeds, return a dictionary with user data.

    return {}  # <--- Corrected: Return an empty dictionary
class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
