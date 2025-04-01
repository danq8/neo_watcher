"""Data update coordinator for the NEO Watcher integration."""

import logging
from datetime import date, timedelta
import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import DOMAIN, CONF_API_KEY, SCAN_INTERVAL, CONF_WEEKS_AHEAD

_LOGGER = logging.getLogger(__name__)


class NeoWatcherCoordinator(DataUpdateCoordinator):
    """Data update coordinator for the NEO Watcher integration."""

    def __init__(self, hass: HomeAssistant, api_key: str, weeks_ahead: int) -> None:
        """Initialize the coordinator."""
        self.api_key = api_key
        self.weeks_ahead = weeks_ahead # New weeks_ahead attribute
        self.headers = None  # Initialize headers attribute
        self.near_earth_objects = []
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint and process it."""
        _LOGGER.debug("Starting data update process.")
        try:
            today = date.today()
            all_objects = []
            all_ph_objects = []
            _LOGGER.debug(f"Today's date: {today}")
            for i in range(self.weeks_ahead): # Use self.weeks_ahead here
                start_date = today + timedelta(days=i * 7)
                end_date = start_date + timedelta(days=6)
                start_date_str = start_date.strftime("%Y-%m-%d")
                end_date_str = end_date.strftime("%Y-%m-%d")
                _LOGGER.debug(f"Fetching data for date range: {start_date_str} to {end_date_str}")
                url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date_str}&end_date={end_date_str}&api_key={self.api_key}"
                _LOGGER.debug(f"API URL: {url}")
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        self.headers = response.headers  # Store response headers
                        _LOGGER.debug(f"Response status: {response.status}")
                        response.raise_for_status()
                        data = await response.json()
                        _LOGGER.debug(f"Received data: {data}")
                        objects = data.get("near_earth_objects", {})
                        _LOGGER.debug(f"Number of dates with objects: {len(objects)}")
                        for date_str, objects_list in objects.items():
                            _LOGGER.debug(f"Processing objects for date: {date_str}")
                            all_ph_objects.extend([obj for obj in objects_list if obj["is_potentially_hazardous_asteroid"]])
                            _LOGGER.debug(f"Number of potentially hazardous objects found for {date_str}: {len([obj for obj in objects_list if obj['is_potentially_hazardous_asteroid']])}")
                            all_objects.extend(objects_list)
            self.near_earth_objects = all_objects
            all_ph_objects.sort(key=lambda x: float(x["close_approach_data"][0]["miss_distance"]["miles"]))
            _LOGGER.debug(f"Total number of potentially hazardous objects found: {len(all_ph_objects)}")
            _LOGGER.debug("Data update process completed successfully.")
            return all_ph_objects
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Error communicating with API: {err}")
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            _LOGGER.error(f"An unexpected error occurred: {err}")
            raise UpdateFailed(f"An unexpected error occurred: {err}") from err
