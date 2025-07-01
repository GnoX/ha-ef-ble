from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from ..commands import TimeCommands
from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import ge305_sys_pb2
from ..props import ProtobufProps, pb_field, proto_attr_mapper
from ..props.enums import IntFieldValue

pb = proto_attr_mapper(ge305_sys_pb2.DisplayPropertyUpload)


class FuelType(IntFieldValue):
    UNKNOWN = -1

    LNG = 1
    LPG = 2
    OIL = 3


class EngineOpen(IntFieldValue):
    UNKNOWN = -1

    CLOSED = 0
    OPENED = 1
    CLOSING = 2


class SubBatteryState(IntFieldValue):
    UNKNOWN = -1

    IDLE = 0
    NO_INPUT = 1
    DISCHARGING = 2
    CHARGING = 3
    NORMAL_FULL = 4
    NORMAL_LOW_PRESSURE = 5


class PerformanceMode(IntFieldValue):
    UNKNOWN = -1

    ECO = 0
    PERFORMANCE = 1
    AUTO = 2


class LiquefiedGasType(IntFieldValue):
    UNKNOWN = -1

    LNG = 0
    LPG = 1


class LiquefiedGasUnit(IntFieldValue):
    UNKNOWN = -1

    LB = 0
    KG = 1

    G = 2
    LPH = 3
    LPM = 4
    GALH = 5
    GALM = 6


class XT150ChargeType(IntFieldValue):
    UNKNOWN = -1

    NONE = 0
    CHARGE_OUT = 1
    CHARGE = 2
    OUT = 3


class AbnormalState(IntFieldValue):
    UNKNOWN = -1

    NO = 0
    OIL_LOW = 1


class Device(DeviceBase, ProtobufProps):
    """Smart Generator"""

    SN_PREFIX = (b"G371",)
    NAME_PREFIX = "EF-GE4"

    output_power = pb_field(pb.pow_out_sum_w)
    ac_output_power = pb_field(pb.pow_get_ac)
    dc_output_power = pb_field(pb.pow_get_dc)

    # xt150_battery_level = pb_field(pb.cms_batt_soc)
    # xt150_charge_type = pb_field(pb.plug_in_info_dcp_dsg_chg_type)

    engine_on = pb_field(
        pb.generator_engine_open,
        lambda x: EngineOpen.from_value(x) in [EngineOpen.OPENED, EngineOpen.CLOSING],
    )
    engine_state = pb_field(pb.generator_engine_open, EngineOpen.from_value)
    performance_mode = pb_field(pb.generator_perf_mode, PerformanceMode.from_value)

    self_start = pb_field(pb.cms_oil_self_start)

    liquefied_gas_type = pb_field(
        pb.fuels_liquefied_gas_type, LiquefiedGasType.from_value
    )
    liquefied_gas_unit = pb_field(
        pb.fuels_liquefied_gas_uint, LiquefiedGasUnit.from_value
    )
    liquefied_gas_value = pb_field(pb.fuels_liquefied_gas_val)
    liquefied_gas_consumption = pb_field(pb.fuels_liquefied_gas_consume_per_hour)

    generator_total_output = pb_field(pb.generator_total_output)
    generator_abnormal_state = pb_field(
        pb.generator_abnormal_state, lambda x: AbnormalState.from_value(x & 1)
    )

    sub_battery_soc = pb_field(pb.generator_sub_battery_soc)
    sub_battery_state = pb_field(
        pb.generator_sub_battery_state, SubBatteryState.from_value
    )

    ac_ports = pb_field(pb.ac_out_open)

    fuel_type = pb_field(pb.generator_fuels_type, FuelType.from_value)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)

    @staticmethod
    def check(sn):
        return sn.startswith(Device.SN_PREFIX)

    @property
    def device(self):
        return "Smart Generator 3000 (Dual Fuel)"

    async def packet_parse(self, data: bytes) -> Packet:
        return Packet.fromBytes(data, is_xor=True)

    async def data_parse(self, packet: Packet):
        processed = False

        if packet.src == 0x08 and packet.cmdSet == 0xFE and packet.cmdId == 0x15:
            self.update_from_bytes(ge305_sys_pb2.DisplayPropertyUpload, packet.payload)
            processed = True
        elif (
            packet.src == 0x35
            and packet.cmdSet == 0x01
            and packet.cmdId == Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME
        ):
            if len(packet.payload) == 0:
                self._time_commands.async_send_all()
            processed = True

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed

    async def _send_config_packet(self, message: ge305_sys_pb2.ConfigWrite):
        payload = message.SerializeToString()
        packet = Packet(0x20, 0x08, 0xFE, 0x11, payload, 0x01, 0x01, 0x13)
        await self._conn.sendPacket(packet)

    async def enable_ac_port(self, enabled: bool):
        await self._send_config_packet(
            ge305_sys_pb2.ConfigWrite(cfg_ac_out_open=enabled)
        )

    async def enable_self_start(self, enabled: bool):
        await self._send_config_packet(
            ge305_sys_pb2.ConfigWrite(cfg_generator_self_on=enabled)
        )

    async def enable_engine_on(self, enabled: bool):
        value = EngineOpen.OPENED if enabled else EngineOpen.CLOSED
        await self._send_config_packet(
            ge305_sys_pb2.ConfigWrite(cfg_generator_engine_open=value.value)
        )

    async def set_engine_open(self, engine_open: EngineOpen):
        if engine_open is EngineOpen.CLOSING:
            return

        await self._send_config_packet(
            ge305_sys_pb2.ConfigWrite(cfg_generator_engine_open=engine_open.value)
        )

    async def set_performance_mode(self, performance_mode: PerformanceMode):
        await self._send_config_packet(
            ge305_sys_pb2.ConfigWrite(cfg_generator_perf_mode=performance_mode.value)
        )

    async def set_dc_output_power_max(self, dc_out_max: int):
        await self._send_config_packet(
            ge305_sys_pb2.ConfigWrite(cfg_generator_dc_out_pow_max=dc_out_max)
        )
