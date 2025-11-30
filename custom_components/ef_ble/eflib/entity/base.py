import dataclasses
from collections.abc import Callable
from typing import TYPE_CHECKING, dataclass_transform

if TYPE_CHECKING:
    from ..props.updatable_props import Field


@dataclasses.dataclass
@dataclass_transform(field_specifiers=(dataclasses.field,))
class EntityType:
    field: "Field" = dataclasses.field(hash=False)

    enabled: bool = dataclasses.field(default=True, kw_only=True)

    @property
    def key(self):
        return self.field.public_name

    def __init_subclass__(cls) -> None:
        dataclasses.dataclass(cls)


type EntityKind = type[EntityType] | EntityType


@dataclasses.dataclass
class DynamicValue[F, T]:
    field: "Field[F]"
    transform: Callable[[F], T] | None = None


def dynamic[F, T](field: "Field[F]", transform: Callable[[F], T] | None = None) -> T:
    return DynamicValue(field, transform)  # pyright: ignore[reportReturnType]
