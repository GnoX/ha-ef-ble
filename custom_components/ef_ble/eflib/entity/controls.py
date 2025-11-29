import dataclasses
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from .base import EntityType

if TYPE_CHECKING:
    from ..devicebase import DeviceBase
    from ..props import Field


class ControlType(EntityType):
    pass


@dataclasses.dataclass
class Toggle(ControlType):
    type SwitchFunc[E: "DeviceBase"] = Callable[[E, bool], Awaitable[None]]

    field: "Field[bool]"
    enable_func: SwitchFunc


@dataclasses.dataclass
class Outlet(Toggle):
    pass


@dataclasses.dataclass
class Switch(Toggle):
    pass
