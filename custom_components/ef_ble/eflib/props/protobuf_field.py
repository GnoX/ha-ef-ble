import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, overload

from google.protobuf.message import Message

from .updatable_props import Field, FieldGroup, Skip

if TYPE_CHECKING:
    from .protobuf_props import ProtobufProps


class _ProtoAttr:
    def __init__(self, message_type: type[Message], names: str | list[str]):
        if isinstance(names, list):
            self.attrs = names.copy()
        else:
            self.attrs = [names]
        self.message_type = message_type

    def __getattr__(self, name: str):
        return _ProtoAttr(self.message_type, [*self.attrs, name])

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
        return _ProtoAttr(self.message_type, name)


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


def proto_attr_name(proto_attr: _ProtoAttr | Any) -> str:
    """Get name of attribute from proto attr returned from `proto_attr_mapper`"""
    return proto_attr.name


def proto_has_attr(msg: Message, proto_attr: _ProtoAttr | Any) -> bool:
    """Return True if protobuf message has specified attribute"""
    if proto_attr is None:
        return False
    for attr in proto_attr.attrs:
        try:
            if not msg.HasField(attr):
                return False
        except ValueError as e:
            if "not have pressence" not in str(e):
                return len(getattr(msg, attr)) > 0
        msg = getattr(msg, attr)
    return True


class TransformIfMissing[T_ATTR, T_OUT]:
    def __init__(self, transform_func: Callable[[T_ATTR], T_OUT | type[Skip]]):
        self._func = transform_func

    def __call__(self, value: T_ATTR) -> T_OUT | type[Skip]:
        return self._func(value)


class ProtobufField[T](Field[T]):
    """
    Field that allows value assignment from protocol buffer message

    It is recommended to not use this class directly - use `pb_field` instead for
    better typing.
    """

    def __init__(
        self,
        pb_field: _ProtoAttr,
        transform_value: Callable[[Any], T] = lambda x: x,
        process_if_missing: bool = False,
    ):
        """
        Create protobuf field that allows value assignment from protobuf message

        Parameters
        ----------
        pb_field
            Instance of protobuf accessor created with `proto_attr_mapper`
        transform_value, optional
            Function that takes protobuf attribute value
        process_if_missing, optional
            If True, transform function receives None
        """
        self.pb_field = pb_field
        self._transform_value = transform_value
        self.process_if_missing = process_if_missing

    def _get_value(self, value: Message | Any):
        if not isinstance(value, Message):
            return value

        n_attrs = len(self.pb_field.attrs)
        for i, attr in enumerate(self.pb_field.attrs):
            if not value.HasField(attr):
                if i == n_attrs - 1 and self.process_if_missing:
                    return None
                return Skip
            value = getattr(value, attr)
        return value

    def __set__(self, instance: "ProtobufProps", value: Any):
        if (value := self._get_value(value)) is Skip:
            return
        super().__set__(instance, value)


@overload
def pb_field[T_ATTR](
    attr: T_ATTR,
    transform: None = None,
) -> "ProtobufField[T_ATTR]": ...


@overload
def pb_field[T_ATTR, T_OUT](
    attr: T_ATTR,
    transform: Callable[[T_ATTR], T_OUT | type[Skip]],
) -> "ProtobufField[T_OUT]": ...


def pb_field(
    attr: Any,
    transform: Callable[[Any], Any] | None = None,
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
            "Attribute has to be an instance returned from "
            f"`proto_attr_mapper`, but received value of '{attr}'"
        )
    return ProtobufField(
        pb_field=attr,
        transform_value=transform if transform is not None else lambda x: x,
        process_if_missing=isinstance(transform, TransformIfMissing),
    )


def _match_to_regex(match: str) -> re.Pattern[str]:
    return re.compile("^" + re.escape(match).replace(r"\{n\}", r"(\d+)") + "$")


def _find_match_segment(
    attr: _ProtoAttr,
    regex: re.Pattern[str],
) -> int:
    for i, a in enumerate(attr.attrs):
        if regex.match(a):
            return i
    raise ValueError(f"No segment matching '{regex.pattern}' in path {attr.attrs}")


def _discover_pb_indices(
    attr: _ProtoAttr,
    pattern: re.Pattern[str],
    match_idx: int,
) -> tuple[int, int]:
    descriptor = attr.message_type.DESCRIPTOR
    for attr_name in attr.attrs[:match_idx]:
        field_desc = descriptor.fields_by_name.get(attr_name)
        if field_desc is None or field_desc.message_type is None:
            raise ValueError(
                f"Cannot traverse protobuf path at '{attr_name}': "
                "field not found or not a message type"
            )
        descriptor = field_desc.message_type

    indices = sorted(
        int(m.group(1))
        for name in descriptor.fields_by_name
        if (m := pattern.match(name))
    )
    if not indices:
        raise ValueError(f"No fields matching '{pattern.pattern}' in {descriptor.name}")
    expected = list(range(indices[0], indices[0] + len(indices)))
    if indices != expected:
        raise ValueError(
            f"Non-contiguous indices {indices} for "
            f"'{pattern.pattern}' in {descriptor.name}"
        )
    return indices[0], len(indices)


def pb_field_group[T](
    attr: T,
    match: str,
    count: int | None = None,
    *,
    transform: Callable[[Any], Any] | None = None,
    start: int | None = None,
    name_template: str | None = None,
    name_prefix: str | None = None,
) -> "FieldGroup[T]":
    """
    Create a FieldGroup of protobuf fields by indexing one path segment

    Parameters
    ----------
    attr
        A fully-typed protobuf path created via `proto_attr_mapper`, e.g.
        `_hall1.ch1_sta.load_sta`
    match
        Pattern with {n} placeholder identifying the indexed segment, e.g. "ch{n}_sta"
    count
        Number of fields to create; when omitted, the count (and start) are discovered
        automatically from the protobuf descriptor
    transform
        Optional transform passed to `pb_field` for every genertaed field
    start
        First index value. Defaults to 1 when *count* is given explicitly, or to the
        lowest discovered index when count is omitted
    name_template
        Explicit naming pattern with {n} placeholder, e.g.  "ch{n}_status"
    name_prefix
        Prefix with {n} placeholder - the template is derived automaticaly from the
        class attribute name (used by `pb_group`)
    """
    if not isinstance(attr, _ProtoAttr):
        raise TypeError(
            "First argument must be a protobuf path from "
            f"`proto_attr_mapper`, got {type(attr)}"
        )

    regex = _match_to_regex(match)
    seg_idx = _find_match_segment(attr, regex)

    if count is None:
        discovered_start, count = _discover_pb_indices(
            attr,
            regex,
            seg_idx,
        )
        if start is None:
            start = discovered_start
    elif start is None:
        start = 1

    def factory(n: int) -> ProtobufField:
        new_attrs = list(attr.attrs)
        new_attrs[seg_idx] = match.format(n=n)
        return pb_field(
            _ProtoAttr(attr.message_type, new_attrs),
            transform,
        )

    return FieldGroup(
        factory,
        count,
        start=start,
        name_template=name_template,
        name_prefix=name_prefix,
    )


class _PbGroupFactory:
    __slots__ = ("_match", "_name_prefix")

    def __init__(
        self,
        match: str,
        name_prefix: str | None = None,
    ) -> None:
        self._match = match
        self._name_prefix = name_prefix

    def __call__[T](
        self,
        attr: T,
        *,
        transform: Callable[[Any], Any] | None = None,
        name_template: str | None = None,
    ) -> "FieldGroup[T]":
        return pb_field_group(
            attr,
            match=self._match,
            transform=transform,
            name_template=name_template,
            name_prefix=self._name_prefix,
        )


def pb_group(
    match: str,
    name_prefix: str | None = None,
) -> _PbGroupFactory:
    """
    Create a factory for building FieldGroups with a fixed match pattern

    Parameters
    ----------
    match
        Pattern with {n} placeholder, e.g. "Energy{n}_info"
    name_prefix
        Optional prefix with {n} for automatic field naming, e.g. "channel{n}" - the
        template is derived from the class attribute name at class creation time
    """
    return _PbGroupFactory(match, name_prefix=name_prefix)


def _find_indexed_segment(attr: _ProtoAttr) -> tuple[int, str]:
    descriptor = attr.message_type.DESCRIPTOR

    for seg_idx, seg_name in enumerate(attr.attrs):
        for m in re.finditer(r"\d+", seg_name):
            candidate = seg_name[: m.start()] + "{n}" + seg_name[m.end() :]
            regex = _match_to_regex(candidate)
            siblings = [n for n in descriptor.fields_by_name if regex.match(n)]
            if len(siblings) > 1:
                return seg_idx, candidate

        field_desc = descriptor.fields_by_name.get(seg_name)
        if field_desc is not None and field_desc.message_type is not None:
            descriptor = field_desc.message_type

    raise ValueError(f"No indexed segment found in protobuf path {attr.attrs}")


@dataclass(slots=True)
class _PbIndexedView[T]:
    msg: Any
    attrs: list[str]
    match_idx: int
    match: str

    def __getitem__(self, index: int) -> T:
        attrs = list(self.attrs)
        attrs[self.match_idx] = self.match.format(n=index)
        msg = self.msg
        for attr_name in attrs:
            msg = getattr(msg, attr_name)
        return msg


def pb_indexed_attr[T](msg: Any, attr: T) -> _PbIndexedView[T]:
    """
    Create an indexed view over a protobuf message using a typed path

    The indexed segment is auto-discovered by scanning for path segments that have
    numbered siblings in the protobuf descriptor. Use [index] on the result to traverse
    the message with that index substituted.

    Parameters
    ----------
    msg
        A real protobuf message instance to traverse
    attr
        A typed protobuf path from `proto_attr_mapper`, e.g.
        `pb_push_set.load_incre_info.hall1_incre_info.ch1_sta`
    """
    if not isinstance(attr, _ProtoAttr):
        raise TypeError(
            "Second argument must be a protobuf path from "
            f"`proto_attr_mapper`, got {type(attr)}"
        )
    match_idx, match = _find_indexed_segment(attr)
    return _PbIndexedView(msg, list(attr.attrs), match_idx, match)
