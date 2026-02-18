from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from . import delta3


class Device(delta3.Device):
    """Delta 3 Ultra"""

    SN_PREFIX = (b"D751",)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self.max_ac_charging_power = 1800
