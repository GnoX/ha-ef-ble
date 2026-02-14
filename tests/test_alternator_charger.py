import pytest
from google.protobuf import text_format
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices import alternator_charger
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import dc009_apl_comm_pb2

_dc009_apl_comm_msg = """
errcode: 32
cms_batt_temp: 29
pow_get_dc_bidi: 0
dev_online_flag: true
sp_charger_car_batt_vol_setting: 240
sp_charger_car_batt_vol: 0.00647016056
cms_batt_soc: 82
cms_dsg_rem_time: 3559
cms_chg_rem_time: 5939
pow_get_dcp: 0
plug_in_info_dcp_in_flag: true
plug_in_info_dcp_type: 79
plug_in_info_dcp_detail: 2
sp_charger_chg_mode: SP_CHARGER_CHG_MODE_DRIVING_CHG
sp_charger_chg_open: false
sp_charger_chg_pow_limit: 300
module_wifi_rssi: -35
sp_charger_chg_pow_max: 800
sp_charger_extension_line_p_setting: 0
sp_charger_extension_line_n_setting: 0
sp_charger_car_batt_chg_amp_limit: 70
sp_charger_dev_batt_chg_amp_limit: 60
sp_charger_dev_batt_chg_xt60_setting {
  car_batt_type: CAR_BATT_24V_TYPE
}
sp_charger_car_batt_chg_amp_max: 70
sp_charger_car_batt_urgent_chg_state: 0
sp_charger_dev_batt_chg_amp_max: 70
sp_charger_car_batt_urgent_chg_switch: false
"""


@pytest.fixture
def dc009_apl_comm_msg():
    return text_format.Merge(
        _dc009_apl_comm_msg, dc009_apl_comm_pb2.DisplayPropertyUpload()
    )


@pytest.fixture
def device(mocker: MockerFixture):
    mocker.patch("custom_components.ef_ble.eflib.devicebase.DeviceLogger")
    device = alternator_charger.Device(mocker.AsyncMock(), mocker.Mock(), "[sn]")
    device._conn = mocker.AsyncMock()
    return device


async def test_smart_generator_updates_from_message(device, dc009_apl_comm_msg):
    to_process = Packet(
        src=0x14,
        dst=0x21,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=dc009_apl_comm_msg.SerializeToString(),
    )

    await device.data_parse(to_process)

    expected_updated_fields: list[str] = [
        alternator_charger.Device.battery_level,
        alternator_charger.Device.battery_temperature,
        alternator_charger.Device.dc_power,
        alternator_charger.Device.car_battery_voltage,
        alternator_charger.Device.start_voltage,
        alternator_charger.Device.charger_mode,
        alternator_charger.Device.charger_open,
        alternator_charger.Device.power_limit,
        alternator_charger.Device.power_max,
    ]

    for field in expected_updated_fields:
        assert field in device.updated_fields
        assert getattr(device, field) is not None
