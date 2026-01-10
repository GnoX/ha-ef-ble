import struct
from dataclasses import dataclass, fields
from functools import cache
from inspect import get_annotations
from typing import Annotated, ClassVar, Self, dataclass_transform, get_args, get_origin


@dataclass_transform()
class RawData:
    _STRUCT_FMT: ClassVar[str]
    SIZE: int

    def __init_subclass__(cls) -> None:
        format_str = getattr(cls, "_STRUCT_FMT", ["<"])

        for name, annotation in get_annotations(cls).items():
            if get_origin(annotation) is Annotated:
                _, *metadata = get_args(annotation)
                if not metadata:
                    continue
                format_str += metadata[0]
                # some data types may have optional extensions so we make all fields
                # optional and only select fields based on the length of the data
                setattr(cls, name, None)

        dataclass(cls)

        cls._FULL_STRUCT_FMT = format_str
        cls._STRUCT_FMT = "".join(format_str)
        cls.SIZE = struct.calcsize(cls._STRUCT_FMT)

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        return cls(*cls.unpack(data))

    @classmethod
    def unpack(cls, data: bytes):
        struct_fmt = cls._STRUCT_FMT
        size = cls.SIZE

        if (data_len := len(data)) < cls.SIZE:
            struct_fmt, size = cls._fit_struct_to_data(data_len)

        return struct.unpack(struct_fmt, data[:size])

    def pack(self):
        return struct.pack(
            self._STRUCT_FMT,
            *[getattr(self, field.name) for field in fields(self)],
        )

    @classmethod
    def list_from_bytes[T](cls: T, data: bytes) -> list[T]:
        raise ValueError("This class does not support decoding into lists")

    @classmethod
    @cache
    def _fit_struct_to_data(cls, data_len: int):
        size = cls.SIZE
        i = 0
        reduced_fmt = "".join(cls._FULL_STRUCT_FMT)
        iter_str = []
        while size > data_len:
            i += 1
            reduced_fmt = "".join(cls._FULL_STRUCT_FMT[:-i])
            size = struct.calcsize(reduced_fmt)
            iter_str.append((reduced_fmt, size))

        return "".join(cls._FULL_STRUCT_FMT[:-i]), size
