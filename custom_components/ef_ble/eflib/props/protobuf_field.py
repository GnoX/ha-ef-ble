from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, cast, overload

from google.protobuf.message import Message

from .updatable_props import Field

if TYPE_CHECKING:
    from .protobuf_props import ProtobufProps


class _ProtoAttr:
    def __init__(self, name: str):
        self.attrs = [name]

    def __getattr__(self, name):
        self.attrs.append(name)
        return self

    def __repr__(self):
        return f"proto_attr({self.attrs})"

    @property
    def name(self):
        return ".".join(self.attrs)


@dataclass
class _ProtoAttrAccessor[T1: Message]:
    message_type: type[T1]

    def __getattr__(self, name: str):
        if name not in self.message_type.DESCRIPTOR.fields_by_name:
            raise AttributeError(
                f"{self.message_type} does not contain field named '{name}'"
            )
        return _ProtoAttr(name)


def proto_attr_mapper[T: Message](pb: type[T]) -> type[T]:
    """
    Create proxy object for protobuf class that returns accessed attributes

    This function is a convenience function for creating typed fields from protobuf
    message classes.

    Returns
    -------
        Proxy object that tracks all accessed attributes
    """
    return _ProtoAttrAccessor(pb)  # type: ignore reportReturnType


class ProtobufField[T](Field[T]):
    """
    Field that allows value assignment from protocol buffer message

    It is recommented to not use this class directly - use `pb_field` instead for
    better typing.
    """

    def __init__(
        self, pb_field: _ProtoAttr, transform_value: Callable[[Any], T] = lambda x: x
    ):
        """
        Create protobuf field that allows value assignment from protobuf message

        Parameters
        ----------
        pb_field
            Instance of protobuf accessor created with `proto_attr_mapper`
        transform_value, optional
            Function that takes protobuf attribute
        """
        self.pb_field = pb_field
        self.transform_value = transform_value

    def __set_name__(self, owner: type["ProtobufProps"], name: str):
        super().__set_name__(owner, name)
        owner._protobuf_fieldnames = [*owner._protobuf_fieldnames, self.public_name]

    def _get_value(self, value: Message):
        for attr in self.pb_field.attrs:
            if not value.HasField(attr):
                return None
            value = getattr(value, attr)
        return value

    def __set__(self, instance: "ProtobufProps", value: Any):
        if not isinstance(value, Message):
            raise TypeError(
                f"Can only set value from protobuf message but received: '{value}', "
                f"field {self.pb_field}"
            )

        if (value := self._get_value(value)) is None:
            return

        super().__set__(instance, self.transform_value(value))


@overload
def pb_field[T_ATTR](
    attr: T_ATTR, transform: None = None
) -> "ProtobufField[T_ATTR]": ...


@overload
def pb_field[T_ATTR, T_OUT](
    attr: T_ATTR, transform: Callable[[T_ATTR], T_OUT]
) -> "ProtobufField[T_OUT]": ...


def pb_field(
    attr: Any, transform: Callable[[Any], Any] | None = None
) -> "ProtobufField[Any]":
    """
    Create field that allows value assignment from protocol buffer messages

    Parameters
    ----------
    attr
        Protobuf field attribute of instance returned from `proto_attr_mapper`
    transform, optional
        Function that is applied to raw protobuf value
    """
    if not isinstance(attr, _ProtoAttr):
        raise TypeError(
            "Attribute has to be an instance returned from `proto_attr_mapper` after "
            f"attribute access, but received value of '{attr}'"
        )
    return ProtobufField(
        pb_field=attr,
        transform_value=transform if transform is not None else lambda x: x,
    )


def proto_attr_name(proto_attr: _ProtoAttr | Any) -> str:
    """Get name of attribute from proto attr returned from `proto_attr_mapper`"""
    return proto_attr.name


def proto_has_attr(msg: Message, proto_attr: _ProtoAttr | Any) -> bool:
    """Return True if protobuf message has specified attribute"""
    for attr in proto_attr.attrs:
        if not msg.HasField(attr):
            return False
        msg = getattr(msg, attr)
    return True
