from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import (
    iot_comm_pb2,
    jt_s1_ecology_dev_pb2,
    jt_s1_sys_pb2,
    platform_comm_pb2,
    jt_s1_parallel_pb2,
    jt_s1_edev_pb2,
    jt_s1_edev_convert_pb2,
    jt_s1_ev_pb2,
    jt_s1_heatpump_pb2,
    jt_s1_heatingrod_pb2,
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

    async def isPowerOceanPlus(self):
        return False

    async def data_parse(self, packet: Packet):
        processed = False
        self.reset_updated()

        match packet.src, packet.cmdSet, packet.cmdId:
            case _, 0xFE, 0x10:
                self.update_from_message(platform_comm_pb2.EventRecordReport())
                # TODO(gnox): should respond with platform_comm_pb2.EventInfoReportAck
            case 0x35, 0x35, 0x71:
                self.update_from_message(iot_comm_pb2.ModuleClusterInfo())
            # 96,96,x  - (47)
            case 0x60, 0x60, 0x0D:  #
                # NOTE(gnox): network config data - even though it is parsable as
                # protocol buffers, in the app, it's parsed manually into NetConfig
                # beans
                pass
            case 0x60, 0x60, 0x0A:  #
                self.update_from_message(jt_s1_sys_pb2.EmsAllTimerTaskReport())
            case 0x60, 0x60, 0x0B: #
                self.update_from_message(jt_s1_sys_pb2.EmsEcologyDevReport())
            case 0x60, 0x60, 0x21: #
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReport())

            case 0x60, 0x60, 0x01: # 1
                self.update_from_message(jt_s1_sys_pb2.HeartbeatReport())
            case 0x60, 0x60, 0x03: # 3
                self.update_from_message(jt_s1_sys_pb2.ErrorChangeReport())
            case 0x60, 0x60, 0x07: # 7
                self.update_from_message(jt_s1_sys_pb2.BpHeartbeatReport())
            case 0x60, 0x60, 0x08: # 8
                if not self.isPowerOceanPlus():
                    self.update_from_message(jt_s1_sys_pb2.EmsChangeReport())
                else:
                    self.update_from_message(jt_s1_sys_pb2.EmsChangeReport()) # TODO(andy) fix wrong proto

            case 0x60, 0x60, 0x21: # 10
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 11
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 12
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 13
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 14
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())

            case 0x60, 0x60, 0x21: # 17
                self.update_from_message(jt_s1_sys_pb2.EnergyStremReport())

            case 0x60, 0x60, 0x21: # 24
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 25
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 26
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())

            case 0x60, 0x60, 0x21: # 33
                self.update_from_message(jt_s1_sys_pb2.EnergyStremReport())
            case 0x60, 0x60, 0x21: # 34
                self.update_from_message(jt_s1_sys_pb2.EnergyStremReport())
            case 0x60, 0x60, 0x21: # 35
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 36
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 37
                self.update_from_message(jt_s1_sys_pb2.EnergyStremReport())


            case 0x60, 0x60, 0x21: # 41
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 39
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())

            case 0x60, 0x60, 0x21: # 50
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())

            case 0x60, 0x60, 0x21: # 98
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 99
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 100
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 101
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 102
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 103
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 105
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 106
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 107
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 109
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())

            case 0x60, 0x60, 0x21: # 112
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())

            case 0x60, 0x60, 0x21: # 121
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 124
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 125
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 126
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 127
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 132
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 133
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 137
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 138
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())

            case 0x60, 0x60, 0x21: # 143
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 144
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 145
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 147
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 148
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 151
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 152
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())
            case 0x60, 0x60, 0x21: # 153
                self.update_from_message(jt_s1_sys_pb2.EnergyStreamReort())








            # 96,209,x -
            case 0x60, 0xD1, 0x02: # 2
                self.update_from_message(jt_s1_ev_pb2.EVChargingTimerTaskReport())
            case 0x60, 0xD1, 0x08: # 8
                self.update_from_message(jt_s1_ev_pb2.EVChargingParamReport())
            case 0x60, 0xD1, 0x21: # 33
                self.update_from_message(jt_s1_ev_pb2.EVChargingEnergyStreamReport())
            case 0x60, 0xD1, 0x61: # 97
                self.update_from_message(jt_s1_ev_pb2.EVChargingListAck())
            case 0x60, 0xD1, 0x62: # 98
                self.update_from_message(jt_s1_ev_pb2.EVChargingBindAck())
            case 0x60, 0xD1, 0x63: # 99
                self.update_from_message(jt_s1_ev_pb2.EVChargingParamSetAck())
            case 0x60, 0xD1, 0x64: # 100
                self.update_from_message(jt_s1_ev_pb2.EVChargingAppCtrlAck())
            case 0x60, 0xD1, 0x65: # 101
                self.update_from_message(jt_s1_ev_pb2.EVChargingTimerTaskCfgAck())
            case 0x60, 0xD1, 0x67: # 103
                self.update_from_message(jt_s1_ev_pb2.EVChargingVehicleSetAck())

            # 96,211,x
            case 0x60, 0xD3, 0x01: # 1
                self.update_from_message(jt_s1_heatpump_pb2.HPUIReport())
            case 0x60, 0xD3, 0x02: # 2
                self.update_from_message(jt_s1_heatpump_pb2.HPTimerTaskReport())
            case 0x60, 0xD3, 0x63: # 99
                self.update_from_message(jt_s1_heatpump_pb2.HPParamSetAck())
            case 0x60, 0xD3, 0x64: # 100
                self.update_from_message(jt_s1_heatpump_pb2.HPParamGetAck())
            case 0x60, 0xD3, 0x66: # 102
                self.update_from_message(jt_s1_heatpump_pb2.HPTimerTaskCfgAck())

            # 96,212,x
            case 0x60, 0xD4, 0x02: # 2
                self.update_from_message(jt_s1_heatingrod_pb2.HeatingRodTimerTaskReport())
            case 0x60, 0xD4, 0x08: # 8
                self.update_from_message(jt_s1_heatingrod_pb2.HRChargingParamReport())
            case 0x60, 0xD4, 0x21: # 33
                self.update_from_message(jt_s1_heatingrod_pb2.HeatingRodEnergyStreamShow())
            case 0x60, 0xD4, 0x63: # 99
                self.update_from_message(jt_s1_heatingrod_pb2.HeatingRodParamSetAck())
            case 0x60, 0xD4, 0x65: # 101
                self.update_from_message(jt_s1_heatingrod_pb2.HeatingRodTimerTaskCfgAck())

            # 96,224,x
            case 0x60, 0xE0, 0x01:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevBindListReport())
            case 0x60, 0xE0, 0x6A:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevBindAck())
            case 0x60, 0xE0, 0x6B:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevGetAck())

            # 96,225,x
            # case 0x60, 0xE1, 0x61:
            #     self.update_from_message(jt_s1_parallel_pb2.ParallelDevList()) # TODO(andy) Not sure if right one
            # case 0x60, 0xE1, 0x62:
            #     self.update_from_message(jt_s1_parallel_pb2.DevInfo()) # TODO(andy) Not sure

            # 96,240,x
            case 0x60, 0xF0, 0x6B:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevGetAck())
            case 0x60, 0xF0, 0x6B:
                self.update_from_message(jt_s1_ecology_dev_pb2.EcologyDevGetAck())


            # 96,241,x
            case 0x60, 0xF1, 0x01:
                self.update_from_message(jt_s1_edev_pb2.EDevBindListReport())
            case 0x60, 0xF1, 0x03: # 3
                self.update_from_message(jt_s1_edev_convert_pb2.EDevParamReport())
            case 0x60, 0xF1, 0x04: # 4
                self.update_from_message(jt_s1_edev_pb2.EDevTimerTaskReport())
            case 0x60, 0xF1, 0x21:  # 33
                self.update_from_message(jt_s1_edev_pb2.EDevEnergyStreamShow())
            case 0x60, 0xF1, 0x64: # 100
                self.update_from_message(jt_s1_edev_pb2.EDevOnOffSetAck())
            case 0x60, 0xF1, 0x65:  # 101
                self.update_from_message(jt_s1_edev_pb2.EDevModeSetAck())
            case 0x60, 0xF1, 0x66:  # 102
                self.update_from_message(jt_s1_edev_convert_pb2.EDevParamSetAck())
            case 0x60, 0xF1, 0x6A:  # 106
                self.update_from_message(jt_s1_edev_pb2.EDevTimerTaskCfgSetAck())
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
