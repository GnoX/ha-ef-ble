from enum import IntEnum

from custom_components.ef_ble.eflib.devices import river3

from ..device_properties import ProtobufField
from ..pb import pr705_pb2


class LedState(IntEnum):
    OFF = 0
    DIM = 1
    BRIGHT = 2
    SOS = 3


class Device(river3.Device):
    """River 3 Plus"""

    SN_PREFIX = (b"R631", b"R634")

    led_state = ProtobufField("led_mode", lambda num: LedState(num))

    async def set_led_state(self, state: LedState):
        config = pr705_pb2.ConfigWrite()
        config.cfg_led_mode = state.value
        await self._send_config_packet(config)

    @property
    def device(self):
        return "River 3 Plus"
