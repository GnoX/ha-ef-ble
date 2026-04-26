from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from ..commands import TimeCommands
from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import pd100_pb2
from ..props import (
    ProtobufProps,
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

    input_power = pb_field(pb.pow_in_sum_w)
    output_power = pb_field(pb.pow_out_sum_w)

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

        self._notify_updated()

        return processed
