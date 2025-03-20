"""Sensor platform for NEO Watcher."""

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ATTRIBUTION
from .coordinator import NeoWatcherCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the NEO Watcher sensor."""
    coordinator = NeoWatcherCoordinator(hass, config_entry.data[CONF_NEO_ID], config_entry.data[CONF_API_KEY])
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([NEOWatcherSensor(coordinator)])

class NEOWatcherSensor(CoordinatorEntity, SensorEntity):
    """Representation of a NEO Watcher sensor."""

    def __init__(self, coordinator: NeoWatcherCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "NEO Watcher"
        self._attr_unique_id = "neo_watcher_sensor"
        self._attr_attribution = ATTRIBUTION

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("name")
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data:
            data = self.coordinator.data
            close_approach_data = data.get("close_approach_data", [])
            closest_approach = close_approach_data[0] if close_approach_data else {}
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
            }
        return {}

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:asteroid"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

