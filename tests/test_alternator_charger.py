import pytest
from google.protobuf import text_format
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices import alternator_charger
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.pb import mr521_pb2
from custom_components.ef_ble.eflib.props import Field

_mr521_msg = """
errcode: 0
cms_batt_temp: 30
pow_get_dc_bidi: 0
dev_online_flag: true
sp_charger_car_batt_vol_setting: 250
sp_charger_car_batt_vol: 26.5222855
cms_batt_soc: 97
cms_dsg_rem_time: 3919
cms_chg_rem_time: 5939
pow_get_dcp: 0
plug_in_info_dcp_in_flag: true
plug_in_info_dcp_type: 79
plug_in_info_dcp_detail: 2
sp_charger_chg_mode: SP_CHARGER_CHG_MODE_PARKING_CHG
sp_charger_chg_open: false
sp_charger_chg_pow_limit: 497
module_wifi_rssi: -33
sp_charger_chg_pow_max: 800
"""


@pytest.fixture
def mr521_msg():
    return text_format.Merge(_mr521_msg, mr521_pb2.DisplayPropertyUpload())


@pytest.fixture
def device(mocker: MockerFixture):
    mocker.patch("custom_components.ef_ble.eflib.devicebase.DeviceLogger")
    device = alternator_charger.Device(mocker.AsyncMock(), mocker.Mock(), "[sn]")
    device._conn = mocker.AsyncMock()
    return device


async def test_smart_generator_updates_from_message(device, mr521_msg):
    to_process = Packet(
        src=0x14,
        dst=0x21,
        cmd_set=0xFE,
        cmd_id=0x15,
        payload=mr521_msg.SerializeToString(),
    )

    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
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
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None
