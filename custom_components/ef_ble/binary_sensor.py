"""EcoFlow BLE binary sensor"""

import logging
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.ef_ble.eflib import DeviceBase

from . import DeviceConfigEntry
from .entity import EcoflowEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EcoflowBinarySensorEntityDescription(BinarySensorEntityDescription):
    update_state: Callable[[bool], None] | None = None


BINARY_SENSOR_TYPES = {
    "error_happened": BinarySensorEntityDescription(
        key="error",
        name="Error",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "plugged_in_ac": BinarySensorEntityDescription(
        key="plugged_in_ac",
        name="AC Plugged In",
        device_class=BinarySensorDeviceClass.PLUG,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add binary sensors for passed config_entry in HA."""
    device = config_entry.runtime_data

    new_sensors = [
        EcoflowBinarySensor(device, sensor)
        for sensor in BINARY_SENSOR_TYPES
        if hasattr(device, sensor)
    ]

    if new_sensors:
        async_add_entities(new_sensors)


class EcoflowBinarySensor(EcoflowEntity, BinarySensorEntity):
    def __init__(
        self,
        device: DeviceBase,
        sensor: str,
    ):
        super().__init__(device)

        self._attr_unique_id = f"{self._device.name}_{sensor}"
        self.entity_description = BINARY_SENSOR_TYPES[sensor]
        self._prop_name = self.entity_description.key

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._device.register_state_update_callback(self.state_updated, self._prop_name)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._device.remove_state_update_calback(self.state_updated, self._prop_name)

    @callback
    def state_updated(self, state: bool):
        self._attr_is_on = state
        self.async_write_ha_state()
