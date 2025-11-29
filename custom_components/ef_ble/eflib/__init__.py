"""Library for EcoFlow BLE protocol"""

import logging

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from . import devices
from .devicebase import DeviceBase
from .entity import controls as controls
from .entity import sensors as sensors
from .props.updatable_props import UpdatableProps

_LOGGER = logging.getLogger(__name__)


def NewDevice(ble_dev: BLEDevice, adv_data: AdvertisementData) -> DeviceBase | None:
    """Return Device if ble dev fits the requirements otherwise None"""

    if not (
        hasattr(adv_data, "manufacturer_data")
        and DeviceBase.MANUFACTURER_KEY in adv_data.manufacturer_data
    ):
        return None

    # Looking for device SN
    man_data = adv_data.manufacturer_data[DeviceBase.MANUFACTURER_KEY]
    sn = man_data[1:17]

    # Check if known devices fits the found serial number
    for device in devices.devices:
        if device.Device.check(sn):
            return device.Device(ble_dev, adv_data, sn.decode(encoding="ASCII"))

    _LOGGER.warning("%s: Unknown SN prefix: %s", ble_dev.address, sn[:4])
    return None


def _check_device(device: "DeviceBase"):
    if not isinstance(device, UpdatableProps):
        raise TypeError("Device has to be subclass of UpdatableProps")
    return device


def get_sensors(device: "DeviceBase"):
    return _check_device(device).get_sensors(sensors.SensorType)


def get_binary_sensors(device: "DeviceBase"):
    return _check_device(device).get_sensors(sensors.BinarySensorType)


def get_toggles(device: "DeviceBase") -> list[controls.Toggle]:
    return _check_device(device).get_controls(controls.Toggle)


__all__ = [
    "DeviceBase",
    "NewDevice",
    "controls",
    "get_binary_sensors",
    "get_sensors",
    "get_toggles",
    "sensors",
]
