from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.ef_ble.eflib.devices import alternator_charger

from . import DeviceConfigEntry
from .eflib import DeviceBase
from .eflib.devices import delta3, delta3_plus, delta_pro_3, river3
from .entity import EcoflowEntity


@dataclass(frozen=True, kw_only=True)
class EcoflowNumberEntityDescription[T: DeviceBase](NumberEntityDescription):
    async_set_native_value: Callable[[T, float], Awaitable[bool]] | None = None

    min_value_prop: str | None = None
    max_value_prop: str | None = None
    availability_prop: str | None = None


NUMBER_TYPES: list[EcoflowNumberEntityDescription] = [
    EcoflowNumberEntityDescription[river3.Device](
        key="energy_backup_battery_level",
        name="Backup Reserve",
        icon="mdi:battery-sync",
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
        icon="mdi:battery-arrow-down-outline",
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
        icon="mdi:battery-arrow-up",
        device_class=NumberDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        native_step=1.0,
        native_max_value=100,
        min_value_prop="battery_charge_limit_min",
        async_set_native_value=(
            lambda device, value: device.set_battery_charge_limit_max(int(value))
        ),
    ),
    EcoflowNumberEntityDescription[river3.Device | delta3.Device | delta_pro_3.Device](
        key="ac_charging_speed",
        name="AC Charging Speed",
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        native_step=1,
        native_min_value=0,
        max_value_prop="max_ac_charging_power",
        async_set_native_value=(
            lambda device, value: device.set_ac_charging_speed(int(value))
        ),
    ),
    EcoflowNumberEntityDescription[river3.Device | delta3.Device](
        key="dc_charging_max_amps",
        name="DC Charging Max Amps",
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        native_step=1,
        native_min_value=0,
        max_value_prop="dc_charging_current_max",
        async_set_native_value=(
            lambda device, value: device.set_dc_charging_amps_max(int(value))
        ),
    ),
    EcoflowNumberEntityDescription[delta3_plus.Device](
        key="dc_charging_max_amps_2",
        name="DC (2) Charging Max Amps",
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        native_step=1,
        native_min_value=0,
        max_value_prop="dc_charging_current_max_2",
        async_set_native_value=(
            lambda device, value: device.set_dc_charging_amps_max_2(int(value))
        ),
    ),
    EcoflowNumberEntityDescription[alternator_charger.Device](
        key="power_limit",
        name="Power Limit",
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        native_step=1,
        native_min_value=0,
        max_value_prop="power_max",
        async_set_native_value=(
            lambda device, value: device.set_power_limit(int(value))
        ),
    ),
    EcoflowNumberEntityDescription[alternator_charger.Device](
        key="start_voltage",
        name="Start Voltage",
        device_class=NumberDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        native_step=0.1,
        min_value_prop="car_battery_voltage_min",
        max_value_prop="car_battery_voltage_max",
        async_set_native_value=(
            lambda device, value: device.set_battery_voltage(int(value))
        ),
    ),
    EcoflowNumberEntityDescription[alternator_charger.Device](
        key="car_battery_charging_amp_limit",
        name="Reverse Charging Current",
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        native_step=1,
        native_min_value=0,
        max_value_prop="car_battery_amp_max",
        async_set_native_value=(
            lambda device, value: device.set_car_battery_curent_charge_limit(value)
        ),
    ),
    EcoflowNumberEntityDescription[alternator_charger.Device](
        key="dev_battery_charging_amp_limit",
        name="Charging Current",
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        native_step=1,
        native_min_value=0,
        max_value_prop="dev_battery_charging_amp_max",
        async_set_native_value=(
            lambda device, value: device.set_device_battery_current_charge_limit(value)
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
        self._update_callbacks: list[tuple[str, Callable[[Any], None]]] = []

        self._register_update_callback("_attr_native_value", self._prop_name)
        self._register_update_callback(
            "_attr_available",
            self._availability_prop,
            lambda state: state if state is not None else False,
        )
        self._register_update_callback(
            "_attr_native_min_value",
            self._min_value_prop,
            lambda state: state if state is not None else EcoflowNumber._SkipWrite,
        )
        self._register_update_callback(
            "_attr_native_max_value",
            self._max_value_prop,
            lambda state: state if state is not None else EcoflowNumber._SkipWrite,
        )

    class _SkipWrite:
        """Sentinel value for skipping write in update callback"""

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

    def _register_update_callback(
        self,
        entity_attr: str,
        prop_name: str | None,
        get_state: Callable[[Any], _SkipWrite | Any] = lambda x: x,
    ):
        if prop_name is None:
            return

        @callback
        def state_updated(state: Any):
            if (state := get_state(state)) is EcoflowNumber._SkipWrite:
                return

            setattr(self, entity_attr, state)
            self.async_write_ha_state()

        if state := getattr(self._device, prop_name, None):
            setattr(self, entity_attr, state)

        self._update_callbacks.append((prop_name, state_updated))

    async def async_added_to_hass(self) -> None:
        for prop, state_callback in self._update_callbacks:
            self._device.register_state_update_callback(state_callback, prop)
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self) -> None:
        for prop, state_callback in self._update_callbacks:
            self._device.remove_state_update_calback(state_callback, prop)
        await super().async_will_remove_from_hass()
