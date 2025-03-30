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

AC_IN_CHG_MODE_BAT_OPTIMAL_POW: AC_IN_CHG_MODE
AC_IN_CHG_MODE_SELF_DEF_POW: AC_IN_CHG_MODE
AC_IN_CHG_MODE_SILENCE: AC_IN_CHG_MODE
DESCRIPTOR: _descriptor.FileDescriptor
INSTALLMENT_PAYMENT_OVERDUE_LIMIT_CLOSE_OUTPUT: INSTALLMENT_PAYMENT_OVERDUE_LIMIT
INSTALLMENT_PAYMENT_OVERDUE_LIMIT_NONE: INSTALLMENT_PAYMENT_OVERDUE_LIMIT
INSTALLMENT_PAYMENT_STATE_ACTIVATED: INSTALLMENT_PAYMENT_STATE
INSTALLMENT_PAYMENT_STATE_MANUAL_LOCKDOWN: INSTALLMENT_PAYMENT_STATE
INSTALLMENT_PAYMENT_STATE_OVERDUE: INSTALLMENT_PAYMENT_STATE
INSTALLMENT_PAYMENT_STATE_SETTLE: INSTALLMENT_PAYMENT_STATE
INSTALLMENT_PAYMENT_STATE_WAIT_FOT_ACTIVATE: INSTALLMENT_PAYMENT_STATE
MODULE_TYPE_EF: MODULE_TYPE
PV_CHG_VOL_SPEC_12V: PV_CHG_VOL_SPEC
PV_CHG_VOL_SPEC_24V: PV_CHG_VOL_SPEC
PV_CHG_VOL_SPEC_48V: PV_CHG_VOL_SPEC
PV_CHG_VOL_SPEC_RESV: PV_CHG_VOL_SPEC
PV_PLUG_INDEX_1: PV_PLUG_INDEX
PV_PLUG_INDEX_2: PV_PLUG_INDEX
PV_PLUG_INDEX_RESV: PV_PLUG_INDEX
SERVE_MIDDLEMEN_NONE: SERVE_MIDDLEMEN
SERVE_MIDDLEMEN_SUNNOVA: SERVE_MIDDLEMEN
SP_CHARGER_CHG_MODE_BAT_MAINTENANCE: SP_CHARGER_CHG_MODE
SP_CHARGER_CHG_MODE_DRIVING_CHG: SP_CHARGER_CHG_MODE
SP_CHARGER_CHG_MODE_IDLE: SP_CHARGER_CHG_MODE
SP_CHARGER_CHG_MODE_PARKING_CHG: SP_CHARGER_CHG_MODE
STATISTICS_OBJECT_AC_IN_0W_100W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_IN_ENERGY: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_IN_OVER_100W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_0W_50W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_100W_200W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_200W_300W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_300W_400W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_400W_500W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_50W_100W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_ENERGY: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_OVER_200W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_AC_OUT_OVER_500W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_DC12V_OUT_ENERGY: STATISTICS_OBJECT
STATISTICS_OBJECT_DC_OUT_0W_60W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_DC_OUT_OVER_60W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_DEV_WORK_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_LED_OUT_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_PV_IN_ENERGY: STATISTICS_OBJECT
STATISTICS_OBJECT_PV_IN_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_START: STATISTICS_OBJECT
STATISTICS_OBJECT_TYPEC_IN_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_TYPEC_OUT_0W_30W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_TYPEC_OUT_30W_60W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_TYPEC_OUT_ENERGY: STATISTICS_OBJECT
STATISTICS_OBJECT_TYPEC_OUT_OVER_60W_TIME: STATISTICS_OBJECT
STATISTICS_OBJECT_USBA_OUT_ENERGY: STATISTICS_OBJECT
STATISTICS_OBJECT_USBA_OUT_TIME: STATISTICS_OBJECT
TIME_TASK_DETAIL_IDLE: TIME_TASK_DETAIL_TYPE
TIME_TASK_DETAIL_LEVEL: TIME_TASK_DETAIL_TYPE
TIME_TASK_DETAIL_POW: TIME_TASK_DETAIL_TYPE
TIME_TASK_DETAIL_TEMP: TIME_TASK_DETAIL_TYPE
TIME_TASK_MODE_ONCE: TIME_TASK_MODE
TIME_TASK_MODE_PER_WEEK: TIME_TASK_MODE
TIME_TASK_MODE_RESV: TIME_TASK_MODE
TIME_TASK_TYPE_AC2_DSG: TIME_TASK_TYPE
TIME_TASK_TYPE_AC_CHG: TIME_TASK_TYPE
TIME_TASK_TYPE_AC_DSG: TIME_TASK_TYPE
TIME_TASK_TYPE_DC2_CHG: TIME_TASK_TYPE
TIME_TASK_TYPE_DC_CHG: TIME_TASK_TYPE
TIME_TASK_TYPE_DC_DSG: TIME_TASK_TYPE
TIME_TASK_TYPE_OIL_OFF: TIME_TASK_TYPE
TIME_TASK_TYPE_OIL_ON: TIME_TASK_TYPE
TIME_TASK_TYPE_USB_CHG: TIME_TASK_TYPE
TIME_TASK_TYPE_USB_DSG: TIME_TASK_TYPE

class CfgAcHvAlwaysOn(_message.Message):
    __slots__ = ["ac_always_on_mini_soc", "ac_hv_always_on"]
    AC_ALWAYS_ON_MINI_SOC_FIELD_NUMBER: _ClassVar[int]
    AC_HV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    ac_always_on_mini_soc: int
    ac_hv_always_on: bool
    def __init__(
        self, ac_hv_always_on: bool = ..., ac_always_on_mini_soc: _Optional[int] = ...
    ) -> None: ...

class CfgAcLvAlwaysOn(_message.Message):
    __slots__ = ["ac_always_on_mini_soc", "ac_lv_always_on"]
    AC_ALWAYS_ON_MINI_SOC_FIELD_NUMBER: _ClassVar[int]
    AC_LV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    ac_always_on_mini_soc: int
    ac_lv_always_on: bool
    def __init__(
        self, ac_lv_always_on: bool = ..., ac_always_on_mini_soc: _Optional[int] = ...
    ) -> None: ...

class CfgAcOutAlwaysOn(_message.Message):
    __slots__ = ["ac_always_on_flag", "ac_always_on_mini_soc"]
    AC_ALWAYS_ON_FLAG_FIELD_NUMBER: _ClassVar[int]
    AC_ALWAYS_ON_MINI_SOC_FIELD_NUMBER: _ClassVar[int]
    ac_always_on_flag: bool
    ac_always_on_mini_soc: int
    def __init__(
        self, ac_always_on_flag: bool = ..., ac_always_on_mini_soc: _Optional[int] = ...
    ) -> None: ...

class CfgBeep(_message.Message):
    __slots__ = ["beep_act_count", "beep_act_ms"]
    BEEP_ACT_COUNT_FIELD_NUMBER: _ClassVar[int]
    BEEP_ACT_MS_FIELD_NUMBER: _ClassVar[int]
    beep_act_count: int
    beep_act_ms: int
    def __init__(
        self, beep_act_count: _Optional[int] = ..., beep_act_ms: _Optional[int] = ...
    ) -> None: ...

class CfgBmsPowerOffWriteAck(_message.Message):
    __slots__ = ["bms_power_off", "bms_power_state"]
    BMS_POWER_OFF_FIELD_NUMBER: _ClassVar[int]
    BMS_POWER_STATE_FIELD_NUMBER: _ClassVar[int]
    bms_power_off: bool
    bms_power_state: int
    def __init__(
        self, bms_power_off: bool = ..., bms_power_state: _Optional[int] = ...
    ) -> None: ...

class CfgBmsPushWrite(_message.Message):
    __slots__ = [
        "bms_health_freq",
        "bms_health_open",
        "bms_heartbeap_freq",
        "bms_heartbeap_open",
    ]
    BMS_HEALTH_FREQ_FIELD_NUMBER: _ClassVar[int]
    BMS_HEALTH_OPEN_FIELD_NUMBER: _ClassVar[int]
    BMS_HEARTBEAP_FREQ_FIELD_NUMBER: _ClassVar[int]
    BMS_HEARTBEAP_OPEN_FIELD_NUMBER: _ClassVar[int]
    bms_health_freq: int
    bms_health_open: bool
    bms_heartbeap_freq: int
    bms_heartbeap_open: bool
    def __init__(
        self,
        bms_heartbeap_open: bool = ...,
        bms_health_open: bool = ...,
        bms_heartbeap_freq: _Optional[int] = ...,
        bms_health_freq: _Optional[int] = ...,
    ) -> None: ...

class CfgBmsPushWriteAck(_message.Message):
    __slots__ = ["bms_health_open", "bms_heartbeap_open"]
    BMS_HEALTH_OPEN_FIELD_NUMBER: _ClassVar[int]
    BMS_HEARTBEAP_OPEN_FIELD_NUMBER: _ClassVar[int]
    bms_health_open: bool
    bms_heartbeap_open: bool
    def __init__(
        self, bms_heartbeap_open: bool = ..., bms_health_open: bool = ...
    ) -> None: ...

class CfgEnergyBackup(_message.Message):
    __slots__ = ["energy_backup_en", "energy_backup_start_soc"]
    ENERGY_BACKUP_EN_FIELD_NUMBER: _ClassVar[int]
    ENERGY_BACKUP_START_SOC_FIELD_NUMBER: _ClassVar[int]
    energy_backup_en: bool
    energy_backup_start_soc: int
    def __init__(
        self,
        energy_backup_en: bool = ...,
        energy_backup_start_soc: _Optional[int] = ...,
    ) -> None: ...

class CfgEnergyStrategyOperateMode(_message.Message):
    __slots__ = [
        "operate_scheduled_open",
        "operate_self_powered_open",
        "operate_tou_mode_open",
    ]
    OPERATE_SCHEDULED_OPEN_FIELD_NUMBER: _ClassVar[int]
    OPERATE_SELF_POWERED_OPEN_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TOU_MODE_OPEN_FIELD_NUMBER: _ClassVar[int]
    operate_scheduled_open: bool
    operate_self_powered_open: bool
    operate_tou_mode_open: bool
    def __init__(
        self,
        operate_self_powered_open: bool = ...,
        operate_scheduled_open: bool = ...,
        operate_tou_mode_open: bool = ...,
    ) -> None: ...

class CfgGeneratorCareMode(_message.Message):
    __slots__ = ["generator_care_mode_open", "generator_care_mode_start_time"]
    GENERATOR_CARE_MODE_OPEN_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_CARE_MODE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    generator_care_mode_open: bool
    generator_care_mode_start_time: int
    def __init__(
        self,
        generator_care_mode_open: bool = ...,
        generator_care_mode_start_time: _Optional[int] = ...,
    ) -> None: ...

class CfgGeneratorMpptHybridMode(_message.Message):
    __slots__ = ["generator_pv_hybrid_mode_open", "generator_pv_hybrid_mode_soc_max"]
    GENERATOR_PV_HYBRID_MODE_OPEN_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PV_HYBRID_MODE_SOC_MAX_FIELD_NUMBER: _ClassVar[int]
    generator_pv_hybrid_mode_open: bool
    generator_pv_hybrid_mode_soc_max: int
    def __init__(
        self,
        generator_pv_hybrid_mode_open: bool = ...,
        generator_pv_hybrid_mode_soc_max: _Optional[int] = ...,
    ) -> None: ...

class CfgRj45CommcService(_message.Message):
    __slots__ = [
        "RJ45_commc_timeout",
        "RJ45_display_property_upload_period",
        "RJ45_runtime_property_upload_period",
    ]
    RJ45_COMMC_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    RJ45_DISPLAY_PROPERTY_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RJ45_RUNTIME_PROPERTY_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RJ45_commc_timeout: int
    RJ45_display_property_upload_period: int
    RJ45_runtime_property_upload_period: int
    def __init__(
        self,
        RJ45_commc_timeout: _Optional[int] = ...,
        RJ45_display_property_upload_period: _Optional[int] = ...,
        RJ45_runtime_property_upload_period: _Optional[int] = ...,
    ) -> None: ...

class CfgStormPattern(_message.Message):
    __slots__ = [
        "storm_pattern_enable",
        "storm_pattern_end_time",
        "storm_pattern_open_flag",
    ]
    STORM_PATTERN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_OPEN_FLAG_FIELD_NUMBER: _ClassVar[int]
    storm_pattern_enable: bool
    storm_pattern_end_time: int
    storm_pattern_open_flag: bool
    def __init__(
        self,
        storm_pattern_enable: bool = ...,
        storm_pattern_open_flag: bool = ...,
        storm_pattern_end_time: _Optional[int] = ...,
    ) -> None: ...

class CfgTouStrategy(_message.Message):
    __slots__ = ["tou_gird_chg_stop_soc", "tou_hours_strategy"]
    TOU_GIRD_CHG_STOP_SOC_FIELD_NUMBER: _ClassVar[int]
    TOU_HOURS_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    tou_gird_chg_stop_soc: int
    tou_hours_strategy: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        tou_hours_strategy: _Optional[_Iterable[int]] = ...,
        tou_gird_chg_stop_soc: _Optional[int] = ...,
    ) -> None: ...

class ConfigRead(_message.Message):
    __slots__ = ["action_id"]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    action_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, action_id: _Optional[_Iterable[int]] = ...) -> None: ...

class ConfigReadAck(_message.Message):
    __slots__ = [
        "cfg_utc_time",
        "cfg_utc_timezone",
        "get_bms_firm_ver",
        "get_inv_firm_ver",
        "get_iot_firm_ver",
        "get_llc_firm_ver",
        "get_mppt_firm_ver",
        "get_pd_firm_ver",
        "get_time_task_list",
        "read_time_task_v2_list",
    ]
    CFG_UTC_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    GET_BMS_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    GET_INV_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    GET_IOT_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    GET_LLC_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    GET_MPPT_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    GET_PD_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    GET_TIME_TASK_LIST_FIELD_NUMBER: _ClassVar[int]
    READ_TIME_TASK_V2_LIST_FIELD_NUMBER: _ClassVar[int]
    cfg_utc_time: int
    cfg_utc_timezone: int
    get_bms_firm_ver: int
    get_inv_firm_ver: int
    get_iot_firm_ver: int
    get_llc_firm_ver: int
    get_mppt_firm_ver: int
    get_pd_firm_ver: int
    get_time_task_list: GetAllTimeTaskReadck
    read_time_task_v2_list: TimeTaskItemV2List
    def __init__(
        self,
        cfg_utc_time: _Optional[int] = ...,
        cfg_utc_timezone: _Optional[int] = ...,
        get_time_task_list: _Optional[_Union[GetAllTimeTaskReadck, _Mapping]] = ...,
        read_time_task_v2_list: _Optional[_Union[TimeTaskItemV2List, _Mapping]] = ...,
        get_pd_firm_ver: _Optional[int] = ...,
        get_iot_firm_ver: _Optional[int] = ...,
        get_mppt_firm_ver: _Optional[int] = ...,
        get_llc_firm_ver: _Optional[int] = ...,
        get_inv_firm_ver: _Optional[int] = ...,
        get_bms_firm_ver: _Optional[int] = ...,
    ) -> None: ...

class ConfigWrite(_message.Message):
    __slots__ = [
        "active_display_property_full_upload",
        "active_runtime_property_full_upload",
        "active_selected_time_task_v2",
        "cfg_RJ45_commc_service",
        "cfg_ac_energy_saving_open",
        "cfg_ac_hv_always_on",
        "cfg_ac_in_chg_mode",
        "cfg_ac_lv_always_on",
        "cfg_ac_out_always_on",
        "cfg_ac_out_freq",
        "cfg_ac_out_open",
        "cfg_ac_standby_time",
        "cfg_backup_reverse_soc",
        "cfg_beep",
        "cfg_beep_en",
        "cfg_ble_standby_time",
        "cfg_bms_power_off",
        "cfg_bms_push",
        "cfg_bypass_out_disable",
        "cfg_cms_oil_off_soc",
        "cfg_cms_oil_on_soc",
        "cfg_cms_oil_self_start",
        "cfg_dc_12v_out_open",
        "cfg_dc_out_open",
        "cfg_dc_standby_time",
        "cfg_dev_standby_time",
        "cfg_display_property_full_upload_period",
        "cfg_display_property_incremental_upload_period",
        "cfg_energy_backup",
        "cfg_energy_strategy_operate_mode",
        "cfg_fuels_liquefied_gas_lng_uint",
        "cfg_fuels_liquefied_gas_lpg_uint",
        "cfg_fuels_liquefied_gas_type",
        "cfg_fuels_liquefied_gas_uint",
        "cfg_fuels_liquefied_gas_val",
        "cfg_generator_ac_out_pow_max",
        "cfg_generator_care_mode",
        "cfg_generator_dc_out_pow_max",
        "cfg_generator_engine_open",
        "cfg_generator_low_power_en",
        "cfg_generator_low_power_threshold",
        "cfg_generator_lpg_monitor_en",
        "cfg_generator_mppt_hybrid_mode",
        "cfg_generator_out_pow_max",
        "cfg_generator_perf_mode",
        "cfg_generator_self_on",
        "cfg_hv_ac_out_open",
        "cfg_installment_payment_serve",
        "cfg_installment_payment_serve_belone",
        "cfg_installment_payment_serve_enable",
        "cfg_lcd_light",
        "cfg_led_mode",
        "cfg_llc_GFCI_flag",
        "cfg_low_power_alarm",
        "cfg_lv_ac_out_open",
        "cfg_max_chg_soc",
        "cfg_min_dsg_soc",
        "cfg_multi_bp_chg_dsg_mode",
        "cfg_output_power_off_memory",
        "cfg_plug_in_info_5p8_chg_pow_max",
        "cfg_plug_in_info_ac_in_chg_pow_max",
        "cfg_plug_in_info_pv_dc_amp_max",
        "cfg_plug_in_info_pv_h_dc_amp_max",
        "cfg_plug_in_info_pv_l_dc_amp_max",
        "cfg_power_off",
        "cfg_power_on",
        "cfg_pv_chg_type",
        "cfg_pv_dc_chg_setting",
        "cfg_runtime_property_full_upload_period",
        "cfg_runtime_property_incremental_upload_period",
        "cfg_screen_off_time",
        "cfg_soc_cali",
        "cfg_sp_charger_car_batt_vol_setting",
        "cfg_sp_charger_chg_mode",
        "cfg_sp_charger_chg_open",
        "cfg_sp_charger_chg_pow_limit",
        "cfg_storm_pattern",
        "cfg_time_task_v2_item",
        "cfg_tou_strategy",
        "cfg_ups_alram",
        "cfg_usb_open",
        "cfg_utc_set_mode",
        "cfg_utc_time",
        "cfg_utc_timezone",
        "cfg_utc_timezone_id",
        "cfg_wireless_oil_off_soc",
        "cfg_wireless_oil_on_soc",
        "cfg_wireless_oil_self_start",
        "cfg_xboost_en",
        "reset_factory_setting",
        "reset_generator_maintence_state",
        "reset_middlemen_delivery_setting",
        "set_time_task",
    ]
    ACTIVE_DISPLAY_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_RUNTIME_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SELECTED_TIME_TASK_V2_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_ENERGY_SAVING_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_HV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_IN_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_LV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_BACKUP_REVERSE_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_FIELD_NUMBER: _ClassVar[int]
    CFG_BLE_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_BMS_POWER_OFF_FIELD_NUMBER: _ClassVar[int]
    CFG_BMS_PUSH_FIELD_NUMBER: _ClassVar[int]
    CFG_BYPASS_OUT_DISABLE_FIELD_NUMBER: _ClassVar[int]
    CFG_CMS_OIL_OFF_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_CMS_OIL_ON_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_CMS_OIL_SELF_START_FIELD_NUMBER: _ClassVar[int]
    CFG_DC_12V_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_DC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_DC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_DEV_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_DISPLAY_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_DISPLAY_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_ENERGY_BACKUP_FIELD_NUMBER: _ClassVar[int]
    CFG_ENERGY_STRATEGY_OPERATE_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_LNG_UINT_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_LPG_UINT_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_UINT_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_VAL_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_AC_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_CARE_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_DC_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_ENGINE_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_LOW_POWER_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_LOW_POWER_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_LPG_MONITOR_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_MPPT_HYBRID_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_PERF_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_SELF_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_HV_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_INSTALLMENT_PAYMENT_SERVE_BELONE_FIELD_NUMBER: _ClassVar[int]
    CFG_INSTALLMENT_PAYMENT_SERVE_ENABLE_FIELD_NUMBER: _ClassVar[int]
    CFG_INSTALLMENT_PAYMENT_SERVE_FIELD_NUMBER: _ClassVar[int]
    CFG_LCD_LIGHT_FIELD_NUMBER: _ClassVar[int]
    CFG_LED_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_LLC_GFCI_FLAG_FIELD_NUMBER: _ClassVar[int]
    CFG_LOW_POWER_ALARM_FIELD_NUMBER: _ClassVar[int]
    CFG_LV_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_MAX_CHG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_MIN_DSG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_MULTI_BP_CHG_DSG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_OUTPUT_POWER_OFF_MEMORY_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_5P8_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_AC_IN_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_H_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_L_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_OFF_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_PV_CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    CFG_PV_DC_CHG_SETTING_FIELD_NUMBER: _ClassVar[int]
    CFG_RJ45_COMMC_SERVICE_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_SCREEN_OFF_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_SOC_CALI_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CAR_BATT_VOL_SETTING_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CHG_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CHG_POW_LIMIT_FIELD_NUMBER: _ClassVar[int]
    CFG_STORM_PATTERN_FIELD_NUMBER: _ClassVar[int]
    CFG_TIME_TASK_V2_ITEM_FIELD_NUMBER: _ClassVar[int]
    CFG_TOU_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    CFG_UPS_ALRAM_FIELD_NUMBER: _ClassVar[int]
    CFG_USB_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_SET_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIMEZONE_ID_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_WIRELESS_OIL_OFF_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_WIRELESS_OIL_ON_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_WIRELESS_OIL_SELF_START_FIELD_NUMBER: _ClassVar[int]
    CFG_XBOOST_EN_FIELD_NUMBER: _ClassVar[int]
    RESET_FACTORY_SETTING_FIELD_NUMBER: _ClassVar[int]
    RESET_GENERATOR_MAINTENCE_STATE_FIELD_NUMBER: _ClassVar[int]
    RESET_MIDDLEMEN_DELIVERY_SETTING_FIELD_NUMBER: _ClassVar[int]
    SET_TIME_TASK_FIELD_NUMBER: _ClassVar[int]
    active_display_property_full_upload: bool
    active_runtime_property_full_upload: bool
    active_selected_time_task_v2: int
    cfg_RJ45_commc_service: CfgRj45CommcService
    cfg_ac_energy_saving_open: bool
    cfg_ac_hv_always_on: CfgAcHvAlwaysOn
    cfg_ac_in_chg_mode: AC_IN_CHG_MODE
    cfg_ac_lv_always_on: CfgAcLvAlwaysOn
    cfg_ac_out_always_on: CfgAcOutAlwaysOn
    cfg_ac_out_freq: int
    cfg_ac_out_open: bool
    cfg_ac_standby_time: int
    cfg_backup_reverse_soc: int
    cfg_beep: CfgBeep
    cfg_beep_en: bool
    cfg_ble_standby_time: int
    cfg_bms_power_off: bool
    cfg_bms_push: CfgBmsPushWrite
    cfg_bypass_out_disable: bool
    cfg_cms_oil_off_soc: int
    cfg_cms_oil_on_soc: int
    cfg_cms_oil_self_start: bool
    cfg_dc_12v_out_open: bool
    cfg_dc_out_open: bool
    cfg_dc_standby_time: int
    cfg_dev_standby_time: int
    cfg_display_property_full_upload_period: int
    cfg_display_property_incremental_upload_period: int
    cfg_energy_backup: CfgEnergyBackup
    cfg_energy_strategy_operate_mode: CfgEnergyStrategyOperateMode
    cfg_fuels_liquefied_gas_lng_uint: int
    cfg_fuels_liquefied_gas_lpg_uint: int
    cfg_fuels_liquefied_gas_type: int
    cfg_fuels_liquefied_gas_uint: int
    cfg_fuels_liquefied_gas_val: float
    cfg_generator_ac_out_pow_max: int
    cfg_generator_care_mode: CfgGeneratorCareMode
    cfg_generator_dc_out_pow_max: int
    cfg_generator_engine_open: int
    cfg_generator_low_power_en: bool
    cfg_generator_low_power_threshold: int
    cfg_generator_lpg_monitor_en: bool
    cfg_generator_mppt_hybrid_mode: CfgGeneratorMpptHybridMode
    cfg_generator_out_pow_max: int
    cfg_generator_perf_mode: int
    cfg_generator_self_on: bool
    cfg_hv_ac_out_open: bool
    cfg_installment_payment_serve: InstallmentPaymentServe
    cfg_installment_payment_serve_belone: InstallmentPaymentServeBelone
    cfg_installment_payment_serve_enable: bool
    cfg_lcd_light: int
    cfg_led_mode: int
    cfg_llc_GFCI_flag: bool
    cfg_low_power_alarm: int
    cfg_lv_ac_out_open: bool
    cfg_max_chg_soc: int
    cfg_min_dsg_soc: int
    cfg_multi_bp_chg_dsg_mode: int
    cfg_output_power_off_memory: bool
    cfg_plug_in_info_5p8_chg_pow_max: int
    cfg_plug_in_info_ac_in_chg_pow_max: int
    cfg_plug_in_info_pv_dc_amp_max: int
    cfg_plug_in_info_pv_h_dc_amp_max: int
    cfg_plug_in_info_pv_l_dc_amp_max: int
    cfg_power_off: bool
    cfg_power_on: bool
    cfg_pv_chg_type: int
    cfg_pv_dc_chg_setting: PvDcChgSetting
    cfg_runtime_property_full_upload_period: int
    cfg_runtime_property_incremental_upload_period: int
    cfg_screen_off_time: int
    cfg_soc_cali: int
    cfg_sp_charger_car_batt_vol_setting: int
    cfg_sp_charger_chg_mode: SP_CHARGER_CHG_MODE
    cfg_sp_charger_chg_open: bool
    cfg_sp_charger_chg_pow_limit: float
    cfg_storm_pattern: CfgStormPattern
    cfg_time_task_v2_item: TimeTaskItemV2
    cfg_tou_strategy: CfgTouStrategy
    cfg_ups_alram: bool
    cfg_usb_open: bool
    cfg_utc_set_mode: bool
    cfg_utc_time: int
    cfg_utc_timezone: int
    cfg_utc_timezone_id: str
    cfg_wireless_oil_off_soc: int
    cfg_wireless_oil_on_soc: int
    cfg_wireless_oil_self_start: bool
    cfg_xboost_en: bool
    reset_factory_setting: int
    reset_generator_maintence_state: bool
    reset_middlemen_delivery_setting: ResetMiddlemenDeliverySetting
    set_time_task: SetTimeTaskWrite
    def __init__(
        self,
        cfg_power_off: bool = ...,
        cfg_power_on: bool = ...,
        reset_factory_setting: _Optional[int] = ...,
        cfg_utc_time: _Optional[int] = ...,
        cfg_utc_timezone: _Optional[int] = ...,
        cfg_beep: _Optional[_Union[CfgBeep, _Mapping]] = ...,
        cfg_beep_en: bool = ...,
        cfg_ac_standby_time: _Optional[int] = ...,
        cfg_dc_standby_time: _Optional[int] = ...,
        cfg_screen_off_time: _Optional[int] = ...,
        cfg_dev_standby_time: _Optional[int] = ...,
        cfg_lcd_light: _Optional[int] = ...,
        cfg_hv_ac_out_open: bool = ...,
        cfg_lv_ac_out_open: bool = ...,
        cfg_ac_out_freq: _Optional[int] = ...,
        cfg_dc_12v_out_open: bool = ...,
        cfg_usb_open: bool = ...,
        cfg_dc_out_open: bool = ...,
        cfg_ac_out_always_on: _Optional[_Union[CfgAcOutAlwaysOn, _Mapping]] = ...,
        cfg_xboost_en: bool = ...,
        cfg_bypass_out_disable: bool = ...,
        cfg_bms_power_off: bool = ...,
        cfg_soc_cali: _Optional[int] = ...,
        cfg_bms_push: _Optional[_Union[CfgBmsPushWrite, _Mapping]] = ...,
        cfg_max_chg_soc: _Optional[int] = ...,
        cfg_min_dsg_soc: _Optional[int] = ...,
        set_time_task: _Optional[_Union[SetTimeTaskWrite, _Mapping]] = ...,
        cfg_energy_backup: _Optional[_Union[CfgEnergyBackup, _Mapping]] = ...,
        cfg_plug_in_info_pv_l_dc_amp_max: _Optional[int] = ...,
        cfg_plug_in_info_pv_h_dc_amp_max: _Optional[int] = ...,
        cfg_plug_in_info_ac_in_chg_pow_max: _Optional[int] = ...,
        cfg_plug_in_info_5p8_chg_pow_max: _Optional[int] = ...,
        cfg_cms_oil_self_start: bool = ...,
        cfg_cms_oil_on_soc: _Optional[int] = ...,
        cfg_cms_oil_off_soc: _Optional[int] = ...,
        cfg_llc_GFCI_flag: bool = ...,
        cfg_ac_hv_always_on: _Optional[_Union[CfgAcHvAlwaysOn, _Mapping]] = ...,
        cfg_ac_lv_always_on: _Optional[_Union[CfgAcLvAlwaysOn, _Mapping]] = ...,
        cfg_tou_strategy: _Optional[_Union[CfgTouStrategy, _Mapping]] = ...,
        cfg_ble_standby_time: _Optional[int] = ...,
        cfg_display_property_full_upload_period: _Optional[int] = ...,
        cfg_display_property_incremental_upload_period: _Optional[int] = ...,
        cfg_runtime_property_full_upload_period: _Optional[int] = ...,
        cfg_runtime_property_incremental_upload_period: _Optional[int] = ...,
        active_display_property_full_upload: bool = ...,
        active_runtime_property_full_upload: bool = ...,
        cfg_RJ45_commc_service: _Optional[_Union[CfgRj45CommcService, _Mapping]] = ...,
        cfg_ac_out_open: bool = ...,
        cfg_generator_perf_mode: _Optional[int] = ...,
        cfg_generator_engine_open: _Optional[int] = ...,
        cfg_generator_out_pow_max: _Optional[int] = ...,
        cfg_generator_ac_out_pow_max: _Optional[int] = ...,
        cfg_generator_dc_out_pow_max: _Optional[int] = ...,
        cfg_generator_self_on: bool = ...,
        reset_generator_maintence_state: bool = ...,
        cfg_fuels_liquefied_gas_type: _Optional[int] = ...,
        cfg_fuels_liquefied_gas_uint: _Optional[int] = ...,
        cfg_fuels_liquefied_gas_val: _Optional[float] = ...,
        cfg_plug_in_info_pv_dc_amp_max: _Optional[int] = ...,
        cfg_ups_alram: bool = ...,
        cfg_led_mode: _Optional[int] = ...,
        cfg_pv_chg_type: _Optional[int] = ...,
        cfg_low_power_alarm: _Optional[int] = ...,
        cfg_storm_pattern: _Optional[_Union[CfgStormPattern, _Mapping]] = ...,
        cfg_generator_mppt_hybrid_mode: _Optional[
            _Union[CfgGeneratorMpptHybridMode, _Mapping]
        ] = ...,
        cfg_generator_care_mode: _Optional[
            _Union[CfgGeneratorCareMode, _Mapping]
        ] = ...,
        cfg_ac_energy_saving_open: bool = ...,
        cfg_multi_bp_chg_dsg_mode: _Optional[int] = ...,
        cfg_backup_reverse_soc: _Optional[int] = ...,
        cfg_energy_strategy_operate_mode: _Optional[
            _Union[CfgEnergyStrategyOperateMode, _Mapping]
        ] = ...,
        cfg_sp_charger_chg_mode: _Optional[_Union[SP_CHARGER_CHG_MODE, str]] = ...,
        cfg_installment_payment_serve_enable: bool = ...,
        cfg_installment_payment_serve_belone: _Optional[
            _Union[InstallmentPaymentServeBelone, _Mapping]
        ] = ...,
        cfg_installment_payment_serve: _Optional[
            _Union[InstallmentPaymentServe, _Mapping]
        ] = ...,
        cfg_sp_charger_chg_open: bool = ...,
        cfg_sp_charger_chg_pow_limit: _Optional[float] = ...,
        reset_middlemen_delivery_setting: _Optional[
            _Union[ResetMiddlemenDeliverySetting, _Mapping]
        ] = ...,
        cfg_ac_in_chg_mode: _Optional[_Union[AC_IN_CHG_MODE, str]] = ...,
        cfg_pv_dc_chg_setting: _Optional[_Union[PvDcChgSetting, _Mapping]] = ...,
        cfg_time_task_v2_item: _Optional[_Union[TimeTaskItemV2, _Mapping]] = ...,
        active_selected_time_task_v2: _Optional[int] = ...,
        cfg_generator_low_power_en: bool = ...,
        cfg_generator_low_power_threshold: _Optional[int] = ...,
        cfg_generator_lpg_monitor_en: bool = ...,
        cfg_fuels_liquefied_gas_lpg_uint: _Optional[int] = ...,
        cfg_fuels_liquefied_gas_lng_uint: _Optional[int] = ...,
        cfg_utc_timezone_id: _Optional[str] = ...,
        cfg_utc_set_mode: bool = ...,
        cfg_sp_charger_car_batt_vol_setting: _Optional[int] = ...,
        cfg_wireless_oil_self_start: bool = ...,
        cfg_wireless_oil_on_soc: _Optional[int] = ...,
        cfg_wireless_oil_off_soc: _Optional[int] = ...,
        cfg_output_power_off_memory: bool = ...,
    ) -> None: ...

class ConfigWriteAck(_message.Message):
    __slots__ = [
        "action_id",
        "active_display_property_full_upload",
        "active_runtime_property_full_upload",
        "active_selected_time_task_v2",
        "cfg_RJ45_commc_service",
        "cfg_ac_energy_saving_open",
        "cfg_ac_hv_always_on",
        "cfg_ac_in_chg_mode",
        "cfg_ac_lv_always_on",
        "cfg_ac_out_always_on",
        "cfg_ac_out_freq",
        "cfg_ac_out_open",
        "cfg_ac_standby_time",
        "cfg_backup_reverse_soc",
        "cfg_beep",
        "cfg_beep_en",
        "cfg_ble_standby_time",
        "cfg_bms_power_off",
        "cfg_bms_push",
        "cfg_bypass_out_disable",
        "cfg_cms_oil_off_soc",
        "cfg_cms_oil_on_soc",
        "cfg_cms_oil_self_start",
        "cfg_dc_12v_out_open",
        "cfg_dc_out_open",
        "cfg_dc_standby_time",
        "cfg_dev_standby_time",
        "cfg_display_property_full_upload_period",
        "cfg_display_property_incremental_upload_period",
        "cfg_energy_backup",
        "cfg_energy_strategy_operate_mode",
        "cfg_fuels_liquefied_gas_lng_uint",
        "cfg_fuels_liquefied_gas_lpg_uint",
        "cfg_fuels_liquefied_gas_type",
        "cfg_fuels_liquefied_gas_uint",
        "cfg_fuels_liquefied_gas_val",
        "cfg_generator_ac_out_pow_max",
        "cfg_generator_care_mode",
        "cfg_generator_dc_out_pow_max",
        "cfg_generator_engine_open",
        "cfg_generator_low_power_en",
        "cfg_generator_low_power_threshold",
        "cfg_generator_lpg_monitor_en",
        "cfg_generator_mppt_hybrid_mode",
        "cfg_generator_out_pow_max",
        "cfg_generator_perf_mode",
        "cfg_generator_self_on",
        "cfg_hv_ac_out_open",
        "cfg_installment_payment_serve",
        "cfg_installment_payment_serve_belone",
        "cfg_installment_payment_serve_enable",
        "cfg_lcd_light",
        "cfg_led_mode",
        "cfg_llc_GFCI_flag",
        "cfg_low_power_alarm",
        "cfg_lv_ac_out_open",
        "cfg_max_chg_soc",
        "cfg_min_dsg_soc",
        "cfg_multi_bp_chg_dsg_mode",
        "cfg_output_power_off_memory",
        "cfg_plug_in_info_5p8_chg_pow_max",
        "cfg_plug_in_info_ac_in_chg_pow_max",
        "cfg_plug_in_info_pv_dc_amp_max",
        "cfg_plug_in_info_pv_h_dc_amp_max",
        "cfg_plug_in_info_pv_l_dc_amp_max",
        "cfg_power_off",
        "cfg_power_on",
        "cfg_pv_chg_type",
        "cfg_pv_dc_chg_setting",
        "cfg_runtime_property_full_upload_period",
        "cfg_runtime_property_incremental_upload_period",
        "cfg_screen_off_time",
        "cfg_soc_cali",
        "cfg_sp_charger_car_batt_vol_setting",
        "cfg_sp_charger_chg_mode",
        "cfg_sp_charger_chg_open",
        "cfg_sp_charger_chg_pow_limit",
        "cfg_storm_pattern",
        "cfg_time_task_v2_item",
        "cfg_tou_strategy",
        "cfg_ups_alram",
        "cfg_usb_open",
        "cfg_utc_set_mode",
        "cfg_utc_time",
        "cfg_utc_timezone",
        "cfg_utc_timezone_id",
        "cfg_wireless_oil_off_soc",
        "cfg_wireless_oil_on_soc",
        "cfg_wireless_oil_self_start",
        "cfg_xboost_en",
        "config_ok",
        "reset_factory_setting",
        "reset_generator_maintence_state",
        "reset_middlemen_delivery_setting",
        "set_time_task",
    ]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_DISPLAY_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_RUNTIME_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SELECTED_TIME_TASK_V2_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_ENERGY_SAVING_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_HV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_IN_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_LV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_BACKUP_REVERSE_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_FIELD_NUMBER: _ClassVar[int]
    CFG_BLE_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_BMS_POWER_OFF_FIELD_NUMBER: _ClassVar[int]
    CFG_BMS_PUSH_FIELD_NUMBER: _ClassVar[int]
    CFG_BYPASS_OUT_DISABLE_FIELD_NUMBER: _ClassVar[int]
    CFG_CMS_OIL_OFF_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_CMS_OIL_ON_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_CMS_OIL_SELF_START_FIELD_NUMBER: _ClassVar[int]
    CFG_DC_12V_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_DC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_DC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_DEV_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_DISPLAY_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_DISPLAY_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_ENERGY_BACKUP_FIELD_NUMBER: _ClassVar[int]
    CFG_ENERGY_STRATEGY_OPERATE_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_LNG_UINT_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_LPG_UINT_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_UINT_FIELD_NUMBER: _ClassVar[int]
    CFG_FUELS_LIQUEFIED_GAS_VAL_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_AC_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_CARE_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_DC_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_ENGINE_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_LOW_POWER_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_LOW_POWER_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_LPG_MONITOR_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_MPPT_HYBRID_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_PERF_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_SELF_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_HV_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_INSTALLMENT_PAYMENT_SERVE_BELONE_FIELD_NUMBER: _ClassVar[int]
    CFG_INSTALLMENT_PAYMENT_SERVE_ENABLE_FIELD_NUMBER: _ClassVar[int]
    CFG_INSTALLMENT_PAYMENT_SERVE_FIELD_NUMBER: _ClassVar[int]
    CFG_LCD_LIGHT_FIELD_NUMBER: _ClassVar[int]
    CFG_LED_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_LLC_GFCI_FLAG_FIELD_NUMBER: _ClassVar[int]
    CFG_LOW_POWER_ALARM_FIELD_NUMBER: _ClassVar[int]
    CFG_LV_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_MAX_CHG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_MIN_DSG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_MULTI_BP_CHG_DSG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_OUTPUT_POWER_OFF_MEMORY_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_5P8_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_AC_IN_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_H_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_L_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_OFF_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_PV_CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    CFG_PV_DC_CHG_SETTING_FIELD_NUMBER: _ClassVar[int]
    CFG_RJ45_COMMC_SERVICE_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_SCREEN_OFF_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_SOC_CALI_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CAR_BATT_VOL_SETTING_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CHG_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_SP_CHARGER_CHG_POW_LIMIT_FIELD_NUMBER: _ClassVar[int]
    CFG_STORM_PATTERN_FIELD_NUMBER: _ClassVar[int]
    CFG_TIME_TASK_V2_ITEM_FIELD_NUMBER: _ClassVar[int]
    CFG_TOU_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    CFG_UPS_ALRAM_FIELD_NUMBER: _ClassVar[int]
    CFG_USB_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_SET_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIMEZONE_ID_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_WIRELESS_OIL_OFF_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_WIRELESS_OIL_ON_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_WIRELESS_OIL_SELF_START_FIELD_NUMBER: _ClassVar[int]
    CFG_XBOOST_EN_FIELD_NUMBER: _ClassVar[int]
    CONFIG_OK_FIELD_NUMBER: _ClassVar[int]
    RESET_FACTORY_SETTING_FIELD_NUMBER: _ClassVar[int]
    RESET_GENERATOR_MAINTENCE_STATE_FIELD_NUMBER: _ClassVar[int]
    RESET_MIDDLEMEN_DELIVERY_SETTING_FIELD_NUMBER: _ClassVar[int]
    SET_TIME_TASK_FIELD_NUMBER: _ClassVar[int]
    action_id: int
    active_display_property_full_upload: bool
    active_runtime_property_full_upload: bool
    active_selected_time_task_v2: int
    cfg_RJ45_commc_service: CfgRj45CommcService
    cfg_ac_energy_saving_open: bool
    cfg_ac_hv_always_on: CfgAcHvAlwaysOn
    cfg_ac_in_chg_mode: AC_IN_CHG_MODE
    cfg_ac_lv_always_on: CfgAcLvAlwaysOn
    cfg_ac_out_always_on: CfgAcOutAlwaysOn
    cfg_ac_out_freq: int
    cfg_ac_out_open: bool
    cfg_ac_standby_time: int
    cfg_backup_reverse_soc: int
    cfg_beep: CfgBeep
    cfg_beep_en: bool
    cfg_ble_standby_time: int
    cfg_bms_power_off: CfgBmsPowerOffWriteAck
    cfg_bms_push: CfgBmsPushWriteAck
    cfg_bypass_out_disable: bool
    cfg_cms_oil_off_soc: int
    cfg_cms_oil_on_soc: int
    cfg_cms_oil_self_start: bool
    cfg_dc_12v_out_open: bool
    cfg_dc_out_open: bool
    cfg_dc_standby_time: int
    cfg_dev_standby_time: int
    cfg_display_property_full_upload_period: int
    cfg_display_property_incremental_upload_period: int
    cfg_energy_backup: CfgEnergyBackup
    cfg_energy_strategy_operate_mode: CfgEnergyStrategyOperateMode
    cfg_fuels_liquefied_gas_lng_uint: int
    cfg_fuels_liquefied_gas_lpg_uint: int
    cfg_fuels_liquefied_gas_type: int
    cfg_fuels_liquefied_gas_uint: int
    cfg_fuels_liquefied_gas_val: float
    cfg_generator_ac_out_pow_max: int
    cfg_generator_care_mode: CfgGeneratorCareMode
    cfg_generator_dc_out_pow_max: int
    cfg_generator_engine_open: int
    cfg_generator_low_power_en: bool
    cfg_generator_low_power_threshold: int
    cfg_generator_lpg_monitor_en: bool
    cfg_generator_mppt_hybrid_mode: CfgGeneratorMpptHybridMode
    cfg_generator_out_pow_max: int
    cfg_generator_perf_mode: int
    cfg_generator_self_on: bool
    cfg_hv_ac_out_open: bool
    cfg_installment_payment_serve: InstallmentPaymentServe
    cfg_installment_payment_serve_belone: InstallmentPaymentServeBelone
    cfg_installment_payment_serve_enable: bool
    cfg_lcd_light: int
    cfg_led_mode: int
    cfg_llc_GFCI_flag: bool
    cfg_low_power_alarm: int
    cfg_lv_ac_out_open: bool
    cfg_max_chg_soc: int
    cfg_min_dsg_soc: int
    cfg_multi_bp_chg_dsg_mode: int
    cfg_output_power_off_memory: bool
    cfg_plug_in_info_5p8_chg_pow_max: int
    cfg_plug_in_info_ac_in_chg_pow_max: int
    cfg_plug_in_info_pv_dc_amp_max: int
    cfg_plug_in_info_pv_h_dc_amp_max: int
    cfg_plug_in_info_pv_l_dc_amp_max: int
    cfg_power_off: bool
    cfg_power_on: bool
    cfg_pv_chg_type: int
    cfg_pv_dc_chg_setting: PvDcChgSetting
    cfg_runtime_property_full_upload_period: int
    cfg_runtime_property_incremental_upload_period: int
    cfg_screen_off_time: int
    cfg_soc_cali: int
    cfg_sp_charger_car_batt_vol_setting: int
    cfg_sp_charger_chg_mode: SP_CHARGER_CHG_MODE
    cfg_sp_charger_chg_open: bool
    cfg_sp_charger_chg_pow_limit: float
    cfg_storm_pattern: CfgStormPattern
    cfg_time_task_v2_item: TimeTaskItemV2
    cfg_tou_strategy: CfgTouStrategy
    cfg_ups_alram: bool
    cfg_usb_open: bool
    cfg_utc_set_mode: bool
    cfg_utc_time: int
    cfg_utc_timezone: int
    cfg_utc_timezone_id: str
    cfg_wireless_oil_off_soc: int
    cfg_wireless_oil_on_soc: int
    cfg_wireless_oil_self_start: bool
    cfg_xboost_en: bool
    config_ok: bool
    reset_factory_setting: int
    reset_generator_maintence_state: bool
    reset_middlemen_delivery_setting: ResetMiddlemenDeliverySetting
    set_time_task: SetTimeTaskWriteAck
    def __init__(
        self,
        action_id: _Optional[int] = ...,
        config_ok: bool = ...,
        cfg_power_off: bool = ...,
        cfg_power_on: bool = ...,
        reset_factory_setting: _Optional[int] = ...,
        cfg_utc_time: _Optional[int] = ...,
        cfg_utc_timezone: _Optional[int] = ...,
        cfg_beep: _Optional[_Union[CfgBeep, _Mapping]] = ...,
        cfg_beep_en: bool = ...,
        cfg_ac_standby_time: _Optional[int] = ...,
        cfg_dc_standby_time: _Optional[int] = ...,
        cfg_screen_off_time: _Optional[int] = ...,
        cfg_dev_standby_time: _Optional[int] = ...,
        cfg_lcd_light: _Optional[int] = ...,
        cfg_hv_ac_out_open: bool = ...,
        cfg_lv_ac_out_open: bool = ...,
        cfg_ac_out_freq: _Optional[int] = ...,
        cfg_dc_12v_out_open: bool = ...,
        cfg_usb_open: bool = ...,
        cfg_dc_out_open: bool = ...,
        cfg_ac_out_always_on: _Optional[_Union[CfgAcOutAlwaysOn, _Mapping]] = ...,
        cfg_xboost_en: bool = ...,
        cfg_bypass_out_disable: bool = ...,
        cfg_bms_power_off: _Optional[_Union[CfgBmsPowerOffWriteAck, _Mapping]] = ...,
        cfg_soc_cali: _Optional[int] = ...,
        cfg_bms_push: _Optional[_Union[CfgBmsPushWriteAck, _Mapping]] = ...,
        cfg_max_chg_soc: _Optional[int] = ...,
        cfg_min_dsg_soc: _Optional[int] = ...,
        set_time_task: _Optional[_Union[SetTimeTaskWriteAck, _Mapping]] = ...,
        cfg_energy_backup: _Optional[_Union[CfgEnergyBackup, _Mapping]] = ...,
        cfg_plug_in_info_pv_l_dc_amp_max: _Optional[int] = ...,
        cfg_plug_in_info_pv_h_dc_amp_max: _Optional[int] = ...,
        cfg_plug_in_info_ac_in_chg_pow_max: _Optional[int] = ...,
        cfg_plug_in_info_5p8_chg_pow_max: _Optional[int] = ...,
        cfg_cms_oil_self_start: bool = ...,
        cfg_cms_oil_on_soc: _Optional[int] = ...,
        cfg_cms_oil_off_soc: _Optional[int] = ...,
        cfg_llc_GFCI_flag: bool = ...,
        cfg_ac_hv_always_on: _Optional[_Union[CfgAcHvAlwaysOn, _Mapping]] = ...,
        cfg_ac_lv_always_on: _Optional[_Union[CfgAcLvAlwaysOn, _Mapping]] = ...,
        cfg_tou_strategy: _Optional[_Union[CfgTouStrategy, _Mapping]] = ...,
        cfg_ble_standby_time: _Optional[int] = ...,
        cfg_display_property_full_upload_period: _Optional[int] = ...,
        cfg_display_property_incremental_upload_period: _Optional[int] = ...,
        cfg_runtime_property_full_upload_period: _Optional[int] = ...,
        cfg_runtime_property_incremental_upload_period: _Optional[int] = ...,
        active_display_property_full_upload: bool = ...,
        active_runtime_property_full_upload: bool = ...,
        cfg_RJ45_commc_service: _Optional[_Union[CfgRj45CommcService, _Mapping]] = ...,
        cfg_ac_out_open: bool = ...,
        cfg_generator_perf_mode: _Optional[int] = ...,
        cfg_generator_engine_open: _Optional[int] = ...,
        cfg_generator_out_pow_max: _Optional[int] = ...,
        cfg_generator_ac_out_pow_max: _Optional[int] = ...,
        cfg_generator_dc_out_pow_max: _Optional[int] = ...,
        cfg_generator_self_on: bool = ...,
        reset_generator_maintence_state: bool = ...,
        cfg_fuels_liquefied_gas_type: _Optional[int] = ...,
        cfg_fuels_liquefied_gas_uint: _Optional[int] = ...,
        cfg_fuels_liquefied_gas_val: _Optional[float] = ...,
        cfg_plug_in_info_pv_dc_amp_max: _Optional[int] = ...,
        cfg_ups_alram: bool = ...,
        cfg_led_mode: _Optional[int] = ...,
        cfg_pv_chg_type: _Optional[int] = ...,
        cfg_low_power_alarm: _Optional[int] = ...,
        cfg_storm_pattern: _Optional[_Union[CfgStormPattern, _Mapping]] = ...,
        cfg_generator_mppt_hybrid_mode: _Optional[
            _Union[CfgGeneratorMpptHybridMode, _Mapping]
        ] = ...,
        cfg_generator_care_mode: _Optional[
            _Union[CfgGeneratorCareMode, _Mapping]
        ] = ...,
        cfg_ac_energy_saving_open: bool = ...,
        cfg_multi_bp_chg_dsg_mode: _Optional[int] = ...,
        cfg_backup_reverse_soc: _Optional[int] = ...,
        cfg_energy_strategy_operate_mode: _Optional[
            _Union[CfgEnergyStrategyOperateMode, _Mapping]
        ] = ...,
        cfg_sp_charger_chg_mode: _Optional[_Union[SP_CHARGER_CHG_MODE, str]] = ...,
        cfg_installment_payment_serve_enable: bool = ...,
        cfg_installment_payment_serve_belone: _Optional[
            _Union[InstallmentPaymentServeBelone, _Mapping]
        ] = ...,
        cfg_installment_payment_serve: _Optional[
            _Union[InstallmentPaymentServe, _Mapping]
        ] = ...,
        cfg_sp_charger_chg_open: bool = ...,
        cfg_sp_charger_chg_pow_limit: _Optional[float] = ...,
        reset_middlemen_delivery_setting: _Optional[
            _Union[ResetMiddlemenDeliverySetting, _Mapping]
        ] = ...,
        cfg_ac_in_chg_mode: _Optional[_Union[AC_IN_CHG_MODE, str]] = ...,
        cfg_pv_dc_chg_setting: _Optional[_Union[PvDcChgSetting, _Mapping]] = ...,
        cfg_time_task_v2_item: _Optional[_Union[TimeTaskItemV2, _Mapping]] = ...,
        active_selected_time_task_v2: _Optional[int] = ...,
        cfg_generator_low_power_en: bool = ...,
        cfg_generator_low_power_threshold: _Optional[int] = ...,
        cfg_generator_lpg_monitor_en: bool = ...,
        cfg_fuels_liquefied_gas_lpg_uint: _Optional[int] = ...,
        cfg_fuels_liquefied_gas_lng_uint: _Optional[int] = ...,
        cfg_utc_timezone_id: _Optional[str] = ...,
        cfg_utc_set_mode: bool = ...,
        cfg_sp_charger_car_batt_vol_setting: _Optional[int] = ...,
        cfg_wireless_oil_self_start: bool = ...,
        cfg_wireless_oil_on_soc: _Optional[int] = ...,
        cfg_wireless_oil_off_soc: _Optional[int] = ...,
        cfg_output_power_off_memory: bool = ...,
    ) -> None: ...

class DevRequest(_message.Message):
    __slots__ = [
        "dev_utc_time",
        "dev_utc_timezone",
        "require_property_upload_period",
        "require_tou_strategy",
    ]
    DEV_UTC_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    DEV_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_PROPERTY_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_TOU_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    dev_utc_time: int
    dev_utc_timezone: float
    require_property_upload_period: bool
    require_tou_strategy: ReqTouStrategy
    def __init__(
        self,
        dev_utc_time: _Optional[int] = ...,
        dev_utc_timezone: _Optional[float] = ...,
        require_property_upload_period: bool = ...,
        require_tou_strategy: _Optional[_Union[ReqTouStrategy, _Mapping]] = ...,
    ) -> None: ...

class DevRequestAck(_message.Message):
    __slots__ = ["property_upload_period", "request_id", "require_ok"]
    PROPERTY_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_OK_FIELD_NUMBER: _ClassVar[int]
    property_upload_period: PropertyUploadPeriod
    request_id: int
    require_ok: int
    def __init__(
        self,
        request_id: _Optional[int] = ...,
        require_ok: _Optional[int] = ...,
        property_upload_period: _Optional[_Union[PropertyUploadPeriod, _Mapping]] = ...,
    ) -> None: ...

class DisplayPropertyUpload(_message.Message):
    __slots__ = [
        "ac_always_on_flag",
        "ac_always_on_mini_soc",
        "ac_energy_saving_open",
        "ac_hv_always_on",
        "ac_lv_always_on",
        "ac_out_freq",
        "ac_out_open",
        "ac_standby_time",
        "ble_standby_time",
        "bms_batt_soc",
        "bms_batt_soh",
        "bms_chg_dsg_state",
        "bms_chg_rem_time",
        "bms_design_cap",
        "bms_dsg_rem_time",
        "bms_err_code",
        "bms_max_cell_temp",
        "bms_max_mos_temp",
        "bms_min_cell_temp",
        "bms_min_mos_temp",
        "btn_ac_out_hv_switch",
        "btn_ac_out_lv_switch",
        "btn_dc_12v_out_switch",
        "btn_usb_switch",
        "bypass_out_disable",
        "cms_batt_design_cap",
        "cms_batt_full_cap",
        "cms_batt_full_energy",
        "cms_batt_pow_in_max",
        "cms_batt_pow_out_max",
        "cms_batt_remain_cap",
        "cms_batt_soc",
        "cms_batt_soh",
        "cms_batt_temp",
        "cms_bms_run_state",
        "cms_chg_dsg_state",
        "cms_chg_rem_time",
        "cms_dsg_rem_time",
        "cms_max_chg_soc",
        "cms_min_dsg_soc",
        "cms_oil_off_soc",
        "cms_oil_on_soc",
        "cms_oil_self_start",
        "current_time_task_v2_item",
        "dc_out_open",
        "dc_standby_time",
        "dcdc_err_code",
        "dev_online_flag",
        "dev_sleep_state",
        "dev_standby_time",
        "display_statistics_sum",
        "en_beep",
        "energy_backup_en",
        "energy_backup_start_soc",
        "energy_backup_state",
        "err_code_record_list",
        "errcode",
        "fast_charge_switch",
        "flow_info_12v",
        "flow_info_24v",
        "flow_info_4p8_1_in",
        "flow_info_4p8_1_out",
        "flow_info_4p8_2_in",
        "flow_info_4p8_2_out",
        "flow_info_5p8_in",
        "flow_info_5p8_out",
        "flow_info_ac2dc",
        "flow_info_ac_hv_out",
        "flow_info_ac_in",
        "flow_info_ac_lv_out",
        "flow_info_ac_out",
        "flow_info_bms_chg",
        "flow_info_bms_dsg",
        "flow_info_dc2ac",
        "flow_info_dcp2_in",
        "flow_info_dcp2_out",
        "flow_info_dcp_in",
        "flow_info_dcp_out",
        "flow_info_pv",
        "flow_info_pv2",
        "flow_info_pv_h",
        "flow_info_pv_l",
        "flow_info_qcusb1",
        "flow_info_qcusb2",
        "flow_info_typec1",
        "flow_info_typec2",
        "fuels_liquefied_gas_consume_per_hour",
        "fuels_liquefied_gas_lng_uint",
        "fuels_liquefied_gas_lpg_uint",
        "fuels_liquefied_gas_remain_val",
        "fuels_liquefied_gas_type",
        "fuels_liquefied_gas_uint",
        "fuels_liquefied_gas_val",
        "fuels_oil_val",
        "generator_abnormal_state",
        "generator_ac_out_pow_max",
        "generator_care_mode_open",
        "generator_care_mode_start_time",
        "generator_conn_dev_errcode",
        "generator_dc_out_pow_max",
        "generator_engine_open",
        "generator_fuels_type",
        "generator_low_power_en",
        "generator_low_power_threshold",
        "generator_lpg_monitor_en",
        "generator_maintence_state",
        "generator_out_pow_max",
        "generator_pcs_err_code",
        "generator_perf_mode",
        "generator_pv_hybrid_mode_open",
        "generator_pv_hybrid_mode_soc_max",
        "generator_remain_time",
        "generator_run_time",
        "generator_sub_battery_soc",
        "generator_sub_battery_state",
        "generator_sub_battery_temp",
        "generator_total_output",
        "installment_payment_overdue_limit",
        "installment_payment_overdue_limit_utc_time",
        "installment_payment_serve_enable",
        "installment_payment_start_utc_time",
        "installment_payment_state",
        "inv_err_code",
        "lcd_light",
        "led_mode",
        "llc_GFCI_flag",
        "llc_err_code",
        "llc_hv_lv_flag",
        "llc_inv_err_code",
        "low_power_alarm",
        "module_bluetooth_rssi",
        "module_bluetooth_snr",
        "module_wifi_rssi",
        "module_wifi_snr",
        "mppt_err_code",
        "multi_bp_chg_dsg_mode",
        "output_power_off_memory",
        "pcs_fan_err_flag",
        "pcs_fan_level",
        "pd_err_code",
        "plug_in_info_4p8_1_charger_flag",
        "plug_in_info_4p8_1_detail",
        "plug_in_info_4p8_1_dsg_chg_type",
        "plug_in_info_4p8_1_err_code",
        "plug_in_info_4p8_1_firm_ver",
        "plug_in_info_4p8_1_in_flag",
        "plug_in_info_4p8_1_resv",
        "plug_in_info_4p8_1_run_state",
        "plug_in_info_4p8_1_sn",
        "plug_in_info_4p8_1_type",
        "plug_in_info_4p8_2_charger_flag",
        "plug_in_info_4p8_2_detail",
        "plug_in_info_4p8_2_dsg_chg_type",
        "plug_in_info_4p8_2_err_code",
        "plug_in_info_4p8_2_firm_ver",
        "plug_in_info_4p8_2_in_flag",
        "plug_in_info_4p8_2_resv",
        "plug_in_info_4p8_2_run_state",
        "plug_in_info_4p8_2_sn",
        "plug_in_info_4p8_2_type",
        "plug_in_info_5p8_charger_flag",
        "plug_in_info_5p8_chg_hal_pow_max",
        "plug_in_info_5p8_chg_pow_max",
        "plug_in_info_5p8_detail",
        "plug_in_info_5p8_dsg_chg",
        "plug_in_info_5p8_dsg_pow_max",
        "plug_in_info_5p8_err_code",
        "plug_in_info_5p8_firm_ver",
        "plug_in_info_5p8_flag",
        "plug_in_info_5p8_resv",
        "plug_in_info_5p8_run_state",
        "plug_in_info_5p8_sn",
        "plug_in_info_5p8_type",
        "plug_in_info_ac_charger_flag",
        "plug_in_info_ac_in_chg_hal_pow_max",
        "plug_in_info_ac_in_chg_mode",
        "plug_in_info_ac_in_chg_pow_max",
        "plug_in_info_ac_in_feq",
        "plug_in_info_ac_in_flag",
        "plug_in_info_ac_out_dsg_pow_max",
        "plug_in_info_acp_charger_flag",
        "plug_in_info_acp_chg_hal_pow_max",
        "plug_in_info_acp_chg_pow_max",
        "plug_in_info_acp_detail",
        "plug_in_info_acp_dsg_chg",
        "plug_in_info_acp_dsg_pow_max",
        "plug_in_info_acp_err_code",
        "plug_in_info_acp_firm_ver",
        "plug_in_info_acp_flag",
        "plug_in_info_acp_resv",
        "plug_in_info_acp_run_state",
        "plug_in_info_acp_sn",
        "plug_in_info_acp_type",
        "plug_in_info_dc_bidi_flag",
        "plug_in_info_dcp2_charger_flag",
        "plug_in_info_dcp2_detail",
        "plug_in_info_dcp2_dsg_chg_type",
        "plug_in_info_dcp2_err_code",
        "plug_in_info_dcp2_firm_ver",
        "plug_in_info_dcp2_in_flag",
        "plug_in_info_dcp2_resv",
        "plug_in_info_dcp2_run_state",
        "plug_in_info_dcp2_sn",
        "plug_in_info_dcp2_type",
        "plug_in_info_dcp_charger_flag",
        "plug_in_info_dcp_detail",
        "plug_in_info_dcp_dsg_chg_type",
        "plug_in_info_dcp_err_code",
        "plug_in_info_dcp_firm_ver",
        "plug_in_info_dcp_in_flag",
        "plug_in_info_dcp_resv",
        "plug_in_info_dcp_run_state",
        "plug_in_info_dcp_sn",
        "plug_in_info_dcp_type",
        "plug_in_info_pv2_charger_flag",
        "plug_in_info_pv2_chg_amp_max",
        "plug_in_info_pv2_chg_max_list",
        "plug_in_info_pv2_chg_vol_max",
        "plug_in_info_pv2_dc_amp_max",
        "plug_in_info_pv2_flag",
        "plug_in_info_pv2_type",
        "plug_in_info_pv_charger_flag",
        "plug_in_info_pv_chg_amp_max",
        "plug_in_info_pv_chg_max_list",
        "plug_in_info_pv_chg_vol_max",
        "plug_in_info_pv_dc_amp_max",
        "plug_in_info_pv_flag",
        "plug_in_info_pv_h_charger_flag",
        "plug_in_info_pv_h_chg_amp_max",
        "plug_in_info_pv_h_chg_vol_max",
        "plug_in_info_pv_h_dc_amp_max",
        "plug_in_info_pv_h_flag",
        "plug_in_info_pv_h_type",
        "plug_in_info_pv_l_charger_flag",
        "plug_in_info_pv_l_chg_amp_max",
        "plug_in_info_pv_l_chg_vol_max",
        "plug_in_info_pv_l_dc_amp_max",
        "plug_in_info_pv_l_flag",
        "plug_in_info_pv_l_type",
        "plug_in_info_pv_type",
        "pow_get_12v",
        "pow_get_24v",
        "pow_get_4p8_1",
        "pow_get_4p8_2",
        "pow_get_5p8",
        "pow_get_ac",
        "pow_get_ac_hv_out",
        "pow_get_ac_in",
        "pow_get_ac_lv_out",
        "pow_get_ac_lv_tt30_out",
        "pow_get_ac_out",
        "pow_get_bms",
        "pow_get_dc",
        "pow_get_dc_bidi",
        "pow_get_dcp",
        "pow_get_dcp2",
        "pow_get_llc",
        "pow_get_pv",
        "pow_get_pv2",
        "pow_get_pv_h",
        "pow_get_pv_l",
        "pow_get_qcusb1",
        "pow_get_qcusb2",
        "pow_get_typec1",
        "pow_get_typec2",
        "pow_in_sum_w",
        "pow_out_sum_w",
        "pv_chg_type",
        "pv_dc_chg_setting_list",
        "screen_off_time",
        "serve_middlemen",
        "silence_chg_watt",
        "sp_charger_car_batt_vol",
        "sp_charger_car_batt_vol_setting",
        "sp_charger_chg_mode",
        "sp_charger_chg_open",
        "sp_charger_chg_pow_limit",
        "sp_charger_chg_pow_max",
        "sp_charger_is_connect_car",
        "sp_charger_run_state",
        "storm_pattern_enable",
        "storm_pattern_end_time",
        "storm_pattern_open_flag",
        "sys_status",
        "time_task_change_cnt",
        "time_task_conflict_flag",
        "time_task_current",
        "ups_alram",
        "utc_set_mode",
        "utc_timezone",
        "utc_timezone_id",
        "wireless_coordinate_dev_list",
        "wireless_oil_off_soc",
        "wireless_oil_on_soc",
        "wireless_oil_self_start",
        "xboost_en",
    ]
    AC_ALWAYS_ON_FLAG_FIELD_NUMBER: _ClassVar[int]
    AC_ALWAYS_ON_MINI_SOC_FIELD_NUMBER: _ClassVar[int]
    AC_ENERGY_SAVING_OPEN_FIELD_NUMBER: _ClassVar[int]
    AC_HV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    AC_LV_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    AC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    BLE_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    BMS_BATT_SOC_FIELD_NUMBER: _ClassVar[int]
    BMS_BATT_SOH_FIELD_NUMBER: _ClassVar[int]
    BMS_CHG_DSG_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_CHG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    BMS_DESIGN_CAP_FIELD_NUMBER: _ClassVar[int]
    BMS_DSG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    BMS_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    BMS_MAX_CELL_TEMP_FIELD_NUMBER: _ClassVar[int]
    BMS_MAX_MOS_TEMP_FIELD_NUMBER: _ClassVar[int]
    BMS_MIN_CELL_TEMP_FIELD_NUMBER: _ClassVar[int]
    BMS_MIN_MOS_TEMP_FIELD_NUMBER: _ClassVar[int]
    BTN_AC_OUT_HV_SWITCH_FIELD_NUMBER: _ClassVar[int]
    BTN_AC_OUT_LV_SWITCH_FIELD_NUMBER: _ClassVar[int]
    BTN_DC_12V_OUT_SWITCH_FIELD_NUMBER: _ClassVar[int]
    BTN_USB_SWITCH_FIELD_NUMBER: _ClassVar[int]
    BYPASS_OUT_DISABLE_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_DESIGN_CAP_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_FULL_CAP_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_FULL_ENERGY_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_POW_IN_MAX_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_POW_OUT_MAX_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_REMAIN_CAP_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_SOH_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_TEMP_FIELD_NUMBER: _ClassVar[int]
    CMS_BMS_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    CMS_CHG_DSG_STATE_FIELD_NUMBER: _ClassVar[int]
    CMS_CHG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    CMS_DSG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    CMS_MAX_CHG_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_MIN_DSG_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_OIL_OFF_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_OIL_ON_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_OIL_SELF_START_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TIME_TASK_V2_ITEM_FIELD_NUMBER: _ClassVar[int]
    DCDC_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    DC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    DC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    DEV_ONLINE_FLAG_FIELD_NUMBER: _ClassVar[int]
    DEV_SLEEP_STATE_FIELD_NUMBER: _ClassVar[int]
    DEV_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_STATISTICS_SUM_FIELD_NUMBER: _ClassVar[int]
    ENERGY_BACKUP_EN_FIELD_NUMBER: _ClassVar[int]
    ENERGY_BACKUP_START_SOC_FIELD_NUMBER: _ClassVar[int]
    ENERGY_BACKUP_STATE_FIELD_NUMBER: _ClassVar[int]
    EN_BEEP_FIELD_NUMBER: _ClassVar[int]
    ERRCODE_FIELD_NUMBER: _ClassVar[int]
    ERR_CODE_RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    FAST_CHARGE_SWITCH_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_12V_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_24V_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_4P8_1_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_4P8_1_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_4P8_2_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_4P8_2_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_5P8_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_5P8_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC2DC_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC_HV_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC_LV_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_BMS_CHG_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_BMS_DSG_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DC2AC_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DCP2_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DCP2_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DCP_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DCP_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_PV2_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_PV_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_PV_H_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_PV_L_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_QCUSB1_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_QCUSB2_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_TYPEC1_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_TYPEC2_FIELD_NUMBER: _ClassVar[int]
    FUELS_LIQUEFIED_GAS_CONSUME_PER_HOUR_FIELD_NUMBER: _ClassVar[int]
    FUELS_LIQUEFIED_GAS_LNG_UINT_FIELD_NUMBER: _ClassVar[int]
    FUELS_LIQUEFIED_GAS_LPG_UINT_FIELD_NUMBER: _ClassVar[int]
    FUELS_LIQUEFIED_GAS_REMAIN_VAL_FIELD_NUMBER: _ClassVar[int]
    FUELS_LIQUEFIED_GAS_TYPE_FIELD_NUMBER: _ClassVar[int]
    FUELS_LIQUEFIED_GAS_UINT_FIELD_NUMBER: _ClassVar[int]
    FUELS_LIQUEFIED_GAS_VAL_FIELD_NUMBER: _ClassVar[int]
    FUELS_OIL_VAL_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_ABNORMAL_STATE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_AC_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_CARE_MODE_OPEN_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_CARE_MODE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_CONN_DEV_ERRCODE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_DC_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_ENGINE_OPEN_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_FUELS_TYPE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_LOW_POWER_EN_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_LOW_POWER_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_LPG_MONITOR_EN_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_MAINTENCE_STATE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_OUT_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PCS_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PERF_MODE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PV_HYBRID_MODE_OPEN_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PV_HYBRID_MODE_SOC_MAX_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_REMAIN_TIME_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_RUN_TIME_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_SUB_BATTERY_SOC_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_SUB_BATTERY_STATE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_SUB_BATTERY_TEMP_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_TOTAL_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_OVERDUE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_OVERDUE_LIMIT_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_SERVE_ENABLE_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_START_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    INV_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    LCD_LIGHT_FIELD_NUMBER: _ClassVar[int]
    LED_MODE_FIELD_NUMBER: _ClassVar[int]
    LLC_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    LLC_GFCI_FLAG_FIELD_NUMBER: _ClassVar[int]
    LLC_HV_LV_FLAG_FIELD_NUMBER: _ClassVar[int]
    LLC_INV_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    LOW_POWER_ALARM_FIELD_NUMBER: _ClassVar[int]
    MODULE_BLUETOOTH_RSSI_FIELD_NUMBER: _ClassVar[int]
    MODULE_BLUETOOTH_SNR_FIELD_NUMBER: _ClassVar[int]
    MODULE_WIFI_RSSI_FIELD_NUMBER: _ClassVar[int]
    MODULE_WIFI_SNR_FIELD_NUMBER: _ClassVar[int]
    MPPT_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    MULTI_BP_CHG_DSG_MODE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_POWER_OFF_MEMORY_FIELD_NUMBER: _ClassVar[int]
    PCS_FAN_ERR_FLAG_FIELD_NUMBER: _ClassVar[int]
    PCS_FAN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PD_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_DETAIL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_DSG_CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_RESV_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_SN_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_DETAIL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_DSG_CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_RESV_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_SN_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_CHG_HAL_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_DETAIL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_DSG_CHG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_DSG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_RESV_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_SN_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_CHG_HAL_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_DETAIL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_DSG_CHG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_DSG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_RESV_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_SN_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_CHG_HAL_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_FEQ_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_DSG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_DETAIL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_DSG_CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_RESV_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_SN_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_DETAIL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_DSG_CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_RESV_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_SN_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DC_BIDI_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_CHG_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_CHG_MAX_LIST_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_CHG_VOL_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_CHG_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_CHG_MAX_LIST_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_CHG_VOL_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_CHG_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_CHG_VOL_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_CHG_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_CHG_VOL_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_TYPE_FIELD_NUMBER: _ClassVar[int]
    POW_GET_12V_FIELD_NUMBER: _ClassVar[int]
    POW_GET_24V_FIELD_NUMBER: _ClassVar[int]
    POW_GET_4P8_1_FIELD_NUMBER: _ClassVar[int]
    POW_GET_4P8_2_FIELD_NUMBER: _ClassVar[int]
    POW_GET_5P8_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_HV_OUT_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_IN_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_LV_OUT_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_LV_TT30_OUT_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_OUT_FIELD_NUMBER: _ClassVar[int]
    POW_GET_BMS_FIELD_NUMBER: _ClassVar[int]
    POW_GET_DCP2_FIELD_NUMBER: _ClassVar[int]
    POW_GET_DCP_FIELD_NUMBER: _ClassVar[int]
    POW_GET_DC_BIDI_FIELD_NUMBER: _ClassVar[int]
    POW_GET_DC_FIELD_NUMBER: _ClassVar[int]
    POW_GET_LLC_FIELD_NUMBER: _ClassVar[int]
    POW_GET_PV2_FIELD_NUMBER: _ClassVar[int]
    POW_GET_PV_FIELD_NUMBER: _ClassVar[int]
    POW_GET_PV_H_FIELD_NUMBER: _ClassVar[int]
    POW_GET_PV_L_FIELD_NUMBER: _ClassVar[int]
    POW_GET_QCUSB1_FIELD_NUMBER: _ClassVar[int]
    POW_GET_QCUSB2_FIELD_NUMBER: _ClassVar[int]
    POW_GET_TYPEC1_FIELD_NUMBER: _ClassVar[int]
    POW_GET_TYPEC2_FIELD_NUMBER: _ClassVar[int]
    POW_IN_SUM_W_FIELD_NUMBER: _ClassVar[int]
    POW_OUT_SUM_W_FIELD_NUMBER: _ClassVar[int]
    PV_CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PV_DC_CHG_SETTING_LIST_FIELD_NUMBER: _ClassVar[int]
    SCREEN_OFF_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVE_MIDDLEMEN_FIELD_NUMBER: _ClassVar[int]
    SILENCE_CHG_WATT_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_CAR_BATT_VOL_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_CAR_BATT_VOL_SETTING_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_CHG_OPEN_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_CHG_POW_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_IS_CONNECT_CAR_FIELD_NUMBER: _ClassVar[int]
    SP_CHARGER_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_OPEN_FLAG_FIELD_NUMBER: _ClassVar[int]
    SYS_STATUS_FIELD_NUMBER: _ClassVar[int]
    TIME_TASK_CHANGE_CNT_FIELD_NUMBER: _ClassVar[int]
    TIME_TASK_CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    TIME_TASK_CURRENT_FIELD_NUMBER: _ClassVar[int]
    UPS_ALRAM_FIELD_NUMBER: _ClassVar[int]
    UTC_SET_MODE_FIELD_NUMBER: _ClassVar[int]
    UTC_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    UTC_TIMEZONE_ID_FIELD_NUMBER: _ClassVar[int]
    WIRELESS_COORDINATE_DEV_LIST_FIELD_NUMBER: _ClassVar[int]
    WIRELESS_OIL_OFF_SOC_FIELD_NUMBER: _ClassVar[int]
    WIRELESS_OIL_ON_SOC_FIELD_NUMBER: _ClassVar[int]
    WIRELESS_OIL_SELF_START_FIELD_NUMBER: _ClassVar[int]
    XBOOST_EN_FIELD_NUMBER: _ClassVar[int]
    ac_always_on_flag: bool
    ac_always_on_mini_soc: int
    ac_energy_saving_open: bool
    ac_hv_always_on: bool
    ac_lv_always_on: bool
    ac_out_freq: int
    ac_out_open: bool
    ac_standby_time: int
    ble_standby_time: int
    bms_batt_soc: float
    bms_batt_soh: float
    bms_chg_dsg_state: int
    bms_chg_rem_time: int
    bms_design_cap: int
    bms_dsg_rem_time: int
    bms_err_code: int
    bms_max_cell_temp: int
    bms_max_mos_temp: int
    bms_min_cell_temp: int
    bms_min_mos_temp: int
    btn_ac_out_hv_switch: bool
    btn_ac_out_lv_switch: bool
    btn_dc_12v_out_switch: bool
    btn_usb_switch: bool
    bypass_out_disable: bool
    cms_batt_design_cap: int
    cms_batt_full_cap: int
    cms_batt_full_energy: int
    cms_batt_pow_in_max: int
    cms_batt_pow_out_max: int
    cms_batt_remain_cap: int
    cms_batt_soc: float
    cms_batt_soh: float
    cms_batt_temp: int
    cms_bms_run_state: int
    cms_chg_dsg_state: int
    cms_chg_rem_time: int
    cms_dsg_rem_time: int
    cms_max_chg_soc: int
    cms_min_dsg_soc: int
    cms_oil_off_soc: int
    cms_oil_on_soc: int
    cms_oil_self_start: bool
    current_time_task_v2_item: TimeTaskItemV2
    dc_out_open: bool
    dc_standby_time: int
    dcdc_err_code: int
    dev_online_flag: bool
    dev_sleep_state: int
    dev_standby_time: int
    display_statistics_sum: DisplayStatisticsRecordList
    en_beep: bool
    energy_backup_en: bool
    energy_backup_start_soc: int
    energy_backup_state: int
    err_code_record_list: ErrcodeRecordList
    errcode: int
    fast_charge_switch: int
    flow_info_12v: int
    flow_info_24v: int
    flow_info_4p8_1_in: int
    flow_info_4p8_1_out: int
    flow_info_4p8_2_in: int
    flow_info_4p8_2_out: int
    flow_info_5p8_in: int
    flow_info_5p8_out: int
    flow_info_ac2dc: int
    flow_info_ac_hv_out: int
    flow_info_ac_in: int
    flow_info_ac_lv_out: int
    flow_info_ac_out: int
    flow_info_bms_chg: int
    flow_info_bms_dsg: int
    flow_info_dc2ac: int
    flow_info_dcp2_in: int
    flow_info_dcp2_out: int
    flow_info_dcp_in: int
    flow_info_dcp_out: int
    flow_info_pv: int
    flow_info_pv2: int
    flow_info_pv_h: int
    flow_info_pv_l: int
    flow_info_qcusb1: int
    flow_info_qcusb2: int
    flow_info_typec1: int
    flow_info_typec2: int
    fuels_liquefied_gas_consume_per_hour: float
    fuels_liquefied_gas_lng_uint: int
    fuels_liquefied_gas_lpg_uint: int
    fuels_liquefied_gas_remain_val: int
    fuels_liquefied_gas_type: int
    fuels_liquefied_gas_uint: int
    fuels_liquefied_gas_val: float
    fuels_oil_val: int
    generator_abnormal_state: int
    generator_ac_out_pow_max: int
    generator_care_mode_open: bool
    generator_care_mode_start_time: int
    generator_conn_dev_errcode: int
    generator_dc_out_pow_max: int
    generator_engine_open: int
    generator_fuels_type: int
    generator_low_power_en: bool
    generator_low_power_threshold: int
    generator_lpg_monitor_en: bool
    generator_maintence_state: bool
    generator_out_pow_max: int
    generator_pcs_err_code: int
    generator_perf_mode: int
    generator_pv_hybrid_mode_open: bool
    generator_pv_hybrid_mode_soc_max: int
    generator_remain_time: int
    generator_run_time: int
    generator_sub_battery_soc: int
    generator_sub_battery_state: int
    generator_sub_battery_temp: int
    generator_total_output: int
    installment_payment_overdue_limit: INSTALLMENT_PAYMENT_OVERDUE_LIMIT
    installment_payment_overdue_limit_utc_time: int
    installment_payment_serve_enable: bool
    installment_payment_start_utc_time: int
    installment_payment_state: INSTALLMENT_PAYMENT_STATE
    inv_err_code: int
    lcd_light: int
    led_mode: int
    llc_GFCI_flag: bool
    llc_err_code: int
    llc_hv_lv_flag: int
    llc_inv_err_code: int
    low_power_alarm: int
    module_bluetooth_rssi: float
    module_bluetooth_snr: float
    module_wifi_rssi: float
    module_wifi_snr: float
    mppt_err_code: int
    multi_bp_chg_dsg_mode: int
    output_power_off_memory: bool
    pcs_fan_err_flag: int
    pcs_fan_level: int
    pd_err_code: int
    plug_in_info_4p8_1_charger_flag: bool
    plug_in_info_4p8_1_detail: int
    plug_in_info_4p8_1_dsg_chg_type: int
    plug_in_info_4p8_1_err_code: int
    plug_in_info_4p8_1_firm_ver: int
    plug_in_info_4p8_1_in_flag: int
    plug_in_info_4p8_1_resv: ResvInfo
    plug_in_info_4p8_1_run_state: int
    plug_in_info_4p8_1_sn: str
    plug_in_info_4p8_1_type: int
    plug_in_info_4p8_2_charger_flag: bool
    plug_in_info_4p8_2_detail: int
    plug_in_info_4p8_2_dsg_chg_type: int
    plug_in_info_4p8_2_err_code: int
    plug_in_info_4p8_2_firm_ver: int
    plug_in_info_4p8_2_in_flag: int
    plug_in_info_4p8_2_resv: ResvInfo
    plug_in_info_4p8_2_run_state: int
    plug_in_info_4p8_2_sn: str
    plug_in_info_4p8_2_type: int
    plug_in_info_5p8_charger_flag: bool
    plug_in_info_5p8_chg_hal_pow_max: int
    plug_in_info_5p8_chg_pow_max: int
    plug_in_info_5p8_detail: int
    plug_in_info_5p8_dsg_chg: int
    plug_in_info_5p8_dsg_pow_max: int
    plug_in_info_5p8_err_code: int
    plug_in_info_5p8_firm_ver: int
    plug_in_info_5p8_flag: int
    plug_in_info_5p8_resv: ResvInfo
    plug_in_info_5p8_run_state: int
    plug_in_info_5p8_sn: str
    plug_in_info_5p8_type: int
    plug_in_info_ac_charger_flag: bool
    plug_in_info_ac_in_chg_hal_pow_max: int
    plug_in_info_ac_in_chg_mode: AC_IN_CHG_MODE
    plug_in_info_ac_in_chg_pow_max: int
    plug_in_info_ac_in_feq: int
    plug_in_info_ac_in_flag: int
    plug_in_info_ac_out_dsg_pow_max: int
    plug_in_info_acp_charger_flag: bool
    plug_in_info_acp_chg_hal_pow_max: int
    plug_in_info_acp_chg_pow_max: int
    plug_in_info_acp_detail: int
    plug_in_info_acp_dsg_chg: int
    plug_in_info_acp_dsg_pow_max: int
    plug_in_info_acp_err_code: int
    plug_in_info_acp_firm_ver: int
    plug_in_info_acp_flag: int
    plug_in_info_acp_resv: ResvInfo
    plug_in_info_acp_run_state: int
    plug_in_info_acp_sn: str
    plug_in_info_acp_type: int
    plug_in_info_dc_bidi_flag: bool
    plug_in_info_dcp2_charger_flag: bool
    plug_in_info_dcp2_detail: int
    plug_in_info_dcp2_dsg_chg_type: int
    plug_in_info_dcp2_err_code: int
    plug_in_info_dcp2_firm_ver: int
    plug_in_info_dcp2_in_flag: bool
    plug_in_info_dcp2_resv: ResvInfo
    plug_in_info_dcp2_run_state: int
    plug_in_info_dcp2_sn: str
    plug_in_info_dcp2_type: int
    plug_in_info_dcp_charger_flag: bool
    plug_in_info_dcp_detail: int
    plug_in_info_dcp_dsg_chg_type: int
    plug_in_info_dcp_err_code: int
    plug_in_info_dcp_firm_ver: int
    plug_in_info_dcp_in_flag: bool
    plug_in_info_dcp_resv: ResvInfo
    plug_in_info_dcp_run_state: int
    plug_in_info_dcp_sn: str
    plug_in_info_dcp_type: int
    plug_in_info_pv2_charger_flag: bool
    plug_in_info_pv2_chg_amp_max: int
    plug_in_info_pv2_chg_max_list: PvChgMaxList
    plug_in_info_pv2_chg_vol_max: int
    plug_in_info_pv2_dc_amp_max: int
    plug_in_info_pv2_flag: bool
    plug_in_info_pv2_type: int
    plug_in_info_pv_charger_flag: bool
    plug_in_info_pv_chg_amp_max: int
    plug_in_info_pv_chg_max_list: PvChgMaxList
    plug_in_info_pv_chg_vol_max: int
    plug_in_info_pv_dc_amp_max: int
    plug_in_info_pv_flag: bool
    plug_in_info_pv_h_charger_flag: bool
    plug_in_info_pv_h_chg_amp_max: int
    plug_in_info_pv_h_chg_vol_max: int
    plug_in_info_pv_h_dc_amp_max: int
    plug_in_info_pv_h_flag: int
    plug_in_info_pv_h_type: int
    plug_in_info_pv_l_charger_flag: bool
    plug_in_info_pv_l_chg_amp_max: int
    plug_in_info_pv_l_chg_vol_max: int
    plug_in_info_pv_l_dc_amp_max: int
    plug_in_info_pv_l_flag: int
    plug_in_info_pv_l_type: int
    plug_in_info_pv_type: int
    pow_get_12v: float
    pow_get_24v: float
    pow_get_4p8_1: float
    pow_get_4p8_2: float
    pow_get_5p8: float
    pow_get_ac: float
    pow_get_ac_hv_out: float
    pow_get_ac_in: float
    pow_get_ac_lv_out: float
    pow_get_ac_lv_tt30_out: float
    pow_get_ac_out: float
    pow_get_bms: float
    pow_get_dc: float
    pow_get_dc_bidi: float
    pow_get_dcp: float
    pow_get_dcp2: float
    pow_get_llc: float
    pow_get_pv: float
    pow_get_pv2: float
    pow_get_pv_h: float
    pow_get_pv_l: float
    pow_get_qcusb1: float
    pow_get_qcusb2: float
    pow_get_typec1: float
    pow_get_typec2: float
    pow_in_sum_w: float
    pow_out_sum_w: float
    pv_chg_type: int
    pv_dc_chg_setting_list: PvDcChgSettingList
    screen_off_time: int
    serve_middlemen: SERVE_MIDDLEMEN
    silence_chg_watt: int
    sp_charger_car_batt_vol: float
    sp_charger_car_batt_vol_setting: int
    sp_charger_chg_mode: SP_CHARGER_CHG_MODE
    sp_charger_chg_open: bool
    sp_charger_chg_pow_limit: float
    sp_charger_chg_pow_max: float
    sp_charger_is_connect_car: bool
    sp_charger_run_state: int
    storm_pattern_enable: bool
    storm_pattern_end_time: int
    storm_pattern_open_flag: bool
    sys_status: int
    time_task_change_cnt: int
    time_task_conflict_flag: int
    time_task_current: SetTimeTaskWrite
    ups_alram: bool
    utc_set_mode: bool
    utc_timezone: int
    utc_timezone_id: str
    wireless_coordinate_dev_list: WirelessCoordinateList
    wireless_oil_off_soc: int
    wireless_oil_on_soc: int
    wireless_oil_self_start: bool
    xboost_en: bool
    def __init__(
        self,
        errcode: _Optional[int] = ...,
        sys_status: _Optional[int] = ...,
        dev_online_flag: bool = ...,
        utc_timezone: _Optional[int] = ...,
        utc_timezone_id: _Optional[str] = ...,
        utc_set_mode: bool = ...,
        cms_bms_run_state: _Optional[int] = ...,
        cms_batt_soc: _Optional[float] = ...,
        cms_batt_soh: _Optional[float] = ...,
        cms_chg_dsg_state: _Optional[int] = ...,
        cms_batt_full_cap: _Optional[int] = ...,
        cms_batt_design_cap: _Optional[int] = ...,
        cms_batt_remain_cap: _Optional[int] = ...,
        cms_batt_full_energy: _Optional[int] = ...,
        cms_dsg_rem_time: _Optional[int] = ...,
        cms_chg_rem_time: _Optional[int] = ...,
        cms_batt_pow_out_max: _Optional[int] = ...,
        cms_batt_pow_in_max: _Optional[int] = ...,
        cms_batt_temp: _Optional[int] = ...,
        cms_max_chg_soc: _Optional[int] = ...,
        cms_min_dsg_soc: _Optional[int] = ...,
        bms_batt_soc: _Optional[float] = ...,
        bms_batt_soh: _Optional[float] = ...,
        bms_chg_dsg_state: _Optional[int] = ...,
        bms_design_cap: _Optional[int] = ...,
        bms_dsg_rem_time: _Optional[int] = ...,
        bms_chg_rem_time: _Optional[int] = ...,
        bms_min_cell_temp: _Optional[int] = ...,
        bms_max_cell_temp: _Optional[int] = ...,
        bms_min_mos_temp: _Optional[int] = ...,
        bms_max_mos_temp: _Optional[int] = ...,
        dev_sleep_state: _Optional[int] = ...,
        en_beep: bool = ...,
        lcd_light: _Optional[int] = ...,
        ac_out_open: bool = ...,
        btn_ac_out_lv_switch: bool = ...,
        btn_ac_out_hv_switch: bool = ...,
        dc_out_open: bool = ...,
        btn_dc_12v_out_switch: bool = ...,
        btn_usb_switch: bool = ...,
        dev_standby_time: _Optional[int] = ...,
        screen_off_time: _Optional[int] = ...,
        ac_standby_time: _Optional[int] = ...,
        dc_standby_time: _Optional[int] = ...,
        ble_standby_time: _Optional[int] = ...,
        ups_alram: bool = ...,
        led_mode: _Optional[int] = ...,
        low_power_alarm: _Optional[int] = ...,
        silence_chg_watt: _Optional[int] = ...,
        ac_out_freq: _Optional[int] = ...,
        llc_hv_lv_flag: _Optional[int] = ...,
        ac_always_on_flag: bool = ...,
        ac_hv_always_on: bool = ...,
        ac_lv_always_on: bool = ...,
        ac_always_on_mini_soc: _Optional[int] = ...,
        xboost_en: bool = ...,
        output_power_off_memory: bool = ...,
        fast_charge_switch: _Optional[int] = ...,
        llc_GFCI_flag: bool = ...,
        ac_energy_saving_open: bool = ...,
        bypass_out_disable: bool = ...,
        pv_dc_chg_setting_list: _Optional[_Union[PvDcChgSettingList, _Mapping]] = ...,
        pv_chg_type: _Optional[int] = ...,
        energy_backup_state: _Optional[int] = ...,
        energy_backup_start_soc: _Optional[int] = ...,
        energy_backup_en: bool = ...,
        storm_pattern_enable: bool = ...,
        storm_pattern_open_flag: bool = ...,
        storm_pattern_end_time: _Optional[int] = ...,
        time_task_current: _Optional[_Union[SetTimeTaskWrite, _Mapping]] = ...,
        current_time_task_v2_item: _Optional[_Union[TimeTaskItemV2, _Mapping]] = ...,
        time_task_conflict_flag: _Optional[int] = ...,
        time_task_change_cnt: _Optional[int] = ...,
        cms_oil_self_start: bool = ...,
        cms_oil_on_soc: _Optional[int] = ...,
        cms_oil_off_soc: _Optional[int] = ...,
        wireless_oil_self_start: bool = ...,
        wireless_oil_on_soc: _Optional[int] = ...,
        wireless_oil_off_soc: _Optional[int] = ...,
        generator_pv_hybrid_mode_open: bool = ...,
        generator_pv_hybrid_mode_soc_max: _Optional[int] = ...,
        generator_care_mode_open: bool = ...,
        generator_care_mode_start_time: _Optional[int] = ...,
        multi_bp_chg_dsg_mode: _Optional[int] = ...,
        pow_in_sum_w: _Optional[float] = ...,
        pow_out_sum_w: _Optional[float] = ...,
        pow_get_qcusb1: _Optional[float] = ...,
        pow_get_qcusb2: _Optional[float] = ...,
        pow_get_typec1: _Optional[float] = ...,
        pow_get_typec2: _Optional[float] = ...,
        pow_get_pv_h: _Optional[float] = ...,
        pow_get_pv_l: _Optional[float] = ...,
        pow_get_pv: _Optional[float] = ...,
        pow_get_pv2: _Optional[float] = ...,
        pow_get_12v: _Optional[float] = ...,
        pow_get_24v: _Optional[float] = ...,
        pow_get_llc: _Optional[float] = ...,
        pow_get_ac: _Optional[float] = ...,
        pow_get_ac_in: _Optional[float] = ...,
        pow_get_ac_out: _Optional[float] = ...,
        pow_get_ac_hv_out: _Optional[float] = ...,
        pow_get_ac_lv_out: _Optional[float] = ...,
        pow_get_ac_lv_tt30_out: _Optional[float] = ...,
        pow_get_5p8: _Optional[float] = ...,
        pow_get_dc: _Optional[float] = ...,
        pow_get_bms: _Optional[float] = ...,
        pow_get_4p8_1: _Optional[float] = ...,
        pow_get_4p8_2: _Optional[float] = ...,
        pow_get_dcp: _Optional[float] = ...,
        pow_get_dcp2: _Optional[float] = ...,
        pow_get_dc_bidi: _Optional[float] = ...,
        display_statistics_sum: _Optional[
            _Union[DisplayStatisticsRecordList, _Mapping]
        ] = ...,
        flow_info_qcusb1: _Optional[int] = ...,
        flow_info_qcusb2: _Optional[int] = ...,
        flow_info_typec1: _Optional[int] = ...,
        flow_info_typec2: _Optional[int] = ...,
        flow_info_pv_h: _Optional[int] = ...,
        flow_info_pv_l: _Optional[int] = ...,
        flow_info_pv: _Optional[int] = ...,
        flow_info_pv2: _Optional[int] = ...,
        flow_info_12v: _Optional[int] = ...,
        flow_info_24v: _Optional[int] = ...,
        flow_info_ac2dc: _Optional[int] = ...,
        flow_info_dc2ac: _Optional[int] = ...,
        flow_info_ac_in: _Optional[int] = ...,
        flow_info_ac_hv_out: _Optional[int] = ...,
        flow_info_ac_lv_out: _Optional[int] = ...,
        flow_info_5p8_in: _Optional[int] = ...,
        flow_info_5p8_out: _Optional[int] = ...,
        flow_info_ac_out: _Optional[int] = ...,
        flow_info_bms_dsg: _Optional[int] = ...,
        flow_info_bms_chg: _Optional[int] = ...,
        flow_info_4p8_1_in: _Optional[int] = ...,
        flow_info_4p8_1_out: _Optional[int] = ...,
        flow_info_4p8_2_in: _Optional[int] = ...,
        flow_info_4p8_2_out: _Optional[int] = ...,
        flow_info_dcp_in: _Optional[int] = ...,
        flow_info_dcp_out: _Optional[int] = ...,
        flow_info_dcp2_in: _Optional[int] = ...,
        flow_info_dcp2_out: _Optional[int] = ...,
        plug_in_info_pv_h_flag: _Optional[int] = ...,
        plug_in_info_pv_h_type: _Optional[int] = ...,
        plug_in_info_pv_h_charger_flag: bool = ...,
        plug_in_info_pv_h_dc_amp_max: _Optional[int] = ...,
        plug_in_info_pv_h_chg_amp_max: _Optional[int] = ...,
        plug_in_info_pv_h_chg_vol_max: _Optional[int] = ...,
        plug_in_info_pv_l_flag: _Optional[int] = ...,
        plug_in_info_pv_l_type: _Optional[int] = ...,
        plug_in_info_pv_l_charger_flag: bool = ...,
        plug_in_info_pv_l_dc_amp_max: _Optional[int] = ...,
        plug_in_info_pv_l_chg_amp_max: _Optional[int] = ...,
        plug_in_info_pv_l_chg_vol_max: _Optional[int] = ...,
        plug_in_info_pv_flag: bool = ...,
        plug_in_info_pv_type: _Optional[int] = ...,
        plug_in_info_pv_charger_flag: bool = ...,
        plug_in_info_pv_dc_amp_max: _Optional[int] = ...,
        plug_in_info_pv_chg_amp_max: _Optional[int] = ...,
        plug_in_info_pv_chg_vol_max: _Optional[int] = ...,
        plug_in_info_pv_chg_max_list: _Optional[_Union[PvChgMaxList, _Mapping]] = ...,
        plug_in_info_pv2_flag: bool = ...,
        plug_in_info_pv2_type: _Optional[int] = ...,
        plug_in_info_pv2_charger_flag: bool = ...,
        plug_in_info_pv2_dc_amp_max: _Optional[int] = ...,
        plug_in_info_pv2_chg_amp_max: _Optional[int] = ...,
        plug_in_info_pv2_chg_vol_max: _Optional[int] = ...,
        plug_in_info_pv2_chg_max_list: _Optional[_Union[PvChgMaxList, _Mapping]] = ...,
        plug_in_info_ac_in_flag: _Optional[int] = ...,
        plug_in_info_ac_charger_flag: bool = ...,
        plug_in_info_ac_in_feq: _Optional[int] = ...,
        plug_in_info_ac_in_chg_pow_max: _Optional[int] = ...,
        plug_in_info_ac_in_chg_hal_pow_max: _Optional[int] = ...,
        plug_in_info_ac_in_chg_mode: _Optional[_Union[AC_IN_CHG_MODE, str]] = ...,
        plug_in_info_ac_out_dsg_pow_max: _Optional[int] = ...,
        plug_in_info_5p8_chg_pow_max: _Optional[int] = ...,
        plug_in_info_5p8_chg_hal_pow_max: _Optional[int] = ...,
        plug_in_info_5p8_dsg_pow_max: _Optional[int] = ...,
        plug_in_info_5p8_flag: _Optional[int] = ...,
        plug_in_info_5p8_dsg_chg: _Optional[int] = ...,
        plug_in_info_5p8_charger_flag: bool = ...,
        plug_in_info_5p8_type: _Optional[int] = ...,
        plug_in_info_5p8_detail: _Optional[int] = ...,
        plug_in_info_5p8_sn: _Optional[str] = ...,
        plug_in_info_5p8_run_state: _Optional[int] = ...,
        plug_in_info_5p8_err_code: _Optional[int] = ...,
        plug_in_info_5p8_firm_ver: _Optional[int] = ...,
        plug_in_info_5p8_resv: _Optional[_Union[ResvInfo, _Mapping]] = ...,
        plug_in_info_acp_chg_pow_max: _Optional[int] = ...,
        plug_in_info_acp_chg_hal_pow_max: _Optional[int] = ...,
        plug_in_info_acp_dsg_pow_max: _Optional[int] = ...,
        plug_in_info_acp_flag: _Optional[int] = ...,
        plug_in_info_acp_dsg_chg: _Optional[int] = ...,
        plug_in_info_acp_charger_flag: bool = ...,
        plug_in_info_acp_type: _Optional[int] = ...,
        plug_in_info_acp_detail: _Optional[int] = ...,
        plug_in_info_acp_sn: _Optional[str] = ...,
        plug_in_info_acp_run_state: _Optional[int] = ...,
        plug_in_info_acp_err_code: _Optional[int] = ...,
        plug_in_info_acp_firm_ver: _Optional[int] = ...,
        plug_in_info_acp_resv: _Optional[_Union[ResvInfo, _Mapping]] = ...,
        plug_in_info_dc_bidi_flag: bool = ...,
        plug_in_info_dcp_in_flag: bool = ...,
        plug_in_info_dcp_dsg_chg_type: _Optional[int] = ...,
        plug_in_info_dcp_charger_flag: bool = ...,
        plug_in_info_dcp_type: _Optional[int] = ...,
        plug_in_info_dcp_detail: _Optional[int] = ...,
        plug_in_info_dcp_sn: _Optional[str] = ...,
        plug_in_info_dcp_run_state: _Optional[int] = ...,
        plug_in_info_dcp_firm_ver: _Optional[int] = ...,
        plug_in_info_dcp_resv: _Optional[_Union[ResvInfo, _Mapping]] = ...,
        plug_in_info_dcp2_in_flag: bool = ...,
        plug_in_info_dcp2_dsg_chg_type: _Optional[int] = ...,
        plug_in_info_dcp2_charger_flag: bool = ...,
        plug_in_info_dcp2_type: _Optional[int] = ...,
        plug_in_info_dcp2_detail: _Optional[int] = ...,
        plug_in_info_dcp2_sn: _Optional[str] = ...,
        plug_in_info_dcp2_run_state: _Optional[int] = ...,
        plug_in_info_dcp2_firm_ver: _Optional[int] = ...,
        plug_in_info_dcp2_resv: _Optional[_Union[ResvInfo, _Mapping]] = ...,
        plug_in_info_4p8_1_in_flag: _Optional[int] = ...,
        plug_in_info_4p8_1_dsg_chg_type: _Optional[int] = ...,
        plug_in_info_4p8_1_charger_flag: bool = ...,
        plug_in_info_4p8_1_type: _Optional[int] = ...,
        plug_in_info_4p8_1_detail: _Optional[int] = ...,
        plug_in_info_4p8_1_sn: _Optional[str] = ...,
        plug_in_info_4p8_1_run_state: _Optional[int] = ...,
        plug_in_info_4p8_1_err_code: _Optional[int] = ...,
        plug_in_info_4p8_1_firm_ver: _Optional[int] = ...,
        plug_in_info_4p8_1_resv: _Optional[_Union[ResvInfo, _Mapping]] = ...,
        plug_in_info_4p8_2_in_flag: _Optional[int] = ...,
        plug_in_info_4p8_2_dsg_chg_type: _Optional[int] = ...,
        plug_in_info_4p8_2_charger_flag: bool = ...,
        plug_in_info_4p8_2_type: _Optional[int] = ...,
        plug_in_info_4p8_2_detail: _Optional[int] = ...,
        plug_in_info_4p8_2_sn: _Optional[str] = ...,
        plug_in_info_4p8_2_run_state: _Optional[int] = ...,
        plug_in_info_4p8_2_err_code: _Optional[int] = ...,
        plug_in_info_4p8_2_firm_ver: _Optional[int] = ...,
        plug_in_info_4p8_2_resv: _Optional[_Union[ResvInfo, _Mapping]] = ...,
        wireless_coordinate_dev_list: _Optional[
            _Union[WirelessCoordinateList, _Mapping]
        ] = ...,
        pd_err_code: _Optional[int] = ...,
        mppt_err_code: _Optional[int] = ...,
        llc_err_code: _Optional[int] = ...,
        llc_inv_err_code: _Optional[int] = ...,
        dcdc_err_code: _Optional[int] = ...,
        plug_in_info_dcp_err_code: _Optional[int] = ...,
        plug_in_info_dcp2_err_code: _Optional[int] = ...,
        bms_err_code: _Optional[int] = ...,
        inv_err_code: _Optional[int] = ...,
        err_code_record_list: _Optional[_Union[ErrcodeRecordList, _Mapping]] = ...,
        pcs_fan_level: _Optional[int] = ...,
        pcs_fan_err_flag: _Optional[int] = ...,
        generator_fuels_type: _Optional[int] = ...,
        generator_remain_time: _Optional[int] = ...,
        generator_run_time: _Optional[int] = ...,
        generator_total_output: _Optional[int] = ...,
        generator_abnormal_state: _Optional[int] = ...,
        fuels_oil_val: _Optional[int] = ...,
        fuels_liquefied_gas_type: _Optional[int] = ...,
        fuels_liquefied_gas_uint: _Optional[int] = ...,
        fuels_liquefied_gas_val: _Optional[float] = ...,
        fuels_liquefied_gas_consume_per_hour: _Optional[float] = ...,
        fuels_liquefied_gas_remain_val: _Optional[int] = ...,
        fuels_liquefied_gas_lpg_uint: _Optional[int] = ...,
        fuels_liquefied_gas_lng_uint: _Optional[int] = ...,
        generator_perf_mode: _Optional[int] = ...,
        generator_engine_open: _Optional[int] = ...,
        generator_low_power_en: bool = ...,
        generator_low_power_threshold: _Optional[int] = ...,
        generator_lpg_monitor_en: bool = ...,
        generator_out_pow_max: _Optional[int] = ...,
        generator_ac_out_pow_max: _Optional[int] = ...,
        generator_dc_out_pow_max: _Optional[int] = ...,
        generator_sub_battery_temp: _Optional[int] = ...,
        generator_sub_battery_soc: _Optional[int] = ...,
        generator_sub_battery_state: _Optional[int] = ...,
        generator_maintence_state: bool = ...,
        generator_pcs_err_code: _Optional[int] = ...,
        generator_conn_dev_errcode: _Optional[int] = ...,
        sp_charger_chg_mode: _Optional[_Union[SP_CHARGER_CHG_MODE, str]] = ...,
        sp_charger_chg_open: bool = ...,
        sp_charger_chg_pow_limit: _Optional[float] = ...,
        sp_charger_chg_pow_max: _Optional[float] = ...,
        sp_charger_run_state: _Optional[int] = ...,
        sp_charger_is_connect_car: bool = ...,
        sp_charger_car_batt_vol_setting: _Optional[int] = ...,
        sp_charger_car_batt_vol: _Optional[float] = ...,
        module_bluetooth_snr: _Optional[float] = ...,
        module_bluetooth_rssi: _Optional[float] = ...,
        module_wifi_snr: _Optional[float] = ...,
        module_wifi_rssi: _Optional[float] = ...,
        installment_payment_serve_enable: bool = ...,
        serve_middlemen: _Optional[_Union[SERVE_MIDDLEMEN, str]] = ...,
        installment_payment_overdue_limit: _Optional[
            _Union[INSTALLMENT_PAYMENT_OVERDUE_LIMIT, str]
        ] = ...,
        installment_payment_state: _Optional[
            _Union[INSTALLMENT_PAYMENT_STATE, str]
        ] = ...,
        installment_payment_start_utc_time: _Optional[int] = ...,
        installment_payment_overdue_limit_utc_time: _Optional[int] = ...,
    ) -> None: ...

class DisplayStatisticsRecordList(_message.Message):
    __slots__ = ["list_info"]
    LIST_INFO_FIELD_NUMBER: _ClassVar[int]
    list_info: _containers.RepeatedCompositeFieldContainer[StatisticsRecordItem]
    def __init__(
        self,
        list_info: _Optional[_Iterable[_Union[StatisticsRecordItem, _Mapping]]] = ...,
    ) -> None: ...

class ErrcodeRecordItem(_message.Message):
    __slots__ = ["errcode", "errcode_timestamp"]
    ERRCODE_FIELD_NUMBER: _ClassVar[int]
    ERRCODE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    errcode: int
    errcode_timestamp: int
    def __init__(
        self, errcode: _Optional[int] = ..., errcode_timestamp: _Optional[int] = ...
    ) -> None: ...

class ErrcodeRecordList(_message.Message):
    __slots__ = ["list_info"]
    LIST_INFO_FIELD_NUMBER: _ClassVar[int]
    list_info: _containers.RepeatedCompositeFieldContainer[ErrcodeRecordItem]
    def __init__(
        self, list_info: _Optional[_Iterable[_Union[ErrcodeRecordItem, _Mapping]]] = ...
    ) -> None: ...

class EventAck(_message.Message):
    __slots__ = ["event_item_num", "event_seq", "result"]
    EVENT_ITEM_NUM_FIELD_NUMBER: _ClassVar[int]
    EVENT_SEQ_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    event_item_num: int
    event_seq: int
    result: int
    def __init__(
        self,
        result: _Optional[int] = ...,
        event_seq: _Optional[int] = ...,
        event_item_num: _Optional[int] = ...,
    ) -> None: ...

class EventPush(_message.Message):
    __slots__ = ["event_item", "event_seq", "event_ver"]

    class LogItem(_message.Message):
        __slots__ = ["event_detail", "event_no", "ms", "unix_time"]
        EVENT_DETAIL_FIELD_NUMBER: _ClassVar[int]
        EVENT_NO_FIELD_NUMBER: _ClassVar[int]
        MS_FIELD_NUMBER: _ClassVar[int]
        UNIX_TIME_FIELD_NUMBER: _ClassVar[int]
        event_detail: _containers.RepeatedScalarFieldContainer[float]
        event_no: int
        ms: int
        unix_time: int
        def __init__(
            self,
            unix_time: _Optional[int] = ...,
            ms: _Optional[int] = ...,
            event_no: _Optional[int] = ...,
            event_detail: _Optional[_Iterable[float]] = ...,
        ) -> None: ...

    EVENT_ITEM_FIELD_NUMBER: _ClassVar[int]
    EVENT_SEQ_FIELD_NUMBER: _ClassVar[int]
    EVENT_VER_FIELD_NUMBER: _ClassVar[int]
    event_item: _containers.RepeatedCompositeFieldContainer[EventPush.LogItem]
    event_seq: int
    event_ver: int
    def __init__(
        self,
        event_ver: _Optional[int] = ...,
        event_seq: _Optional[int] = ...,
        event_item: _Optional[_Iterable[_Union[EventPush.LogItem, _Mapping]]] = ...,
    ) -> None: ...

class GetAllTimeTaskReadck(_message.Message):
    __slots__ = ["time_task"]
    TIME_TASK_FIELD_NUMBER: _ClassVar[int]
    time_task: _containers.RepeatedCompositeFieldContainer[SetTimeTaskWrite]
    def __init__(
        self, time_task: _Optional[_Iterable[_Union[SetTimeTaskWrite, _Mapping]]] = ...
    ) -> None: ...

class InstallmentPaymentServe(_message.Message):
    __slots__ = [
        "installment_payment_overdue_limit_utc_time",
        "installment_payment_start_utc_time",
        "installment_payment_state",
    ]
    INSTALLMENT_PAYMENT_OVERDUE_LIMIT_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_START_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    installment_payment_overdue_limit_utc_time: int
    installment_payment_start_utc_time: int
    installment_payment_state: INSTALLMENT_PAYMENT_STATE
    def __init__(
        self,
        installment_payment_state: _Optional[
            _Union[INSTALLMENT_PAYMENT_STATE, str]
        ] = ...,
        installment_payment_start_utc_time: _Optional[int] = ...,
        installment_payment_overdue_limit_utc_time: _Optional[int] = ...,
    ) -> None: ...

class InstallmentPaymentServeBelone(_message.Message):
    __slots__ = [
        "installment_payment_overdue_limit",
        "installment_payment_state",
        "serve_middlemen",
    ]
    INSTALLMENT_PAYMENT_OVERDUE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    INSTALLMENT_PAYMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    SERVE_MIDDLEMEN_FIELD_NUMBER: _ClassVar[int]
    installment_payment_overdue_limit: INSTALLMENT_PAYMENT_OVERDUE_LIMIT
    installment_payment_state: INSTALLMENT_PAYMENT_STATE
    serve_middlemen: SERVE_MIDDLEMEN
    def __init__(
        self,
        serve_middlemen: _Optional[_Union[SERVE_MIDDLEMEN, str]] = ...,
        installment_payment_overdue_limit: _Optional[
            _Union[INSTALLMENT_PAYMENT_OVERDUE_LIMIT, str]
        ] = ...,
        installment_payment_state: _Optional[
            _Union[INSTALLMENT_PAYMENT_STATE, str]
        ] = ...,
    ) -> None: ...

class PropertyUploadPeriod(_message.Message):
    __slots__ = [
        "display_property_full_upload_period",
        "display_property_incremental_upload_period",
        "runtime_property_full_upload_period",
        "runtime_property_incremental_upload_period",
    ]
    DISPLAY_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    display_property_full_upload_period: int
    display_property_incremental_upload_period: int
    runtime_property_full_upload_period: int
    runtime_property_incremental_upload_period: int
    def __init__(
        self,
        display_property_full_upload_period: _Optional[int] = ...,
        display_property_incremental_upload_period: _Optional[int] = ...,
        runtime_property_full_upload_period: _Optional[int] = ...,
        runtime_property_incremental_upload_period: _Optional[int] = ...,
    ) -> None: ...

class PvChgMaxItem(_message.Message):
    __slots__ = ["pv_chg_amp_max", "pv_chg_amp_mini", "pv_chg_vol_type"]
    PV_CHG_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    PV_CHG_AMP_MINI_FIELD_NUMBER: _ClassVar[int]
    PV_CHG_VOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    pv_chg_amp_max: int
    pv_chg_amp_mini: int
    pv_chg_vol_type: int
    def __init__(
        self,
        pv_chg_vol_type: _Optional[int] = ...,
        pv_chg_amp_max: _Optional[int] = ...,
        pv_chg_amp_mini: _Optional[int] = ...,
    ) -> None: ...

class PvChgMaxList(_message.Message):
    __slots__ = ["pv_chg_max_item"]
    PV_CHG_MAX_ITEM_FIELD_NUMBER: _ClassVar[int]
    pv_chg_max_item: _containers.RepeatedCompositeFieldContainer[PvChgMaxItem]
    def __init__(
        self,
        pv_chg_max_item: _Optional[_Iterable[_Union[PvChgMaxItem, _Mapping]]] = ...,
    ) -> None: ...

class PvDcChgSetting(_message.Message):
    __slots__ = ["pv_chg_amp_limit", "pv_chg_vol_spec", "pv_plug_index"]
    PV_CHG_AMP_LIMIT_FIELD_NUMBER: _ClassVar[int]
    PV_CHG_VOL_SPEC_FIELD_NUMBER: _ClassVar[int]
    PV_PLUG_INDEX_FIELD_NUMBER: _ClassVar[int]
    pv_chg_amp_limit: int
    pv_chg_vol_spec: PV_CHG_VOL_SPEC
    pv_plug_index: PV_PLUG_INDEX
    def __init__(
        self,
        pv_plug_index: _Optional[_Union[PV_PLUG_INDEX, str]] = ...,
        pv_chg_vol_spec: _Optional[_Union[PV_CHG_VOL_SPEC, str]] = ...,
        pv_chg_amp_limit: _Optional[int] = ...,
    ) -> None: ...

class PvDcChgSettingList(_message.Message):
    __slots__ = ["list_info"]
    LIST_INFO_FIELD_NUMBER: _ClassVar[int]
    list_info: _containers.RepeatedCompositeFieldContainer[PvDcChgSetting]
    def __init__(
        self, list_info: _Optional[_Iterable[_Union[PvDcChgSetting, _Mapping]]] = ...
    ) -> None: ...

class ReqTouStrategy(_message.Message):
    __slots__ = ["req_state"]
    REQ_STATE_FIELD_NUMBER: _ClassVar[int]
    req_state: int
    def __init__(self, req_state: _Optional[int] = ...) -> None: ...

class ResetMiddlemenDeliverySetting(_message.Message):
    __slots__ = ["serve_middlemen"]
    SERVE_MIDDLEMEN_FIELD_NUMBER: _ClassVar[int]
    serve_middlemen: SERVE_MIDDLEMEN
    def __init__(
        self, serve_middlemen: _Optional[_Union[SERVE_MIDDLEMEN, str]] = ...
    ) -> None: ...

class ResvInfo(_message.Message):
    __slots__ = ["resv_info"]
    RESV_INFO_FIELD_NUMBER: _ClassVar[int]
    resv_info: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, resv_info: _Optional[_Iterable[int]] = ...) -> None: ...

class RuntimePropertyUpload(_message.Message):
    __slots__ = [
        "ac_phase_type",
        "ads_ntc_temp",
        "bms_alm_state",
        "bms_alm_state_2",
        "bms_bal_state",
        "bms_batt_amp",
        "bms_batt_vol",
        "bms_err_code",
        "bms_firm_ver",
        "bms_flt_state",
        "bms_full_cap",
        "bms_high_temp_icon",
        "bms_limit_icon",
        "bms_low_temp_icon",
        "bms_max_cell_vol",
        "bms_min_cell_vol",
        "bms_overload_icon",
        "bms_pro_state",
        "bms_pro_state_2",
        "bms_remain_cap",
        "bms_warn_icon",
        "cms_batt_amp",
        "cms_batt_vol",
        "cms_chg_req_amp",
        "cms_chg_req_vol",
        "dcdc_chg_req_cur",
        "dcdc_firm_ver",
        "display_property_full_upload_period",
        "display_property_incremental_upload_period",
        "generator_commc_cnt_ems_to_psdr",
        "generator_commc_cnt_psdr_to_ems",
        "generator_engine_activation_cnt",
        "generator_engine_head_temp",
        "generator_engine_oil_val",
        "generator_engine_spd",
        "generator_oil_val_real",
        "generator_pcs_bus_amp",
        "generator_pcs_bus_vol",
        "generator_pcs_fan_level",
        "generator_pcs_fules_type",
        "generator_pcs_temp1",
        "generator_pcs_temp2",
        "generator_run_state",
        "generator_sub_battery_amp",
        "generator_sub_battery_vol",
        "inv_bus_vol",
        "inv_firm_ver",
        "inv_main_fsmstate",
        "inv_monitor_flag",
        "inv_ntc_temp2",
        "inv_ntc_temp3",
        "inv_to_llc_ac_pow_lim",
        "iot_firm_ver",
        "l1_main_fsmstate",
        "l2_main_fsmstate",
        "llc_bat_cur",
        "llc_bat_vol",
        "llc_bus_vol",
        "llc_firm_ver",
        "llc_fsmstate",
        "llc_inv_firm_ver",
        "llc_monitor_flag",
        "llc_ntc_temp",
        "llc_recv_cms_chg_req_vol",
        "mppt_bat_amp",
        "mppt_bat_vol",
        "mppt_fanspeed",
        "mppt_firm_ver",
        "mppt_hardware_ver",
        "mppt_monitor_flag",
        "mppt_recv_cms_chg_req_amp",
        "mppt_recv_cms_chg_req_vol",
        "pcs_work_mode",
        "pd_bms_comm_err",
        "pd_dcdc_comm_err",
        "pd_firm_ver",
        "pd_inv_comm_err",
        "pd_iot_comm_err",
        "pd_llc_comm_err",
        "pd_mppt_comm_err",
        "pd_skt_ocp1",
        "pd_skt_ocp2",
        "pd_skt_ocp3",
        "pd_skt_ocp4",
        "pd_skt_ocp5",
        "pd_to_inv_dsg_mode",
        "plug_in_info_12v_amp",
        "plug_in_info_12v_vol",
        "plug_in_info_24v_amp",
        "plug_in_info_24v_vol",
        "plug_in_info_4p8_1_amp",
        "plug_in_info_4p8_1_vol",
        "plug_in_info_4p8_2_amp",
        "plug_in_info_4p8_2_vol",
        "plug_in_info_5p8_amp",
        "plug_in_info_5p8_freq",
        "plug_in_info_5p8_vol",
        "plug_in_info_ac_in_amp",
        "plug_in_info_ac_in_vol",
        "plug_in_info_ac_out_amp",
        "plug_in_info_ac_out_freq",
        "plug_in_info_ac_out_type",
        "plug_in_info_ac_out_vol",
        "plug_in_info_acp_amp",
        "plug_in_info_acp_freq",
        "plug_in_info_acp_l1_vol",
        "plug_in_info_acp_l1l2_vol",
        "plug_in_info_acp_vol",
        "plug_in_info_bms_vol",
        "plug_in_info_dc_bidi_amp",
        "plug_in_info_dc_bidi_vol",
        "plug_in_info_dcp2_amp",
        "plug_in_info_dcp2_vol",
        "plug_in_info_dcp_amp",
        "plug_in_info_dcp_vol",
        "plug_in_info_l1_amp",
        "plug_in_info_l1_vol",
        "plug_in_info_l2_amp",
        "plug_in_info_l2_vol",
        "plug_in_info_pfc_out_vol",
        "plug_in_info_pv2_amp",
        "plug_in_info_pv2_vol",
        "plug_in_info_pv_amp",
        "plug_in_info_pv_h_amp",
        "plug_in_info_pv_h_vol",
        "plug_in_info_pv_l_amp",
        "plug_in_info_pv_l_vol",
        "plug_in_info_pv_vol",
        "pow_get_l1",
        "pow_get_l2",
        "pv2_bus_vol",
        "pv2_pause_cnt",
        "pv2_vin_ref",
        "pv_pause_cnt",
        "pv_vin_ref",
        "runtime_property_full_upload_period",
        "runtime_property_incremental_upload_period",
        "runtime_statistics_sum",
        "temp_pcs_ac",
        "temp_pcs_dc",
        "temp_pv",
        "temp_pv2",
        "temp_pv_h",
        "temp_pv_l",
    ]
    AC_PHASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ADS_NTC_TEMP_FIELD_NUMBER: _ClassVar[int]
    BMS_ALM_STATE_2_FIELD_NUMBER: _ClassVar[int]
    BMS_ALM_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_BAL_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_BATT_AMP_FIELD_NUMBER: _ClassVar[int]
    BMS_BATT_VOL_FIELD_NUMBER: _ClassVar[int]
    BMS_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    BMS_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    BMS_FLT_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_FULL_CAP_FIELD_NUMBER: _ClassVar[int]
    BMS_HIGH_TEMP_ICON_FIELD_NUMBER: _ClassVar[int]
    BMS_LIMIT_ICON_FIELD_NUMBER: _ClassVar[int]
    BMS_LOW_TEMP_ICON_FIELD_NUMBER: _ClassVar[int]
    BMS_MAX_CELL_VOL_FIELD_NUMBER: _ClassVar[int]
    BMS_MIN_CELL_VOL_FIELD_NUMBER: _ClassVar[int]
    BMS_OVERLOAD_ICON_FIELD_NUMBER: _ClassVar[int]
    BMS_PRO_STATE_2_FIELD_NUMBER: _ClassVar[int]
    BMS_PRO_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_REMAIN_CAP_FIELD_NUMBER: _ClassVar[int]
    BMS_WARN_ICON_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_AMP_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_VOL_FIELD_NUMBER: _ClassVar[int]
    CMS_CHG_REQ_AMP_FIELD_NUMBER: _ClassVar[int]
    CMS_CHG_REQ_VOL_FIELD_NUMBER: _ClassVar[int]
    DCDC_CHG_REQ_CUR_FIELD_NUMBER: _ClassVar[int]
    DCDC_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_COMMC_CNT_EMS_TO_PSDR_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_COMMC_CNT_PSDR_TO_EMS_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_ENGINE_ACTIVATION_CNT_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_ENGINE_HEAD_TEMP_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_ENGINE_OIL_VAL_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_ENGINE_SPD_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_OIL_VAL_REAL_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PCS_BUS_AMP_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PCS_BUS_VOL_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PCS_FAN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PCS_FULES_TYPE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PCS_TEMP1_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_PCS_TEMP2_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_SUB_BATTERY_AMP_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_SUB_BATTERY_VOL_FIELD_NUMBER: _ClassVar[int]
    INV_BUS_VOL_FIELD_NUMBER: _ClassVar[int]
    INV_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    INV_MAIN_FSMSTATE_FIELD_NUMBER: _ClassVar[int]
    INV_MONITOR_FLAG_FIELD_NUMBER: _ClassVar[int]
    INV_NTC_TEMP2_FIELD_NUMBER: _ClassVar[int]
    INV_NTC_TEMP3_FIELD_NUMBER: _ClassVar[int]
    INV_TO_LLC_AC_POW_LIM_FIELD_NUMBER: _ClassVar[int]
    IOT_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    L1_MAIN_FSMSTATE_FIELD_NUMBER: _ClassVar[int]
    L2_MAIN_FSMSTATE_FIELD_NUMBER: _ClassVar[int]
    LLC_BAT_CUR_FIELD_NUMBER: _ClassVar[int]
    LLC_BAT_VOL_FIELD_NUMBER: _ClassVar[int]
    LLC_BUS_VOL_FIELD_NUMBER: _ClassVar[int]
    LLC_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    LLC_FSMSTATE_FIELD_NUMBER: _ClassVar[int]
    LLC_INV_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    LLC_MONITOR_FLAG_FIELD_NUMBER: _ClassVar[int]
    LLC_NTC_TEMP_FIELD_NUMBER: _ClassVar[int]
    LLC_RECV_CMS_CHG_REQ_VOL_FIELD_NUMBER: _ClassVar[int]
    MPPT_BAT_AMP_FIELD_NUMBER: _ClassVar[int]
    MPPT_BAT_VOL_FIELD_NUMBER: _ClassVar[int]
    MPPT_FANSPEED_FIELD_NUMBER: _ClassVar[int]
    MPPT_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    MPPT_HARDWARE_VER_FIELD_NUMBER: _ClassVar[int]
    MPPT_MONITOR_FLAG_FIELD_NUMBER: _ClassVar[int]
    MPPT_RECV_CMS_CHG_REQ_AMP_FIELD_NUMBER: _ClassVar[int]
    MPPT_RECV_CMS_CHG_REQ_VOL_FIELD_NUMBER: _ClassVar[int]
    PCS_WORK_MODE_FIELD_NUMBER: _ClassVar[int]
    PD_BMS_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_DCDC_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PD_INV_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_IOT_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_LLC_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_MPPT_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_SKT_OCP1_FIELD_NUMBER: _ClassVar[int]
    PD_SKT_OCP2_FIELD_NUMBER: _ClassVar[int]
    PD_SKT_OCP3_FIELD_NUMBER: _ClassVar[int]
    PD_SKT_OCP4_FIELD_NUMBER: _ClassVar[int]
    PD_SKT_OCP5_FIELD_NUMBER: _ClassVar[int]
    PD_TO_INV_DSG_MODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_12V_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_12V_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_24V_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_24V_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_1_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_4P8_2_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_FREQ_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_5P8_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_FREQ_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_L1L2_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_L1_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_ACP_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_BMS_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP2_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DC_BIDI_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DC_BIDI_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_L1_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_L1_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_L2_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_L2_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PFC_OUT_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_H_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_L_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_VOL_FIELD_NUMBER: _ClassVar[int]
    POW_GET_L1_FIELD_NUMBER: _ClassVar[int]
    POW_GET_L2_FIELD_NUMBER: _ClassVar[int]
    PV2_BUS_VOL_FIELD_NUMBER: _ClassVar[int]
    PV2_PAUSE_CNT_FIELD_NUMBER: _ClassVar[int]
    PV2_VIN_REF_FIELD_NUMBER: _ClassVar[int]
    PV_PAUSE_CNT_FIELD_NUMBER: _ClassVar[int]
    PV_VIN_REF_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_STATISTICS_SUM_FIELD_NUMBER: _ClassVar[int]
    TEMP_PCS_AC_FIELD_NUMBER: _ClassVar[int]
    TEMP_PCS_DC_FIELD_NUMBER: _ClassVar[int]
    TEMP_PV2_FIELD_NUMBER: _ClassVar[int]
    TEMP_PV_FIELD_NUMBER: _ClassVar[int]
    TEMP_PV_H_FIELD_NUMBER: _ClassVar[int]
    TEMP_PV_L_FIELD_NUMBER: _ClassVar[int]
    ac_phase_type: int
    ads_ntc_temp: int
    bms_alm_state: int
    bms_alm_state_2: int
    bms_bal_state: int
    bms_batt_amp: float
    bms_batt_vol: float
    bms_err_code: int
    bms_firm_ver: int
    bms_flt_state: int
    bms_full_cap: int
    bms_high_temp_icon: int
    bms_limit_icon: int
    bms_low_temp_icon: int
    bms_max_cell_vol: int
    bms_min_cell_vol: int
    bms_overload_icon: int
    bms_pro_state: int
    bms_pro_state_2: int
    bms_remain_cap: int
    bms_warn_icon: int
    cms_batt_amp: float
    cms_batt_vol: float
    cms_chg_req_amp: float
    cms_chg_req_vol: float
    dcdc_chg_req_cur: float
    dcdc_firm_ver: int
    display_property_full_upload_period: int
    display_property_incremental_upload_period: int
    generator_commc_cnt_ems_to_psdr: int
    generator_commc_cnt_psdr_to_ems: int
    generator_engine_activation_cnt: int
    generator_engine_head_temp: int
    generator_engine_oil_val: int
    generator_engine_spd: int
    generator_oil_val_real: int
    generator_pcs_bus_amp: float
    generator_pcs_bus_vol: float
    generator_pcs_fan_level: int
    generator_pcs_fules_type: int
    generator_pcs_temp1: int
    generator_pcs_temp2: int
    generator_run_state: int
    generator_sub_battery_amp: int
    generator_sub_battery_vol: int
    inv_bus_vol: float
    inv_firm_ver: int
    inv_main_fsmstate: int
    inv_monitor_flag: int
    inv_ntc_temp2: int
    inv_ntc_temp3: int
    inv_to_llc_ac_pow_lim: float
    iot_firm_ver: int
    l1_main_fsmstate: int
    l2_main_fsmstate: int
    llc_bat_cur: float
    llc_bat_vol: float
    llc_bus_vol: float
    llc_firm_ver: int
    llc_fsmstate: int
    llc_inv_firm_ver: int
    llc_monitor_flag: int
    llc_ntc_temp: int
    llc_recv_cms_chg_req_vol: float
    mppt_bat_amp: float
    mppt_bat_vol: float
    mppt_fanspeed: int
    mppt_firm_ver: int
    mppt_hardware_ver: int
    mppt_monitor_flag: int
    mppt_recv_cms_chg_req_amp: float
    mppt_recv_cms_chg_req_vol: float
    pcs_work_mode: int
    pd_bms_comm_err: bool
    pd_dcdc_comm_err: bool
    pd_firm_ver: int
    pd_inv_comm_err: bool
    pd_iot_comm_err: bool
    pd_llc_comm_err: bool
    pd_mppt_comm_err: bool
    pd_skt_ocp1: float
    pd_skt_ocp2: float
    pd_skt_ocp3: float
    pd_skt_ocp4: float
    pd_skt_ocp5: float
    pd_to_inv_dsg_mode: int
    plug_in_info_12v_amp: float
    plug_in_info_12v_vol: float
    plug_in_info_24v_amp: float
    plug_in_info_24v_vol: float
    plug_in_info_4p8_1_amp: float
    plug_in_info_4p8_1_vol: float
    plug_in_info_4p8_2_amp: float
    plug_in_info_4p8_2_vol: float
    plug_in_info_5p8_amp: float
    plug_in_info_5p8_freq: int
    plug_in_info_5p8_vol: float
    plug_in_info_ac_in_amp: float
    plug_in_info_ac_in_vol: float
    plug_in_info_ac_out_amp: float
    plug_in_info_ac_out_freq: int
    plug_in_info_ac_out_type: int
    plug_in_info_ac_out_vol: float
    plug_in_info_acp_amp: float
    plug_in_info_acp_freq: int
    plug_in_info_acp_l1_vol: float
    plug_in_info_acp_l1l2_vol: float
    plug_in_info_acp_vol: float
    plug_in_info_bms_vol: float
    plug_in_info_dc_bidi_amp: float
    plug_in_info_dc_bidi_vol: float
    plug_in_info_dcp2_amp: float
    plug_in_info_dcp2_vol: float
    plug_in_info_dcp_amp: float
    plug_in_info_dcp_vol: float
    plug_in_info_l1_amp: float
    plug_in_info_l1_vol: float
    plug_in_info_l2_amp: float
    plug_in_info_l2_vol: float
    plug_in_info_pfc_out_vol: float
    plug_in_info_pv2_amp: float
    plug_in_info_pv2_vol: float
    plug_in_info_pv_amp: float
    plug_in_info_pv_h_amp: float
    plug_in_info_pv_h_vol: float
    plug_in_info_pv_l_amp: float
    plug_in_info_pv_l_vol: float
    plug_in_info_pv_vol: float
    pow_get_l1: float
    pow_get_l2: float
    pv2_bus_vol: float
    pv2_pause_cnt: int
    pv2_vin_ref: float
    pv_pause_cnt: int
    pv_vin_ref: float
    runtime_property_full_upload_period: int
    runtime_property_incremental_upload_period: int
    runtime_statistics_sum: RuntimeStatisticsRecordList
    temp_pcs_ac: float
    temp_pcs_dc: float
    temp_pv: float
    temp_pv2: float
    temp_pv_h: float
    temp_pv_l: float
    def __init__(
        self,
        display_property_full_upload_period: _Optional[int] = ...,
        display_property_incremental_upload_period: _Optional[int] = ...,
        runtime_property_full_upload_period: _Optional[int] = ...,
        runtime_property_incremental_upload_period: _Optional[int] = ...,
        cms_batt_vol: _Optional[float] = ...,
        cms_batt_amp: _Optional[float] = ...,
        cms_chg_req_vol: _Optional[float] = ...,
        cms_chg_req_amp: _Optional[float] = ...,
        bms_firm_ver: _Optional[int] = ...,
        bms_batt_vol: _Optional[float] = ...,
        bms_batt_amp: _Optional[float] = ...,
        bms_bal_state: _Optional[int] = ...,
        bms_full_cap: _Optional[int] = ...,
        bms_remain_cap: _Optional[int] = ...,
        bms_alm_state: _Optional[int] = ...,
        bms_alm_state_2: _Optional[int] = ...,
        bms_pro_state: _Optional[int] = ...,
        bms_pro_state_2: _Optional[int] = ...,
        bms_flt_state: _Optional[int] = ...,
        bms_err_code: _Optional[int] = ...,
        bms_min_cell_vol: _Optional[int] = ...,
        bms_max_cell_vol: _Optional[int] = ...,
        ac_phase_type: _Optional[int] = ...,
        pcs_work_mode: _Optional[int] = ...,
        runtime_statistics_sum: _Optional[
            _Union[RuntimeStatisticsRecordList, _Mapping]
        ] = ...,
        plug_in_info_pv_h_vol: _Optional[float] = ...,
        plug_in_info_pv_h_amp: _Optional[float] = ...,
        plug_in_info_pv_l_vol: _Optional[float] = ...,
        plug_in_info_pv_l_amp: _Optional[float] = ...,
        plug_in_info_pv_vol: _Optional[float] = ...,
        plug_in_info_pv_amp: _Optional[float] = ...,
        plug_in_info_pv2_vol: _Optional[float] = ...,
        plug_in_info_pv2_amp: _Optional[float] = ...,
        plug_in_info_ac_in_vol: _Optional[float] = ...,
        plug_in_info_ac_in_amp: _Optional[float] = ...,
        plug_in_info_ac_out_type: _Optional[int] = ...,
        plug_in_info_ac_out_freq: _Optional[int] = ...,
        plug_in_info_ac_out_vol: _Optional[float] = ...,
        plug_in_info_ac_out_amp: _Optional[float] = ...,
        plug_in_info_5p8_vol: _Optional[float] = ...,
        plug_in_info_5p8_amp: _Optional[float] = ...,
        plug_in_info_5p8_freq: _Optional[int] = ...,
        plug_in_info_acp_vol: _Optional[float] = ...,
        plug_in_info_acp_amp: _Optional[float] = ...,
        plug_in_info_acp_freq: _Optional[int] = ...,
        plug_in_info_12v_vol: _Optional[float] = ...,
        plug_in_info_12v_amp: _Optional[float] = ...,
        plug_in_info_bms_vol: _Optional[float] = ...,
        plug_in_info_dc_bidi_vol: _Optional[float] = ...,
        plug_in_info_dc_bidi_amp: _Optional[float] = ...,
        plug_in_info_dcp_vol: _Optional[float] = ...,
        plug_in_info_dcp_amp: _Optional[float] = ...,
        plug_in_info_dcp2_vol: _Optional[float] = ...,
        plug_in_info_dcp2_amp: _Optional[float] = ...,
        plug_in_info_4p8_1_vol: _Optional[float] = ...,
        plug_in_info_4p8_1_amp: _Optional[float] = ...,
        plug_in_info_4p8_2_vol: _Optional[float] = ...,
        plug_in_info_4p8_2_amp: _Optional[float] = ...,
        pd_mppt_comm_err: bool = ...,
        pd_llc_comm_err: bool = ...,
        pd_bms_comm_err: bool = ...,
        pd_iot_comm_err: bool = ...,
        pd_dcdc_comm_err: bool = ...,
        pd_inv_comm_err: bool = ...,
        pd_firm_ver: _Optional[int] = ...,
        iot_firm_ver: _Optional[int] = ...,
        mppt_firm_ver: _Optional[int] = ...,
        llc_firm_ver: _Optional[int] = ...,
        llc_inv_firm_ver: _Optional[int] = ...,
        dcdc_firm_ver: _Optional[int] = ...,
        inv_firm_ver: _Optional[int] = ...,
        temp_pcs_dc: _Optional[float] = ...,
        temp_pcs_ac: _Optional[float] = ...,
        temp_pv_h: _Optional[float] = ...,
        temp_pv_l: _Optional[float] = ...,
        temp_pv: _Optional[float] = ...,
        temp_pv2: _Optional[float] = ...,
        bms_overload_icon: _Optional[int] = ...,
        bms_warn_icon: _Optional[int] = ...,
        bms_high_temp_icon: _Optional[int] = ...,
        bms_low_temp_icon: _Optional[int] = ...,
        bms_limit_icon: _Optional[int] = ...,
        generator_run_state: _Optional[int] = ...,
        generator_oil_val_real: _Optional[int] = ...,
        generator_engine_spd: _Optional[int] = ...,
        generator_engine_oil_val: _Optional[int] = ...,
        generator_engine_activation_cnt: _Optional[int] = ...,
        generator_engine_head_temp: _Optional[int] = ...,
        generator_sub_battery_vol: _Optional[int] = ...,
        generator_sub_battery_amp: _Optional[int] = ...,
        generator_commc_cnt_ems_to_psdr: _Optional[int] = ...,
        generator_commc_cnt_psdr_to_ems: _Optional[int] = ...,
        generator_pcs_fan_level: _Optional[int] = ...,
        generator_pcs_bus_vol: _Optional[float] = ...,
        generator_pcs_bus_amp: _Optional[float] = ...,
        generator_pcs_temp1: _Optional[int] = ...,
        generator_pcs_temp2: _Optional[int] = ...,
        generator_pcs_fules_type: _Optional[int] = ...,
        plug_in_info_24v_vol: _Optional[float] = ...,
        plug_in_info_24v_amp: _Optional[float] = ...,
        plug_in_info_l1_vol: _Optional[float] = ...,
        plug_in_info_l1_amp: _Optional[float] = ...,
        plug_in_info_l2_vol: _Optional[float] = ...,
        plug_in_info_l2_amp: _Optional[float] = ...,
        plug_in_info_acp_l1_vol: _Optional[float] = ...,
        plug_in_info_acp_l1l2_vol: _Optional[float] = ...,
        mppt_monitor_flag: _Optional[int] = ...,
        mppt_recv_cms_chg_req_vol: _Optional[float] = ...,
        mppt_recv_cms_chg_req_amp: _Optional[float] = ...,
        pv_vin_ref: _Optional[float] = ...,
        pv2_vin_ref: _Optional[float] = ...,
        pv2_bus_vol: _Optional[float] = ...,
        mppt_bat_vol: _Optional[float] = ...,
        mppt_bat_amp: _Optional[float] = ...,
        pv_pause_cnt: _Optional[int] = ...,
        pv2_pause_cnt: _Optional[int] = ...,
        mppt_fanspeed: _Optional[int] = ...,
        ads_ntc_temp: _Optional[int] = ...,
        mppt_hardware_ver: _Optional[int] = ...,
        inv_monitor_flag: _Optional[int] = ...,
        inv_main_fsmstate: _Optional[int] = ...,
        l1_main_fsmstate: _Optional[int] = ...,
        l2_main_fsmstate: _Optional[int] = ...,
        plug_in_info_pfc_out_vol: _Optional[float] = ...,
        pow_get_l1: _Optional[float] = ...,
        pow_get_l2: _Optional[float] = ...,
        inv_bus_vol: _Optional[float] = ...,
        inv_ntc_temp2: _Optional[int] = ...,
        inv_ntc_temp3: _Optional[int] = ...,
        llc_monitor_flag: _Optional[int] = ...,
        llc_ntc_temp: _Optional[int] = ...,
        llc_fsmstate: _Optional[int] = ...,
        pd_to_inv_dsg_mode: _Optional[int] = ...,
        dcdc_chg_req_cur: _Optional[float] = ...,
        llc_recv_cms_chg_req_vol: _Optional[float] = ...,
        inv_to_llc_ac_pow_lim: _Optional[float] = ...,
        llc_bat_vol: _Optional[float] = ...,
        llc_bat_cur: _Optional[float] = ...,
        llc_bus_vol: _Optional[float] = ...,
        pd_skt_ocp1: _Optional[float] = ...,
        pd_skt_ocp2: _Optional[float] = ...,
        pd_skt_ocp3: _Optional[float] = ...,
        pd_skt_ocp4: _Optional[float] = ...,
        pd_skt_ocp5: _Optional[float] = ...,
    ) -> None: ...

class RuntimeStatisticsRecordList(_message.Message):
    __slots__ = ["list_info"]
    LIST_INFO_FIELD_NUMBER: _ClassVar[int]
    list_info: _containers.RepeatedCompositeFieldContainer[StatisticsRecordItem]
    def __init__(
        self,
        list_info: _Optional[_Iterable[_Union[StatisticsRecordItem, _Mapping]]] = ...,
    ) -> None: ...

class SetTimeTaskWrite(_message.Message):
    __slots__ = [
        "conflict_flag",
        "is_cfg",
        "is_enable",
        "is_valid",
        "task_index",
        "time_mode",
        "time_param",
        "time_table",
        "type",
    ]
    CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    IS_CFG_FIELD_NUMBER: _ClassVar[int]
    IS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    TASK_INDEX_FIELD_NUMBER: _ClassVar[int]
    TIME_MODE_FIELD_NUMBER: _ClassVar[int]
    TIME_PARAM_FIELD_NUMBER: _ClassVar[int]
    TIME_TABLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    conflict_flag: int
    is_cfg: bool
    is_enable: bool
    is_valid: bool
    task_index: int
    time_mode: int
    time_param: int
    time_table: _containers.RepeatedScalarFieldContainer[int]
    type: int
    def __init__(
        self,
        task_index: _Optional[int] = ...,
        is_valid: bool = ...,
        is_cfg: bool = ...,
        is_enable: bool = ...,
        conflict_flag: _Optional[int] = ...,
        type: _Optional[int] = ...,
        time_mode: _Optional[int] = ...,
        time_param: _Optional[int] = ...,
        time_table: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class SetTimeTaskWriteAck(_message.Message):
    __slots__ = ["sta", "task_index", "type"]
    STA_FIELD_NUMBER: _ClassVar[int]
    TASK_INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    sta: int
    task_index: int
    type: int
    def __init__(
        self,
        task_index: _Optional[int] = ...,
        type: _Optional[int] = ...,
        sta: _Optional[int] = ...,
    ) -> None: ...

class StatisticsRecordItem(_message.Message):
    __slots__ = ["statistics_content", "statistics_object"]
    STATISTICS_CONTENT_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_OBJECT_FIELD_NUMBER: _ClassVar[int]
    statistics_content: int
    statistics_object: STATISTICS_OBJECT
    def __init__(
        self,
        statistics_object: _Optional[_Union[STATISTICS_OBJECT, str]] = ...,
        statistics_content: _Optional[int] = ...,
    ) -> None: ...

class TimeTaskItemV2(_message.Message):
    __slots__ = [
        "conflict_flag",
        "is_cfg",
        "is_enable",
        "task_index",
        "task_param",
        "task_param_detail",
        "task_type",
        "time_mode",
        "time_param",
        "time_table",
    ]
    CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    IS_CFG_FIELD_NUMBER: _ClassVar[int]
    IS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    TASK_INDEX_FIELD_NUMBER: _ClassVar[int]
    TASK_PARAM_DETAIL_FIELD_NUMBER: _ClassVar[int]
    TASK_PARAM_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_MODE_FIELD_NUMBER: _ClassVar[int]
    TIME_PARAM_FIELD_NUMBER: _ClassVar[int]
    TIME_TABLE_FIELD_NUMBER: _ClassVar[int]
    conflict_flag: int
    is_cfg: bool
    is_enable: bool
    task_index: int
    task_param: int
    task_param_detail: _containers.RepeatedCompositeFieldContainer[TimeTaskParamDetail]
    task_type: TIME_TASK_TYPE
    time_mode: TIME_TASK_MODE
    time_param: int
    time_table: int
    def __init__(
        self,
        task_index: _Optional[int] = ...,
        is_cfg: bool = ...,
        is_enable: bool = ...,
        conflict_flag: _Optional[int] = ...,
        time_mode: _Optional[_Union[TIME_TASK_MODE, str]] = ...,
        time_param: _Optional[int] = ...,
        time_table: _Optional[int] = ...,
        task_type: _Optional[_Union[TIME_TASK_TYPE, str]] = ...,
        task_param: _Optional[int] = ...,
        task_param_detail: _Optional[
            _Iterable[_Union[TimeTaskParamDetail, _Mapping]]
        ] = ...,
    ) -> None: ...

class TimeTaskItemV2List(_message.Message):
    __slots__ = ["time_task"]
    TIME_TASK_FIELD_NUMBER: _ClassVar[int]
    time_task: _containers.RepeatedCompositeFieldContainer[TimeTaskItemV2]
    def __init__(
        self, time_task: _Optional[_Iterable[_Union[TimeTaskItemV2, _Mapping]]] = ...
    ) -> None: ...

class TimeTaskParamDetail(_message.Message):
    __slots__ = ["type", "val"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    type: TIME_TASK_DETAIL_TYPE
    val: float
    def __init__(
        self,
        type: _Optional[_Union[TIME_TASK_DETAIL_TYPE, str]] = ...,
        val: _Optional[float] = ...,
    ) -> None: ...

class WirelessCoordinateList(_message.Message):
    __slots__ = [
        "connect_flag",
        "dev_detail",
        "dev_err_code",
        "dev_firm_ver",
        "dev_sn",
        "dev_type",
    ]
    CONNECT_FLAG_FIELD_NUMBER: _ClassVar[int]
    DEV_DETAIL_FIELD_NUMBER: _ClassVar[int]
    DEV_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    DEV_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    DEV_SN_FIELD_NUMBER: _ClassVar[int]
    DEV_TYPE_FIELD_NUMBER: _ClassVar[int]
    connect_flag: bool
    dev_detail: int
    dev_err_code: int
    dev_firm_ver: int
    dev_sn: str
    dev_type: int
    def __init__(
        self,
        connect_flag: bool = ...,
        dev_type: _Optional[int] = ...,
        dev_detail: _Optional[int] = ...,
        dev_sn: _Optional[str] = ...,
        dev_firm_ver: _Optional[int] = ...,
        dev_err_code: _Optional[int] = ...,
    ) -> None: ...

class MODULE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SP_CHARGER_CHG_MODE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SERVE_MIDDLEMEN(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class INSTALLMENT_PAYMENT_STATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class INSTALLMENT_PAYMENT_OVERDUE_LIMIT(
    int, metaclass=_enum_type_wrapper.EnumTypeWrapper
):
    __slots__ = []

class STATISTICS_OBJECT(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class AC_IN_CHG_MODE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PV_PLUG_INDEX(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PV_CHG_VOL_SPEC(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TIME_TASK_MODE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TIME_TASK_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TIME_TASK_DETAIL_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
