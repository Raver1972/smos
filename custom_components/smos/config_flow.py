"""Config flow for SMOS integration."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_TEXT

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SmosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for the SMOS integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user inputs text.

        Shows a form with a text field for the user to enter some text.
        The entered text will be displayed as the state of a sensor entity.
        """
        errors = {}

        if user_input is not None:
            # Store the entered text in the config entry data
            return self.async_create_entry(
                title=user_input.get(CONF_TEXT, "SMOS"),
                data={CONF_TEXT: user_input.get(CONF_TEXT)},
            )

        # Show form for user input with a text field
        schema = vol.Schema(
            {
                vol.Required(CONF_TEXT, default=""): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )