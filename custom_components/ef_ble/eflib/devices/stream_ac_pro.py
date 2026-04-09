from ..entity import controls
from ..pb import bk_series_pb2
from ..props import ProtobufProps, pb_field
from . import stream_ac

pb = stream_ac.pb


class Device(stream_ac.Device, ProtobufProps):
    """STREAM AC PRO"""

    SN_PREFIX = (b"BK31",)

    ac_power_1 = pb_field(pb.pow_get_schuko1)
    ac_power_2 = pb_field(pb.pow_get_schuko2)

    ac_1 = pb_field(pb.relay2_onoff)
    ac_2 = pb_field(pb.relay3_onoff)

    @controls.outlet(ac_1)
    async def enable_ac_1(self, enable: bool):  # pyright: ignore[reportIncompatibleMethodOverride]
        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_relay2_onoff=enable)
        )

    @controls.outlet(ac_2)
    async def enable_ac_2(self, enable: bool):  # pyright: ignore[reportIncompatibleMethodOverride]
        await self._send_config_packet(
            bk_series_pb2.ConfigWrite(cfg_relay3_onoff=enable)
        )
