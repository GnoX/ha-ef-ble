from typing import Any

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DeviceConfigEntry
from .eflib import DeviceBase
from .entity import EcoflowEntity

SWITCH_TYPES = [
    SwitchEntityDescription(
        key="dc_12v_port",
        name="DC 12V Port",
        device_class=SwitchDeviceClass.OUTLET,
    ),
    SwitchEntityDescription(
        key="ac_ports",
        name="AC Ports",
        device_class=SwitchDeviceClass.OUTLET,
    ),
    SwitchEntityDescription(
        key="energy_backup",
        name="Backup Reserve",
        device_class=SwitchDeviceClass.SWITCH,
    )
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    device = entry.runtime_data

    switches = [
        EcoflowSwitchEntity(device, switch_desc)
        for switch_desc in SWITCH_TYPES
        if hasattr(device, switch_desc.key)
        and hasattr(device, f"enable_{switch_desc.key}")
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
        self._method_name = f"enable_{self._prop_name}"
        self.entity_description = entity_description
        self._on_off_state = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        await getattr(self._device, self._method_name)(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await getattr(self._device, self._method_name)(False)

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
