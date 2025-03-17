from dataclasses import dataclass
from typing import Any, ClassVar


class UpdatableProps:
    """
    Mixin for augmenting device classes with advanced properties

    If any property changed its value after calling `reset_updated`, attribute
    `updated` is set to True and all updated field names are added to
    `updated_fields`.

    Attributes
    ----------
    updated
        Holds True if any fields are updated after calling `reset_updated`
    """

    updated: bool = False
    _updated_fields: list[str] | None = None

    @property
    def updated_fields(self):
        """List of field names that were updated after calling `reset_updated`"""
        if self._updated_fields is None:
            self._updated_fields = []
        return self._updated_fields

    @updated_fields.setter
    def updated_fields(self, value: list[str]):
        self._updated_fields = value

    _fields: ClassVar[list["Field[Any]"]] = []

    def reset_updated(self):
        self.updated = False
        self.updated_fields = []


@dataclass(kw_only=True)
class Field[T]:
    """Descriptor for updating values only if they changed"""

    def __set_name__[T_PROPS: UpdatableProps](self, owner: type[T_PROPS], name: str):
        self.public_name = name
        self.private_name = f"_{name}"
        owner._fields = owner._fields + [self]

    def __set__(self, instance, value: Any):
        self._set_value(instance, value)

    def _set_value(self, instance, value):
        if not isinstance(instance, UpdatableProps):
            raise TypeError(
                f"Descriptor {self.__class__.__name__} can only be used on subclasses "
                f"of {UpdatableProps.__name__}"
            )

        if value == getattr(instance, self.public_name):
            return

        setattr(instance, self.private_name, value)
        instance.updated = True
        instance.updated_fields.append(self.public_name)

    def __get__(
        self, instance: UpdatableProps, owner: type[UpdatableProps]
    ) -> T | None:
        return getattr(instance, self.private_name, None)
