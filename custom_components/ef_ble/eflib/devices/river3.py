from collections.abc import Sequence
import logging
from typing import Any

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from google.protobuf.message import Message

from ..commands import TimeCommands
from ..device_properties import Field, ProtobufField, ProtobufListField, UpdatableProps
from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import pr705_pb2

_LOGGER = logging.getLogger(__name__)


class _StatField[T](ProtobufListField[T]):
    _stat_enum = pr705_pb2.STATISTICS_OBJECT  # type: ignore[attr-defined]

    @property
    def list_name(self):
        return "display_statistics_sum"

    def get_list(self, message: Any) -> Sequence[Message]:
        return message.list_info

    def should_update(self, message: Any) -> bool:
        return self._stat_enum.Name(message.statistics_object) == self.pb_field_name

    def get_item_value(self, message: Any) -> T | None:
        return message.statistics_content


def _out_power(x):
    return -round(x, 2) if x != 0 else 0


class Device(DeviceBase, UpdatableProps):
    """River 3"""

    SN_PREFIX = b"R6"
    NAME_PREFIX = "EF-R3"

    battery_level = ProtobufField[int]("bms_batt_soc")

    ac_input_power = ProtobufField[float]("pow_get_ac_in")
    ac_input_energy = _StatField[int]("STATISTICS_OBJECT_AC_IN_ENERGY")

    ac_output_power = ProtobufField[float]("pow_get_ac_out", _out_power)
    ac_output_energy = _StatField[int]("STATISTICS_OBJECT_AC_OUT_ENERGY")

    input_power = ProtobufField[int]("pow_in_sum_w")
    input_energy = Field[int]()

    output_power = ProtobufField[int]("pow_out_sum_w")
    output_energy = Field[int]()

    dc_input_power = ProtobufField[float]("pow_get_pv")
    dc_input_energy = _StatField[int]("STATISTICS_OBJECT_PV_IN_ENERGY")

    dc12v_output_power = ProtobufField[float]("pow_get_12v")
    dc12v_output_energy = _StatField[int]("STATISTICS_OBJECT_DC12V_OUT_ENERGY")

    usbc_output_power = ProtobufField[float]("pow_get_typec1", _out_power)
    usbc_output_energy = _StatField[int]("STATISTICS_OBJECT_TYPEC_OUT_ENERGY")

    usba_output_power = ProtobufField[float]("pow_get_qcusb1", _out_power)
    usba_output_energy = _StatField[int]("STATISTICS_OBJECT_USBA_OUT_ENERGY")

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)

    @staticmethod
    def check(sn):
        return sn.startswith(Device.SN_PREFIX)

    async def packet_parse(self, data: bytes) -> Packet:
        return Packet.fromBytes(data, is_xor=True)

    async def data_parse(self, packet: Packet):
        processed = False

        if packet.src == 0x02 and packet.cmdSet == 0xFE and packet.cmdId == 0x15:
            p = pr705_pb2.DisplayPropertyUpload()
            p.ParseFromString(packet.payload)
            _LOGGER.debug("%s: %s: Parsed data: %r", self.address, self.name, packet)
            self.update_fields(p)
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

        for field_name in self.updated_fields:
            self.update_callback(field_name)

        return processed
