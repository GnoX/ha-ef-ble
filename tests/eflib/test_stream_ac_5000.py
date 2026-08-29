import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.stream_ac_5000 import Device
from custom_components.ef_ble.eflib.packet import Packet, PacketV4
from custom_components.ef_ble.eflib.pb import es22_bkw_pb2
from custom_components.ef_ble.eflib.serial_routing import SerialRouting


@pytest.fixture
def payload_sequence():
    """Telemetry payloads captured from a STREAM AC 5000, with the serial masked"""
    return [
        # discharging into a 300 W load: battery, converter and backup port power
        "5a0b08d80420d704281430d804620320ac02720628d70438d804e2020710b50528ca950492032a0a280a1045533232585858585858585858343437150000a04125822896c328023520b79b433d82289643",
        # battery SoC, cell temperatures and the charge limits
        "720628d70438d804b2023a0a380813106418bd0528a02730f9950438c40140b32e48c91950ca1958236027682470247a01008a011045533232585858585858585858343437b2031b0a190a10455332325858585858585858583434371014180020d704",
        # charging with a 200 W input limit, which pins down the sign of battery power
        "5a0e08900310a406209403280d309303620630c80138ca0192032a0a280a10455332325858585858585858583434371500005041257fc04943280235d82941c33d7fc049c3b2031b0a190a1045533232585858585858585858343437100d1800209203",
        # the configuration blocks, which ride along with the telemetry; the unit's
        # group and LAN identifiers are blanked
        "2a020807521008c41310c4131801200428a00630c4137a00820100920104080012009a01020801ba010710900328003000c80102d201100a0c0800080008000800080008001200da010408002001ea010408641000f2010408001028fa010408c0ee6d820206080010001800ea020228008203020800c203020800",
    ]


@pytest.fixture
def routed_frame():
    """A serial-routed V4 frame from the same capture, serial masked"""
    # unobfuscated, and closing with a sentinel where a session frame keeps its CRC16
    return "aa04a001d7010001214553323258585858585858585834343721014003032efe27de020121015a0e08900310e41220d40f280230d30f620630c80138ea077214080010001800200028d40f300238d30f40004801a201020800ba01060887a8e5d306da0104100118018a023c0d00001d4515000000001d72f97f3f25a4707d3f2d00809c453509eb1b403d0000c84245000000004d0000484455000048445d00401c456500b01a459202009a02020800b2023a0a3808021064189e0e28902730d0830138b32e40f00248f61850fc1858256028682a702a7a01008a011045533232585858585858585858343437c202310a2f0802100118012001280130003a04e882e021421b08011a170a1045533232585858585858585858343437103218e807d80202e20214080210a20e180020902728c7830130b32e38f002f00200f8020082030a08001000180020002a0092032a0a280a10455332325858585858585858583434371500000040256bb27a442802354d6e79c43d6bb27ac4b2031b0a190a10455332325858585858585858583434371002180020d40fca030c0a0a00000000000000000000bbbb"


@pytest.fixture
def device(mocker: MockerFixture):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    adv_data = mocker.MagicMock()
    device = Device(ble_dev, adv_data, "ES22XXXXXXXXX447")
    device._conn = mocker.AsyncMock()
    return device


def _telemetry(payload_hex: str) -> Packet:
    return Packet(0x02, 0x21, 0xFE, 0x27, bytes.fromhex(payload_hex), 0x01, 0x01, 0x03)


async def test_stream_ac_5000_processes_all_payloads_successfully(
    device, payload_sequence
):
    for i, payload_hex in enumerate(payload_sequence):
        processed = await device.data_parse(_telemetry(payload_hex))
        assert processed is True, f"Payload {i} was not processed"


async def test_stream_ac_5000_parses_battery_level_and_temperature(
    device, payload_sequence
):
    processed = await device.data_parse(_telemetry(payload_sequence[1]))

    assert processed is True
    assert device.battery_level == 20
    # the pack reports four temperatures; the hottest one is what gets exposed
    assert device.cell_temperature == 39


async def test_stream_ac_5000_reports_battery_power_negative_while_discharging(
    device, payload_sequence
):
    processed = await device.data_parse(_telemetry(payload_sequence[0]))

    assert processed is True
    assert device.battery_power == pytest.approx(-311.43)
    assert device.battery_ac_input_power == 0.0
    assert device.battery_ac_output_power == pytest.approx(300.32)
    assert device.load_from_battery == 300
    assert device.backup_port_power is None


async def test_stream_ac_5000_reports_battery_power_positive_while_charging(
    device, payload_sequence
):
    processed = await device.data_parse(_telemetry(payload_sequence[2]))

    assert processed is True
    assert device.battery_power == pytest.approx(193.16)
    assert device.battery_ac_input_power == pytest.approx(201.75)
    assert device.battery_ac_output_power == 0.0
    assert device.battery_level == 13


async def test_stream_ac_5000_prefers_the_power_block_for_backup_port_power(device):
    # no capture carries `backup_pwr`, so only a built message reaches this branch
    message = es22_bkw_pb2.DisplayPropertyUpload()
    message.system_sub_dev_energy_flow_detail.dev_energy_flow_detail.add(
        backup_pwr=431.47
    )
    message.energy_flow_from_to_detail.bp_to_load = 1212

    device.update_from_message(message)

    assert device.backup_port_power == pytest.approx(431.47)


async def test_stream_ac_5000_ignores_packets_from_other_modules(device):
    processed = await device.data_parse(
        Packet(0x35, 0x21, 0xFE, 0x27, b"", 0x01, 0x01, 0x03)
    )

    assert processed is False


async def test_stream_ac_5000_parses_serial_routed_v4_frames(device, routed_frame):
    packet = await device.packet_parse(bytes.fromhex(routed_frame))

    assert isinstance(packet, PacketV4)
    assert packet.sentinel
    assert not packet.obfuscated

    envelope = SerialRouting.envelope(packet.payload)
    assert envelope is not None
    assert (envelope.src, envelope.cmd_set, envelope.cmd_id) == (0x02, 0xFE, 0x27)

    assert await device.data_parse(packet) is True


async def test_stream_ac_5000_reads_its_configuration_blocks(device, payload_sequence):
    packet = _telemetry(payload_sequence[3])

    assert await device.data_parse(packet) is True

    assert device.battery_charge_limit_max == 100
    assert device.battery_charge_limit_min == 0
    assert device.energy_backup is False
    assert device.energy_backup_battery_level == 40
    assert device.ac_ports is True


async def test_stream_ac_5000_routed_frame_round_trips(routed_frame):
    original = bytes.fromhex(routed_frame)

    packet = Packet.from_bytes(original)

    assert isinstance(packet, PacketV4)
    assert packet.to_bytes() == original


async def test_stream_ac_5000_zeroes_battery_power_when_the_entry_omits_it(device):
    # every captured entry reports `inv_pwr`, so the omission has to be built
    reported = es22_bkw_pb2.DisplayPropertyUpload()
    reported.system_sub_dev_energy_flow_detail.dev_energy_flow_detail.add(
        inv_pwr=-311.43
    )
    device.update_from_message(reported)

    omitted = es22_bkw_pb2.DisplayPropertyUpload()
    omitted.system_sub_dev_energy_flow_detail.dev_energy_flow_detail.add(
        on_grid_pwr=10.0
    )
    device.update_from_message(omitted)

    assert device.battery_power == 0.0
    assert device.grid_power == 10.0


async def test_stream_ac_5000_exact_values_from_known_packets(
    device, payload_sequence, routed_frame
):
    for payload_hex in payload_sequence:
        await device.data_parse(_telemetry(payload_hex))
    await device.data_parse(await device.packet_parse(bytes.fromhex(routed_frame)))

    expected = {
        Device.battery_level: 2,
        Device.battery_level_main: 2,
        Device.battery_power: 997.72,
        Device.battery_ac_input_power: 1002.79,
        Device.battery_ac_output_power: 0.0,
        Device.grid_power: -1002.79,
        Device.backup_port_power: None,
        Device.load_system: 200,
        Device.load_from_battery: 300,
        Device.load_from_grid: 200,
        Device.cell_temperature: 40,
        Device.remaining_time_charging: 368,
        Device.remaining_time_discharging: 5939,
        Device.battery_charge_limit_max: 100,
        Device.battery_charge_limit_min: 0,
        Device.energy_backup: False,
        Device.energy_backup_battery_level: 40,
        Device.ac_ports: True,
    }

    for field, expected_value in expected.items():
        actual_value = device.get_value(field)
        assert actual_value == expected_value, (
            f"{field.public_name}: expected {expected_value}, got {actual_value}"
        )
