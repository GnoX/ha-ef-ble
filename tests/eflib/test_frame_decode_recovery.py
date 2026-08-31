"""A device repeating a handshake reply must not spend the session-loss budget"""

from custom_components.ef_ble.eflib.encpacket import EncPacket
from custom_components.ef_ble.eflib.encryption import Type7Encryption
from custom_components.ef_ble.eflib.frame_assembler import (
    EncPacketAssembler,
    SimplePacketAssembler,
)


def _assembler() -> EncPacketAssembler:
    return EncPacketAssembler(Type7Encryption(b"\x11" * 16, b"\x22" * 16))


async def test_plaintext_command_frames_are_not_decrypted_as_device_data():
    frame = SimplePacketAssembler.encode(b"\x02" + b"\x33" * 32)

    assert await _assembler().reassemble(frame) == []


async def test_a_command_frame_does_not_hide_the_data_frame_behind_it():
    assembler = _assembler()
    payload = b"\x0a\x04test"
    data_frame = EncPacket(
        EncPacket.FRAME_TYPE_PROTOCOL,
        EncPacket.PAYLOAD_TYPE_VX_PROTOCOL,
        payload,
        0,
        0,
        b"\x11" * 16,
        b"\x22" * 16,
    ).to_bytes()
    frame = SimplePacketAssembler.encode(b"\x01" + b"\x44" * 42) + data_frame

    assert await assembler.reassemble(frame) == [payload]
