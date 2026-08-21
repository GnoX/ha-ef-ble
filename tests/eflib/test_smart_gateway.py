import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.devices.shp3 import Device as Shp3Device
from custom_components.ef_ble.eflib.devices.smart_gateway import Device
from custom_components.ef_ble.eflib.packet import PacketV4

# Application payloads of real heartbeats from a 200 A Smart Gateway on firmware
# 7.0.1.95. Only the serial fragment at the start of each 22-byte routing header is
# replaced; everything after it is the `DisplayPropertyUpload` the unit actually sent.
_PAYLOADS = [
    bytes.fromhex(
        "485236354d41534b3021014003032efe156d0b012101d2312408021204080110021d"
        "0000704220062a0d5465736c61204368617267657230013a020861b23f00c84200ed"
        "4b00000000f54b00000000f84b64804cc801b84c01dd4c00000000e54c00000000f2"
        "4c00824d00924d00a24d15556e6974656420537461746573204f616b6c616e64b54d"
        "de152442c54dce7e94c2d84d00f04d00f84d00824e00ba4e0720065d00002042c24e"
        "0920065d000020427801ca4e0920065d000020427801b85a00f05a01f85a00805b00"
        "885b00905b00f05b06"
    ),
    bytes.fromhex(
        "485236354d41534b3021014003032efe157d0b012101da311508021204080110011d"
        "00007042200630013a020861e2310d08021d0000b44230013a020802ea310d08021d"
        "0000b44230013a020801f2310d08021d0000b44230013a020862fa310d08021d0000"
        "b44230013a02086382320b1d0000c84230013a0208078a320b1d0000c84230013a02"
        "0808e53bcfb7f242ed3bf4fdf242f53b60e5503dfd3b60e5503d853c00c082468d3c"
        "00c08246953c0000e03e9d3c0000103fa53c00009ec0ad3c0000a2c0b53cccccbc40"
        "bd3c6766c640ba3f0a0d4087ec421df6f4f93ec23f0a0db66eec421d70adfc3eca3f"
        "0a0d29d2eb421dd93ac83ed23f0a0dd3b8ec421d671d863eda3f0a0dcd3cec421d3d"
        "8c063fe23f0a0d52dfed421d150e9d3eea3f00"
    ),
    bytes.fromhex(
        "485236354d41534b3021014003032efe158a0b0121011000ad0300000000f20700a8"
        "08f0fcffffffffffffff01b20810416d65726963612f4e65775f596f726bb80800b5"
        "1000006042e010c702e81000f01064f81000d01101e81100f0119001c01300ca1800"
        "e81800e81c0af01c80c001981d00a01d00a81d009d2000000000a52000000000ad20"
        "00007643b52034b3ffc4c02001c82000d82000e02000f02000fa20009a21080a068a"
        "4080808004a82100b52100000000bd2100000000d02128e02132f821008022e80788"
        "22e807902200982200bd2500000000c52500000000cd2500000000d52500000000e0"
        "2500e82500f02500f82500d826029a2700aa2700fd2700000000f530000000008a3f"
        "00923f38081d1a10593731315a414241394831373033383920022d00004042308060"
        "38fd0240c4f8ffffffffffffff014869620683800484800470029a3f39081d1a1059"
        "3731315a414241394831373033393620022d00007c4230806038da0240caf5ffffff"
        "ffffffff01488d0162068580048680047002f23f00bd42d87dee42c54213d4ee42e0"
        "4f00c05a00e85c33f05c33d05d00c060f311c86000d860f311f0600ef86001c06100"
        "8065009a6900a06901"
    ),
    bytes.fromhex(
        "485236354d41534b3021014003032efe15970b012101c22d025553c82d00d02d0080"
        "2f01902f038d3000000000e030c0bb01ed3000000000fa3000c031c025c831f403b0"
        "3232ba3200c2320a08021a02000022020000ca3200d23200dd3200000000e5320000"
        "0000ed3200000000f03200fd32000000008033008d3300000000a83302f23700fa37"
        "008238008a38009238009a3800a03801d23d00ea3e0410015801f23e00fa3e00823f"
        "00a23f00c24c0a08021805200228023001ca4c0c080110011806200228013003d24c"
        "0c080110011807200228013003e04de05dea4d020801a84e01b05b00885c00a05d00"
        "d85d01e05d00e06000"
    ),
]


def _heartbeat(payload: bytes, src: int) -> PacketV4:
    return PacketV4(src=src, dst=0x5B, cmd_set=0x40, cmd_id=0x30, payload=payload)


def _make(mocker: MockerFixture, cls, sn: str):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    ble_dev.name = cls.NAME_PREFIX + sn[-4:]
    adv = mocker.Mock()
    adv.manufacturer_data = {cls.MANUFACTURER_KEY: bytes(30)}
    device = cls(ble_dev, adv, sn)
    device._conn = mocker.AsyncMock()
    return device


@pytest.fixture
def device(mocker: MockerFixture):
    return _make(mocker, Device, "HR65XXXXXXXXX037")


def test_gateway_is_recognised_by_its_serial_prefix():
    assert Device.check(b"HR65XXXXXXXXX037")
    assert not Shp3Device.check(b"HR65XXXXXXXXX037")
    assert not Device.check(b"HR62XXXXXXXXX037")


def test_gateway_reports_from_a_different_module_address_than_the_panel():
    assert Device.MAIN_SRC == 0x34
    assert Shp3Device.MAIN_SRC == 0x32


async def test_gateway_parses_its_own_heartbeats(device):
    for payload in _PAYLOADS:
        assert await device.data_parse(_heartbeat(payload, Device.MAIN_SRC)) is True

    # eight load channels, six of them wired on this unit
    assert device.circuit_is_enabled_1 is True
    assert device.circuit_is_enabled_7 is False
    assert device.circuit_power_1 == pytest.approx(0.0)
    assert device.circuit_voltage_1 == pytest.approx(118.3, abs=0.05)
    assert device.circuit_current_1 == pytest.approx(0.49, abs=0.01)
    assert device.circuit_status_1 == 2

    # split phase, so L1 and L2 only
    assert device.l1_voltage == pytest.approx(121.4, abs=0.05)
    assert device.l2_voltage == pytest.approx(121.5, abs=0.05)
    assert device.l3_voltage is None

    assert device.pv_power_sum == pytest.approx(246.0, abs=0.5)
    assert device.grid_is_energized is True
    assert device.operating_mode_select == 1
    assert device.storm_guard is False
    assert device.eps_mode is False


async def test_panel_ignores_a_heartbeat_from_the_gateway_address(mocker: MockerFixture):
    """To the panel, 0x34 is a sub device, so its telemetry must not be parsed"""
    panel = _make(mocker, Shp3Device, "HR62XXXXXXXXX037")

    for payload in _PAYLOADS:
        assert await panel.data_parse(_heartbeat(payload, Device.MAIN_SRC)) is True

    assert panel.l1_voltage is None
    assert panel.circuit_is_enabled_1 is None
