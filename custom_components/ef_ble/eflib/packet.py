import logging
import struct
from functools import cached_property
from typing import TypeGuard

from .crc import crc8, crc16

_LOGGER = logging.getLogger(__name__)


class Packet:
    PREFIX = b"\xaa"

    NET_BLE_COMMAND_CMD_CHECK_RET_TIME = 0x53
    NET_BLE_COMMAND_CMD_SET_RET_TIME = 0x52

    def __init__(
        self,
        src,
        dst,
        cmd_set,
        cmd_id,
        payload=b"",
        dsrc=1,
        ddst=1,
        version=3,
        seq=None,
        product_id=0,
    ):
        self._src = src
        self._dst = dst
        self._cmd_set = cmd_set
        self._cmd_id = cmd_id
        self._payload = payload
        self._dsrc = dsrc
        self._ddst = ddst
        self._version = version
        self._seq = seq if seq is not None else b"\x00\x00\x00\x00"
        self._product_id = product_id

    @property
    def src(self):
        return self._src

    @property
    def dst(self):
        return self._dst

    @property
    def cmdSet(self):
        return self._cmd_set

    @property
    def cmdId(self):
        return self._cmd_id

    @property
    def payload(self):
        return self._payload

    @cached_property
    def payload_hex(self):
        return bytearray(self._payload).hex()

    @property
    def dsrc(self):
        return self._dsrc

    @property
    def ddst(self):
        return self._ddst

    @property
    def version(self):
        return self._version

    @property
    def seq(self):
        return self._seq

    @property
    def productId(self):
        return self._product_id

    @staticmethod
    def fromBytes(data: bytes, xor_payload: bool = False):
        """Deserialize bytes stream into internal data"""
        if not data.startswith(Packet.PREFIX):
            error_msg = "Unable to parse packet - prefix is incorrect: %s"
            _LOGGER.error(error_msg, bytearray(data).hex())
            return InvalidPacket(error_msg % bytearray(data).hex())

        version_byte = data[1]

        if version_byte == 4:
            return PacketV4.fromBytes(data)

        version = version_byte & 0x0F
        sentinel_format = (version_byte & 0x10) != 0

        if (version == 2 and len(data) < 18) or (version == 3 and len(data) < 20):
            error_msg = "Unable to parse packet - too small: %s"
            _LOGGER.error(error_msg, bytearray(data).hex())
            return InvalidPacket(error_msg % bytearray(data).hex())

        payload_length = struct.unpack("<H", data[2:4])[0]

        # Sentinel-format frames (high-nibble bit set, e.g. 0x13) carry a 0xBB
        # 0xBB sentinel inside the payload instead of a trailing CRC16.
        if version in (2, 3) and not sentinel_format:
            if crc16(data[:-2]) != struct.unpack("<H", data[-2:])[0]:
                error_msg = "Unable to parse packet - incorrect CRC16: %s"
                _LOGGER.error(error_msg, bytearray(data).hex())
                return InvalidPacket(error_msg % bytearray(data).hex())

        # Check header CRC8
        if crc8(data[:4]) != data[4]:
            error_msg = "Unable to parse packet - incorrect header CRC8: %s"
            _LOGGER.error(error_msg, bytearray(data).hex())
            return InvalidPacket(error_msg % bytearray(data).hex())

        # data[4] # crc8 of header
        # product_id = data[5] # We can't determine the product id from the bytestream

        # Seq is used for multiple purposes, so leaving as is
        seq = data[6:10]
        # data[10:12] # static zeroes in V2/V3; used differently in V19
        src = data[12]
        dst = data[13]

        dsrc = ddst = 0
        payload_start = 16 if version == 2 else 18

        if version == 2:
            cmd_set, cmd_id = data[14:payload_start]
        else:
            dsrc, ddst, cmd_set, cmd_id = data[14:payload_start]

        payload = b""
        if payload_length > 0:
            payload = data[payload_start : payload_start + payload_length]

            # When the high-nibble bit is set, the device XORs the payload
            # with seq[0] before transmission - undo it here.
            if xor_payload and seq[0] != 0:
                payload = bytes(c ^ seq[0] for c in payload)

            if sentinel_format and payload[-2:] == b"\xbb\xbb":
                payload = payload[:-2]

        return Packet(
            src=src,
            dst=dst,
            cmd_set=cmd_set,
            cmd_id=cmd_id,
            payload=payload,
            dsrc=dsrc,
            ddst=ddst,
            version=version_byte,
            seq=seq,
        )

    def toBytes(self):
        """Will serialize the internal data to bytes stream"""
        # Header
        data = Packet.PREFIX
        data += struct.pack("<B", self._version) + struct.pack("<H", len(self._payload))
        # Header crc
        data += struct.pack("<B", crc8(data))
        # Additional data
        data += self.productByte() + self._seq
        data += b"\x00\x00"  # Unknown static zeroes, no strings attached right now

        data += struct.pack("<B", self._src) + struct.pack("<B", self._dst)

        # V3+ includes dsrc/ddst fields, V2 does not
        if self._version >= 0x03:
            data += struct.pack("<B", self._dsrc) + struct.pack("<B", self._ddst)

        data += struct.pack("<B", self._cmd_set) + struct.pack("<B", self._cmd_id)
        # Payload
        data += self._payload
        # Packet crc
        data += struct.pack("<H", crc16(data))

        return data

    def productByte(self):
        """Return magics depends on product id"""

        if self._product_id >= 0:
            return b"\x0d"
        return b"\x0c"

    def __repr__(self):
        return (
            "Packet("
            f"src=0x{self._src:02X}, "
            f"dst=0x{self._dst:02X}, "
            f"cmd_set=0x{self._cmd_set:02X}, "
            f"cmd_id=0x{self._cmd_id:02X}, "
            f"payload=bytes.fromhex('{self.payload_hex}'), "
            f"dsrc=0x{self._dsrc:02X}, "
            f"ddst=0x{self._ddst:02X}, "
            f"version=0x{self._version:02X}, "
            f"seq={self._seq}, "
            f"product_id=0x{self._product_id:02X}"
            ")"
        )

    @staticmethod
    def is_invalid(
        packet: "Packet | PacketV4 | InvalidPacket",
    ) -> TypeGuard["InvalidPacket"]:
        """Check if the given packet is invalid."""
        return isinstance(packet, InvalidPacket)


class PacketV4:
    """
    V4 (version 0x04) packet codec.

    Wire format:
      [0]      0xaa prefix
      [1]      version
      [2:3]    payload_length LE
      [4]      CRC8 of bytes 0..3 - also the XOR key for bytes [8:]
      [5]      type_byte: enc_type[7:5] | check_type[4:2] | is_rw_cmd[1] | is_ack[0]
      [6]      v4_type_a - part of V4 session info
      [7]      v4_type_b - layer-3 XOR key when non-zero

      [8]      cmd_flags  (inner cmd header byte 0, always has bit 5 set after XOR)
      [9]      frame_type
      [10]     payload_type
      [11]     time_snap_b0
      [12]     src
      [13]     dst
      [14]     cmd_set
      [15]     cmd_id
      [16:8+payload_length-1] data payload (for SHP3 - first 22 bytes is routing header)

      [8+payload_length:-1]   CRC16 LE  (computed over obfuscated bytes)

    Two layers of obfuscation are applied to the body:

    1. CRC8 layer (always applied) - every byte from position [8] onward (inner cmd
       header + payload) is XOR'd with the outer header CRC8 value at data[4]
    2. v4_type_b layer (applied to the application payload only when v4_type_b is
       non-zero)
    """

    PREFIX = b"\xaa"
    VERSION = 0x04

    def __init__(
        self,
        src,
        dst,
        cmd_set,
        cmd_id,
        payload=b"",
        enc_type=0,
        check_type=0,
        is_rw_cmd=False,
        is_ack=False,
        frame_type=0,
        payload_type=0,
        cmd_flags=0x20,
        v4_type_a=0,
        v4_type_b=0,
        time_snap_b0=0,
    ):
        self._src = src
        self._dst = dst
        self._cmd_set = cmd_set
        self._cmd_id = cmd_id
        self._payload = payload

        self._enc_type = enc_type
        self._check_type = check_type
        self._is_rw_cmd = is_rw_cmd
        self._is_ack = is_ack
        self._frame_type = frame_type
        self._payload_type = payload_type
        self._cmd_flags = cmd_flags
        self._v4_type_a = v4_type_a
        self._v4_type_b = v4_type_b
        self._time_snap_b0 = time_snap_b0

    @property
    def src(self):
        return self._src

    @property
    def dst(self):
        return self._dst

    @property
    def cmdSet(self):
        return self._cmd_set

    @property
    def cmdId(self):
        return self._cmd_id

    @property
    def payload(self):
        return self._payload

    @cached_property
    def payload_hex(self):
        return bytearray(self._payload).hex()

    @property
    def version(self):
        return self.VERSION

    @property
    def encType(self):
        return self._enc_type

    @property
    def checkType(self):
        return self._check_type

    @property
    def isRwCmd(self):
        return self._is_rw_cmd

    @property
    def isAck(self):
        return self._is_ack

    @property
    def frameType(self):
        return self._frame_type

    @property
    def payloadType(self):
        return self._payload_type

    @property
    def cmdFlags(self):
        return self._cmd_flags

    @property
    def v4TypeA(self):
        return self._v4_type_a

    @property
    def v4TypeB(self):
        return self._v4_type_b

    @property
    def timeSnapB0(self):
        return self._time_snap_b0

    @staticmethod
    def fromBytes(data: bytes) -> "PacketV4 | InvalidPacket":
        if len(data) < 18:
            error_msg = "Unable to parse packet - too small: %s"
            _LOGGER.error(error_msg, bytearray(data).hex())
            return InvalidPacket(error_msg % bytearray(data).hex())

        payload_length = struct.unpack("<H", data[2:4])[0]

        if crc16(data[:-2]) != struct.unpack("<H", data[-2:])[0]:
            error_msg = "Unable to parse packet - incorrect CRC16: %s"
            _LOGGER.error(error_msg, bytearray(data).hex())
            return InvalidPacket(error_msg % bytearray(data).hex())

        if crc8(data[:4]) != data[4]:
            error_msg = "Unable to parse packet - incorrect header CRC8: %s"
            _LOGGER.error(error_msg, bytearray(data).hex())
            return InvalidPacket(error_msg % bytearray(data).hex())

        if payload_length < 8:
            error_msg = "Unable to parse packet - V4 payload too short: %s"
            _LOGGER.error(error_msg, bytearray(data).hex())
            return InvalidPacket(error_msg % bytearray(data).hex())

        # Outer header fields - bytes [5:7] are not obfuscated
        type_byte = data[5]
        enc_type = (type_byte >> 5) & 0x7
        check_type = (type_byte >> 2) & 0x7
        is_rw_cmd = bool((type_byte >> 1) & 0x1)
        is_ack = bool(type_byte & 0x1)
        v4_type_a = data[6]
        v4_type_b = data[7]

        # Layer-2 deobfuscate - XOR bytes [8:8+payload_length] with the CRC8 key
        xor_key = data[4]
        inner_and_payload = bytes(b ^ xor_key for b in data[8 : 8 + payload_length])

        # Inner command header occupies the first 8 bytes of the deobfuscated block
        cmd_flags = inner_and_payload[0]
        frame_type = inner_and_payload[1]
        payload_type_val = inner_and_payload[2]
        time_snap_b0 = inner_and_payload[3]
        src = inner_and_payload[4]
        dst = inner_and_payload[5]
        cmd_set = inner_and_payload[6]
        cmd_id = inner_and_payload[7]

        actual_payload_len = payload_length - 8
        if actual_payload_len > 0:
            payload = inner_and_payload[8 : 8 + actual_payload_len]
            # Layer-3 deobfuscation - when v4_type_b is non-zero the device XOR-encodes
            # the application payload with it before encryption
            if v4_type_b:
                payload = bytes(b ^ v4_type_b for b in payload)
        else:
            payload = b""

        return PacketV4(
            src=src,
            dst=dst,
            cmd_set=cmd_set,
            cmd_id=cmd_id,
            payload=payload,
            enc_type=enc_type,
            check_type=check_type,
            is_rw_cmd=is_rw_cmd,
            is_ack=is_ack,
            frame_type=frame_type,
            payload_type=payload_type_val,
            cmd_flags=cmd_flags,
            v4_type_a=v4_type_a,
            v4_type_b=v4_type_b,
            time_snap_b0=time_snap_b0,
        )

    def toBytes(self) -> bytes:
        inner_cmd = bytes(
            [
                self._cmd_flags,
                self._frame_type,
                self._payload_type,
                self._time_snap_b0,
                self._src,
                self._dst,
                self._cmd_set,
                self._cmd_id,
            ]
        )

        payload_length = 8 + len(self._payload)

        type_byte = (
            ((self._enc_type & 0x7) << 5)
            | ((self._check_type & 0x7) << 2)
            | (int(self._is_rw_cmd) << 1)
            | int(self._is_ack)
        )

        # Build outer header; CRC8 byte is also the XOR key for the inner content
        data = PacketV4.PREFIX
        data += struct.pack("<B", self.VERSION) + struct.pack("<H", payload_length)
        crc8_byte = crc8(data)
        data += struct.pack("<B", crc8_byte)
        data += struct.pack("<B", type_byte)
        data += struct.pack("<B", self._v4_type_a) + struct.pack("<B", self._v4_type_b)

        if self._v4_type_b:
            payload = bytes(b ^ self._v4_type_b for b in self._payload)
        else:
            payload = self._payload
        inner_content = inner_cmd + payload
        data += bytes(b ^ crc8_byte for b in inner_content)

        data += struct.pack("<H", crc16(data))

        return data

    def __repr__(self):
        return (
            "PacketV4("
            f"src=0x{self._src:02X}, "
            f"dst=0x{self._dst:02X}, "
            f"cmd_set=0x{self._cmd_set:02X}, "
            f"cmd_id=0x{self._cmd_id:02X}, "
            f"payload=bytes.fromhex('{self.payload_hex}'), "
            f"enc_type={self._enc_type}, "
            f"check_type={self._check_type}, "
            f"is_rw_cmd={self._is_rw_cmd}, "
            f"is_ack={self._is_ack}, "
            f"frame_type=0x{self._frame_type:02X}, "
            f"payload_type=0x{self._payload_type:02X}, "
            f"cmd_flags=0x{self._cmd_flags:02X}, "
            f"v4_type_a=0x{self._v4_type_a:02X}, "
            f"v4_type_b=0x{self._v4_type_b:02X}, "
            f"time_snap_b0=0x{self._time_snap_b0:02X}"
            ")"
        )


class InvalidPacket(Packet):
    """Represents an invalid packet that could not be parsed"""

    def __init__(self, error_message: str):
        super().__init__(src=0, dst=0, cmd_set=0, cmd_id=0, payload=b"")
        self.error_message = error_message

    def __bool__(self):
        return False

    def __repr__(self):
        return f"InvalidPacket(error_message='{self.error_message}')"
