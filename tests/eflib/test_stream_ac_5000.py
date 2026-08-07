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
    assert device.ac_output_power == 300


async def test_stream_ac_5000_reports_battery_power_positive_while_charging(device):
    processed = await device.data_parse(_telemetry(CHARGE_BATTERY_AND_AC))

    assert processed is True
    assert device.battery_power == pytest.approx(193.16)
    assert device.ac_input_power == 202
    assert device.battery_level == 13


async def test_stream_ac_5000_ignores_packets_from_other_modules(device):
    processed = await device.data_parse(
        Packet(0x35, 0x21, 0xFE, 0x27, b"", 0x01, 0x01, 0x03)
    )

    assert processed is False


async def test_stream_ac_5000_requests_a_full_property_upload(device):
    await device._request_full_upload()

    device._conn.sendPacket.assert_awaited_once()
    packet = device._conn.sendPacket.await_args.args[0]
    assert (packet.src, packet.dst, packet.cmd_set, packet.cmd_id) == (
        0x21,
        0x02,
        0xFE,
        0x11,
    )

    config = es22_sys_pb2.ConfigWrite()
    config.ParseFromString(packet.payload)
    assert config.active_display_property_full_upload is True
    assert config.active_runtime_property_full_upload is True


async def test_stream_ac_5000_skips_the_upload_request_while_disconnected(device):
    device._conn = None

    await device._request_full_upload()
