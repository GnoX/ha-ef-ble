import time
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, cast

from google.protobuf.message import Message

from ..props import ProtobufProps, proto_has_attr
from .protobuf_field import _ProtoAttr


@dataclass
class _FieldUpdateTracker:
    discriminator_field: _ProtoAttr | None = None
    last_updated: float = 0

    def needs_update(self, new_time: float, update_period: float):
        return new_time - self.last_updated > update_period

    def update(self, new_time: float):
        self.last_updated = new_time


@dataclass
class _MessageUpdateTracker:
    update_period: int = 0
    message_type: type[Message] | None = None
    field_trackers: list[_FieldUpdateTracker] = field(default_factory=list)

    def add_tracker(self, discriminator_field: _ProtoAttr | None = None):
        self.field_trackers.append(_FieldUpdateTracker(discriminator_field))

    def needs_update(self):
        if self.update_period == 0:
            return True

        now = time.time()
        return any(
            field_tracker.needs_update(now, self.update_period)
            for field_tracker in self.field_trackers
        )

    def update(self, msg: Message):
        now = time.time()

        for tracker in self.field_trackers:
            if proto_has_attr(msg, tracker.discriminator_field):
                tracker.update(now)

    def reset(self):
        for tracker in self.field_trackers:
            tracker.update(0)


class ThrottledProtobufProps(ProtobufProps):
    @classmethod
    def with_field_discriminators(cls, discriminators: list[Any]):
        class DiscriminatedThrottledProtobufProps(cls):
            @property
            def discriminator_fields(self):
                return discriminators

        return DiscriminatedThrottledProtobufProps

    @property
    def update_period(self) -> int:
        if not hasattr(self, "_update_period"):
            self._update_period = 0
        return self._update_period

    @property
    def discriminator_fields(self):
        if not hasattr(self, "_discriminator_fields"):
            self._discriminator_fields: list[Any] = []
        return self._discriminator_fields

    def with_update_period(self, period: int):
        self._update_period = period
        return self

    def update_throttled[T_MSG: Message](
        self,
        message_type: type[T_MSG],
        serialized_message: bytes,
    ):
        message_tracker = self._message_update_trackers[message_type]
        if not message_tracker.needs_update():
            return None

        msg = message_type()
        msg.ParseFromString(serialized_message)
        self.update_from_message(msg)

        message_tracker.update(msg)

        return msg

    def allow_next_update(self):
        for tracker in self._message_update_trackers.values():
            tracker.reset()

    @cached_property
    def _message_update_trackers(self):
        trackers: dict[type[Message], _MessageUpdateTracker] = defaultdict(
            lambda: _MessageUpdateTracker(self.update_period)
        )

        if self.update_period == 0 or not self.discriminator_fields:
            return trackers

        for disc_field in self.discriminator_fields:
            disc_field = cast(_ProtoAttr, disc_field)
            trackers.setdefault(
                disc_field.message_type,
                _MessageUpdateTracker(self.update_period, disc_field.message_type),
            ).add_tracker(disc_field)
        return trackers
