import logging

from ..devicebase import DeviceBase
from ..entity import controls
from ..packet import Packet
from ..pb import ac517_apl_comm_pb2
from ..props import ProtobufProps, pb_field
from ..props.enums import IntFieldValue
from ..props.protobuf_field import proto_attr_mapper
from ..props.transforms import pround

pb_disp = proto_attr_mapper(ac517_apl_comm_pb2.DisplayPropertyUpload)
pb_mode = proto_attr_mapper(ac517_apl_comm_pb2.WaveOperatingModeParamItem)

_LOGGER = logging.getLogger(__name__)


class OperatingMode(IntFieldValue):
    UNKNOWN = -1

    NULL = 0
    COOLING = 1
    HEATING = 2
    VENTING = 3
    DEHUMIDIFYING = 4
    THERMOSTATIC = 5


class TemperatureUnit(IntFieldValue):
    UNKNOWN = -1

    NONE = 0
    CELSIUS = 1
    FAHRENHEIT = 2

    @classmethod
    def from_mode(cls, mode: ac517_apl_comm_pb2.USER_TEMP_UNIT_TYPE):
        try:
            return cls(mode)
        except ValueError:
            _LOGGER.debug("Encountered invalid value %s for %s", mode, cls.__name__)
            return TemperatureUnit.UNKNOWN

    def as_pb_enum(self):
        return {
            TemperatureUnit.NONE: ac517_apl_comm_pb2.USER_TEMP_UNIT_NONE,
            TemperatureUnit.CELSIUS: ac517_apl_comm_pb2.USER_TEMP_UNIT_C,
            TemperatureUnit.FAHRENHEIT: ac517_apl_comm_pb2.USER_TEMP_UNIT_F,
        }[self]


class FanSpeed(IntFieldValue):
    UNKNOWN = -1

    LOW = 20
    MEDIUM_LOW = 40
    MEDIUM = 60
    MEDIUM_HIGH = 80
    HIGH = 100


class SubMode(IntFieldValue):
    UNKNOWN = -1

    MAX = 0
    SLEEP = 1
    ECO = 2
    MANUAL = 3


class TemperatureDisplayType(IntFieldValue):
    UNKNOWN = -1

    AMBIENT = 0
    SUPPLY_AIR = 1


class SleepState(IntFieldValue):
    UNKNOWN = -1

    ON = 0
    STANDBY = 1


class Device(DeviceBase, ProtobufProps):
    """Wave 3"""

    SN_PREFIX = (b"AC71",)
    NAME_PREFIX = "EF-AC"

    battery_level = pb_field(pb_disp.cms_batt_soc, pround(2))
    ambient_temperature = pb_field(pb_disp.temp_ambient, pround(2))
    ambient_humidity = pb_field(pb_disp.humi_ambient, pround(2))
    operating_mode = pb_field(pb_disp.wave_operating_mode, OperatingMode.from_value)
    condensate_water_level = pb_field(pb_disp.condensate_water_level)
    cell_temperature = pb_field(pb_disp.bms_max_cell_temp)

    pcs_fan_level = pb_field(pb_disp.pcs_fan_level)
    in_drainage = pb_field(pb_disp.in_drainage)
    drainage_mode = pb_field(pb_disp.drainage_mode)
    # lcd_show_temp_type = pb_field(
    #     pb_disp.lcd_show_temp_type, TemperatureDisplayType.from_value
    # )

    input_power = pb_field(pb_disp.pow_in_sum_w, pround(1))
    output_power = pb_field(pb_disp.pow_out_sum_w, pround(1))
    ac_input_power = pb_field(pb_disp.pow_get_ac, pround(1))
    battery_power = pb_field(pb_disp.pow_get_bms, pround(1))

    temp_indoor_supply_air = pb_field(pb_disp.temp_indoor_supply_air, pround(1))
    # temp_indoor_return_air = pb_field(pb_run.temp_indoor_return_air, pround(1))
    # temp_outdoor_ambient = pb_field(pb_run.temp_outdoor_ambient, pround(1))
    # temp_condenser = pb_field(pb_run.temp_condenser, pround(1))
    # temp_evaporator = pb_field(pb_run.temp_evaporator, pround(1))
    # temp_compressor_discharge = pb_field(pb_run.temp_compressor_discharge, pround(1))

    temp_unit = pb_field(pb_disp.user_temp_unit, TemperatureUnit.from_mode)

    en_pet_care = pb_field(pb_disp.en_pet_care)
    pet_care_warning = pb_field(pb_disp.pet_care_warning)

    battery_charge_limit_min = pb_field(pb_disp.cms_min_dsg_soc)
    battery_charge_limit_max = pb_field(pb_disp.cms_max_chg_soc)
    sleep_state = pb_field(pb_disp.dev_sleep_state, SleepState.from_value)
    power = pb_field(pb_disp.dev_sleep_state, lambda x: x == SleepState.ON)

    _wave_mode_info = pb_field(pb_disp.wave_mode_info)
    target_temperature_climate = pb_field(pb_mode.temp_set, pround(1))
    fan_speed_climate = pb_field(pb_mode.airflow_speed, FanSpeed.from_value)

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet):
        processed = False
        self.reset_updated()

        if packet.src == 0x42 and packet.cmdSet == 0xFE and packet.cmdId == 0x15:
            self.update_from_bytes(
                ac517_apl_comm_pb2.DisplayPropertyUpload, packet.payload
            )
            processed = True

        if packet.src == 0x42 and packet.cmdSet == 0xFE and packet.cmdId == 0x16:
            self.update_from_bytes(
                ac517_apl_comm_pb2.RuntimePropertyUpload, packet.payload
            )
            processed = True

        self.target_temperature_climate = self.fan_speed_climate = (
            self._current_mode_item
        )

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))
        return processed

    async def _send_config_packet(self, message: ac517_apl_comm_pb2.ConfigWrite):
        payload = message.SerializeToString()
        packet = Packet(0x20, 0x42, 0xFE, 0x11, payload, 0x01, 0x01, 0x13)
        await self._conn.sendPacket(packet)

    async def set_battery_charge_limit_min(self, limit: int):
        if (
            self.battery_charge_limit_max is not None
            and limit > self.battery_charge_limit_max
        ):
            return False

        await self._send_config_packet(
            ac517_apl_comm_pb2.ConfigWrite(cfg_min_dsg_soc=limit)
        )
        return True

    async def set_battery_charge_limit_max(self, limit: int):
        if (
            self.battery_charge_limit_min is not None
            and limit < self.battery_charge_limit_min
        ):
            return False

        await self._send_config_packet(
            ac517_apl_comm_pb2.ConfigWrite(cfg_max_chg_soc=limit)
        )
        return True

    _climate = controls.climate(
        operating_mode,
        hvac_modes={
            "cool": OperatingMode.COOLING,
            "heat": OperatingMode.HEATING,
            "fan_only": OperatingMode.VENTING,
            "dry": OperatingMode.DEHUMIDIFYING,
            "auto": OperatingMode.THERMOSTATIC,
        },
        fan_modes={
            "low": FanSpeed.LOW,
            "medium_low": FanSpeed.MEDIUM_LOW,
            "medium": FanSpeed.MEDIUM,
            "medium_high": FanSpeed.MEDIUM_HIGH,
            "high": FanSpeed.HIGH,
        },
        power_field=power,
        current_temperature_field=ambient_temperature,
        target_temperature_field=target_temperature_climate,
        fan_speed_field=fan_speed_climate,
        min_temp=16,
        max_temp=30,
    )

    @_climate.power
    async def enable_power(self, enabled: bool):
        cfg = ac517_apl_comm_pb2.ConfigWrite()
        if enabled:
            cfg.cfg_power_on = True
        else:
            cfg.cfg_power_off = True
        await self._send_config_packet(cfg)

    @_climate.mode
    async def set_operating_mode(self, mode: OperatingMode):
        await self._send_config_packet(
            ac517_apl_comm_pb2.ConfigWrite(cfg_wave_operating_mode=mode.value)
        )

    @_climate.target_temp
    async def set_target_temperature(self, temperature: float):
        await self._send_config_packet(
            ac517_apl_comm_pb2.ConfigWrite(cfg_temp_set=temperature)
        )
        self.notify_field(Device.target_temperature_climate, temperature)

    @_climate.fan
    async def set_fan_speed(self, speed: FanSpeed):
        await self._send_config_packet(
            ac517_apl_comm_pb2.ConfigWrite(cfg_airflow_speed=speed.value)
        )
        self.notify_field(Device.fan_speed_climate, speed)

    @controls.switch(en_pet_care)
    async def enable_en_pet_care(self, enabled: bool):
        await self._send_config_packet(
            ac517_apl_comm_pb2.ConfigWrite(cfg_en_pet_care=enabled)
        )

    async def _request_full_upload(self):
        await self._send_config_packet(
            ac517_apl_comm_pb2.ConfigWrite(
                active_display_property_full_upload=True,
                active_runtime_property_full_upload=True,
            )
        )

    @property
    def _current_mode_item(self):
        if (
            self._wave_mode_info is None
            or self.operating_mode is None
            or self.operating_mode == OperatingMode.NULL
        ):
            return None

        items = self._wave_mode_info.list_info
        if not items:
            return None

        # The list may contain 5 entries (modes 1-5) or 6 (modes 0-5 with NULL
        # placeholder at index 0)
        idx = self.operating_mode if len(items) > 5 else self.operating_mode - 1
        if 0 <= idx < len(items):
            return items[idx]

        self._logger.debug(
            "mode_index %d out of range (list length %d, mode %s)",
            idx,
            len(items),
            self.operating_mode,
        )
        return None
