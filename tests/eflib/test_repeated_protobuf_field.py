import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices import devices
from custom_components.ef_ble.eflib.devices.delta3 import Device as Delta3
from custom_components.ef_ble.eflib.pb import pd335_sys_pb2
from custom_components.ef_ble.eflib.props.protobuf_props import ProtobufProps
from custom_components.ef_ble.eflib.props.repeated_protobuf_field import (
    ProtobufRepeatedField,
)

_PROTOBUF_DEVICES = [
    module
    for module in devices
    if isinstance(getattr(module, "Device", None), type)
    and issubclass(module.Device, ProtobufProps)
]


def _declared_repeated_fields(device_type: type[ProtobufProps]) -> set[str]:
    return {
        field.public_name
        for field in device_type._fields
        if isinstance(field, ProtobufRepeatedField)
    }


def _registered_repeated_fields(device_type: type[ProtobufProps]) -> set[str]:
    return {
        field.public_name
        for fields_by_name in device_type._repeated_field_map.values()
        for fields in fields_by_name.values()
        for field in fields
    }


@pytest.mark.parametrize(
    "module", _PROTOBUF_DEVICES, ids=lambda module: module.Device.__module__
)
def test_device_registers_only_the_repeated_fields_it_declares(module):
    device_type = module.Device
    assert _registered_repeated_fields(device_type) == _declared_repeated_fields(
        device_type
    )


def test_repeated_field_of_another_device_does_not_become_an_attribute(
    mocker: MockerFixture,
):
    """
    A repeated field declared on a sibling device must not be parsed here

    Devices sharing a base class also share the message type that keys the repeated
    field registry. When the registry leaks, the raw protobuf sequence is written
    straight onto the instance, which surfaces as a sensor holding an empty list.
    """
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    device = Delta3(ble_dev, mocker.MagicMock(), "P351TEST1234")

    message = pd335_sys_pb2.DisplayPropertyUpload()
    message.pow_get_ac_out_list.SetInParent()
    device.update_from_message(message)

    assert "ac_power_1_1" not in _registered_repeated_fields(Delta3)
    assert not hasattr(device, "ac_power_1_1")
    assert not hasattr(device, "ac_power_1")
