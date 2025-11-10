import time

from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import bk_series_pb2
from ..props import ProtobufProps, pb_field, proto_attr_mapper

pb = proto_attr_mapper(bk_series_pb2.DisplayPropertyUpload)


def _round(precision: int = 2):
    def _apply(value: float):
        return round(value, precision)

    return _apply


class Device(DeviceBase, ProtobufProps):
    """STREAM Microinverter"""

    SN_PREFIX = (b"BK01", b"BK02")
    NAME_PREFIX = "EF-BK"

    pv_power_1 = pb_field(pb.pow_get_pv, _round())
    pv_voltage_1 = pb_field(pb.plug_in_info_pv_vol, _round(1))
    pv_current_1 = pb_field(pb.plug_in_info_pv_amp, _round())

    pv_power_2 = pb_field(pb.pow_get_pv2, _round())
    pv_voltage_2 = pb_field(pb.plug_in_info_pv2_vol, _round(1))
    pv_current_2 = pb_field(pb.plug_in_info_pv2_amp, _round())

    grid_power = pb_field(pb.grid_connection_power)
    grid_voltage = pb_field(pb.grid_connection_vol, _round())
    grid_current = pb_field(pb.grid_connection_amp, _round())
    grid_frequency = pb_field(pb.grid_connection_freq, _round())

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    async def packet_parse(self, data: bytes) -> Packet:
        return Packet.fromBytes(data, is_xor=True)

    async def data_parse(self, packet: Packet):
        processed = False
        if packet.src == 0x02 and packet.cmdSet == 0xFE and packet.cmdId == 0x15:
            self.update_from_bytes(bk_series_pb2.DisplayPropertyUpload, packet.payload)
            processed = True

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed

    async def _send_config_packet(self, message: bk_series_pb2.ConfigWrite):
        payload = message.SerializeToString()
        message.cfg_utc_time = round(time.time())
        packet = Packet(0x20, 0x02, 0xFE, 0x11, payload, 0x01, 0x01, 0x13)
        await self._conn.sendPacket(packet)

    async def set_inverter_target_power(self, power: int):
        if power < 0:
            return False

        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_inv_target_pwr=power)
        )
        return True
