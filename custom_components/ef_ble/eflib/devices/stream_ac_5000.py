from ..devicebase import DeviceBase
from ..packet import Packet
from ..pb import es22_sys_pb2
from ..props import ProtobufProps, computed_field, pb_field, proto_attr_mapper
from ..props.protobuf_field import TransformIfMissing
from ..props.transforms import out_power

pb = proto_attr_mapper(es22_sys_pb2.DisplayPropertyUpload)


class Device(DeviceBase, ProtobufProps):
    """STREAM AC 5000"""

    SN_PREFIX = (b"ES22",)
    NAME_PREFIX = "EF-6"

    battery_level = pb_field(pb.system.info.bp_soc)
    battery_power = pb_field(
        pb.power.info.bp_pwr,
        TransformIfMissing[float, float](
            lambda v: out_power(v) if v is not None else 0.0
        ),
    )
    ac_input_power = pb_field(
        pb.ac.ac_in_pwr,
        TransformIfMissing[int, int](lambda v: v if v is not None else 0),
    )
    _ac_out_pwr = pb_field(pb.power.info.ac_out_pwr)
    _ac_out_pwr_fallback = pb_field(
        pb.ac.ac_out_pwr,
        TransformIfMissing[int, int](lambda v: v if v is not None else 0),
    )

    _bp_temp1 = pb_field(pb.battery.info.bp_temp1)
    _bp_temp2 = pb_field(pb.battery.info.bp_temp2)
    _bp_temp3 = pb_field(pb.battery.info.bp_temp3)
    _bp_temp4 = pb_field(pb.battery.info.bp_temp4)

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    @computed_field
    def ac_output_power(self) -> float | None:
        """
        Power drawn from the AC output port

        `PowerInfo.ac_out_pwr` is the figure the app shows and is reported on every
        message that carries the block, so it is preferred. Firmware that does not send
        it leaves only `AcInfo.ac_out_pwr`, which is coarser and arrives intermittently
        """
        if self._ac_out_pwr is not None:
            return round(self._ac_out_pwr, 2)
        return self._ac_out_pwr_fallback

    @computed_field
    def cell_temperature(self) -> int | None:
        temperatures = [
            temperature
            for temperature in (
                self._bp_temp1,
                self._bp_temp2,
                self._bp_temp3,
                self._bp_temp4,
            )
            if temperature is not None
        ]
        return max(temperatures) if temperatures else None

    async def packet_parse(self, data: bytes) -> Packet:
        return Packet.from_bytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        if packet.src == 0x02 and packet.cmd_set == 0xFE and packet.cmd_id == 0x27:
            self.update_from_bytes(es22_sys_pb2.DisplayPropertyUpload, packet.payload)
            processed = True

        self._notify_updated()

        return processed
