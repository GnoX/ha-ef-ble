from ..pb import pr705_pb2
from ..props import pb_field
from ..props.enums import IntFieldValue
from . import river3


class LedMode(IntFieldValue):
    OFF = 0
    DIM = 1
    BRIGHT = 2
    SOS = 3


class Device(river3.Device):
    """River 3 Plus"""

    SN_PREFIX = (b"R631", b"R634", b"R635")

    battery_level_main = pb_field(river3.pb.bms_batt_soc)

    led_mode = pb_field(river3.pb.led_mode, LedMode.from_value)

    async def set_led_mode(self, state: LedMode):
        await self._send_config_packet(pr705_pb2.ConfigWrite(cfg_led_mode=state.value))

    @property
    def device(self):
        model = ""
        match self._sn[:4]:
            case "R634":
                model = "(270)"
            case "R635":
                model = "Wireless"
        return f"River 3 Plus {model}".strip()
