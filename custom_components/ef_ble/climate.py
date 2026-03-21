"""EcoFlow BLE climate entity for Wave 3."""

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DeviceConfigEntry
from .eflib.devices import wave3
from .entity import EcoflowEntity

_HVAC_MODE_TO_OPERATING = {
    HVACMode.COOL: wave3.OperatingMode.COOLING,
    HVACMode.HEAT: wave3.OperatingMode.HEATING,
    HVACMode.FAN_ONLY: wave3.OperatingMode.VENTING,
    HVACMode.DRY: wave3.OperatingMode.DEHUMIDIFYING,
    HVACMode.AUTO: wave3.OperatingMode.THERMOSTATIC,
}

_OPERATING_TO_HVAC_MODE = {v: k for k, v in _HVAC_MODE_TO_OPERATING.items()}

_FAN_MODE_MAP = {
    "low": wave3.FanSpeed.LOW,
    "medium_low": wave3.FanSpeed.MEDIUM_LOW,
    "medium": wave3.FanSpeed.MEDIUM,
    "medium_high": wave3.FanSpeed.MEDIUM_HIGH,
    "high": wave3.FanSpeed.HIGH,
}

_FAN_SPEED_TO_MODE = {v: k for k, v in _FAN_MODE_MAP.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    device = entry.runtime_data
    if isinstance(device, wave3.Device):
        async_add_entities([EcoflowClimateEntity(device)])


class EcoflowClimateEntity(EcoflowEntity, ClimateEntity):

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 1.0
    _attr_min_temp = 16.0
    _attr_max_temp = 30.0
    _attr_fan_modes = list(_FAN_MODE_MAP.keys())
    _attr_hvac_modes = [
        HVACMode.OFF,
        HVACMode.COOL,
        HVACMode.HEAT,
        HVACMode.FAN_ONLY,
        HVACMode.DRY,
        HVACMode.AUTO,
    ]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    _enable_turn_on_off_backwards_compat = False

    def __init__(self, device: wave3.Device) -> None:
        super().__init__(device)
        self._device: wave3.Device = device
        self._attr_unique_id = f"ef_{device.serial_number}_climate"
        self._attr_translation_key = "climate"

    async def async_added_to_hass(self) -> None:
        self._device.register_state_update_callback(self._on_power, "power")
        self._device.register_state_update_callback(
            self._on_operating_mode, "operating_mode"
        )
        self._device.register_state_update_callback(
            self._on_target_temperature, "target_temperature"
        )
        self._device.register_state_update_callback(
            self._on_current_temperature, "ambient_temperature"
        )
        self._device.register_state_update_callback(self._on_fan_speed, "fan_speed")
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self) -> None:
        self._device.remove_state_update_calback(self._on_power, "power")
        self._device.remove_state_update_calback(
            self._on_operating_mode, "operating_mode"
        )
        self._device.remove_state_update_calback(
            self._on_target_temperature, "target_temperature"
        )
        self._device.remove_state_update_calback(
            self._on_current_temperature, "ambient_temperature"
        )
        self._device.remove_state_update_calback(self._on_fan_speed, "fan_speed")
        await super().async_will_remove_from_hass()

    # -- state callbacks -------------------------------------------------------

    @callback
    def _on_power(self, state):
        self.async_write_ha_state()

    @callback
    def _on_operating_mode(self, state):
        self.async_write_ha_state()

    @callback
    def _on_target_temperature(self, state):
        self.async_write_ha_state()

    @callback
    def _on_current_temperature(self, state):
        self.async_write_ha_state()

    @callback
    def _on_fan_speed(self, state):
        self.async_write_ha_state()

    # -- properties ------------------------------------------------------------

    @property
    def hvac_mode(self) -> HVACMode | None:
        if self._device.power is not True:
            return HVACMode.OFF
        mode = self._device.operating_mode
        if mode is None:
            return None
        return _OPERATING_TO_HVAC_MODE.get(mode)

    @property
    def current_temperature(self) -> float | None:
        return self._device.ambient_temperature

    @property
    def target_temperature(self) -> float | None:
        return self._device.target_temperature

    @property
    def fan_mode(self) -> str | None:
        speed = self._device.fan_speed
        if speed is None:
            return None
        return _FAN_SPEED_TO_MODE.get(speed)

    # -- commands --------------------------------------------------------------

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            await self._device.enable_power(False)
            return

        if self._device.power is not True:
            await self._device.enable_power(True)

        operating = _HVAC_MODE_TO_OPERATING.get(hvac_mode)
        if operating is not None:
            await self._device.set_operating_mode(operating)

    async def async_set_temperature(self, **kwargs) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            await self._device.set_target_temperature(float(temperature))

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        speed = _FAN_MODE_MAP.get(fan_mode)
        if speed is not None:
            await self._device.set_fan_speed(speed)

    async def async_turn_on(self) -> None:
        await self._device.enable_power(True)

    async def async_turn_off(self) -> None:
        await self._device.enable_power(False)
