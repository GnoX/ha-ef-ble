import abc
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, cast, dataclass_transform

from google.protobuf.message import Message

from .protobuf_field import ProtobufField

if TYPE_CHECKING:
    from .protobuf_props import ProtobufProps


@dataclass_transform()
class ProtobufRepeatedField[T_ITEM, T_OUT](ProtobufField[T_OUT]):
    """
    Represents field for repeated protobuf fields

    Do not use this class directly - use `repeated_pb_field_type` for better typing
    """

    def __init_subclass__(cls) -> None:
        dataclass(cls)

    def get_list(self, value: Message) -> Sequence[Message]:
        """
        Get sequence from protobuf message

        Parameters
        ----------
        value
            Parsed protobuf message

        Returns
        -------
            Sequence of values accessed from protobuf message
        """
        list_attrs = self.pb_field.attrs
        if not list_attrs:
            raise ValueError(f"Received accessor with no attributes: '{self.pb_field}'")

        if not value.HasField(list_attrs[0]):
            return []

        for attr in list_attrs:
            value = getattr(value, attr)

        return cast(Sequence[Message], value)

    @abc.abstractmethod
    def process_item(self, value: T_ITEM) -> T_OUT | None:
        """Process item from sequence returned from `get_list`"""

    def __set_name__(self, owner: type["ProtobufProps"], name: str):
        super().__set_name__(owner, name)
        owner.add_repeated_field(self)

    def __set__(self, instance: "ProtobufProps", value: Any):
        if (value := self.process_item(value)) is None:
            return

        self._set_value(instance, value)


def _raise[T_IN](v: T_IN, exc: type[Exception]) -> T_IN:
    raise exc


def repeated_pb_field_type[T_ITEM, T_OUT](
    list_field: Sequence[T_ITEM],
    value_field: Callable[[T_ITEM], T_OUT] = lambda x: _raise(x, NotImplementedError),
) -> type[ProtobufRepeatedField[T_ITEM, T_OUT]]:
    """
    Create repeated field type from protobuf accessor repesenting sequence type

    Usage
    -----
    Assuming protobuf message looks like this
    ```
    message RecordType { int value = 1; }
    messsage SomeMessageType { repeated RecordType some_list = 1; }
    ```

    We can create a field that processes items like so
    ```
    pb = proto_attr_mapper(some_pb2.SomeMessageType)

    class SomeRepeatedField(
        repeated_field_type(
            list_field=pb.some_list,
            value_field=lambda x: x.value,
        )
    ):
        def process_item(self, value: some_pb2.RecordType):
            return x.value
    ```

    Returns
    -------
        Type of repeated protobuf message
    """

    class CustomRepeatedField(ProtobufRepeatedField[T_ITEM, T_OUT]):
        pb_field = list_field

        def process_item(self, value: T_ITEM) -> T_OUT | None:
            return value_field(value)

    return CustomRepeatedField
