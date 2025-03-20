"""NEO Watcher integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import NeoWatcherCoordinator
from .const import CONF_NEO_ID, CONF_API_KEY
from .sensor import async_setup_entry

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NEO Watcher from a config entry."""
    coordinator = NeoWatcherCoordinator(hass, entry.data[CONF_NEO_ID], entry.data[CONF_API_KEY])
    await coordinator.async_config_entry_first_refresh()
    await async_setup_entry(hass, entry) # Corrected line
    return True
