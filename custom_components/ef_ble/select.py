from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.ef_ble.eflib import DeviceBase

from . import DeviceConfigEntry
from .eflib.devices import river3, river3_plus
from .entity import EcoflowEntity


@dataclass(kw_only=True, frozen=True)
class EcoflowSelectEntityDescription[T: DeviceBase](SelectEntityDescription):
    set_state: Callable[[T, str], Awaitable] | None = None


SELECT_TYPES: list[EcoflowSelectEntityDescription] = [
    # River 3 Plus
    EcoflowSelectEntityDescription[river3_plus.Device](
        key="led_mode",
        name="LED",
        options=[opt.name.lower() for opt in river3_plus.LedMode],
        set_state=(
            lambda device, value: device.set_led_mode(
                river3_plus.LedMode[value.upper()]
            )
        ),
    ),
    EcoflowSelectEntityDescription[river3.Device](
        key="dc_charging_type",
        name="DC Charging Type",
        options=[
            opt.name.lower()
            for opt in river3.DcChargingType
            if opt is not river3.DcChargingType.UNKNOWN
        ],
        set_state=(
            lambda device, value: device.set_dc_charging_type(
                river3.DcChargingType[value.upper()]
            )
        ),
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add binary sensors for passed config_entry in HA."""
    device = config_entry.runtime_data

    new_sensors = [
        EcoflowSelect(device, description)
        for description in SELECT_TYPES
        if hasattr(device, description.key)
    ]

    if new_sensors:
        async_add_entities(new_sensors)


class EcoflowSelect(EcoflowEntity, SelectEntity):
    def __init__(
        self,
        device: DeviceBase,
        description: EcoflowSelectEntityDescription[DeviceBase],
    ):
        super().__init__(device)

        self._attr_unique_id = f"{self._device.name}_{description.key}"
        self.entity_description = description
        self._prop_name = self.entity_description.key
        self._set_state = description.set_state
        self._attr_current_option = None

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._device.register_state_update_callback(self.state_updated, self._prop_name)

    async def async_will_remove_from_hass(self) -> None:
        """Entity being removed from hass."""
        self._device.remove_state_update_calback(self.state_updated, self._prop_name)

    @callback
    def state_updated(self, state: Enum):
        self._attr_current_option = state.name.lower()
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        if self._set_state is not None:
            await self._set_state(self._device, option)
            return

        await super().async_select_option(option)
