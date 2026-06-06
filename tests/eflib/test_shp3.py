import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.shp3 import Device, GridStatus
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import dev_apl_comm_pb2
from custom_components.ef_ble.eflib.props import FieldGroup


@pytest.fixture
def packet_sequence():
    return [
        # time request (src 0x35) - no payload
        "aa030000de2df6160000065f3521010101520466",
        # master heartbeat: battery / backup / limits / load / per-circuit power
        "aa044e0142011301620b1175701902721b1b1b1b1b1b1b737262420340406dbd56cf484262425343ee4043434343b14443f14b40161700f65343438b01a35343ab5343b35327bb5343935243ab5243b35243835043895b43ab5b43ab5f71b35f43db5e42e35e43eb5e43de63ff265d06e663ff265d06ee6343434343f663434343438363428b63439b6343a36343b36343b96343d9624b4945c903c3c3c34793626ba36271bb6243c361ab44be6443434343b67343434343c97c43d17c43d97c43b103494e7eb9ae015e833a5e7db9034c4e8dffa80156914f2e815e29a2667cc1024c4e7307a80156c09fcc815eeb54d87cc90243d1024c4e6f9faa0156f5db2a875e2c75b803d902465e6a8ae57de10243e902465e742b3a7df10243fe010ee8b30186014a4fb201831971ab1fab07b31fc924931e438323a5508b23439b2343b3234dbb2342832257a30c43c32643d92a43e32a42eaac",
        # master heartbeat: grid voltage / current and per-circuit voltage / current
        "aa0440029d011301bdd4ceaaafc6ddadc4c4c4c4c4c4c4acadbd9ddc9f9fb262891d979dbd9d26a685949d819c9c28debc97b696dff5eeffe9f5e8bcaea4a69e94f75ea685819c9c28debc9db696dff5eeffe9f5e8bcaea5a69e94fbdc9d56a685819c9c28debc9db696dff5eeffe9f5e8bcafaca69e94f4dc9d4ea685819c9c28debc9db696dff5eeffe9f5e8bcafada69e94f5dc9d46a685819c9c28debc9db696dff5eeffe9f5e8bcafaea69e94f6dc9d79a7cc116dde71a7a5e86cde69a717f091dd61a70f84c8dd19a09c0c1eda11a09c0c1eda09a0a85febd801a051cc58d839a05180985f31a0a86f0d5e29a0fb4a19d821a0fb4059d826a39391f4ed71de89feb7375e81b200c1a35ea39691b35c71de817c5e25a256a39691803970de81347c88a24ea39991ccb573de46a39691b4a572de81816181a27ea393915c1e73de8904de985f81849a08a376a39691d48f72de819c07daa26ea39391dcc471de898cfb1e5d81d07068a266a39391fdb471de894763fd5f8124a998dc1edc9391b62371de89bba0485d81daf8f7a316dc9391467877de89dec18f5e81bd46b5a30edc93911f1671de89ac10da5e81aa16b2a306dc9991933f71de3edc99911cc071de36dc9691fee570de818c95faa22edc9691c0bf71de8144d0dba226dc9391cb1f71de895936315f81f1fed1dc5edc9691ef1a72de8106d182a256dc96911c6c71de8137e351a14edc9391aa8073de893bcb665f81910a15dc46dc9691144373de81568ebda27edc93919f1773de8921091e5e8124fa1aa376dc9691469972de81ac0696a2dec3",
        # master heartbeat: grid connection status / grid energized
        "aa048b00e9011301c9a0badedbb2a9d9b0b0b0b0b0b0b0d8d9c9e9a8ebebc616fd71e3e9c9e960ca00ef78cae870cae808cde800cde818cde810cde830cee972cfece2ea0ce742cfe82ac5e838c5e868c7e978c7eb65d8e8e8e8e808d82853e905d8e8e8e8e812d8e828d9e820d91ceb58dada2aa4e2e0eaf0edc8eac0ead8e922a4e2e0eaf0eec8eac0ead8e958b3e848b5e82b31",
        # sub-device heartbeat
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


async def test_shp3_auth_uses_v3_packet_version(device):
    assert device.packet_version == 0x03


async def test_shp3_parses_all_packets_successfully(device, packet_sequence):
    expected_cmd_ids = [0x52, 0x30, 0x30, 0x30, 0x30]
    expected_cmd_sets = [0x01, 0x40, 0x40, 0x40, 0x40]

    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert not Packet.is_invalid(packet), f"Packet {i} parsed as InvalidPacket"
        assert packet.cmd_set == expected_cmd_sets[i], (
            f"Packet {i} has unexpected cmdSet: 0x{packet.cmd_set:02x}"
        )
        assert packet.cmd_id == expected_cmd_ids[i], (
            f"Packet {i} has unexpected cmdId: 0x{packet.cmd_id:02x}"
        )


async def test_shp3_processes_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        processed = await device.data_parse(packet)
        assert processed is True, f"Packet {i} was not processed"


async def test_shp3_updates_master_state_from_v4_heartbeat(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[1]))
    await device.data_parse(packet)

    assert Device.battery_level.public_name in device.updated_fields
    battery_level = device.get_value(Device.battery_level)
    assert battery_level is not None
    assert 0 <= battery_level <= 100, f"Battery level {battery_level} out of range"


async def test_shp3_recognizes_sub_device_heartbeat(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[4]))
    processed = await device.data_parse(packet)
    assert processed is True
    assert packet.src == 0x30


async def test_shp3_v4_payload_is_fully_deobfuscated(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[1]))
    assert packet.payload[:9] == "XXXXXXX01".encode("ascii")


async def test_shp3_exact_values_from_known_packets(device, packet_sequence):
    """Test that known packet data produces exact expected values"""
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    expected = {
        Device.battery_level: 100.0,
        Device.backup_reserve_level: 50,
        Device.battery_charge_limit_max: 100,
        Device.battery_charge_limit_min: 0,
        Device.remaining_time_charging: 0,
        Device.load_system: 2534.36,
        Device.pv_power_sum: 0.0,
        Device.grid_connection_status: GridStatus.GRID_IN,
        Device.grid_is_energized: True,
        Device.l1_voltage: 120.8,
        Device.l2_voltage: 120.2,
        Device.l1_current: 8.84,
        Device.l2_current: 13.26,
        Device.circuit_power[1]: -85.58,
        Device.circuit_voltage[1]: 118.7,
        Device.circuit_current[1]: 0.87,
        Device.circuit_power[28]: -934.39,
    }

    for field, expected_value in expected.items():
        actual_value = device.get_value(field)
        assert actual_value == expected_value, (
            f"{field.public_name}: expected {expected_value}, got {actual_value}"
        )


def test_shp3_field_groups_are_expanded_and_renamed():
    expected_names = {
        *(f"circuit_power_{i}" for i in range(1, Device.NUM_OF_CIRCUITS + 1)),
        *(f"circuit_current_{i}" for i in range(1, Device.NUM_OF_CIRCUITS + 1)),
        *(f"circuit_voltage_{i}" for i in range(1, Device.NUM_OF_CIRCUITS + 1)),
    }

    actual_names: set[str] = set()
    for attr_name in dir(Device):
        attr = getattr(Device, attr_name, None)
        if isinstance(attr, FieldGroup):
            for field in attr:
                actual_names.add(field.public_name)

    assert actual_names == expected_names


async def test_shp3_set_backup_reserve_level_sends_config_write(device):
    await device.set_backup_reserve_level(40)

    device._conn.sendPacket.assert_awaited_once()
    packet = device._conn.sendPacket.await_args.args[0]
    assert (
        packet.src,
        packet.dst,
        packet.cmd_set,
        packet.cmd_id,
        packet.dsrc,
        packet.ddst,
        packet.version,
    ) == (0x21, 0x60, 0xFE, 0x11, 0x01, 0x01, 0x13)

    config = dev_apl_comm_pb2.ConfigWrite()
    config.ParseFromString(packet.payload)
    assert config.cfg_backup_reverse_soc == 40


async def test_shp3_charge_limit_controls_send_expected_fields(device):
    await device.set_battery_charge_limit_max(95)
    await device.set_battery_charge_limit_min(15)

    payloads = [
        call.args[0].payload for call in device._conn.sendPacket.await_args_list
    ]
    max_cfg = dev_apl_comm_pb2.ConfigWrite()
    max_cfg.ParseFromString(payloads[0])
    min_cfg = dev_apl_comm_pb2.ConfigWrite()
    min_cfg.ParseFromString(payloads[1])

    assert max_cfg.cfg_max_chg_soc == 95
    assert min_cfg.cfg_min_dsg_soc == 15


async def test_shp3_handles_v3_time_ping_without_crash(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[0]))
    processed = await device.data_parse(packet)
    assert processed is True
    assert packet.src == 0x35
    assert packet.cmd_set == 0x01
    assert packet.cmd_id == Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME
