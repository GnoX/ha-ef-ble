from dataclasses import dataclass
from typing import Any, cast

from google.protobuf.message import Message

from .. import DeviceBase
from ..connection import PacketIterator
from ..props import ProtobufProps, proto_attr_name, proto_has_attr


@dataclass
class DeviceUpdater:
    device: DeviceBase

    @property
    def _device_props(self) -> ProtobufProps:
        return cast(ProtobufProps, self.device)

    def notify_state(self):
        for field_name in self._device_props.updated_fields:
            self.device.update_callback(field_name)
            self.device.update_state(field_name, getattr(self.device, field_name))
        self._device_props.reset_updated()

    def update_from_message(self, p: Message) -> bool:
        self._device_props.update_from_message(p)
        return True


@dataclass
class ThrottledBatchUpdater(DeviceUpdater):
    discriminator_fields: list[Any]

    def __post_init__(self):
        self._updated_this_cycle = []

    @property
    def _fully_updated(self):
        return (
            False
            if not self._updated_this_cycle
            else all(
                proto_attr_name(disc_field) in self._updated_this_cycle
                for disc_field in self.discriminator_fields
            )
        )

    def _skip_update_for_message(self, p):
        for disc_field in self.discriminator_fields:
            has_attr = proto_has_attr(p, disc_field)
            if not has_attr:
                continue

            attr_name = proto_attr_name(disc_field)
            if has_attr and attr_name not in self._updated_this_cycle:
                self._updated_this_cycle.append(attr_name)
                return False

            if attr_name in self._updated_this_cycle:
                return True

        return False

    def update_from_message(self, p: Message) -> bool:
        if self._skip_update_for_message(p):
            return False
        return super().update_from_message(p)

    async def parse_batch(self, packet_iterator: PacketIterator):
        async for packet in packet_iterator.reversed():
            if self._fully_updated:
                break

            packet.parsed = await self.device.data_parse(packet)
        self._updated_this_cycle.clear()
        self.notify_state()
