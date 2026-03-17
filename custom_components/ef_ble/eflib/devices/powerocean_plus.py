from . import powerocean


class Device(powerocean.Device):
    """Power Ocean Plus"""

    # R372ZD Plus - 3 phase

    SN_PREFIX = (b"R37",)
    NAME_PREFIX = "EF-R37"


    def isPowerOceanPlus(self):
        return True
