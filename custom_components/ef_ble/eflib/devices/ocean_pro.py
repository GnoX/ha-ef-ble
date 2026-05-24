from collections.abc import Sequence

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
    repeated_pb_field_type,
)
from ..props.transforms import pround

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)
pb_rt = proto_attr_mapper(dev_apl_comm_pb2.RuntimePropertyUpload)


class _LoadChPower(
    repeated_pb_field_type(list_field=pb.load_ch_power.common_float_list)
):
    """Per-channel real-time power from `DisplayPropertyUpload.load_ch_power`"""

    idx: int

    def get_item(self, value: Sequence[float]) -> float | None:
        return round(value[self.idx], 2) if value and len(value) > self.idx else None


class Device(DeviceBase, ProtobufProps):
    """OCEAN Pro"""

    SN_PREFIX = (b"HR61",)
    NAME_PREFIX = "EF-HR6"

    NUM_OF_CHANNELS = 34

    plugged_in_ac = pb_field(pb.plug_in_info_acp_charger_flag)
    inverter_frequency = pb_field(pb_rt.third_inv_offgrid_ctrl_freq_curr, pround(2))

    # load_ch_power = field_group(
    #     lambda n: _LoadChPower(n - 1),
    #     count=NUM_OF_CHANNELS,
    #     name_template="load_ch{n}_power",
    # )

    _HEARTBEAT_INTERVAL = 30

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)
        self.add_timer_task(self._request_heartbeat, interval=self._HEARTBEAT_INTERVAL)

    async def _request_heartbeat(self):
        await self._conn.send_auth_status_packet()

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    async def packet_parse(self, data: bytes):
        return Packet.from_bytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        match packet.version, packet.src, packet.cmd_set, packet.cmd_id:
            case 0x04, 0x30, 0x40, 0x30:
                body = _process_payload(packet)
                self.update_from_bytes(dev_apl_comm_pb2.DisplayPropertyUpload, body)
                self.update_from_bytes(dev_apl_comm_pb2.RuntimePropertyUpload, body)
                processed = True
            case (_, 0x35, 0x01, Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME):
                if len(packet.payload) == 0:
                    self._time_commands.async_send_all()
                processed = True

        self._notify_updated()
        return processed


# V4 payload begins with a fixed 22-byte routing header before the DisplayPropertyUpload
# protobuf body. Bytes [0:9] carry the source device SN suffix; the rest of the header
# is a subsystem nibble + sequence counter + a stable end-of-header sentinel that we
# don't need to interpret to read state.
_V4_ROUTING_HEADER_LEN = 22


def _process_payload(packet: Packet) -> bytes:
    return packet.payload[_V4_ROUTING_HEADER_LEN:]
