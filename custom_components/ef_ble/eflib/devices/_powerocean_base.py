import logging
from bleak import AdvertisementData, BLEDevice
from ..packet import Packet
from custom_components.ef_ble.eflib import DeviceBase
from ..connection import ConnectionState
from ..pb import (
    iot_comm_pb2,
    jt_s1_sys_pb2,
    jt_s1_edev_pb2,
    jt_s1_ev_pb2,
    jt_s1_heatpump_pb2,
    jt_s1_heatingrod_pb2,
)

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

    # def __str__(self):
    #     return self.state_name.upper()

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

    # def __str__(self):
    #     return self.state_name.upper()

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

    # def __str__(self):
    #     return self.state_name.upper()

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
            if type == "bp_temp":
                array = getattr(item, self.type, None)
                if array is not None:
                    return array[0]
            else:
                return getattr(item, self.type, None)
        else:
            return None


class _BpHeartbeatBmsSysState(repeated_pb_field_type(pb_bp_heart.bp_heart_beat, lambda msg: msg, per_item=True)):
    idx: int

    def get_value(self, item: jt_s1_sys_pb2.BpStaReport) -> BmsSysState | None:
        if item.bp_dsrc == self.idx:
            return BmsSysState.from_mode(item.bp_sys_state)  # from_mode ?
        else:
            return None


class _BpHeartbeatBmsRunStaDef(repeated_pb_field_type(pb_bp_heart.bp_heart_beat, lambda msg: msg, per_item=True)):
    idx: int

    def get_value(self, item: jt_s1_sys_pb2.BpStaReport) -> BmsRunStaDef | None:
        if item.bp_dsrc == self.idx:
            return BmsRunStaDef.from_mode(item.bms_run_sta)  # from_mode ?
        else:
            return None


class _MpptPv(repeated_pb_field_type(pb_heartbeat.mppt_heart_beat, lambda msg: msg, per_item=True)):
    idx: int
    type: str

    def get_value(self, item: jt_s1_sys_pb2.MpptStaReport) -> float | None:
        if not item.mppt_pv:
            return None

        resolved_idx = self.idx - 1

        if (self.idx > len(item.mppt_pv)):
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

        resolved_idx = self.idx - 1

        if self.idx > len(item.energy):
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


class PowerOceanBase(DeviceBase, ProtobufProps):

    PO_INTERNAL_VERSION = "0.5.1"

    # ecr_ems_sn = pb_field(pb_error_change_report.ems_err_code.module_sn)
    # pcs_sn = pb_field(pb_error_change_report.pcs_err_code.module_sn)

    sys_load_pwr = pb_field(pb_energy_stream_report.sys_load_pwr)
    grid_power = pb_field(pb_energy_stream_report.sys_grid_pwr)  # sys_grid_pwr
    mppt_pwr = pb_field(pb_energy_stream_report.mppt_pwr)
    bp_pwr = pb_field(pb_energy_stream_report.bp_pwr)

    pv1_main_power = pb_field(pb_energy_stream_report.pv1_pwr)  # pv1_pwr
    pv2_main_power = pb_field(pb_energy_stream_report.pv2_pwr)  # pv2_pwr
    pv3_main_power = pb_field(pb_energy_stream_report.pv3_pwr)  # on Plus pv3_pwr
    pv_inv_pwr = pb_field(pb_energy_stream_report.pv_inv_pwr)

    pcs_meter_power = pb_field(pb_heartbeat.pcs_meter_power)
    ems_bp_power = pb_field(pb_heartbeat.ems_bp_power)
    pcs_act_pwr = pb_field(pb_heartbeat.pcs_act_pwr)

    # Connected devices - Battery
    bpack1_bp_amp = _BpHeartbeatFloatValue(1, 'bp_amp')
    bpack1_bp_err_code = _BpHeartbeatIntValue(1, 'bp_err_code')
    bpack1_bp_env_temp = _BpHeartbeatFloatValue(1, 'bp_env_temp')

    battery_1_max_cell_temperature = _BpHeartbeatFloatValue(1, 'bp_max_cell_temp')  # bpack1_bp_max_cell_temp
    battery_1_min_cell_temperature = _BpHeartbeatFloatValue(1, 'bp_min_cell_temp')  # bpack1_bp_min_cell_temp

    bpack1_bp_pwr = _BpHeartbeatFloatValue(1, 'bp_pwr')  # bpack1_bp_pwr
    bpack1_bp_remain_watth = _BpHeartbeatFloatValue(1, 'bp_remain_watth')  # bpack1_bp_remain_watth

    battery_1_battery_level = _BpHeartbeatIntValue(1, 'bp_soc')  # bpack1_bp_soc

    bpack1_bp_soh = _BpHeartbeatIntValue(1, 'bp_soh')  # bpack1_bp_soh
    bpack1_bp_vol = _BpHeartbeatFloatValue(1, 'bp_vol')  # bpack1_bp_vol
    bpack1_bp_cycles = _BpHeartbeatIntValue(1, 'bp_cycles')  # Diag  bpack1_bp_cycles

    battery_1_system_state = _BpHeartbeatBmsSysState(1)  # Diag  bpack1_bp_sys_state
    battery_1_bms_run_state = _BpHeartbeatBmsRunStaDef(1)  # Diag  bpack1_bms_run_sta

    bpack2_bp_amp = _BpHeartbeatFloatValue(2, 'bp_amp')
    bpack2_bp_err_code = _BpHeartbeatIntValue(2, 'bp_err_code')
    bpack2_bp_env_temp = _BpHeartbeatFloatValue(2, 'bp_env_temp')
    battery_2_max_cell_temperature = _BpHeartbeatFloatValue(2, 'bp_max_cell_temp')
    battery_2_min_cell_temperature = _BpHeartbeatFloatValue(2, 'bp_min_cell_temp')
    bpack2_bp_pwr = _BpHeartbeatFloatValue(2, 'bp_pwr')
    bpack2_bp_remain_watth = _BpHeartbeatFloatValue(2, 'bp_remain_watth')
    battery_2_battery_level = _BpHeartbeatIntValue(2, 'bp_soc')
    bpack2_bp_soh = _BpHeartbeatIntValue(2, 'bp_soh')
    bpack2_bp_vol = _BpHeartbeatFloatValue(2, 'bp_vol')
    bpack2_bp_cycles = _BpHeartbeatIntValue(2, 'bp_cycles')  # Diag
    battery_2_system_state = _BpHeartbeatBmsSysState(2)  # Diag
    battery_2_bms_run_state = _BpHeartbeatBmsRunStaDef(2)  # Diag

    bpack3_bp_amp = _BpHeartbeatFloatValue(3, 'bp_amp')
    bpack3_bp_err_code = _BpHeartbeatIntValue(3, 'bp_err_code')
    bpack3_bp_env_temp = _BpHeartbeatFloatValue(3, 'bp_env_temp')
    battery_3_max_cell_temperature = _BpHeartbeatFloatValue(3, 'bp_max_cell_temp')
    bpack3_bp_min_cell_temp = _BpHeartbeatFloatValue(3, 'bp_min_cell_temp')
    bpack3_bp_pwr = _BpHeartbeatFloatValue(3, 'bp_pwr')
    bpack3_bp_remain_watth = _BpHeartbeatFloatValue(3, 'bp_remain_watth')
    battery_3_battery_level = _BpHeartbeatIntValue(3, 'bp_soc')
    bpack3_bp_soh = _BpHeartbeatIntValue(3, 'bp_soh')
    bpack3_bp_vol = _BpHeartbeatFloatValue(3, 'bp_vol')
    bpack3_bp_cycles = _BpHeartbeatIntValue(3, 'bp_cycles')  # Diag
    battery_3_system_state = _BpHeartbeatBmsSysState(3)  # Diag
    battery_3_bms_run_state = _BpHeartbeatBmsRunStaDef(3)  # Diag

    bpack4_bp_amp = _BpHeartbeatFloatValue(4, 'bp_amp')
    bpack4_bp_err_code = _BpHeartbeatIntValue(4, 'bp_err_code')
    bpack4_bp_env_temp = _BpHeartbeatFloatValue(4, 'bp_env_temp')
    battery_4_max_cell_temperature = _BpHeartbeatFloatValue(4, 'bp_max_cell_temp')
    bpack4_bp_min_cell_temp = _BpHeartbeatFloatValue(4, 'bp_min_cell_temp')
    bpack4_bp_pwr = _BpHeartbeatFloatValue(4, 'bp_pwr')
    bpack4_bp_remain_watth = _BpHeartbeatFloatValue(4, 'bp_remain_watth')
    battery_4_battery_level = _BpHeartbeatIntValue(4, 'bp_soc')
    bpack4_bp_soh = _BpHeartbeatIntValue(4, 'bp_soh')
    bpack4_bp_vol = _BpHeartbeatFloatValue(4, 'bp_vol')
    bpack4_bp_cycles = _BpHeartbeatIntValue(4, 'bp_cycles')  # Diag
    battery_4_system_state = _BpHeartbeatBmsSysState(4)  # Diag
    battery_4_bms_run_state = _BpHeartbeatBmsRunStaDef(4)  # Diag

    bp_remain_watth = pb_field(pb_heartbeat.bp_remain_watth)

    # Connected Devices: Phases
    l1_voltage = pb_field(pb_heartbeat.pcs_a_phase.vol)  # pcs_a_phase_vol
    l1_current = pb_field(pb_heartbeat.pcs_a_phase.amp)  # pcs_a_phase_amp
    l1_active_power = pb_field(pb_heartbeat.pcs_a_phase.act_pwr)  # pcs_a_phase_act_pwr
    l1_reactive_power = pb_field(pb_heartbeat.pcs_a_phase.react_pwr)  # pcs_a_phase_react_pwr
    l1_apparent_power = pb_field(pb_heartbeat.pcs_a_phase.apparent_pwr)  # pcs_a_phase_apparent_pwr

    l2_voltage = pb_field(pb_heartbeat.pcs_b_phase.vol)
    l2_current = pb_field(pb_heartbeat.pcs_b_phase.amp)
    l2_active_power = pb_field(pb_heartbeat.pcs_b_phase.act_pwr)
    l2_reactive_power = pb_field(pb_heartbeat.pcs_b_phase.react_pwr)
    l2_apparent_power = pb_field(pb_heartbeat.pcs_b_phase.apparent_pwr)

    l3_voltage = pb_field(pb_heartbeat.pcs_c_phase.vol)
    l3_current = pb_field(pb_heartbeat.pcs_c_phase.amp)
    l3_active_power = pb_field(pb_heartbeat.pcs_c_phase.act_pwr)
    l3_reactive_power = pb_field(pb_heartbeat.pcs_c_phase.react_pwr)
    l3_apparent_power = pb_field(pb_heartbeat.pcs_c_phase.apparent_pwr)

    extra_battery_name = "PowerOcean Battery Pack"

    # todayElectricityGeneration     4.09     kWh
    # totalElectricityGeneration     14.48     kWh
    # monthElectricityGeneration     14.48     kWh
    # yearElectricityGeneration      14.48     kWh

    # String data
    pv_voltage_1 = _MpptPv(1, 'vol')
    pv_current_1 = _MpptPv(1, 'amp')  # mppt_pv1_amp
    pv_power_1 = _MpptPv(1, 'pwr')  # mppt_pv1_pwr

    pv_voltage_2 = _MpptPv(2, 'vol')
    pv_current_2 = _MpptPv(2, 'amp')
    pv_power_2 = _MpptPv(2, 'pwr')

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

        return f"PowerOcean {model}".strip()

    def __init__(
            self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)

    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    # In this method we create ignore list, to prevent any "unsupported" or "new" packets to slip through
    def isOnIgnoreList(self, packet: Packet):
        if packet.src == 0x60 and packet.cmdSet == 0x60:  # base power ocean
            return (packet.cmdId in [10, 11, 12, 13, 14, 24, 25, 26, 34, 35, 36, 41, 50, 98, 99, 100, 101, 102,
                                     103, 105, 106, 107, 109, 112, 121, 124, 125, 126, 127, 132, 133, 137, 138,
                                     143, 144, 145, 147, 148, 151, 152, 153])
        elif packet.src == 0x60 and packet.cmdSet == 0xD1:  # EV  (96,209)
            return packet.cmdId in [2, 97, 98, 99, 100, 101, 103]
        elif packet.src == 0x60 and packet.cmdSet == 0xD3:  # Heat Pump  (96,211)
            return packet.cmdId in [2, 99, 100, 102]
        elif packet.src == 0x60 and packet.cmdSet == 0xD4:  # Heating Rod  (96,212)
            return packet.cmdId in [2, 99, 101]
        elif packet.src == 0x60 and packet.cmdSet == 0xE0:  # ecology_dev (96,224)  Unknown 38
            return packet.cmdId in [1, 36, 38, 106, 107]
        elif packet.src == 0x60 and packet.cmdSet == 0xE1:  # parallel_lan (96,225)
            return packet.cmdId in [97, 98]
        elif packet.src == 0x60 and packet.cmdSet == 0xF0:  # edev (96,240)
            return packet.cmdId in [2, 97, 98, 99]
        elif packet.src == 0x60 and packet.cmdSet == 0xF1:  # edev (96,241)  Unknown 5, 36
            return packet.cmdId in [1, 3, 4, 5, 36, 100, 101, 102, 106, 108, 113]
        elif packet.src == 0x03 and packet.cmdSet == 0x32:  # eco (3,50)
            return packet.cmdId in [62]
        elif packet.src == 0x35 and packet.cmdSet == 0x35:  # 53,53
            return packet.cmdId in [13, 113, 170]
        elif packet.cmdSet == 0xFE and packet.cmdId == 0x10:  # _, 0xFE, 0x10
            return True
        else:
            return False

    async def data_parse(self, packet: Packet):
        if (state := self.connection_state) is not None and not state.authenticated:
            self._conn._set_state(ConnectionState.AUTHENTICATED)
            self._conn._connected.set()
            self._logger.info("Authenticated")

        # if not self.connection_state.authenticated:
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
                self.processEmsChangeReport(packet)
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
            # else:
            #     processed = True
        else:
            processed = True

        # TODO temporary
        # processed = False

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed


    def processEmsChangeReport(self, packet: Packet):
        pass
