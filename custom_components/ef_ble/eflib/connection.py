import asyncio
import contextlib
import hashlib
import logging
import struct
import time
import traceback
from collections.abc import Awaitable, Callable
from enum import Enum, auto

import ecdsa
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError
from bleak_retry_connector import (
    MAX_CONNECT_ATTEMPTS,
    BleakClientWithServiceCache,
    BleakNotFoundError,
    establish_connection,
)
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from . import keydata
from .crc import crc16
from .encpacket import EncPacket
from .packet import Packet

_LOGGER = logging.getLogger(__name__)


class PacketParseError(Exception):
    """Error during parsing Packet"""


class EncPacketParseError(Exception):
    """Error during parsing EncPacket"""


class PacketReceiveError(Exception):
    """Error during receiving packet"""


class AuthFailedError(Exception):
    """Error during authentificating"""


class ConnectionState(Enum):
    INIT = auto()
    ERROR_TIMEOUT = auto()
    ERROR_NOT_FOUND = auto()
    ERROR_BLEAK = auto()
    ERROR_PACKET_PARSE = auto()
    ERROR_SEND_REQUEST = auto()
    ERROR_UNKNOWN = auto()
    ERROR_AUTH_FAILED = auto()
    AUTHENTICATED = auto()

    @property
    def is_processing_messages(self):
        return self in [ConnectionState.AUTHENTICATED]


class Connection:
    """Connection object manages client creation, authentification and sends the packets to parse back"""

    NOTIFY_CHARACTERISTIC = "00000003-0000-1000-8000-00805f9b34fb"
    WRITE_CHARACTERISTIC = "00000002-0000-1000-8000-00805f9b34fb"

    def __init__(
        self,
        ble_dev: BLEDevice,
        dev_sn: str,
        user_id: str,
        data_parse: Callable[[Packet], Awaitable[bool]],
        packet_parse: Callable[[bytes], Awaitable[Packet]],
        update_period: float | None = None,
        n_messages_per_update: int = 1,
    ) -> None:
        self._ble_dev = ble_dev
        self._address = ble_dev.address
        self._dev_sn = dev_sn
        self._user_id = user_id
        self._data_parse = data_parse
        self._packet_parse = packet_parse
        self._authenticated = False

        self._errors = 0
        self._last_error_msg = ""
        self._client = None
        self._connected = asyncio.Event()
        self._disconnected = asyncio.Event()
        self._retry_on_disconnect = False
        self._retry_on_disconnect_delay = 10
        self._state = ConnectionState.INIT
        self._cancel_lock = asyncio.Lock()

        self._enc_packet_buffer = b""
        self._tasks: list[asyncio.Task] = []
        self._cancelling = False

        # number of seconds to wait before processing next message
        self._update_period = update_period
        self._last_update = 0
        # number of messages to process in sequence (some devices send multiple images
        # with different fields set)
        self._n_messages_per_update = n_messages_per_update
        self._updated_current_period = self._n_messages_per_update

    @property
    def is_connected(self) -> bool:
        return self._client != None and self._client.is_connected

    def ble_dev(self) -> BLEDevice:
        return self._ble_dev

    async def connect(self, max_attempts: int = MAX_CONNECT_ATTEMPTS):
        self._connected.clear()
        self._disconnected.clear()

        error = None
        try:
            if self._client != None:
                if self._client.is_connected:
                    _LOGGER.warning("%s: Device is already connected", self._address)
                    return
                _LOGGER.info("%s: Reconnecting to device", self._address)
                await self._client.connect()
            else:
                _LOGGER.info("%s: Connecting to device", self._address)
                self._client = await establish_connection(
                    BleakClientWithServiceCache,
                    self.ble_dev(),
                    self._ble_dev.name,
                    disconnected_callback=self.disconnected,
                    ble_device_callback=self.ble_dev,
                    max_attempts=max_attempts,
                )
        except asyncio.TimeoutError as err:
            error = err
            self._state = ConnectionState.ERROR_TIMEOUT
        except BleakNotFoundError as err:
            error = err
            self._state = ConnectionState.ERROR_NOT_FOUND
        except BleakError as err:
            error = err
            self._state = ConnectionState.ERROR_BLEAK

        if error is not None:
            self._last_error_msg = str(error)
            _LOGGER.error(
                "%s: Failed to connect to the device: %s", self._address, error
            )
            self.disconnected()
            return

        _LOGGER.info(
            "%s: Connected",
            self._address,
        )
        self._errors = 0
        self._retry_on_disconnect = True
        self._retry_on_disconnect_delay = 10

        if self._client._backend.__class__.__name__ == "BleakClientBlueZDBus":
            await self._client._backend._acquire_mtu()
        _LOGGER.debug("%s: MTU: %d", self._address, self._client.mtu_size)

        _LOGGER.info("%s: Init completed, starting auth routine...", self._address)

        await self.initBleSessionKey()

    def disconnected(self, *args, **kwargs) -> None:
        _LOGGER.warning("%s: Disconnected from device", self._address)
        if self._retry_on_disconnect:
            loop = asyncio.get_event_loop()
            loop.create_task(self.reconnect())
        else:
            self._connected.set()
            self._disconnected.set()

    async def reconnect(self) -> None:
        # Wait before reconnect
        _LOGGER.warning(
            "%s: Reconnecting to the device in %d seconds...",
            self._address,
            self._retry_on_disconnect_delay,
        )
        await asyncio.sleep(self._retry_on_disconnect_delay)
        if not self._retry_on_disconnect:
            _LOGGER.warning("%s: Reconnect is aborted", self._address)
            return
        self._retry_on_disconnect_delay += 10
        await self.connect()

    async def disconnect(self) -> None:
        _LOGGER.info("%s: Disconnecting from device", self._address)
        self._retry_on_disconnect = False
        if self._client != None and self._client.is_connected:
            await self._client.disconnect()

    async def waitConnected(self, timeout: int = 20):
        """Will release when connection is happened and authenticated"""
        try:
            await asyncio.wait_for(self._connected.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            self._state = ConnectionState.ERROR_TIMEOUT

    async def waitDisconnected(self):
        """Will release when client got disconnected from the device"""
        await self._disconnected.wait()

    async def errorsAdd(self, exception: Exception):
        tb = traceback.format_tb(exception.__traceback__)
        _LOGGER.error(
            "%s: Captured exception: %s:\n%s", self._address, exception, "".join(tb)
        )
        if self._errors > 5:
            # Too much errors happened - let's reconnect
            self._errors = 0
            if self._client != None and self._client.is_connected:
                await self._client.disconnect()

    # En/Decrypt functions must create AES object every time, because
    # it saves the internal state after encryption and become useless
    async def decryptShared(self, encrypted_payload: str):
        aes_shared = AES.new(self._shared_key, AES.MODE_CBC, self._iv)
        return unpad(aes_shared.decrypt(encrypted_payload), AES.block_size)

    async def decryptSession(self, encrypted_payload: str):
        aes_session = AES.new(self._session_key, AES.MODE_CBC, self._iv)
        return unpad(aes_session.decrypt(encrypted_payload), AES.block_size)

    async def encryptSession(self, payload: str):
        aes_session = AES.new(self._session_key, AES.MODE_CBC, self._iv)
        return aes_session.encrypt(pad(payload, AES.block_size))

    async def genSessionKey(self, seed: bytes, srand: bytes):
        """Implements the necessary part of the logic, rest is skipped"""
        data_num = [0, 0, 0, 0]

        # Using seed and predefined key to get first 2 numbers
        pos = seed[0] * 0x10 + ((seed[1] - 1) & 0xFF) * 0x100
        data_num[0] = struct.unpack("<Q", keydata.get8bytes(pos))[0]
        pos += 8
        data_num[1] = struct.unpack("<Q", keydata.get8bytes(pos))[0]

        # Getting the last 2 numbers from srand
        srand_len = len(srand)
        lower_srand_len = srand_len & 0xFFFFFFFF
        if srand_len < 0x20:
            srand_len = 0
        else:
            raise Exception("Not implemented")

        # Just putting srand in there byte-by-byte
        data_num[2] = struct.unpack("<Q", srand[0:8])[0]
        data_num[3] = struct.unpack("<Q", srand[8:16])[0]

        # Converting data numbers to 32 bytes
        data = b""
        data += struct.pack("<Q", data_num[0])
        data += struct.pack("<Q", data_num[1])
        data += struct.pack("<Q", data_num[2])
        data += struct.pack("<Q", data_num[3])

        # Hashing data to get the session key
        session_key = hashlib.md5(data).digest()

        return session_key

    async def parseSimple(self, data: str):
        """Deserializes bytes stream into the simple bytes"""
        _LOGGER.debug("%s: parseSimple: Data: %r", self._address, bytearray(data).hex())

        header = data[0:6]
        data_end = 6 + struct.unpack("<H", header[4:6])[0]
        payload_data = data[6 : data_end - 2]
        payload_crc = data[data_end - 2 : data_end]

        # Check the payload CRC16
        if crc16(header + payload_data) != struct.unpack("<H", payload_crc)[0]:
            _LOGGER.error(
                "%s: parseSimple: Unable to parse simple packet - incorrect CRC16: %r",
                self._address,
                bytearray(payload_data).hex(),
            )
            raise PacketParseError

        return payload_data

    async def parseEncPackets(self, data: str):
        """Deserializes bytes stream into a list of Packets"""
        # In case there are leftovers from previous processing - adding them to current data
        if self._enc_packet_buffer:
            data = self._enc_packet_buffer + data
            self._enc_packet_buffer = b""

        _LOGGER.debug(
            "%s: parseEncPackets: Data: %r", self._address, bytearray(data).hex()
        )
        if len(data) < 8:
            _LOGGER.error(
                "%s: parseEncPackets: Unable to parse encrypted packet - too small: %r",
                self._address,
                bytearray(data).hex(),
            )
            raise EncPacketParseError

        # Data can contain multiple EncPackets and even incomplete ones, so walking through
        packets = []
        while data:
            if not data.startswith(EncPacket.PREFIX):
                _LOGGER.error(
                    "%s: parseEncPackets: Unable to parse encrypted packet - prefix is incorrect: %r",
                    self._address,
                    bytearray(data).hex(),
                )
                return packets

            header = data[0:6]
            data_end = 6 + struct.unpack("<H", header[4:6])[0]
            if data_end > len(data):
                self._enc_packet_buffer += data
                break

            payload_data = data[6 : data_end - 2]
            payload_crc = data[data_end - 2 : data_end]

            # Move to next data packet
            data = data[data_end:]

            try:
                # Check the packet CRC16
                if crc16(header + payload_data) != struct.unpack("<H", payload_crc)[0]:
                    _LOGGER.error(
                        "%s: Unable to parse encrypted packet - incorrect CRC16: %r",
                        self._address,
                        bytearray(payload_data).hex(),
                    )
                    raise PacketParseError

                # Decrypt the payload packet
                payload = await self.decryptSession(payload_data)
                _LOGGER.debug(
                    "%s: parseEncPackets: decrypted payload: %r",
                    self._address,
                    bytearray(payload).hex(),
                )

                # Parse packet
                packet = await self._packet_parse(payload)
                if packet is not None:
                    packets.append(packet)
            except Exception as e:
                self._state = ConnectionState.ERROR_PACKET_PARSE
                await self.errorsAdd(e)

        return packets

    async def sendRequest(self, send_data: bytes, response_handler=None):
        _LOGGER.debug("%s: Sending: %r", self._address, bytearray(send_data).hex())
        # In case exception happens we need to try again
        err = None
        for retry in range(3):
            try:
                await self._sendRequest(send_data, response_handler)
                return
            except Exception as e:
                if err is None:
                    err = e
                await asyncio.sleep(retry + 1)
                continue

        await self.errorsAdd(err)

    async def _sendRequest(self, send_data: bytes, response_handler=None):
        # Make sure the connection is here, otherwise just skipping
        if not self._client.is_connected:
            _LOGGER.debug(
                "%s: Skip sending: disconnected: %r",
                self._address,
                bytearray(send_data).hex(),
            )
            return
        if response_handler:
            await self._client.start_notify(
                Connection.NOTIFY_CHARACTERISTIC, response_handler
            )
        await self._client.write_gatt_char(
            Connection.WRITE_CHARACTERISTIC, bytearray(send_data)
        )

    async def sendPacket(self, packet: Packet, response_handler=None):
        _LOGGER.debug("%s: Sending packet: %r", self._address, packet)
        # Wrapping and encrypting with session key
        to_send = EncPacket(
            EncPacket.FRAME_TYPE_PROTOCOL,
            EncPacket.PAYLOAD_TYPE_VX_PROTOCOL,
            packet.toBytes(),
            0,
            0,
            self._session_key,
            self._iv,
        ).toBytes()

        await self.sendRequest(to_send, response_handler)

    async def replyPacket(self, packet: Packet):
        """Copies and changes the packet to be reply packet and sends it back to device"""
        # Found it's necesary to send back the packets, otherwise device will not send moar info
        # then strict minimum - which just about power params, but not configs & advanced params
        reply_packet = Packet(
            packet.dst,  # Switching src to dst
            packet.src,  # Switching dst to src
            packet.cmdSet,
            packet.cmdId,
            packet.payload,
            0x01,
            0x01,  # Replacing 0 with 1
            packet.version,
            packet.seq,
            packet.productId,
        )
        # Running reply asynchroneously
        await self._add_task(asyncio.create_task(self.sendPacket(reply_packet)))

    async def initBleSessionKey(self):
        _LOGGER.debug("%s: initBleSessionKey: Pub key exchange", self._address)
        self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP160r1)
        self._public_key = self._private_key.get_verifying_key()

        to_send = EncPacket(
            EncPacket.FRAME_TYPE_COMMAND,
            EncPacket.PAYLOAD_TYPE_VX_PROTOCOL,
            # Payload contains some weird prefix and generated public key
            b"\x01\x00" + self._public_key.to_string(),
        ).toBytes()

        # Device public key is sent as response, process will continue on device response in handler
        await self.sendRequest(to_send, self.initBleSessionKeyHandler)

    async def initBleSessionKeyHandler(
        self, characteristic: BleakGATTCharacteristic, recv_data: bytearray
    ):
        await self._client.stop_notify(Connection.NOTIFY_CHARACTERISTIC)

        data = await self.parseSimple(bytes(recv_data))
        if len(data) < 3:
            raise Exception(
                "Incorrect size of the returned pub key data: " + data.hex()
            )
        status = data[1]
        ecdh_type_size = getEcdhTypeSize(data[2])
        self._dev_pub_key = ecdsa.VerifyingKey.from_string(
            data[3 : ecdh_type_size + 3], curve=ecdsa.SECP160r1
        )

        # Generating shared key from our private key and received device public key
        # NOTE: The device will do the same with it's private key and our public key to generate the
        # same shared key value and use it to encrypt/decrypt using symmetric encryption algorithm
        self._shared_key = ecdsa.ECDH(
            ecdsa.SECP160r1, self._private_key, self._dev_pub_key
        ).generate_sharedsecret_bytes()
        # Set Initialization Vector from digest of the original shared key
        self._iv = hashlib.md5(self._shared_key).digest()
        if len(self._shared_key) > 16:
            # Using just 16 bytes of generated shared key
            self._shared_key = self._shared_key[0:16]

        await self.getKeyInfoReq()

    async def getKeyInfoReq(self):
        _LOGGER.debug("%s: getKeyInfoReq: Receiving session key", self._address)
        to_send = EncPacket(
            EncPacket.FRAME_TYPE_COMMAND,
            EncPacket.PAYLOAD_TYPE_VX_PROTOCOL,
            b"\x02",  # command to get key info to make the shared key
        ).toBytes()

        await self.sendRequest(to_send, self.getKeyInfoReqHandler)

    async def getKeyInfoReqHandler(
        self, characteristic: BleakGATTCharacteristic, recv_data: bytearray
    ):
        await self._client.stop_notify(Connection.NOTIFY_CHARACTERISTIC)
        encrypted_data = await self.parseSimple(bytes(recv_data))

        if encrypted_data[0] != 0x02:
            raise Exception(
                "Received type of KeyInfo is != 0x02, need to dig into: "
                + encrypted_data.hex()
            )

        # Skipping the first byte - type of the payload (0x02)
        data = await self.decryptShared(encrypted_data[1:])

        # Parse the data that contains sRand (first 16 bytes) & seed (last 2 bytes)
        self._session_key = await self.genSessionKey(data[16:18], data[:16])

        await self.getAuthStatus()

    async def getAuthStatus(self):
        _LOGGER.debug("%s: getKeyInfoReq: Receiving auth status", self._address)

        # Preparing packet with empty payload
        packet = Packet(0x21, 0x35, 0x35, 0x89, b"", 0x01, 0x01, 0x03)

        await self.sendPacket(packet, self.getAuthStatusHandler)

    async def getAuthStatusHandler(
        self, characteristic: BleakGATTCharacteristic, recv_data: bytearray
    ):
        await self._client.stop_notify(Connection.NOTIFY_CHARACTERISTIC)
        packets = await self.parseEncPackets(bytes(recv_data))
        if len(packets) < 1:
            raise PacketReceiveError
        data = packets[0].payload

        _LOGGER.debug(
            "%s: getAuthStatusHandler: data: %r", self._address, bytearray(data).hex()
        )
        await self.autoAuthentication()

    async def autoAuthentication(self):
        _LOGGER.info(
            "%s: autoAuthentication: Sending secretKey consists of user id and device serial number",
            self._address,
        )

        # Building payload for auth
        md5_data = hashlib.md5((self._user_id + self._dev_sn).encode("ASCII")).digest()
        # We need upper case in MD5 data here
        payload = ("".join(f"{c:02X}" for c in md5_data)).encode("ASCII")

        # Forming packet
        packet = Packet(0x21, 0x35, 0x35, 0x86, payload, 0x01, 0x01, 0x03)

        # Sending request and starting the common listener
        await self.sendPacket(packet, self.listenForDataHandler)

    def _can_update(self):
        # can update if
        # 1. update_period is 0 or we are not yet authenticated
        if not self._update_period or not self._state.is_processing_messages:
            return True

        # 2. if we are waiting for next message in sequence
        if self._updated_current_period > 0:
            self._updated_current_period -= 1
            return True

        # 3. if less than update_period seconds have passed since last message
        now = time.time()
        if now - self._last_update < self._update_period:
            return False

        self.allow_next_update()
        return True

    def allow_next_update(self):
        """
        Allow next received message to be parsed before next update period

        Useful for updating state after sending command to the device.
        """
        self._last_update = 0
        self._updated_current_period = self._n_messages_per_update

    async def listenForDataHandler(
        self, characteristic: BleakGATTCharacteristic, recv_data: bytearray
    ):
        if not self._can_update():
            return

        try:
            packets = await self.parseEncPackets(bytes(recv_data))
        except Exception as e:
            self._state = ConnectionState.ERROR_PACKET_PARSE
            await self.errorsAdd(e)
            return

        for packet in packets:
            processed = False

            # Handling autoAuthentication response
            if packet.src == 0x35 and packet.cmdSet == 0x35 and packet.cmdId == 0x86:
                if packet.payload != b"\x00":
                    # TODO: Most probably we need to follow some other way for auth, but happens rarely
                    _LOGGER.error(
                        "%s: Auth failed with response: %r", self._address, packet
                    )
                    self._state = ConnectionState.ERROR_AUTH_FAILED
                    self._connected.set()
                    raise AuthFailedError
                processed = True
                _LOGGER.info("%s: Auth completed, everything is fine", self._address)
                self._state = ConnectionState.AUTHENTICATED
                self._connected.set()
            else:
                # Processing the packet with specific device
                processed = await self._data_parse(packet)

            if not processed:
                _LOGGER.debug("%s: listenForDataHandler: %r", self._address, packet)

    async def _cancel_tasks(self):
        for task in self._tasks:
            task.cancel()

            with contextlib.suppress(asyncio.CancelledError):
                await task

        async with self._cancel_lock:
            self._tasks = []

    async def _add_task(self, task: asyncio.Task):
        async with self._cancel_lock:
            self._tasks.append(task)


def getEcdhTypeSize(curve_num: int):
    """Returns size of ecdh based on type"""
    match curve_num:
        case 1:
            return 52
        case 2:
            return 56
        case 3, 4:
            return 64
        case _:
            return 40
