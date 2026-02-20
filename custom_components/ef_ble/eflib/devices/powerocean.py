from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import (
    iot_comm_pb2,
    jt_s1_ecology_dev_pb2,
    jt_s1_sys_pb2,
    platform_comm_pb2, jt_s1_parallel_pb2, jt_s1_edev_convert_pb2, jt_s1_ev_pb2,
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
        return sn[:4] in cls.SN_PREFIX

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
            # 96,96,x  - 47
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

            # 96,209,x -
            case 0x60, 0xD1, 0x0A: # 2
                self.update_from_message(jt_s1_ev_pb2.EVChargingTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 8
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 33
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 97
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 98
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 99
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 100
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 101
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0xD1, 0x0A: # 103
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())


            # 96,211,x
            # 96,212,x
            # 96,224,x
            case 0x60, 0xE0, 0x01:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevBindListReport())
            case 0x60, 0xE0, 0x6A:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevBindAck())
            case 0x60, 0xE0, 0x6B:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevGetAck())

            # 96,225,x
            case 0x60, 0xE1, 0x61:
                self.update_from_message(jt_s1_parallel_pb2.ParallelDevList()) # TODO(andy) Not sure if right one
            case 0x60, 0xE1, 0x62:
                self.update_from_message(jt_s1_parallel_pb2.DevInfo()) # TODO(andy) Not sure

            # 96,240,x
            case 0x60, 0xF0, 0x6B:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevGetAck())

            # 96,241,x
            # case 0x60, 0xF1, 0x01:
            #     self.update_from_message(jt_s1_edev_convert_pb2.EDevBindListReport())
            case 0x60, 0xF1, 0x03: # 3
                self.update_from_message(jt_s1_edev_convert_pb2.EDevParamReport())
            # case 0x60, 0xF1, 0x04: # 4
            #     self.update_from_message(jt_s1_edev_convert_pb2.EDevTimerTaskReport())
            # case 0x60, 0xF1, 0x21:  # 33
            #     self.update_from_message(jt_s1_edev_convert_pb2.EDevEnergyStreamShow())
            # case 0x60, 0xF1, 0x64: # 100
            #     self.update_from_message(jt_s1_edev_convert_pb2.EDevOnOffSetAck())
            # case 0x60, 0xF1, 0x65:  # 101
            #     self.update_from_message(jt_s1_edev_convert_pb2.EDevModeSetAck())
            case 0x60, 0xF1, 0x66:  # 102
                self.update_from_message(jt_s1_edev_convert_pb2.EDevParamSetAck())
            # case 0x60, 0xF1, 0x6A:  # 106
            #     self.update_from_message(jt_s1_edev_convert_pb2.EDevTimerTaskCfgSetAck())
            case 0x60, 0xF1, 0x6C: # 108
                self.update_from_message(jt_s1_edev_convert_pb2.EDevExpendCtrlAck())
            case 0x60, 0xF1, 0x71:  # 113
                self.update_from_message(jt_s1_edev_convert_pb2.BatchBindAck())

            # _,53,x
            # 53,53,x
            # 3,50,x



        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed
