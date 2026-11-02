from custom_components.ef_ble.eflib.frame_assembler import SimplePacketAssembler


def test_simple_packet_assembler_encodes_command_frame():
    payload = b"\x01\x00test"

    encoded = SimplePacketAssembler.encode(payload)

    assert encoded.startswith(b"\x5a\x5a")
    assert SimplePacketAssembler().parse(encoded) == payload
