import logging
from enum import IntEnum


class IntFieldValue(IntEnum):
    @classmethod
    def from_value(cls, value: int):
        try:
            return cls(value)
        except ValueError:
            logging.debug("Encountered invalid value %s for %s", value, cls.__name__)
            return getattr(cls, "UNKNOWN")

    @property
    def state_name(self):
        return self.name.lower()
