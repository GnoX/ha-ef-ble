import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.shp3 import Device
from custom_components.ef_ble.eflib.packet import Packet


@pytest.fixture
def packet_sequence():
    return [
        "aa030000de2df6160000065f3521010101520466",
        "aa0433000e0113012e475d393c554e3e575757575757573f3e2e0e4f0c0c21f11ad6040e2e0ee5311d151f5c5c5c5c5c5c5c5c3f3f3f3f3f3f3f3fb8b0",
        "aa04340065011301452c3652573e25553c3c3c3c3c3c3c545545652467674a9a71bd6f654565d66c67313027d1746464f0268c74d84b9474009c74643e16",
        "aa0420006601130146375651563d26563457575757575757574667276464499972be616646676f677964",
    ]


@pytest.fixture
def device(mocker: MockerFixture):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    adv_data = mocker.MagicMock()
    device = Device(ble_dev, adv_data, "HR63XXXXXXXXX001")
    device._conn = mocker.AsyncMock()
    return device


async def test_shp3_uses_v4_packet_version(device):
    assert device.packet_version == 0x04


async def test_shp3_parses_all_packets_successfully(device, packet_sequence):
    expected_cmd_ids = [0x52, 0x30, 0x30, 0x30]
    expected_cmd_sets = [0x01, 0x40, 0x40, 0x40]

    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert not Packet.is_invalid(packet), f"Packet {i} parsed as InvalidPacket"
        assert packet.cmdSet == expected_cmd_sets[i], (
            f"Packet {i} has unexpected cmdSet: 0x{packet.cmdSet:02x}"
        )
        assert packet.cmdId == expected_cmd_ids[i], (
            f"Packet {i} has unexpected cmdId: 0x{packet.cmdId:02x}"
        )


async def test_shp3_processes_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        processed = await device.data_parse(packet)
        assert processed is True, f"Packet {i} was not processed"


async def test_shp3_updates_master_state_from_v4_heartbeat(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[2]))
    await device.data_parse(packet)

    assert device.battery_level == 74.0


async def test_shp3_recognizes_sub_device_heartbeat(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[3]))
    processed = await device.data_parse(packet)
    assert processed is True
    assert packet.src == 0x30


async def test_shp3_v4_payload_is_fully_deobfuscated(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[1]))
    assert packet.payload[:9] == "XXXXXXX01".encode("ascii")


async def test_shp3_handles_v3_time_ping_without_crash(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[0]))
    processed = await device.data_parse(packet)
    assert processed is True
    assert packet.src == 0x35
    assert packet.cmdSet == 0x01
    assert packet.cmdId == Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME
