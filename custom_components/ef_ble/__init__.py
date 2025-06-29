"""The unofficial EcoFlow BLE devices integration"""

from __future__ import annotations

import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, CONF_TYPE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.device_registry import DeviceInfo

from . import eflib
from .config_flow import ConfLogOptions, LogOptions
from .const import CONF_UPDATE_PERIOD, CONF_USER_ID, DOMAIN, MANUFACTURER

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SELECT,
]

type DeviceConfigEntry = ConfigEntry[eflib.DeviceBase]

_LOGGER = logging.getLogger(__name__)


class _ConfigNotReady(ConfigEntryNotReady):
    def __init__(
        self,
        translation_key: str | None = None,
        translation_placeholders: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            translation_domain=DOMAIN,
            translation_key=translation_key,
            translation_placeholders=translation_placeholders,
        )


async def async_setup_entry(hass: HomeAssistant, entry: DeviceConfigEntry) -> bool:
    """Set up EF BLE device from a config entry."""
    _LOGGER.debug("Init EcoFlow BLE Integration")

    address = entry.data.get(CONF_ADDRESS)
    user_id = entry.data.get(CONF_USER_ID)
    merged_options = entry.data | entry.options
    update_period = merged_options.get(CONF_UPDATE_PERIOD, 0)

    if address is None or user_id is None:
        return False

    if not bluetooth.async_address_present(hass, address):
        raise _ConfigNotReady("device_not_present")

    _LOGGER.debug("Connecting Device")
    discovery_info = bluetooth.async_last_service_info(hass, address, connectable=True)
    device = eflib.NewDevice(discovery_info.device, discovery_info.advertisement)
    if device is None:
        raise _ConfigNotReady("unable_to_create_device")

    await (
        device.with_update_period(update_period)
        .with_logging_options(ConfLogOptions.from_config(merged_options))
        .connect(user_id)
    )
    entry.runtime_data = device

    timeout = 30
    state = await device.wait_until_connected_or_error(timeout=timeout)

    if state.connection_error():
        raise _ConfigNotReady(
            "could_not_connect", translation_placeholders={"time": str(timeout)}
        )
    if state.is_error():
        raise _ConfigNotReady("error_after_connected")
    if not state.authenticated():
        raise _ConfigNotReady("could_not_authenticate")

    _LOGGER.debug("Creating entities")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug("Setup done")
    entry.async_on_unload(entry.add_update_listener(_update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: DeviceConfigEntry) -> bool:
    """Unload a config entry."""
    device = entry.runtime_data
    await device.disconnect()
    device.with_logging_options(LogOptions.no_options())
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


def device_info(entry: ConfigEntry) -> DeviceInfo:
    """Device info."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.data.get(CONF_ADDRESS))},
        name=entry.title,
        manufacturer=MANUFACTURER,
        model=entry.data.get(CONF_TYPE),
    )


async def _update_listener(hass: HomeAssistant, entry: DeviceConfigEntry):
    device = entry.runtime_data
    merged_options = entry.data | entry.options
    update_period = merged_options.get(CONF_UPDATE_PERIOD, 0)
    device.with_update_period(update_period).with_logging_options(
        ConfLogOptions.from_config(merged_options)
    )
