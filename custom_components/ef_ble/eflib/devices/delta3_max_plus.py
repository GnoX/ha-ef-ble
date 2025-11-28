from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from . import delta3_plus


class Device(delta3_plus.Device):
    """Delta 3 Max Plus"""

    SN_PREFIX = (b"D3M1",)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self.max_ac_charging_power = 2400
