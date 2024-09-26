"""Config flow for EcoFlow BLE integration."""
from __future__ import annotations

import logging

from typing import Any

import voluptuous as vol

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_ADDRESS
from homeassistant.helpers import config_validation as cv

from . import eflib
from .const import DOMAIN, CONF_USER_ID

_LOGGER = logging.getLogger(__name__)

class EFBLEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """EcoFlow BLE ConfigFlow"""
    VERSION = 1
    MINOR_VERSION = 0

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_device: eflib.DeviceBase | None = None
        self._discovered_devices: dict[str, str] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        device = eflib.NewDevice(discovery_info.device, discovery_info.advertisement)
        if device == None:
            return self.async_abort(reason="not_supported")
        self._discovery_info = discovery_info
        self._discovered_device = device
        _LOGGER.debug("Discovered device: %s" % (device,))
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        assert self._discovered_device is not None
        device = self._discovered_device
        assert self._discovery_info is not None
        discovery_info = self._discovery_info
        title = discovery_info.name # TODO: Read user defined title of device here
        _LOGGER.debug("Confirm discovery: %s, %s" % (title,user_input))
        if user_input is not None:
            return self.async_create_entry(title=title, data=user_input)

        self._set_confirm_only()
        placeholders = {"name": title}
        self.context["title_placeholders"] = placeholders
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders=placeholders,
            data_schema=vol.Schema({
                vol.Required(CONF_USER_ID): str,
            }),
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step to pick discovered device."""
        errors = {}
        if user_input is not None:
            try:
                address = user_input[CONF_ADDRESS]
                await self.async_set_unique_id(address, raise_on_progress=False)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=self._discovered_devices[address], data=user_input
                )
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        current_addresses = self._async_current_ids()
        for discovery_info in async_discovered_service_info(self.hass, False):
            address = discovery_info.address
            if address in current_addresses or address in self._discovered_devices:
                continue
            device = eflib.NewDevice(discovery_info.device, discovery_info.advertisement)
            if device != None:
                self._discovered_devices[address] = (
                    discovery_info.name # TODO: read user-defined title from device
                )

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USER_ID): str,
                vol.Required(CONF_ADDRESS): vol.In(self._discovered_devices),
            }),
            errors=errors,
        )
