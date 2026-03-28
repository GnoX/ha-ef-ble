from bleak import AdvertisementData, BLEDevice

from ._powerocean_base import PowerOceanBase, WorkMode
from ..packet import Packet
from ..pb import (
    re307_sys_pb2,
)
from ..props import proto_attr_mapper, pb_field

pb_ems_state_change_report = proto_attr_mapper(re307_sys_pb2.EmsStateChangeReport)
pb_ems_change_report = proto_attr_mapper(re307_sys_pb2.EmsChangeReport)


# It seems that Plus uses EmsStateChangeReport instead EmsChangeReport, and what Plus calls EmsChangeReport
# contains different data

class Device(PowerOceanBase):
    """PowerOcean Plus"""

    # R372ZD Plus - 3 phase

    SN_PREFIX = (b"R37",)
    NAME_PREFIX = "EF-R37"

    ems_work_mode = pb_field(pb_ems_change_report.ems_word_mode, WorkMode.from_mode)

    bp_soc = pb_field(pb_ems_state_change_report.bp_soc)
    bp_total_chg_energy = pb_field(pb_ems_state_change_report.bp_total_chg_energy)
    bp_total_dsg_energy = pb_field(pb_ems_state_change_report.bp_total_dsg_energy)
    bp_online_sum = pb_field(pb_ems_state_change_report.bp_online_sum)

    # String data (only Plus supports 3rd string)
    pv_fault_code_1 = pb_field(pb_ems_state_change_report.mppt1_fault_code)
    pv_warning_code_1 = pb_field(pb_ems_state_change_report.mppt1_warning_code)

    pv_fault_code_2 = pb_field(pb_ems_state_change_report.mppt2_fault_code)
    pv_warning_code_2 = pb_field(pb_ems_state_change_report.mppt2_warning_code)

    # pv_voltage_3 = _MpptPv(3, 'vol')
    # pv_current_3 = _MpptPv(3, 'amp')
    # pv_power_3 = _MpptPv(3, 'pwr')
    pv_fault_code_3 = pb_field(pb_ems_state_change_report.mppt3_fault_code)
    pv_warning_code_3 = pb_field(pb_ems_state_change_report.mppt3_warning_code)

    def __init__(
            self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)

    # TODO(andy) - we have three different codes on same message. In PO Standard all go to the same message
    #    but with po_plus, two different messages will need to be served (probably):
    #        pb_ems_state_change_report
    #        pb_ems_change_report
    #    until we have test device we can't be sure which is processed with which. It seems like
    #        po.pb_ems_change_report is similar than pb_ems_state_change_report (and not pb_ems_change_report as we
    #        would expect)
    #    packet.cmdId == 0x08 or packet.cmdId == 0x11 or packet.cmdId == 0x25:
    def processEmsChangeReport(self, packet: Packet):
        self.update_from_bytes(re307_sys_pb2.EmsChangeReport, packet.payload)
