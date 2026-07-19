"""OMOS (per-device-token) auth helpers for the config-entry setup flow."""

import asyncio
import logging
from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_REGION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import eflib
from .const import CONF_OMOS_TOKEN, CONF_USER_TOKEN
from .eflib.exceptions import AuthErrors
from .eflib.login import (
    DeviceBindInfo,
    EcoFlowLogin,
    Region,
    decode_device_token,
)

_LOGGER = logging.getLogger(__name__)

type DeviceConfigEntry = ConfigEntry[eflib.DeviceBase]


def is_configured(merged_options: dict) -> bool:
    """
    True when this entry carries OMOS material for the device

    OMOS is a per-installation property (e.g. a professionally-installed unit), not a
    fixed per-model trait, so the presence of a pasted device token or a previously
    minted token is the real signal - not the device class.
    """
    return bool(
        merged_options.get(CONF_USER_TOKEN) or merged_options.get(CONF_OMOS_TOKEN)
    )


def make_omos_token_listener(
    hass: HomeAssistant, entry: DeviceConfigEntry
) -> Callable[[str | None], None]:
    """Build a callback that persists (or clears) the device-minted OMOS token"""

    def _persist(token: str | None) -> None:
        data = {**entry.data}
        if token:
            if data.get(CONF_OMOS_TOKEN) == token:
                return
            data[CONF_OMOS_TOKEN] = token
        elif CONF_OMOS_TOKEN in data:
            del data[CONF_OMOS_TOKEN]
        else:
            return
        hass.config_entries.async_update_entry(entry, data=data)

    return _persist


async def _refresh_bind_material(
    hass: HomeAssistant, entry: DeviceConfigEntry, device: eflib.DeviceBase
) -> DeviceBindInfo | None:
    """
    Re-fetch fresh OMOS bind material from the cloud using stored credentials

    Returns `None` when no credentials are stored (the account-free setup) or the
    cloud call fails, in which case the caller surfaces the original auth error and the
    user regenerates a device token by hand.
    """
    email = entry.data.get(CONF_EMAIL)
    password = entry.data.get(CONF_PASSWORD)
    if not email or not password:
        return None

    region = entry.data.get(CONF_REGION, Region.AUTO.value)
    client = EcoFlowLogin(async_get_clientsession(hass))
    result = await client.login(email, password, region)
    if result.error or not result.token or not result.base_url:
        _LOGGER.warning("OMOS token refresh login failed: %s", result.error)
        return None

    info = await client.get_device_bind_info(
        result.base_url, result.token, device.serial_number
    )
    if info.error:
        _LOGGER.warning("OMOS bind material refresh failed: %s", info.error)
        return None
    return info


async def connect_omos(
    hass: HomeAssistant,
    entry: DeviceConfigEntry,
    device: eflib.DeviceBase,
    *,
    user_id: str,
    timeout: float,
    merged_options: dict,
):
    """
    Connect and authenticate a token-auth (OMOS) device

    Reads the pasted device-token blob and the persisted minted token from the entry,
    then authenticates. A `NeedRefreshToken` failure means the persisted token and any
    stored blob are exhausted; when credentials are stored the bind material is
    re-fetched from the cloud and the connection retried once, mirroring the app's
    refresh-and-retry.
    """
    token_blob = merged_options.get(CONF_USER_TOKEN)
    bind = decode_device_token(token_blob) if token_blob else None
    if bind is not None and bind.error:
        _LOGGER.warning("Ignoring invalid device token: %s", bind.error)
        bind = None
    omos_token = merged_options.get(CONF_OMOS_TOKEN)
    persist = make_omos_token_listener(hass, entry)

    async def _attempt(active_bind: DeviceBindInfo | None, active_token: str | None):
        await device.connect(
            user_id=user_id,
            max_attempts=0 if eflib.is_solar_only(device) else None,
            omos_user_token=active_token,
            omos_random_code=active_bind.random_code if active_bind else None,
            omos_user_info_en=active_bind.user_info_en if active_bind else None,
            omos_token_listener=persist,
        )
        async with asyncio.timeout(timeout):
            return await device.wait_until_authenticated_or_error(raise_on_error=True)

    try:
        return await _attempt(bind, omos_token)
    except AuthErrors.NeedRefreshToken:
        fresh = await _refresh_bind_material(hass, entry, device)
        if fresh is None or fresh.error:
            raise
        persist(None)  # drop the stale persisted token before re-minting
        await device.disconnect()
        return await _attempt(fresh, None)
