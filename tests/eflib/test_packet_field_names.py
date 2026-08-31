"""Both spellings of a packet's command fields have to resolve"""

from custom_components.ef_ble.eflib.packet import Packet, PacketV4


def test_packet_exposes_command_fields_under_both_names():
    packet = Packet(0x21, 0x35, 0x35, 0x86, b"")

    assert packet.cmd_set == packet.cmdSet == 0x35
    assert packet.cmd_id == packet.cmdId == 0x86
    assert packet.product_id == packet.productId == 0


def test_packet_v4_exposes_command_fields_under_both_names():
    packet = PacketV4(0x21, 0x02, 0xFE, 0x26, b"")

    assert packet.cmd_set == packet.cmdSet == 0xFE
    assert packet.cmd_id == packet.cmdId == 0x26
