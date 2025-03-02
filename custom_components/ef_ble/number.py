from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DeviceConfigEntry
from .eflib import DeviceBase
from .eflib.devices import river3
from .entity import EcoflowEntity


@dataclass(frozen=True, kw_only=True)
class EcoflowNumberEntityDescription[T: DeviceBase](NumberEntityDescription):
    async_set_native_value: Callable[[T, float], Awaitable[bool]] | None = None

    min_value_prop: str | None = None
    max_value_prop: str | None = None
    availability_prop: str | None = None


NUMBER_TYPES = [
    # River 3
    EcoflowNumberEntityDescription[river3.Device](
        key="energy_backup_battery_level",
        name="Backup Reserve",
        device_class=NumberDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        native_step=1.0,
        min_value_prop="battery_charge_limit_min",
        max_value_prop="battery_charge_limit_max",
        async_set_native_value=(
            lambda device, value: device.set_energy_backup_battery_level(int(value))
        ),
        availability_prop="energy_backup",
    ),
    EcoflowNumberEntityDescription[river3.Device](
        key="battery_charge_limit_min",
        name="Discharge Limit",
        device_class=NumberDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        native_step=1.0,
        native_min_value=0,
        max_value_prop="battery_charge_limit_max",
        async_set_native_value=(
            lambda device, value: device.set_battery_charge_limit_min(int(value))
        ),
    ),
    EcoflowNumberEntityDescription[river3.Device](
        key="battery_charge_limit_max",
        name="Charge Limit",
        device_class=NumberDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        native_step=1.0,
        native_max_value=100,
        min_value_prop="battery_charge_limit_min",
        async_set_native_value=(
            lambda device, value: device.set_battery_charge_limit_max(int(value))
        ),
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    device = config_entry.runtime_data

    async_add_entities(
        [
            EcoflowNumber(device, entity_description)
            for entity_description in NUMBER_TYPES
            if hasattr(device, entity_description.key)
        ]
    )


class EcoflowNumber(EcoflowEntity, NumberEntity):
    def __init__(
        self,
        device: DeviceBase,
        entity_description: EcoflowNumberEntityDescription[DeviceBase],
    ):
        super().__init__(device)
        self._attr_unique_id = f"{device.name}_{entity_description.key}"
        self.entity_description = entity_description
        self._min_value_prop = entity_description.min_value_prop
        self._max_value_prop = entity_description.max_value_prop
        self._availability_prop = entity_description.availability_prop
        self._set_native_value = entity_description.async_set_native_value
        self._prop_name = entity_description.key
        self._attr_native_value = getattr(device, self._prop_name)

    @property
    def available(self):
        is_available = super().available
        if not is_available or self._availability_prop is None:
            return is_available

        return self._attr_available

    async def async_set_native_value(self, value: float) -> None:
        if self._set_native_value is not None:
            await self._set_native_value(self._device, value)
            return

        await super().async_set_native_value(value)

    @callback
    def state_updated(self, state: float | None):
        self._attr_native_value = state
        self.async_write_ha_state()

    @callback
    def _min_state_updated(self, state: float | None):
        if state is not None:
            self._attr_native_min_value = state
            self.async_write_ha_state()

    @callback
    def _max_state_updated(self, state: float | None):
        if state is not None:
            self._attr_native_max_value = state
            self.async_write_ha_state()

    @callback
    def _availability_updated(self, state: bool | None):
        self._attr_available = state if state is not None else False
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        self._device.register_state_update_callback(self.state_updated, self._prop_name)
        if self._min_value_prop is not None:
            self._device.register_state_update_callback(
                self._min_state_updated, self._min_value_prop
            )
        if self._max_value_prop is not None:
            self._device.register_state_update_callback(
                self._max_state_updated,
                self._max_value_prop,
            )
        if self._availability_prop is not None:
            self._device.register_state_update_callback(
                self._availability_updated,
                self._availability_prop,
            )
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self) -> None:
        self._device.remove_state_update_calback(self.state_updated, self._prop_name)
        if self._min_value_prop is not None:
            self._device.remove_state_update_calback(
                self._min_state_updated, self._min_value_prop
            )
        if self._max_value_prop is not None:
            self._device.remove_state_update_calback(
                self._max_state_updated,
                self._max_value_prop,
            )
        if self._availability_prop is not None:
            self._device.remove_state_update_calback(
                self._availability_updated,
                self._availability_prop,
            )
        await super().async_will_remove_from_hass()
