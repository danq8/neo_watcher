"""Sensor platform for NEO Watcher."""

import logging
from typing import Any
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ATTRIBUTION,  CONF_API_KEY
from .coordinator import NeoWatcherCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up the NEO Watcher sensor."""
    coordinator = NeoWatcherCoordinator(hass, config_entry.data[CONF_API_KEY])
    await coordinator.async_config_entry_first_refresh()
    entities = [
        NEOWatcherRateLimitSensor(coordinator, "X-RateLimit-Limit", "Your NASA RateLimit", SensorEntityDescription(key="rate_limit_limit")),
        NEOWatcherRateLimitSensor(coordinator, "X-RateLimit-Remaining", "Your NASA RateLimit remaining calls", SensorEntityDescription(key="rate_limit_remaining"))
    ]
    for i in range(min(5, len(coordinator.data))):        
        entities.append(NEOWatcherFeedSensor(coordinator, i, i+1))
    async_add_entities(entities)



class NEOWatcherFeedSensor(CoordinatorEntity, SensorEntity):
    """Representation of a NEO Watcher sensor."""

    def __init__(self, coordinator: NeoWatcherCoordinator, index: int, rank: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._index = index
        self._rank = rank
        self._attr_name = f"{self._rank}{self._get_rank_suffix(self._rank)} closest object"
        self._attr_unique_id = f"neo_watcher_feed_{self.data['id']}"
        self._attr_attribution = ATTRIBUTION
        self._attr_native_value = self.data['name']

    def _get_rank_suffix(self, rank):
        """Return the suffix for the rank."""
        if 11 <= rank <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(rank % 10, "th")

    @property
    def data(self) -> dict[str, Any]:
        """Return data for this sensor."""
        return self.coordinator.data[self._index]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        data = self.data
        closest_approach = data.get("close_approach_data", [])[0]
        return {
            "nasa_jpl_url": data.get("nasa_jpl_url"),
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
            "name": data.get("name"),
        }

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
        self.async_write_ha_state()


class NEOWatcherRateLimitSensor(CoordinatorEntity, SensorEntity):
    """Representation of a NEO Watcher rate limit sensor."""
    
    def __init__(self, coordinator: NeoWatcherCoordinator, header_name: str, name: str, entity_description: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        self.entity_description = entity_description
        super().__init__(coordinator, entity_description)
        self._header_name = header_name
        self._attr_name = name
        self._attr_unique_id = f"neo_watcher_{header_name.lower().replace('-', '_')}"
        self._attr_attribution = ATTRIBUTION
        self._attr_native_value = None
        self.coordinator = coordinator
        self._update_native_value()

    def _update_native_value(self):
        """Update the native value with the header information."""
        if self.coordinator.headers:
            self._attr_native_value = self.coordinator.headers.get(self._header_name)

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
        self._update_native_value()
        self.async_write_ha_state()
