"""EcoFlow BLE climate entities."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityDescription,
)
from homeassistant.components.climate.const import ClimateEntityFeature, HVACMode
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DeviceConfigEntry
from .eflib import DeviceBase
from .eflib.devices import wave3
from .entity import EcoflowEntity


@dataclass(frozen=True, kw_only=True)
class EcoflowClimateEntityDescription[T: DeviceBase](ClimateEntityDescription):
    hvac_mode_mapping: dict[HVACMode, Any] = field(default_factory=dict)
    fan_mode_mapping: dict[str, Any] = field(default_factory=dict)

    power_prop: str | None = None
    operating_mode_prop: str | None = None
    target_temperature_prop: str | None = None
    current_temperature_prop: str | None = None
    fan_speed_prop: str | None = None
    min_temp_prop: str | None = None
    max_temp_prop: str | None = None

    min_temp: float | None = None
    max_temp: float | None = None
    temperature_step: float = 1.0
    temperature_unit: str = UnitOfTemperature.CELSIUS

    climate_features: ClimateEntityFeature = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )

    async_set_power: Callable[[T, bool], Awaitable] | None = None
    async_set_operating_mode: Callable[[T, Any], Awaitable] | None = None
    async_set_target_temp: Callable[[T, float], Awaitable] | None = None
    async_set_fan_speed: Callable[[T, Any], Awaitable] | None = None


CLIMATE_TYPES: dict[str, EcoflowClimateEntityDescription] = {
    "operating_mode": EcoflowClimateEntityDescription[wave3.Device](
        key="climate",
        power_prop="power",
        operating_mode_prop="operating_mode",
        target_temperature_prop="target_temperature_climate",
        current_temperature_prop="ambient_temperature",
        fan_speed_prop="fan_speed_climate",
        hvac_mode_mapping={
            HVACMode.COOL: wave3.OperatingMode.COOLING,
            HVACMode.HEAT: wave3.OperatingMode.HEATING,
            HVACMode.FAN_ONLY: wave3.OperatingMode.VENTING,
            HVACMode.DRY: wave3.OperatingMode.DEHUMIDIFYING,
            HVACMode.AUTO: wave3.OperatingMode.THERMOSTATIC,
        },
        fan_mode_mapping={
            "low": wave3.FanSpeed.LOW,
            "medium_low": wave3.FanSpeed.MEDIUM_LOW,
            "medium": wave3.FanSpeed.MEDIUM,
            "medium_high": wave3.FanSpeed.MEDIUM_HIGH,
            "high": wave3.FanSpeed.HIGH,
        },
        async_set_power=lambda device, enabled: device.enable_power(enabled),
        async_set_operating_mode=lambda device, mode: device.set_operating_mode(mode),
        async_set_target_temp=lambda device, temp: device.set_target_temperature(temp),
        async_set_fan_speed=lambda device, speed: device.set_fan_speed(speed),
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DeviceConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    device = entry.runtime_data
    entities = [
        EcoflowClimateEntity(device, description)
        for attr, description in CLIMATE_TYPES.items()
        if hasattr(device, attr)
    ]
    if entities:
        async_add_entities(entities)


class EcoflowClimateEntity(EcoflowEntity, ClimateEntity):
    _enable_turn_on_off_backwards_compat = False

    def __init__(
        self,
        device: DeviceBase,
        description: EcoflowClimateEntityDescription[DeviceBase],
    ) -> None:
        super().__init__(device)
        self.entity_description = description
        self._attr_unique_id = f"ef_{device.serial_number}_{description.key}"

        if description.translation_key is None:
            self._attr_translation_key = description.key

        self._attr_temperature_unit = description.temperature_unit
        self._attr_target_temperature_step = description.temperature_step
        self._attr_supported_features = description.climate_features

        self._power_prop = description.power_prop
        self._set_power = description.async_set_power
        self._set_operating_mode = description.async_set_operating_mode
        self._set_target_temp = description.async_set_target_temp
        self._set_fan_speed = description.async_set_fan_speed

        self._register_update_callback(
            "_attr_min_temp",
            description.min_temp_prop,
        )
        self._register_update_callback(
            "_attr_max_temp",
            description.max_temp_prop,
        )

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

        operating_mode_prop = description.operating_mode_prop
        power_prop = self._power_prop

        self._register_update_callback(
            "_attr_hvac_mode",
            power_prop,
            get_state=lambda state: (
                HVACMode.OFF
                if state is not True
                else self._operating_to_hvac.get(
                    getattr(self._device, operating_mode_prop)
                    if operating_mode_prop
                    else None
                )
            ),
        )
        self._register_update_callback(
            "_attr_hvac_mode",
            operating_mode_prop,
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
            "_attr_current_temperature",
            description.current_temperature_prop,
        )
        self._register_update_callback(
            "_attr_fan_mode",
            description.fan_speed_prop,
            get_state=self._speed_to_fan.get,
        )

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
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None and self._set_target_temp:
            await self._set_target_temp(self._device, float(temperature))

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
