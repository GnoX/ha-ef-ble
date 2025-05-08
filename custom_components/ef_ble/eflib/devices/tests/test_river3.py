import pytest
from google.protobuf import text_format
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices import river3
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import pr705_pb2
from custom_components.ef_ble.eflib.props import Field

pr705_msg1 = """
errcode: 0
pow_in_sum_w: 34
pow_out_sum_w: 34
energy_backup_en: true
energy_backup_start_soc: 74
pow_get_qcusb1: 0
pow_get_qcusb2: 0
pow_get_typec1: 0
pow_get_typec2: 0
dev_standby_time: 1440
screen_off_time: 10
ac_standby_time: 0
ac_always_on_flag: false
ac_always_on_mini_soc: 15
xboost_en: false
pow_get_12v: 0
pow_get_ac: 0
pow_get_ac_in: 34.3072739
dc_out_open: false
pow_get_dcp2: 0
output_power_off_memory: true
pv_chg_type: 2
pow_get_bms: -2
en_beep: true
ac_out_freq: 50
dev_sleep_state: 0
time_task_current {
}
llc_hv_lv_flag: 230
bms_batt_soc: 74
bms_batt_soh: 100
bms_design_cap: 12800
bms_dsg_rem_time: 3794
bms_chg_rem_time: 3781
bms_min_cell_temp: 29
bms_max_cell_temp: 30
bms_min_mos_temp: 25
bms_max_mos_temp: 25
cms_batt_soc: 74
cms_batt_soh: 100
cms_dsg_rem_time: 3794
cms_chg_rem_time: 3781
cms_max_chg_soc: 90
cms_min_dsg_soc: 10
cms_bms_run_state: 1
bms_chg_dsg_state: 0
cms_chg_dsg_state: 0
time_task_conflict_flag: 0
time_task_change_cnt: 0
ups_alram: false
led_mode: 0
low_power_alarm: 0
silence_chg_watt: 50
pow_get_pv: 0
pow_get_ac_out: -34.3072739
pow_get_dcp: 0
display_statistics_sum {
  list_info {
    statistics_object: STATISTICS_OBJECT_AC_OUT_ENERGY
    statistics_content: 15341
  }
  list_info {
    statistics_object: STATISTICS_OBJECT_DC12V_OUT_ENERGY
  }
  list_info {
    statistics_object: STATISTICS_OBJECT_TYPEC_OUT_ENERGY
    statistics_content: 60
  }
  list_info {
    statistics_object: STATISTICS_OBJECT_USBA_OUT_ENERGY
    statistics_content: 20
  }
  list_info {
    statistics_object: STATISTICS_OBJECT_AC_IN_ENERGY
    statistics_content: 13
  }
  list_info {
    statistics_object: STATISTICS_OBJECT_PV_IN_ENERGY
    statistics_content: 1885
  }
}
"""

pr705_msg2 = """
flow_info_qcusb1: 0
flow_info_qcusb2: 0
flow_info_typec1: 0
flow_info_typec2: 0
flow_info_12v: 0
flow_info_ac2dc: 0
flow_info_dc2ac: 0
flow_info_ac_in: 2
plug_in_info_ac_in_flag: 0
plug_in_info_ac_in_feq: 0
flow_info_dcp2_in: 0
flow_info_dcp2_out: 0
flow_info_bms_dsg: 30
flow_info_bms_chg: 30
plug_in_info_ac_charger_flag: true
plug_in_info_ac_in_chg_pow_max: 50
plug_in_info_ac_out_dsg_pow_max: 300
plug_in_info_pv_dc_amp_max: 8
flow_info_pv: 0
plug_in_info_pv_flag: false
plug_in_info_pv_type: 2
plug_in_info_pv_charger_flag: false
plug_in_info_pv_chg_amp_max: 0
plug_in_info_pv_chg_vol_max: 0
flow_info_ac_out: 2
flow_info_dcp_in: 0
flow_info_dcp_out: 0
plug_in_info_dcp_in_flag: false
plug_in_info_dcp_type: 0
plug_in_info_dcp_detail: 0
plug_in_info_dcp_dsg_chg_type: 0
plug_in_info_dcp_sn: ""
plug_in_info_dcp_charger_flag: false
plug_in_info_ac_in_chg_hal_pow_max: 305
"""

pr705_msg3 = """
pcs_fan_level: 0
plug_in_info_dcp2_in_flag: false
plug_in_info_dcp2_dsg_chg_type: 0
plug_in_info_dcp2_charger_flag: false
plug_in_info_dcp2_type: 0
plug_in_info_dcp2_detail: 0
plug_in_info_dcp2_sn: ""
plug_in_info_dcp2_run_state: 0
plug_in_info_dcp2_firm_ver: 0
plug_in_info_dcp2_resv {
}
bms_err_code: 0
err_code_record_list {
  list_info {
    errcode: 606
  }
  list_info {
    errcode: 606
  }
  list_info {
    errcode: 606
  }
  list_info {
    errcode: 606
  }
  list_info {
    errcode: 606
  }
  list_info {
  }
  list_info {
  }
  list_info {
  }
  list_info {
  }
  list_info {
  }
}
pd_err_code: 0
mppt_err_code: 0
llc_inv_err_code: 0
plug_in_info_dcp_resv {
}
plug_in_info_dcp_firm_ver: 0
plug_in_info_dcp_run_state: 0
plug_in_info_dcp_err_code: 0
plug_in_info_dcp2_err_code: 0


"""


@pytest.fixture
def pr705_message_1():
    return text_format.Merge(pr705_msg1, pr705_pb2.DisplayPropertyUpload())


@pytest.fixture
def pr705_message_2():
    return text_format.Merge(pr705_msg2, pr705_pb2.DisplayPropertyUpload())


@pytest.fixture
def pr705_message_3():
    return text_format.Merge(pr705_msg3, pr705_pb2.DisplayPropertyUpload())


@pytest.fixture
def device(mocker: MockerFixture):
    device = river3.Device(mocker.AsyncMock(), mocker.Mock(), "[sn]")
    device._conn = mocker.AsyncMock()
    return device


async def test_river3_updates_from_message(
    device,
    pr705_message_1,
):
    to_process = Packet(
        src=0x02,
        dst=0x00,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=pr705_message_1.SerializeToString(),
    )

    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        river3.Device.battery_level,
        river3.Device.ac_input_power,
        river3.Device.ac_output_power,
        river3.Device.dc_input_power,
        river3.Device.dc12v_output_power,
        river3.Device.usbc_output_power,
        river3.Device.usba_output_power,
        river3.Device.energy_backup,
        river3.Device.energy_backup_battery_level,
        river3.Device.battery_input_power,
        river3.Device.battery_output_power,
        river3.Device.battery_charge_limit_min,
        river3.Device.battery_charge_limit_max,
        river3.Device.cell_temperature,
        river3.Device.dc_charging_type,
        river3.Device.ac_input_energy,
        river3.Device.ac_output_energy,
        river3.Device.dc_input_energy,
        river3.Device.dc12v_output_energy,
        river3.Device.usbc_output_energy,
        river3.Device.usba_output_energy,
        river3.Device.input_energy,
        river3.Device.output_energy,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None
