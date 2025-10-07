from ..pb import ge305_sys_pb2
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

    def __init__(
        self,
        ble_dev: smart_generator.BLEDevice,
        adv_data: smart_generator.AdvertisementData,
        sn: str,
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self.dc_output_power_max = 3200
        self.dc_output_power_min = 1000

    xt150_battery_level = pb_field(pb.cms_batt_soc)
    xt150_charge_type = pb_field(pb.plug_in_info_dcp_dsg_chg_type)

    dc_output_power_limit = pb_field(pb.generator_dc_out_pow_max)

    async def set_dc_output_power_max(self, limit: int):
        if (
            self.dc_output_power_max is None
            or self.dc_output_power_min is None
            or limit < self.dc_output_power_min
            or limit > self.dc_output_power_max
        ):
            return False
        await self._send_config_packet(
            ge305_sys_pb2.ConfigWrite(cfg_generator_dc_out_pow_max=limit)
        )
        return True
