import logging
from enum import IntEnum

_LOGGER = logging.getLogger(__name__)


class IntFieldValue(IntEnum):
    @classmethod
    def from_value(cls, value: int):
        try:
            return cls(value)
        except ValueError:
            _LOGGER.debug("Encountered invalid value %s for %s", value, cls.__name__)
            return cls.UNKNOWN

    @classmethod
    def str_from_value(cls, value: int):
        return cls.from_value(value).state_name

    @property
    def state_name(self):
        return self.name.lower()

    @classmethod
    def options(cls, include_unknown: bool = True):
        return [
            opt.name.lower()
            for opt in cls
            if opt is not getattr(cls, "UNKNOWN", None) or include_unknown
        ]
