import asyncio
import logging
import struct
import time

from ..devicebase import AdvertisementData, BLEDevice, DeviceBase
from ..packet import Packet
from ..pb import pd303_pb2, utc_sys_pb2

_LOGGER = logging.getLogger(__name__)


class Device(DeviceBase):
    """Smart Home Panel 2"""

    SN_PREFIX = b"HD31"
    NAME_PREFIX = "EF-HD3"

    NUM_OF_CIRCUITS = 12
    NUM_OF_CHANNELS = 3

    @staticmethod
    def check(sn):
        return sn.startswith(Device.SN_PREFIX)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)

        self._data_circuit_power = [None] * Device.NUM_OF_CIRCUITS
        self._data_circuit_current = [None] * Device.NUM_OF_CIRCUITS

        self._data_grid_power = None
        self._data_in_use_power = None

        self._data_channel_power = [None] * Device.NUM_OF_CHANNELS

        self._data_error_count = 0
        self._data_battery_level = None

    @property
    def battery_level(self) -> int | None:
        """Battery level as a percentage."""
        return self._data_battery_level

    @battery_level.setter
    def battery_level(self, value: int) -> None:
        """Sets Battery level as a percentage and calls callbacks."""
        if self._data_battery_level != value:
            self._data_battery_level = value
            self.update_callback("battery_level")

    @property
    def channel_power(self) -> list[int | None]:
        """Backup channels wattage in W."""
        return self._data_channel_power

    @property
    def circuit_power(self) -> list[int | None]:
        """Circuit consuming wattage in W."""
        return self._data_circuit_power

    @property
    def circuit_current(self) -> list[float | None]:
        """Circuit consuming amperage in A."""
        return self._data_circuit_current

    @property
    def grid_power(self) -> int | None:
        """Grid intake wattage in W."""
        return self._data_grid_power

    @property
    def in_use_power(self) -> int | None:
        """In use wattage in W."""
        return self._data_in_use_power

    @property
    def error_happened(self) -> bool:
        """Will return true if error happened during the last update."""
        return self._data_error_count > 0

    async def data_parse(self, packet: Packet) -> bool:
        """Processing the incoming notifications from the device"""
        processed = False
        updated_fields = []
        if packet.src == 0x0B and packet.cmdSet == 0x0C:
            if (
                packet.cmdId == 0x01
            ):  # master_info, load_info, backup_info, watt_info, master_ver_info
                await self._conn.replyPacket(packet)

                p = pd303_pb2.ProtoTime()
                p.ParseFromString(packet.payload)
                _LOGGER.debug(
                    "%s: %s: Parsed data: %r", self.address, self.name, packet
                )

                if p.HasField("load_info"):
                    for i, w in enumerate(p.load_info.hall1_watt):
                        if self._data_circuit_power[i] != w:
                            self._data_circuit_power[i] = w
                            updated_fields.append(f"circuit_power_{i}")
                    for i, a in enumerate(p.load_info.hall1_curr):
                        if self._data_circuit_current[i] != a:
                            self._data_circuit_current[i] = a
                            updated_fields.append(f"circuit_current_{i}")

                if p.HasField("watt_info"):
                    wi = p.watt_info
                    if wi.HasField("grid_watt"):
                        if self._data_grid_power != wi.grid_watt:
                            self._data_grid_power = wi.grid_watt
                            updated_fields.append("grid_power")
                    elif self._data_grid_power != 0:
                        self._data_grid_power = 0
                        updated_fields.append("grid_power")

                    for i, w in enumerate(wi.ch_watt):
                        if self._data_channel_power[i] != w:
                            self._data_channel_power[i] = w
                            updated_fields.append(f"channel_power_{i}")

                    if wi.HasField("all_hall_watt"):
                        if self._data_in_use_power != wi.all_hall_watt:
                            self._data_in_use_power = wi.all_hall_watt
                            updated_fields.append("in_use_power")

                processed = True

            elif packet.cmdId == 0x20:  # backup_incre_info
                await self._conn.replyPacket(packet)

                p = pd303_pb2.ProtoPushAndSet()
                p.ParseFromString(packet.payload)
                _LOGGER.debug(
                    "%s: %s: Parsed data: %r", self.address, self.name, packet
                )

                if p.HasField("backup_incre_info"):
                    info = p.backup_incre_info
                    if info.HasField("errcode"):
                        errors = []
                        for e in info.errcode.err_code:
                            if e != b"\x00\x00\x00\x00\x00\x00\x00\x00":
                                errors.append(e)
                        if self._data_error_count != len(errors):
                            if len(errors) > self._data_error_count:
                                _LOGGER.warning(
                                    "%s: %s: Error happened on device: %s",
                                    self.address,
                                    self.name,
                                    errors,
                                )
                            self._data_error_count = len(errors)

                    if info.HasField("backup_bat_per"):
                        self.battery_level = info.backup_bat_per

                    # TODO: Energy2_info.pv_height_charge_watts
                    # TODO: Energy2_info.pv_low_charge_watts

                processed = True

            elif packet.cmdId == 0x21:  # is_get_cfg_flag
                p = pd303_pb2.ProtoPushAndSet()
                p.ParseFromString(packet.payload)
                _LOGGER.debug(
                    "%s: %s: Parsed data: %r", self.address, self.name, packet
                )
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

        elif packet.src == 0x0B and packet.cmdSet == 0x01 and packet.cmdId == 0x55:
            # Device reply that it's online and ready
            asyncio.create_task(self.setConfigFlag(True))
            processed = True

        for prop_name in updated_fields:
            self.update_callback(prop_name)

        return processed

    async def setConfigFlag(self, enable):
        """Sends command to enable/disable sending config data from device to the host"""
        _LOGGER.debug("%s: setConfigFlag: %s", self._address, enable)

        ppas = pd303_pb2.ProtoPushAndSet()
        ppas.is_get_cfg_flag = enable
        payload = ppas.SerializeToString()
        packet = Packet(0x21, 0x0B, 0x0C, 0x21, payload, 0x01, 0x01, 0x13)

        await self._conn.sendPacket(packet)

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

    async def setCircuitPower(self, circuit_id, enable):
        """Sends command to power on / off the specific circuit of the panel"""
        _LOGGER.debug(
            "%s: setCircuitPower for %d: %s", self._address, circuit_id, enable
        )

        ppas = pd303_pb2.ProtoPushAndSet()
        sta = getattr(
            ppas.load_incre_info.hall1_incre_info, "ch" + str(circuit_id + 1) + "_sta"
        )
        sta.load_sta = (
            pd303_pb2.LOAD_CH_STA.LOAD_CH_POWER_ON
            if enable
            else pd303_pb2.LOAD_CH_STA.LOAD_CH_POWER_OFF
        )
        sta.ctrl_mode = pd303_pb2.CTRL_MODE.RLY_HAND_CTRL_MODE
        payload = ppas.SerializeToString()
        packet = Packet(0x21, 0x0B, 0x0C, 0x21, payload, 0x01, 0x01, 0x13)

        await self._conn.sendPacket(packet)
