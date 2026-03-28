import functools
from collections.abc import Callable


def pround(precision: int = 2):
    def _round(val: float | None) -> float | None:
        return None if val is None else round(val, precision)

    return _round


def pmultiply(x: int) -> Callable[[float | None], float | None]:
    def _multiply(value: float | None) -> float | None:
        return None if value is None else value * x

    return _multiply


def prop_has_bit_on(bit_position: int) -> Callable[[int | None], bool]:
    def transform(value: int | None) -> bool:
        if value is None:
            return False
        return bool((value >> bit_position) & 1)

    return transform


def prop_has_bit_off(bit_position: int) -> Callable[[int | None], bool]:
    def transform(value: int | None) -> bool:
        if value is None:
            return False
        return not bool((value >> bit_position) & 1)

    return transform


class classproperty[T]:
    def __init__(self, method: Callable[..., T]):
        self.method = method
        functools.update_wrapper(self, method)

    def __get__(self, obj, cls=None) -> T:
        if cls is None:
            cls = type(obj)
        return self.method(cls)
