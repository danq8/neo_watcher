"""Data update coordinator for the NEO Watcher integration."""

import logging
from datetime import date, timedelta
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

    def __init__(self, hass: HomeAssistant, api_key: str) -> None:
        """Initialize the coordinator."""
        self.api_key = api_key
        self.headers = None  # Initialize headers attribute
        self.near_earth_objects = []
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _fetch_feed(self, start_date: date, end_date: date):
        """Fetch data from API endpoint and process it."""
        today = date.today()
        all_objects = {}
        for i in range(4):
            start_date = today + timedelta(days=i * 7)
            end_date = start_date + timedelta(days=6)
            objects = await self._fetch_feed(start_date, end_date)
            for date_str, objects_list in objects.items():
                if date_str not in all_objects:
                    all_objects[date_str] = []
                all_objects[date_str].extend(objects_list)

        self.near_earth_objects = [obj for date_list in all_objects.values() for obj in date_list if obj["is_potentially_hazardous_asteroid"]]
        self.near_earth_objects.sort(key=lambda x: float(x["close_approach_data"][0]["miss_distance"]["miles"]))

        return self.near_earth_objects

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

