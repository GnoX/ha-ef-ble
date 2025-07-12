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
from custom_components.ef_ble.eflib.devices import alternator_charger, smart_generator

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
        options=river3_plus.LedMode.options(include_unknown=False),
        set_state=(
            lambda device, value: device.set_led_mode(
                river3_plus.LedMode[value.upper()]
            )
        ),
    ),
    EcoflowSelectEntityDescription[river3.Device](
        key="dc_charging_type",
        options=river3.DcChargingType.options(include_unknown=False),
        set_state=(
            lambda device, value: device.set_dc_charging_type(
                river3.DcChargingType[value.upper()]
            )
        ),
    ),
    EcoflowSelectEntityDescription[smart_generator.Device](
        key="performance_mode",
        options=smart_generator.PerformanceMode.options(include_unknown=False),
        set_state=(
            lambda device, value: device.set_performance_mode(
                smart_generator.PerformanceMode[value.upper()]
            )
        ),
    ),
    EcoflowSelectEntityDescription[alternator_charger.Device](
        key="charger_mode",
        options=alternator_charger.ChargerMode.options(include_unknown=False),
        set_state=(
            lambda device, value: device.set_charger_mode(
                alternator_charger.ChargerMode[value.upper()]
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

        if self.entity_description.translation_key is None:
            self._attr_translation_key = self.entity_description.key

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
