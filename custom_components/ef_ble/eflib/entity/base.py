import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..props.updatable_props import Field


@dataclasses.dataclass
class EntityType:
    field: "Field" = dataclasses.field(hash=False)

    enabled: bool = dataclasses.field(default=True, kw_only=True)

    @property
    def key(self):
        return self.field.public_name


type EntityKind = type[EntityType] | EntityType
