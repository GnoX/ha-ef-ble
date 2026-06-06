from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from google.protobuf.message import Message

from ..commands import TimeCommands
from ..devicebase import DeviceBase
from ..entity import controls
from ..entity.base import dynamic
from ..packet import Packet
from ..pb import dev_apl_comm_pb2
from ..props import (
    ProtobufProps,
    pb_field,
    pb_field_group,
    proto_attr_mapper,
)
from ..props.enums import IntFieldValue
from ..props.transforms import pround

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)


class GridStatus(IntFieldValue):
    UNKNOWN = -1

    NOT_VALID = 0
    GRID_IN = 1
    GRID_OFFLINE = 2
    FEED_GRID = 3


class Device(DeviceBase, ProtobufProps):
    """Smart Home Panel 3"""

    SN_PREFIX = (b"HR62", b"HR63", b"HR6C")
    NAME_PREFIX = "EF-SHP3"

    NUM_OF_CIRCUITS = 32

    battery_level = pb_field(pb.cms_batt_soc, pround(2))
    remaining_time_charging = pb_field(pb.cms_chg_rem_time)
    remaining_time_discharging = pb_field(pb.cms_dsg_rem_time)

    battery_charge_limit_min = pb_field(pb.cms_min_dsg_soc)
    battery_charge_limit_max = pb_field(pb.cms_max_chg_soc)
    backup_reserve_level = pb_field(pb.backup_reverse_soc)

    l1_power = pb_field(pb.grid_connection_power_L1, pround(2))
    l2_power = pb_field(pb.grid_connection_power_L2, pround(2))
    l3_power = pb_field(pb.grid_connection_power_L3, pround(2))

    l1_voltage = pb_field(pb.grid_connection_vol_L1, pround(1))
    l2_voltage = pb_field(pb.grid_connection_vol_L2, pround(1))
    l3_voltage = pb_field(pb.grid_connection_vol_L3, pround(1))

    l1_current = pb_field(pb.grid_connection_amp_L1, pround(2))
    l2_current = pb_field(pb.grid_connection_amp_L2, pround(2))
    l3_current = pb_field(pb.grid_connection_amp_L3, pround(2))

    grid_connection_status = pb_field(pb.grid_connection_sta, GridStatus.from_value)
    grid_is_energized = pb_field(pb.grid_is_energized)

    circuit_power = pb_field_group(
        pb.load_ch1_sample_info.load_ch_power,
        match="load_ch{n}_sample_info",
        count=NUM_OF_CIRCUITS,
        transform=pround(2),
        name_template="circuit_power_{n}",
    )
    circuit_current = pb_field_group(
        pb.load_ch1_sample_info.load_ch_curr,
        match="load_ch{n}_sample_info",
        count=NUM_OF_CIRCUITS,
        transform=pround(2),
        name_template="circuit_current_{n}",
    )
    circuit_voltage = pb_field_group(
        pb.load_ch1_sample_info.load_ch_vol,
        match="load_ch{n}_sample_info",
        count=NUM_OF_CIRCUITS,
        transform=pround(1),
        name_template="circuit_voltage_{n}",
    )

    load_system = pb_field(pb.pow_get_sys_load, pround(2))
    load_from_grid = pb_field(pb.pow_get_sys_grid, pround(2))
    battery_power = pb_field(pb.pow_get_bp_cms, pround(2))
    pv_power_sum = pb_field(pb.pow_get_pv_sum, pround(2))

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    async def packet_parse(self, data: bytes):
        return Packet.from_bytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        match packet.version, packet.src, packet.cmd_set, packet.cmd_id:
            case 0x04, 0x32, 0x40, 0x30:
                _, body = _process_payload(packet)
                self.update_from_bytes(dev_apl_comm_pb2.DisplayPropertyUpload, body)
                processed = True
            case 0x04, _, 0x40, 0x30:
                # sub device update
                # sn_suffix, body = _process_payload(packet)
                processed = True
            case (_, 0x35, 0x01, Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME):
                if len(packet.payload) == 0:
                    self._time_commands.async_send_all()
                processed = True

        self._notify_updated()
        return processed

    async def _send_config_packet(self, message: Message):
        payload = message.SerializeToString()
        packet = Packet(0x21, 0x60, 0xFE, 0x11, payload, 0x01, 0x01, 0x13)
        await self._conn.sendPacket(packet)

    @controls.battery(
        battery_charge_limit_min,
        max=dynamic(battery_charge_limit_max),
    )
    async def set_battery_charge_limit_min(self, limit: float):
        await self._send_config_packet(
            dev_apl_comm_pb2.ConfigWrite(cfg_min_dsg_soc=int(limit))
        )
        return True

    @controls.battery(
        battery_charge_limit_max,
        min=dynamic(battery_charge_limit_min),
    )
    async def set_battery_charge_limit_max(self, limit: float):
        await self._send_config_packet(
            dev_apl_comm_pb2.ConfigWrite(cfg_max_chg_soc=int(limit))
        )
        return True

    @controls.battery(backup_reserve_level, max=100)
    async def set_backup_reserve_level(self, value: float):
        await self._send_config_packet(
            dev_apl_comm_pb2.ConfigWrite(cfg_backup_reverse_soc=int(value))
        )
        return True


def _process_payload(packet: Packet):
    # SHP3 v4 payload begins with a fixed 22-byte routing header before the
    # DisplayPropertyUpload protobuf body. Bytes [0:8] carry the source device SN
    # suffix, bytes [18:21] are a stable end-of-header sentinel; bytes [14:17] hold a
    # subsystem nibble + 24-bit seq counter that we don't need to interpret to read
    # state.
    _V4_ROUTING_HEADER_LEN = 22
    _V4_SN_SUFFIX_LEN = 9
    sn_suffix = packet.payload[:_V4_SN_SUFFIX_LEN].decode("ascii", errors="replace")
    body = packet.payload[_V4_ROUTING_HEADER_LEN:]
    return sn_suffix, body
