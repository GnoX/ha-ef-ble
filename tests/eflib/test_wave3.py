import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.wave3 import (
    Device,
    FanSpeed,
    OperatingMode,
    SleepState,
)


@pytest.fixture
def packet_sequence():
    return [
        "aa130d01920d13e10300000042210101fe153b0d9b122f831213be1013131313fb1012e11413bb1b77a11b10464750ab1b12e61a131313138b1f13b31e12861c13131313d31c13e31c13eb1c138303138b0313a60313131313e30313eb03138b0213db0213de0513131313c30513cb0513c30913cb0913f30913990813b60d622eaf52be0d2e195551a30d11e60dbd541551d60c13131313db0c13c30c12cb0c11f30c13fb0c13e60c131333519333129b331381332f1913191a1b1003070e1313c352191a1b12033b0e1313db5219171b120307191a1b12037736131333511902033b0ededfa7523ededfd75226dedfb75289341b1915131313131313de2313131313c32313cb23139115111b11fb3113c15d1803ecececec1c0bff9a831e",
        "aa130d01920ddfe30300000042210101fe15f7c157dee34fdedf72dc1f60c7e237dcde2dd8df77d7bb6dd7dc8a8b9c67d7de2ad6dfdfdfdf47d3df7fd2de4ad0dfdfdfdf1fd0df2fd0df27d0df4fcfdf47cfdf6acfdfdfdfdf2fcfdf27cfdf47cedf17cedf12c9dfdfdfdf0fc9df07c9df0fc5df07c5df3fc5df55c4df7ac1cb71629e72c1973e889d6fc1dd2ac1b9b9dc9d1ac0dfdfdfdf17c0df0fc0de07c0dd3fc0df37c0df2ac0dfdfff9d5fffde57ffdf4dffe3d5dfd5d6d7dccfcbc2dfdf0f9ed5d6d7decff7c2dfdf179ed5dbd7decfcbd5d6d7decfbbfadfdfff9dd5cecff7c212136b9ef212131b9eea12137b9e45f8d7d5d9dfdfdfdfdfdf12ef1f60c7e20fefdf07efdf5dd9ddd7dd37fddf0d91d4cf20202020d0c733564fd2",
    ]


@pytest.fixture
def device(mocker: MockerFixture):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    adv_data = mocker.MagicMock()
    device = Device(ble_dev, adv_data, "AC71TEST1234")
    device._conn = mocker.AsyncMock()
    return device


async def test_wave3_parses_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))

        assert packet is not None, f"Packet {i} failed to parse"
        assert packet.src == 0x42, f"Packet {i} has unexpected src: {packet.src:#04x}"
        assert packet.cmdSet == 0xFE, (
            f"Packet {i} has unexpected cmdSet: {packet.cmdSet:#04x}"
        )
        assert packet.cmdId == 0x15, (
            f"Packet {i} has unexpected cmdId: {packet.cmdId:#04x}"
        )


async def test_wave3_processes_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        processed = await device.data_parse(packet)
        assert processed is True, f"Packet {i} was not processed"


async def test_wave3_updates_battery_level(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[0]))
    await device.data_parse(packet)

    assert Device.battery_level.public_name in device.updated_fields
    battery_level = device.get_value(Device.battery_level)
    assert isinstance(battery_level, (int, float))
    assert 0 <= battery_level <= 100


async def test_wave3_updates_temperature_fields(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[0]))
    await device.data_parse(packet)

    temp_fields = [
        Device.ambient_temperature,
        Device.temp_indoor_supply_air,
    ]

    for field in temp_fields:
        value = device.get_value(field)
        assert value is not None, f"{field} should not be None"
        assert isinstance(value, float), f"{field} has wrong type: {type(value)}"


async def test_wave3_derives_power_from_sleep_state(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[0]))
    await device.data_parse(packet)

    assert device.sleep_state == SleepState.STANDBY
    assert device.power is False


async def test_wave3_extracts_mode_params(device, packet_sequence):
    packet = await device.packet_parse(bytes.fromhex(packet_sequence[0]))
    await device.data_parse(packet)

    assert device.operating_mode == OperatingMode.HEATING
    assert device.target_temperature_climate == 25.0
    assert device.fan_speed_climate == FanSpeed.from_value(40)


async def test_wave3_updates_on_second_packet(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    assert device.ambient_temperature == 23.71
    assert device.ambient_humidity == 53.97


async def test_wave3_field_types_are_consistent(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    numeric_fields = [
        Device.battery_level,
        Device.ambient_temperature,
        Device.ambient_humidity,
        Device.ac_input_power,
        Device.battery_power,
        Device.temp_indoor_supply_air,
        Device.cell_temperature,
    ]

    for field in numeric_fields:
        value = device.get_value(field)
        if value is not None:
            assert isinstance(value, (int, float)), (
                f"Field {field} has wrong type: {type(value)}"
            )

    enum_fields = {
        Device.operating_mode: OperatingMode,
        Device.sleep_state: SleepState,
    }

    for field, enum_type in enum_fields.items():
        value = device.get_value(field)
        if value is not None:
            assert isinstance(value, enum_type), (
                f"Field {field} has wrong type: {type(value)}"
            )


async def test_wave3_exact_values_from_known_packets(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    expected = {
        Device.battery_level: 0.0,
        Device.ambient_temperature: 23.71,
        Device.ambient_humidity: 53.97,
        Device.operating_mode: OperatingMode.HEATING,
        Device.ac_input_power: 0.0,
        Device.battery_power: 0.0,
        Device.temp_indoor_supply_air: 32.8,
        Device.sleep_state: SleepState.STANDBY,
        Device.en_pet_care: False,
        Device.target_temperature_climate: 25.0,
        Device.fan_speed_climate: FanSpeed.from_value(40),
    }

    for field, expected_value in expected.items():
        actual_value = device.get_value(field)
        assert actual_value == expected_value, (
            f"{field}: expected {expected_value}, got {actual_value}"
        )

    # These fields lack presence in these packets, so they remain None
    assert device.input_power is None
    assert device.output_power is None
    assert device.power is False
