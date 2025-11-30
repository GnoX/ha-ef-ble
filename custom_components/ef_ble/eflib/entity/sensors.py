from collections.abc import Callable
from typing import TYPE_CHECKING

from ..props.enums import IntFieldValue
from . import EntityType, units

if TYPE_CHECKING:
    from ..devicebase import DeviceBase
    from ..props import Field


class SensorType(EntityType):
    pass


class BinarySensorType(EntityType):
    pass


class Battery(SensorType):
    precision: int = 0


class Power(SensorType):
    precision: int = 0
    unit: units.Power = units.Power.WATT


class Energy(SensorType):
    precision: int = 3


type DynamicUnit[E: "DeviceBase"] = Callable[[E], units.Unit]


class Temperature(SensorType):
    precision: int = 1
    unit: units.Temperature | DynamicUnit = units.Temperature.C


class Enum(SensorType):
    options: list[str]

    @classmethod
    def from_enum(cls, field: "Field", enum_cls: type[IntFieldValue]):
        return cls(field=field, options=[item.name.lower() for item in enum_cls])


class Plug(BinarySensorType):
    pass


class Problem(BinarySensorType):
    pass
