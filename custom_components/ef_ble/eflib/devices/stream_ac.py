import time

from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import bk_series_pb2
from ..props import ProtobufProps, pb_field, proto_attr_mapper
from ..props.enums import IntFieldValue

pb = proto_attr_mapper(bk_series_pb2.DisplayPropertyUpload)


class EnergyStrategy(IntFieldValue):
    SELF_POWERED = 1
    SCHEDULED = 2
    TOU = 3
    INTELLIGENT_SCHEDULE = 4


class Device(DeviceBase, ProtobufProps):
    """STREAM AC"""

    SN_PREFIX = (b"BK51",)
    NAME_PREFIX = "EF-6"

    battery_level = pb_field(pb.cms_batt_soc)
    cell_temperature = pb_field(pb.bms_max_cell_temp)

    grid_power = pb_field(pb.grid_connection_power)
    grid_voltage = pb_field(pb.grid_connection_vol, lambda v: round(v, 2))
    grid_frequency = pb_field(pb.grid_connection_freq, lambda v: round(v, 2))

    battery_charge_limit_min = pb_field(pb.cms_min_dsg_soc)
    battery_charge_limit_max = pb_field(pb.cms_max_chg_soc)

    load_from_battery = pb_field(pb.pow_get_sys_load_from_bp)
    load_from_grid = pb_field(pb.pow_get_sys_load_from_grid)

    feed_grid = pb_field(pb.feed_grid_mode, lambda x: x == 2)
    feed_grid_pow_limit = pb_field(pb.feed_grid_mode_pow_limit)
    feed_grid_pow_max = pb_field(pb.feed_grid_mode_pow_max)

    energy_backup_battery_level = pb_field(pb.backup_reverse_soc)

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

    async def set_battery_charge_limit_max(self, limit: int):
        await self._send_config_packet(bk_series_pb2.ConfigWrite(cfg_max_chg_soc=limit))
        return True

    async def set_battery_charge_limit_min(self, limit: int):
        await self._send_config_packet(bk_series_pb2.ConfigWrite(cfg_min_dsg_soc=limit))
        return True

    async def enable_ac_1(self, enable: bool):
        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_relay2_onoff=enable)
        )

    async def enable_ac_2(self, enable: bool):
        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_relay3_onoff=enable)
        )

    async def set_energy_backup_battery_level(self, value: int):
        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_backup_reverse_soc=value)
        )
        return True

    async def enable_feed_grid(self, enable: bool):
        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_feed_grid_mode=2 if enable else 0)
        )

    async def set_feed_grid_pow_limit(self, value: int):
        if self.feed_grid_pow_max is None or value > self.feed_grid_pow_max:
            return False
        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_feed_grid_mode_pow_limit=value)
        )
        return True
