import math
import struct


def _has_entries(msg, minimum: int = 15) -> list | None:
    if msg is None or len(msg.resv_info) < minimum:
        return None
    return msg.resv_info


def resv_soc(resv_info_msg) -> float | None:
    if (entries := _has_entries(resv_info_msg)) is None:
        return None
    soc = _uint32_as_float(entries[0])
    return round(max(0.0, min(100.0, soc)), 2)


def resv_temperature(resv_info_msg) -> int | None:
    if (entries := _has_entries(resv_info_msg)) is None:
        return None
    b0 = entries[13] & 0xFF
    b1 = (entries[13] >> 8) & 0xFF
    return b1 if b1 >= 25 else b0


def resv_is_charging(resv_info_msg) -> bool | None:
    if (entries := _has_entries(resv_info_msg)) is None:
        return None
    return (entries[14] & 0xFF) == 2


def resv_output_power(resv_info_msg) -> float | None:
    if (entries := _has_entries(resv_info_msg, minimum=16)) is None:
        return None
    return _uint32_as_float(entries[15])


def _uint32_as_float(value: int) -> float:
    data = (value & 0xFFFFFFFF).to_bytes(4, "little")
    result = struct.unpack("<f", data)[0]
    return result if math.isfinite(result) else 0.0
