"""EcoFlow BLE binary sensor"""

import dataclasses
from collections.abc import Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DeviceConfigEntry
from .description_builder import BinarySensorBuilder
from .eflib import DeviceBase, get_binary_sensors, sensors
from .entity import EcoflowEntity


@dataclasses.dataclass
class Builder[E: sensors.EntityType]:
    builder: Callable[[E, BinarySensorBuilder], BinarySensorBuilder]


type BuilderDict[E: sensors.EntityType] = dict[type[E], Builder[E]]

BUILDERS: BuilderDict = {
    sensors.Plug: Builder[sensors.Plug](
        lambda _, builder: builder.device_class(BinarySensorDeviceClass.PLUG)
    ),
    sensors.Problem: Builder[sensors.Problem](
        lambda _, builder: (
            builder.device_class(BinarySensorDeviceClass.PROBLEM).entity_category(
                EntityCategory.DIAGNOSTIC
            )
        )
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
        EcoflowBinarySensor(
            device,
            BUILDERS[sensor.__class__]
            .builder(
                sensor,
                BinarySensorBuilder(sensor.field)
                .key(sensor.key)
                .enabled(sensor.enabled),
            )
            .build(),
        )
        for sensor in get_binary_sensors(device)
    ]

    if new_sensors:
        async_add_entities(new_sensors)


class EcoflowBinarySensor(EcoflowEntity, BinarySensorEntity):
    def __init__(
        self,
        device: DeviceBase,
        description: BinarySensorEntityDescription,
    ):
        super().__init__(device)

        self._attr_unique_id = f"{self._device.name}_{description.key}"
        self.entity_description = description
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
