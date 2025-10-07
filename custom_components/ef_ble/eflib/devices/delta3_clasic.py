from . import delta3


class Device(delta3.Device):
    """Delta 3 Classic"""

    SN_PREFIX = (b"P321",)
    NAME_PREFIX = "EF-P3"
