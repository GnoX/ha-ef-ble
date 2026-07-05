import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.ocean_pro import Device, GridStatus
from custom_components.ef_ble.eflib.pb import dev_apl_comm_pb2


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
    # HR51 is the OCEAN Pro inverter; HR61 is the separate OCEAN Panel.
    assert Device.check(b"HR51XXXXXXXXX001")
    assert not Device.check(b"HR61XXXXXXXXX001")


async def test_ocean_pro_auth_uses_v3_packet_version(device):
    assert device.packet_version == 0x03


async def test_ocean_pro_decodes_inverter_sensors(device):
    display = dev_apl_comm_pb2.DisplayPropertyUpload()
    display.cms_batt_soc = 96
    display.pow_get_bp_cms = -2759.34
    display.pow_get_sys_load = 2968.34
    display.pow_get_sys_grid = 0
    display.pow_get_pv_sum = 209
    display.cms_chg_rem_time = 0
    display.cms_dsg_rem_time = 450
    display.grid_connection_sta = 1
    display.grid_is_energized = True
    display.plug_in_info_acp_charger_flag = True
    device.update_from_message(display)

    runtime = dev_apl_comm_pb2.RuntimePropertyUpload()
    runtime.third_inv_offgrid_ctrl_freq_curr = 60.0
    device.update_from_message(runtime)

    assert device.battery_level == 96.0
    assert device.battery_power == -2759.34
    assert device.load_system == 2968.34
    assert device.load_from_grid == 0.0
    assert device.pv_power_sum == 209.0
    assert device.remaining_time_charging == 0
    assert device.remaining_time_discharging == 450
    assert device.grid_connection_status is GridStatus.GRID_IN
    assert device.grid_is_energized is True
    assert device.plugged_in_ac is True
    assert device.inverter_frequency == 60.0


def test_ocean_pro_has_no_circuits():
    # Circuits belong to the separate OCEAN Panel, not the inverter.
    field_names = {f.public_name for f in Device._fields}
    assert not any(name.startswith("circuit_") for name in field_names)
