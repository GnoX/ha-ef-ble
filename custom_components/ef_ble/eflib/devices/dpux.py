from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from ..commands import TimeCommands
from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import pd100_pb2
from ..props import (
    ProtobufProps,
    computed_field,
    pb_field,
    proto_attr_mapper,
)
from ..props.transforms import pround

pb = proto_attr_mapper(pd100_pb2.DisplayPropertyUpload)


class Device(DeviceBase, ProtobufProps):
    """Delta Pro Ultra X"""

    SN_PREFIX = (b"P101",)
    NAME_PREFIX = "EF-P10"

    battery_level = pb_field(pb.cms_batt_soc, pround(2))
    cell_temperature = pb_field(pb.cms_batt_temp)

    input_power = pb_field(pb.pow_in_sum_w, pround(2))
    output_power = pb_field(pb.pow_out_sum_w, pround(2))

    ac_input_power = pb_field(pb.pow_get_acp, pround(2))
    ac_input_voltage = pb_field(pb.plug_in_info_acp_vol, pround(2))
    ac_input_current = pb_field(pb.plug_in_info_acp_amp, pround(2))
    plugged_in_ac = pb_field(pb.plug_in_info_ac_charger_flag)

    solar_input_power = pb_field(pb.pow_get_pv)
    solar_input_power_2 = pb_field(pb.pow_get_pv2)
    pv_voltage_1 = pb_field(pb.plug_in_info_pv_vol, pround(2))
    pv_current_1 = pb_field(pb.plug_in_info_pv_amp, pround(2))
    pv_voltage_2 = pb_field(pb.plug_in_info_pv2_vol, pround(2))
    pv_current_2 = pb_field(pb.plug_in_info_pv2_amp, pround(2))

    remaining_time_charging = pb_field(pb.cms_chg_rem_time)
    remaining_time_discharging = pb_field(pb.cms_dsg_rem_time)

    storm_mode = pb_field(pb.storm_pattern_open_flag)
    error_code = pb_field(pb.errcode)

    wifi_rssi = pb_field(pb.module_wifi_rssi)
    sleep_state = pb_field(pb.dev_sleep_state)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet):
        processed = False
        self.reset_updated()

        match packet.src, packet.cmdSet, packet.cmdId:
            case 0x02, 0xFE, 0x15:
                self.update_from_bytes(pd100_pb2.DisplayPropertyUpload, packet.payload)
                processed = True
            case 0x35, 0x01, Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME:
                if len(packet.payload) == 0:
                    self._time_commands.async_send_all()
                processed = True
            case 0x35, 0x35, 0x20:
                # device-initiated BLE keepalive ping - no response expected
                processed = True
            case 0x30, 0x40, 0x30:
                # V4-framed BMS telemetry forwarded from a connected battery pack - the
                # inner protobuf schema is not in the EF Android app source, so we
                # ignore it for now
                processed = True

        self._notify_updated()

        return processed

    @computed_field
    def error_occurred(self) -> bool:
        return bool(self.error_code)
