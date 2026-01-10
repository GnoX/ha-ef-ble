from ..devicebase import DeviceBase
from ..model.kt210_sac import KT210SAC
from ..packet import Packet
from ..props.enums import IntFieldValue
from ..props.raw_data_field import dataclass_attr_mapper, raw_field
from ..props.raw_data_props import RawDataProps

pb = dataclass_attr_mapper(KT210SAC)


class FanGear(IntFieldValue):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class MainMode(IntFieldValue):
    COLD = 0
    WARM = 1
    FAN = 2


class SubMode(IntFieldValue):
    MAX = 0
    NIGHT = 1
    ECO = 2
    NORMAL = 3


class PowerMode(IntFieldValue):
    INIT = 0
    ON = 1
    STANDBY = 2
    OFF = 3


class WaterLevel(IntFieldValue):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class DrainMode(IntFieldValue):
    EXTERNAL = 0
    DRAIN_FREE = 1

    @classmethod
    def from_int(cls, value: int) -> "DrainMode":
        if (value & 0b01) == 1:
            return cls.DRAIN_FREE
        return cls.EXTERNAL


class Device(DeviceBase, RawDataProps):
    """Wave 2"""

    SN_PREFIX = b"KT21"
    NAME_PREFIX = "EF-KT2"

    @property
    def packet_version(self):
        return 2

    battery_level = raw_field(pb.bat_soc)

    ambient_temperature = raw_field(pb.env_temp, lambda v: round(v, 2))
    outlet_temperature = raw_field(pb.outlet_temp, lambda v: round(v, 2))

    main_mode = raw_field(pb.mode, MainMode.from_value)
    sub_mode = raw_field(pb.sub_mode, SubMode.from_value)
    fan_speed = raw_field(pb.fan_value, FanGear.from_value)

    power_battery = raw_field(pb.bat_pwr_watt)
    power_psdr = raw_field(pb.psdr_pwr_watt)
    power_mppt = raw_field(pb.mptt_pwr_watt)

    drain_mode = raw_field(pb.wte_fth_en, DrainMode.from_int)
    automatic_drain = raw_field(pb.wte_fth_en, lambda x: (x & 0b10) == 0)
    water_level = raw_field(pb.water_value, WaterLevel.from_value)

    wte_fth_en = raw_field(pb.wte_fth_en)

    ambient_light = raw_field(pb.rgb_state, lambda x: x == 0x01)

    target_temperature = raw_field(pb.set_temp)
    power_mode = raw_field(pb.power_mode, PowerMode.from_value)

    # power_src looks like a bitmask, observations:
    # bit 0 - battery
    # bits 1-2 - optional internal power sources?
    # Bits 3, 5–7 - unused
    # bit 4 - AC mains
    # power_src = raw_field(pb.power_src)

    @classmethod
    def check(cls, sn):
        return sn.startswith(cls.SN_PREFIX)

    async def packet_parse(self, data: bytes) -> Packet:
        # Wave 2 uses V2 protocol with XOR encoding based on sequence number
        return Packet.fromBytes(data, is_xor=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        if packet.src == 0x42 and packet.cmdSet == 0x42 and packet.cmdId == 0x50:
            self.update_from_bytes(KT210SAC, packet.payload)
            processed = True
        # elif packet.src == 0x06 and packet.cmdSet == 0x20 and packet.cmdId == 0x32:
        #     processed = False

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed

    async def _send_config_packet(self, cmd_id: int, payload: bytes):
        packet = Packet(
            src=0x21,
            dst=0x42,
            cmd_set=0x42,
            cmd_id=cmd_id,
            payload=payload,
            version=self.packet_version,
        )

        await self._conn.sendPacket(packet)

    async def enable_ambient_light(self, enabled: bool):
        await self._send_config_packet(0x5C, (0x01 if enabled else 0x02).to_bytes())

    async def enable_automatic_drain(self, enabled: bool):
        drain_mode = (
            self.drain_mode if self.drain_mode is not None else DrainMode.EXTERNAL
        )
        if self.main_mode != MainMode.COLD:
            payload = 0x01
        else:
            payload = (0 if enabled else 0b10) | drain_mode.value

        await self._send_config_packet(0x59, payload.to_bytes())

    async def set_drain_mode(self, mode: DrainMode):
        if self.main_mode != MainMode.COLD:
            payload = 0x01
        else:
            payload = (0 if self.automatic_drain else 0b10) | mode.value

        await self._send_config_packet(0x59, payload.to_bytes())

    async def set_fan_speed(self, fan_gear: FanGear):
        await self._send_config_packet(0x5E, fan_gear.to_bytes())

    async def set_main_mode(self, mode: MainMode):
        await self._send_config_packet(0x51, mode.to_bytes())

    async def set_power_mode(self, mode: PowerMode):
        await self._send_config_packet(0x5B, mode.to_bytes())

    async def set_temperature(self, temperature: int):
        await self._send_config_packet(0x58, temperature.to_bytes())
        return True

    async def set_sub_mode(self, sub_mode: SubMode):
        await self._send_config_packet(0x52, sub_mode.to_bytes())
