import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.dpu_x import Device


@pytest.fixture
def packet_sequence():
    """
    Raw packet sequence captured from a Delta Pro Ultra X device

    - Packet 0: AC plug info + WiFi RSSI
    - Packet 1: battery SOC, sleep state, BMS info
    - Packet 2: power totals, PV power, operating mode
    - Packet 3: AC flow / charging state and charging power limits
    """
    return [
        "aa135e00a60d00000000000002210101fe15800700880700900700a00700a80700b00700ba0700c507d8e87543cd07396c8841d0073c981700d52500007442ea3c160a147489373ee7369f3d000000000000000000000000e84c00c85000e85a00806900c569dbb7f242cd697893f14228b0",
        "aa130801d30d00000000000002210101fe150800b00616b80800e00800a00d00a80d00b80d00b51000001041bd1000000000e010ffe408e8108b02f01064f81000d01102f811a8cd038012008812d626a81b00b01b00b81b00901c00d81ce05de01ce05df01c8090019a2700a22700a02f00a82f0092316d0a121001180220092da69bc4403500e0bf45401a0a121002180220092da69bc4403500e0bf4540180a053500e0bf450a053500e0bf450a053500e0bf450a121006180220082da69bc4403500e0bf4540160a053500e0bf450a053500e0bf450a053500e0bf450a053500e0bf45f83c9e868008823d260a110890ff9bd70610e0f9ffffffffffffff010a1108a0cad9dc0610c4faffffffffffffff01883d00e04b00dd5b",
        "aa13ae00b20d00000000000002210101fe151d86298345250000000028003000380040058801009001ac02980100e80200f00200b50400000000f50586298345f2070d100118012801307f389385cc41900900980901980c01980d3c801100881100e81103f01104c01600cd1600000000ca18021001d01800d81801e01800e81800f01800f01900c01c00e81c05981d00a01d00a81d00d02128d82100e0210ae82100c831901ce23c160a140000000000000000000000000000000000000000f584",
        "aa137200f40d00000000000002210101fe15f80202e80301f00300bd04bd7b943d800500d806e820e00600e806e05df00601f80600e00700ca08040a000a00c00900c80900d00c01880d00f00e00a01600d01600d81600e01600f81602e517345d293eed174cbb003ba81a00b01a00b81a00c01a00f01a00d51b62723b3e804f00884f00b044",
    ]


@pytest.fixture
def device(mocker: MockerFixture):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    adv_data = mocker.MagicMock()
    device = Device(ble_dev, adv_data, "P101TEST1234")
    device._conn = mocker.AsyncMock()
    return device


async def test_dpu_x_parses_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))

        assert packet is not None, f"Packet {i} failed to parse"
        assert packet.src == 0x02, f"Packet {i} has unexpected src: {packet.src:#04x}"
        assert packet.cmd_set == 0xFE, (
            f"Packet {i} has unexpected cmd_set: {packet.cmd_set:#04x}"
        )
        assert packet.cmd_id == 0x15, (
            f"Packet {i} has unexpected cmd_id: {packet.cmd_id:#04x}"
        )


async def test_dpu_x_processes_all_packets_successfully(device, packet_sequence):
    for i, hex_packet in enumerate(packet_sequence):
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        processed = await device.data_parse(packet)
        assert processed is True, f"Packet {i} was not processed"


async def test_dpu_x_updates_battery_level(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    battery_level = device.get_value(Device.battery_level)
    assert battery_level is not None
    assert isinstance(battery_level, (int, float))
    assert 0 <= battery_level <= 100, f"Battery level {battery_level} out of range"


async def test_dpu_x_updates_power_fields(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    power_field_names = [
        Device.input_power,
        Device.output_power,
        Device.ac_input_power,
        Device.pv_power_1,
        Device.pv_power_2,
    ]

    for field_name in power_field_names:
        value = device.get_value(field_name)
        assert isinstance(value, (int, float)), (
            f"Power field {field_name} has wrong type: {type(value)}"
        )


async def test_dpu_x_field_types_are_consistent(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    numeric_fields = [
        Device.battery_level,
        Device.cell_temperature,
        Device.input_power,
        Device.output_power,
        Device.ac_input_power,
        Device.ac_input_voltage,
        Device.ac_input_current,
        Device.ac_charging_speed,
        Device.pv_power_1,
        Device.pv_power_2,
        Device.wifi_rssi,
    ]

    for field_name in numeric_fields:
        value = device.get_value(field_name)
        if value is not None:
            assert isinstance(value, (int, float)), (
                f"Field {field_name} has wrong type: {type(value)}"
            )

    boolean_fields = [
        Device.plugged_in_ac,
        Device.ac_ports,
    ]

    for field_name in boolean_fields:
        value = device.get_value(field_name)
        assert isinstance(value, (bool, int)), (
            f"Field {field_name} has wrong type: {type(value)}"
        )
        if isinstance(value, int):
            assert value in (0, 1), f"Boolean field {field_name} has invalid int value"


async def test_dpu_x_battery_soc_values_are_valid(device, packet_sequence):
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    battery_level = device.battery_level
    assert battery_level is not None
    assert 0 <= battery_level <= 100, (
        f"Battery level {battery_level} is out of valid range (0-100%)"
    )


async def test_dpu_x_exact_values_from_known_packets(device, packet_sequence):
    """Test that known packet data produces exact expected values"""
    for hex_packet in packet_sequence:
        packet = await device.packet_parse(bytes.fromhex(hex_packet))
        await device.data_parse(packet)

    expected = {
        Device.battery_level: 9.0,
        Device.cell_temperature: 22,
        Device.input_power: 4197.19,
        Device.output_power: 0.0,
        Device.ac_input_power: 4197.19,
        Device.ac_input_voltage: 245.91,
        Device.ac_input_current: 17.05,
        Device.ac_charging_speed: 4200,
        Device.pv_power_1: 0.0,
        Device.pv_power_2: 0.0,
        Device.plugged_in_ac: True,
        Device.ac_ports: True,
        Device.wifi_rssi: 61.0,
    }

    for field_name, expected_value in expected.items():
        actual_value = device.get_value(field_name)
        assert actual_value == expected_value, (
            f"{field_name}: expected {expected_value}, got {actual_value}"
        )
