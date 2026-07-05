from ..entity import controls
from ..entity.base import dynamic
from ..pb import dev_apl_comm_pb2
from ..props import (
    computed_field,
    pb_field,
    pb_field_group,
    pb_indexed_attr,
    proto_attr_mapper,
)
from ..props.enums import IntFieldValue
from ..props.protobuf_field import TransformIfMissing
from ..props.transforms import pround
from ._v4_panel import CircuitStatus, GridStatus, V4PanelDevice

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)
pb_cfg = proto_attr_mapper(dev_apl_comm_pb2.ConfigWrite)


class OperatingMode(IntFieldValue):
    """SHP3 energy-strategy operating mode (`CfgEnergyStrategyOperateMode` subfields)"""

    UNKNOWN = -1

    NONE = 0  # no operating mode selected ("Backup")
    SELF_POWERED = 1
    SCHEDULED = 2
    INTELLIGENT = 6


class BackupChannelType(IntFieldValue):
    UNKNOWN = -1

    NONE = 0
    BATTERY = 1
    OIL = 2
    STATION_CHARGER = 3


def _operating_mode_from_message(
    message: (
        dev_apl_comm_pb2.CfgEnergyStrategyOperateMode
        | dev_apl_comm_pb2.CfgPanelEnergyStrategyOperateMode
    ),
) -> OperatingMode:
    if message.operate_self_powered_open:
        return OperatingMode.SELF_POWERED
    if message.operate_scheduled_open:
        return OperatingMode.SCHEDULED
    if message.operate_intelligent_schedule_mode_open:
        return OperatingMode.INTELLIGENT
    return OperatingMode.NONE


def _channel_enabled(info: dev_apl_comm_pb2.BackupChInfo) -> bool | None:
    if not info.ch_dev_type:
        return None
    return info.ch_sta == 1


def _channel_type(info: dev_apl_comm_pb2.BackupChInfo) -> "BackupChannelType | None":
    if not info.ch_dev_type:
        return None
    return BackupChannelType.from_value(info.ch_dev_type)


def _channel_force_charging(info: dev_apl_comm_pb2.BackupChInfo) -> bool | None:
    if not info.ch_dev_type:
        return None
    return info.force_chg_sta == 1


def _channel_signal_connected(info: dev_apl_comm_pb2.BackupChInfo) -> bool | None:
    if not info.ch_dev_type:
        return None
    return info.signal_line_sta == 1


class Device(V4PanelDevice):
    """Smart Home Panel 3"""

    SN_PREFIX = (b"HR62", b"HR63", b"HR6C")
    NAME_PREFIX = "EF-SHP3"

    NUM_OF_CIRCUITS = 32
    NUM_OF_CHANNELS = 3
    _TELEMETRY_SRC = 0x32

    battery_level = pb_field(pb.cms_batt_soc, pround(2))
    remaining_time_charging = pb_field(pb.cms_chg_rem_time)
    remaining_time_discharging = pb_field(pb.cms_dsg_rem_time)

    battery_charge_limit_min = pb_field(pb.cms_min_dsg_soc)
    battery_charge_limit_max = pb_field(pb.cms_max_chg_soc)
    backup_reserve_level = pb_field(pb.backup_reverse_soc)

    l1_power = pb_field(pb.grid_connection_power_L1, pround(2))
    l2_power = pb_field(pb.grid_connection_power_L2, pround(2))
    l3_power = pb_field(pb.grid_connection_power_L3, pround(2))

    l1_voltage = pb_field(pb.grid_connection_vol_L1, pround(1))
    l2_voltage = pb_field(pb.grid_connection_vol_L2, pround(1))
    l3_voltage = pb_field(pb.grid_connection_vol_L3, pround(1))

    l1_current = pb_field(pb.grid_connection_amp_L1, pround(2))
    l2_current = pb_field(pb.grid_connection_amp_L2, pround(2))
    l3_current = pb_field(pb.grid_connection_amp_L3, pround(2))

    grid_connection_status = pb_field(pb.grid_connection_sta, GridStatus.from_value)
    grid_is_energized = pb_field(pb.grid_is_energized)

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
    circuit_is_enabled = pb_field_group(
        pb.load_ch1_sta.load_sta,
        match="load_ch{n}_sta",
        count=NUM_OF_CIRCUITS,
        transform=TransformIfMissing(lambda v: (v or 0) in (1, 2)),
        name_template="circuit_is_enabled_{n}",
    )
    circuit_name = pb_field_group(
        pb.load_ch1_sta.ch_name,
        match="load_ch{n}_sta",
        count=NUM_OF_CIRCUITS,
        name_template="circuit_name_{n}",
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

    load_system = pb_field(pb.pow_get_sys_load, pround(2))
    load_from_grid = pb_field(pb.pow_get_sys_grid, pround(2))
    battery_power = pb_field(pb.pow_get_bp_cms, pround(2))
    pv_power_sum = pb_field(pb.pow_get_pv_sum, pround(2))

    # Per-channel enable state, driving the switch control below. ch_sta is the
    # enable/connected status (None for an empty channel); the switch writes ctrl_en.
    channel_is_enabled = pb_field_group(
        pb.panel_backup_ch1_Info,
        match="panel_backup_ch{n}_Info",
        count=NUM_OF_CHANNELS,
        transform=_channel_enabled,
        name_template="ch{n}_is_enabled",
    )

    channel_type = pb_field_group(
        pb.panel_backup_ch1_Info,
        match="panel_backup_ch{n}_Info",
        count=NUM_OF_CHANNELS,
        transform=_channel_type,
        name_template="ch{n}_type",
    )
    channel_force_charge = pb_field_group(
        pb.panel_backup_ch1_Info,
        match="panel_backup_ch{n}_Info",
        count=NUM_OF_CHANNELS,
        transform=_channel_force_charging,
        name_template="ch{n}_force_charge",
    )
    channel_signal_line = pb_field_group(
        pb.panel_backup_ch1_Info,
        match="panel_backup_ch{n}_Info",
        count=NUM_OF_CHANNELS,
        transform=_channel_signal_connected,
        name_template="ch{n}_signal_line",
    )

    ac_charging_speed = pb_field(pb.panel_max_charge_pow_set)
    min_ac_charging_power = 600
    max_ac_charging_power = 12000
    ac_charging_speed_step = 100

    storm_guard = pb_field(pb.storm_pattern_enable)

    _mode_panel = pb_field(
        pb.panle_energy_strategy_operate_mode, _operating_mode_from_message
    )
    _mode_generic = pb_field(
        pb.energy_strategy_operate_mode, _operating_mode_from_message
    )
    _eps_mode = pb_field(
        pb.panle_energy_strategy_operate_mode.operate_eps_mode,
        TransformIfMissing(bool),
    )
    _mix_scheduled = pb_field(
        pb.panle_energy_strategy_operate_mode.operate_mix_scheduled_open,
        TransformIfMissing(bool),
    )

    @computed_field
    def operating_mode_select(self) -> OperatingMode | None:
        if self._mode_panel is not None:
            return self._mode_panel
        return self._mode_generic

    def _parse_telemetry(self, body: bytes) -> None:
        self.update_from_bytes(dev_apl_comm_pb2.DisplayPropertyUpload, body)

    @controls.battery(
        battery_charge_limit_min,
        max=dynamic(battery_charge_limit_max),
    )
    async def set_battery_charge_limit_min(self, limit: float):
        await self._send_config_packet(
            dev_apl_comm_pb2.ConfigWrite(cfg_min_dsg_soc=int(limit))
        )
        return True

    @controls.battery(
        battery_charge_limit_max,
        min=dynamic(battery_charge_limit_min),
    )
    async def set_battery_charge_limit_max(self, limit: float):
        await self._send_config_packet(
            dev_apl_comm_pb2.ConfigWrite(cfg_max_chg_soc=int(limit))
        )
        return True

    @controls.battery(backup_reserve_level, max=100)
    async def set_backup_reserve_level(self, value: float):
        await self._send_config_packet(
            dev_apl_comm_pb2.ConfigWrite(cfg_backup_reverse_soc=int(value))
        )
        return True

    @controls.power(
        ac_charging_speed,
        min=min_ac_charging_power,
        max=max_ac_charging_power,
        step=ac_charging_speed_step,
    )
    async def set_ac_charging_speed(self, value: float):
        watts = int(value) // self.ac_charging_speed_step * self.ac_charging_speed_step
        await self._send_config_packet(
            dev_apl_comm_pb2.ConfigWrite(cfg_panel_max_charge_pow_set=watts)
        )
        return True

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
        return True

    @controls.select(operating_mode_select, options=OperatingMode)
    async def set_operating_mode(self, mode: OperatingMode):
        if mode is OperatingMode.UNKNOWN:
            return

        config = dev_apl_comm_pb2.ConfigWrite()
        message = config.cfg_panle_energy_strategy_operate_mode
        message.operate_self_powered_open = mode is OperatingMode.SELF_POWERED
        message.operate_scheduled_open = mode is OperatingMode.SCHEDULED
        message.operate_intelligent_schedule_mode_open = (
            mode is OperatingMode.INTELLIGENT
        )
        message.operate_eps_mode = bool(self._eps_mode)
        message.operate_mix_scheduled_open = bool(self._mix_scheduled)

        await self._send_config_packet(config)

    @controls.switch(storm_guard)
    async def set_storm_guard(self, enable: bool):
        config = dev_apl_comm_pb2.ConfigWrite()
        config.cfg_storm_pattern.storm_pattern_enable = enable
        await self._send_config_packet(config)

    @controls.for_each(
        channel_is_enabled,
        control=controls.switch,
        translation_key="channel_is_enabled",
        translation_placeholders=lambda i: {"channel": str(i)},
    )
    async def set_channel_enable(self, channel_id: int, enable: bool):
        """
        Enable / disable a backup channel via `cfg_panel_backup_ch{N}_ctrl`.

        `BackupCtrl` carries both the channel enable (ctrl_en) and the force-charge
        toggle (ctrl_force_chg), and the panel applies them together, so we send the
        current force-charge state alongside the new enable value (on = 1, off = 2).
        """
        config = dev_apl_comm_pb2.ConfigWrite()
        ctrl = pb_indexed_attr(
            config, pb_cfg.cfg_panel_backup_ch1_ctrl, "cfg_panel_backup_ch{n}_ctrl"
        )
        backup = ctrl[channel_id]
        backup.ctrl_en = 1 if enable else 2
        backup.ctrl_force_chg = 1 if self.channel_force_charge[channel_id] else 2
        await self._send_config_packet(config)
