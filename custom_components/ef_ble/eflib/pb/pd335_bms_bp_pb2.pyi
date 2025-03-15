from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

APP_AUTO_SET: AppDateType
APP_MANUAL_SET: AppDateType
BMS_AUTO_SET: AppDateType
DESCRIPTOR: _descriptor.FileDescriptor
HAS_RESET_VAL: BpResetType
MASTER_RESET: BpResetType
NEED_RESET_VAL: BpResetType
NONE_RESET_VAL: BpResetType
NONE_SET: AppDateType

class AppRuquestBpEuLawData(_message.Message):
    __slots__ = [
        "app_launch_date_set_type",
        "app_to_bms_launch_date",
        "app_to_bms_reset_flag",
        "bms_data_upload_en",
        "pack_sn",
    ]
    APP_LAUNCH_DATE_SET_TYPE_FIELD_NUMBER: _ClassVar[int]
    APP_TO_BMS_LAUNCH_DATE_FIELD_NUMBER: _ClassVar[int]
    APP_TO_BMS_RESET_FLAG_FIELD_NUMBER: _ClassVar[int]
    BMS_DATA_UPLOAD_EN_FIELD_NUMBER: _ClassVar[int]
    PACK_SN_FIELD_NUMBER: _ClassVar[int]
    app_launch_date_set_type: int
    app_to_bms_launch_date: int
    app_to_bms_reset_flag: int
    bms_data_upload_en: int
    pack_sn: str
    def __init__(
        self,
        pack_sn: _Optional[str] = ...,
        app_to_bms_launch_date: _Optional[int] = ...,
        app_launch_date_set_type: _Optional[int] = ...,
        app_to_bms_reset_flag: _Optional[int] = ...,
        bms_data_upload_en: _Optional[int] = ...,
    ) -> None: ...

class AppRuquestBpEuLawDataAck(_message.Message):
    __slots__ = [
        "accu_chg_cap",
        "accu_chg_energy",
        "accu_dsg_cap",
        "accu_dsg_energy",
        "bms_sn",
        "bp_cycles",
        "bp_launch_date",
        "bp_launch_date_flag",
        "bp_ohm_res",
        "bp_power_capability",
        "bp_reset_flag",
        "bp_round_trip_eff",
        "bp_self_dsg_rate",
        "deep_dsg_cnt",
        "high_temp_chg_time",
        "high_temp_use_time",
        "low_temp_chg_time",
        "low_temp_use_time",
        "num",
        "soh",
    ]
    ACCU_CHG_CAP_FIELD_NUMBER: _ClassVar[int]
    ACCU_CHG_ENERGY_FIELD_NUMBER: _ClassVar[int]
    ACCU_DSG_CAP_FIELD_NUMBER: _ClassVar[int]
    ACCU_DSG_ENERGY_FIELD_NUMBER: _ClassVar[int]
    BMS_SN_FIELD_NUMBER: _ClassVar[int]
    BP_CYCLES_FIELD_NUMBER: _ClassVar[int]
    BP_LAUNCH_DATE_FIELD_NUMBER: _ClassVar[int]
    BP_LAUNCH_DATE_FLAG_FIELD_NUMBER: _ClassVar[int]
    BP_OHM_RES_FIELD_NUMBER: _ClassVar[int]
    BP_POWER_CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    BP_RESET_FLAG_FIELD_NUMBER: _ClassVar[int]
    BP_ROUND_TRIP_EFF_FIELD_NUMBER: _ClassVar[int]
    BP_SELF_DSG_RATE_FIELD_NUMBER: _ClassVar[int]
    DEEP_DSG_CNT_FIELD_NUMBER: _ClassVar[int]
    HIGH_TEMP_CHG_TIME_FIELD_NUMBER: _ClassVar[int]
    HIGH_TEMP_USE_TIME_FIELD_NUMBER: _ClassVar[int]
    LOW_TEMP_CHG_TIME_FIELD_NUMBER: _ClassVar[int]
    LOW_TEMP_USE_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    SOH_FIELD_NUMBER: _ClassVar[int]
    accu_chg_cap: int
    accu_chg_energy: int
    accu_dsg_cap: int
    accu_dsg_energy: int
    bms_sn: str
    bp_cycles: int
    bp_launch_date: int
    bp_launch_date_flag: AppDateType
    bp_ohm_res: float
    bp_power_capability: float
    bp_reset_flag: BpResetType
    bp_round_trip_eff: float
    bp_self_dsg_rate: float
    deep_dsg_cnt: int
    high_temp_chg_time: int
    high_temp_use_time: int
    low_temp_chg_time: int
    low_temp_use_time: int
    num: int
    soh: int
    def __init__(
        self,
        bms_sn: _Optional[str] = ...,
        soh: _Optional[int] = ...,
        accu_chg_cap: _Optional[int] = ...,
        accu_dsg_cap: _Optional[int] = ...,
        accu_chg_energy: _Optional[int] = ...,
        accu_dsg_energy: _Optional[int] = ...,
        deep_dsg_cnt: _Optional[int] = ...,
        high_temp_use_time: _Optional[int] = ...,
        low_temp_use_time: _Optional[int] = ...,
        high_temp_chg_time: _Optional[int] = ...,
        low_temp_chg_time: _Optional[int] = ...,
        bp_launch_date: _Optional[int] = ...,
        bp_cycles: _Optional[int] = ...,
        bp_power_capability: _Optional[float] = ...,
        bp_round_trip_eff: _Optional[float] = ...,
        bp_self_dsg_rate: _Optional[float] = ...,
        bp_ohm_res: _Optional[float] = ...,
        bp_reset_flag: _Optional[_Union[BpResetType, str]] = ...,
        bp_launch_date_flag: _Optional[_Union[AppDateType, str]] = ...,
        num: _Optional[int] = ...,
    ) -> None: ...

class BMSHeartBeatReport(_message.Message):
    __slots__ = [
        "accu_chg_cap",
        "accu_chg_energy",
        "accu_dsg_cap",
        "accu_dsg_energy",
        "act_soc",
        "afe_sys_status",
        "all_bms_fault",
        "all_err_code",
        "amp",
        "balance_cmd",
        "balance_state",
        "bms_alarm_state1",
        "bms_alarm_state2",
        "bms_fault",
        "bms_fault_state",
        "bms_heartbeat_ver",
        "bms_protect_state1",
        "bms_protect_state2",
        "bms_sn",
        "bq_sys_stat_reg",
        "calendar_soh",
        "cell_id",
        "cell_ntc_num",
        "cell_series_num",
        "cell_temp",
        "cell_vol",
        "chg_dsg_state",
        "cur_sensor_ntc_num",
        "cur_sensor_temp",
        "cycle_soh",
        "cycles",
        "design_cap",
        "diff_soc",
        "ecloud_ocv",
        "env_ntc_num",
        "env_temp",
        "err_code",
        "f32_show_soc",
        "full_cap",
        "heatfilm_ntc_num",
        "heatfilm_temp",
        "hw_ver",
        "input_watts",
        "max_cell_temp",
        "max_cell_vol",
        "max_cur_sensor_temp",
        "max_env_temp",
        "max_heatfilm_temp",
        "max_mos_temp",
        "max_vol_diff",
        "mcu_pin_in_status",
        "mcu_pin_out_status",
        "min_cell_temp",
        "min_cell_vol",
        "min_cur_sensor_temp",
        "min_env_temp",
        "min_heatfilm_temp",
        "min_mos_temp",
        "mos_ntc_num",
        "mos_state",
        "mos_temp",
        "num",
        "open_bms_flag",
        "output_watts",
        "pack_sn",
        "product_detail",
        "product_type",
        "real_soh",
        "remain_balance_time",
        "remain_cap",
        "remain_time",
        "soc",
        "soh",
        "sys_loader_ver",
        "sys_state",
        "sys_ver",
        "tag_chg_amp",
        "target_soc",
        "temp",
        "type",
        "vol",
        "water_in_flag",
    ]
    ACCU_CHG_CAP_FIELD_NUMBER: _ClassVar[int]
    ACCU_CHG_ENERGY_FIELD_NUMBER: _ClassVar[int]
    ACCU_DSG_CAP_FIELD_NUMBER: _ClassVar[int]
    ACCU_DSG_ENERGY_FIELD_NUMBER: _ClassVar[int]
    ACT_SOC_FIELD_NUMBER: _ClassVar[int]
    AFE_SYS_STATUS_FIELD_NUMBER: _ClassVar[int]
    ALL_BMS_FAULT_FIELD_NUMBER: _ClassVar[int]
    ALL_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    AMP_FIELD_NUMBER: _ClassVar[int]
    BALANCE_CMD_FIELD_NUMBER: _ClassVar[int]
    BALANCE_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_ALARM_STATE1_FIELD_NUMBER: _ClassVar[int]
    BMS_ALARM_STATE2_FIELD_NUMBER: _ClassVar[int]
    BMS_FAULT_FIELD_NUMBER: _ClassVar[int]
    BMS_FAULT_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_HEARTBEAT_VER_FIELD_NUMBER: _ClassVar[int]
    BMS_PROTECT_STATE1_FIELD_NUMBER: _ClassVar[int]
    BMS_PROTECT_STATE2_FIELD_NUMBER: _ClassVar[int]
    BMS_SN_FIELD_NUMBER: _ClassVar[int]
    BQ_SYS_STAT_REG_FIELD_NUMBER: _ClassVar[int]
    CALENDAR_SOH_FIELD_NUMBER: _ClassVar[int]
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    CELL_NTC_NUM_FIELD_NUMBER: _ClassVar[int]
    CELL_SERIES_NUM_FIELD_NUMBER: _ClassVar[int]
    CELL_TEMP_FIELD_NUMBER: _ClassVar[int]
    CELL_VOL_FIELD_NUMBER: _ClassVar[int]
    CHG_DSG_STATE_FIELD_NUMBER: _ClassVar[int]
    CUR_SENSOR_NTC_NUM_FIELD_NUMBER: _ClassVar[int]
    CUR_SENSOR_TEMP_FIELD_NUMBER: _ClassVar[int]
    CYCLES_FIELD_NUMBER: _ClassVar[int]
    CYCLE_SOH_FIELD_NUMBER: _ClassVar[int]
    DESIGN_CAP_FIELD_NUMBER: _ClassVar[int]
    DIFF_SOC_FIELD_NUMBER: _ClassVar[int]
    ECLOUD_OCV_FIELD_NUMBER: _ClassVar[int]
    ENV_NTC_NUM_FIELD_NUMBER: _ClassVar[int]
    ENV_TEMP_FIELD_NUMBER: _ClassVar[int]
    ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    F32_SHOW_SOC_FIELD_NUMBER: _ClassVar[int]
    FULL_CAP_FIELD_NUMBER: _ClassVar[int]
    HEATFILM_NTC_NUM_FIELD_NUMBER: _ClassVar[int]
    HEATFILM_TEMP_FIELD_NUMBER: _ClassVar[int]
    HW_VER_FIELD_NUMBER: _ClassVar[int]
    INPUT_WATTS_FIELD_NUMBER: _ClassVar[int]
    MAX_CELL_TEMP_FIELD_NUMBER: _ClassVar[int]
    MAX_CELL_VOL_FIELD_NUMBER: _ClassVar[int]
    MAX_CUR_SENSOR_TEMP_FIELD_NUMBER: _ClassVar[int]
    MAX_ENV_TEMP_FIELD_NUMBER: _ClassVar[int]
    MAX_HEATFILM_TEMP_FIELD_NUMBER: _ClassVar[int]
    MAX_MOS_TEMP_FIELD_NUMBER: _ClassVar[int]
    MAX_VOL_DIFF_FIELD_NUMBER: _ClassVar[int]
    MCU_PIN_IN_STATUS_FIELD_NUMBER: _ClassVar[int]
    MCU_PIN_OUT_STATUS_FIELD_NUMBER: _ClassVar[int]
    MIN_CELL_TEMP_FIELD_NUMBER: _ClassVar[int]
    MIN_CELL_VOL_FIELD_NUMBER: _ClassVar[int]
    MIN_CUR_SENSOR_TEMP_FIELD_NUMBER: _ClassVar[int]
    MIN_ENV_TEMP_FIELD_NUMBER: _ClassVar[int]
    MIN_HEATFILM_TEMP_FIELD_NUMBER: _ClassVar[int]
    MIN_MOS_TEMP_FIELD_NUMBER: _ClassVar[int]
    MOS_NTC_NUM_FIELD_NUMBER: _ClassVar[int]
    MOS_STATE_FIELD_NUMBER: _ClassVar[int]
    MOS_TEMP_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    OPEN_BMS_FLAG_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_WATTS_FIELD_NUMBER: _ClassVar[int]
    PACK_SN_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_DETAIL_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_TYPE_FIELD_NUMBER: _ClassVar[int]
    REAL_SOH_FIELD_NUMBER: _ClassVar[int]
    REMAIN_BALANCE_TIME_FIELD_NUMBER: _ClassVar[int]
    REMAIN_CAP_FIELD_NUMBER: _ClassVar[int]
    REMAIN_TIME_FIELD_NUMBER: _ClassVar[int]
    SOC_FIELD_NUMBER: _ClassVar[int]
    SOH_FIELD_NUMBER: _ClassVar[int]
    SYS_LOADER_VER_FIELD_NUMBER: _ClassVar[int]
    SYS_STATE_FIELD_NUMBER: _ClassVar[int]
    SYS_VER_FIELD_NUMBER: _ClassVar[int]
    TAG_CHG_AMP_FIELD_NUMBER: _ClassVar[int]
    TARGET_SOC_FIELD_NUMBER: _ClassVar[int]
    TEMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VOL_FIELD_NUMBER: _ClassVar[int]
    WATER_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    accu_chg_cap: int
    accu_chg_energy: int
    accu_dsg_cap: int
    accu_dsg_energy: int
    act_soc: float
    afe_sys_status: int
    all_bms_fault: int
    all_err_code: int
    amp: int
    balance_cmd: int
    balance_state: int
    bms_alarm_state1: int
    bms_alarm_state2: int
    bms_fault: int
    bms_fault_state: int
    bms_heartbeat_ver: int
    bms_protect_state1: int
    bms_protect_state2: int
    bms_sn: str
    bq_sys_stat_reg: int
    calendar_soh: float
    cell_id: int
    cell_ntc_num: int
    cell_series_num: int
    cell_temp: _containers.RepeatedScalarFieldContainer[int]
    cell_vol: _containers.RepeatedScalarFieldContainer[int]
    chg_dsg_state: int
    cur_sensor_ntc_num: int
    cur_sensor_temp: _containers.RepeatedScalarFieldContainer[int]
    cycle_soh: float
    cycles: int
    design_cap: int
    diff_soc: float
    ecloud_ocv: int
    env_ntc_num: int
    env_temp: _containers.RepeatedScalarFieldContainer[int]
    err_code: int
    f32_show_soc: float
    full_cap: int
    heatfilm_ntc_num: int
    heatfilm_temp: _containers.RepeatedScalarFieldContainer[int]
    hw_ver: str
    input_watts: int
    max_cell_temp: int
    max_cell_vol: int
    max_cur_sensor_temp: int
    max_env_temp: int
    max_heatfilm_temp: int
    max_mos_temp: int
    max_vol_diff: int
    mcu_pin_in_status: int
    mcu_pin_out_status: int
    min_cell_temp: int
    min_cell_vol: int
    min_cur_sensor_temp: int
    min_env_temp: int
    min_heatfilm_temp: int
    min_mos_temp: int
    mos_ntc_num: int
    mos_state: int
    mos_temp: _containers.RepeatedScalarFieldContainer[int]
    num: int
    open_bms_flag: int
    output_watts: int
    pack_sn: str
    product_detail: int
    product_type: int
    real_soh: float
    remain_balance_time: _containers.RepeatedScalarFieldContainer[int]
    remain_cap: int
    remain_time: int
    soc: int
    soh: int
    sys_loader_ver: int
    sys_state: int
    sys_ver: int
    tag_chg_amp: int
    target_soc: float
    temp: int
    type: int
    vol: int
    water_in_flag: int
    def __init__(
        self,
        num: _Optional[int] = ...,
        type: _Optional[int] = ...,
        cell_id: _Optional[int] = ...,
        err_code: _Optional[int] = ...,
        sys_ver: _Optional[int] = ...,
        soc: _Optional[int] = ...,
        vol: _Optional[int] = ...,
        amp: _Optional[int] = ...,
        temp: _Optional[int] = ...,
        open_bms_flag: _Optional[int] = ...,
        design_cap: _Optional[int] = ...,
        remain_cap: _Optional[int] = ...,
        full_cap: _Optional[int] = ...,
        cycles: _Optional[int] = ...,
        soh: _Optional[int] = ...,
        max_cell_vol: _Optional[int] = ...,
        min_cell_vol: _Optional[int] = ...,
        max_cell_temp: _Optional[int] = ...,
        min_cell_temp: _Optional[int] = ...,
        max_mos_temp: _Optional[int] = ...,
        min_mos_temp: _Optional[int] = ...,
        bms_fault: _Optional[int] = ...,
        bq_sys_stat_reg: _Optional[int] = ...,
        tag_chg_amp: _Optional[int] = ...,
        f32_show_soc: _Optional[float] = ...,
        input_watts: _Optional[int] = ...,
        output_watts: _Optional[int] = ...,
        remain_time: _Optional[int] = ...,
        mos_state: _Optional[int] = ...,
        balance_state: _Optional[int] = ...,
        max_vol_diff: _Optional[int] = ...,
        cell_series_num: _Optional[int] = ...,
        cell_vol: _Optional[_Iterable[int]] = ...,
        cell_ntc_num: _Optional[int] = ...,
        cell_temp: _Optional[_Iterable[int]] = ...,
        hw_ver: _Optional[str] = ...,
        bms_heartbeat_ver: _Optional[int] = ...,
        ecloud_ocv: _Optional[int] = ...,
        bms_sn: _Optional[str] = ...,
        product_type: _Optional[int] = ...,
        product_detail: _Optional[int] = ...,
        act_soc: _Optional[float] = ...,
        diff_soc: _Optional[float] = ...,
        target_soc: _Optional[float] = ...,
        sys_loader_ver: _Optional[int] = ...,
        sys_state: _Optional[int] = ...,
        chg_dsg_state: _Optional[int] = ...,
        all_err_code: _Optional[int] = ...,
        all_bms_fault: _Optional[int] = ...,
        accu_chg_cap: _Optional[int] = ...,
        accu_dsg_cap: _Optional[int] = ...,
        real_soh: _Optional[float] = ...,
        calendar_soh: _Optional[float] = ...,
        cycle_soh: _Optional[float] = ...,
        mos_ntc_num: _Optional[int] = ...,
        mos_temp: _Optional[_Iterable[int]] = ...,
        env_ntc_num: _Optional[int] = ...,
        env_temp: _Optional[_Iterable[int]] = ...,
        heatfilm_ntc_num: _Optional[int] = ...,
        heatfilm_temp: _Optional[_Iterable[int]] = ...,
        cur_sensor_ntc_num: _Optional[int] = ...,
        cur_sensor_temp: _Optional[_Iterable[int]] = ...,
        max_env_temp: _Optional[int] = ...,
        min_env_temp: _Optional[int] = ...,
        max_heatfilm_temp: _Optional[int] = ...,
        min_heatfilm_temp: _Optional[int] = ...,
        max_cur_sensor_temp: _Optional[int] = ...,
        min_cur_sensor_temp: _Optional[int] = ...,
        balance_cmd: _Optional[int] = ...,
        remain_balance_time: _Optional[_Iterable[int]] = ...,
        afe_sys_status: _Optional[int] = ...,
        mcu_pin_in_status: _Optional[int] = ...,
        mcu_pin_out_status: _Optional[int] = ...,
        bms_alarm_state1: _Optional[int] = ...,
        bms_alarm_state2: _Optional[int] = ...,
        bms_protect_state1: _Optional[int] = ...,
        bms_protect_state2: _Optional[int] = ...,
        bms_fault_state: _Optional[int] = ...,
        accu_chg_energy: _Optional[int] = ...,
        accu_dsg_energy: _Optional[int] = ...,
        pack_sn: _Optional[str] = ...,
        water_in_flag: _Optional[int] = ...,
    ) -> None: ...

class CMSHeartBeatReport(_message.Message):
    __slots__ = ["v1p0", "v1p3"]
    V1P0_FIELD_NUMBER: _ClassVar[int]
    V1P3_FIELD_NUMBER: _ClassVar[int]
    v1p0: ems_heartbeat_pack_v1p0_t
    v1p3: ems_heartbeat_pack_v1p3_t
    def __init__(
        self,
        v1p0: _Optional[_Union[ems_heartbeat_pack_v1p0_t, _Mapping]] = ...,
        v1p3: _Optional[_Union[ems_heartbeat_pack_v1p3_t, _Mapping]] = ...,
    ) -> None: ...

class ems_heartbeat_pack_v1p0_t(_message.Message):
    __slots__ = [
        "bms_is_connt",
        "bms_model",
        "bms_warning_state",
        "chg_amp",
        "chg_cmd",
        "chg_remain_time",
        "chg_state",
        "chg_vol",
        "dsg_cmd",
        "dsg_remain_time",
        "ems_is_normal_flag",
        "f32_lcd_show_soc",
        "fan_level",
        "lcd_show_soc",
        "max_available_num",
        "max_charge_soc",
        "max_close_oil_eb_soc",
        "min_dsg_soc",
        "min_open_oil_eb_soc",
        "open_bms_idx",
        "open_ups_flag",
        "para_vol_max",
        "para_vol_min",
    ]
    BMS_IS_CONNT_FIELD_NUMBER: _ClassVar[int]
    BMS_MODEL_FIELD_NUMBER: _ClassVar[int]
    BMS_WARNING_STATE_FIELD_NUMBER: _ClassVar[int]
    CHG_AMP_FIELD_NUMBER: _ClassVar[int]
    CHG_CMD_FIELD_NUMBER: _ClassVar[int]
    CHG_REMAIN_TIME_FIELD_NUMBER: _ClassVar[int]
    CHG_STATE_FIELD_NUMBER: _ClassVar[int]
    CHG_VOL_FIELD_NUMBER: _ClassVar[int]
    DSG_CMD_FIELD_NUMBER: _ClassVar[int]
    DSG_REMAIN_TIME_FIELD_NUMBER: _ClassVar[int]
    EMS_IS_NORMAL_FLAG_FIELD_NUMBER: _ClassVar[int]
    F32_LCD_SHOW_SOC_FIELD_NUMBER: _ClassVar[int]
    FAN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LCD_SHOW_SOC_FIELD_NUMBER: _ClassVar[int]
    MAX_AVAILABLE_NUM_FIELD_NUMBER: _ClassVar[int]
    MAX_CHARGE_SOC_FIELD_NUMBER: _ClassVar[int]
    MAX_CLOSE_OIL_EB_SOC_FIELD_NUMBER: _ClassVar[int]
    MIN_DSG_SOC_FIELD_NUMBER: _ClassVar[int]
    MIN_OPEN_OIL_EB_SOC_FIELD_NUMBER: _ClassVar[int]
    OPEN_BMS_IDX_FIELD_NUMBER: _ClassVar[int]
    OPEN_UPS_FLAG_FIELD_NUMBER: _ClassVar[int]
    PARA_VOL_MAX_FIELD_NUMBER: _ClassVar[int]
    PARA_VOL_MIN_FIELD_NUMBER: _ClassVar[int]
    bms_is_connt: _containers.RepeatedScalarFieldContainer[int]
    bms_model: int
    bms_warning_state: int
    chg_amp: int
    chg_cmd: int
    chg_remain_time: int
    chg_state: int
    chg_vol: int
    dsg_cmd: int
    dsg_remain_time: int
    ems_is_normal_flag: int
    f32_lcd_show_soc: float
    fan_level: int
    lcd_show_soc: int
    max_available_num: int
    max_charge_soc: int
    max_close_oil_eb_soc: int
    min_dsg_soc: int
    min_open_oil_eb_soc: int
    open_bms_idx: int
    open_ups_flag: int
    para_vol_max: int
    para_vol_min: int
    def __init__(
        self,
        chg_state: _Optional[int] = ...,
        chg_cmd: _Optional[int] = ...,
        dsg_cmd: _Optional[int] = ...,
        chg_vol: _Optional[int] = ...,
        chg_amp: _Optional[int] = ...,
        fan_level: _Optional[int] = ...,
        max_charge_soc: _Optional[int] = ...,
        bms_model: _Optional[int] = ...,
        lcd_show_soc: _Optional[int] = ...,
        open_ups_flag: _Optional[int] = ...,
        bms_warning_state: _Optional[int] = ...,
        chg_remain_time: _Optional[int] = ...,
        dsg_remain_time: _Optional[int] = ...,
        ems_is_normal_flag: _Optional[int] = ...,
        f32_lcd_show_soc: _Optional[float] = ...,
        bms_is_connt: _Optional[_Iterable[int]] = ...,
        max_available_num: _Optional[int] = ...,
        open_bms_idx: _Optional[int] = ...,
        para_vol_min: _Optional[int] = ...,
        para_vol_max: _Optional[int] = ...,
        min_dsg_soc: _Optional[int] = ...,
        min_open_oil_eb_soc: _Optional[int] = ...,
        max_close_oil_eb_soc: _Optional[int] = ...,
    ) -> None: ...

class ems_heartbeat_pack_v1p3_t(_message.Message):
    __slots__ = [
        "chg_disable_cond",
        "chg_line_plug_in_flag",
        "dsg_disable_cond",
        "ems_heartbeat_ver",
        "sys_chg_dsg_state",
    ]
    CHG_DISABLE_COND_FIELD_NUMBER: _ClassVar[int]
    CHG_LINE_PLUG_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    DSG_DISABLE_COND_FIELD_NUMBER: _ClassVar[int]
    EMS_HEARTBEAT_VER_FIELD_NUMBER: _ClassVar[int]
    SYS_CHG_DSG_STATE_FIELD_NUMBER: _ClassVar[int]
    chg_disable_cond: int
    chg_line_plug_in_flag: int
    dsg_disable_cond: int
    ems_heartbeat_ver: int
    sys_chg_dsg_state: int
    def __init__(
        self,
        chg_disable_cond: _Optional[int] = ...,
        dsg_disable_cond: _Optional[int] = ...,
        chg_line_plug_in_flag: _Optional[int] = ...,
        sys_chg_dsg_state: _Optional[int] = ...,
        ems_heartbeat_ver: _Optional[int] = ...,
    ) -> None: ...

class AppDateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class BpResetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
