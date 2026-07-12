import pytest
from pytest_mock import MockerFixture

from custom_components.ef_ble.eflib import controls
from custom_components.ef_ble.eflib.devices.wave2 import (
    Device,
    DrainMode,
    MainMode,
)


@pytest.fixture
def device(mocker: MockerFixture):
    ble_dev = mocker.Mock()
    ble_dev.address = "AA:BB:CC:DD:EE:FF"
    adv_data = mocker.MagicMock()
    device = Device(ble_dev, adv_data, "KT21TEST1234")
    device._conn = mocker.AsyncMock()
    return device


def _set_state(device: Device, main_mode: MainMode, wte_fth_en: int):
    device.main_mode = main_mode.value
    device.wte_fth_en = wte_fth_en


def _sent_drain_payload(device: Device) -> bytes:
    packet = device._conn.sendPacket.call_args.args[0]
    assert packet.cmd_id == 0x59
    return packet.payload


@pytest.mark.parametrize(
    ("main_mode", "wte_fth_en", "expected_auto", "expected_mode"),
    [
        (MainMode.COLD, 0, True, DrainMode.EXTERNAL),
        (MainMode.COLD, 1, True, DrainMode.DRAIN_FREE),
        (MainMode.COLD, 2, False, DrainMode.EXTERNAL),
        (MainMode.COLD, 3, False, DrainMode.DRAIN_FREE),
        (MainMode.WARM, 0, False, DrainMode.EXTERNAL),
        (MainMode.WARM, 1, True, DrainMode.EXTERNAL),
        (MainMode.WARM, 3, False, DrainMode.EXTERNAL),
        (MainMode.FAN, 0, False, DrainMode.EXTERNAL),
        (MainMode.FAN, 1, True, DrainMode.EXTERNAL),
    ],
)
def test_drain_state_is_decoded_per_main_mode(
    device, main_mode, wte_fth_en, expected_auto, expected_mode
):
    _set_state(device, main_mode, wte_fth_en)

    assert device.automatic_drain is expected_auto
    assert device.drain_mode is expected_mode


def test_drain_state_is_unknown_before_first_heartbeat(device):
    assert device.automatic_drain is None
    assert device.drain_mode is None


@pytest.mark.parametrize(
    ("main_mode", "wte_fth_en", "enabled", "expected_payload"),
    [
        (MainMode.COLD, 2, True, 0),
        (MainMode.COLD, 3, True, 1),
        (MainMode.COLD, 0, False, 2),
        (MainMode.COLD, 1, False, 3),
        # drain-free is unsupported in Heat/Fan; enabling always sends 1
        (MainMode.WARM, 2, True, 1),
        (MainMode.FAN, 2, True, 1),
        (MainMode.WARM, 1, False, 3),
    ],
)
async def test_enable_automatic_drain_preserves_drain_mode_preference(
    device, main_mode, wte_fth_en, enabled, expected_payload
):
    _set_state(device, main_mode, wte_fth_en)

    await device.enable_automatic_drain(enabled)

    assert _sent_drain_payload(device) == expected_payload.to_bytes()


@pytest.mark.parametrize(
    ("wte_fth_en", "mode", "expected_payload"),
    [
        (0, DrainMode.DRAIN_FREE, 1),
        (1, DrainMode.EXTERNAL, 0),
        # with auto drain off only the preference bit is stored
        (2, DrainMode.DRAIN_FREE, 3),
        (3, DrainMode.EXTERNAL, 2),
    ],
)
async def test_set_drain_mode_in_cool_mode_sends_new_wte_value(
    device, wte_fth_en, mode, expected_payload
):
    _set_state(device, MainMode.COLD, wte_fth_en)

    await device.set_drain_mode(mode)

    assert _sent_drain_payload(device) == expected_payload.to_bytes()


@pytest.mark.parametrize("main_mode", [MainMode.WARM, MainMode.FAN])
@pytest.mark.parametrize("mode", [DrainMode.DRAIN_FREE, DrainMode.EXTERNAL])
async def test_set_drain_mode_is_a_noop_outside_cool_mode(device, main_mode, mode):
    _set_state(device, main_mode, 1)

    await device.set_drain_mode(mode)

    device._conn.sendPacket.assert_not_called()


def test_power_mode_select_hides_internal_init_state(device):
    select = next(
        c
        for c in device.get_controls(control_type=controls.select)
        if c.key == "power_mode"
    )

    assert select.options_str == ["on", "standby", "off"]
