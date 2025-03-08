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
MODULE_TYPE_EF: MODULE_TYPE
PV_CHG_VOL_SPEC_12V: PV_CHG_VOL_SPEC
PV_CHG_VOL_SPEC_24V: PV_CHG_VOL_SPEC
PV_CHG_VOL_SPEC_48V: PV_CHG_VOL_SPEC
PV_CHG_VOL_SPEC_RESV: PV_CHG_VOL_SPEC
PV_PLUG_INDEX_1: PV_PLUG_INDEX
PV_PLUG_INDEX_2: PV_PLUG_INDEX
PV_PLUG_INDEX_RESV: PV_PLUG_INDEX
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
    __slots__ = ["cfg_utc_time", "cfg_utc_timezone", "get_time_task_list"]
    CFG_UTC_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    CFG_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    GET_TIME_TASK_LIST_FIELD_NUMBER: _ClassVar[int]
    cfg_utc_time: int
    cfg_utc_timezone: int
    get_time_task_list: GetAllTimeTaskReadck
    def __init__(
        self,
        cfg_utc_time: _Optional[int] = ...,
        cfg_utc_timezone: _Optional[int] = ...,
        get_time_task_list: _Optional[_Union[GetAllTimeTaskReadck, _Mapping]] = ...,
    ) -> None: ...

class ConfigWrite(_message.Message):
    __slots__ = [
        "active_display_property_full_upload",
        "active_runtime_property_full_upload",
        "cfg_ac_in_chg_mode",
        "cfg_ac_out_always_on",
        "cfg_ac_out_freq",
        "cfg_ac_out_open",
        "cfg_ac_standby_time",
        "cfg_backup_reverse_soc",
        "cfg_beep",
        "cfg_beep_en",
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
        "cfg_generator_care_mode",
        "cfg_generator_mppt_hybrid_mode",
        "cfg_lcd_light",
        "cfg_max_chg_soc",
        "cfg_min_dsg_soc",
        "cfg_output_power_off_memory",
        "cfg_plug_in_info_ac_in_chg_pow_max",
        "cfg_plug_in_info_pv_dc_amp_max",
        "cfg_power_off",
        "cfg_power_on",
        "cfg_pv_dc_chg_setting",
        "cfg_runtime_property_full_upload_period",
        "cfg_runtime_property_incremental_upload_period",
        "cfg_screen_off_time",
        "cfg_soc_cali",
        "cfg_storm_pattern",
        "cfg_tou_strategy",
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
        "set_time_task",
    ]
    ACTIVE_DISPLAY_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_RUNTIME_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_IN_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_BACKUP_REVERSE_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_FIELD_NUMBER: _ClassVar[int]
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
    CFG_GENERATOR_CARE_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_MPPT_HYBRID_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_LCD_LIGHT_FIELD_NUMBER: _ClassVar[int]
    CFG_MAX_CHG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_MIN_DSG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_OUTPUT_POWER_OFF_MEMORY_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_AC_IN_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_OFF_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_PV_DC_CHG_SETTING_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_SCREEN_OFF_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_SOC_CALI_FIELD_NUMBER: _ClassVar[int]
    CFG_STORM_PATTERN_FIELD_NUMBER: _ClassVar[int]
    CFG_TOU_STRATEGY_FIELD_NUMBER: _ClassVar[int]
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
    SET_TIME_TASK_FIELD_NUMBER: _ClassVar[int]
    active_display_property_full_upload: bool
    active_runtime_property_full_upload: bool
    cfg_ac_in_chg_mode: AC_IN_CHG_MODE
    cfg_ac_out_always_on: CfgAcOutAlwaysOn
    cfg_ac_out_freq: int
    cfg_ac_out_open: bool
    cfg_ac_standby_time: int
    cfg_backup_reverse_soc: int
    cfg_beep: CfgBeep
    cfg_beep_en: bool
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
    cfg_generator_care_mode: CfgGeneratorCareMode
    cfg_generator_mppt_hybrid_mode: CfgGeneratorMpptHybridMode
    cfg_lcd_light: int
    cfg_max_chg_soc: int
    cfg_min_dsg_soc: int
    cfg_output_power_off_memory: bool
    cfg_plug_in_info_ac_in_chg_pow_max: int
    cfg_plug_in_info_pv_dc_amp_max: int
    cfg_power_off: bool
    cfg_power_on: bool
    cfg_pv_dc_chg_setting: PvDcChgSetting
    cfg_runtime_property_full_upload_period: int
    cfg_runtime_property_incremental_upload_period: int
    cfg_screen_off_time: int
    cfg_soc_cali: int
    cfg_storm_pattern: CfgStormPattern
    cfg_tou_strategy: CfgTouStrategy
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
        cfg_plug_in_info_ac_in_chg_pow_max: _Optional[int] = ...,
        cfg_cms_oil_self_start: bool = ...,
        cfg_cms_oil_on_soc: _Optional[int] = ...,
        cfg_cms_oil_off_soc: _Optional[int] = ...,
        cfg_tou_strategy: _Optional[_Union[CfgTouStrategy, _Mapping]] = ...,
        cfg_display_property_full_upload_period: _Optional[int] = ...,
        cfg_display_property_incremental_upload_period: _Optional[int] = ...,
        cfg_runtime_property_full_upload_period: _Optional[int] = ...,
        cfg_runtime_property_incremental_upload_period: _Optional[int] = ...,
        active_display_property_full_upload: bool = ...,
        active_runtime_property_full_upload: bool = ...,
        cfg_ac_out_open: bool = ...,
        cfg_plug_in_info_pv_dc_amp_max: _Optional[int] = ...,
        cfg_storm_pattern: _Optional[_Union[CfgStormPattern, _Mapping]] = ...,
        cfg_generator_mppt_hybrid_mode: _Optional[
            _Union[CfgGeneratorMpptHybridMode, _Mapping]
        ] = ...,
        cfg_generator_care_mode: _Optional[
            _Union[CfgGeneratorCareMode, _Mapping]
        ] = ...,
        cfg_backup_reverse_soc: _Optional[int] = ...,
        cfg_energy_strategy_operate_mode: _Optional[
            _Union[CfgEnergyStrategyOperateMode, _Mapping]
        ] = ...,
        cfg_ac_in_chg_mode: _Optional[_Union[AC_IN_CHG_MODE, str]] = ...,
        cfg_pv_dc_chg_setting: _Optional[_Union[PvDcChgSetting, _Mapping]] = ...,
        cfg_utc_timezone_id: _Optional[str] = ...,
        cfg_utc_set_mode: bool = ...,
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
        "cfg_ac_in_chg_mode",
        "cfg_ac_out_always_on",
        "cfg_ac_out_freq",
        "cfg_ac_out_open",
        "cfg_ac_standby_time",
        "cfg_backup_reverse_soc",
        "cfg_beep",
        "cfg_beep_en",
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
        "cfg_generator_care_mode",
        "cfg_generator_mppt_hybrid_mode",
        "cfg_lcd_light",
        "cfg_max_chg_soc",
        "cfg_min_dsg_soc",
        "cfg_output_power_off_memory",
        "cfg_plug_in_info_ac_in_chg_pow_max",
        "cfg_plug_in_info_pv_dc_amp_max",
        "cfg_power_off",
        "cfg_power_on",
        "cfg_pv_dc_chg_setting",
        "cfg_runtime_property_full_upload_period",
        "cfg_runtime_property_incremental_upload_period",
        "cfg_screen_off_time",
        "cfg_soc_cali",
        "cfg_storm_pattern",
        "cfg_tou_strategy",
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
        "set_time_task",
    ]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_DISPLAY_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_RUNTIME_PROPERTY_FULL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_IN_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_ALWAYS_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_OUT_OPEN_FIELD_NUMBER: _ClassVar[int]
    CFG_AC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_BACKUP_REVERSE_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_EN_FIELD_NUMBER: _ClassVar[int]
    CFG_BEEP_FIELD_NUMBER: _ClassVar[int]
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
    CFG_GENERATOR_CARE_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_GENERATOR_MPPT_HYBRID_MODE_FIELD_NUMBER: _ClassVar[int]
    CFG_LCD_LIGHT_FIELD_NUMBER: _ClassVar[int]
    CFG_MAX_CHG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_MIN_DSG_SOC_FIELD_NUMBER: _ClassVar[int]
    CFG_OUTPUT_POWER_OFF_MEMORY_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_AC_IN_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_PLUG_IN_INFO_PV_DC_AMP_MAX_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_OFF_FIELD_NUMBER: _ClassVar[int]
    CFG_POWER_ON_FIELD_NUMBER: _ClassVar[int]
    CFG_PV_DC_CHG_SETTING_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_RUNTIME_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CFG_SCREEN_OFF_TIME_FIELD_NUMBER: _ClassVar[int]
    CFG_SOC_CALI_FIELD_NUMBER: _ClassVar[int]
    CFG_STORM_PATTERN_FIELD_NUMBER: _ClassVar[int]
    CFG_TOU_STRATEGY_FIELD_NUMBER: _ClassVar[int]
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
    SET_TIME_TASK_FIELD_NUMBER: _ClassVar[int]
    action_id: int
    active_display_property_full_upload: bool
    active_runtime_property_full_upload: bool
    cfg_ac_in_chg_mode: AC_IN_CHG_MODE
    cfg_ac_out_always_on: CfgAcOutAlwaysOn
    cfg_ac_out_freq: int
    cfg_ac_out_open: bool
    cfg_ac_standby_time: int
    cfg_backup_reverse_soc: int
    cfg_beep: CfgBeep
    cfg_beep_en: bool
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
    cfg_generator_care_mode: CfgGeneratorCareMode
    cfg_generator_mppt_hybrid_mode: CfgGeneratorMpptHybridMode
    cfg_lcd_light: int
    cfg_max_chg_soc: int
    cfg_min_dsg_soc: int
    cfg_output_power_off_memory: bool
    cfg_plug_in_info_ac_in_chg_pow_max: int
    cfg_plug_in_info_pv_dc_amp_max: int
    cfg_power_off: bool
    cfg_power_on: bool
    cfg_pv_dc_chg_setting: PvDcChgSetting
    cfg_runtime_property_full_upload_period: int
    cfg_runtime_property_incremental_upload_period: int
    cfg_screen_off_time: int
    cfg_soc_cali: int
    cfg_storm_pattern: CfgStormPattern
    cfg_tou_strategy: CfgTouStrategy
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
        cfg_plug_in_info_ac_in_chg_pow_max: _Optional[int] = ...,
        cfg_cms_oil_self_start: bool = ...,
        cfg_cms_oil_on_soc: _Optional[int] = ...,
        cfg_cms_oil_off_soc: _Optional[int] = ...,
        cfg_tou_strategy: _Optional[_Union[CfgTouStrategy, _Mapping]] = ...,
        cfg_display_property_full_upload_period: _Optional[int] = ...,
        cfg_display_property_incremental_upload_period: _Optional[int] = ...,
        cfg_runtime_property_full_upload_period: _Optional[int] = ...,
        cfg_runtime_property_incremental_upload_period: _Optional[int] = ...,
        active_display_property_full_upload: bool = ...,
        active_runtime_property_full_upload: bool = ...,
        cfg_ac_out_open: bool = ...,
        cfg_plug_in_info_pv_dc_amp_max: _Optional[int] = ...,
        cfg_storm_pattern: _Optional[_Union[CfgStormPattern, _Mapping]] = ...,
        cfg_generator_mppt_hybrid_mode: _Optional[
            _Union[CfgGeneratorMpptHybridMode, _Mapping]
        ] = ...,
        cfg_generator_care_mode: _Optional[
            _Union[CfgGeneratorCareMode, _Mapping]
        ] = ...,
        cfg_backup_reverse_soc: _Optional[int] = ...,
        cfg_energy_strategy_operate_mode: _Optional[
            _Union[CfgEnergyStrategyOperateMode, _Mapping]
        ] = ...,
        cfg_ac_in_chg_mode: _Optional[_Union[AC_IN_CHG_MODE, str]] = ...,
        cfg_pv_dc_chg_setting: _Optional[_Union[PvDcChgSetting, _Mapping]] = ...,
        cfg_utc_timezone_id: _Optional[str] = ...,
        cfg_utc_set_mode: bool = ...,
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
        "require_time_service",
        "require_tou_strategy",
    ]
    DEV_UTC_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    DEV_UTC_TIME_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_PROPERTY_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_TIME_SERVICE_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_TOU_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    dev_utc_time: int
    dev_utc_timezone: float
    require_property_upload_period: bool
    require_time_service: bool
    require_tou_strategy: ReqTouStrategy
    def __init__(
        self,
        dev_utc_time: _Optional[int] = ...,
        dev_utc_timezone: _Optional[float] = ...,
        require_property_upload_period: bool = ...,
        require_tou_strategy: _Optional[_Union[ReqTouStrategy, _Mapping]] = ...,
        require_time_service: bool = ...,
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
        "ac_out_freq",
        "ac_standby_time",
        "backup_reverse_soc",
        "bms_batt_soc",
        "bms_batt_soh",
        "bms_chg_dsg_state",
        "bms_chg_rem_time",
        "bms_design_cap",
        "bms_dsg_rem_time",
        "bms_err_code",
        "bms_main_sn",
        "bms_max_cell_temp",
        "bms_max_mos_temp",
        "bms_min_cell_temp",
        "bms_min_mos_temp",
        "bypass_out_disable",
        "bypass_out_disable_conflict_flag",
        "cms_batt_full_energy",
        "cms_batt_pow_in_max",
        "cms_batt_pow_out_max",
        "cms_batt_soc",
        "cms_batt_soh",
        "cms_bms_run_state",
        "cms_chg_dsg_state",
        "cms_chg_rem_time",
        "cms_dsg_rem_time",
        "cms_max_chg_soc",
        "cms_min_dsg_soc",
        "cms_oil_off_soc",
        "cms_oil_on_soc",
        "cms_oil_self_start",
        "dc_standby_time",
        "dcdc_err_code",
        "dev_sleep_state",
        "dev_standby_time",
        "en_beep",
        "energy_backup_conflict_flag",
        "energy_backup_en",
        "energy_backup_start_soc",
        "energy_strategy_operate_mode",
        "errcode",
        "fast_charge_switch",
        "flow_info_12v",
        "flow_info_ac2dc",
        "flow_info_ac_in",
        "flow_info_ac_out",
        "flow_info_bms_chg",
        "flow_info_bms_dsg",
        "flow_info_dc2ac",
        "flow_info_dcp_in",
        "flow_info_dcp_out",
        "flow_info_pv",
        "flow_info_pv2",
        "flow_info_qcusb1",
        "flow_info_qcusb2",
        "flow_info_typec1",
        "flow_info_typec2",
        "inv_err_code",
        "lcd_light",
        "output_power_off_memory",
        "pcs_fan_err_flag",
        "pcs_fan_level",
        "pd_err_code",
        "plug_in_info_ac_charger_flag",
        "plug_in_info_ac_in_chg_mode",
        "plug_in_info_ac_in_chg_pow_max",
        "plug_in_info_ac_in_feq",
        "plug_in_info_ac_in_flag",
        "plug_in_info_ac_out_dsg_pow_max",
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
        "plug_in_info_pv_type",
        "pow_get_12v",
        "pow_get_ac",
        "pow_get_ac_in",
        "pow_get_ac_out",
        "pow_get_bms",
        "pow_get_dc",
        "pow_get_dcp",
        "pow_get_pv",
        "pow_get_pv2",
        "pow_get_qcusb1",
        "pow_get_qcusb2",
        "pow_get_typec1",
        "pow_get_typec2",
        "pow_in_sum_w",
        "pow_out_sum_w",
        "pv_dc_chg_setting_list",
        "screen_off_time",
        "self_powered_conflict_flag",
        "storm_pattern_conflict_flag",
        "storm_pattern_enable",
        "storm_pattern_end_time",
        "storm_pattern_open_flag",
        "time_task_change_cnt",
        "time_task_conflict_flag",
        "time_task_current",
        "tou_mode_conflict_flag",
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
    AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    AC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    BACKUP_REVERSE_SOC_FIELD_NUMBER: _ClassVar[int]
    BMS_BATT_SOC_FIELD_NUMBER: _ClassVar[int]
    BMS_BATT_SOH_FIELD_NUMBER: _ClassVar[int]
    BMS_CHG_DSG_STATE_FIELD_NUMBER: _ClassVar[int]
    BMS_CHG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    BMS_DESIGN_CAP_FIELD_NUMBER: _ClassVar[int]
    BMS_DSG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    BMS_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    BMS_MAIN_SN_FIELD_NUMBER: _ClassVar[int]
    BMS_MAX_CELL_TEMP_FIELD_NUMBER: _ClassVar[int]
    BMS_MAX_MOS_TEMP_FIELD_NUMBER: _ClassVar[int]
    BMS_MIN_CELL_TEMP_FIELD_NUMBER: _ClassVar[int]
    BMS_MIN_MOS_TEMP_FIELD_NUMBER: _ClassVar[int]
    BYPASS_OUT_DISABLE_CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    BYPASS_OUT_DISABLE_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_FULL_ENERGY_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_POW_IN_MAX_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_POW_OUT_MAX_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_BATT_SOH_FIELD_NUMBER: _ClassVar[int]
    CMS_BMS_RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    CMS_CHG_DSG_STATE_FIELD_NUMBER: _ClassVar[int]
    CMS_CHG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    CMS_DSG_REM_TIME_FIELD_NUMBER: _ClassVar[int]
    CMS_MAX_CHG_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_MIN_DSG_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_OIL_OFF_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_OIL_ON_SOC_FIELD_NUMBER: _ClassVar[int]
    CMS_OIL_SELF_START_FIELD_NUMBER: _ClassVar[int]
    DCDC_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    DC_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    DEV_SLEEP_STATE_FIELD_NUMBER: _ClassVar[int]
    DEV_STANDBY_TIME_FIELD_NUMBER: _ClassVar[int]
    ENERGY_BACKUP_CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    ENERGY_BACKUP_EN_FIELD_NUMBER: _ClassVar[int]
    ENERGY_BACKUP_START_SOC_FIELD_NUMBER: _ClassVar[int]
    ENERGY_STRATEGY_OPERATE_MODE_FIELD_NUMBER: _ClassVar[int]
    EN_BEEP_FIELD_NUMBER: _ClassVar[int]
    ERRCODE_FIELD_NUMBER: _ClassVar[int]
    FAST_CHARGE_SWITCH_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_12V_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC2DC_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_AC_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_BMS_CHG_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_BMS_DSG_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DC2AC_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DCP_IN_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_DCP_OUT_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_PV2_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_PV_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_QCUSB1_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_QCUSB2_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_TYPEC1_FIELD_NUMBER: _ClassVar[int]
    FLOW_INFO_TYPEC2_FIELD_NUMBER: _ClassVar[int]
    INV_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    LCD_LIGHT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_POWER_OFF_MEMORY_FIELD_NUMBER: _ClassVar[int]
    PCS_FAN_ERR_FLAG_FIELD_NUMBER: _ClassVar[int]
    PCS_FAN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PD_ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_CHARGER_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_CHG_MODE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_CHG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_FEQ_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_FLAG_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_DSG_POW_MAX_FIELD_NUMBER: _ClassVar[int]
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
    PLUG_IN_INFO_PV_TYPE_FIELD_NUMBER: _ClassVar[int]
    POW_GET_12V_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_IN_FIELD_NUMBER: _ClassVar[int]
    POW_GET_AC_OUT_FIELD_NUMBER: _ClassVar[int]
    POW_GET_BMS_FIELD_NUMBER: _ClassVar[int]
    POW_GET_DCP_FIELD_NUMBER: _ClassVar[int]
    POW_GET_DC_FIELD_NUMBER: _ClassVar[int]
    POW_GET_PV2_FIELD_NUMBER: _ClassVar[int]
    POW_GET_PV_FIELD_NUMBER: _ClassVar[int]
    POW_GET_QCUSB1_FIELD_NUMBER: _ClassVar[int]
    POW_GET_QCUSB2_FIELD_NUMBER: _ClassVar[int]
    POW_GET_TYPEC1_FIELD_NUMBER: _ClassVar[int]
    POW_GET_TYPEC2_FIELD_NUMBER: _ClassVar[int]
    POW_IN_SUM_W_FIELD_NUMBER: _ClassVar[int]
    POW_OUT_SUM_W_FIELD_NUMBER: _ClassVar[int]
    PV_DC_CHG_SETTING_LIST_FIELD_NUMBER: _ClassVar[int]
    SCREEN_OFF_TIME_FIELD_NUMBER: _ClassVar[int]
    SELF_POWERED_CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    STORM_PATTERN_OPEN_FLAG_FIELD_NUMBER: _ClassVar[int]
    TIME_TASK_CHANGE_CNT_FIELD_NUMBER: _ClassVar[int]
    TIME_TASK_CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
    TIME_TASK_CURRENT_FIELD_NUMBER: _ClassVar[int]
    TOU_MODE_CONFLICT_FLAG_FIELD_NUMBER: _ClassVar[int]
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
    ac_out_freq: int
    ac_standby_time: int
    backup_reverse_soc: int
    bms_batt_soc: float
    bms_batt_soh: float
    bms_chg_dsg_state: int
    bms_chg_rem_time: int
    bms_design_cap: int
    bms_dsg_rem_time: int
    bms_err_code: int
    bms_main_sn: str
    bms_max_cell_temp: int
    bms_max_mos_temp: int
    bms_min_cell_temp: int
    bms_min_mos_temp: int
    bypass_out_disable: bool
    bypass_out_disable_conflict_flag: int
    cms_batt_full_energy: int
    cms_batt_pow_in_max: int
    cms_batt_pow_out_max: int
    cms_batt_soc: float
    cms_batt_soh: float
    cms_bms_run_state: int
    cms_chg_dsg_state: int
    cms_chg_rem_time: int
    cms_dsg_rem_time: int
    cms_max_chg_soc: int
    cms_min_dsg_soc: int
    cms_oil_off_soc: int
    cms_oil_on_soc: int
    cms_oil_self_start: bool
    dc_standby_time: int
    dcdc_err_code: int
    dev_sleep_state: int
    dev_standby_time: int
    en_beep: bool
    energy_backup_conflict_flag: int
    energy_backup_en: bool
    energy_backup_start_soc: int
    energy_strategy_operate_mode: CfgEnergyStrategyOperateMode
    errcode: int
    fast_charge_switch: int
    flow_info_12v: int
    flow_info_ac2dc: int
    flow_info_ac_in: int
    flow_info_ac_out: int
    flow_info_bms_chg: int
    flow_info_bms_dsg: int
    flow_info_dc2ac: int
    flow_info_dcp_in: int
    flow_info_dcp_out: int
    flow_info_pv: int
    flow_info_pv2: int
    flow_info_qcusb1: int
    flow_info_qcusb2: int
    flow_info_typec1: int
    flow_info_typec2: int
    inv_err_code: int
    lcd_light: int
    output_power_off_memory: bool
    pcs_fan_err_flag: int
    pcs_fan_level: int
    pd_err_code: int
    plug_in_info_ac_charger_flag: bool
    plug_in_info_ac_in_chg_mode: AC_IN_CHG_MODE
    plug_in_info_ac_in_chg_pow_max: int
    plug_in_info_ac_in_feq: int
    plug_in_info_ac_in_flag: int
    plug_in_info_ac_out_dsg_pow_max: int
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
    plug_in_info_pv_type: int
    pow_get_12v: float
    pow_get_ac: float
    pow_get_ac_in: float
    pow_get_ac_out: float
    pow_get_bms: float
    pow_get_dc: float
    pow_get_dcp: float
    pow_get_pv: float
    pow_get_pv2: float
    pow_get_qcusb1: float
    pow_get_qcusb2: float
    pow_get_typec1: float
    pow_get_typec2: float
    pow_in_sum_w: float
    pow_out_sum_w: float
    pv_dc_chg_setting_list: PvDcChgSettingList
    screen_off_time: int
    self_powered_conflict_flag: int
    storm_pattern_conflict_flag: int
    storm_pattern_enable: bool
    storm_pattern_end_time: int
    storm_pattern_open_flag: bool
    time_task_change_cnt: int
    time_task_conflict_flag: int
    time_task_current: SetTimeTaskWrite
    tou_mode_conflict_flag: int
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
        utc_timezone: _Optional[int] = ...,
        utc_timezone_id: _Optional[str] = ...,
        utc_set_mode: bool = ...,
        cms_bms_run_state: _Optional[int] = ...,
        cms_batt_soc: _Optional[float] = ...,
        cms_batt_soh: _Optional[float] = ...,
        cms_chg_dsg_state: _Optional[int] = ...,
        cms_batt_full_energy: _Optional[int] = ...,
        cms_dsg_rem_time: _Optional[int] = ...,
        cms_chg_rem_time: _Optional[int] = ...,
        cms_batt_pow_out_max: _Optional[int] = ...,
        cms_batt_pow_in_max: _Optional[int] = ...,
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
        bms_main_sn: _Optional[str] = ...,
        dev_sleep_state: _Optional[int] = ...,
        en_beep: bool = ...,
        lcd_light: _Optional[int] = ...,
        dev_standby_time: _Optional[int] = ...,
        screen_off_time: _Optional[int] = ...,
        ac_standby_time: _Optional[int] = ...,
        dc_standby_time: _Optional[int] = ...,
        ac_out_freq: _Optional[int] = ...,
        ac_always_on_flag: bool = ...,
        ac_always_on_mini_soc: _Optional[int] = ...,
        xboost_en: bool = ...,
        output_power_off_memory: bool = ...,
        fast_charge_switch: _Optional[int] = ...,
        bypass_out_disable: bool = ...,
        bypass_out_disable_conflict_flag: _Optional[int] = ...,
        pv_dc_chg_setting_list: _Optional[_Union[PvDcChgSettingList, _Mapping]] = ...,
        energy_backup_start_soc: _Optional[int] = ...,
        energy_backup_en: bool = ...,
        storm_pattern_enable: bool = ...,
        storm_pattern_open_flag: bool = ...,
        storm_pattern_end_time: _Optional[int] = ...,
        storm_pattern_conflict_flag: _Optional[int] = ...,
        time_task_current: _Optional[_Union[SetTimeTaskWrite, _Mapping]] = ...,
        time_task_conflict_flag: _Optional[int] = ...,
        time_task_change_cnt: _Optional[int] = ...,
        energy_strategy_operate_mode: _Optional[
            _Union[CfgEnergyStrategyOperateMode, _Mapping]
        ] = ...,
        backup_reverse_soc: _Optional[int] = ...,
        energy_backup_conflict_flag: _Optional[int] = ...,
        self_powered_conflict_flag: _Optional[int] = ...,
        tou_mode_conflict_flag: _Optional[int] = ...,
        cms_oil_self_start: bool = ...,
        cms_oil_on_soc: _Optional[int] = ...,
        cms_oil_off_soc: _Optional[int] = ...,
        wireless_oil_self_start: bool = ...,
        wireless_oil_on_soc: _Optional[int] = ...,
        wireless_oil_off_soc: _Optional[int] = ...,
        pow_in_sum_w: _Optional[float] = ...,
        pow_out_sum_w: _Optional[float] = ...,
        pow_get_qcusb1: _Optional[float] = ...,
        pow_get_qcusb2: _Optional[float] = ...,
        pow_get_typec1: _Optional[float] = ...,
        pow_get_typec2: _Optional[float] = ...,
        pow_get_pv: _Optional[float] = ...,
        pow_get_pv2: _Optional[float] = ...,
        pow_get_12v: _Optional[float] = ...,
        pow_get_ac: _Optional[float] = ...,
        pow_get_ac_in: _Optional[float] = ...,
        pow_get_ac_out: _Optional[float] = ...,
        pow_get_dc: _Optional[float] = ...,
        pow_get_bms: _Optional[float] = ...,
        pow_get_dcp: _Optional[float] = ...,
        flow_info_qcusb1: _Optional[int] = ...,
        flow_info_qcusb2: _Optional[int] = ...,
        flow_info_typec1: _Optional[int] = ...,
        flow_info_typec2: _Optional[int] = ...,
        flow_info_pv: _Optional[int] = ...,
        flow_info_pv2: _Optional[int] = ...,
        flow_info_12v: _Optional[int] = ...,
        flow_info_ac2dc: _Optional[int] = ...,
        flow_info_dc2ac: _Optional[int] = ...,
        flow_info_ac_in: _Optional[int] = ...,
        flow_info_ac_out: _Optional[int] = ...,
        flow_info_bms_dsg: _Optional[int] = ...,
        flow_info_bms_chg: _Optional[int] = ...,
        flow_info_dcp_in: _Optional[int] = ...,
        flow_info_dcp_out: _Optional[int] = ...,
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
        plug_in_info_ac_in_chg_mode: _Optional[_Union[AC_IN_CHG_MODE, str]] = ...,
        plug_in_info_ac_out_dsg_pow_max: _Optional[int] = ...,
        plug_in_info_dcp_in_flag: bool = ...,
        plug_in_info_dcp_dsg_chg_type: _Optional[int] = ...,
        plug_in_info_dcp_charger_flag: bool = ...,
        plug_in_info_dcp_type: _Optional[int] = ...,
        plug_in_info_dcp_detail: _Optional[int] = ...,
        plug_in_info_dcp_sn: _Optional[str] = ...,
        plug_in_info_dcp_run_state: _Optional[int] = ...,
        plug_in_info_dcp_firm_ver: _Optional[int] = ...,
        plug_in_info_dcp_resv: _Optional[_Union[ResvInfo, _Mapping]] = ...,
        wireless_coordinate_dev_list: _Optional[
            _Union[WirelessCoordinateList, _Mapping]
        ] = ...,
        pd_err_code: _Optional[int] = ...,
        dcdc_err_code: _Optional[int] = ...,
        plug_in_info_dcp_err_code: _Optional[int] = ...,
        bms_err_code: _Optional[int] = ...,
        inv_err_code: _Optional[int] = ...,
        pcs_fan_level: _Optional[int] = ...,
        pcs_fan_err_flag: _Optional[int] = ...,
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

class ResvInfo(_message.Message):
    __slots__ = ["resv_info"]
    RESV_INFO_FIELD_NUMBER: _ClassVar[int]
    resv_info: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, resv_info: _Optional[_Iterable[int]] = ...) -> None: ...

class RuntimePropertyUpload(_message.Message):
    __slots__ = [
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
        "dcdc_firm_ver",
        "display_property_full_upload_period",
        "display_property_incremental_upload_period",
        "inv_firm_ver",
        "iot_firm_ver",
        "pd_bms_comm_err",
        "pd_dcdc_comm_err",
        "pd_firm_ver",
        "pd_inv_comm_err",
        "pd_iot_comm_err",
        "plug_in_info_ac_in_amp",
        "plug_in_info_ac_in_vol",
        "plug_in_info_ac_out_amp",
        "plug_in_info_ac_out_freq",
        "plug_in_info_ac_out_type",
        "plug_in_info_ac_out_vol",
        "plug_in_info_bms_vol",
        "plug_in_info_dcp_amp",
        "plug_in_info_dcp_vol",
        "plug_in_info_pv2_amp",
        "plug_in_info_pv2_vol",
        "plug_in_info_pv_amp",
        "plug_in_info_pv_vol",
        "runtime_property_full_upload_period",
        "runtime_property_incremental_upload_period",
        "temp_pcs_ac",
        "temp_pcs_dc",
        "temp_pv",
        "temp_pv2",
    ]
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
    DCDC_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    INV_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    IOT_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PD_BMS_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_DCDC_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_FIRM_VER_FIELD_NUMBER: _ClassVar[int]
    PD_INV_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PD_IOT_COMM_ERR_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_IN_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_FREQ_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_AC_OUT_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_BMS_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_DCP_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV2_VOL_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_AMP_FIELD_NUMBER: _ClassVar[int]
    PLUG_IN_INFO_PV_VOL_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_PROPERTY_FULL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_PROPERTY_INCREMENTAL_UPLOAD_PERIOD_FIELD_NUMBER: _ClassVar[int]
    TEMP_PCS_AC_FIELD_NUMBER: _ClassVar[int]
    TEMP_PCS_DC_FIELD_NUMBER: _ClassVar[int]
    TEMP_PV2_FIELD_NUMBER: _ClassVar[int]
    TEMP_PV_FIELD_NUMBER: _ClassVar[int]
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
    dcdc_firm_ver: int
    display_property_full_upload_period: int
    display_property_incremental_upload_period: int
    inv_firm_ver: int
    iot_firm_ver: int
    pd_bms_comm_err: bool
    pd_dcdc_comm_err: bool
    pd_firm_ver: int
    pd_inv_comm_err: bool
    pd_iot_comm_err: bool
    plug_in_info_ac_in_amp: float
    plug_in_info_ac_in_vol: float
    plug_in_info_ac_out_amp: float
    plug_in_info_ac_out_freq: int
    plug_in_info_ac_out_type: int
    plug_in_info_ac_out_vol: float
    plug_in_info_bms_vol: float
    plug_in_info_dcp_amp: float
    plug_in_info_dcp_vol: float
    plug_in_info_pv2_amp: float
    plug_in_info_pv2_vol: float
    plug_in_info_pv_amp: float
    plug_in_info_pv_vol: float
    runtime_property_full_upload_period: int
    runtime_property_incremental_upload_period: int
    temp_pcs_ac: float
    temp_pcs_dc: float
    temp_pv: float
    temp_pv2: float
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
        plug_in_info_bms_vol: _Optional[float] = ...,
        plug_in_info_dcp_vol: _Optional[float] = ...,
        plug_in_info_dcp_amp: _Optional[float] = ...,
        pd_bms_comm_err: bool = ...,
        pd_iot_comm_err: bool = ...,
        pd_dcdc_comm_err: bool = ...,
        pd_inv_comm_err: bool = ...,
        pd_firm_ver: _Optional[int] = ...,
        iot_firm_ver: _Optional[int] = ...,
        dcdc_firm_ver: _Optional[int] = ...,
        inv_firm_ver: _Optional[int] = ...,
        temp_pcs_dc: _Optional[float] = ...,
        temp_pcs_ac: _Optional[float] = ...,
        temp_pv: _Optional[float] = ...,
        temp_pv2: _Optional[float] = ...,
        bms_overload_icon: _Optional[int] = ...,
        bms_warn_icon: _Optional[int] = ...,
        bms_high_temp_icon: _Optional[int] = ...,
        bms_low_temp_icon: _Optional[int] = ...,
        bms_limit_icon: _Optional[int] = ...,
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
