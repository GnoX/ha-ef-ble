import asyncio
import logging
import struct
import time

from ..devicebase import AdvertisementData, BLEDevice, DeviceBase
from ..packet import Packet
from ..pb import utc_sys_pb2, yj751_sys_pb2

_LOGGER = logging.getLogger(__name__)


class Device(DeviceBase):
    """Delta Pro Ultra"""

    SN_PREFIX = b"Y711"
    NAME_PREFIX = "EF-YJ"

    @staticmethod
    def check(sn):
        return sn.startswith(Device.SN_PREFIX)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)

        # AppShowHeartbeatReport

        # in_hv_mppt_pwr: 62.3074646
        self._data_hv_solar_power = None
        # in_lv_mppt_pwr: 0
        self._data_lv_solar_power = None

        # watts_in_sum: 62
        self._data_input_power = None
        # watts_out_sum: 518
        self._data_output_power = None

        # soc: 62
        self._data_battery_level = None

    async def packet_parse(self, data: bytes) -> Packet:
        """Need to override because packet payload is xor-encoded by the first byte of seq"""
        return Packet.fromBytes(data, True)

    @property
    def hv_solar_power(self) -> float | None:
        """High Voltage solar MPPT input in watts."""
        return self._data_hv_solar_power

    @property
    def lv_solar_power(self) -> float | None:
        """Low Voltage solar MPPT input in watts."""
        return self._data_lv_solar_power

    @property
    def input_power(self) -> int | None:
        """Total inverter input in watts."""
        return self._data_input_power

    @property
    def output_power(self) -> int | None:
        """Total inverter output in watts."""
        return self._data_output_power

    @property
    def battery_level(self) -> int | None:
        """Battery level as a percentage."""
        return self._data_battery_level

    async def data_parse(self, packet: Packet) -> bool:
        """Processing the incoming notifications from the device"""
        processed = False
        updated_props: list[str] = []

        if packet.src == 0x02 and packet.cmdSet == 0x02:
            if packet.cmdId == 0x01:  # Ping
                await self._conn.replyPacket(packet)

                p = yj751_sys_pb2.AppShowHeartbeatReport()
                p.ParseFromString(packet.payload)
                _LOGGER.debug(
                    "%s: %s: Parsed data: %r", self.address, self.name, packet
                )

                if p.HasField("in_hv_mppt_pwr"):
                    if self._data_hv_solar_power != p.in_hv_mppt_pwr:
                        self._data_hv_solar_power = p.in_hv_mppt_pwr
                        updated_props.append("hv_solar_power")
                elif self._data_hv_solar_power != 0:
                    self._data_hv_solar_power = 0
                    updated_props.append("hv_solar_power")

                if p.HasField("in_lv_mppt_pwr"):
                    if self._data_lv_solar_power != p.in_lv_mppt_pwr:
                        self._data_lv_solar_power = p.in_lv_mppt_pwr
                        updated_props.append("lv_solar_power")
                elif self._data_lv_solar_power != 0:
                    self._data_lv_solar_power = 0
                    updated_props.append("lv_solar_power")

                if p.HasField("watts_in_sum"):
                    if self._data_input_power != p.watts_in_sum:
                        self._data_input_power = p.watts_in_sum
                        updated_props.append("input_power")

                if p.HasField("watts_out_sum"):
                    if self._data_output_power != p.watts_out_sum:
                        self._data_output_power = p.watts_out_sum
                        updated_props.append("output_power")

                if p.HasField("soc"):
                    if self._data_battery_level != p.soc:
                        self._data_battery_level = p.soc
                        updated_props.append("battery_level")

                processed = True

        elif packet.src == 0x35 and packet.cmdSet == 0x35 and packet.cmdId == 0x20:
            _LOGGER.debug("%s: %s: Ping received: %r", self.address, self.name, packet)
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

        for prop_name in updated_props:
            self.update_callback(prop_name)

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
