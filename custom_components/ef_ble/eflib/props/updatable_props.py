import inspect
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Self, overload

if TYPE_CHECKING:
    from ..entity import controls, sensors
    from ..entity.base import EntityKind, EntityType


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

    _sensors: list["sensors.SensorType | sensors.BinarySensorType"] | None = None
    _controls: list["controls.Switch"]

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

    def _get_entities[E: "EntityType"](
        self, sensor_type: type[E], collection_attr: str
    ) -> list[E]:
        if getattr(self, collection_attr) is None:
            return []

        return [
            item
            for cls in inspect.getmro(type(self))
            if cls.__dict__.get(collection_attr)
            for item in cls.__dict__.get(collection_attr, [])
            if isinstance(item, sensor_type)
        ]

    def get_sensors[E: "EntityType"](self, sensor_type: type[E]):
        return self._get_entities(sensor_type, "_sensors")

    def get_controls[E: "controls.ControlType"](self, control_type: type[E]):
        return self._get_entities(control_type, "_controls")


@dataclass(kw_only=True)
class Field[T]:
    """Descriptor for updating values only if they changed"""

    sensor_type: "EntityType | None" = field(default=None, repr=False, init=False)

    def __set_name__[T_PROPS: UpdatableProps](self, owner: type[T_PROPS], name: str):
        self.public_name = name
        self.private_name = f"_{name}"
        owner._fields = [*owner._fields, self]

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

        setattr(instance, self.private_name, self._transform_value(value))
        instance.updated = True
        instance.updated_fields.append(self.public_name)

    @property
    def _transform_value(self):
        return getattr(self, "_transform", lambda x: x)

    @_transform_value.setter
    def _transform_value(self, value: Callable[[Any], Any] | None = None):
        if value is None:
            return

        setattr(self, "_transform", value)

    @overload
    def __get__(self, instance: None, owner: type[UpdatableProps]) -> Self: ...

    @overload
    def __get__(
        self, instance: UpdatableProps, owner: type[UpdatableProps]
    ) -> T | None: ...

    @overload
    def __get__(self, instance: Any, owner: Any) -> Self: ...

    def __get__(
        self, instance: UpdatableProps | None, owner: type[UpdatableProps]
    ) -> T | Self | None:
        if instance is None:
            return self
        if not isinstance(instance, UpdatableProps):
            return self

        return getattr(instance, self.private_name, None)

    def sensor(
        self,
        sensor: "EntityKind",
        db_precision: int | None = None,
    ) -> Self:
        """
        Mark this field as sensor type

        Parameters
        ----------
        sensor
            Sensor type
        db_precision, optional
            Floating point precision to use for writing to db, by default None

        Returns
        -------
        Same field
        """
        if db_precision is not None:

            def _transform_precision(value: Any) -> T:
                return round(value, db_precision)

            self._transform_value = _transform_precision

        if isinstance(sensor, type):
            sensor = sensor()

        self.sensor_type = sensor
        return self
