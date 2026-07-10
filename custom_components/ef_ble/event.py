"""EcoFlow BLE connection event"""

from homeassistant.components.event import EventEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DeviceConfigEntry
from .eflib import DeviceBase
from .eflib.connection import ConnectionState
from .entity import EcoflowEntity

EVENT_CONNECTED = "connected"
EVENT_DISCONNECTED = "disconnected"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: DeviceConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the connection event entity for the config entry."""
    async_add_entities([EcoflowConnectionEvent(config_entry.runtime_data)])


class EcoflowConnectionEvent(EcoflowEntity, EventEntity):
    """
    Fires when the device connection is (re-)established or lost.

    Because a dropped BLE link reloads the config entry, this entity is recreated right
    after each successful (re-)authentication, so it fires `connected` as soon as it is
    added while authenticated - giving automations a reliable reconnect trigger instead
    of relying on a fixed delay.
    """

    _attr_translation_key = "connection"
    _attr_event_types = [EVENT_CONNECTED, EVENT_DISCONNECTED]

    def __init__(self, device: DeviceBase) -> None:
        super().__init__(device)
        self._attr_unique_id = f"ef_{self._device.serial_number}_connection"
        self._remove_listener = None
        self._last_event_type: str | None = None

    @property
    def available(self) -> bool:
        """Keep the event available so its last-fired value survives a reconnect."""
        return True

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._remove_listener = self._device.on_connection_state_change(
            self._on_connection_state_change
        )
        state = self._device.connection_state
        if state is not None and state.authenticated:
            self._fire(EVENT_CONNECTED)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove_listener is not None:
            self._remove_listener()
            self._remove_listener = None
        await super().async_will_remove_from_hass()

    @callback
    def _on_connection_state_change(self, state: ConnectionState) -> None:
        if state.authenticated:
            self._fire(EVENT_CONNECTED)
        elif state.is_error or state == ConnectionState.DISCONNECTED:
            self._fire(EVENT_DISCONNECTED)

    def _fire(self, event_type: str) -> None:
        # Avoid re-firing the same state twice in a row (e.g. the initial `connected`
        # fired on add followed by a redundant authenticated callback)
        if self._last_event_type == event_type:
            return
        self._last_event_type = event_type
        self._trigger_event(event_type)
        self.async_write_ha_state()
