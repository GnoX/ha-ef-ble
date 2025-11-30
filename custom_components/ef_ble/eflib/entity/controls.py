import dataclasses
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, Concatenate

from . import units
from .base import EntityType

if TYPE_CHECKING:
    from ..devicebase import DeviceBase
    from ..props import Field


class ControlType(EntityType):
    pass


@dataclasses.dataclass
class Toggle(ControlType):
    type SwitchFunc[D: "DeviceBase"] = Callable[[D, bool], Awaitable[None]]

    field: "Field[bool]"
    enable_func: SwitchFunc


class Outlet(Toggle):
    pass


class Switch(Toggle):
    pass


class NumberType(ControlType):
    type ValueFunc[D: "DeviceBase", N] = Callable[[D, N], Awaitable[None]]

    set_value_func: ValueFunc
    max: float | None = None
    min: float = 0
    step: float = 1.0

    availability: "Field[bool] | None" = None


class Number:
    class Power(NumberType):
        unit: units.Power = units.Power.WATT

    class Battery(NumberType):
        pass

    class Current(NumberType):
        unit: units.Current = units.Current.AMPERE


def switch(field: "Field[bool]"):
    def _switch[D: "DeviceBase"](func: Callable[[D, bool], Awaitable[None]]):
        field.sensor(Switch(field, enable_func=func))
        return func

    return _switch


def _make_number_decorator[**P, D: "DeviceBase"](
    number_type: Callable[
        Concatenate["Field", Callable[[D, int], Awaitable[None]], P], Any
    ],
):
    def number_decorator(
        field: "Field[int]",
        *args: P.args,
        **kwargs: P.kwargs,
    ):
        def wrapper(func: Callable[[D, int], Awaitable[None]]):
            field.sensor(number_type(field, func, *args, **kwargs))
            return func

        return wrapper

    return number_decorator


power = _make_number_decorator(Number.Power)
battery = _make_number_decorator(Number.Battery)
current = _make_number_decorator(Number.Current)
