import abc
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from google.protobuf.message import Message


class UpdatableProps:
    """
    Mixin for augmenting device classes with advanced properties

    If any property changed its value after calling ``update_fields``, attribute
    ``updated`` is set to True and all updated field names are added to
    ``updated_fields``.

    Attributes
    ----------
    updated
        Holds True if any fields are updated in ``update_fields``
    updated_fields
        List of field names that were updated after calling ``update_fields``
    """

    updated: bool = False
    updated_fields: list[str] = []

    _pb_field_names: list[str] = []
    _pb_list_field_names: list[str] = []
    _list_field_name_to_field: dict[str, "ProtobufListField"] = {}

    def update_fields(self, message: Message):
        """
        Update all defined fields and return names of updated fields

        Parameters
        ----------
        message
            Parsed protobuf message to assign to updated fields
        """
        self.updated = False
        self.updated_fields = []

        for field_name in self._pb_field_names:
            setattr(self, field_name, message)

        for list_field_name, field in self._list_field_name_to_field.items():
            if not message.HasField(list_field_name):
                continue

            for item in field.get_list(getattr(message, list_field_name)):
                for pb_list_field_name in self._pb_list_field_names:
                    setattr(self, pb_list_field_name, item)


@dataclass(kw_only=True)
class Field[T]:
    """
    Descriptor for updating values only if they changed

    Using this field is basically the same as the following code:

        class Device:
            _field = None

            @property
            def field(self):
                return self._field

            def parse(self):
                value = parse_value()
                if value != self._field:
                    self._field = value
                    self.updated = True
                    self.updated_fields.append("field")
    """

    def __set_name__(self, owner: type[UpdatableProps], name: str):
        self.public_name = name
        self.private_name = f"_{name}"

    def __set__(self, instance: UpdatableProps, value: Any):
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


@dataclass
class ProtobufField[T](Field[T]):
    """
    Descriptor for field that assigns value from a protobuf message

    Setter first checks if message contains field named as value of `pb_field_name` and
    assigns it if it does, otherwise skips assignment without error.

    If value other than protocol buffer message is passed to setter, TypeError is
    raised.

    Usage::

        class Device(UpdatableProps):
            battery_level = ProtobufField[int]("soc")

            def parse(self):
                ...
                message = protobuf_cls()
                message.ParseFromString(payload)

                self.update_fields(message)

                for field in self.updated_fields:
                    self.callback(field)

    The code above defines field ``battery_level`` that retreives field ``soc`` from
    provided parsed protobuf message. If the value in protobuf is different from the
    current value, `updated_fields` will contain name of the updated field which can
    be used to run callbacks only on updated values.

    Attributes
    ----------
    pb_field_name
        Name of field in protobuf message
    transform_value
        Callable that accepts raw value from protobuf message and returns transformed
        value, by default returns raw value
    """

    pb_field_name: str
    transform_value: Callable[[T], T] = lambda x: x

    def __set_name__(self, owner: type[UpdatableProps], name: str):
        super().__set_name__(owner, name)

        owner._pb_field_names = owner._pb_field_names + [self.public_name]

    def __set__(self, instance: UpdatableProps, value: Any):
        if not isinstance(value, Message):
            raise TypeError(
                f"Can only set value from protobuf message but received: {value}"
            )

        if not value.HasField(self.pb_field_name):
            return

        value = self.transform_value(getattr(value, self.pb_field_name))
        super().__set__(instance, value)


@dataclass
class ProtobufListField[T](Field[T], abc.ABC):
    """
    Abstract descriptor for repeated fields from protobuf message

    This descriptor can be explained with the following snippet:

        if not message.HasField(field.list_name):
            continue

        for item in field.get_list(getattr(message, field.list_name)):
            if not field.should_update(message):
                continue

            value = field.get_item_value(message)
            if value is None:
                continue

            setattr(self, field.public_name, item)

    Attributes
    ----------
    pb_field_name
        Name of compound field to get from parsed list
    transform_value
        Callable that accepts raw value for each item in repeated protobuf type and
        returns transformed value, by default returns value without change
    """

    pb_field_name: str
    transform_value: Callable[[T], T] = lambda x: x

    @property
    @abc.abstractmethod
    def list_name(self) -> str:
        """Top level protobuf message attribute name"""

    def get_list(self, message: Any) -> Sequence[Message]:
        """Get list from repeated message"""
        return message

    @abc.abstractmethod
    def get_item_value(self, message: Message) -> T | None:
        """Get final value from parsed list item"""

    def should_update(self, message: Any) -> bool:
        """Return True if field should be updated from passed in message"""
        return False

    def __set_name__(self, owner: type[UpdatableProps], name: str):
        super().__set_name__(owner, name)
        owner._list_field_name_to_field = owner._list_field_name_to_field | {
            self.list_name: self
        }
        owner._pb_list_field_names = owner._pb_list_field_names + [name]

    def __set__(self, instance: UpdatableProps, value: Any):
        if not self.should_update(value):
            return

        value = self.get_item_value(value)
        if value is None:
            return

        super().__set__(instance, self.transform_value(value))
