"""
Main setup for SMOS integration.

Handles setting up and unloading config entries, and forwarding setup to sensor platform.
"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """General setup of the integration.

    This is called once when Home Assistant starts.
    It does not perform any configuration and always returns True.
    """
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry.

    Initializes the component for this entry and forwards setup to platforms.

    Args:
        hass: Home Assistant instance.
        entry: ConfigEntry to setup.

    Returns:
        True if setup successful, False otherwise.
    """
    try:
        # Forward setup to sensor platform
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        return True
    except Exception as err:
        _LOGGER.error("Error setting up entry %s: %s", entry.entry_id, err)
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and its associated platforms.

    Args:
        hass: Home Assistant instance.
        entry: ConfigEntry to unload.

    Returns:
        True if unload successful, False otherwise.
    """
    try:
        # Unload all platforms for the entry
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

        if unload_ok:
            # Remove coordinator/reference from hass data
            hass.data[DOMAIN].pop(entry.entry_id, None)

        return unload_ok
    except Exception as err:
        _LOGGER.error("Error unloading entry %s: %s", entry.entry_id, err)
        return False