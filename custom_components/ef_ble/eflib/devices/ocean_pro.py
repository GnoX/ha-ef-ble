from ..pb import dev_apl_comm_pb2
from ..props import pb_field, proto_attr_mapper
from ..props.transforms import pround
from ._v4_panel import GridStatus, V4PanelDevice

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)
pb_rt = proto_attr_mapper(dev_apl_comm_pb2.RuntimePropertyUpload)


class Device(V4PanelDevice):
    """OCEAN Pro"""

    SN_PREFIX = (b"HR51",)
    NAME_PREFIX = "EF-HR5"

    _TELEMETRY_SRC = 0x30

    battery_level = pb_field(pb.cms_batt_soc, pround(2))
    battery_power = pb_field(pb.pow_get_bp_cms, pround(2))

    load_system = pb_field(pb.pow_get_sys_load, pround(2))
    load_from_grid = pb_field(pb.pow_get_sys_grid, pround(2))
    pv_power_sum = pb_field(pb.pow_get_pv_sum, pround(2))

    remaining_time_charging = pb_field(pb.cms_chg_rem_time)
    remaining_time_discharging = pb_field(pb.cms_dsg_rem_time)

    grid_connection_status = pb_field(pb.grid_connection_sta, GridStatus.from_value)
    grid_is_energized = pb_field(pb.grid_is_energized)
    plugged_in_ac = pb_field(pb.plug_in_info_acp_charger_flag)

    inverter_frequency = pb_field(pb_rt.third_inv_offgrid_ctrl_freq_curr, pround(2))

    def _parse_telemetry(self, body: bytes) -> None:
        # A single upload carries either display or runtime properties; parsing against
        # both is safe since absent fields report no presence and are skipped rather
        # than overwritten with defaults.
        self.update_from_bytes(dev_apl_comm_pb2.DisplayPropertyUpload, body)
        self.update_from_bytes(dev_apl_comm_pb2.RuntimePropertyUpload, body)
