from . import powerocean
from ..packet import Packet
from ..pb import (
    re307_sys_pb2,
)
from ..props import proto_attr_mapper, pb_field

pb_ems_state_change_report = proto_attr_mapper(re307_sys_pb2.EmsStateChangeReport)


# It seems that Plus uses EmsStateChangeReport instead EmsChangeReport, and what Plus calls EmsChangeReport
# contains different data

class Device(powerocean.Device):
    """Power Ocean Plus"""

    # R372ZD Plus - 3 phase

    SN_PREFIX = (b"R37",)
    NAME_PREFIX = "EF-R37"


    pv_fault_code_3 = pb_field(pb_ems_state_change_report.mppt3_fault_code)
    pv_warning_code_3 = pb_field(pb_ems_state_change_report.mppt3_warning_code)


    def isPowerOceanPlus(self):
        return True


    def processEmsChangeReport(self, packet: Packet):
        self.update_from_bytes(re307_sys_pb2.EmsChangeReport, packet.payload)