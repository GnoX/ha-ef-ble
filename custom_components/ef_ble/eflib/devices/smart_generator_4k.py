from ..props import ProtobufProps, pb_field
from ..props.enums import IntFieldValue
from . import smart_generator

pb = smart_generator.pb


class XT150ChargeType(IntFieldValue):
    UNKNOWN = -1

    NONE = 0
    CHARGE_OUT = 1
    CHARGE = 2
    OUT = 3


class Device(smart_generator.Device, ProtobufProps):
    """Smart Generator 4000 (Dual Fuel)"""

    SN_PREFIX = (b"G351",)

    xt150_battery_level = pb_field(pb.cms_batt_soc)
    xt150_charge_type = pb_field(pb.plug_in_info_dcp_dsg_chg_type)

    output_power = pb_field(pb.pow_out_sum_w)

    # dc_out_max = pb_field(pb.generator_dc_out_pow_max)

    # async def set_dc_output_power_max(self, dc_out_max: int):
    #     await self._send_config_packet(
    #         ge305_sys_pb2.ConfigWrite(cfg_generator_dc_out_pow_max=dc_out_max)
    #     )
