import logging

from ..connection import ConnectionState
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
    jt_parallel_lan_pb2,
    re307_sys_pb2,
)
from ..pb.jt_s1_sys_pb2 import bms_SysState
from ..props import (
    ProtobufProps,
    pb_field,
    proto_attr_mapper, repeated_pb_field_type,
)
from ..props.enums import IntFieldValue

_LOGGER = logging.getLogger(__name__)

pb_heartbeat = proto_attr_mapper(jt_s1_sys_pb2.HeartbeatReport)
pb_moduleinfo = proto_attr_mapper(iot_comm_pb2.ModuleInfo)
pb_energy_stream_report = proto_attr_mapper(jt_s1_sys_pb2.EnergyStreamReport)
pb_error_change_report = proto_attr_mapper(jt_s1_sys_pb2.ErrorChangeReport)
pb_bp_heart = proto_attr_mapper(jt_s1_sys_pb2.BpHeartbeatReport)
pb_ems_change_report = proto_attr_mapper(jt_s1_sys_pb2.EmsChangeReport)
pb_sys_param_get_ack = proto_attr_mapper(jt_s1_sys_pb2.SysParamGetAck)
pb_edev_energy_stream = proto_attr_mapper(jt_s1_edev_pb2.EDevEnergyStreamShow)



class WorkMode(IntFieldValue):
    WORKMODE_SELFUSE = 0
    WORKMODE_TOU = 1
    WORKMODE_BACKUP = 2
    WORKMODE_DBG = 3
    WORKMODE_AC_MAKEUP = 4
    WORKMODE_DRM_MODE = 5
    WORKMODE_REMOTE_SCHED = 6
    WORKMODE_STANDBY_MODE = 7
    WORKMODE_SOC_CALIB = 8
    WORKMODE_TIMER_MODE = 9
    WORKMODE_FCR_MODE = 10
    WORKMODE_THIRD_MODE = 11
    WORKMODE_AI_SCHEDULE = 12
    WORKMODE_KRAKEN = 13
    UNKNOWN = -1

    @classmethod
    def from_mode(cls, mode: jt_s1_sys_pb2.WorkMode):
        try:
            return cls(mode)
        except ValueError:
            _LOGGER.debug("Encountered invalid value %s for %s", mode, cls.__name__)
            return WorkMode.UNKNOWN

    def __str__(self):
        return self.state_name.upper()

    def as_pb_enum(self):
        return {
            WorkMode.WORKMODE_SELFUSE: jt_s1_sys_pb2.WORKMODE_SELFUSE,
            WorkMode.WORKMODE_TOU: jt_s1_sys_pb2.WORKMODE_TOU,
            WorkMode.WORKMODE_BACKUP: jt_s1_sys_pb2.WORKMODE_BACKUP,
            WorkMode.WORKMODE_DBG: jt_s1_sys_pb2.WORKMODE_DBG,
            WorkMode.WORKMODE_AC_MAKEUP: jt_s1_sys_pb2.WORKMODE_AC_MAKEUP,
            WorkMode.WORKMODE_DRM_MODE: jt_s1_sys_pb2.WORKMODE_DRM_MODE,
            WorkMode.WORKMODE_REMOTE_SCHED: jt_s1_sys_pb2.WORKMODE_REMOTE_SCHED,
            WorkMode.WORKMODE_STANDBY_MODE: jt_s1_sys_pb2.WORKMODE_STANDBY_MODE,
            WorkMode.WORKMODE_SOC_CALIB: jt_s1_sys_pb2.WORKMODE_SOC_CALIB,
            WorkMode.WORKMODE_TIMER_MODE: jt_s1_sys_pb2.WORKMODE_TIMER_MODE,
            WorkMode.WORKMODE_FCR_MODE: jt_s1_sys_pb2.WORKMODE_FCR_MODE,
            WorkMode.WORKMODE_THIRD_MODE: jt_s1_sys_pb2.WORKMODE_THIRD_MODE,
            WorkMode.WORKMODE_AI_SCHEDULE: jt_s1_sys_pb2.WORKMODE_AI_SCHEDULE,
            WorkMode.WORKMODE_KRAKEN: jt_s1_sys_pb2.WORKMODE_KRAKEN,
        }[self]



class BmsSysState(IntFieldValue):
    PRE_POWER_ON_STATE = 0
    CFM_POWER_ON_STATE = 1
    NORMAL_STATE = 2
    POWER_OFF_STATE = 3
    SLEEP_STATE = 4
    UNKNOWN = -1

    @classmethod
    def from_mode(cls, mode: jt_s1_sys_pb2.bms_SysState):
        try:
            return cls(mode)
        except ValueError:
            _LOGGER.debug("Encountered invalid value %s for %s", mode, cls.__name__)
            return BmsSysState.UNKNOWN

    def __str__(self):
        return self.state_name.upper()

    def as_pb_enum(self):
        return {
            BmsSysState.NORMAL_STATE: jt_s1_sys_pb2.NORMAL_STATE,
            BmsSysState.CFM_POWER_ON_STATE: jt_s1_sys_pb2.CFM_POWER_ON_STATE,
            BmsSysState.POWER_OFF_STATE: jt_s1_sys_pb2.POWER_OFF_STATE,
            BmsSysState.PRE_POWER_ON_STATE: jt_s1_sys_pb2.PRE_POWER_ON_STATE,
            BmsSysState.SLEEP_STATE: jt_s1_sys_pb2.SLEEP_STATE,
        }[self]


class BmsRunStaDef(IntFieldValue):
    PB_BMS_STATE_SHUTDOWN = 0
    PB_BMS_STATE_NORMAL = 1
    PB_BMS_STATE_CHARGEABLE = 2
    PB_BMS_STATE_DISCHARGEABLE = 3
    PB_BMS_STATE_FAULT = 4
    UNKNOWN = -1

    @classmethod
    def from_mode(cls, mode: jt_s1_sys_pb2.bms_RunStaDef):
        try:
            return cls(mode)
        except ValueError:
            _LOGGER.debug("Encountered invalid value %s for %s", mode, cls.__name__)
            return BmsRunStaDef.UNKNOWN

    def __str__(self):
        return self.state_name.upper()

    def as_pb_enum(self):
        return {
            BmsRunStaDef.PB_BMS_STATE_SHUTDOWN: jt_s1_sys_pb2.PB_BMS_STATE_SHUTDOWN,
            BmsRunStaDef.PB_BMS_STATE_NORMAL: jt_s1_sys_pb2.PB_BMS_STATE_NORMAL,
            BmsRunStaDef.PB_BMS_STATE_CHARGEABLE: jt_s1_sys_pb2.PB_BMS_STATE_CHARGEABLE,
            BmsRunStaDef.PB_BMS_STATE_DISCHARGEABLE: jt_s1_sys_pb2.PB_BMS_STATE_DISCHARGEABLE,
            BmsRunStaDef.PB_BMS_STATE_FAULT: jt_s1_sys_pb2.PB_BMS_STATE_FAULT,
        }[self]


class _BpHeartbeatIntValue(repeated_pb_field_type(pb_bp_heart.bp_heart_beat, lambda msg: msg, per_item=True)):
    idx: int
    type: str
    def get_value(self, item: jt_s1_sys_pb2.BpStaReport) -> int | None:
        if item.bp_dsrc == self.idx:
            return getattr(item, self.type, None)
        else:
            return None

class _BpHeartbeatFloatValue(repeated_pb_field_type(pb_bp_heart.bp_heart_beat, lambda msg: msg, per_item=True)):
    idx: int
    type: str
    def get_value(self, item: jt_s1_sys_pb2.BpStaReport) -> float | None:
        if item.bp_dsrc == self.idx:
            return getattr(item, self.type, None)
        else:
            return None

class _BpHeartbeatBmsSysState(repeated_pb_field_type(pb_bp_heart.bp_heart_beat, lambda msg: msg, per_item=True)):
    idx: int
    def get_value(self, item: jt_s1_sys_pb2.BpStaReport) -> BmsSysState | None:
        if item.bp_dsrc == self.idx:
            return BmsSysState.from_mode(item.bp_sys_state)
        else:
            return None

class _BpHeartbeatBmsRunStaDef(repeated_pb_field_type(pb_bp_heart.bp_heart_beat, lambda msg: msg, per_item=True)):
    idx: int
    def get_value(self, item: jt_s1_sys_pb2.BpStaReport) -> BmsRunStaDef | None:
        if item.bp_dsrc == self.idx:
            return BmsRunStaDef.from_mode(item.bms_run_sta)
        else:
            return None


class _MpptPv(repeated_pb_field_type(pb_heartbeat.mppt_heart_beat, lambda msg: msg, per_item=True)):
    idx: int
    type: str
    def get_value(self, item: jt_s1_sys_pb2.MpptStaReport) -> float | None:
        if not item.mppt_pv:
            return None

        resolved_idx = self.idx-1

        if (self.idx> len(item.mppt_pv)):
            item_pv = None
        else:
            item_pv = item.mppt_pv[resolved_idx]

        return getattr(item_pv, self.type, None) if item_pv else None


# pb_error_change_report.pcs_err_code.err_code
# ems_err_code


class _EDevEnergyStreamShow(repeated_pb_field_type(pb_edev_energy_stream.energy, lambda msg: msg, per_item=True)):
    idx: int
    type: str
    def get_value(self, item: jt_s1_edev_pb2.EDevEnergyStreamShow) -> float | None:
        if not item.energy:
            return None

        resolved_idx = self.idx-1

        if (self.idx> len(item.energy)):
            item_pv = None
        else:
            item_pv = item.energy[resolved_idx]

        return getattr(item_pv, self.type, None) if item_pv else None


class _EmsErrorCode(repeated_pb_field_type(pb_error_change_report.ems_err_code, lambda msg: msg, per_item=True)):
    def get_value(self, item: jt_s1_sys_pb2.ErrorCode) -> int | None:
        if not item.err_code:
            return None
        else:
            return item.err_code[0]



class _PcsErrorCode(repeated_pb_field_type(pb_error_change_report.pcs_err_code, lambda msg: msg, per_item=True)):
    def get_value(self, item: jt_s1_sys_pb2.ErrorCode) -> int | None:
        if not item.err_code:
            return None
        else:
            return item.err_code[0]


# class _ErrorChangeReport(repeated_pb_field_type(pb_error_change_report, lambda msg: msg, per_item=True)):
#     type: str
#     def get_value(self, item: jt_s1_sys_pb2.MpptStaReport) -> float | None:
#         if not item.mppt_pv:
#             return None
#
#         if self.idx==1:
#             itemPv = item.mppt_pv[0]
#         elif self.idx==2:
#             if len(item.mppt_pv)>1:
#                 itemPv = item.mppt_pv[1]
#             else:
#                 return None
#
#         return getattr(itemPv, self.type, None) if itemPv else None

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

class Device(DeviceBase, ProtobufProps):
    """Power Ocean"""

    #SN_PREFIX = (b"J32")
    SN_PREFIX = (b"J32", b"HJ3", b"HC3")  # 1-phase, 3-phase, DC-Fit
    NAME_PREFIX = "EF-J32"

    PO_INTERNAL_VERSION = "0.3.1"

    ecr_ems_sn = pb_field(pb_error_change_report.ems_err_code.module_sn)
    pcs_sn = pb_field(pb_error_change_report.pcs_err_code.module_sn)

    sys_load_pwr = pb_field(pb_energy_stream_report.sys_load_pwr)
    grid_power = pb_field(pb_energy_stream_report.sys_grid_pwr)  # sys_grid_pwr
    mppt_pwr = pb_field(pb_energy_stream_report.mppt_pwr)
    bp_pwr = pb_field(pb_energy_stream_report.bp_pwr)
    ems_work_mode = pb_field(pb_ems_change_report.ems_word_mode, WorkMode.from_mode)

    pv_power_1 = pb_field(pb_energy_stream_report.pv1_pwr) # pv1_pwr
    pv_power_2 = pb_field(pb_energy_stream_report.pv2_pwr) # pv2_pwr
    pv_power_3 = pb_field(pb_energy_stream_report.pv3_pwr) # on Plus pv3_pwr
    pv_inv_pwr = pb_field(pb_energy_stream_report.pv_inv_pwr)

    pcs_meter_power = pb_field(pb_heartbeat.pcs_meter_power)
    ems_bp_power = pb_field(pb_heartbeat.ems_bp_power)
    pcs_act_pwr = pb_field(pb_heartbeat.pcs_act_pwr)

    bpack1_bp_amp = _BpHeartbeatFloatValue(1, 'bp_amp')
    bpack1_bp_err_code = _BpHeartbeatIntValue(1, 'bp_err_code')
    bpack1_bp_env_temp = _BpHeartbeatFloatValue(1, 'bp_env_temp')
    bpack1_bp_max_cell_temp = _BpHeartbeatFloatValue(1, 'bp_max_cell_temp')
    bpack1_bp_min_cell_temp = _BpHeartbeatFloatValue(1, 'bp_min_cell_temp')
    bpack1_bp_pwr = _BpHeartbeatFloatValue(1, 'bp_pwr')
    bpack1_bp_remain_watth = _BpHeartbeatFloatValue(1, 'bp_remain_watth')
    bpack1_bp_soc = _BpHeartbeatIntValue(1, 'bp_soc')
    bpack1_bp_soh = _BpHeartbeatIntValue(1, 'bp_soh')
    bpack1_bp_vol = _BpHeartbeatFloatValue(1, 'bp_vol')
    bpack1_bp_cycles = _BpHeartbeatIntValue(1, 'bp_cycles') # Diag
    bpack1_bp_sys_state = _BpHeartbeatBmsSysState(1) # Diag
    bpack1_bms_run_sta = _BpHeartbeatBmsRunStaDef(1) # Diag

    bpack2_bp_amp = _BpHeartbeatFloatValue(2, 'bp_amp')
    bpack2_bp_err_code = _BpHeartbeatIntValue(2, 'bp_err_code')
    bpack2_bp_env_temp = _BpHeartbeatFloatValue(2, 'bp_env_temp')
    bpack2_bp_max_cell_temp = _BpHeartbeatFloatValue(2, 'bp_max_cell_temp')
    bpack2_bp_min_cell_temp = _BpHeartbeatFloatValue(2, 'bp_min_cell_temp')
    bpack2_bp_pwr = _BpHeartbeatFloatValue(2, 'bp_pwr')
    bpack2_bp_remain_watth = _BpHeartbeatFloatValue(2, 'bp_remain_watth')
    bpack2_bp_soc = _BpHeartbeatIntValue(2, 'bp_soc')
    bpack2_bp_soh = _BpHeartbeatIntValue(2, 'bp_soh')
    bpack2_bp_vol = _BpHeartbeatFloatValue(2, 'bp_vol')
    bpack2_bp_cycles = _BpHeartbeatIntValue(2, 'bp_cycles') # Diag
    bpack2_bp_sys_state = _BpHeartbeatBmsSysState(2) # Diag
    bpack2_bms_run_sta = _BpHeartbeatBmsRunStaDef(2) # Diag

    bpack3_bp_amp = _BpHeartbeatFloatValue(3, 'bp_amp')
    bpack3_bp_err_code = _BpHeartbeatIntValue(3, 'bp_err_code')
    bpack3_bp_env_temp = _BpHeartbeatFloatValue(3, 'bp_env_temp')
    bpack3_bp_max_cell_temp = _BpHeartbeatFloatValue(3, 'bp_max_cell_temp')
    bpack3_bp_min_cell_temp = _BpHeartbeatFloatValue(3, 'bp_min_cell_temp')
    bpack3_bp_pwr = _BpHeartbeatFloatValue(3, 'bp_pwr')
    bpack3_bp_remain_watth = _BpHeartbeatFloatValue(3, 'bp_remain_watth')
    bpack3_bp_soc = _BpHeartbeatIntValue(3, 'bp_soc')
    bpack3_bp_soh = _BpHeartbeatIntValue(3, 'bp_soh')
    bpack3_bp_vol = _BpHeartbeatFloatValue(3, 'bp_vol')
    bpack3_bp_cycles = _BpHeartbeatIntValue(3, 'bp_cycles')  # Diag
    bpack3_bp_sys_state = _BpHeartbeatBmsSysState(3) # Diag
    bpack3_bms_run_sta = _BpHeartbeatBmsRunStaDef(3) # Diag

    bpack4_bp_amp = _BpHeartbeatFloatValue(4, 'bp_amp')
    bpack4_bp_err_code = _BpHeartbeatIntValue(4, 'bp_err_code')
    bpack4_bp_env_temp = _BpHeartbeatFloatValue(4, 'bp_env_temp')
    bpack4_bp_max_cell_temp = _BpHeartbeatFloatValue(4, 'bp_max_cell_temp')
    bpack4_bp_min_cell_temp = _BpHeartbeatFloatValue(4, 'bp_min_cell_temp')
    bpack4_bp_pwr = _BpHeartbeatFloatValue(4, 'bp_pwr')
    bpack4_bp_remain_watth = _BpHeartbeatFloatValue(4, 'bp_remain_watth')
    bpack4_bp_soc = _BpHeartbeatIntValue(4, 'bp_soc')
    bpack4_bp_soh = _BpHeartbeatIntValue(4, 'bp_soh')
    bpack4_bp_vol = _BpHeartbeatFloatValue(4, 'bp_vol')
    bpack4_bp_cycles = _BpHeartbeatIntValue(4, 'bp_cycles')  # Diag
    bpack4_bp_sys_state = _BpHeartbeatBmsSysState(4) # Diag
    bpack4_bms_run_sta = _BpHeartbeatBmsRunStaDef(4) # Diag

    bp_remain_watth = pb_field(pb_heartbeat.bp_remain_watth)
    bp_soc = pb_field(pb_ems_change_report.bp_soc)
    bp_total_chg_energy = pb_field(pb_ems_change_report.bp_total_chg_energy)
    bp_total_dsg_energy = pb_field(pb_ems_change_report.bp_total_dsg_energy)
    bp_online_sum = pb_field(pb_ems_change_report.bp_online_sum)

    pcs_a_phase_vol = pb_field(pb_heartbeat.pcs_a_phase.vol)
    pcs_a_phase_amp = pb_field(pb_heartbeat.pcs_a_phase.amp)
    pcs_a_phase_act_pwr = pb_field(pb_heartbeat.pcs_a_phase.act_pwr)
    pcs_a_phase_react_pwr = pb_field(pb_heartbeat.pcs_a_phase.react_pwr)
    pcs_a_phase_apparent_pwr = pb_field(pb_heartbeat.pcs_a_phase.apparent_pwr)

    pcs_b_phase_vol = pb_field(pb_heartbeat.pcs_b_phase.vol)
    pcs_b_phase_amp = pb_field(pb_heartbeat.pcs_b_phase.amp)
    pcs_b_phase_act_pwr = pb_field(pb_heartbeat.pcs_b_phase.act_pwr)
    pcs_b_phase_react_pwr = pb_field(pb_heartbeat.pcs_b_phase.react_pwr)
    pcs_b_phase_apparent_pwr = pb_field(pb_heartbeat.pcs_b_phase.apparent_pwr)

    pcs_c_phase_vol = pb_field(pb_heartbeat.pcs_c_phase.vol)
    pcs_c_phase_amp = pb_field(pb_heartbeat.pcs_c_phase.amp)
    pcs_c_phase_act_pwr = pb_field(pb_heartbeat.pcs_c_phase.act_pwr)
    pcs_c_phase_react_pwr = pb_field(pb_heartbeat.pcs_c_phase.react_pwr)
    pcs_c_phase_apparent_pwr = pb_field(pb_heartbeat.pcs_c_phase.apparent_pwr)

    mppt_pv1_fault_code = pb_field(pb_ems_change_report.mppt1_fault_code)
    mppt_pv1_warning_code = pb_field(pb_ems_change_report.mppt1_warning_code)
    mppt_pv2_fault_code = pb_field(pb_ems_change_report.mppt2_fault_code)
    mppt_pv2_warning_code = pb_field(pb_ems_change_report.mppt1_warning_code)

    mppt_pv1_vol = _MpptPv(1,'vol')
    mppt_pv1_amp = _MpptPv(1,'amp')
    mppt_pv1_pwr = _MpptPv(1,'pwr')

    mppt_pv2_vol = _MpptPv(2, 'vol')
    mppt_pv2_amp = _MpptPv(2, 'amp')
    mppt_pv2_pwr = _MpptPv(2, 'pwr')

    mppt_pv3_vol = _MpptPv(3, 'vol')
    mppt_pv3_amp = _MpptPv(3, 'amp')
    mppt_pv3_pwr = _MpptPv(3, 'pwr')



    # mpptPv_pwrTotal     0.00015777285     W

    # todayElectricityGeneration     4.09     kWh
    # totalElectricityGeneration     14.48     kWh
    # monthElectricityGeneration     14.48     kWh
    # yearElectricityGeneration      14.48     kWh


    # TODO testing edev
    edev_1_from_pv = _EDevEnergyStreamShow(1, 'from_pv')
    edev_1_from_bat = _EDevEnergyStreamShow(1, 'from_bat')
    edev_1_from_grid = _EDevEnergyStreamShow(1, 'from_grid')
    edev_1_pwr = _EDevEnergyStreamShow(1, 'pwr')


    # TODO test code for island mode - remove before production
    spga_sys_grid_disconnect_mode = pb_field(pb_sys_param_get_ack.sys_grid_disconnect_mode)
    spga_ems_backup_event = pb_field(pb_sys_param_get_ack.ems_backup_event)
    spga_ems_max_feed_pwr = pb_field(pb_sys_param_get_ack.ems_max_feed_pwr)
    spga_ems_work_mode = pb_field(pb_sys_param_get_ack.ems_work_mode)
    # Test fields trying to see if offgrid is indicated
    power_limit_mode = pb_field(pb_heartbeat.power_limit_mode)
    pcs_offgrid_para_type = pb_field(pb_heartbeat.pcs_offgrid_para_type)
    pcs_offgrid_para_addr = pb_field(pb_heartbeat.pcs_offgrid_para_addr)

    @classmethod
    def check(cls, sn: bytes):
        return sn[:3] in cls.SN_PREFIX

    @property
    def device(self):
        model = " (Unidentified)"
        match self._sn[:4]:
            case "HJ31":
                model = "10 kW"
            case "HJ35":
                model = "6kW"
            case "HJ36":
                model = "8kW"
            case "HJ37":
                model = "12kW"
            case "J321":
                model = "Single Phase"
            case "J32A":
                model = "Single Phase 3kW"
            case "J32B":
                model = "Single Phase 3.68kW"
            case "J32C":
                model = "Single Phase 4.6kW"
            case "J32D":
                model = "Single Phase 5kW"
            case "J32E":
                model = "Single Phase 6kW"
            case "R372ZD":
                model = "Plus - 3 phase"
            case "HC31":
                model = "DC Fit"  # this might work or not

        return f"Power Ocean {model}".strip()


    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    def isPowerOceanPlus(self):
        return False

    # In this method we create ignore list, to prevent any "unsupported" or "new" packets to slip through
    def isOnIgnoreList(self, packet: Packet):
        if packet.src == 0x60 and packet.cmdSet == 0x60:  # base power ocean
            return (packet.cmdId in [10, 11, 12, 13, 14, 24, 25, 26, 34, 35, 36, 41, 50, 98, 99, 100, 101, 102,
                                     103,105,106.107,109,112,121,124,125,126,127,132,133,137,138,143,144,
                                     145,147,148,151,152,153])
        elif packet.src == 0x60 and packet.cmdSet == 0xD1:  # EV  (96,209)
            return packet.cmdId in [2, 97, 98, 99, 100, 101, 103]
        elif packet.src == 0x60 and packet.cmdSet == 0xD3:  # Heat Pump  (96,211)
            return packet.cmdId in [2, 99, 100, 102]
        elif packet.src == 0x60 and packet.cmdSet == 0xD4:  # Heating Rod  (96,212)
            return packet.cmdId in [2, 99, 101]
        elif packet.src == 0x60 and packet.cmdSet == 0xE0:  # ecology_dev (96,224)
            return packet.cmdId in [1, 36, 106, 107]
        elif packet.src == 0x60 and packet.cmdSet == 0xE1:  # parallel_lan (96,225)
            return packet.cmdId in [97, 98]
        elif packet.src == 0x60 and packet.cmdSet == 0xF0:  # edev (96,240)
            return packet.cmdId in [2, 97, 98, 99, 0x02]
        elif packet.src == 0x60 and packet.cmdSet == 0xF1:  # edev (96,241)  Unknown 5, 36
            return packet.cmdId in [1, 3, 4, 5, 36, 100, 101, 102, 106, 108, 113]
        elif packet.src == 0x03 and packet.cmdSet == 0x32:  # eco (3,50)
            return packet.cmdId in [62]
        elif packet.src == 0x35 and packet.cmdSet == 0x35:  #  53,53
            return packet.cmdId in [13, 113, 170]
        elif packet.cmdSet == 0xFE and packet.cmdId == 0x10: # _, 0xFE, 0x10
            return True
        else:
            return False


    async def data_parse(self, packet: Packet):
        if not self.connection_state.authenticated:
            self._conn._set_state(ConnectionState.AUTHENTICATED)
            self._conn._connected.set()

        processed = False
        self.reset_updated()

        check_ignore_list = False

        if packet.src == 0x60 and packet.cmdSet == 0x60:  # base power ocean functionality
            if packet.cmdId == 0x01:  # 1
                self.update_from_bytes(jt_s1_sys_pb2.HeartbeatReport, packet.payload)
            elif packet.cmdId == 0x03:  # 3
                self.update_from_bytes(jt_s1_sys_pb2.ErrorChangeReport, packet.payload)
            elif packet.cmdId == 0x07:  # 7
                self.update_from_bytes(jt_s1_sys_pb2.BpHeartbeatReport, packet.payload)
            elif packet.cmdId == 0x08 or packet.cmdId == 0x11 or packet.cmdId == 0x25:  # 8, 17, 37
                if not self.isPowerOceanPlus():
                    self.update_from_bytes(jt_s1_sys_pb2.EmsChangeReport, packet.payload)
                else:
                    self.update_from_bytes(re307_sys_pb2.EmsChangeReport, packet.payload)
            elif packet.cmdId == 0x21:  # 33
                self.update_from_bytes(jt_s1_sys_pb2.EnergyStreamReport, packet.payload)
            elif packet.cmdId == 0x27:  # 39
                self.update_from_bytes(jt_s1_sys_pb2.EmsPVInvEnergyStreamReport, packet.payload)
            else:
                check_ignore_list = True

        elif packet.src == 0x60 and packet.cmdSet == 0xD1:  # EV (96,209)
            if packet.cmdId == 0x08:  # 8
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingParamReport, packet.payload)
            elif packet.cmdId == 0x21:  # 33
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingEnergyStreamReport, packet.payload)
            else:
                check_ignore_list = True

        elif packet.src == 0x60 and packet.cmdSet == 0xD3:  # Heat Pump (96,211)
            if packet.cmdId == 0x01:  # 1
                self.update_from_bytes(jt_s1_heatpump_pb2.HPUIReport, packet.payload)
            else:
                check_ignore_list = True

        elif packet.src == 0x60 and packet.cmdSet == 0xD4:  # Heating Rod  (96,212)
            if packet.cmdId == 0x08:  # 8
                self.update_from_bytes(jt_s1_heatingrod_pb2.HRChargingParamReport, packet.payload)
            elif packet.cmdId == 0x21:  # 33
                self.update_from_bytes(jt_s1_heatingrod_pb2.HeatingRodEnergyStreamShow, packet.payload)
            else:
                check_ignore_list = True

        elif packet.src == 0x60 and packet.cmdSet == 0xF1:  # EDev  (96,241)
            if packet.cmdId == 0x21:  # 33
                self.update_from_bytes(jt_s1_edev_pb2.EDevEnergyStreamShow, packet.payload)
            else:
                check_ignore_list = True

        else:
            check_ignore_list = True

        if check_ignore_list:
            if not self.isOnIgnoreList(packet):
                self._logger.info("Unknown packet: src=%d,cmdSet=%d,cmdId=%d: \nPacket=%s", packet.src, packet.cmdSet,
                                  packet.cmdId, packet)

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed


    def data_parse_old(self, packet: Packet):
        # TODO temporary solution since PO doesn't return authenticated response and just starts sending data
        if not self.connection_state.authenticated:
            self._conn._set_state(ConnectionState.AUTHENTICATED)
            self._conn._connected.set()

        processed = False
        self.reset_updated()

        # Lot of messages are useless, so I will mark them with pass, but leave processing under comment (in case
        # we need to enable in the future. - Andy

        match packet.src, packet.cmdSet, packet.cmdId:
            case _, 0xFE, 0x10:
                pass # self.update_from_bytes(platform_comm_pb2.EventRecordReport, packet.payload)
                # TODO(gnox): should respond with platform_comm_pb2.EventInfoReportAck
            # 53,53
            case 0x35, 0x35, 0x0d: # 13
                pass   # not sure about this java code call something
            case 0x35, 0x35, 0x71: # 113
                # self._logger.info("PowerOcean: Module Info")
                self.update_from_bytes(iot_comm_pb2.ModuleClusterInfo, packet.payload)
            case 0x35, 0x35, 0xaa: # 170
                pass # self.update_from_bytes(iot_comm_pb2.RefreshTokenAck, packet.payload)

            # 96,96,x  - (47)
            case 0x60, 0x60, 0x01: # 1
                self.update_from_bytes(jt_s1_sys_pb2.HeartbeatReport, packet.payload)
            case 0x60, 0x60, 0x03: # 3
                self.update_from_bytes(jt_s1_sys_pb2.ErrorChangeReport, packet.payload)
            case 0x60, 0x60, 0x07: # 7
                self.update_from_bytes(jt_s1_sys_pb2.BpHeartbeatReport, packet.payload)
            case 0x60, 0x60, 0x08: # 8
                if not self.isPowerOceanPlus():
                    self.update_from_bytes(jt_s1_sys_pb2.EmsChangeReport, packet.payload)
                else:
                    self.update_from_bytes(re307_sys_pb2.EmsChangeReport, packet.payload)
            case 0x60, 0x60, 0x0a: # 10
                self.update_from_bytes(jt_s1_sys_pb2.EmsAllTimerTaskReport, packet.payload)
            case 0x60, 0x60, 0x0b: # 11
                pass # self.update_from_bytes(jt_s1_sys_pb2.EmsEcologyDevReport, packet.payload)
            case 0x60, 0x60, 0x0c: # 12
                self.update_from_bytes(jt_s1_parallel_pb2.ParallelDevListReport, packet.payload)
            case 0x60, 0x60, 0x0D: # 13
                # NOTE(gnox): network config data - even though it is parsable as
                # protocol buffers, in the app, it's parsed manually into NetConfig
                # beans
                pass
            case 0x60, 0x60, 0x0e: # 14
                self.update_from_bytes(jt_s1_sys_pb2.EmsAllTouTaskReport, packet.payload)

            case 0x60, 0x60, 0x11: # 17
                if not self.isPowerOceanPlus():
                    self.update_from_bytes(jt_s1_sys_pb2.EmsChangeReport, packet.payload)
                else:
                    self.update_from_bytes(re307_sys_pb2.EmsChangeReport, packet.payload) # andy - has some code see 8 too
            case 0x60, 0x60, 0x18: # 24
                self.update_from_bytes(jt_s1_sys_pb2.OilEngineBindAck, packet.payload)
            case 0x60, 0x60, 0x19: # 25
                self.update_from_bytes(jt_s1_sys_pb2.OilEngineParaSetAck, packet.payload)
            case 0x60, 0x60, 0x1a: # 26
                self.update_from_bytes(jt_s1_sys_pb2.OilEngineParaReport, packet.payload)

            case 0x60, 0x60, 0x21: # 33
                self.update_from_bytes(jt_s1_sys_pb2.EnergyStreamReport, packet.payload)
            case 0x60, 0x60, 0x22: # 34
                pass  # ignored in java
            case 0x60, 0x60, 0x23: # 35
                self.update_from_bytes(jt_s1_sys_pb2.SysRTCSync, packet.payload)
            case 0x60, 0x60, 0x24: # 36
                self.update_from_bytes(jt_s1_sys_pb2.SysEventRecordReport, packet.payload)
            case 0x60, 0x60, 0x25: # 37
                self.update_from_bytes(jt_s1_sys_pb2.EmsChangeReport, packet.payload)
            case 0x60, 0x60, 0x27: # 39
                self.update_from_bytes(jt_s1_sys_pb2.EmsPVInvEnergyStreamReport, packet.payload)


            case 0x60, 0x60, 0x29: # 41
                self.update_from_bytes(jt_s1_sys_pb2.EmsEcologyDevEnergyStreamReport, packet.payload)

            case 0x60, 0x60, 0x32: # 50
                self.update_from_bytes(jt_s1_parallel_pb2.ParallelEnergyStreamReport, packet.payload)

            case 0x60, 0x60, 0x62: # 98
                self.update_from_bytes(jt_s1_sys_pb2.SysWorkModeSetAck, packet.payload)
            case 0x60, 0x60, 0x63: # 99
                self.update_from_bytes(jt_s1_sys_pb2.SysBackupEventSetAck, packet.payload)
            case 0x60, 0x60, 0x64: # 100
                self.update_from_bytes(jt_s1_sys_pb2.SysKeepSocSetAck, packet.payload)
            case 0x60, 0x60, 0x65: # 101
                self.update_from_bytes(jt_s1_sys_pb2.SysFeedPowerSetAck, packet.payload)
            case 0x60, 0x60, 0x66: # 102
                self.update_from_bytes(jt_s1_sys_pb2.SysOffGridSetAck, packet.payload)
            case 0x60, 0x60, 0x67: # 103
                self.update_from_bytes(jt_s1_sys_pb2.SysParamGetAck, packet.payload)
            case 0x60, 0x60, 0x69: # 105
                self.update_from_bytes(jt_s1_sys_pb2.SysOnOffMachineSetAck, packet.payload)
            case 0x60, 0x60, 0x6a: # 106
                self.update_from_bytes(jt_s1_sys_pb2.EmsEcologyDevGetAck, packet.payload)
            case 0x60, 0x60, 0x6b: # 107
                self.update_from_bytes(jt_s1_sys_pb2.EmsEcologyDevBindAck, packet.payload)
            case 0x60, 0x60, 0x6d: # 109
                pass # self.update_from_bytes(jt_s1_sys_pb2.EmsEcologyDevParamSetAck, packet.payload) this produced error

            case 0x60, 0x60, 0x70: # 112
                self.update_from_bytes(jt_s1_sys_pb2.SysBatChgDsgSetAck, packet.payload)

            case 0x60, 0x60, 0x79: # 121
                self.update_from_bytes(jt_s1_sys_pb2.SysFactoryResetAck, packet.payload)
            case 0x60, 0x60, 0x7c: # 124
                self.update_from_bytes(jt_s1_sys_pb2.EmsSgReadySetAck, packet.payload)
            case 0x60, 0x60, 0x7d: # 125
                self.update_from_bytes(jt_s1_sys_pb2.EmsTimerTaskCfgAck, packet.payload)
            case 0x60, 0x60, 0x7e: # 126
                self.update_from_bytes(jt_s1_sys_pb2.EmsTimerTaskGetAck, packet.payload)
            case 0x60, 0x60, 0x7f: # 127
                self.update_from_bytes(jt_s1_sys_pb2.EmsAllTimerTaskGetAck, packet.payload)
            case 0x60, 0x60, 0x84: # 132
                self.update_from_bytes(jt_s1_sys_pb2.EmsPVInvMeterGetAck, packet.payload)
            case 0x60, 0x60, 0x85: # 133
                self.update_from_bytes(jt_s1_sys_pb2.EmsPVInvMeterCfgSetAck, packet.payload)
            case 0x60, 0x60, 0x89: # 137
                self.update_from_bytes(jt_s1_sys_pb2.EmsParamSetAck, packet.payload)
            case 0x60, 0x60, 0x8a: # 138
                self.update_from_bytes(jt_s1_sys_pb2.EmsEnergyEfficientSetAck, packet.payload)

            case 0x60, 0x60, 0x8f: # 143
                self.update_from_bytes(jt_s1_sys_pb2.EmsTouTaskCfgAck, packet.payload)
            case 0x60, 0x60, 0x90: # 144
                self.update_from_bytes(jt_s1_sys_pb2.EmsTouTaskGetAck, packet.payload)
            case 0x60, 0x60, 0x91: # 145
                self.update_from_bytes(jt_s1_sys_pb2.EmsAllTouTaskGetAck, packet.payload)
            case 0x60, 0x60, 0x93: # 147
                self.update_from_bytes(jt_s1_sys_pb2.EmsTaskTypeEnableFlagSetAck, packet.payload)
            case 0x60, 0x60, 0x94: # 148
                self.update_from_bytes(jt_s1_sys_pb2.EmsSupplyTypeEnableFlagSetAck, packet.payload)
            case 0x60, 0x60, 0x97: # 151
                self.update_from_bytes(jt_s1_sys_pb2.PeakTaskCfgAck, packet.payload)
            case 0x60, 0x60, 0x98: # 152
                self.update_from_bytes(jt_s1_sys_pb2.EmsPeakShavingTaskGetAck, packet.payload)
            case 0x60, 0x60, 0x99: # 153
                self.update_from_bytes(jt_s1_sys_pb2.EmsAllPeakShavingTaskGetAck, packet.payload)



            # 96,209,x -
            case 0x60, 0xD1, 0x02: # 2
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingTimerTaskReport, packet.payload)
            case 0x60, 0xD1, 0x08: # 8
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingParamReport, packet.payload)
            case 0x60, 0xD1, 0x21: # 33
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingEnergyStreamReport, packet.payload)
            case 0x60, 0xD1, 0x61: # 97
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingListAck, packet.payload)
            case 0x60, 0xD1, 0x62: # 98
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingBindAck, packet.payload)
            case 0x60, 0xD1, 0x63: # 99
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingParamSetAck, packet.payload)
            case 0x60, 0xD1, 0x64: # 100
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingAppCtrlAck, packet.payload)
            case 0x60, 0xD1, 0x65: # 101
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingTimerTaskCfgAck, packet.payload)
            case 0x60, 0xD1, 0x67: # 103
                self.update_from_bytes(jt_s1_ev_pb2.EVChargingVehicleSetAck, packet.payload)

            # 96,211,x
            case 0x60, 0xD3, 0x01: # 1
                self.update_from_bytes(jt_s1_heatpump_pb2.HPUIReport, packet.payload)
            case 0x60, 0xD3, 0x02: # 2
                self.update_from_bytes(jt_s1_heatpump_pb2.HPTimerTaskReport, packet.payload)
            case 0x60, 0xD3, 0x63: # 99
                self.update_from_bytes(jt_s1_heatpump_pb2.HPParamSetAck, packet.payload)
            case 0x60, 0xD3, 0x64: # 100
                self.update_from_bytes(jt_s1_heatpump_pb2.HPParamGetAck, packet.payload)
            case 0x60, 0xD3, 0x66: # 102
                self.update_from_bytes(jt_s1_heatpump_pb2.HPTimerTaskCfgAck, packet.payload)

            # 96,212,x
            case 0x60, 0xD4, 0x02: # 2
                self.update_from_bytes(jt_s1_heatingrod_pb2.HeatingRodTimerTaskReport, packet.payload)
            case 0x60, 0xD4, 0x08: # 8
                self.update_from_bytes(jt_s1_heatingrod_pb2.HRChargingParamReport, packet.payload)
            case 0x60, 0xD4, 0x21: # 33
                self.update_from_bytes(jt_s1_heatingrod_pb2.HeatingRodEnergyStreamShow, packet.payload)
            case 0x60, 0xD4, 0x63: # 99
                self.update_from_bytes(jt_s1_heatingrod_pb2.HeatingRodParamSetAck, packet.payload)
            case 0x60, 0xD4, 0x65: # 101
                self.update_from_bytes(jt_s1_heatingrod_pb2.HeatingRodTimerTaskCfgAck, packet.payload)

            # 96,224,x
            case 0x60, 0xE0, 0x01:
                pass # self.update_from_bytes(jt_s1_ecology_dev_pb2.EcologyDevBindListReport, packet.payload)
            case 0x60, 0xE0, 0x6A:  # 36
                pass # unknown message
            case 0x60, 0xE0, 0x6A: # 106
                pass # self.update_from_bytes(jt_s1_ecology_dev_pb2.EcologyDevBindAck, packet.payload)
            case 0x60, 0xE0, 0x6B: # 107
                pass # self.update_from_bytes(jt_s1_ecology_dev_pb2.EcologyDevGetAck, packet.payload)

            # 96,225,x
            case 0x60, 0xE1, 0x61: # 97
                self.update_from_bytes(jt_parallel_lan_pb2.ScanParallelDevListAck, packet.payload)
            case 0x60, 0xE1, 0x62: # 98
                self.update_from_bytes(jt_parallel_lan_pb2.BindParallelDevAck, packet.payload)

            # 96,240,x
            case 0x60, 0xF0, 0x02: # 2
                pass # self.update_from_bytes(jt_s1_edev_pb2.EDevPriorityListReport, packet.payload)
            case 0x60, 0xF0, 0x61: # 97
                self.update_from_bytes(jt_s1_edev_pb2.EDevGetAck, packet.payload)
            case 0x60, 0xF0, 0x62: # 98
                self.update_from_bytes(jt_s1_edev_pb2.EDevBindAck, packet.payload)
            case 0x60, 0xF0, 0x63: # 99
                self.update_from_bytes(jt_s1_edev_pb2.EDevPriorityListSetAck, packet.payload)

            # 96,241,x
            case 0x60, 0xF1, 0x01:
                pass # self.update_from_bytes(jt_s1_edev_pb2.EDevBindListReport, packet.payload)
            case 0x60, 0xF1, 0x03: # 3
                self.update_from_bytes(jt_s1_edev_convert_pb2.EDevParamReport, packet.payload)
            case 0x60, 0xF1, 0x04: # 4
                self.update_from_bytes(jt_s1_edev_pb2.EDevTimerTaskReport, packet.payload)
            case 0x60, 0xF1, 0x21:  # 33
                self.update_from_bytes(jt_s1_edev_pb2.EDevEnergyStreamShow, packet.payload)
            case 0x60, 0xF1, 0x64: # 100
                self.update_from_bytes(jt_s1_edev_pb2.EDevOnOffSetAck, packet.payload)
            case 0x60, 0xF1, 0x65:  # 101
                self.update_from_bytes(jt_s1_edev_pb2.EDevModeSetAck, packet.payload)
            case 0x60, 0xF1, 0x66:  # 102
                self.update_from_bytes(jt_s1_edev_convert_pb2.EDevParamSetAck, packet.payload)
            case 0x60, 0xF1, 0x6A:  # 106
                self.update_from_bytes(jt_s1_edev_pb2.EDevTimerTaskCfgSetAck, packet.payload)
            case 0x60, 0xF1, 0x6C: # 108
                self.update_from_bytes(jt_s1_edev_convert_pb2.EDevExpendCtrlAck, packet.payload)
            case 0x60, 0xF1, 0x71:  # 113
                self.update_from_bytes(jt_s1_edev_convert_pb2.BatchBindAck, packet.payload)

            # 3,50,x
            case 0x03,0x32,0x62: # 98
                pass # EcoPacket ??

            case _:
                self._logger.info("Unprocessed packet sss: src=%d,cmdSet=%d,cmdId=%d: Packet=%s", packet.src, packet.cmdSet, packet.cmdId, packet)

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed

