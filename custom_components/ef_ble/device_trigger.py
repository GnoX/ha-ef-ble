"""Device triggers for the EcoFlow BLE connection event."""

import voluptuous as vol
from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.event import DOMAIN as EVENT_DOMAIN
from homeassistant.components.homeassistant.triggers import state as state_trigger
from homeassistant.const import (
    CONF_ATTRIBUTE,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_PLATFORM,
    CONF_TYPE,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .event import EVENT_CONNECTED, EVENT_DISCONNECTED

TRIGGER_TYPES = (EVENT_CONNECTED, EVENT_DISCONNECTED)

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_id_or_uuid,
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    """List `connected`/`disconnected` triggers for the device's connection event"""
    registry = er.async_get(hass)
    triggers: list[dict[str, str]] = []
    for entry in er.async_entries_for_device(registry, device_id):
        if entry.domain != EVENT_DOMAIN or not (entry.unique_id or "").endswith(
            "_connection"
        ):
            continue
        triggers.extend(
            {
                CONF_PLATFORM: "device",
                CONF_DEVICE_ID: device_id,
                CONF_DOMAIN: DOMAIN,
                CONF_ENTITY_ID: entry.id,
                CONF_TYPE: trigger_type,
            }
            for trigger_type in TRIGGER_TYPES
        )
    return triggers


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """
    Fire when the connection event of the configured type is emitted

    Delegates to the state trigger watching the event entity's `event_type` attribute,
    which changes to the fired type on every emission (including the `connected` fired
    when the entity is recreated after a reconnect).
    """
    state_config = {
        CONF_PLATFORM: "state",
        state_trigger.CONF_ENTITY_ID: config[CONF_ENTITY_ID],
        CONF_ATTRIBUTE: "event_type",
        state_trigger.CONF_TO: config[CONF_TYPE],
    }
    state_config = await state_trigger.async_validate_trigger_config(hass, state_config)
    return await state_trigger.async_attach_trigger(
        hass, state_config, action, trigger_info, platform_type="device"
    )
