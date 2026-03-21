import string
from collections.abc import Callable, Iterable, Iterator
from typing import Any, ClassVar, overload


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
    _updated_fields: set[str] | None = None
    _fields: ClassVar[list["Field[Any]"]] = []

    @property
    def updated_fields(self):
        """List of field names that were updated after calling `reset_updated`"""
        if self._updated_fields is None:
            self._updated_fields = set()
        return self._updated_fields

    @updated_fields.setter
    def updated_fields(self, value: list[str]):
        self._updated_fields = set(value)

    def reset_updated(self):
        """Clear the updated flag and the set of changed field names"""
        self.updated = False
        self.updated_fields.clear()

    def get_value[T](self, field: "Field[T] | str") -> T:
        """Read the current value of a field by descriptor or name"""
        return getattr(
            self,
            field.public_name if isinstance(field, Field) else field,
        )

    def set_value(self, field: "Field[Any] | str", value: Any):
        """Write a value to a field by descriptor or name"""
        setattr(
            self,
            field.public_name if isinstance(field, Field) else field,
            value,
        )

    def __str__(self) -> str:
        cls = f"{self.__class__.__module__}.{self.__class__.__name__}"
        lines = [
            f"  {f.public_name}: {getattr(self, f.public_name)!r}" for f in self._fields
        ]
        return f"{cls}:\n" + "\n".join(lines)


class Skip:
    """Sentinel value for skipping assignment in field's transform function"""


class Field[T]:
    """Descriptor for updating values only if they changed"""

    transform_value: Callable[[Any], T] | None = None

    def __set_name__[P: UpdatableProps](
        self,
        owner: type[P],
        name: str,
    ):
        self.public_name = name
        self.private_name = (
            f"_{name}" if not hasattr(owner, f"_{name}") else f"__{name}"
        )
        owner._fields = [*owner._fields, self]

    def __set__(self, instance, value: Any):
        self._set_value(instance, value)

    def _set_value(self, instance: UpdatableProps, value: Any):
        if value == getattr(instance, self.public_name):
            return
        if (value := self._transform_value(value)) is Skip:
            return
        setattr(instance, self.private_name, value)
        instance.updated = True
        instance.updated_fields.add(self.public_name)

    @property
    def _transform_value(self):
        return getattr(self, "_transform", lambda x: x)

    @_transform_value.setter
    def _transform_value(
        self,
        value: Callable[[Any], Any] | None = None,
    ):
        if value is not None:
            setattr(self, "_transform", value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.public_name})"

    @overload
    def __get__(
        self,
        instance: None,
        owner: type[UpdatableProps],
    ) -> "Field[T]": ...

    @overload
    def __get__(
        self,
        instance: UpdatableProps,
        owner: type[UpdatableProps],
    ) -> T | None: ...

    def __get__(
        self,
        instance: UpdatableProps | None,
        owner: type[UpdatableProps],
    ) -> "T | Field | None":
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)


class FieldGroupView[T, K: (int, str) = int]:
    """Provides indexed access to field values on a device instance"""

    __slots__ = ("_fields", "_index_map", "_instance")

    def __init__(
        self,
        instance: UpdatableProps,
        fields: "list[Field[T]]",
        index_map: dict[K, int],
    ) -> None:
        self._instance = instance
        self._fields = fields
        self._index_map = index_map

    def __getitem__(self, index: K) -> "T | None":
        field = self._fields[self._index_map[index]]
        return field.__get__(self._instance, type(self._instance))

    def __iter__(self) -> Iterator[K]:
        return iter(self._index_map)

    def __len__(self) -> int:
        return len(self._fields)

    def values(self) -> "Iterator[T | None]":
        """Iterate over field values"""
        for key in self._index_map:
            yield self[key]

    def items(self) -> "Iterator[tuple[K, T | None]]":
        """Iterate over (index, value) pairs"""
        for key in self._index_map:
            yield key, self[key]


class Indices:
    """Pre-defined index sequences for FieldGroup and pb_indexed_attr"""

    @staticmethod
    def numeric(count: int, start: int = 1) -> list[int]:
        """Sequential integers: [1, 2, 3, ...] (or from start)"""
        return list(range(start, start + count))

    @staticmethod
    def alpha(count: int) -> list[str]:
        """Lowercase letters: ["a", "b", "c", ...]"""
        return list(string.ascii_lowercase[:count])

    @staticmethod
    def alpha_upper(count: int) -> list[str]:
        """Uppercase letters: ["A", "B", "C", ...]"""
        return list(string.ascii_uppercase[:count])


class FieldGroup[T, K: (int, str) = int]:
    """
    Descriptor that creates N individually-named fields and provides indexed access

    When assigned as a class attribute with name `name`, it registers N sub-fields as
    `{name}_{key}` for each index key (or a custom `name_template` / `name_prefix`).

    Class access returns the FieldGroup itself (iterable over Field descriptors).
    Instance access returns a FieldGroupView with indexed __getitem__.

    Parameters
    ----------
    factory
        Callable receiving the index key and returning a Field instance
    indices
        An integer (number of 1-based fields) or an iterable of explicit index keys
        (e.g. `Indices.numeric(6)`, `Indices.alpha(3)`, `range(1, 7)`, or
        `["a", "b", "c"]`)
    name_template
        Explicit naming pattern with {n} placeholder, e.g. "ch{n}_status"
    name_prefix
        Prefix with {n} placeholder - the template is derived automatically from the
        class attribute name (used by `pb_group`)
    """

    def __init__(
        self,
        factory: "Callable[[K], Field[T]]",
        indices: "int | Iterable[K]",
        *,
        name_template: str | None = None,
        name_prefix: str | None = None,
    ) -> None:
        self._indices: tuple = (
            tuple(range(1, 1 + indices)) if isinstance(indices, int) else tuple(indices)
        )

        self._index_map: dict[K, int] = {
            key: pos for pos, key in enumerate(self._indices)
        }
        self._name_template = name_template
        self._name_prefix = name_prefix
        self._fields: list[Field[T]] = [factory(i) for i in self._indices]
        self._name: str = ""

    @property
    def indices(self) -> tuple[K, ...]:
        """The index keys for this group"""
        return self._indices

    def _resolve_template(self, name: str) -> str | None:
        if self._name_template is not None:
            return self._name_template
        if self._name_prefix is not None:
            base = self._name_prefix.replace("{n}", "")
            return self._name_prefix + name[len(base) :]
        return None

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name
        template = self._resolve_template(name)
        for key, field in zip(self._indices, self._fields, strict=True):
            field_name = template.format(n=key) if template else f"{name}_{key}"
            field.__set_name__(owner, field_name)
            setattr(owner, field_name, field)

    @overload
    def __get__(
        self,
        instance: None,
        owner: type,
    ) -> "FieldGroup[T, K]": ...

    @overload
    def __get__(
        self,
        instance: UpdatableProps,
        owner: type,
    ) -> "FieldGroupView[T, K]": ...

    def __get__(
        self,
        instance: UpdatableProps | None,
        owner: type,
    ) -> "FieldGroup[T, K] | FieldGroupView[T, K]":
        if instance is None:
            return self
        return FieldGroupView(instance, self._fields, self._index_map)

    def __iter__(self) -> "Iterator[Field[T]]":
        return iter(self._fields)

    def __len__(self) -> int:
        return len(self._fields)

    def __getitem__(self, index: K) -> "Field[T]":
        return self._fields[self._index_map[index]]


@overload
def field_group[T](
    factory: "Callable[[int], Field[T]]",
    indices: int,
    *,
    name_template: str | None = None,
) -> "FieldGroup[T, int]": ...


@overload
def field_group[T, K: (int, str)](
    factory: "Callable[[K], Field[T]]",
    indices: "Iterable[K]",
    *,
    name_template: str | None = None,
) -> "FieldGroup[T, K]": ...


def field_group(
    factory: "Callable[[Any], Field[Any]]",
    indices: "int | Iterable[Any]",
    *,
    name_template: str | None = None,
) -> "FieldGroup[Any, Any]":
    """
    Create a group of related fields

    When assigned to a class attribute with name `name`, the individual fields are
    registered as `{name}_{key}` for each index key.

    Parameters
    ----------
    factory
        Callable receiving the index key and returning a Field instance
    indices
        An integer (number of 1-based fields) or an iterable of explicit index keys
        (e.g. `Indices.numeric(6)`, `Indices.alpha(3)`, `range(1, 7)`, or
        `["a", "b", "c"]`)
    name_template
        Explicit naming pattern with {n} placeholder, e.g. "ch{n}_status"
    """
    return FieldGroup(
        factory,
        indices,
        name_template=name_template,
    )
