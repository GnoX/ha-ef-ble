import dataclasses
from collections.abc import Callable
from typing import Any

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DeviceConfigEntry
from .description_builder import EcoflowSwitchEntityDescription, SwitchBuilder
from .eflib import DeviceBase, controls, get_controls
from .entity import EcoflowEntity

# SWITCH_TYPES = [
#     SwitchEntityDescription(
#         key="dc_12v_port",
#         name="DC 12V Port",
#         device_class=SwitchDeviceClass.OUTLET,
#     ),
#     SwitchEntityDescription(
#         key="ac_ports",
#         name="AC Ports",
#         device_class=SwitchDeviceClass.OUTLET,
#     ),
#     SwitchEntityDescription(
#         key="ac_port",
#         name="AC Port",
#         device_class=SwitchDeviceClass.OUTLET,
#     ),
#     SwitchEntityDescription(
#         key="self_start",
#         name="Self Start",
#     ),
#     SwitchEntityDescription(
#         key="ac_lv_port",
#         name="LV AC",
#         device_class=SwitchDeviceClass.OUTLET,
#     ),
#     SwitchEntityDescription(
#         key="ac_hv_port",
#         name="HV AC",
#         device_class=SwitchDeviceClass.OUTLET,
#     ),
#     SwitchEntityDescription(
#         key="energy_backup",
#         name="Backup Reserve",
#         device_class=SwitchDeviceClass.SWITCH,
#         translation_key="battery_sync",
#     ),
#     SwitchEntityDescription(
#         key="usb_ports",
#         name="USB Ports",
#         icon="mdi:usb",
#     ),
#     SwitchEntityDescription(
#         key="engine_on",
#         name="Engine",
#     ),
#     SwitchEntityDescription(
#         key="charger_open",
#         name="Charger",
#     ),
#     SwitchEntityDescription(
#         key="lpg_level_monitoring",
#         name="LPG Level Monitoring",
#     ),
#     SwitchEntityDescription(
#         key="ac_1",
#         name="AC (1)",
#         device_class=SwitchDeviceClass.OUTLET,
#     ),
#     SwitchEntityDescription(
#         key="ac_2",
#         name="AC (2)",
#         device_class=SwitchDeviceClass.OUTLET,
#     ),
#     SwitchEntityDescription(
#         key="feed_grid",
#         name="Feed Grid",
#     ),
#     SwitchEntityDescription(
#         key="power",
#         name="Power",
#         device_class=SwitchDeviceClass.SWITCH,
#     ),
# ]


@dataclasses.dataclass
class Builder[E: controls.ControlType]:
    builder: Callable[[E, SwitchBuilder], SwitchBuilder]


type BuilderDict[E: controls.ControlType] = dict[type[E], Builder[E]]

BUILDERS: BuilderDict = {
    controls.Outlet: Builder[controls.Outlet](
        lambda outlet, builder: builder.device_class(SwitchDeviceClass.OUTLET)
    ),
    controls.Switch: Builder[controls.Switch](
        lambda switch, builder: builder.device_class(SwitchDeviceClass.SWITCH)
    ),
    controls.Toggle: Builder[controls.Toggle](lambda toggle, builder: builder),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    device = entry.runtime_data

    switches = [
        EcoflowSwitchEntity(
            device,
            (
                BUILDERS[switch.__class__]
                .builder(
                    switch,
                    SwitchBuilder.from_entity(switch).enable_func(switch.enable_func),
                )
                .build()
            ),
        )
        for switch in get_controls(device, controls.Toggle)
    ]

    if switches:
        async_add_entities(switches)


class EcoflowSwitchEntity(EcoflowEntity, SwitchEntity):
    def __init__(
        self, device: DeviceBase, entity_description: SwitchEntityDescription
    ) -> None:
        super().__init__(device)

        self._attr_unique_id = f"{device.name}_{entity_description.key}"
        self._prop_name = entity_description.key
        self.entity_description = entity_description
        self._on_off_state = False

        if not isinstance(entity_description, EcoflowSwitchEntityDescription):
            raise TypeError(
                "EntityDescription must be of type EcoflowSwitchEntityDescription"
            )

        self._enable_method = entity_description.enable

        if entity_description.translation_key is None:
            self._attr_translation_key = self.entity_description.key

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._enable_method(self._device, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._enable_method(self._device, False)

    async def async_added_to_hass(self) -> None:
        self._device.register_state_update_callback(self.state_updated, self._prop_name)
        await super().async_added_to_hass()

    @callback
    def state_updated(self, state: bool | None):
        self._on_off_state = state
        self.async_write_ha_state()

    @property
    def available(self):
        return self._device.is_connected and self._on_off_state is not None

    @property
    def is_on(self):
        return self._on_off_state if self._on_off_state is not None else False
