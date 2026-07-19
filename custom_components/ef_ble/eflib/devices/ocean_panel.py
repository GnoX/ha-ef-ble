from ..entity import controls
from ..pb import dev_apl_comm_pb2
from ..props import (
    pb_field,
    pb_field_group,
    proto_attr_mapper,
)
from ..props.protobuf_field import TransformIfMissing
from ..props.transforms import pround
from ._v4_panel import CircuitStatus, GridStatus, V4PanelDevice

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)
pb_rt = proto_attr_mapper(dev_apl_comm_pb2.RuntimePropertyUpload)


class Device(V4PanelDevice):
    """OCEAN Panel"""

    SN_PREFIX = (b"HR61", b"HR6B", b"HR6D")
    NAME_PREFIX = "EF-HR6"

    @property
    def supports_device_token(self) -> bool:
        return True

    NUM_OF_CIRCUITS = 40
    _TELEMETRY_SRC = 0x30

    battery_level = pb_field(pb.cms_batt_soc, pround(2))
    battery_power = pb_field(pb.pow_get_bp_cms, pround(2))

    load_system = pb_field(pb.pow_get_sys_load, pround(2))
    load_from_grid = pb_field(pb.pow_get_sys_grid, pround(2))
    home_load = pb_field(pb.pow_home_load, pround(2))
    sub_panel_load = pb_field(pb.pow_sub_panel_load_w, pround(2))
    ev_load = pb_field(pb.pow_ev_load_w, pround(2))
    pv_power_sum = pb_field(pb.pow_get_pv_sum, pround(2))

    remaining_time_charging = pb_field(pb.cms_chg_rem_time)
    remaining_time_discharging = pb_field(pb.cms_dsg_rem_time)

    grid_connection_status = pb_field(pb.grid_connection_sta, GridStatus.from_value)
    grid_is_energized = pb_field(pb.grid_is_energized)
    plugged_in_ac = pb_field(pb.plug_in_info_acp_charger_flag)

    inverter_frequency = pb_field(pb_rt.third_inv_offgrid_ctrl_freq_curr, pround(2))

    circuit_power = pb_field_group(
        pb.load_ch1_sample_info.load_ch_power,
        match="load_ch{n}_sample_info",
        count=NUM_OF_CIRCUITS,
        transform=pround(2),
        name_template="circuit_power_{n}",
    )
    circuit_current = pb_field_group(
        pb.load_ch1_sample_info.load_ch_curr,
        match="load_ch{n}_sample_info",
        count=NUM_OF_CIRCUITS,
        transform=pround(2),
        name_template="circuit_current_{n}",
    )
    circuit_voltage = pb_field_group(
        pb.load_ch1_sample_info.load_ch_vol,
        match="load_ch{n}_sample_info",
        count=NUM_OF_CIRCUITS,
        transform=pround(1),
        name_template="circuit_voltage_{n}",
    )

    circuit_status = pb_field_group(
        pb.load_ch1_sta.load_sta,
        match="load_ch{n}_sta",
        count=NUM_OF_CIRCUITS,
        transform=TransformIfMissing(lambda v: CircuitStatus.from_value(v or 0)),
        name_template="circuit_status_{n}",
    )
    circuit_name = pb_field_group(
        pb.load_ch1_sta.ch_name,
        match="load_ch{n}_sta",
        count=NUM_OF_CIRCUITS,
        name_template="circuit_name_{n}",
    )
    circuit_is_enabled = pb_field_group(
        pb.load_ch1_sta.load_sta,
        match="load_ch{n}_sta",
        count=NUM_OF_CIRCUITS,
        transform=TransformIfMissing(lambda v: (v or 0) in (1, 2)),
        name_template="circuit_is_enabled_{n}",
    )
    circuit_split_link = pb_field_group(
        pb.load_ch1_sta.splitphase.link_ch,
        match="load_ch{n}_sta",
        count=NUM_OF_CIRCUITS,
        name_template="circuit_split_link_{n}",
    )
    circuit_split_info_loaded = pb_field_group(
        pb.load_ch1_sta.splitphase.link_ch,
        match="load_ch{n}_sta",
        count=NUM_OF_CIRCUITS,
        transform=lambda value: value is not None,
        name_template="circuit_split_info_loaded_{n}",
    )

    @controls.for_each(
        circuit_is_enabled,
        control=controls.outlet,
        availability=circuit_split_info_loaded,
        translation_key="circuit_is_enabled",
        translation_placeholders=lambda i: {"circuit": str(i)},
    )
    async def set_circuit_power(self, circuit_id: int, enable: bool):
        self._logger.debug("set_circuit_power for %d: %s", circuit_id, enable)
        config = self._build_circuit_power_config(circuit_id, enable)
        if config is not None:
            await self._send_config_packet(config)

    def _parse_telemetry(self, body: bytes) -> None:
        self.update_from_bytes(dev_apl_comm_pb2.DisplayPropertyUpload, body)
        self.update_from_bytes(dev_apl_comm_pb2.RuntimePropertyUpload, body)
