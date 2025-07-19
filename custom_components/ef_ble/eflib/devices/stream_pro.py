from ..props import ProtobufProps, pb_field
from . import stream_ac, stream_max

pb = stream_ac.pb


class Device(stream_max.Device, ProtobufProps):
    """STREAM Pro"""

    SN_PREFIX = (b"BK12",)

    ac_2 = pb_field(pb.relay3_onoff)
    ac_power_2 = pb_field(pb.pow_get_schuko2)

    pv_power_3 = pb_field(pb.pow_get_pv3)
