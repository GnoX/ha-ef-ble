import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.ocean_pro import Device, GridStatus
from custom_components.ef_ble.eflib.packet import Packet, PacketV4
from custom_components.ef_ble.eflib.pb import dev_apl_comm_pb2, jt_s1_sys_pb2


@pytest.fixture
def packet_sequence():
    return [
        # Runtime: grid frequency
        "aa04ab0047011301670e1473771c07771e1e1e1e1e1e1e7677674706454560b8507526476747db24923b6e83e3244606da03eb244606da03f62447fe24468324b87b43f98b249e28c4069624479e2446a62446ae2447b3248c433604bb2446468e05c62547ce2547d32546460e84db2546460686e3258b8a8a7beb2546464646f325b1e21684fb25df7d2d04832546c6fd008b25464646469325464694059e2544a62546ae2545b32546464646be2546c622465cb4",
        # Runtime: PV1 voltage/current
        "aa04bc007b0113015b32284f4b203b4b222222222222224a4b5b7b3a79795c846c421a7b5b7bc773a2018f38df76af3b2b3bd7763b268f38cf76b0bc363bd2689add68ca68da8470c268da8d4cba68da8470926f79f76c9786cbbeef6c68a0cabeea6d4fda5b7aba5b7bb25b7be7517ccc7339d751e3855244cf51106f573bc751da7f5f39b751912e7844af51cefa7a38a75144fe3639975123d51e448f519c2b3c3b875127845739f756185d3b44ef567a7a7a7ae756afa86939d756b81ceb44f21e7a6c88",
        # Display: battery, loads, PV sum, remaining times
        "aa048d0097011301b7dec4a3a7ccd7a7cececececececea6a7b797d69595b06883aff697b797369b9723869696b2d47686f57e86966686f24687977e87966687965c8e949e977e8e964e8a06d8768a1eb17e8a95668a1dc00e8b96368b963e8b960bb6f0b0bdd233b6cd30c2d33bb67d31cad423b6b4fcb05356b69756cca406ff0fb326ff9726fc962efc9616fd962efd9656fd96f663",
        # Display: plugged-in AC
        "aa04a600ae0113018ee7fd9a9ef5ee9ef7f7f7f7f7f7f79f9e8eaeefacac8951b695cfae8eaea2af2f14e9baafaf39e9b26263e3908aafaf39e9826263e3909aaf2f14e997acefad07a927881fa9ae12a9505054ed6aa92fbb73ed62a9c9c9dfed7aa9afafc1ed77a947a84fa94f08bd47a94f08bd5fa9af52a9afaf2f902fa8a922a8afaf5fed3aa8afafdfed37a8af0fa8af02a8afaf5fed1fa8af72a8afaf39ec4fa8ae47a8af5aa8afaf2f902bb9",
        # Runtime: grid L1/L2 voltage/current + PV8 voltage
        "aa04cf00e6011301c6afb5d2d6bda6d6bfbfbfbfbfbfbfd7d6c6e6a7e4e4c119f1a787e6c6e667cfe76acfe91888a572cfc1e697a57acf4c1d13a542cf7ff312a54acf3582d5a652cf9594d5a65acff18712a522cff18712a52acf2a40a0a632cf462da5a63acf99fd615b02cffd899b5b0acf1d714c5a12cf1d714c5a1acf4ba2a0a462ce88dca0a46aceb7776cd972cef82c34d87acec1840a5952cbe7e7e7e75acb8d53a4a52acbe7e7e7e732cbe7e7e7e73acbc687d9a50acbe7e7e7e712cbe7e7e7e71acb0786a7a56acae7e7e7e772cae7e7e7e7c371",
        # Display: grid connection status
        "aa045b0053011301731a0067630813630a0a0a0a0a0a0a6263735312515174ac4713325373539a725282722a8a7252b27252ba7252a27252a87252c87352fa7352aa7352d270b64bc27052ca7052f27052b27750ba7753a27753aa77528a7453c875521f7c",
        # Runtime: grid L1/L2 active power
        "aa04bd006e0113014e273d5a5e352e5e373737373737375f5e4e6e2f6c6c499179270f6e4e6eca462447a72cc246fb1054a9da466f6f6f6fd246fb1054a9aa466f6f6f6fa7466fbf466fb246dce2c52b8a46a158c8ab82467e2ac1d09a469360c42b92460365c8abea451c4b14afe2456f301caefa45c8791faef245feccc82fca454143cf2fc2456f6f6f6fda456f6f6f6fd2456f6f6f6faa456f6f6f6fa2456f6f6f6fba456f6f6f6fb2456f6f6f6f82456f6f6f6f9f456f97456fef446fe7446fb732665e10",
        # Display: AC output power
        "aa04c50064011301442d3750543f24543d3d3d3d3d3d3d55544464256666439b7c2e05644464d86765656565a067cb2284dba8676565c525b56765b867cb22845b80676565e5da8867656565659067656565da986765656565e066a8a929dbe86665656565f066a8a9295bf86665656565c0666565655ac866cb2284dbd0666565e55add6665a06665656565ad6665b06603039b27b8666565e55a806665656126886665656565906665654524986665656126e06165657526ed61ad00f561c564f8615656b627c06165651527fc99",
        # Display: grid energized + PV1 power
        "aa04920003011301234a5037335843335a5a5a5a5a5a5a3233230342010124fc175162032303822d03e232c2b903f73202020202f8320608001201f24f82f500ca5802bf59c21df740c759b8b34443cf592a59f740d759effc4043df5973e8a7c6e759fe35a4c6ea5937f25902fa5994bbfd05825e03a75e44393443af5eeedbfc43b75e37fb4543bf5e02020202c75e02020202cf5e0202020264af",
        # Display: PV8 power
        "aa0486000001130120495334305b4030595959595959593130200041020227ff145a61002000eb3f161b11495334335959595959595959595931302c01012543e14a01895d01915d00995d00d45d01010101dc5d01010101e95dfefefe06f15dfefefe06f95dfefefe06d15c01b16001c16015cc69fefe7e4ad469fefe7e4adc69fefe7e4a8b6801c96a01d16a0131e9",
    ]


@pytest.fixture
def device(mocker: MockerFixture):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    adv_data = mocker.MagicMock()
    device = Device(ble_dev, adv_data, "HR51XXXXXXXXX001")
    device._conn = mocker.AsyncMock()
    device._conn._user_id = "test-user-id"
    return device


def test_ocean_pro_recognizes_hr51_only():
    assert Device.check(b"HR51XXXXXXXXX001")
    assert not Device.check(b"HR61XXXXXXXXX001")


async def test_ocean_pro_auth_uses_v3_packet_version(device):
    assert device.packet_version == 0x03


async def test_ocean_pro_parses_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert not Packet.is_invalid(packet), f"Packet {i} parsed as InvalidPacket"


async def test_ocean_pro_processes_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        processed = await device.data_parse(packet)
        assert processed is True, f"Packet {i} was not processed"


async def test_ocean_pro_telemetry_is_v4_from_expected_address(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert isinstance(packet, PacketV4)
        assert (packet.src, packet.cmd_set, packet.cmd_id) == (0x30, 0x40, 0x30)


async def test_ocean_pro_v4_payload_is_fully_deobfuscated(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        assert packet.payload[:9] == b"XXXXXXX01"


async def test_ocean_pro_exact_values_from_known_packets(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    assert device.battery_level == 41.0
    assert device.battery_power == -2662.63
    assert device.load_system == 3402.4
    assert device.load_from_grid == 684.6
    assert device.pv_power_sum == 55.16
    assert device.remaining_time_charging == 0
    assert device.remaining_time_discharging == 99
    assert device.grid_connection_status is GridStatus.GRID_IN
    assert device.grid_is_energized is True
    assert device.plugged_in_ac is True
    assert device.ac_output_power == 0.44
    assert device.grid_frequency == 60.01
    assert device.l1_voltage == 122.5
    assert device.l2_voltage == 122.5
    assert device.l1_current == 11.15
    assert device.l2_current == 11.15
    assert device.l1_power == 1337.74
    assert device.l2_power == 1336.33
    assert device.pv_power_1 == 11.4
    assert device.pv_power_8 == 0.0
    assert device.pv_voltage_1 == 137.7
    assert device.pv_voltage_8 == 48.1
    assert device.pv_current_1 == 0.17


def test_ocean_pro_has_no_circuits():
    # Circuits belong to the separate OCEAN Panel, not the inverter.
    field_names = {f.public_name for f in Device._fields}
    assert not any(name.startswith("circuit_") for name in field_names)


async def test_ocean_pro_charge_limit_writes_go_to_e7_mcu(device):
    display = dev_apl_comm_pb2.DisplayPropertyUpload()
    display.cms_min_dsg_soc = 15
    display.cms_max_chg_soc = 95
    device.update_from_message(display)

    await device.set_battery_charge_limit_max(88)
    pkt = device._conn.sendPacket.await_args.args[0]
    assert (pkt.src, pkt.dst, pkt.cmd_set, pkt.cmd_id) == (0x21, 0x60, 0x60, 0x70)
    assert pkt.version == 0x13
    msg = jt_s1_sys_pb2.SysBatChgDsgSet.FromString(pkt.payload)
    assert msg.sys_bat_chg_up_limit == 88
    assert msg.sys_bat_dsg_down_limie == 15

    await device.set_battery_charge_limit_min(10)
    pkt = device._conn.sendPacket.await_args.args[0]
    msg = jt_s1_sys_pb2.SysBatChgDsgSet.FromString(pkt.payload)
    assert msg.sys_bat_chg_up_limit == 95
    assert msg.sys_bat_dsg_down_limie == 10


async def test_ocean_pro_keepalive_reasserts_energy_stream(device):
    await device._send_keepalive()
    pkt = device._conn.sendPacket.await_args.args[0]
    assert (pkt.src, pkt.dst, pkt.cmd_set, pkt.cmd_id) == (0x21, 0x60, 0x60, 0x61)
    assert pkt.payload == bytes([0x08, 0x01])


async def test_ocean_pro_sends_report_rate_ctrl(device):
    await device._send_report_rate_ctrl()
    pkt = device._conn.sendPacket.await_args.args[0]
    assert (pkt.src, pkt.dst, pkt.cmd_set, pkt.cmd_id) == (0x21, 0x60, 0x60, 0x74)
    assert pkt.payload == bytes([0x08, 0x01, 0x20, 0x03, 0x28, 0x01])
