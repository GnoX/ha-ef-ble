import asyncio
import logging
import struct
import time
from dataclasses import dataclass
from typing import Any, Callable

from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import pr705_pb2
from ..pb import utc_sys_pb2_v4 as utc_sys_pb2

_LOGGER = logging.getLogger(__name__)

@dataclass(kw_only=True)
class _DeviceField[T]:
    default: T | None = None
    def __set_name__(self, owner: type["Device"], name: str):
        self.public_name = name
        self.private_name = f"_{name}"

    def __set__(self, instance: "Device", value: Any):
        if value == getattr(instance, self.public_name):
            return

        setattr(instance, self.private_name, value)
        instance.updated = True

    def __get__(self, instance, owner) -> T | None:
        return getattr(instance, self.private_name, self.default)

@dataclass
class _ProtobufField[T](_DeviceField[T]):
    pb_field_name: str
    transform_value: Callable[[T], T] | None = lambda x: x

    def __set_name__(self, owner: type["Device"], name: str):
        super().__set_name__(owner, name)
        owner._pb_field_names.append(self.public_name)

    def __set__(self, instance: "Device", value: Any):
        if not isinstance(value, pr705_pb2.DisplayPropertyUpload):
            raise ValueError("Can only set value from protobuf message")


        if not value.HasField(self.pb_field_name):
            return

        value = self.transform_value(getattr(value, self.pb_field_name))
        super().__set__(instance, value)

@dataclass
class _StatField[T](_DeviceField[T]):
    stat_name: str

    def __set_name__(self, owner: type["Device"], name: str):
        super().__set_name__(owner, name)
        owner._stat_field_dict[self.stat_name] = name


def _out_power(x):
    return -round(x, 2)

class Device(DeviceBase):
    """River 3"""

    SN_PREFIX = b"R6"
    NAME_PREFIX = "EF-R3"

    battery_level = _ProtobufField[int]("bms_batt_soc")

    ac_input_power = _ProtobufField[float]("pow_get_ac_in")
    ac_input_energy = _StatField[int]("STATISTICS_OBJECT_AC_IN_ENERGY")

    ac_output_power = _ProtobufField[float]("pow_get_ac_out", _out_power)
    ac_output_energy = _StatField[int]("STATISTICS_OBJECT_AC_OUT_ENERGY")

    input_power = _ProtobufField[int]("pow_in_sum_w")
    input_energy = _DeviceField[int]()

    output_power = _ProtobufField[int]("pow_out_sum_w")
    output_energy = _DeviceField[int]()

    dc_input_power = _ProtobufField[float]("pow_get_pv")
    dc_input_energy = _StatField[int]("STATISTICS_OBJECT_PV_IN_ENERGY")

    dc12v_output_power = _ProtobufField[float]("pow_get_12v")
    dc12v_output_energy = _StatField[int]("STATISTICS_OBJECT_DC12V_OUT_ENERGY")

    usbc_output_power = _ProtobufField[float]("pow_get_typec1", _out_power)
    usbc_output_energy = _StatField[int](
        "STATISTICS_OBJECT_TYPEC_OUT_ENERGY", default=0
    )

    usba_output_power = _ProtobufField[float]("pow_get_qcusb1", _out_power)
    usba_output_energy = _StatField[int](
        "STATISTICS_OBJECT_USBA_OUT_ENERGY", default=0
    )

    _pb_field_names: list[str] = []
    _stat_field_dict: dict[str, str] = {}

    @staticmethod
    def check(sn):
        return sn.startswith(Device.SN_PREFIX)

    async def packet_parse(self, data: bytes) -> Packet:
        return Packet.fromBytes(data, is_xor=True)

    async def data_parse(self, packet: Packet):
        processed = False
        self.updated = False

        if packet.src == 0x02 and packet.cmdSet == 0xFE and packet.cmdId == 0x15:
            p = pr705_pb2.DisplayPropertyUpload()
            p.ParseFromString(packet.payload)

            for prop in self._pb_field_names:
                setattr(self, prop, p)

            if p.HasField("display_statistics_sum"):
                stat_enum = pr705_pb2.STATISTICS_OBJECT
                for stat in p.display_statistics_sum.list_info:
                    field_name = self._stat_field_dict.get(
                        stat_enum.Name(stat.statistics_object),
                        None,
                    )
                    if not field_name:
                        continue
                    setattr(self, field_name, stat.statistics_content)

            processed = True
        elif (
            packet.src == 0x35
            and packet.cmdSet == 0x01
            and packet.cmdId == Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME
        ):
            # Device requested for time and timezone offset, so responding with that
            # otherwise it will not be able to send us predictions and config data
            if len(packet.payload) == 0:
                asyncio.create_task(self.sendUtcTime())
                asyncio.create_task(self.sendRTCRespond())
                asyncio.create_task(self.sendRTCCheck())
            processed = True

        if self.ac_input_energy is not None and self.dc_input_energy is not None:
            self.input_energy = self.ac_input_energy + self.dc_input_energy
        
        if (
            self.ac_output_energy is not None
            and self.usba_output_energy is not None
            and self.usbc_output_energy is not None
            and self.dc12v_output_energy is not None
        ):
            self.output_energy = (
                self.ac_output_energy
                + self.usba_output_energy
                + self.usbc_output_energy
                + self.dc12v_output_energy
            )
       

        if self.updated:
            for callback in self._callbacks:
                callback()
        return processed


    async def sendUtcTime(self):
        """Sends UTC time as unix timestamp seconds through PB"""
        _LOGGER.debug("%s: sendUtcTime", self._address)

        utcs = utc_sys_pb2.SysUTCSync()
        utcs.sys_utc_time = int(time.time())
        payload = utcs.SerializeToString()
        packet = Packet(0x21, 0x0B, 0x01, 0x55, payload, 0x01, 0x01, 0x13)

        await self._conn.sendPacket(packet)

    async def sendRTCRespond(self):
        """Sends RTC timestamp seconds and TZ as respond to device's request"""
        _LOGGER.debug("%s: sendRTCRespond", self._address)

        # Building payload
        tz_offset = (
            (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone)
            / 60
            / 60
            * -1
        )
        tz_maj = int(tz_offset)
        tz_min = int((tz_offset - tz_maj) * 100)
        time_sec = int(time.time())
        payload = (
            struct.pack("<L", time_sec)
            + struct.pack("<b", tz_maj)
            + struct.pack("<b", tz_min)
        )

        # Forming packet
        packet = Packet(
            0x21,
            0x35,
            0x01,
            Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME,
            payload,
            0x01,
            0x01,
            0x03,
        )

        await self._conn.sendPacket(packet)

    async def sendRTCCheck(self):
        """Sends command to check RTC of the device"""
        _LOGGER.debug("%s: sendRTCCheck", self._address)

        # Building payload
        tz_offset = (
            (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone)
            / 60
            / 60
            * -1
        )
        tz_maj = int(tz_offset)
        tz_min = int((tz_offset - tz_maj) * 100)
        time_sec = int(time.time())
        payload = (
            struct.pack("<L", time_sec)
            + struct.pack("<b", tz_maj)
            + struct.pack("<b", tz_min)
        )

        # Forming packet
        packet = Packet(
            0x21,
            0x35,
            0x01,
            Packet.NET_BLE_COMMAND_CMD_CHECK_RET_TIME,
            payload,
            0x01,
            0x01,
            0x03,
        )

        await self._conn.sendPacket(packet)

