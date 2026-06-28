import time
from enum import IntEnum

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from google.protobuf.message import Message

from ..commands import TimeCommands
from ..devicebase import DeviceBase
from ..entity import controls
from ..entity.base import dynamic
from ..packet import Packet, PacketV4
from ..pb import dev_apl_comm_pb2
from ..props import (
    ProtobufProps,
    computed_field,
    pb_field,
    pb_field_group,
    pb_indexed_attr,
    proto_attr_mapper,
)
from ..props.enums import IntFieldValue
from ..props.protobuf_field import TransformIfMissing
from ..props.transforms import pround

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)
pb_cfg = proto_attr_mapper(dev_apl_comm_pb2.ConfigWrite)


class CircuitControl(IntEnum):
    ON = 1
    OFF = 2


class GridStatus(IntFieldValue):
    UNKNOWN = -1

    NOT_VALID = 0
    GRID_IN = 1
    GRID_OFFLINE = 2
    FEED_GRID = 3


class CircuitStatus(IntFieldValue):
    """Per-circuit relay status from `LoadChSta.load_sta` (`LOAD_CH_STA`)"""

    UNKNOWN = -1  # LOAD_CH_UNKNOWN_STA (4) and any unrecognized value

    OFF = 0  # relay open / circuit off
    ON_GRID = 1  # on, powered from grid
    ON_BACK = 2  # on, powered from battery backup
    EM_STOP = 3  # emergency stop


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


def _ac_input_connected(info: dev_apl_comm_pb2.BackupChInfo) -> bool | None:
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


class Device(DeviceBase, ProtobufProps):
    """Smart Home Panel 3"""

    SN_PREFIX = (b"HR62", b"HR63", b"HR6C")
    NAME_PREFIX = "EF-SHP3"

    NUM_OF_CIRCUITS = 32
    NUM_OF_CHANNELS = 3
    _KEEPALIVE_INTERVAL = 20

    _USERID_FIELD_LEN = 64

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

    ac1_input_connected = pb_field(pb.panel_backup_ch1_Info, _ac_input_connected)
    ac2_input_connected = pb_field(pb.panel_backup_ch2_Info, _ac_input_connected)
    ac3_input_connected = pb_field(pb.panel_backup_ch3_Info, _ac_input_connected)

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

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)
        self._routing = _StandardProtocolRouting(sn)
        self.add_timer_task(self._send_keepalive, interval=self._KEEPALIVE_INTERVAL)
        self._userid_sent = False

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    async def _send_keepalive(self) -> None:
        await self._time_commands.sendRTCCheck()

    async def _send_userid_registration(self) -> None:
        user_id = (getattr(self._conn, "_user_id", "") or "").encode("ascii")
        userid_field_len = 64
        payload = (
            bytes([0x01])
            + user_id[:userid_field_len].ljust(userid_field_len, b"\x00")
            + int(time.time()).to_bytes(4, "little")
        )
        packet = Packet(
            0x21,
            0x35,
            0x35,
            0xA8,
            payload,
            0x01,
            0x01,
            3,
        )
        await self._conn.sendPacket(packet, wait_for_response=False)

    async def packet_parse(self, data: bytes):
        return Packet.from_bytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        match packet.version, packet.src, packet.cmd_set, packet.cmd_id:
            case 0x04, 0x32, 0x40, 0x30:
                if isinstance(packet, PacketV4):
                    self._routing.remember_post(packet)
                _, body = self._routing.split(packet.payload)
                self.update_from_bytes(dev_apl_comm_pb2.DisplayPropertyUpload, body)
                processed = True
            case 0x04, _, 0x40, 0x30:
                # sub device update (per-battery telemetry forwarded by the panel)
                processed = True
            case _, 0x35, 0x01, Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME:
                if len(packet.payload) == 0:
                    self._time_commands.async_send_all()
                    if not self._userid_sent:
                        self._userid_sent = True
                        await self._send_userid_registration()
                processed = True
            case _, 0x35, 0x35, 0x20:
                await self._conn.replyPacket(packet)
                processed = True

        self._notify_updated()
        return processed

    async def _send_config_packet(self, message: Message):
        packet = self._routing.write_packet(message.SerializeToString())
        await self._conn.sendPacket(packet)

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

        split_link = self.circuit_split_link[circuit_id]
        if split_link is None:
            self._logger.warning(
                (
                    "Cannot set circuit power for circuit %d because split circuit "
                    "info is not available"
                ),
                circuit_id,
            )
            return None

        is_split = split_link != 0
        if is_split and (split_link < 1 or split_link > self.NUM_OF_CIRCUITS):
            self._logger.warning(
                (
                    "Cannot set circuit power for circuit %d because split link "
                    "circuit id %d is invalid"
                ),
                circuit_id,
                split_link,
            )
            return None

        config = dev_apl_comm_pb2.ConfigWrite()
        state = CircuitControl.ON if enable else CircuitControl.OFF
        ctrl = pb_indexed_attr(
            config, pb_cfg.cfg_load_ch1_ctrl_info, "cfg_load_ch{n}_ctrl_info"
        )

        ch = ctrl[circuit_id]
        ch.chanel_enable_ctrl = state
        ch.ctrl_mode = dev_apl_comm_pb2.LOAD_RLY_CTRL_MODE_HAND

        if is_split:
            ch_link = ctrl[split_link]
            ch_link.chanel_enable_ctrl = state
            ch_link.ctrl_mode = dev_apl_comm_pb2.LOAD_RLY_CTRL_MODE_HAND

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

    async def set_storm_guard(self, enable: bool):
        config = dev_apl_comm_pb2.ConfigWrite()
        config.cfg_storm_pattern.storm_pattern_enable = enable
        await self._send_config_packet(config)


class _StandardProtocolRouting:
    """
    SHP3 standard-protocol routing layer that wraps the protobuf inside the v4 payload.

    Reads: the v4 application payload is a routing header (the device-side SN fragment
    plus a 13-byte envelope) followed by the `DisplayPropertyUpload` protobuf.

    Writes: reconstruct the control frame - a v4 packet addressed src=0x21 dst=0x60,
    cmd_set=0xFE cmd_id=0x11, whose application payload is the routing header followed
    by the `ConfigWrite`. The routing header is the panel's own latest post routing
    header (device serial + envelope, captured verbatim) with the embedded standard-
    protocol command swapped to PROPERTY_WRITE (FE 11); the two v4 obfuscation keys are
    lifted from the same post. This mirrors the panel's exact addressing rather than
    rebuilding it from the host's connection serial.
    """

    HEADER_LEN = 22  # device SN fragment (9) + envelope (13), on reads
    _SERIAL_FRAGMENT_LEN = 9
    _ENVELOPE_LEN = 13
    _CMD_SET = 0xFE
    _PROPERTY_WRITE = 0x11
    _DEFAULT_V4_TYPE_A = 0x13
    _DEFAULT_V4_TYPE_B = 0x01

    def __init__(self, serial: str) -> None:
        self._serial = serial
        self._v4_type_a = self._DEFAULT_V4_TYPE_A
        self._v4_type_b = self._DEFAULT_V4_TYPE_B
        self._post_routing_header: bytes | None = None

    @classmethod
    def split(cls, payload: bytes) -> tuple[str, bytes]:
        """Split a v4 application payload into (device SN fragment, protobuf body)"""
        serial = payload[: cls._SERIAL_FRAGMENT_LEN].decode("ascii", errors="replace")
        return serial, payload[cls.HEADER_LEN :]

    def remember_post(self, packet: PacketV4) -> None:
        """Capture the post's v4 obfuscation keys and its routing header verbatim"""
        self._v4_type_a = packet.v4_type_a
        self._v4_type_b = packet.v4_type_b
        if len(packet.payload) >= self.HEADER_LEN:
            self._post_routing_header = bytes(packet.payload[: self.HEADER_LEN])

    def _routing_header(self) -> bytes:
        if self._post_routing_header is not None:
            header = bytearray(self._post_routing_header)
            # Envelope is `21 01 40 03 03 <seq> FE <cmd> ...`, so the standard-protocol
            # command sits right after the 0xFE marker at a fixed offset.
            fe = self._SERIAL_FRAGMENT_LEN + 6
            if fe + 1 < len(header) and header[fe] == self._CMD_SET:
                header[fe + 1] = self._PROPERTY_WRITE
            return bytes(header)

        # No post captured yet: best-effort rebuild from the host connection serial.
        # fmt: off
        envelope = bytes(
            [0x21, 0x01, 0x40, 0x03, 0x03, 0x00, self._CMD_SET, self._PROPERTY_WRITE,
             0x00, 0x00, 0x01, 0x21, 0x01]
        )
        # fmt: on
        return self._serial.encode("ascii") + envelope

    def write_packet(self, config_bytes: bytes) -> Packet | PacketV4:
        return PacketV4(
            src=0x21,
            dst=0x60,
            cmd_set=self._CMD_SET,
            cmd_id=self._PROPERTY_WRITE,
            payload=self._routing_header() + config_bytes,
            cmd_flags=0x20,
            v4_type_a=self._v4_type_a,
            v4_type_b=self._v4_type_b,
        )
