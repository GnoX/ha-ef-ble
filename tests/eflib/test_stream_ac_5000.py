import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.stream_ac_5000 import Device
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import es22_sys_pb2

# Telemetry payloads captured from a STREAM AC 5000, with the serial number masked. The
# device reports only the properties that changed, so battery and power readings arrive
# in separate messages. One capture discharges into a 300 W load and one charges with a
# 200 W input limit, which is what pins down the sign of the battery power.
DISCHARGE_BATTERY_AND_AC = (
    "5a0b08d80420d704281430d804620320ac02720628d70438d804e2020710b50528ca950492"
    "032a0a280a1045533232585858585858585858343437150000a04125822896c328023520b7"
    "9b433d82289643"
)
DISCHARGE_SOC_AND_TEMPERATURES = (
    "720628d70438d804b2023a0a380813106418bd0528a02730f9950438c40140b32e48c91950"
    "ca1958236027682470247a01008a011045533232585858585858585858343437b2031b0a19"
    "0a10455332325858585858585858583434371014180020d704"
)
CHARGE_BATTERY_AND_AC = (
    "5a0e08900310a406209403280d309303620630c80138ca0192032a0a280a10455332325858"
    "585858585858583434371500005041257fc04943280235d82941c33d7fc049c3b2031b0a19"
    "0a1045533232585858585858585858343437100d1800209203"
)


# A serial-routed V4 frame from the same capture, serial masked. These arrive mixed
# in with the V3 telemetry and were previously discarded as checksum failures.
ROUTED_V4_FRAME = (
    "aa04a001d7010001214553323258585858585858585834343721014003032efe27de020121"
    "015a0e08900310e41220d40f280230d30f620630c80138ea077214080010001800200028d4"
    "0f300238d30f40004801a201020800ba01060887a8e5d306da0104100118018a023c0d0000"
    "1d4515000000001d72f97f3f25a4707d3f2d00809c453509eb1b403d0000c8424500000000"
    "4d0000484455000048445d00401c456500b01a459202009a02020800b2023a0a3808021064"
    "189e0e28902730d0830138b32e40f00248f61850fc1858256028682a702a7a01008a011045"
    "533232585858585858585858343437c202310a2f0802100118012001280130003a04e882e0"
    "21421b08011a170a1045533232585858585858585858343437103218e807d80202e2021408"
    "0210a20e180020902728c7830130b32e38f002f00200f8020082030a08001000180020002a"
    "0092032a0a280a10455332325858585858585858583434371500000040256bb27a44280235"
    "4d6e79c43d6bb27ac4b2031b0a190a10455332325858585858585858583434371002180020"
    "d40fca030c0a0a00000000000000000000bbbb"
)


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


async def test_stream_ac_5000_parses_battery_level_and_temperature(device):
    processed = await device.data_parse(_telemetry(DISCHARGE_SOC_AND_TEMPERATURES))

    assert processed is True
    assert device.battery_level == 20
    # the pack reports four temperatures; the hottest one is what gets exposed
    assert device.cell_temperature == 39


async def test_stream_ac_5000_reports_battery_power_negative_while_discharging(device):
    processed = await device.data_parse(_telemetry(DISCHARGE_BATTERY_AND_AC))

    assert processed is True
    assert device.battery_power == pytest.approx(-311.43)
    assert device.battery_ac_input_power == 0.0
    assert device.battery_ac_output_power == pytest.approx(300.32)
    assert device.backup_port_power == 300


async def test_stream_ac_5000_reports_battery_power_positive_while_charging(device):
    processed = await device.data_parse(_telemetry(CHARGE_BATTERY_AND_AC))

    assert processed is True
    assert device.battery_power == pytest.approx(193.16)
    assert device.battery_ac_input_power == pytest.approx(201.75)
    assert device.battery_ac_output_power == 0.0
    assert device.battery_level == 13


async def test_stream_ac_5000_prefers_the_power_block_for_backup_port_power(device):
    message = es22_sys_pb2.DisplayPropertyUpload()
    message.power.info.ac_out_pwr = 431.47
    message.ac.ac_out_pwr = 1212

    device.update_from_message(message)

    assert device.backup_port_power == pytest.approx(431.47)


async def test_stream_ac_5000_falls_back_to_the_ac_block_for_backup_port_power(device):
    """Firmware that omits `PowerInfo.ac_out_pwr` still reports the coarser figure"""
    message = es22_sys_pb2.DisplayPropertyUpload()
    message.ac.ac_out_pwr = 300

    device.update_from_message(message)

    assert device.backup_port_power == 300


async def test_stream_ac_5000_ignores_packets_from_other_modules(device):
    processed = await device.data_parse(
        Packet(0x35, 0x21, 0xFE, 0x27, b"", 0x01, 0x01, 0x03)
    )

    assert processed is False


async def test_stream_ac_5000_parses_serial_routed_v4_frames(device):
    packet = await device.packet_parse(bytes.fromhex(ROUTED_V4_FRAME))

    assert not Packet.is_invalid(packet)
    assert (packet.src, packet.cmd_set, packet.cmd_id) == (0x02, 0xFE, 0x27)
    assert packet.serial.startswith("ES22")

    assert await device.data_parse(packet) is True
