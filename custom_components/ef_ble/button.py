"""EcoFlow BLE Button"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from functools import partial

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DeviceConfigEntry
from .description_builder import EntityDescriptionBuilder
from .eflib import DeviceBase, get_controls
from .eflib.entity import controls
from .entity import EcoflowEntity


@dataclass(frozen=True, kw_only=True)
class EcoflowButtonEntityDescription(ButtonEntityDescription):
    press_func: Callable[[DeviceBase], Awaitable]
    availability_prop: str | None = None


@dataclass(init=False)
class ButtonBuilder(EntityDescriptionBuilder):
    _press_func: Callable[[DeviceBase], Awaitable] | None = None

    def press_func(self, func: Callable[[DeviceBase], Awaitable]):
        self._press_func = func
        return self

    def build(self):
        if self._press_func is None:
            raise ValueError("Cannot build button entity without press func")
        return EcoflowButtonEntityDescription(
            key=self._entity_key,
            name=self._entity_name,
            entity_category=self._entity_category,
            press_func=self._press_func,
            entity_registry_enabled_default=self._entity_registry_enabled_default,
            translation_key=self._entity_translation_key,
            translation_placeholders=self._translation_placeholders,
            availability_prop=self._availability_prop,
            icon=self._icon,
        )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add buttons for passed config_entry in HA."""
    device = config_entry.runtime_data

    descriptions = [
        (ButtonBuilder.from_entity(button).press_func(button.press_func).build())
        for button in get_controls(device, controls.button)
    ]

    new_buttons = [EcoflowButton(device, desc) for desc in descriptions]
    if new_buttons:
        async_add_entities(new_buttons)


class EcoflowButton(EcoflowEntity, ButtonEntity):
    def __init__(
        self, device: DeviceBase, entity_description: EcoflowButtonEntityDescription
    ):
        super().__init__(device)

        self._attr_unique_id = f"ef_{device.serial_number}_{entity_description.key}"
        self._prop_name = entity_description.key
        self.entity_description = entity_description
        self._availability_prop = entity_description.availability_prop

        if entity_description.translation_key is None:
            self._attr_translation_key = self.entity_description.key

        self._register_update_callback(
            entity_attr="_attr_available",
            prop_name=self._availability_prop,
            get_state=lambda state: state if state is not None else self.SkipWrite,
        )

        self._press = partial(entity_description.press_func, device)

    @callback
    def availability_updated(self, state: bool):
        self._attr_available = state
        self.async_write_ha_state()

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._press()
