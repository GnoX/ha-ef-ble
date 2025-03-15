from ..props import Field, pb_field
from . import delta3_common
from .delta3_common import DCPortState, pb


class Device(delta3_common.Device):
    """Delta 3"""

    SN_PREFIX = (b"P231", b"D361")

    dc_input_power = pb_field(pb.pow_get_pv)
    dc_port_state = pb_field(
        pb.plug_in_info_pv_type, lambda v: DCPortState(v).state_name
    )

    solar_input_power = Field[float]()

    def _after_message_parsed(self):
        self.solar_input_power = (
            round(self.dc_input_power, 2)
            if (
                self.dc_port_state == DCPortState.SOLAR.state_name
                and self.dc_input_power is not None
            )
            else 0
        )
