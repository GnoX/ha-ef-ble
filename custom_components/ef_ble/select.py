from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.ef_ble.eflib import DeviceBase

from . import DeviceConfigEntry
from .eflib.devices import river3, river3_plus, stream_ac
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
        options=river3.DcChargingType.options(include_unknown=False),
        set_state=(
            lambda device, value: device.set_dc_charging_type(
                river3.DcChargingType[value.upper()]
            )
        ),
    ),
    EcoflowSelectEntityDescription[stream_ac.Device](
        key="energy_strategy",
        name="Energy Strategy",
        options=stream_ac.EnergyStrategy.options(include_unknown=False),
        set_state=(
            lambda device, value: device.set_energy_strategy(
                stream_ac.EnergyStrategy[value.upper()]
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

        self._register_update_callback(
            entity_attr="_attr_current_option",
            prop_name=self._prop_name,
            get_state=(
                lambda value: value.name.lower()
                if value is not None
                else self.SkipWrite
            ),
        )

    async def async_select_option(self, option: str) -> None:
        if self._set_state is not None:
            await self._set_state(self._device, option)
            return

        await super().async_select_option(option)
