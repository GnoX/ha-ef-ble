from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from ..commands import TimeCommands
from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import dev_apl_comm_pb2
from ..props import (
    ProtobufProps,
    pb_field,
    proto_attr_mapper,
)
from ..props.transforms import pround

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)


class Device(DeviceBase, ProtobufProps):
    """Smart Home Panel 3"""

    SN_PREFIX = (b"HR62", b"HR63", b"HR6C")
    NAME_PREFIX = "EF-SHP3"

    battery_level = pb_field(pb.cms_batt_soc, pround(2))

    l1_power = pb_field(pb.grid_connection_power_L1, pround(2))
    l2_power = pb_field(pb.grid_connection_power_L2, pround(2))
    l3_power = pb_field(pb.grid_connection_power_L3, pround(2))

    load_total = pb_field(pb.pow_get_sys_load, pround(2))
    load_from_grid = pb_field(pb.pow_get_sys_grid, pround(2))
    battery_power = pb_field(pb.pow_get_bp_cms, pround(2))
    pv_power_sum = pb_field(pb.pow_get_pv_sum, pround(2))

    @property
    def packet_version(self) -> int:
        return 0x04

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

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        match packet.version, packet.src, packet.cmdSet, packet.cmdId:
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


def _process_payload(packet: Packet):
    # SHP3 v4 payload begins with a fixed 22-byte routing header before the
    # DisplayPropertyUpload protobuf body. Bytes [0:8] carry the source device SN
    # suffix, bytes [18:21] are a stable end-of-header sentinel; bytes [14:17] hold
    # a subsystem nibble + 24-bit seq counter that we don't need to interpret to
    # read state.
    _V4_ROUTING_HEADER_LEN = 22
    _V4_SN_SUFFIX_LEN = 9
    sn_suffix = packet.payload[:_V4_SN_SUFFIX_LEN].decode("ascii", errors="replace")
    body = packet.payload[_V4_ROUTING_HEADER_LEN:]
    return sn_suffix, body
