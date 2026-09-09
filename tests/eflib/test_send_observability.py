import asyncio

import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib.connection import Connection, ConnectionState
from custom_components.ef_ble.eflib.packet import Packet


@pytest.fixture
def connection(mocker: MockerFixture) -> Connection:
    ble = mocker.Mock()
    ble.address = "AA:BB:CC:DD:EE:FF"
    conn = Connection(
        ble,
        "HR51XXXXXXXXX001",
        "user-id",
        data_parse=mocker.AsyncMock(),
        packet_parse=mocker.AsyncMock(),
        encrypt_type=0,
    )
    conn._client = mocker.Mock()
    conn._client.is_connected = True
    conn._client.write_gatt_char = mocker.AsyncMock()
    conn._get_characteristics = mocker.Mock(return_value=mocker.Mock())
    conn._state = ConnectionState.AUTHENTICATED
    return conn


def _packet() -> Packet:
    return Packet(
        src=0x21,
        dst=0x60,
        cmd_set=0x60,
        cmd_id=0x61,
        payload=bytes([0x08, 0x01]),
        dsrc=0x01,
        ddst=0x01,
        version=0x13,
    )


async def test_send_without_response_is_published_to_listeners(connection):
    """
    A send that bypasses `send_request` must still reach `on_data_send`

    This connection's assembler writes without a response, so the send takes the
    direct `write_gatt_char` branch. That branch used to publish nothing, so a
    keepalive sent with `wait_for_response=False` was absent from both the log and the
    diagnostics dump, making a keepalive that never ran indistinguishable from one
    that did.
    """
    assert not connection._create_frame_assembler().write_with_response

    seen: list[bytes] = []
    connection.on_data_send(seen.append)

    await connection.send_packet(_packet(), wait_for_response=False)

    connection._client.write_gatt_char.assert_awaited_once()
    assert len(seen) == 1
    assert seen[0]


async def test_timer_task_survives_a_failing_send(connection, mocker):
    """One bad send must not end the timer for the rest of the session"""
    calls = 0

    async def flaky():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("write failed")

    logger = mocker.patch.object(connection._logger, "exception")
    connection.add_timer_task(flaky, interval=0.01)

    await asyncio.sleep(0.1)

    assert calls > 1, "timer stopped after the first failure"
    logger.assert_called()
