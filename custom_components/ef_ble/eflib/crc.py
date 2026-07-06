"""
Table-based CRC8/CRC16 for the BLE receive path

Hand-rolled instead of relying on the `crc` package: that library re-derives its
lookup table via a bit-by-bit register on every `Calculator` construction and, even
when using its table-based register, still processes each byte through a Python-level
`Byte` wrapper object (plus an extra bit-reversal pass per byte for CRC16, since our
config uses reflected input). This runs once per candidate frame while scanning for a
BLE notification's frame boundary and once per packet parsed, so the per-byte overhead
adds up. The tables below are precomputed once at import time; encoding/decoding a byte
is then a single list lookup and XOR - no per-byte object wrapping.

crc8: width=8, poly=0x07, init=0x00, no reflection (matches `crc.Crc8.CCITT`)
crc16: width=16, poly=0x8005, init=0x0000, reflected in/out (matches CRC-16/ARC)
"""


def _build_crc8_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            crc = ((crc << 1) ^ 0x07) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
        table.append(crc)
    return table


def _build_crc16_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
        table.append(crc)
    return table


_CRC8_TABLE = _build_crc8_table()
_CRC16_TABLE = _build_crc16_table()


def crc8(data: bytes) -> int:
    crc = 0x00
    for b in data:
        crc = _CRC8_TABLE[crc ^ b]
    return crc


def crc16(data: bytes) -> int:
    crc = 0x0000
    for b in data:
        crc = _CRC16_TABLE[(crc ^ b) & 0xFF] ^ (crc >> 8)
    return crc
