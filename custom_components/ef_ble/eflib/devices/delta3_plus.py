from ..props import Field, pb_field
from . import delta3_common
from .delta3_common import DCPortState, pb


class Device(delta3_common.Device):
    """Delta 3 Plus"""

    SN_PREFIX = (b"P351",)

    dc_port_1_input_power = pb_field(pb.pow_get_pv)
    dc_port_2_input_power = pb_field(pb.pow_get_pv2)

    dc_port_1_state = pb_field(
        pb.plug_in_info_pv_type, lambda v: DCPortState(v).state_name
    )
    dc_port_2_state = pb_field(
        pb.plug_in_info_pv2_type, lambda v: DCPortState(v).state_name
    )

    solar_input_power_1 = Field[float]()
    solar_input_power_2 = Field[float]()

    def _after_message_parsed(self):
        self.solar_input_power_1 = (
            round(self.dc_port_1_input_power, 2)
            if (
                self.dc_port_1_state == DCPortState.SOLAR.state_name
                and self.dc_port_1_input_power is not None
            )
            else 0
        )

        self.solar_input_power_2 = (
            round(self.dc_port_2_input_power, 2)
            if (
                self.dc_port_2_state == DCPortState.SOLAR.state_name
                and self.dc_port_2_input_power is not None
            )
            else 0
        )
