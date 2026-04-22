"""EcoFlow BLE climate entities."""

import dataclasses
from typing import Any

from homeassistant.components.climate import ClimateEntity, ClimateEntityDescription
from homeassistant.components.climate.const import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DeviceConfigEntry
from .description_builder import EntityDescriptionBuilder
from .eflib import DeviceBase, controls, get_controls
from .entity import EcoflowEntity


@dataclasses.dataclass(frozen=True, kw_only=True)
class EcoflowClimateEntityDescription(ClimateEntityDescription):
    hvac_mode_mapping: dict[HVACMode, Any] = dataclasses.field(default_factory=dict)
    fan_mode_mapping: dict[str, Any] = dataclasses.field(default_factory=dict)

    power_prop: str | None = None
    operating_mode_prop: str | None = None
    target_temperature_prop: str | None = None
    target_temperature_low_prop: str | None = None
    target_temperature_high_prop: str | None = None
    target_humidity_prop: str | None = None
    current_temperature_prop: str | None = None
    fan_speed_prop: str | None = None

    target_temperature_hvac_modes: frozenset[HVACMode] | None = None
    target_temperature_range_hvac_modes: frozenset[HVACMode] | None = None
    target_humidity_hvac_modes: frozenset[HVACMode] | None = None
    fan_speed_hvac_modes: frozenset[HVACMode] | None = None

    min_temp: float | None = None
    max_temp: float | None = None
    target_temperature_step: float = 1.0
    min_range_temp: float | None = None
    max_range_temp: float | None = None
    target_temperature_range_step: float = 1.0
    min_humidity: int | None = None
    max_humidity: int | None = None
    temperature_unit: str = UnitOfTemperature.CELSIUS

    set_power_func: Any = None
    set_operating_mode_func: Any = None
    set_target_temp_func: Any = None
    set_target_temp_range_func: Any = None
    set_target_humidity_func: Any = None
    set_fan_speed_func: Any = None


@dataclasses.dataclass(init=False)
class ClimateBuilder(EntityDescriptionBuilder):
    _hvac_mode_mapping: dict[HVACMode, Any] = dataclasses.field(default_factory=dict)
    _fan_mode_mapping: dict[str, Any] = dataclasses.field(default_factory=dict)
    _power_prop: str | None = None
    _target_temperature_prop: str | None = None
    _target_temperature_low_prop: str | None = None
    _target_temperature_high_prop: str | None = None
    _target_humidity_prop: str | None = None
    _current_temperature_prop: str | None = None
    _fan_speed_prop: str | None = None
    _target_temperature_hvac_modes: frozenset[HVACMode] | None = None
    _target_temperature_range_hvac_modes: frozenset[HVACMode] | None = None
    _target_humidity_hvac_modes: frozenset[HVACMode] | None = None
    _fan_speed_hvac_modes: frozenset[HVACMode] | None = None
    _min_temp: float | None = None
    _max_temp: float | None = None
    _target_temperature_step: float = 1.0
    _min_range_temp: float | None = None
    _max_range_temp: float | None = None
    _target_temperature_range_step: float = 1.0
    _min_humidity: int | None = None
    _max_humidity: int | None = None
    _temperature_unit: str = UnitOfTemperature.CELSIUS
    _set_power_func: Any = None
    _set_operating_mode_func: Any = None
    _set_target_temp_func: Any = None
    _set_target_temp_range_func: Any = None
    _set_target_humidity_func: Any = None
    _set_fan_speed_func: Any = None

    def hvac_modes(self, mapping: dict[HVACMode, Any]):
        self._hvac_mode_mapping = mapping
        return self

    def fan_modes(self, mapping: dict[str, Any]):
        self._fan_mode_mapping = mapping
        return self

    def power_prop(self, prop: Any):
        if field := self._get_field(prop):
            self._power_prop = field.public_name
        else:
            self._power_prop = prop
        return self

    def target_temperature_prop(self, prop: Any):
        if field := self._get_field(prop):
            self._target_temperature_prop = field.public_name
        else:
            self._target_temperature_prop = prop
        return self

    def target_temperature_low_prop(self, prop: Any):
        if field := self._get_field(prop):
            self._target_temperature_low_prop = field.public_name
        else:
            self._target_temperature_low_prop = prop
        return self

    def target_temperature_high_prop(self, prop: Any):
        if field := self._get_field(prop):
            self._target_temperature_high_prop = field.public_name
        else:
            self._target_temperature_high_prop = prop
        return self

    def target_humidity_prop(self, prop: Any):
        if field := self._get_field(prop):
            self._target_humidity_prop = field.public_name
        else:
            self._target_humidity_prop = prop
        return self

    def target_temperature_hvac_modes(self, modes: frozenset[HVACMode] | None):
        self._target_temperature_hvac_modes = modes
        return self

    def target_temperature_range_hvac_modes(self, modes: frozenset[HVACMode] | None):
        self._target_temperature_range_hvac_modes = modes
        return self

    def target_humidity_hvac_modes(self, modes: frozenset[HVACMode] | None):
        self._target_humidity_hvac_modes = modes
        return self

    def fan_speed_hvac_modes(self, modes: frozenset[HVACMode] | None):
        self._fan_speed_hvac_modes = modes
        return self

    def min_humidity(self, value: int | None):
        self._min_humidity = value
        return self

    def max_humidity(self, value: int | None):
        self._max_humidity = value
        return self

    def current_temperature_prop(self, prop: Any):
        if field := self._get_field(prop):
            self._current_temperature_prop = field.public_name
        else:
            self._current_temperature_prop = prop
        return self

    def fan_speed_prop(self, prop: Any):
        if field := self._get_field(prop):
            self._fan_speed_prop = field.public_name
        else:
            self._fan_speed_prop = prop
        return self

    def min_temp(self, value: float | None):
        self._min_temp = value
        return self

    def max_temp(self, value: float | None):
        self._max_temp = value
        return self

    def min_range_temp(self, value: float | None):
        self._min_range_temp = value
        return self

    def max_range_temp(self, value: float | None):
        self._max_range_temp = value
        return self

    def target_temperature_step(self, value: float):
        self._target_temperature_step = value
        return self

    def target_temperature_range_step(self, value: float):
        self._target_temperature_range_step = value
        return self

    def temperature_unit(self, value: str):
        self._temperature_unit = value
        return self

    def set_power_func(self, func: Any):
        self._set_power_func = func
        return self

    def set_operating_mode_func(self, func: Any):
        self._set_operating_mode_func = func
        return self

    def set_target_temp_func(self, func: Any):
        self._set_target_temp_func = func
        return self

    def set_target_temp_range_func(self, func: Any):
        self._set_target_temp_range_func = func
        return self

    def set_target_humidity_func(self, func: Any):
        self._set_target_humidity_func = func
        return self

    def set_fan_speed_func(self, func: Any):
        self._set_fan_speed_func = func
        return self

    def build(self) -> EcoflowClimateEntityDescription:
        return EcoflowClimateEntityDescription(
            key=self._entity_key,
            name=self._entity_name,
            hvac_mode_mapping=self._hvac_mode_mapping,
            fan_mode_mapping=self._fan_mode_mapping,
            power_prop=self._power_prop,
            operating_mode_prop=self._entity_key,
            target_temperature_prop=self._target_temperature_prop,
            target_temperature_low_prop=self._target_temperature_low_prop,
            target_temperature_high_prop=self._target_temperature_high_prop,
            target_humidity_prop=self._target_humidity_prop,
            current_temperature_prop=self._current_temperature_prop,
            fan_speed_prop=self._fan_speed_prop,
            target_temperature_hvac_modes=self._target_temperature_hvac_modes,
            target_temperature_range_hvac_modes=(
                self._target_temperature_range_hvac_modes
            ),
            target_humidity_hvac_modes=self._target_humidity_hvac_modes,
            fan_speed_hvac_modes=self._fan_speed_hvac_modes,
            min_temp=self._min_temp,
            max_temp=self._max_temp,
            target_temperature_step=self._target_temperature_step,
            min_range_temp=self._min_range_temp,
            max_range_temp=self._max_range_temp,
            target_temperature_range_step=self._target_temperature_range_step,
            min_humidity=self._min_humidity,
            max_humidity=self._max_humidity,
            temperature_unit=self._temperature_unit,
            set_power_func=self._set_power_func,
            set_operating_mode_func=self._set_operating_mode_func,
            set_target_temp_func=self._set_target_temp_func,
            set_target_temp_range_func=self._set_target_temp_range_func,
            set_target_humidity_func=self._set_target_humidity_func,
            set_fan_speed_func=self._set_fan_speed_func,
            translation_key=self._entity_translation_key,
            icon=self._icon,
        )


def _to_hvac_modes(
    modes: frozenset[str] | None,
) -> frozenset[HVACMode] | None:
    return None if modes is None else frozenset(HVACMode(m) for m in modes)


def _mode_allowed(
    mode: HVACMode | str | None, allowed: frozenset[HVACMode] | None
) -> bool:
    return allowed is None or mode in allowed


def _build_from_control(
    ctrl: controls.climate, builder: ClimateBuilder
) -> ClimateBuilder:
    return (
        builder.hvac_modes({HVACMode(k): v for k, v in ctrl.hvac_modes.items()})
        .fan_modes(dict(ctrl.fan_modes))
        .power_prop(ctrl.power_field)
        .target_temperature_prop(ctrl.target_temperature_field)
        .target_temperature_low_prop(ctrl.target_temperature_low_field)
        .target_temperature_high_prop(ctrl.target_temperature_high_field)
        .target_humidity_prop(ctrl.target_humidity_field)
        .current_temperature_prop(ctrl.current_temperature_field)
        .fan_speed_prop(ctrl.fan_speed_field)
        .target_temperature_hvac_modes(
            _to_hvac_modes(ctrl.target_temperature_hvac_modes)
        )
        .target_temperature_range_hvac_modes(
            _to_hvac_modes(ctrl.target_temperature_range_hvac_modes)
        )
        .target_humidity_hvac_modes(_to_hvac_modes(ctrl.target_humidity_hvac_modes))
        .fan_speed_hvac_modes(_to_hvac_modes(ctrl.fan_speed_hvac_modes))
        .min_temp(ctrl.min_temp)
        .max_temp(ctrl.max_temp)
        .target_temperature_step(ctrl.target_temperature_step)
        .min_range_temp(ctrl.min_range_temp)
        .max_range_temp(ctrl.max_range_temp)
        .target_temperature_range_step(ctrl.target_temperature_range_step)
        .min_humidity(ctrl.min_humidity)
        .max_humidity(ctrl.max_humidity)
        .temperature_unit(ctrl.temperature_unit)
        .set_power_func(ctrl.set_power)
        .set_operating_mode_func(ctrl.set_operating_mode)
        .set_target_temp_func(ctrl.set_target_temperature)
        .set_target_temp_range_func(ctrl.set_target_temperature_range)
        .set_target_humidity_func(ctrl.set_target_humidity)
        .set_fan_speed_func(ctrl.set_fan_speed)
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DeviceConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    device = entry.runtime_data
    entities = [
        EcoflowClimateEntity(
            device, _build_from_control(ctrl, ClimateBuilder.from_entity(ctrl)).build()
        )
        for ctrl in get_controls(device, controls.climate)
    ]
    if entities:
        async_add_entities(entities)


class EcoflowClimateEntity(EcoflowEntity, ClimateEntity):
    _enable_turn_on_off_backwards_compat = False

    def __init__(
        self,
        device: DeviceBase,
        description: EcoflowClimateEntityDescription,
    ) -> None:
        super().__init__(device)
        self.entity_description = description
        self._attr_unique_id = f"ef_{device.serial_number}_{description.key}"

        if description.translation_key is None:
            self._attr_translation_key = description.key

        self._min_temp = description.min_temp
        self._max_temp = description.max_temp
        self._target_temperature_step = description.target_temperature_step
        self._min_range_temp = description.min_range_temp
        self._max_range_temp = description.max_range_temp
        self._target_temperature_range_step = description.target_temperature_range_step
        self._min_humidity = description.min_humidity
        self._max_humidity = description.max_humidity
        self._attr_target_temperature_step = description.target_temperature_step
        self._attr_temperature_unit = description.temperature_unit

        base_features = ClimateEntityFeature(0)
        if description.set_power_func:
            base_features |= (
                ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF
            )
        self._base_features = base_features

        self._set_power = description.set_power_func
        self._set_operating_mode = description.set_operating_mode_func
        self._set_target_temp = description.set_target_temp_func
        self._set_target_temp_range = description.set_target_temp_range_func
        self._set_target_humidity = description.set_target_humidity_func
        self._set_fan_speed = description.set_fan_speed_func

        self._target_temperature_hvac_modes = description.target_temperature_hvac_modes
        self._target_temperature_range_hvac_modes = (
            description.target_temperature_range_hvac_modes
        )
        self._target_humidity_hvac_modes = description.target_humidity_hvac_modes
        self._fan_speed_hvac_modes = description.fan_speed_hvac_modes

        self._hvac_to_operating = description.hvac_mode_mapping
        self._operating_to_hvac: dict[Any, HVACMode] = {
            v: k for k, v in description.hvac_mode_mapping.items()
        }
        self._fan_to_speed = description.fan_mode_mapping
        self._speed_to_fan: dict[Any, str] = {
            v: k for k, v in description.fan_mode_mapping.items()
        }

        self._attr_hvac_modes = [HVACMode.OFF, *description.hvac_mode_mapping]
        self._attr_fan_modes = list(description.fan_mode_mapping)
        self._power_prop = description.power_prop

        power_prop = description.power_prop
        mode_prop = description.operating_mode_prop

        self._register_update_callback(
            "_attr_hvac_mode",
            power_prop,
            get_state=lambda state: (
                HVACMode.OFF
                if state is not True
                else self._operating_to_hvac.get(
                    getattr(self._device, mode_prop) if mode_prop else None
                )
            ),
        )
        self._register_update_callback(
            "_attr_hvac_mode",
            mode_prop,
            get_state=lambda state: (
                HVACMode.OFF
                if not power_prop or getattr(self._device, power_prop, None) is not True
                else self._operating_to_hvac.get(state)
            ),
        )
        self._register_update_callback(
            "_attr_target_temperature",
            description.target_temperature_prop,
        )
        self._register_update_callback(
            "_attr_target_temperature_low",
            description.target_temperature_low_prop,
        )
        self._register_update_callback(
            "_attr_target_temperature_high",
            description.target_temperature_high_prop,
        )
        self._register_update_callback(
            "_attr_target_humidity",
            description.target_humidity_prop,
            get_state=lambda state: int(state) if state is not None else self.SkipWrite,
        )
        self._register_update_callback(
            "_attr_current_temperature",
            description.current_temperature_prop,
        )
        self._register_update_callback(
            "_attr_fan_mode",
            description.fan_speed_prop,
            get_state=self._speed_to_fan.get,
        )

        self._update_supported_features()

    @callback
    def async_write_ha_state(self) -> None:
        self._update_supported_features()
        super().async_write_ha_state()

    def _update_supported_features(self) -> None:
        mode = self._attr_hvac_mode
        features = self._base_features

        if mode == HVACMode.OFF:
            self._attr_supported_features = features
            return

        if self._set_fan_speed is not None and _mode_allowed(
            mode, self._fan_speed_hvac_modes
        ):
            features |= ClimateEntityFeature.FAN_MODE

        if self._set_target_temp_range is not None and _mode_allowed(
            mode, self._target_temperature_range_hvac_modes
        ):
            features |= ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
            self._attr_target_temperature_step = self._target_temperature_range_step
            if self._min_range_temp is not None:
                self._attr_min_temp = self._min_range_temp
            if self._max_range_temp is not None:
                self._attr_max_temp = self._max_range_temp

        elif self._set_target_humidity is not None and _mode_allowed(
            mode, self._target_humidity_hvac_modes
        ):
            features |= ClimateEntityFeature.TARGET_HUMIDITY
            if self._min_humidity is not None:
                self._attr_min_humidity = self._min_humidity
            if self._max_humidity is not None:
                self._attr_max_humidity = self._max_humidity
        elif self._set_target_temp is not None and _mode_allowed(
            mode, self._target_temperature_hvac_modes
        ):
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
            self._attr_target_temperature_step = self._target_temperature_step
            if self._min_temp is not None:
                self._attr_min_temp = self._min_temp
            if self._max_temp is not None:
                self._attr_max_temp = self._max_temp

        self._attr_supported_features = features

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            if self._set_power:
                await self._set_power(self._device, False)
            return

        if (
            self._power_prop
            and getattr(self._device, self._power_prop, None) is not True
        ):
            if self._set_power:
                await self._set_power(self._device, True)

        operating = self._hvac_to_operating.get(hvac_mode)
        if operating is not None and self._set_operating_mode:
            await self._set_operating_mode(self._device, operating)

    async def async_set_temperature(self, **kwargs) -> None:
        if self._set_target_temp_range:
            if (low := kwargs.get(ATTR_TARGET_TEMP_LOW)) is not None and (
                high := kwargs.get(ATTR_TARGET_TEMP_HIGH)
            ) is not None:
                await self._set_target_temp_range(self._device, float(low), float(high))
                return

        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None and self._set_target_temp:
            await self._set_target_temp(self._device, float(temperature))

    async def async_set_humidity(self, humidity: int) -> None:
        if self._set_target_humidity is not None:
            await self._set_target_humidity(self._device, int(humidity))

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        speed = self._fan_to_speed.get(fan_mode)
        if speed is not None and self._set_fan_speed:
            await self._set_fan_speed(self._device, speed)

    async def async_turn_on(self) -> None:
        if self._set_power:
            await self._set_power(self._device, True)

    async def async_turn_off(self) -> None:
        if self._set_power:
            await self._set_power(self._device, False)
