"""NEO Watcher integration."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import NeoWatcherCoordinator
from .const import CONF_API_KEY
import asyncio

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NEO Watcher from a config entry."""
    _LOGGER.debug("Setting up NEO Watcher integration.")
    _LOGGER.debug(f"Config entry data: {entry.data}")
    coordinator = NeoWatcherCoordinator(hass, entry.data[CONF_API_KEY])
    _LOGGER.debug("Created NeoWatcherCoordinator instance.")
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug("Coordinator first refresh completed.")

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    _LOGGER.debug(f"Coordinator added to hass.data for entry_id: {entry.entry_id}")

    # Load the sensor platform and wait for it to complete
    _LOGGER.debug("Forwarding entry setup to sensor platform.")
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    _LOGGER.debug("Sensor platform setup completed.")

    _LOGGER.debug("NEO Watcher integration setup completed successfully.")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug(f"Unloading NEO Watcher integration for entry_id: {entry.entry_id}")
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, "sensor")]
        )
    )
    _LOGGER.debug(f"Sensor platform unload result: {unload_ok}")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug(f"Coordinator removed from hass.data for entry_id: {entry.entry_id}")

    _LOGGER.debug(f"NEO Watcher integration unload completed with result: {unload_ok}")
    return unload_ok
