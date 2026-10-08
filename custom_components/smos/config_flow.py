"""Config flow for SMOS integration."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Define a constant key for the selected entity
CONF_SELECTED_ENTITY = "selected_entity"


class SmosConfigFlow(config_entries.ConfigFlow):
    """Handle the configuration flow for the SMOS integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user selects a P1 entity."""
        errors = {}

        # Fetch all entities from Home Assistant to find P1 entities
        self._hass = hass = self.hass

        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_SELECTED_ENTITY, "SMOS"),
                data={CONF_SELECTED_ENTITY: user_input.get(CONF_SELECTED_ENTITY)},
            )

        # Fetch entities containing "P1" in their name (case-insensitive)
        entities = await self._async_get_p1_entities()

        # Build the schema with a dropdown selector
        entity_choices = {}
        for entity in entities:
            entity_choices[entity.entity_id] = f"{entity.name} ({entity.entity_id})"

        if not entity_choices:
            errors["base"] = "no_p1_entities_found"

        schema = vol.Schema(
            {
                vol.Optional(CONF_SELECTED_ENTITY, default=""): vol.In(entity_choices),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def _async_get_p1_entities(self) -> list:
        """Fetch all entities containing 'P1' in their name (case-insensitive)."""
        # Get all entities from the entity registry
        entity_registry = await self.hass.helpers.entity_registry.async_get_registry()
        entities = await self.hass.states.async_all()

        # Filter entities that have "P1" in their name (case-insensitive)
        p1_entities = []
        for entity in entities:
            entity_name = entity.name or ""
            if entity_name and "p1" in entity_name.lower():
                p1_entities.append(entity)

        return p1_entities