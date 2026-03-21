from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import (
    iot_comm_pb2,
    jt_s1_ecology_dev_pb2,
    jt_s1_sys_pb2,
    platform_comm_pb2,
)
from ..props import (
    ProtobufProps,
    pb_field,
    proto_attr_mapper,
)

pb_heartbeat = proto_attr_mapper(jt_s1_sys_pb2.HeartbeatReport)
pb_moduleinfo = proto_attr_mapper(iot_comm_pb2.ModuleInfo)


class Device(DeviceBase, ProtobufProps):
    SN_PREFIX = (b"J32",)
    NAME_PREFIX = "EF-J32"

    grid_power = pb_field(pb_heartbeat.ems_bp_power)

    @classmethod
    def check(cls, sn: bytes):
        return sn[:3] in cls.SN_PREFIX

    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet):
        processed = False
        self.reset_updated()

        match packet.src, packet.cmdSet, packet.cmdId:
            case _, 0xFE, 0x10:
                self.update_from_message(platform_comm_pb2.EventRecordReport())
                # TODO(gnox): should respond with platform_comm_pb2.EventInfoReportAck
            case 0x35, 0x35, 0x71:
                self.update_from_message(iot_comm_pb2.ModuleClusterInfo())
            case 0x60, 0x60, 0x01:
                self.update_from_message(jt_s1_sys_pb2.HeartbeatReport())
            case 0x60, 0x60, 0x03:
                self.update_from_message(jt_s1_sys_pb2.ErrorChangeReport())
            case 0x60, 0x60, 0x07:
                self.update_from_message(jt_s1_sys_pb2.BpHeartbeatReport())
            case 0x60, 0x60, 0x08:
                self.update_from_message(jt_s1_sys_pb2.EmsChangeReport())
            case 0x60, 0x60, 0x0D:
                # NOTE(gnox): network config data - even though it is parsable as
                # protocol buffers, in the app, it's parsed manually into NetConfig
                # beans
                pass
            case 0x60, 0x60, 0x0A:
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0x60, 0x0B:
                self.update_from_message(jt_s1_sys_pb2.EmsEcologyDevReport())
            case 0x60, 0x60, 0x21:
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReport())
            case 0x60, 0xE0, 0x01:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevGetAck())

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed
