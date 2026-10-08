"""Coordinator for SMOS integration."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SmosCoordinator(DataUpdateCoordinator):
    """Coordinator managing SMOS data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize the coordinator with connection parameters."""
        self.hass = hass
        entry_data = entry.data or {}

        # Store the text from config entry
        self.text = entry_data.get("text", "")

        # Initialize the base DataUpdateCoordinator
        # This integration does not poll - the text is static from config entry
        super().__init__(
            hass,
            _LOGGER,
            name="Smos",
            update_interval=timedelta(seconds=300),
        )

    async def _async_update_data(self):
        """Update data from the config entry.

        For this integration, the text is static from the config entry,
        so we simply return the stored text.
        """
        return self.text