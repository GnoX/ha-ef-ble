import pytest

from custom_components.ef_ble.eflib.devices.river2_max import Device


@pytest.mark.parametrize("serial", [b"R611XXXXXXXXX001", b"R613XXXXXXXXX001"])
def test_river2_max_is_recognised_by_every_declared_prefix(serial: bytes):
    """`R613` was a `str` among `bytes`, so those units never matched and stayed unsupported"""
    assert Device.check(serial)


def test_all_declared_prefixes_are_bytes():
    """A `str` entry can never match, since `check` compares against a bytes serial"""
    assert all(isinstance(p, bytes) for p in Device.SN_PREFIX)
