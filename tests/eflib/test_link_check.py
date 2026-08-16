import asyncio

import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib import connection as connection_module
from custom_components.ef_ble.eflib.connection import Connection, ConnectionState


@pytest.fixture
def conn(mocker: MockerFixture) -> Connection:
    ble = mocker.Mock()
    ble.address = "AA:BB:CC:DD:EE:FF"
    ble.name = "Test Device"
    conn = Connection(
        ble_dev=ble,
        dev_sn="HW51XXXXXXXX0001",
        user_id="112233445566",
        data_parse=mocker.AsyncMock(),
        packet_parse=mocker.AsyncMock(),
    )
    conn._connection_state = ConnectionState.AUTHENTICATED
    return conn


async def test_link_check_reports_a_disconnect_bleak_never_announced(
    conn: Connection, mocker: MockerFixture
):
    """A link that drops without `disconnected_callback` must still start recovery"""
    conn._client = mocker.Mock(is_connected=False)
    disconnected = mocker.patch.object(conn, "disconnected")

    conn._check_link()

    disconnected.assert_called_once()


async def test_link_check_reschedules_itself_while_the_link_is_up(
    conn: Connection, mocker: MockerFixture
):
    conn._client = mocker.Mock(is_connected=True)
    disconnected = mocker.patch.object(conn, "disconnected")

    conn._check_link()

    disconnected.assert_not_called()
    assert conn._link_check_handle is not None
    conn._cancel_link_check()


async def test_link_check_stops_once_the_client_is_gone(
    conn: Connection, mocker: MockerFixture
):
    conn._client = None
    disconnected = mocker.patch.object(conn, "disconnected")

    conn._check_link()

    disconnected.assert_not_called()
    assert conn._link_check_handle is None


async def test_link_check_runs_even_though_call_later_would_skip_it(
    conn: Connection, mocker: MockerFixture
):
    """
    The check cannot go through `call_later`

    That helper drops its callback when `is_connected` is false, which is exactly the
    state the check has to notice, so it has to own its timer
    """
    conn._client = mocker.Mock(is_connected=False)
    assert conn.is_connected is False

    skipped = mocker.Mock()
    conn.call_later(0, skipped, key="never_runs")
    await asyncio.sleep(0)

    disconnected = mocker.patch.object(conn, "disconnected")
    conn._check_link()

    skipped.assert_not_called()
    disconnected.assert_called_once()


async def test_link_check_interval_is_scheduled_without_a_running_link(
    conn: Connection, mocker: MockerFixture
):
    conn._client = mocker.Mock(is_connected=True)
    call_later = mocker.patch.object(
        asyncio.get_running_loop(),
        "call_later",
        wraps=asyncio.get_running_loop().call_later,
    )

    conn._schedule_link_check()

    assert call_later.call_args.args[0] == connection_module.LINK_CHECK_INTERVAL
    conn._cancel_link_check()
