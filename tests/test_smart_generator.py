import pytest
from google.protobuf import text_format
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices import smart_generator
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import ge305_sys_pb2
from custom_components.ef_ble.eflib.props import Field

_ge305_msg = """
sys_status: 1
pow_out_sum_w: 0
dev_standby_time: 3
screen_off_time: 180
xboost_en: false
pow_get_ac: 0
generator_conn_dev_errcode: 0
current_time_task_v2_item {
  task_index: 65535
}
generator_low_power_en: false
generator_low_power_threshold: 0
generator_lpg_monitor_en: true
fuels_liquefied_gas_lpg_uint: 0
fuels_liquefied_gas_lng_uint: 0
en_beep: false
ac_out_freq: 50
pd_err_code: 0
cms_batt_soc: 0
cms_dsg_rem_time: 0
cms_chg_rem_time: 0
cms_oil_self_start: true
time_task_change_cnt: 0
pow_get_dc: 0
ac_out_open: true
generator_fuels_type: 3
generator_remain_time: 53328
generator_run_time: 1293
generator_total_output: 0
generator_abnormal_state: 17
fuels_oil_val: 0
fuels_liquefied_gas_type: 0
fuels_liquefied_gas_uint: 0
fuels_liquefied_gas_val: 4.535
fuels_liquefied_gas_consume_per_hour: 0
fuels_liquefied_gas_remain_val: 0
generator_perf_mode: 0
generator_engine_open: 0
generator_out_pow_max: 0
generator_dc_out_pow_max: 3200
generator_sub_battery_temp: 2400
generator_sub_battery_soc: 46
generator_sub_battery_state: 0
generator_pcs_err_code: 0
plug_in_info_dcp_in_flag: false
plug_in_info_dcp_type: 0
plug_in_info_dcp_detail: 0
plug_in_info_dcp_dsg_chg_type: 0
plug_in_info_dcp_charger_flag: false
"""


@pytest.fixture
def ge305_msg():
    return text_format.Merge(_ge305_msg, ge305_sys_pb2.DisplayPropertyUpload())


@pytest.fixture
def device(mocker: MockerFixture):
    mocker.patch("custom_components.ef_ble.eflib.devicebase.DeviceLogger")
    device = smart_generator.Device(mocker.AsyncMock(), mocker.Mock(), "[sn]")
    device._conn = mocker.AsyncMock()
    return device


async def test_smart_generator_updates_from_message(device, ge305_msg):
    to_process = Packet(
        src=0x08,
        dst=0x21,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=ge305_msg.SerializeToString(),
    )

    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        smart_generator.Device.output_power,
        smart_generator.Device.ac_output_power,
        smart_generator.Device.dc_output_power,
        # smart_generator.Device.xt150_battery_level,
        # smart_generator.Device.xt150_charge_type,
        smart_generator.Device.self_start,
        smart_generator.Device.engine_state,
        smart_generator.Device.performance_mode,
        smart_generator.Device.liquefied_gas_type,
        smart_generator.Device.liquefied_gas_value,
        smart_generator.Device.liquefied_gas_consumption,
        smart_generator.Device.liquefied_gas_unit,
        smart_generator.Device.generator_total_output,
        smart_generator.Device.generator_abnormal_state,
        smart_generator.Device.sub_battery_soc,
        smart_generator.Device.sub_battery_state,
        smart_generator.Device.ac_ports,
        smart_generator.Device.fuel_type,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None
