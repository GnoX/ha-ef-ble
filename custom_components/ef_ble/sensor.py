"""EcoFlow BLE sensor"""

import itertools
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DeviceConfigEntry
from .eflib import DeviceBase
from .eflib.devices import delta_pro_3, shp2
from .entity import EcoflowEntity

_UPPER_WORDS = ["ac", "dc", "lv", "hv", "tt", "5p8"]


def _auto_name_from_key(key: str):
    return " ".join(
        [
            part.capitalize() if part.lower() not in _UPPER_WORDS else part.upper()
            for part in key.split("_")
        ]
    )


@dataclass(frozen=True, kw_only=True)
class EcoflowSensorEntityDescription(SensorEntityDescription):
    state_attribute_fields: list[str] = field(default_factory=list)


SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    # Common
    "battery_level": EcoflowSensorEntityDescription(
        key="battery_level",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "battery_level_bms": EcoflowSensorEntityDescription(
        key="battery_level_bms",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "battery_level_main": SensorEntityDescription(
        key="battery_level_main",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "input_power": SensorEntityDescription(
        key="input_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    "output_power": SensorEntityDescription(
        key="output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    # SHP2
    "grid_power": SensorEntityDescription(
        key="grid_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "in_use_power": SensorEntityDescription(
        key="in_use_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    **{
        f"circuit_power_{i}": SensorEntityDescription(
            key=f"circuit_power_{i}",
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_display_precision=2,
            translation_key="circuit_power",
            translation_placeholders={"index": f"{i:02}"},
        )
        for i in range(1, shp2.Device.NUM_OF_CIRCUITS + 1)
    },
    **{
        f"circuit_current_{i}": SensorEntityDescription(
            key=f"circuit_current_{i}",
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=2,
            entity_registry_enabled_default=False,
            translation_key="circuit_current",
            translation_placeholders={"index": f"{i:02}"},
        )
        for i in range(1, shp2.Device.NUM_OF_CIRCUITS + 1)
    },
    **{
        f"channel_power_{i}": SensorEntityDescription(
            key=f"channel_power_{i}",
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=2,
            translation_key="channel_power",
            translation_placeholders={"index": f"{i:02}"},
        )
        for i in range(1, shp2.Device.NUM_OF_CHANNELS + 1)
    },
    # DPU
    **{
        f"{sensor}_{measurement}": SensorEntityDescription(
            key=f"{sensor}_{measurement}",
            native_unit_of_measurement=UnitOfPower.WATT,
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key=f"port_{measurement}",
            translation_placeholders={"name": _auto_name_from_key(sensor)},
            suggested_display_precision=2,
        )
        for measurement, sensor in itertools.product(
            ["power"],
            [
                "lv_solar",
                "hv_solar",
                "ac_l1_1_out",
                "ac_l1_2_out",
                "ac_l2_1_out",
                "ac_l2_2_out",
                "ac_l14_out",
                "ac_tt_out",
                "ac_5p8_out",
            ],
        )
    },
    **{
        f"battery_{i}_battery_level": SensorEntityDescription(
            key=f"battery_{i}_battery_level",
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.BATTERY,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="additional_battery_level",
            translation_placeholders={"index": f"{i}"},
            entity_registry_enabled_default=False,
        )
        for i in range(1, 6)
    },
    # River 3, Delta 3
    "input_energy": SensorEntityDescription(
        key="input_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "output_energy": SensorEntityDescription(
        key="output_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "ac_input_power": SensorEntityDescription(
        key="ac_input_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "ac_output_power": SensorEntityDescription(
        key="ac_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "ac_input_energy": SensorEntityDescription(
        key="ac_input_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "ac_output_energy": SensorEntityDescription(
        key="ac_output_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "dc_input_power": SensorEntityDescription(
        key="dc_input_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "dc_input_energy": SensorEntityDescription(
        key="dc_input_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "dc12v_output_power": SensorEntityDescription(
        key="dc12v_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "dc12v_output_energy": SensorEntityDescription(
        key="dc12v_output_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "usbc_output_power": SensorEntityDescription(
        key="usbc_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "usbc_output_energy": SensorEntityDescription(
        key="usbc_output_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "usba_output_power": SensorEntityDescription(
        key="usba_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "usba_output_energy": SensorEntityDescription(
        key="usba_output_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=3,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "usbc2_output_power": SensorEntityDescription(
        key="usbc2_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "usba2_output_power": SensorEntityDescription(
        key="usba2_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "battery_input_power": SensorEntityDescription(
        key="battery_input_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    "battery_output_power": SensorEntityDescription(
        key="battery_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    "cell_temperature": SensorEntityDescription(
        key="cell_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_enabled_default=False,
    ),
    "dc_port_input_power": SensorEntityDescription(
        key="dc_port_input_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=2,
    ),
    "dc_port_2_input_power": SensorEntityDescription(
        key="dc_port_input_power_2",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=2,
    ),
    "dc_port_state": SensorEntityDescription(
        key="dc_port_state",
        device_class=SensorDeviceClass.ENUM,
    ),
    "dc_port_2_state": SensorEntityDescription(
        key="dc_port_2_state",
        device_class=SensorDeviceClass.ENUM,
    ),
    "solar_input_power": SensorEntityDescription(
        key="input_power_solar",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    "solar_input_power_2": SensorEntityDescription(
        key="input_power_solar_2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    # DP3
    "ac_lv_output_power": SensorEntityDescription(
        key="ac_lv_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "ac_hv_output_power": SensorEntityDescription(
        key="ac_hv_output_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "solar_lv_power": SensorEntityDescription(
        key="input_power_solar_lv",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    "solar_hv_power": SensorEntityDescription(
        key="input_power_solar_hv",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    "dc_lv_input_power": SensorEntityDescription(
        key="dc_lv_input_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=2,
    ),
    "dc_hv_input_power": SensorEntityDescription(
        key="dc_hv_input_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=2,
    ),
    "dc_lv_state": SensorEntityDescription(
        key="dc_lv_state",
        device_class=SensorDeviceClass.ENUM,
        options=delta_pro_3.DCPortState.options(),
    ),
    "dc_hv_state": SensorEntityDescription(
        key="dc_hv_state",
        device_class=SensorDeviceClass.ENUM,
        options=delta_pro_3.DCPortState.options(),
    ),
    # STREAM
    "grid_voltage": SensorEntityDescription(
        key="grid_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "grid_frequency": SensorEntityDescription(
        key="grid_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "load_from_battery": SensorEntityDescription(
        key="load_from_battery",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "load_from_grid": SensorEntityDescription(
        key="load_from_grid",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    **{
        f"ac_power_{i}": SensorEntityDescription(
            key=f"ac_power_{i}",
            native_unit_of_measurement=UnitOfPower.WATT,
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="port_power",
            translation_placeholders={"name": f"AC ({i})"},
        )
        for i in range(3)
    },
    **{
        f"pv_power_{i}": SensorEntityDescription(
            key=f"ac_power_{i}",
            native_unit_of_measurement=UnitOfPower.WATT,
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="port_power_pv",
            translation_placeholders={"index": f"{i}"},
        )
        for i in range(5)
    },
    # STREAM runtime properties
    "lan_sys_device_count": SensorEntityDescription(
        key="lan_sys_device_count",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "lan_sys_home_need_power": SensorEntityDescription(
        key="lan_sys_home_need_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "lan_sys_work_mode": SensorEntityDescription(
        key="lan_sys_work_mode",
    ),
    "cascade_sys_soc": SensorEntityDescription(
        key="cascade_sys_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Additional sensor definitions to add to SENSOR_TYPES dictionary
    # CMS Battery Management
    "cms_batt_soc": SensorEntityDescription(
        key="cms_batt_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_batt_soh": SensorEntityDescription(
        key="cms_batt_soh",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_batt_full_energy": SensorEntityDescription(
        key="cms_batt_full_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_dsg_rem_time": SensorEntityDescription(
        key="cms_dsg_rem_time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_chg_rem_time": SensorEntityDescription(
        key="cms_chg_rem_time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_batt_pow_out_max": SensorEntityDescription(
        key="cms_batt_pow_out_max",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_batt_pow_in_max": SensorEntityDescription(
        key="cms_batt_pow_in_max",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_max_chg_soc": SensorEntityDescription(
        key="cms_max_chg_soc",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cms_min_dsg_soc": SensorEntityDescription(
        key="cms_min_dsg_soc",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # BMS Advanced Monitoring
    "bms_batt_soh": SensorEntityDescription(
        key="bms_batt_soh",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "bms_design_cap": SensorEntityDescription(
        key="bms_design_cap",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "bms_dsg_rem_time": SensorEntityDescription(
        key="bms_dsg_rem_time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "bms_chg_rem_time": SensorEntityDescription(
        key="bms_chg_rem_time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "bms_min_cell_temp": SensorEntityDescription(
        key="bms_min_cell_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "bms_max_cell_temp": SensorEntityDescription(
        key="bms_max_cell_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "bms_min_mos_temp": SensorEntityDescription(
        key="bms_min_mos_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "bms_max_mos_temp": SensorEntityDescription(
        key="bms_max_mos_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # System Power Limits
    "max_inv_input": SensorEntityDescription(
        key="max_inv_input",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "max_inv_output": SensorEntityDescription(
        key="max_inv_output",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "max_bp_input": SensorEntityDescription(
        key="max_bp_input",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "max_bp_output": SensorEntityDescription(
        key="max_bp_output",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "busbar_pow_limit": SensorEntityDescription(
        key="busbar_pow_limit",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Inverter and Grid
    "inv_target_pwr": SensorEntityDescription(
        key="inv_target_pwr",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "backup_reverse_soc": SensorEntityDescription(
        key="backup_reverse_soc",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "feed_grid_mode_pow_limit": SensorEntityDescription(
        key="feed_grid_mode_pow_limit",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "feed_grid_mode_pow_max": SensorEntityDescription(
        key="feed_grid_mode_pow_max",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # System Power Distribution
    "pow_get_sys_load": SensorEntityDescription(
        key="pow_get_sys_load",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_sys_grid": SensorEntityDescription(
        key="pow_get_sys_grid",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_pv_sum": SensorEntityDescription(
        key="pow_get_pv_sum",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_bp_cms": SensorEntityDescription(
        key="pow_get_bp_cms",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_sys_load_from_pv": SensorEntityDescription(
        key="pow_get_sys_load_from_pv",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_sys_load_from_bp": SensorEntityDescription(
        key="pow_get_sys_load_from_bp",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_sys_load_from_grid": SensorEntityDescription(
        key="pow_get_sys_load_from_grid",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    # Schuko Sockets
    "pow_get_schuko1": SensorEntityDescription(
        key="pow_get_schuko1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_schuko2": SensorEntityDescription(
        key="pow_get_schuko2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    # Additional PV Monitoring
    "pow_get_pv": SensorEntityDescription(
        key="pow_get_pv",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_pv2": SensorEntityDescription(
        key="pow_get_pv2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_pv3": SensorEntityDescription(
        key="pow_get_pv3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "pow_get_pv4": SensorEntityDescription(
        key="pow_get_pv4",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    # PV Voltage and Current
    "plug_in_info_pv_vol": SensorEntityDescription(
        key="plug_in_info_pv_vol",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "plug_in_info_pv_amp": SensorEntityDescription(
        key="plug_in_info_pv_amp",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "plug_in_info_pv2_vol": SensorEntityDescription(
        key="plug_in_info_pv2_vol",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "plug_in_info_pv2_amp": SensorEntityDescription(
        key="plug_in_info_pv2_amp",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "plug_in_info_pv3_vol": SensorEntityDescription(
        key="plug_in_info_pv3_vol",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "plug_in_info_pv3_amp": SensorEntityDescription(
        key="plug_in_info_pv3_amp",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "plug_in_info_pv4_vol": SensorEntityDescription(
        key="plug_in_info_pv4_vol",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "plug_in_info_pv4_amp": SensorEntityDescription(
        key="plug_in_info_pv4_amp",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    # Grid Connection Advanced
    "grid_connection_vol": SensorEntityDescription(
        key="grid_connection_vol",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "grid_connection_amp": SensorEntityDescription(
        key="grid_connection_amp",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "grid_connection_power": SensorEntityDescription(
        key="grid_connection_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "grid_connection_power_factor": SensorEntityDescription(
        key="grid_connection_power_factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    "sys_grid_connection_power": SensorEntityDescription(
        key="sys_grid_connection_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "socket_measure_power": SensorEntityDescription(
        key="socket_measure_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    # System Capabilities
    "pow_sys_ac_out_max": SensorEntityDescription(
        key="pow_sys_ac_out_max",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "pow_sys_ac_in_max": SensorEntityDescription(
        key="pow_sys_ac_in_max",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Miscellaneous
    "pow_consumption_measurement": SensorEntityDescription(
        key="pow_consumption_measurement",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "module_wifi_rssi": SensorEntityDescription(
        key="module_wifi_rssi",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    # Stream Ultra
    "cloud_metter_model": SensorEntityDescription(
        key="cloud_metter_model",
    ),
    "cloud_metter_sn": SensorEntityDescription(
        key="cloud_metter_sn",
    ),
    "cloud_metter_phase_a_power": SensorEntityDescription(
        key="cloud_metter_phase_a_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "distributed_device_status": SensorEntityDescription(
        key="distributed_device_status",
    ),
    "energy_backup_state": SensorEntityDescription(
        key="energy_backup_state",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "feed_grid_mode": SensorEntityDescription(
        key="feed_grid_mode",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "grid_code_selection": SensorEntityDescription(
        key="grid_code_selection",
    ),
    "grid_code_version": SensorEntityDescription(
        key="grid_code_version",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "grid_connection_sta": SensorEntityDescription(
        key="grid_connection_sta",
    ),
    "grid_sys_device_cnt": SensorEntityDescription(
        key="grid_sys_device_cnt",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "scoket1_bind_device_sn": SensorEntityDescription(
        key="scoket1_bind_device_sn",
    ),
    "scoket2_bind_device_sn": SensorEntityDescription(
        key="scoket2_bind_device_sn",
    ),
    "series_connect_device_id": SensorEntityDescription(
        key="series_connect_device_id",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "series_connect_device_status": SensorEntityDescription(
        key="series_connect_device_status",
    ),
    "system_group_id": SensorEntityDescription(
        key="system_group_id",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "system_mesh_id": SensorEntityDescription(
        key="system_mesh_id",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "town_code": SensorEntityDescription(
        key="town_code",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "update_ban_flag": SensorEntityDescription(
        key="update_ban_flag",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "utc_timezone": SensorEntityDescription(
        key="utc_timezone",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "utc_timezone_id": SensorEntityDescription(
        key="utc_timezone_id",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: DeviceConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    device = config_entry.runtime_data

    new_sensors = [
        EcoflowSensor(device, sensor)
        for sensor in SENSOR_TYPES
        if hasattr(device, sensor)
    ]

    if new_sensors:
        async_add_entities(new_sensors)


class EcoflowSensor(EcoflowEntity, SensorEntity):
    """Base representation of a sensor."""

    def __init__(self, device: DeviceBase, sensor: str):
        """Initialize the sensor."""
        super().__init__(device)

        self._sensor = sensor
        self._attr_unique_id = f"{device.name}_{sensor}"

        if sensor in SENSOR_TYPES:
            self.entity_description = SENSOR_TYPES[sensor]
            if self.entity_description.translation_key is None:
                self._attr_translation_key = self.entity_description.key

        self._attribute_fields = (
            self.entity_description.state_attribute_fields
            if isinstance(self.entity_description, EcoflowSensorEntityDescription)
            else []
        )

    @property
    def native_value(self):
        """Return the value of the sensor."""
        value = getattr(self._device, self._sensor, None)
        if isinstance(value, Enum):
            return value.name.lower()
        return value

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        if not self._attribute_fields:
            return {}

        return {
            field_name: getattr(self._device, field_name)
            for field_name in self._attribute_fields
            if hasattr(self._device, field_name)
        }

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._device.register_callback(self.async_write_ha_state, self._sensor)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._device.remove_callback(self.async_write_ha_state, self._sensor)
