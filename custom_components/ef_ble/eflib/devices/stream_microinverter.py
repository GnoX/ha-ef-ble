import time

from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import bk_series_pb2
from ..props import ProtobufProps, pb_field, proto_attr_mapper
from ..props.enums import IntFieldValue

pb = proto_attr_mapper(bk_series_pb2.DisplayPropertyUpload)


class GridStdCode(IntFieldValue):
    UNKNOWN = -1

    AUSTRIA = 1
    SWITZER = 2
    POLAND = 3
    NETHERLANDS = 4
    VDE_4105 = 5
    IEEE_1547 = 6
    USER_DEFINED = 7
    NORWAY = 8
    CZECH_REPUBLIC = 9
    DENMARK = 10
    IRELAND = 11
    SWEDEN = 12
    LATVIA = 13
    GREECE_A = 14
    GREECE_B = 15
    PORTUGAL = 16
    ROMANIA = 17
    LITHUANIA = 18
    HUNGARY = 19
    ITALY = 20
    G98 = 21
    G99 = 22
    NTS_631 = 23
    UNE_217001 = 24
    UNE_217002 = 25
    UTE_MAINLAND = 26
    UTE_50HZ_ISLAND = 27
    UTE_60HZ_ISLAND = 28
    BELGIUM = 29
    UKRAINE = 30
    SLOVENIA = 31
    BULGARIA = 32
    EU_GENERAL = 33
    JAPAN = 34
    PHILIPPINES = 35
    NORTH_AMERICA = 1001


def _round(precision: int = 2):
    def _apply(value: float):
        return round(value, precision)

    return _apply


class Device(DeviceBase, ProtobufProps):
    """STREAM Microinverter"""

    SN_PREFIX = (b"BK01", b"BK02", b"N011")
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

    feed_grid_mode_power_limit = pb_field(pb.feed_grid_mode_pow_limit)
    feed_grid_mode_power_max = pb_field(pb.feed_grid_mode_pow_max)

    grid_code = pb_field(pb.grid_code_selection, GridStdCode.from_value)

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet):
        processed = False
        self.reset_updated()

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

    async def set_feed_grid_mode_pow_limit(self, power: int):
        if power < 0 or power > 1200:
            return False

        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_feed_grid_mode_pow_limit=power)
        )
        return True

    async def set_feed_grid_mode_pow_max(self, power: int) -> bool:
        """Set the feed grid mode maximum power."""
        if power < 0 or power > 1200:
            return False

        msg = bk_series_pb2.DisplayPropertyUpload(feed_grid_mode_pow_max=power)
        payload = msg.SerializeToString()
        packet = Packet(0x20, 0x02, 0xFE, 0x11, payload, 0x01, 0x01, 0x13)
        await self._conn.sendPacket(packet)
        return True

    async def set_grid_code(self, code: GridStdCode) -> bool:
        """Set the grid standard code."""
        pb_code = getattr(bk_series_pb2, f"GRID_STD_CODE_{code.name}")
        message = bk_series_pb2.SafetyParamSet(grid_code_selection=pb_code)
        payload = message.SerializeToString()
        packet = Packet(0x20, 0x02, 0xFE, 0x1A, payload, 0x01, 0x01, 0x13)
        await self._conn.sendPacket(packet)
        return True
