import logging
from collections import defaultdict
from collections.abc import Callable
from typing import Any

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak_retry_connector import MAX_CONNECT_ATTEMPTS

from .connection import Connection, PacketIterator
from .packet import Packet

_LOGGER = logging.getLogger(__name__)


class DeviceBase:
    """Device Base"""

    MANUFACTURER_KEY = 0xB5B5

    def __init__(
        self,
        ble_dev: BLEDevice,
        adv_data: AdvertisementData,
        sn: str,
    ) -> None:
        self._sn = sn
        _LOGGER.debug(
            "%s: Creating new device: %s (%s)",
            ble_dev.address,
            self.device,
            sn,
        )
        self._ble_dev = ble_dev
        self._address = ble_dev.address
        # We can't use advertisement name here - it's prone to change to "Ecoflow-dev"
        self._name = self.NAME_PREFIX + self._sn[-4:]
        self._name_by_user = self._name

        self._conn = None
        self._callbacks = set()
        self._callbacks_map = {}
        self._state_update_callbacks: dict[str, set[Callable[[Any], None]]] = (
            defaultdict(set)
        )
        self._update_period = None

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

    @property
    def connection_state(self):
        return None if self._conn is None else self._conn._state

    async def data_parse(self, packet: Packet) -> bool:
        """Function to parse incoming data and trigger sensors update"""
        return False

    async def data_parse_batch(self, packet_iterator: PacketIterator):
        """Parse incoming data packet batch"""
        async for packet in packet_iterator:
            if not await self.data_parse(packet):
                packet.parsed = False

    async def packet_parse(self, data: bytes):
        """Function to parse packet"""
        return Packet.fromBytes(data)

    async def connect(
        self, user_id: str | None = None, max_attempts: int = MAX_CONNECT_ATTEMPTS
    ):
        if self._conn is None:
            self._conn = Connection(
                ble_dev=self._ble_dev,
                dev_sn=self._sn,
                user_id=user_id,
                data_parse=self.data_parse_batch,
                packet_parse=self.packet_parse,
                update_period=self._update_period,
            )
            _LOGGER.info("%s: Connecting to %s", self._address, self.__doc__)
        elif self._conn._user_id != user_id:
            self._conn._user_id = user_id

        await self._conn.connect(max_attempts=max_attempts)

    async def disconnect(self):
        if self._conn == None:
            _LOGGER.error("%s: Device has no connection", self._address)
            return

        await self._conn.disconnect()

    async def waitConnected(self, timeout: int = 20):
        if self._conn == None:
            _LOGGER.error("%s: Device has no connection", self._address)
            return
        await self._conn.waitConnected(timeout=timeout)

    async def waitDisconnected(self):
        if self._conn == None:
            _LOGGER.error("%s: Device has no connection", self._address)
            return

        await self._conn.waitDisconnected()

    def register_callback(
        self, callback: Callable[[], None], propname: str | None = None
    ) -> None:
        """Register callback, called when Device changes state."""
        if propname is None:
            self._callbacks.add(callback)
        else:
            self._callbacks_map[propname] = self._callbacks_map.get(
                propname, set()
            ).union([callback])

    def remove_callback(
        self, callback: Callable[[], None], propname: str | None = None
    ) -> None:
        """Remove previously registered callback."""
        if propname is None:
            self._callbacks.discard(callback)
        else:
            self._callbacks_map.get(propname, set()).discard(callback)

    def update_callback(self, propname: str) -> None:
        """Find the registered callbacks in the map and then calling the callbacks"""
        for callback in self._callbacks_map.get(propname, set()):
            callback()

    def register_state_update_callback(
        self, state_update_callback: Callable[[Any], None], propname: str
    ):
        """Register a callback called that receives value of updated property"""
        self._state_update_callbacks[propname].add(state_update_callback)

    def remove_state_update_calback(
        self, callback: Callable[[Any], None], propname: str
    ):
        """Remove previously registered state update callback"""
        self._state_update_callbacks[propname].discard(callback)

    def update_state(self, propname: str, value: Any):
        """Run callback for updated state"""
        if propname not in self._state_update_callbacks:
            return
        for update in self._state_update_callbacks[propname]:
            update(value)

    def set_update_period(self, update_period: int | None):
        """Set number of seconds to wait between parsing messages"""
        self._update_period = update_period
        return self

    def allow_next_update(self):
        """
        Allow next received message to be parsed before next update period

        Useful for updating state after sending command to the device.
        """
        self._conn.allow_next_update()
