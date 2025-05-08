import logging

from custom_components.ef_ble.eflib.props import (
    ProtobufProps,
    pb_field,
    proto_attr_mapper,
)

from ..commands import TimeCommands
from ..devicebase import AdvertisementData, BLEDevice, DeviceBase
from ..packet import Packet
from ..pb import yj751_sys_pb2

_LOGGER = logging.getLogger(__name__)

pb = proto_attr_mapper(yj751_sys_pb2.AppShowHeartbeatReport)


class Device(DeviceBase, ProtobufProps):
    """Delta Pro Ultra"""

    SN_PREFIX = b"Y711"
    NAME_PREFIX = "EF-YJ"

    battery_level = pb_field(pb.soc)

    hv_solar_power = pb_field(pb.in_hv_mppt_pwr, lambda x: round(x, 2))
    lv_solar_power = pb_field(pb.in_lv_mppt_pwr)

    input_power = pb_field(pb.watts_in_sum)
    output_power = pb_field(pb.watts_out_sum)

    @staticmethod
    def check(sn):
        return sn.startswith(Device.SN_PREFIX)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)

    async def packet_parse(self, data: bytes) -> Packet:
        # Need to override because packet payload is xor-encoded by the first seq byte
        return Packet.fromBytes(data, True)

    async def data_parse(self, packet: Packet) -> bool:
        """Process the incoming notifications from the device"""
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

                self.update_from_message(p, reset=True)

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
                self._time_commands.async_send_all()
            processed = True

        for prop_name in updated_props:
            self.update_callback(prop_name)

        return processed
