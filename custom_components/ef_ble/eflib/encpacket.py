import struct
from dataclasses import dataclass
from typing import ClassVar

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .crc import crc16


@dataclass(slots=True)
class EncPacket:
    """Outside wrapper of Packet that actually transferred through the BLE channel"""

    frame_type: int
    payload_type: int
    payload: bytes
    cmd_id: int = 0
    version: int = 0
    enc_key: bytes | None = None
    iv: bytes | None = None

    PREFIX: ClassVar[bytes] = b"\x5a\x5a"

    FRAME_TYPE_COMMAND: ClassVar[int] = 0x00
    FRAME_TYPE_PROTOCOL: ClassVar[int] = 0x01
    FRAME_TYPE_PROTOCOL_INT: ClassVar[int] = 0x10

    PAYLOAD_TYPE_VX_PROTOCOL: ClassVar[int] = 0x00
    PAYLOAD_TYPE_ODM_PROTOCOL: ClassVar[int] = 0x04

    def encrypt_payload(self) -> bytes:
        if self.enc_key is None or self.iv is None:
            return self.payload  # Not encrypted

        engine = AES.new(self.enc_key, AES.MODE_CBC, self.iv)
        return engine.encrypt(pad(self.payload, AES.block_size))

    def to_bytes(self) -> bytes:
        """Will serialize the internal data to bytes stream"""
        payload = self.encrypt_payload()

        data = (
            EncPacket.PREFIX + struct.pack("<B", self.frame_type << 4) + b"\x01"
        )  # Unknown byte
        data += struct.pack("<H", len(payload) + 2)  # +2 here is len(crc16)
        data += payload
        data += struct.pack("<H", crc16(data))

        return data
