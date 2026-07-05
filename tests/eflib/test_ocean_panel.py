import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.ocean_panel import (
    CircuitStatus,
    Device,
    GridStatus,
)
from custom_components.ef_ble.eflib.packet import Packet, PacketV4
from custom_components.ef_ble.eflib.pb import dev_apl_comm_pb2


def _config_write(packet) -> dev_apl_comm_pb2.ConfigWrite:
    """Decode the ConfigWrite carried by a control write (v4 mirror or v3 fallback)"""
    payload = packet.payload
    if isinstance(packet, PacketV4):
        marker = payload.index(bytes([0xFE, 0x11]))
        payload = payload[marker + 7 :]
    config = dev_apl_comm_pb2.ConfigWrite()
    config.ParseFromString(payload)
    return config


@pytest.fixture
def packet_sequence():
    # Real OCEAN Pro (HR61) captures, deobfuscated round-trip and scrubbed of personal
    # data: device serials masked to "XXXXXXX01", timezone reset to UTC, circuit names
    # replaced with generic "Circuit N" labels. All telemetry values are unchanged.
    return [
        # V4 single-field DisplayPropertyUpload (plug_in_info_acp_charger_flag)
        "aa042d008f011301afc6dcb8bfd4cfbfd6d6d6d6d6d6d6bebfaf8fce8d8da8709775858faf8f0e898803898e8e7ecc1b898e8efecc41bd",
        # V4 RuntimePropertyUpload (firmware ver, EMS state, inverter frequency)
        "aa045100d1011301f19882e6e18a91e188888888888888e0e1f1d190d3d3f62ec63adbd1f1d150db575550c078c23077c260c23004d368c27027e610c2702eda70f1d0508d409e5d8dd0d0a092458dabc4aa924d8dd0d0a09298e2",
        # V4 DisplayPropertyUpload with per-circuit status (load_ch26_sta..load_ch34_sta)
        "aa045c013f0113011f766c080f647f0f666666666666660e0f1f3f7e3d3d18c02b76353f1f3f94041f363f2c3a363f2e22233e3e767c1e3b14347d574c5d4b574a1e0c080e3f043c36308c0421363f2c3a363f2e23233e3ece7f1e3d14347d574c5d4b574a1e0c09043c363484041f363f2c3a363f2e24233e3e767c1e3b14347d574c5d4b574a1e0c060e3f043c3631fc0421363f2c3a363f2e25233e3ece7f1e3d14347d574c5d4b574a1e0c07043c3635f4041f363f2c3a363f2e1e233e3ef67c1e2d14347d574c5d4b574a1e0d0e0e3f043c3636ec041f363f2c3a363f2e1f233e3ece7f1e3a14347d574c5d4b574a1e0d0f0e3f043c3659e4041f363f2c3a363f2e20233e3ef67c1e2d14347d574c5d4b574a1e0d0c0e3f043c3637dc041f363f2c3a363f2e21233e3ece7f1e3a14347d574c5d4b574a1e0d0d0e3f043c3656d40421363f2c3a363f2e1a233e3ef67c14347d574c5d4b574a1e0d0a0e3f043c361ce6e7",
        # V4 DisplayPropertyUpload: battery, system/grid load, battery flow, PV, times
        "aa04ff001f0113013f564c282f445f2f464646464646462e2f3f1f5e1d1d30e00bf6151f3f1f0e1eec191eb6161eac161d4b4a5da6161eab0e1e1ede5cfe0edc1df60e1eee0e44e60e1ece0f1ff60f1eee0f1ede0d1ed4061ef6061ef6022cee02a8b91f86031fbe031eb6031e833e1e1e1e1ebb3e639b275bb33e1e1e4f5dab3e636b32dbde3e1cd63edea51fc63e1efe3e1eee3e1ee43e1e843f161418945e9e9e9e14b63f1eab3f1e1e1e1ea33f1e1e1e1ece3f36fe3f2ce63f1f9e3cf619963cf6198e3c1e863c1ea33b1e1e1e1edb3b1e1e1e1ed33b1e1e1e1ecb3b1e1e1e1efe3b9c1af63b1eee3b1ee63b1ec6381f84391eb4391ede447ace431ede7e1ed67e1ec67e1e49a8",
        # V4 DisplayPropertyUpload (incremental): grid_is_energized, backup channels
        "aa0490002901130109607a1e197269197070707070707018190929682b2b06d63dcf23290929820f28a80729b8072bc818e89329d21820222a3829222a382be819c02fe019dc2b981a1a921a20202d382a0a2a0a0cea1a28e21a28801b29ea6422202a302d082a002a1829e26422202a302e082a002a1829fa6422202a302f082a002a1829c865c875c2652a20298066299873b86688752a263f",
        # V3 time request (src 0x35, cmd_set 0x01, cmd_id 0x52 RET_TIME) - no payload
        "aa030000de2df6160000065f3521010101520466",
    ]


@pytest.fixture
def device(mocker: MockerFixture):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    adv_data = mocker.MagicMock()
    device = Device(ble_dev, adv_data, "HR61XXXXXXXXX001")
    device._conn = mocker.AsyncMock()
    device._conn._user_id = "test-user-id"
    return device


def test_ocean_panel_recognizes_hr61_family():
    # HR61 / HR6B / HR6D are the OCEAN Panel (product_shp3_shp3).
    assert Device.check(b"HR61XXXXXXXXX001")
    assert Device.check(b"HR6BXXXXXXXXX001")
    assert not Device.check(b"HR51XXXXXXXXX001")  # OCEAN Pro inverter, not the panel


async def test_ocean_panel_auth_uses_v3_packet_version(device):
    assert device.packet_version == 0x03


async def test_ocean_panel_parses_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert not Packet.is_invalid(packet), f"Packet {i} parsed as InvalidPacket"


async def test_ocean_panel_processes_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        processed = await device.data_parse(packet)
        assert processed is True, f"Packet {i} was not processed"


async def test_ocean_panel_telemetry_is_v4_from_expected_address(
    device, packet_sequence
):
    for hex_packet in packet_sequence[:5]:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert isinstance(packet, PacketV4)
        assert (packet.src, packet.cmd_set, packet.cmd_id) == (0x30, 0x40, 0x30)


async def test_ocean_panel_v4_payload_is_fully_deobfuscated(device, packet_sequence):
    for hex_packet in packet_sequence[:5]:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert packet.payload[:9] == b"XXXXXXX01"


async def test_ocean_panel_exact_values_from_known_packets(device, packet_sequence):
    """Feed the full capture sequence and assert the exact decoded values"""
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    assert device.battery_level == 96.0
    assert device.battery_power == -2759.34
    assert device.load_system == 2968.34
    assert device.load_from_grid == 0.0
    assert device.pv_power_sum == 209.0
    assert device.remaining_time_charging == 0
    assert device.remaining_time_discharging == 450
    assert device.inverter_frequency == 60.0
    assert device.grid_connection_status is GridStatus.GRID_IN
    assert device.grid_is_energized is True
    assert device.plugged_in_ac is True


async def test_ocean_panel_decodes_circuit_status_and_names(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[2]))
    await device.data_parse(packet)

    assert device.circuit_status[26] is CircuitStatus.ON_GRID
    assert device.circuit_status[34] is CircuitStatus.ON_GRID
    assert device.circuit_name[26] == "Circuit 26"
    assert device.circuit_name[34] == "Circuit 34"
    assert device.circuit_split_link[26] == 28


async def test_ocean_panel_set_circuit_power_gangs_split_phase(device, packet_sequence):
    """Toggling a split-phase circuit switches both breaker legs (ch26 links ch28)"""
    await device.data_parse(
        await device.packet_parse(bytes.fromhex(packet_sequence[2]))
    )
    assert device.circuit_split_link[26] == 28

    await device.set_circuit_power(26, False)
    config = _config_write(device._conn.sendPacket.await_args.args[0])
    assert config.cfg_load_ch26_ctrl_info.chanel_enable_ctrl == 2  # OFF
    assert config.cfg_load_ch28_ctrl_info.chanel_enable_ctrl == 2  # ganged leg
    assert (
        config.cfg_load_ch26_ctrl_info.ctrl_mode
        == dev_apl_comm_pb2.LOAD_RLY_CTRL_MODE_HAND
    )


async def test_ocean_panel_registers_userid_once_on_time_request(
    device, packet_sequence
):
    """The one-time user-id frame (cmd_set 0x35 / cmd_id 0xA8) is sent post-auth"""
    time_request = packet_sequence[5]
    await device.data_parse(await device.packet_parse(bytes.fromhex(time_request)))

    userid = [
        c.args[0]
        for c in device._conn.sendPacket.await_args_list
        if (c.args[0].cmd_set, c.args[0].cmd_id) == (0x35, 0xA8)
    ]
    assert len(userid) == 1
    assert userid[0].payload[0] == 0x01
    assert len(userid[0].payload) == 69

    # A second time request must not re-register.
    device._conn.sendPacket.reset_mock()
    await device.data_parse(await device.packet_parse(bytes.fromhex(time_request)))
    assert not [
        c
        for c in device._conn.sendPacket.await_args_list
        if (c.args[0].cmd_set, c.args[0].cmd_id) == (0x35, 0xA8)
    ]
