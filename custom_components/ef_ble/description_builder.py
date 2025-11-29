from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Self

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntityDescription
from homeassistant.const import EntityCategory, UnitOfPower, UnitOfTemperature

from .eflib import DeviceBase, sensors
from .eflib.entity.base import EntityType
from .eflib.props import Field
from .sensor import SensorEntityDescription

_UPPER_WORDS = ["ac", "dc"]


@dataclass(frozen=True, kw_only=True)
class EcoflowSensorEntityDescription[Device: DeviceBase](SensorEntityDescription):
    state_attribute_fields: list[str] = field(default_factory=list)
    native_unit_of_measurement_field: Callable[[Device], str] | None = None


class EntityDescriptionBuilder:
    def __init__(self, field: "Field | None" = None):
        self._field = field
        self._name = None
        self._key = None
        self._device_class = None
        self._icon = None
        self._translation_key = None
        self._entity_registry_enabled_default = True

    @classmethod
    def from_entity(cls, entity: EntityType):
        return cls(entity.field).key(entity.key).enabled(entity.enabled)

    def field(self, field: "Field") -> Self:
        self._field = field
        return self

    def name(self, name: str) -> Self:
        self._name = name
        return self

    def key(self, key: str) -> Self:
        self._key = key
        return self

    def icon(self, icon: str):
        self._icon = icon
        return self

    def enabled(self, enabled: bool = True):
        self._entity_registry_enabled_default = enabled
        return self

    def translation_key(self, translation_key: str):
        self._translation_key = translation_key
        return self

    @property
    def _entity_key(self):
        if self._key is not None:
            return self._key

        if self._field is None:
            raise ValueError("Cannot create sensor key without field")

        return self._field.public_name

    @property
    def _entity_name(self):
        if self._name is not None:
            return self._name

        if self._field is None:
            raise ValueError("Cannot create default sensor name without field")

        return " ".join(
            [
                word.upper() if word in _UPPER_WORDS else word.capitalize()
                for word in self._entity_key.split("_")
            ]
        )

    @property
    def _entity_translation_key(self):
        if self._translation_key is not None:
            return self._translation_key

        if self._field is None:
            raise ValueError("Cannot create default translation key without field")

        return self._entity_key


class SensorBuilder(EntityDescriptionBuilder):
    def __init__(self, field: "Field"):
        super().__init__(field)
        self._native_unit_of_measurement = None
        self._state_class = None
        self._icon = None
        self._suggested_display_precision = None
        self._suggested_unit_of_measurement = None
        self._native_unit_of_measurement_field = None
        self._options = None

    def device_class(self, device_class: SensorDeviceClass):
        self._device_class = device_class
        return self

    def state_class(self, state_class: SensorStateClass):
        self._state_class = state_class
        return self

    def native_unit_of_measurement(
        self, unit: str | sensors.SensorUnit | sensors.DynamicUnit
    ):
        if isinstance(unit, sensors.DynamicValue):
            self._native_unit_of_measurement_field = lambda dev: unit_to_hassunit(
                unit.transform(getattr(dev, unit.field.public_name))
            )
            return self

        if isinstance(unit, Callable):
            self._native_unit_of_measurement_field = lambda dev: unit_to_hassunit(
                unit(dev)
            )
            return self

        if isinstance(unit, Field):
            self._native_unit_of_measurement_field = unit.public_name
            return self

        self._native_unit_of_measurement = unit_to_hassunit(unit)
        return self

    def suggested_display_precision(self, precision: int):
        self._suggested_display_precision = precision
        return self

    def suggested_unit_of_measurement(self, unit: str):
        self._suggested_unit_of_measurement = unit
        return self

    def options(self, options: list[str]):
        self._options = options
        return self

    def build(self) -> SensorEntityDescription:
        if self._field is None:
            raise ValueError("Cannot build sensor entity without field")

        return EcoflowSensorEntityDescription(
            key=self._entity_key,
            name=self._entity_name,
            device_class=self._device_class,
            state_class=self._state_class,
            native_unit_of_measurement=self._native_unit_of_measurement,
            native_unit_of_measurement_field=self._native_unit_of_measurement_field,
            options=self._options,
            suggested_display_precision=self._suggested_display_precision,
            suggested_unit_of_measurement=self._suggested_unit_of_measurement,
            translation_key=self._entity_translation_key,
            entity_registry_enabled_default=self._entity_registry_enabled_default,
        )


class BinarySensorBuilder(EntityDescriptionBuilder):
    def __init__(self, field: "Field"):
        super().__init__(field)
        self._device_class = None
        self._entity_category = None

    def device_class(self, device_class: BinarySensorDeviceClass):
        self._device_class = device_class
        return self

    def plug(self):
        self._device_class = BinarySensorDeviceClass.PLUG
        return self

    def entity_category(self, entity_category: EntityCategory):
        self._entity_category = entity_category
        return self

    def build(self):
        return BinarySensorEntityDescription(
            key=self._entity_key,
            name=self._entity_name,
            device_class=self._device_class,
            entity_category=self._entity_category,
            entity_registry_enabled_default=self._entity_registry_enabled_default,
            translation_key=self._entity_translation_key,
        )


@dataclass(frozen=True, kw_only=True)
class EcoflowSwitchEntityDescription(SwitchEntityDescription):
    enable: Callable[[DeviceBase, bool], Awaitable[None]]


class SwitchBuilder(EntityDescriptionBuilder):
    def __init__(self, field: "Field"):
        super().__init__(field)
        self._device_class = None
        self._entity_category = None
        self._enable_func = None

    def device_class(self, device_class: SwitchDeviceClass):
        self._device_class = device_class
        return self

    def enable_func(self, func: Callable[[DeviceBase, bool], Awaitable[None]]):
        self._enable_func = func
        return self

    def build(self):
        if self._enable_func is None:
            raise ValueError("Cannot build switch entity without enable func")

        return EcoflowSwitchEntityDescription(
            key=self._entity_key,
            name=self._entity_name,
            device_class=self._device_class,
            entity_category=self._entity_category,
            enable=self._enable_func,
            entity_registry_enabled_default=self._entity_registry_enabled_default,
            translation_key=self._entity_translation_key,
            icon=self._icon,
        )


def unit_to_hassunit(unit: str | sensors.Power.Unit | sensors.Temperature.Unit):
    match unit:
        case sensors.Power.Unit.WATT:
            return UnitOfPower.WATT
        case sensors.Temperature.Unit.C:
            return UnitOfTemperature.CELSIUS
        case sensors.Temperature.Unit.F:
            return UnitOfTemperature.FAHRENHEIT
        case str():
            return unit
