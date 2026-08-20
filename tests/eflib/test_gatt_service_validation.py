import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib import connection as conn_mod
from custom_components.ef_ble.eflib.connection import Connection, ConnectionState
from custom_components.ef_ble.eflib.exceptions import UnsupportedBluetoothProtocol

_RFCOMM = conn_mod._BT_PROTOCOL_UUIDS["rfcomm"]


class _FakeServices:
    def __init__(self, by_uuid: dict[str, object], characteristics: dict | None = None):
        self._by_uuid = by_uuid
        self.characteristics = characteristics or {}

    def get_characteristic(self, uuid: str):
        return self._by_uuid.get(uuid)


def _make_connection(mocker: MockerFixture) -> Connection:
    ble = mocker.Mock()
    ble.address = "AA:BB:CC:DD:EE:FF"
    ble.name = "Test Device"
    return Connection(
        ble_dev=ble,
        dev_sn="R331XXXXXXXX0001",
        user_id="112233445566",
        data_parse=mocker.AsyncMock(),
        packet_parse=mocker.AsyncMock(),
    )


def _char(mocker: MockerFixture, uuid: str, description: str, service_uuid: str):
    return mocker.Mock(
        uuid=uuid,
        description=description,
        properties=["read"],
        service_uuid=service_uuid,
    )


def _make_client(mocker: MockerFixture, services: _FakeServices):
    client = mocker.MagicMock()
    client.is_connected = True
    client.services = services
    client.disconnect = mocker.AsyncMock()
    client.clear_cache = mocker.AsyncMock()
    client.start_notify = mocker.AsyncMock()
    client.stop_notify = mocker.AsyncMock()
    return client


def _patch_connect(mocker: MockerFixture, client) -> None:
    mocker.patch.object(conn_mod, "close_stale_connections_by_address", autospec=True)
    mocker.patch.object(conn_mod, "establish_connection", return_value=client)


async def test_connect_clears_gatt_cache_when_service_table_is_empty(
    mocker: MockerFixture,
):
    conn = _make_connection(mocker)
    client = _make_client(mocker, _FakeServices({}))
    _patch_connect(mocker, client)

    await conn.connect()

    client.clear_cache.assert_awaited_once()
    assert isinstance(conn._last_exception, UnsupportedBluetoothProtocol)


_GAP = "00001800-0000-1000-8000-00805f9b34fb"
_GATT = "00001801-0000-1000-8000-00805f9b34fb"


async def test_connect_clears_gatt_cache_when_only_generic_services_resolve(
    mocker: MockerFixture,
):
    """A table of nothing but GAP and GATT is as broken as an empty one"""
    conn = _make_connection(mocker)
    characteristics = {
        1: _char(mocker, "00002a00-0000-1000-8000-00805f9b34fb", "Device Name", _GAP),
        2: _char(mocker, "00002a01-0000-1000-8000-00805f9b34fb", "Appearance", _GAP),
        3: _char(
            mocker, "00002a05-0000-1000-8000-00805f9b34fb", "Service Changed", _GATT
        ),
    }
    client = _make_client(mocker, _FakeServices({}, characteristics=characteristics))
    _patch_connect(mocker, client)

    await conn.connect()

    client.clear_cache.assert_awaited_once()
    assert isinstance(conn._last_exception, UnsupportedBluetoothProtocol)


async def test_connect_keeps_gatt_cache_when_device_exposes_a_real_service(
    mocker: MockerFixture,
):
    """A device advertising a service of its own is genuinely unsupported"""
    conn = _make_connection(mocker)
    characteristics = {
        1: _char(
            mocker,
            "0000fff1-0000-1000-8000-00805f9b34fb",
            "Vendor Data",
            "0000fff0-0000-1000-8000-00805f9b34fb",
        )
    }
    client = _make_client(mocker, _FakeServices({}, characteristics=characteristics))
    _patch_connect(mocker, client)

    await conn.connect()

    client.clear_cache.assert_not_awaited()
    assert isinstance(conn._last_exception, UnsupportedBluetoothProtocol)


async def test_connect_proceeds_to_auth_when_characteristics_resolve(
    mocker: MockerFixture,
):
    conn = _make_connection(mocker)
    notify_char, write_char = mocker.Mock(), mocker.Mock()
    client = _make_client(
        mocker,
        _FakeServices({_RFCOMM["notify"]: notify_char, _RFCOMM["write"]: write_char}),
    )
    _patch_connect(mocker, client)
    init_auth = mocker.patch.object(conn, "_init_ble_session_key", mocker.AsyncMock())

    await conn.connect()

    init_auth.assert_awaited_once()
    client.clear_cache.assert_not_awaited()
    assert conn._connection_state == ConnectionState.CONNECTED
    assert conn._notify_characteristic is notify_char
    assert conn._write_characteristic is write_char


async def test_missing_notify_characteristic_is_reported_as_notify(
    mocker: MockerFixture,
):
    conn = _make_connection(mocker)
    conn._client = _make_client(mocker, _FakeServices({}))

    with pytest.raises(UnsupportedBluetoothProtocol) as exc_info:
        conn._get_characteristics("notify")

    assert exc_info.value.characteristic_type == "notify"
    assert "unsupported protocol for notify" in str(exc_info.value)


async def test_characteristics_resolve_against_current_client_after_reconnect(
    mocker: MockerFixture,
):
    conn = _make_connection(mocker)
    old_char, new_char = mocker.Mock(), mocker.Mock()
    conn._client = _make_client(mocker, _FakeServices({_RFCOMM["notify"]: old_char}))
    assert conn._notify_characteristic is old_char

    conn.disconnected()
    conn._client = _make_client(mocker, _FakeServices({_RFCOMM["notify"]: new_char}))

    assert conn._notify_characteristic is new_char
