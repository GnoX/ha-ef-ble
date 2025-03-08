from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, MANUFACTURER
from .eflib import DeviceBase


class EcoflowEntity(Entity):
    _attr_has_entity_name = True

    def __init__(self, device: DeviceBase):
        self._device = device

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self._device.address),
            },
            connections={
                (CONNECTION_NETWORK_MAC, self._device.address),
            },
            name=self._device.name,
            manufacturer=MANUFACTURER,
            model=self._device.device,
            serial_number=self._device._sn,
        )

    @property
    def available(self) -> bool:
        """Return True if device is connected."""
        return self._device.is_connected
