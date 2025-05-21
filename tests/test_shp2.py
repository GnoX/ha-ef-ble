import pytest
from google.protobuf import text_format
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.shp2 import Device, pd303_pb2
from custom_components.ef_ble.eflib.packet import Packet
from custom_components.ef_ble.eflib.props import Field

_proto_time_str = """master_info {
  sys_timezone: -400
  timezone_id: "America/New_York"
}
load_info {
  hall1_watt: 0
  hall1_watt: 20
  hall1_watt: 87
  hall1_watt: 162
  hall1_watt: 14
  hall1_watt: 0
  hall1_watt: 12
  hall1_watt: 0
  hall1_watt: 0
  hall1_watt: 0
  hall1_watt: 0
  hall1_watt: 366
  hall1_curr: 0.105744965
  hall1_curr: 1.95453179
  hall1_curr: 1.14581943
  hall1_curr: 2.81968117
  hall1_curr: 0.15358378
  hall1_curr: 0.100819223
  hall1_curr: 0.116041183
  hall1_curr: 0
  hall1_curr: 0.231809422
  hall1_curr: 0
  hall1_curr: 0.400631398
  hall1_curr: 3.61784816
}
backup_info {
  ch_watt: 0
  ch_watt: -344.076935
  ch_watt: -294.923065
  backup_discharge_time: 1086
  energy_2 {
    charge_time: 143999
    discharge_time: 1191
  }
  energy_3 {
    charge_time: 143999
    discharge_time: 1187
  }
}
watt_info {
  ch_watt: 0
  ch_watt: -344.076935
  ch_watt: -294.923065
  all_hall_watt: 677
}
master_ver_info {
  app_main_ver: 4
  app_dbg_ver: 2
  app_test_ver: 18
}"""

_proto_push_and_set_str = """backup_incre_info {
  errcode {
    err_code: "\000\000\000\000\000\000\000\001"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
    err_code: "\000\000\000\000\000\000\000\000"
  }
  backup_full_cap: 17141
  backup_bat_per: 46
  backup_discharge_rmain_bat_cap: 17141.7598
  cur_discharge_soc: 46.5
  ch1_info {
    backup_is_ready: false
    ctrl_sta: BACKUP_CH_OFF
    force_charge_sta: FORCE_CHARGE_OFF
    backup_rly1_cnt: 7
    backup_rly2_cnt: 7
    wake_up_charge_sta: 0
    energy_5p8_type: 0
  }
  ch2_info {
    backup_is_ready: true
    ctrl_sta: BACKUP_CH_DISCHARGE
    force_charge_sta: FORCE_CHARGE_OFF
    backup_rly1_cnt: 159
    backup_rly2_cnt: 159
    wake_up_charge_sta: 0
    energy_5p8_type: 29
  }
  ch3_info {
    backup_is_ready: true
    ctrl_sta: BACKUP_CH_DISCHARGE
    force_charge_sta: FORCE_CHARGE_OFF
    backup_rly1_cnt: 197
    backup_rly2_cnt: 197
    wake_up_charge_sta: 0
    energy_5p8_type: 29
  }
  Energy1_info {
    dev_info {
      type: 81
    }
    is_enable: 0
    is_connect: 0
    is_ac_open: 0
    is_power_output: 0
    is_grid_charge: 0
    is_mppt_charge: 0
    battery_percentage: 0
    output_power: 0
    oil_pack_num: 0
    mult_pack_num: 0
    ems_chg_flag: 0
    hw_connect: 0
    ems_bat_temp: 0
    lcd_input_watts: 0
    pv_charge_watts: 0
    pv_low_charge_watts: 0
    pv_height_charge_watts: 0
    error_code_num: 0
  }
}"""


@pytest.fixture
def shp2_proto_time():
    return text_format.Merge(_proto_time_str, pd303_pb2.ProtoTime())


@pytest.fixture
def shp2_proto_push_and_set():
    return text_format.Merge(_proto_push_and_set_str, pd303_pb2.ProtoPushAndSet())


@pytest.fixture
def device(mocker: MockerFixture):
    mocker.patch("custom_components.ef_ble.eflib.devicebase.DeviceLogger")
    device = Device(mocker.AsyncMock(), mocker.Mock(), "[sn]")
    device._conn = mocker.AsyncMock()
    return device


async def test_shp2_updates_from_proto_time_message(device, shp2_proto_time):
    to_process = Packet(
        src=0x0B,
        dst=0x00,
        cmd_set=0x0C,
        cmd_id=0x01,
        payload=shp2_proto_time.SerializeToString(),
    )

    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        Device.in_use_power,
        Device.circuit_power_1,
        Device.circuit_power_2,
        Device.circuit_power_3,
        Device.circuit_power_4,
        Device.circuit_power_5,
        Device.circuit_power_6,
        Device.circuit_power_7,
        Device.circuit_power_8,
        Device.circuit_power_9,
        Device.circuit_power_10,
        Device.circuit_power_11,
        Device.circuit_power_12,
        Device.circuit_current_1,
        Device.circuit_current_2,
        Device.circuit_current_3,
        Device.circuit_current_4,
        Device.circuit_current_5,
        Device.circuit_current_6,
        Device.circuit_current_7,
        Device.circuit_current_8,
        Device.circuit_current_9,
        Device.circuit_current_10,
        Device.circuit_current_11,
        Device.circuit_current_12,
        Device.channel_power_1,
        Device.channel_power_2,
        Device.channel_power_3,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None


async def test_shp2_updates_from_proto_push_and_set_message(
    device, shp2_proto_push_and_set
):
    to_process = Packet(
        src=0x0B,
        dst=0x00,
        cmd_set=0x0C,
        cmd_id=0x20,
        payload=shp2_proto_push_and_set.SerializeToString(),
    )

    await device.data_parse(to_process)

    expected_updated_fields: list[Field] = [
        Device.battery_level,
        Device.error_count,
        Device.error_happened,
    ]

    for field in expected_updated_fields:
        assert field.public_name in device.updated_fields
        assert getattr(device, field.public_name) is not None


async def test_shp2_sets_default_for_grid_watt_if_missing(device, shp2_proto_time):
    to_process = Packet(
        src=0x0B,
        dst=0x00,
        cmd_set=0x0C,
        cmd_id=0x01,
        payload=shp2_proto_time.SerializeToString(),
    )

    await device.data_parse(to_process)

    assert getattr(device, Device.grid_power.public_name) == 0.0

    shp2_proto_time.watt_info.grid_watt = 10.5
    to_process = Packet(
        src=0x0B,
        dst=0x00,
        cmd_set=0x0C,
        cmd_id=0x01,
        payload=shp2_proto_time.SerializeToString(),
    )

    await device.data_parse(to_process)
    assert getattr(device, Device.grid_power.public_name) == 10.5
