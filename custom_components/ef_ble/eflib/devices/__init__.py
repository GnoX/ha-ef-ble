import importlib
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ..devicebase import DeviceBase

    class ModuleWithDevice(Protocol):
        Device: type[DeviceBase]


__all__ = [
    f.stem
    for f in Path(__file__).parent.glob("*.py")
    if f.is_file() and f.stem != "__init__"
]

devices: list["ModuleWithDevice | ModuleType"]


def __getattr__(name: str):
    if name == "devices":
        return [importlib.import_module(f".{device}", __name__) for device in __all__]

    return None
