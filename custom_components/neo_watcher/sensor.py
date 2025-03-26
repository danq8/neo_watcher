"""Sensor platform for NEO Watcher."""

import logging
from typing import Any
from urllib.parse import quote_plus
import aiohttp
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ATTRIBUTION, CONF_API_KEY
from .coordinator import NeoWatcherCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up the NEO Watcher sensor."""
    _LOGGER.debug("Setting up NEO Watcher sensor platform.")
    _LOGGER.debug(f"Config entry data: {config_entry.data}")
    coordinator = NeoWatcherCoordinator(hass, config_entry.data[CONF_API_KEY])
    _LOGGER.debug("Created NeoWatcherCoordinator instance.")
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug("Coordinator first refresh completed.")
    entities = [
        NEOWatcherRateLimitSensor(coordinator, "X-RateLimit-Limit", "Your NASA RateLimit", SensorEntityDescription(key="rate_limit_limit")),
        NEOWatcherRateLimitSensor(coordinator, "X-RateLimit-Remaining", "Your NASA RateLimit remaining calls", SensorEntityDescription(key="rate_limit_remaining")),
        NEOWatcherTotalObjectsSensor(coordinator)
    ]
    # Loop around to get the top 6
    _LOGGER.debug(f"Found {len(coordinator.data)} potentially hazardous objects.")
    for i in range(min(6, len(coordinator.data))):
        _LOGGER.debug(f"Creating NEOWatcherFeedSensor for object at index {i}.")
        entities.append(NEOWatcherFeedSensor(coordinator, i, i+1))
    _LOGGER.debug(f"Adding {len(entities)} entities to Home Assistant.")
    async_add_entities(entities)
    _LOGGER.debug("NEO Watcher sensor platform setup completed.")


class NEOWatcherFeedSensor(CoordinatorEntity, SensorEntity):
    """Representation of a NEO Watcher sensor."""

    def __init__(self, coordinator: NeoWatcherCoordinator, index: int, rank: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._index = index
        self._rank = rank
        self._attr_name = f"Neo Watcher_{self._rank}{self._get_rank_suffix(self._rank)} closest object"
        self._attr_unique_id = f"neo_watcher_feed_{self.data['id']}"
        self._attr_attribution = ATTRIBUTION
        self._attr_native_value = self.data['name']
        _LOGGER.debug(f"NEOWatcherFeedSensor initialized for object: {self.data['name']}")

    def _get_rank_suffix(self, rank):
        """Return the suffix for the rank."""
        if 11 <= rank <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(rank % 10, "th")

    @property
    def data(self) -> dict[str, Any]:
        """Return data for this sensor."""
        return self.coordinator.data[self._index]

    async def fetch_horizon_data(self, url):
        """Fetch data from the Horizons API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Error communicating with API: {err}")
            return None
        except Exception as err:
            _LOGGER.error(f"An unexpected error occurred: {err}")
            return None

    @property
    async def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        data = self.data
        closest_approach = data.get("close_approach_data", [])[0]
        _LOGGER.debug(f"Getting extra state attributes for object: {data['name']}")
        name = data.get("name")
        name_without_brackets = name.replace("(", "").replace(")", "")
        name_urlencoded = quote_plus(name_without_brackets)
        horizon_url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND=%27{name_urlencoded}%27"

        # New code to fetch and parse data from horizon_url
        horizon_data = await self.fetch_horizon_data(horizon_url)

        if horizon_data is None:
            adist = None
            argument_of_perihelion_wrt_ecliptic = None
            perihelion = None
            magnitude = None
            epoch = None
            ecliptic = None
            perihelion_julian_day = None
            semi_major_axis = None
            perihelion_distance = None
            mean_motion = None
            inclination_wrt_ecliptic = None
            longitude_of_ascending_node_wrt_ecliptic = None
            neo_watcher_orbit_viewer_url = None
        else:
            result_text = horizon_data.get("result", "")
            
            adist = self._extract_value(result_text, "ADIST=")
            _LOGGER.debug(f"adist value {adist}")
            argument_of_perihelion_wrt_ecliptic = self._extract_value(result_text, "W=")
            _LOGGER.debug(f"argument_of_perihelion_wrt_ecliptic value {argument_of_perihelion_wrt_ecliptic}")
            perihelion = float(self._extract_value(result_text, "PER=")) * 365.25 if self._extract_value(result_text, "PER=") is not None else None
            _LOGGER.debug(f"perihelion value {perihelion}")
            magnitude = self._extract_value(result_text, "MA=")
            _LOGGER.debug(f"magnitude value {magnitude}")
            epoch = self._extract_value(result_text, "EPOCH=")
            _LOGGER.debug(f"epoch value {epoch}")
            ecliptic = self._extract_value(result_text, "EC=")
            _LOGGER.debug(f"ecliptic value {ecliptic}")
            perihelion_julian_day = self._extract_value(result_text, "TP=")
            _LOGGER.debug(f"perihelion_julian_day value {perihelion_julian_day}")
            semi_major_axis = self._extract_value(result_text, "A=")
            _LOGGER.debug(f"semi_major_axis value {semi_major_axis}")
            perihelion_distance = self._extract_value(result_text, "QR=")
            _LOGGER.debug(f"perihelion_distance value {perihelion_distance}")
            mean_motion = self._extract_value(result_text, "N=")
            _LOGGER.debug(f"mean_motion value {mean_motion}")
            inclination_wrt_ecliptic = self._extract_value(result_text, "IN=")
            _LOGGER.debug(f"inclination_wrt_ecliptic value {inclination_wrt_ecliptic}")
            longitude_of_ascending_node_wrt_ecliptic = self._extract_value(result_text, "OM=")
            _LOGGER.debug(f"longitude_of_ascending_node_wrt_ecliptic value {longitude_of_ascending_node_wrt_ecliptic}")

            neo_watcher_orbit_viewer_url = (
                f"https://ssd.jpl.nasa.gov/ov/index.html#no-add-menu=1&elem=ad:{adist},w:{argument_of_perihelion_wrt_ecliptic},label:{quote_plus('('+name_without_brackets+')')},per:{perihelion},ma:{magnitude},epoch:{epoch},e:{ecliptic},tp:{perihelion_julian_day},a:{semi_major_axis},q:{perihelion_distance},n:{mean_motion},i:{inclination_wrt_ecliptic},om:{longitude_of_ascending_node_wrt_ecliptic}"
            )
            _LOGGER.debug(f"neo_watcher_orbit_viewer_url value {neo_watcher_orbit_viewer_url}")

        return {
            "name": name,
            "nasa_jpl_url": data.get("nasa_jpl_url"),
            "Neo_Watcher_Orbit_Viewer_URL": neo_watcher_orbit_viewer_url,
            "horizon_url": horizon_url,
            "absolute_magnitude_h": data.get("absolute_magnitude_h"),
            "estimated_diameter_min_km": data.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min"),
            "estimated_diameter_max_km": data.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max"),
            "estimated_diameter_min_mi": data.get("estimated_diameter", {}).get("miles", {}).get("estimated_diameter_min"),
            "estimated_diameter_max_mi": data.get("estimated_diameter", {}).get("miles", {}).get("estimated_diameter_max"),
            "is_potentially_hazardous_asteroid": data.get("is_potentially_hazardous_asteroid"),
            "close_approach_date": closest_approach.get("close_approach_date"),
            "close_approach_date_full": closest_approach.get("close_approach_date_full"),
            "relative_velocity_km_per_s": closest_approach.get("relative_velocity", {}).get("kilometers_per_second"),
            "relative_velocity_km_per_h": closest_approach.get("relative_velocity", {}).get("kilometers_per_hour"),
            "relative_velocity_mi_per_h": closest_approach.get("relative_velocity", {}).get("miles_per_hour"),
            "miss_distance_km": closest_approach.get("miss_distance", {}).get("kilometers"),
            "miss_distance_mi": closest_approach.get("miss_distance", {}).get("miles"),
            "orbiting_body": closest_approach.get("orbiting_body"),
            "ADIST": adist,
            "Argument_of_perihelion_wrt_ecliptic": argument_of_perihelion_wrt_ecliptic,
            "Perihelion": perihelion,
            "Magnitude": magnitude,
            "Epoch": epoch,
            "Ecliptic": ecliptic,
            "Perihelion_Julian_Day": perihelion_julian_day,
            "Semi-major_axis": semi_major_axis,
            "Perihelion distance": perihelion_distance,
            "Mean_motion": mean_motion,
            "Inclination_wrt_ecliptic": inclination_wrt_ecliptic,
            "Longitude_of_ascending_node_wrt_ecliptic": longitude_of_ascending_node_wrt_ecliptic,
            
        }

    def _extract_value(self, text, key):
        """Extract a value from the text based on the key."""
        try:
            start_index = text.find(key)
            if start_index == -1:
                return None
            start_index += len(key)
            end_index = text.find(" ", start_index)
            if end_index == -1:
                return text[start_index:].strip()
            return text[start_index:end_index].strip()
        except:
            return None

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:asteroid"

    @property
    def unit_of_measurement(self) -> None:
        """Return the unit of measurement."""
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(f"Coordinator updated for {self._attr_name}")
        self.async_write_ha_state()


class NEOWatcherRateLimitSensor(CoordinatorEntity, SensorEntity):
    """Representation of a NEO Watcher rate limit sensor."""

    def __init__(self, coordinator: NeoWatcherCoordinator, header_name: str, name: str, entity_description: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        self.entity_description = entity_description
        super().__init__(coordinator, entity_description)
        self._header_name = header_name
        self._attr_name = f"Neo Watcher_{name}"
        self._attr_unique_id = f"neo_watcher_{header_name.lower().replace('-', '_')}"
        self._attr_attribution = ATTRIBUTION
        self._attr_native_value = None
        self.coordinator = coordinator
        self._update_native_value()
        _LOGGER.debug(f"NEOWatcherRateLimitSensor initialized: {name}")

    def _update_native_value(self):
        """Update the native value with the header information."""
        if self.coordinator.headers:
            self._attr_native_value = self.coordinator.headers.get(self._header_name)
            _LOGGER.debug(f"Updated native value for {self._attr_name}: {self._attr_native_value}")

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:api"

    @property
    def unit_of_measurement(self) -> None:
        """Return the unit of measurement."""
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(f"Coordinator updated for {self._attr_name}")
        self._update_native_value()
        self.async_write_ha_state()

class NEOWatcherTotalObjectsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a NEO Watcher total objects sensor."""

    def __init__(self, coordinator: NeoWatcherCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Neo Watcher_Total number of potentially hazardous objects found"
        self._attr_unique_id = "neo_watcher_total_objects"
        self._attr_attribution = ATTRIBUTION
        self._attr_native_value = len(coordinator.data)
        _LOGGER.debug(f"NEOWatcherTotalObjectsSensor initialized")

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return len(self.coordinator.data)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:counter"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "objects"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(f"Coordinator updated for {self._attr_name}")
        self._attr_native_value = len(self.coordinator.data)
        self.async_write_ha_state()
