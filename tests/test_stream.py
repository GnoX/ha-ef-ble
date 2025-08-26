from typing import TYPE_CHECKING

import pytest
from google.protobuf import text_format
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices import (
    stream_ac,
    stream_ac_pro,
    stream_max,
    stream_pro,
    stream_ultra,
)
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import bk_series_pb2
from custom_components.ef_ble.eflib.props import Field

if TYPE_CHECKING:
    from custom_components.ef_ble.eflib.devices import ModuleWithDevice

_bk_msg_str = """
energy_backup_state: 0
pow_get_pv2: 5.89536715
plug_in_info_pv2_amp: 0.189511433
power_socket {
}
utc_timezone: 200
utc_timezone_id: "Europe/London"
utc_set_mode: true
bms_batt_soc: 51
bms_batt_soh: 100
bms_design_cap: 1920
bms_dsg_rem_time: 291
bms_chg_rem_time: 5939
bms_min_cell_temp: 33
bms_max_cell_temp: 34
bms_min_mos_temp: 36
bms_max_mos_temp: 36
cms_batt_soc: 51
cms_batt_soh: 100
cms_dsg_rem_time: 291
cms_chg_rem_time: 5939
cms_max_chg_soc: 90
cms_min_dsg_soc: 15
cms_bms_run_state: 1
bms_chg_dsg_state: 1
cms_chg_dsg_state: 1
pow_get_pv: 6.53502131
plug_in_info_pv_flag: true
plug_in_info_pv_vol: 31.1227493
plug_in_info_pv_amp: 0.209975705
energy_strategy_operate_mode {
  operate_self_powered_open: true
}
plug_in_info_pv2_flag: true
plug_in_info_pv2_vol: 31.1082401
cms_batt_pow_out_max: 1200
cms_batt_pow_in_max: 1030
backup_reverse_soc: 18
cms_batt_full_energy: 1920
pow_get_sys_grid: 0
pow_get_sys_load: 200
pow_get_pv_sum: 0
pow_get_bp_cms: -200
feed_grid_mode: 1
feed_grid_mode_pow_limit: 800
module_wifi_rssi: -38
grid_connection_vol: 239.02565
grid_connection_freq: 49.9994431
grid_connection_power: 199.262299
grid_connection_sta: PANEL_FEED_GRID
dev_errcode_list {
}
feed_grid_mode_pow_max: 800
town_code: 0
grid_code_selection: GRID_STD_CODE_EU_GENERAL
grid_code_version: 10001
grid_sys_device_cnt: 1
wifi_ap_mesh_id {
}
pow_consumption_measurement: 1
cloud_metter {
}
timezone_change_list {
  time_zone_change_item {
    utc_time: 1761440400
    utc_timezone: 100
  }
  time_zone_change_item {
    utc_time: 1774746000
    utc_timezone: 200
  }
}
update_ban_flag: 0
day_resident_load_list {
  load {
    end_min: 1440
    load_power: 200
  }
}
relay2_onoff: false
relay4_onoff: true
relay3_onoff: false
relay1_onoff: true
system_group_id: 142807041
pow_sys_ac_out_max: 800
plug_in_info_pv3_flag: true
plug_in_info_pv4_flag: false
pow_sys_ac_in_max: 2231
distributed_device_status: MASTER
series_connect_device_status: MASTER
sys_grid_connection_power: 199.262299
socket_measure_power: 0
brightness: 100
system_mesh_id: 1
pow_get_pv3: 9.31538105
pow_get_pv4: 0
plug_in_info_pv3_vol: 31.2470322
plug_in_info_pv3_amp: 0.298120499
plug_in_info_pv4_vol: 2.69650793
plug_in_info_pv4_amp: -0.0138375871
pow_get_sys_load_from_pv: 0
pow_get_sys_load_from_bp: 199.262299
pow_get_sys_load_from_grid: 0.737701416
pow_get_schuko1: 0
pow_get_schuko2: 0
bms_batt_heating: false
dev_ctrl_status: 1
busbar_pow_limit: 2300
max_inv_input: 1200
max_inv_output: 1200
max_bp_input: 1050
max_bp_output: 1200
series_connect_device_id: 1
use_lan_meter: false
grid_connection_port_bind {
}
scoket1_bind_device_sn: ""
scoket2_bind_device_sn: ""
sys_offgrid: false
"""


@pytest.fixture
def bk_message():
    return text_format.Merge(_bk_msg_str, bk_series_pb2.DisplayPropertyUpload())


@pytest.fixture
def device(mocker: MockerFixture):
    def _mocked_device(module: "ModuleWithDevice"):
        mocker.patch("custom_components.ef_ble.eflib.devicebase.DeviceLogger")
        device = module.Device(mocker.AsyncMock(), mocker.Mock(), "[sn]")
        device._conn = mocker.AsyncMock()
        return device

    return _mocked_device


async def test_stream_ac_updates_from_message(device, bk_message):
    to_process = Packet(
        src=0x02,
        dst=0x20,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=bk_message.SerializeToString(),
    )

    device = device(stream_ac)
    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        stream_ac.Device.battery_level,
        stream_ac.Device.cell_temperature,
        stream_ac.Device.battery_charge_limit_max,
        stream_ac.Device.battery_charge_limit_min,
        stream_ac.Device.grid_frequency,
        stream_ac.Device.grid_voltage,
        stream_ac.Device.grid_power,
        stream_ac.Device.load_from_battery,
        stream_ac.Device.load_from_grid,
        stream_ac.Device.energy_strategy,
        stream_ac.Device._resident_load,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None

    assert (
        getattr(device, stream_ac.Device.energy_strategy.public_name)
        == stream_ac.EnergyStrategy.SELF_POWERED
    )


async def test_stream_ac_pro_updates_from_message(device, bk_message):
    to_process = Packet(
        src=0x02,
        dst=0x20,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=bk_message.SerializeToString(),
    )

    device = device(stream_ac_pro)
    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        stream_ac_pro.Device.battery_level,
        stream_ac_pro.Device.cell_temperature,
        stream_ac_pro.Device.battery_charge_limit_max,
        stream_ac_pro.Device.battery_charge_limit_min,
        stream_ac_pro.Device.grid_frequency,
        stream_ac_pro.Device.grid_voltage,
        stream_ac_pro.Device.grid_power,
        stream_ac_pro.Device.load_from_battery,
        stream_ac_pro.Device.load_from_grid,
        stream_ac_pro.Device.ac_power_1,
        stream_ac_pro.Device.ac_power_2,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None


async def test_stream_max_updates_from_message(device, bk_message):
    to_process = Packet(
        src=0x02,
        dst=0x20,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=bk_message.SerializeToString(),
    )

    device = device(stream_max)
    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        stream_max.Device.battery_level,
        stream_max.Device.cell_temperature,
        stream_max.Device.battery_charge_limit_max,
        stream_max.Device.battery_charge_limit_min,
        stream_max.Device.grid_frequency,
        stream_max.Device.grid_voltage,
        stream_max.Device.grid_power,
        stream_max.Device.load_from_battery,
        stream_max.Device.load_from_grid,
        stream_max.Device.ac_power_1,
        stream_max.Device.pv_power_1,
        stream_max.Device.pv_power_2,
        stream_max.Device.load_from_pv,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None


async def test_stream_pro_updates_from_message(device, bk_message):
    to_process = Packet(
        src=0x02,
        dst=0x20,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=bk_message.SerializeToString(),
    )

    device = device(stream_pro)
    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        stream_pro.Device.battery_level,
        stream_pro.Device.cell_temperature,
        stream_pro.Device.battery_charge_limit_max,
        stream_pro.Device.battery_charge_limit_min,
        stream_pro.Device.grid_frequency,
        stream_pro.Device.grid_voltage,
        stream_pro.Device.grid_power,
        stream_pro.Device.load_from_battery,
        stream_pro.Device.load_from_grid,
        stream_pro.Device.ac_power_1,
        stream_pro.Device.ac_power_2,
        stream_pro.Device.pv_power_1,
        stream_pro.Device.pv_power_2,
        stream_pro.Device.pv_power_3,
        stream_pro.Device.load_from_pv,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None


async def test_stream_ultra_updates_from_message(device, bk_message):
    to_process = Packet(
        src=0x02,
        dst=0x20,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=bk_message.SerializeToString(),
    )

    device = device(stream_ultra)
    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        stream_ultra.Device.battery_level,
        stream_ultra.Device.cell_temperature,
        stream_ultra.Device.battery_charge_limit_max,
        stream_ultra.Device.battery_charge_limit_min,
        stream_ultra.Device.grid_frequency,
        stream_ultra.Device.grid_voltage,
        stream_ultra.Device.grid_power,
        stream_ultra.Device.load_from_battery,
        stream_ultra.Device.load_from_grid,
        stream_ultra.Device.ac_power_1,
        stream_ultra.Device.ac_power_2,
        stream_ultra.Device.pv_power_1,
        stream_ultra.Device.pv_power_2,
        stream_ultra.Device.pv_power_3,
        stream_ultra.Device.pv_power_4,
        stream_ultra.Device.load_from_pv,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None
