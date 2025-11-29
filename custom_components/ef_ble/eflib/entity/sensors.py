import dataclasses
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from ..props.enums import IntFieldValue
from .base import EntityType

if TYPE_CHECKING:
    from ..devicebase import DeviceBase
    from ..props import Field


class SensorType(EntityType):
    pass


class BinarySensorType(EntityType):
    pass


@dataclasses.dataclass
class Battery(SensorType):
    precision: int = 0


@dataclasses.dataclass
class Power(SensorType):
    class Unit(enum.Enum):
        WATT = "WATT"

    precision: int = 0
    unit: Unit = Unit.WATT


@dataclasses.dataclass
class Energy(SensorType):
    precision: int = 3


@dataclasses.dataclass
class DynamicValue[F, T]:
    field: "Field[F]"
    transform: Callable[[F], T]


def depends[F, T](field: "Field[F]", transform: Callable[[F], T]) -> T:
    return DynamicValue(field, transform)  # pyright: ignore[reportReturnType]


type DynamicUnit[E: "DeviceBase"] = Callable[[E], str]


@dataclasses.dataclass
class Temperature(SensorType):
    class Unit(enum.Enum):
        C = "C"
        F = "F"

    precision: int = 1
    unit: Unit | DynamicUnit = Unit.C


@dataclasses.dataclass
class Enum(SensorType):
    options: list[str]

    @classmethod
    def from_enum(cls, field: "Field", enum_cls: type[IntFieldValue]):
        return cls(field=field, options=[item.name.lower() for item in enum_cls])


type SensorUnit = Power.Unit | Temperature.Unit


@dataclasses.dataclass
class Plug(BinarySensorType):
    pass


@dataclasses.dataclass
class Problem(BinarySensorType):
    pass
