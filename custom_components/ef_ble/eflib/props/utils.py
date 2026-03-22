import functools
from collections.abc import Callable
from typing import Protocol


class _SupportsRound2[T_co](Protocol):
    def __round__(self, ndigits: int, /) -> T_co: ...


def pround[T](precision: int = 2) -> Callable[[_SupportsRound2[T]], T]:
    def _round(val: _SupportsRound2[T]):
        return round(val, precision)

    return _round


class classproperty[T]:
    def __init__(self, method: Callable[..., T]):
        self.method = method
        functools.update_wrapper(self, method)

    def __get__(self, obj, cls=None) -> T:
        if cls is None:
            cls = type(obj)
        return self.method(cls)
