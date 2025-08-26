from ..props import ProtobufProps, pb_field
from . import stream_ac, stream_pro

pb = stream_ac.pb


class Device(stream_pro.Device, ProtobufProps):
    """STREAM Ultra"""

    SN_PREFIX = (b"BK11", b"ES11")

    pv_power_4 = pb_field(pb.pow_get_pv4, lambda v: round(v, 2))
