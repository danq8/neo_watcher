"""Data update coordinator for the NEO Watcher integration."""

import logging
from datetime import timedelta
import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import DOMAIN, CONF_NEO_ID, CONF_API_KEY, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class NeoWatcherCoordinator(DataUpdateCoordinator):
    """Data update coordinator for the NEO Watcher integration."""

    def __init__(self, hass: HomeAssistant, neo_id: str, api_key: str) -> None:
        """Initialize the coordinator."""
        self.neo_id = neo_id
        self.api_key = api_key
        self.headers = None  # Initialize headers attribute
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            url = f"https://api.nasa.gov/neo/rest/v1/neo/{self.neo_id}?api_key={self.api_key}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    self.headers = response.headers  # Store response headers
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

