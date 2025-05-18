import pytest
from google.protobuf import text_format
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices import dpu
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import yj751_sys_pb2
from custom_components.ef_ble.eflib.props import Field

_bp_info_message_str = """
bp_info {
  bp_no: 1
  bp_soc: 34
  bp_pwr: -0
  bp_energy: 6144
  remain_time: 8123
  bp_soc_max: 100
  bp_temp: 39
}
bp_info {
  bp_no: 2
  bp_soc: 45
  bp_pwr: -0
  bp_energy: 6144
  remain_time: 10986
  bp_soc_max: 100
  bp_temp: 37
}
bp_info {
  bp_no: 3
  bp_soc: 43
  bp_pwr: -0
  bp_energy: 6144
  remain_time: 10287
  bp_soc_max: 100
  bp_temp: 35
}
"""

_para_heartbeat_report_message_str = """
sys_word_mode: 0
sys_backup_event: 0
sys_backup_soc: 100
energy_mamage_enable: 0
backup_ratio: 30
ac_xboost: 0
ac_out_freq: 60
bms_mode_set: 1
chg_max_soc: 100
dsg_min_soc: 0
ac_often_open_flg: 0
ac_often_open_min_soc: 0
chg_5p8_set_watts: 1800
chg_c20_set_watts: 1800
power_standby_mins: 0
screen_standby_sec: 300
dc_standby_mins: 720
ac_standby_mins: 720
solar_only_flg: 0
timezone_settype: 1
sys_timezone: -400
sys_timezone_id: "America/New_York"
"""

_show_heartbeat_report_message_str = """
proto_ver: 50464776
show_flag: 2560
access_type: 8
wireless_4g_on: 0
wireless_4G_sta: 0
access_5p8_in_type: 0
access_5p8_out_type: 0
wireless_4g_con: -1
wirlesss_4g_err_code: 5
sim_iccid: ""
soc: 41
bp_num: 3
pcs_type: 1
c20_chg_max_watts: 1800
para_chg_max_watts: 7200
remain_time: 14939
sys_err_code: 0
full_combo: 100
remain_combo: 30
watts_in_sum: 0
watts_out_sum: 0
out_usb1_pwr: 0
out_usb2_pwr: 0
out_typec1_pwr: 0
out_typec2_pwr: 0
out_ads_pwr: 0
out_ac_l1_1_pwr: 0
out_ac_l1_2_pwr: 0
out_ac_l2_1_pwr: 0
out_ac_l2_2_pwr: 0
out_ac_tt_pwr: 0
out_ac_l14_pwr: 0
out_ac_5p8_pwr: 0
in_ac_5p8_pwr: 0
in_ac_c20_pwr: 0
in_lv_mppt_pwr: 0
in_hv_mppt_pwr: 0
out_pr_pwr: 0
time_task_change_cnt: 0
time_task_conflict_flag: 0
chg_time_task_notice: 0
chg_time_task_type: 4294967295
chg_time_task_index: 4294967295
chg_time_task_mode: 4294967295
chg_time_task_param: 0
chg_time_task_table_0: 0
chg_time_task_table_1: 0
chg_time_task_table_2: 0
dsg_time_task_notice: 0
dsg_time_task_type: 4294967295
dsg_time_task_index: 4294967295
dsg_time_task_mode: 4294967295
dsg_time_task_param: 0
dsg_time_task_table_0: 0
dsg_time_task_table_1: 0
dsg_time_task_table_2: 0
"""


@pytest.fixture
def show_heartbeat_report_message():
    return text_format.Merge(
        _show_heartbeat_report_message_str, yj751_sys_pb2.AppShowHeartbeatReport()
    )


@pytest.fixture
def device(mocker: MockerFixture):
    device = dpu.Device(mocker.AsyncMock(), mocker.Mock(), "[sn]")
    device._conn = mocker.AsyncMock()
    return device


async def test_dpu_updates_from_show_heartbeat_report_message(
    device, show_heartbeat_report_message
):
    to_process = Packet(
        src=0x02,
        dst=0x00,
        cmd_set=0x02,
        cmd_id=0x01,
        payload=show_heartbeat_report_message.SerializeToString(),
    )

    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        dpu.Device.battery_level,
        dpu.Device.hv_solar_power,
        dpu.Device.lv_solar_power,
        dpu.Device.input_power,
        dpu.Device.output_power,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None
