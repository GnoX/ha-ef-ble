from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from google.protobuf.message import Message

from ..entity import controls
from ..entity.base import dynamic
from ..packet import Packet
from ..pb import dev_apl_comm_pb2, jt_s1_sys_pb2
from ..props import pb_field, pb_field_group, proto_attr_mapper
from ..props.transforms import out_power, pround
from ._v4_panel import GridStatus, V4PanelDevice

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)
pb_rt = proto_attr_mapper(dev_apl_comm_pb2.RuntimePropertyUpload)


class Device(V4PanelDevice):
    """OCEAN Pro"""

    SN_PREFIX = (b"HR51",)
    NAME_PREFIX = "EF-HR5"

    _TELEMETRY_SRC = 0x30

    _KEEPALIVE_INTERVAL = 10
    _REPORT_RATE_INTERVAL = 25

    battery_level = pb_field(pb.cms_batt_soc, pround(2))
    battery_power = pb_field(pb.pow_get_bp_cms, pround(2))

    load_system = pb_field(pb.pow_get_sys_load, pround(2))
    load_from_grid = pb_field(pb.pow_get_sys_grid, pround(2))
    pv_power_sum = pb_field(pb.pow_get_pv_sum, pround(2))

    remaining_time_charging = pb_field(pb.cms_chg_rem_time)
    remaining_time_discharging = pb_field(pb.cms_dsg_rem_time)

    grid_connection_status = pb_field(pb.grid_connection_sta, GridStatus.from_value)

    battery_charge_limit_min = pb_field(pb.cms_min_dsg_soc)
    battery_charge_limit_max = pb_field(pb.cms_max_chg_soc)

    grid_frequency = pb_field(pb_rt.dt_pcs_ecap_grid_freq_lpf, pround(2))
    ac_output_power = pb_field(pb.pow_get_ac, out_power)

    l_voltage = pb_field_group(
        pb_rt.dt_pcs_grid_vol_l1_rms,
        match="dt_pcs_grid_vol_l{n}_rms",
        count=2,
        transform=pround(1),
        name_template="l{n}_voltage",
    )
    l_current = pb_field_group(
        pb_rt.dt_pcs_grid_curr_l1_rms,
        match="dt_pcs_grid_curr_l{n}_rms",
        count=2,
        transform=pround(2),
        name_template="l{n}_current",
    )
    l_power = pb_field_group(
        pb_rt.dt_pcs_active_power_l1,
        match="dt_pcs_active_power_l{n}",
        count=2,
        transform=out_power,
        name_template="l{n}_power",
    )

    # PV strings 1-8: string 1 has no index suffix in the proto, and PV power is
    # reported in the display upload while voltage/current come from the runtime upload.
    pv_voltage_1 = pb_field(pb_rt.dt_pv_vol_current, pround(1))
    pv_current_1 = pb_field(pb_rt.dt_pv_cur_current, pround(2))
    pv_power_1 = pb_field(pb.dt_pv_pwr_current, pround(1))
    pv_voltage = pb_field_group(
        pb_rt.dt_pv2_vol_current,
        match="dt_pv{n}_vol_current",
        count=7,
        start=2,
        transform=pround(1),
        name_template="pv_voltage_{n}",
    )
    pv_current = pb_field_group(
        pb_rt.dt_pv2_cur_current,
        match="dt_pv{n}_cur_current",
        count=7,
        start=2,
        transform=pround(2),
        name_template="pv_current_{n}",
    )
    pv_power = pb_field_group(
        pb.dt_pv2_pwr_current,
        match="dt_pv{n}_pwr_current",
        count=7,
        start=2,
        transform=pround(1),
        name_template="pv_power_{n}",
    )

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self.add_timer_task(
            self._send_report_rate_ctrl, interval=self._REPORT_RATE_INTERVAL
        )

    async def _send_keepalive(self) -> None:
        await self._conn.sendPacket(
            Packet(
                src=0x21,
                dst=0x60,
                cmd_set=0x60,
                cmd_id=0x61,
                payload=bytes([0x08, 0x01]),
                dsrc=0x01,
                ddst=0x01,
                version=0x13,
            ),
            wait_for_response=False,
        )

    async def _send_report_rate_ctrl(self) -> None:
        await self._conn.sendPacket(
            Packet(
                src=0x21,
                dst=0x60,
                cmd_set=0x60,
                cmd_id=0x74,
                payload=bytes([0x08, 0x01, 0x20, 0x03, 0x28, 0x01]),
                dsrc=0x01,
                ddst=0x01,
                version=0x13,
            ),
            wait_for_response=False,
        )

    def _parse_telemetry(self, body: bytes) -> None:
        self.update_from_bytes(dev_apl_comm_pb2.DisplayPropertyUpload, body)
        self.update_from_bytes(dev_apl_comm_pb2.RuntimePropertyUpload, body)

    async def _send_s1_config(self, cmd_id: int, message: Message) -> None:
        await self._conn.sendPacket(
            Packet(
                src=0x21,
                dst=0x60,
                cmd_set=0x60,
                cmd_id=cmd_id,
                payload=message.SerializeToString(),
                dsrc=0x01,
                ddst=0x01,
                version=0x13,
            ),
            wait_for_response=False,
        )

    @controls.battery(
        battery_charge_limit_min,
        max=dynamic(battery_charge_limit_max),
    )
    async def set_battery_charge_limit_min(self, limit: float):
        message = jt_s1_sys_pb2.SysBatChgDsgSet(sys_bat_dsg_down_limie=int(limit))
        if self.battery_charge_limit_max is not None:
            message.sys_bat_chg_up_limit = int(self.battery_charge_limit_max)
        await self._send_s1_config(0x70, message)
        return True

    @controls.battery(
        battery_charge_limit_max,
        min=dynamic(battery_charge_limit_min),
    )
    async def set_battery_charge_limit_max(self, limit: float):
        message = jt_s1_sys_pb2.SysBatChgDsgSet(sys_bat_chg_up_limit=int(limit))
        if self.battery_charge_limit_min is not None:
            message.sys_bat_dsg_down_limie = int(self.battery_charge_limit_min)
        await self._send_s1_config(0x70, message)
        return True
