import itertools
from collections import defaultdict

from google.protobuf.message import Message

from .protobuf_field import ProtobufField
from .repeated_protobuf_field import ProtobufRepeatedField
from .updatable_props import UpdatableProps


class ProtobufProps(UpdatableProps):
    """
    Mixin for augmenting device classes with properties parsed from protobuf messages

    This mixin provides method `update_from_message` that should be called for each
    incoming protobuf message and updates every defined `ProtobufField`.

    Usage
    -----
    ```
    pb = proto_attr_mapper(<protobuf_class>)

    class Device(DeviceBase, ProtobufProps):
        proto_field = pb_field(pb.field_from_message)

        def data_parse(self, packet):
            message = <protobuf_class>()
            message.ParseFromString(packet.payload)
            self.update_from_message(message)

            # self.updated_fields now holds all updated fields
            for field_name in self.updated_fields:
                self.update_state(field_name, getattr(self, field_name))
    ```

    """

    _repeated_field_map: dict[str, list[ProtobufRepeatedField]] = defaultdict(list)

    @classmethod
    def add_repeated_field(  # noqa: D102 - internal method
        cls, repeated_field: ProtobufRepeatedField
    ):
        updated_field_map = cls._repeated_field_map.copy()
        updated_field_map[repeated_field.pb_field.name].append(repeated_field)
        cls._repeated_field_map = updated_field_map

    def reset_updated(self):  # noqa: D102 - inherited
        self._processed_fields = []
        return super().reset_updated()

    def update_from_message(self, message: Message):
        """
        Update defined fields values from provided message

        Parameters
        ----------
        message
            Protocol buffer message to update fields from
        """
        self.reset_updated()

        for field in self._fields:
            if isinstance(field, ProtobufRepeatedField):
                continue

            if isinstance(field, ProtobufField):
                setattr(self, field.public_name, message)

        for repeated_fields in self._repeated_field_map.values():
            field_list = repeated_fields[0].get_list(message)
            if field_list is None:
                continue

            for item, field in itertools.product(field_list, repeated_fields):
                setattr(self, field.public_name, item)
