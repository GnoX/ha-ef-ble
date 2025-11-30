import enum


class Unit(enum.Enum):
    pass


class Power(Unit):
    WATT = "W"


class Temperature(Unit):
    C = "C"
    F = "F"


class Current(Unit):
    AMPERE = "A"
