"""Config flow for EcoFlow BLE integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import (
    CONN_CLASS_LOCAL_PUSH,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import callback

from . import eflib
from .const import CONF_USER_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


class EFBLEConfigFlow(ConfigFlow, domain=DOMAIN):
    """EcoFlow BLE ConfigFlow"""

    VERSION = 1
    MINOR_VERSION = 0

    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_device: eflib.DeviceBase | None = None
        self._discovered_devices: dict[str, str] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> ConfigFlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        device = eflib.NewDevice(discovery_info.device, discovery_info.advertisement)
        if device is None:
            return self.async_abort(reason="not_supported")
        self._discovery_info = discovery_info
        self._discovered_device = device
        _LOGGER.debug("Discovered device: %s", device)
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm discovery."""
        assert self._discovered_device is not None
        device = self._discovered_device
        assert self._discovery_info is not None
        discovery_info = self._discovery_info
        title = device.name_by_user or device.name
        _LOGGER.debug("Confirm discovery: %s, %s", title, user_input)
        if user_input is not None:
            return self.async_create_entry(title=title, data=user_input)

        self._set_confirm_only()
        placeholders = {"name": title}
        self.context["title_placeholders"] = placeholders
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders=placeholders,
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USER_ID): str,
                    vol.Required(CONF_ADDRESS, default=device.address): str,
                }
            ),
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
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
            device = eflib.NewDevice(
                discovery_info.device, discovery_info.advertisement
            )
            if device != None:
                self._discovered_devices[address] = device.name_by_user or device.name

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USER_ID): str,
                    vol.Required(CONF_ADDRESS): vol.In(self._discovered_devices),
                }
            ),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Reconfiguration of the picked device."""
        reconfigure_entry = self._get_reconfigure_entry()
        errors = {}
        if user_input is not None:
            try:
                address = self.config_entry.data.get(CONF_ADDRESS)
                await self.async_set_unique_id(address, raise_on_progress=False)
                self._abort_if_unique_id_mismatch()
                return self.async_update_reload_and_abort(
                    reconfigure_entry,
                    data_updates=user_input,
                )
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USER_ID): str,
                    vol.Required(CONF_DEVICE_NAME): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EFBLEOptionsFlowHandler(config_entry)


class EFBLEOptionsFlowHandler(OptionsFlow):
    """EcoFlow BLE config flow options handler."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    # Should contain: USER_ID, sensor aggregation tolerance & max time
                    vol.Required(x, default=self.options.get(x, 0.5)): float
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
