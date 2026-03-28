import logging

from bleak import BLEDevice, AdvertisementData

from ._powerocean_base import PowerOceanBase, WorkMode
from ..packet import Packet
from ..pb import (
    jt_s1_sys_pb2,
)
#from ..pb.jt_s1_sys_pb2 import WorkMode
from ..props import (
    pb_field,
    proto_attr_mapper,
)


_LOGGER = logging.getLogger(__name__)

# pb_heartbeat = proto_attr_mapper(jt_s1_sys_pb2.HeartbeatReport)
# pb_moduleinfo = proto_attr_mapper(iot_comm_pb2.ModuleInfo)
# pb_energy_stream_report = proto_attr_mapper(jt_s1_sys_pb2.EnergyStreamReport)
# pb_error_change_report = proto_attr_mapper(jt_s1_sys_pb2.ErrorChangeReport)
# pb_bp_heart = proto_attr_mapper(jt_s1_sys_pb2.BpHeartbeatReport)
# pb_ems_change_report = proto_attr_mapper(jt_s1_sys_pb2.EmsChangeReport)
# pb_sys_param_get_ack = proto_attr_mapper(jt_s1_sys_pb2.SysParamGetAck)
# pb_edev_energy_stream = proto_attr_mapper(jt_s1_edev_pb2.EDevEnergyStreamShow)


pb_ems_change_report = proto_attr_mapper(jt_s1_sys_pb2.EmsChangeReport)



#      TODO:
#       X  - error change report
#       - sensor values:
#           - add sensor values from cloud implementation   DONE
#           - support for total accumulating values if possible and few missing
#       - add diagnostic values
#       OK - put pass on most of messages (I wouldn't remove implementation, because we have all of there, if we need to
#       OK   use it we can just uncomment it and use the message)
#       - hotrod support (v2)
#       - EV support (v2)
#       - HeatPump support (v2)
#       OK    - split into plus and normal version
#       Integration:
#                    - add standalone sensors
#                    - connected devices: Phases (A,B,C)
#                    - connected devices: PV String (1,2,3)
#                    - connected devices: Battery packs (1-4)
#

#   Description:
#   This device is to be used for all PowerOcean models that are not plus and pro. There is quite a lot of
#   "Standard" models available and they all should be handled by this implementation.

class Device(PowerOceanBase):
    """PowerOcean"""

    SN_PREFIX = (b"J32", b"HJ3", b"HC3")  # 1-phase, 3-phase, DC-Fit
    NAME_PREFIX = "EF-J32"

    ems_work_mode = pb_field(pb_ems_change_report.ems_word_mode, WorkMode.from_mode)

    bp_soc = pb_field(pb_ems_change_report.bp_soc)
    bp_total_chg_energy = pb_field(pb_ems_change_report.bp_total_chg_energy)
    bp_total_dsg_energy = pb_field(pb_ems_change_report.bp_total_dsg_energy)
    bp_online_sum = pb_field(pb_ems_change_report.bp_online_sum)

    # String data
    pv_fault_code_1 = pb_field(pb_ems_change_report.mppt1_fault_code)  # mppt_pv1_fault_code
    pv_warning_code_1 = pb_field(pb_ems_change_report.mppt1_warning_code)  # mppt_pv1_warning_code

    pv_fault_code_2 = pb_field(pb_ems_change_report.mppt2_fault_code)
    pv_warning_code_2 = pb_field(pb_ems_change_report.mppt2_warning_code)


    def process_ems_change_report(self, packet: Packet):
        self.update_from_bytes(jt_s1_sys_pb2.EmsChangeReport, packet.payload)
