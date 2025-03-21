"""NEO Watcher integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import NeoWatcherCoordinator
from .const import CONF_API_KEY
import asyncio

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NEO Watcher from a config entry."""
    coordinator = NeoWatcherCoordinator(hass, entry.data[CONF_API_KEY])
    await coordinator.async_config_entry_first_refresh()


    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator    
    # Load the sensor platform and wait for it to complete
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, "sensor")
        ]
    ))
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
