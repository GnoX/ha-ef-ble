import asyncio
import logging
from collections.abc import Callable

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from .connection import Connection
from .packet import Packet

_LOGGER = logging.getLogger(__name__)


class DeviceBase:
    """Device Base"""

    MANUFACTURER_KEY = 0xB5B5

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        _LOGGER.debug(
            "%s: Creating new device: %s (%s)",
            ble_dev.address,
            self.device,
            sn,
        )
        self._ble_dev = ble_dev
        self._address = ble_dev.address
        self._sn = sn
        # We can't use advertisement name here - it's prone to change to "Ecoflow-dev"
        self._name = self.NAME_PREFIX + self._sn[-4:]
        self._name_by_user = self._name

        self._conn = None
        self._callbacks = set()
        self._callbacks_map = dict()

    @property
    def device(self):
        return self.__doc__

    @property
    def address(self):
        return self._address

    @property
    def name(self):
        return self._name

    @property
    def name_by_user(self):
        return self._name_by_user

    def isValid(self):
        return self._sn != None

    @property
    def is_connected(self) -> bool:
        return self._conn != None and self._conn.is_connected

    async def data_parse(self, packet: Packet):
        """Function to parse incoming data and trigger sensors update"""
        return False

    async def packet_parse(self, data: bytes):
        """Function to parse packet"""
        return Packet.fromBytes(data)

    async def connect(self, user_id: str | None = None):
        if self._conn == None:
            if user_id != None:
                self._user_id = user_id
            self._conn = Connection(
                self._ble_dev,
                self._sn,
                self._user_id,
                self.data_parse,
                self.packet_parse,
            )
            _LOGGER.info("%s: Connecting to %s", self._address, self.__doc__)
        await self._conn.connect()

    async def disconnect(self):
        if self._conn == None:
            _LOGGER.error("%s: Device has no connection", self._address)
            return

        await self._conn.disconnect()

    async def waitConnected(self):
        if self._conn == None:
            _LOGGER.error("%s: Device has no connection", self._address)
            return

        await self._conn.waitConnected()

    async def waitDisconnected(self):
        if self._conn == None:
            _LOGGER.error("%s: Device has no connection", self._address)
            return

        await self._conn.waitDisconnected()

    def register_callback(
        self, callback: Callable[[], None], propname: str | None
    ) -> None:
        """Register callback, called when Device changes state."""
        if propname is None:
            self._callbacks.add(callback)
        else:
            self._callbacks_map[propname] = self._callbacks_map.get(
                propname, set()
            ).union([callback])

    def remove_callback(
        self, callback: Callable[[], None], propname: str | None
    ) -> None:
        """Remove previously registered callback."""
        if propname is None:
            self._callbacks.discard(callback)
        else:
            self._callbacks_map.get(propname, set()).discard(callback)

    def update_callback(self, propname: str) -> None:
        """Finding the registered callbacks in the map and then calling the callbacks"""
        for callback in self._callbacks_map.get(propname, set()):
            callback()
