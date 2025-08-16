from custom_components.ef_ble.eflib.devices import stream_ac

from ..props import ProtobufProps, pb_field

pb = stream_ac.pb


# This class expands on the base stream_ac.Device class, adding properties
# specific to the STREAM AC PRO model.
# @see stream_ac.py
class Device(stream_ac.Device, ProtobufProps):
    """STREAM AC PRO"""

    SN_PREFIX = (b"BK31",)

    ac_power_1 = pb_field(pb.pow_get_schuko1)
    ac_power_2 = pb_field(pb.pow_get_schuko2)

    ac_1 = pb_field(pb.relay2_onoff)
    ac_2 = pb_field(pb.relay3_onoff)

    # Sniffer data
    bms_batt_heating = pb_field(pb.bms_batt_heating)
    bms_batt_soh = pb_field(pb.bms_batt_soh, lambda v: round(v, 2))
    bms_chg_dsg_state = pb_field(pb.bms_chg_dsg_state)
    bms_chg_rem_time = pb_field(pb.bms_chg_rem_time)
    bms_design_cap = pb_field(pb.bms_design_cap)
    bms_dsg_rem_time = pb_field(pb.bms_dsg_rem_time)
    bms_max_mos_temp = pb_field(pb.bms_max_mos_temp)
    bms_min_cell_temp = pb_field(pb.bms_min_cell_temp)
    bms_min_mos_temp = pb_field(pb.bms_min_mos_temp)
    brightness = pb_field(pb.brightness)
    busbar_pow_limit = pb_field(pb.busbar_pow_limit)
    cloud_metter_model = pb_field(pb.cloud_metter.model)
    cloud_metter_sn = pb_field(pb.cloud_metter.sn)
    cloud_metter_phase_a_power = pb_field(pb.cloud_metter.phase_a_power)
    cms_batt_full_energy = pb_field(pb.cms_batt_full_energy)
    cms_batt_pow_in_max = pb_field(pb.cms_batt_pow_in_max)
    cms_batt_pow_out_max = pb_field(pb.cms_batt_pow_out_max)
    cms_batt_soc = pb_field(pb.cms_batt_soc, lambda v: round(v, 2))
    cms_batt_soh = pb_field(pb.cms_batt_soh, lambda v: round(v, 2))
    cms_bms_run_state = pb_field(pb.cms_bms_run_state)
    cms_chg_dsg_state = pb_field(pb.cms_chg_dsg_state)
    cms_chg_rem_time = pb_field(pb.cms_chg_rem_time)
    cms_dsg_rem_time = pb_field(pb.cms_dsg_rem_time)
    dev_ctrl_status = pb_field(pb.dev_ctrl_status)
    distributed_device_status = pb_field(pb.distributed_device_status)
    energy_backup_state = pb_field(pb.energy_backup_state)
    grid_code_selection = pb_field(pb.grid_code_selection)
    grid_code_version = pb_field(pb.grid_code_version)
    grid_connection_sta = pb_field(pb.grid_connection_sta)
    grid_sys_device_cnt = pb_field(pb.grid_sys_device_cnt)
    max_bp_input = pb_field(pb.max_bp_input)
    max_bp_output = pb_field(pb.max_bp_output)
    max_inv_input = pb_field(pb.max_inv_input)
    max_inv_output = pb_field(pb.max_inv_output)
    module_wifi_rssi = pb_field(pb.module_wifi_rssi)
    pow_consumption_measurement = pb_field(pb.pow_consumption_measurement)
    pow_get_bp_cms = pb_field(pb.pow_get_bp_cms, lambda v: round(v, 2))
    pow_get_schuko1 = pb_field(pb.pow_get_schuko1, lambda v: round(v, 2))
    pow_get_schuko2 = pb_field(pb.pow_get_schuko2, lambda v: round(v, 2))
    pow_get_sys_grid = pb_field(pb.pow_get_sys_grid, lambda v: round(v, 2))
    pow_get_sys_load = pb_field(pb.pow_get_sys_load, lambda v: round(v, 2))
    pow_sys_ac_in_max = pb_field(pb.pow_sys_ac_in_max)
    pow_sys_ac_out_max = pb_field(pb.pow_sys_ac_out_max)
    scoket1_bind_device_sn = pb_field(pb.scoket1_bind_device_sn)
    scoket2_bind_device_sn = pb_field(pb.scoket2_bind_device_sn)
    series_connect_device_id = pb_field(pb.series_connect_device_id)
    series_connect_device_status = pb_field(pb.series_connect_device_status)
    socket_measure_power = pb_field(pb.socket_measure_power, lambda v: round(v, 2))
    sys_grid_connection_power = pb_field(
        pb.sys_grid_connection_power, lambda v: round(v, 2)
    )
    system_group_id = pb_field(pb.system_group_id)
    system_mesh_id = pb_field(pb.system_mesh_id)
    town_code = pb_field(pb.town_code)
    update_ban_flag = pb_field(pb.update_ban_flag)
    utc_timezone = pb_field(pb.utc_timezone)
    utc_timezone_id = pb_field(pb.utc_timezone_id)
