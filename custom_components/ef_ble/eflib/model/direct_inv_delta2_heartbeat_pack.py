from typing import Annotated

from .base import RawData


class DirectInvDelta2HeartbeatPack(RawData):
    err_code: Annotated[bytes, "4s", "errCode"]
    sys_ver: Annotated[bytes, "4s", "sysVer"]
    charger_type: Annotated[int, "B", "chargerType"]
    input_watts: Annotated[int, "H", "inputWatts"]
    output_watts: Annotated[int, "H", "outputWatts"]
