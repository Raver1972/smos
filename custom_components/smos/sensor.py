"""SMOS sensor entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import SmosCoordinator
from .const import DOMAIN
from .const import MANUFACTURER, MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all SMOS sensors from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create sensor entity from coordinator-provided definition
    entities = [SmosSensor(coordinator, entry)]

    # Add all entities to Home Assistant
    async_add_entities(entities)


class SmosSensor(CoordinatorEntity, SensorEntity):
    """Sensor displaying the text entered by the user via config flow."""

    def __init__(self, coordinator: SmosCoordinator, entry: ConfigEntry):
        """Initialize the SMOS sensor."""
        super().__init__(coordinator)

        # Store the text from config entry data
        self._text = entry.data.get("text", "")

        # Set entity attributes from config entry
        self._attr_unique_id = f"{entry.entry_id}_text_input"
        self._attr_has_entity_name = True
        self._attr_translation_key = "text_input"
        self._attr_name = "SMOS Text Input"
        self._attr_native_value = self._text

        # Set manufacturer and model from constants
        self._attr_extra_state_attributes = {
            "manufacturer": MANUFACTURER,
            "model": MODEL,
            "domain": DOMAIN,
        }

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        return self._attr_extra_state_attributes