"""Utils for simple use of crc"""

from crc import Calculator, Configuration, Crc8

crc16_arc = Configuration(
    width=16,
    polynomial=0x8005,
    init_value=0x0000,
    final_xor_value=0x0000,
    reverse_input=True,
    reverse_output=True,
)


_crc8_calculator = Calculator(Crc8.CCITT, optimized=True)
_crc16_calculator = Calculator(crc16_arc, optimized=True)


def crc8(data: bytes):
    return _crc8_calculator.checksum(data)


def crc16(data: bytes):
    return _crc16_calculator.checksum(data)
