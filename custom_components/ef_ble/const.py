"""Constants for EcoFlow BLE"""

DOMAIN = "ef_ble"
MANUFACTURER = "EcoFlow"

CONF_USER_ID = "user_id"
CONF_USER_TOKEN = "user_token"
# Device-minted OMOS `user_token`, persisted so the single-use device-token blob is
# exchanged only once; reused on later connects instead of re-minting.
CONF_OMOS_TOKEN = "omos_token"
# Opt-in: store account credentials so an expired OMOS token can be refreshed from the
# cloud automatically instead of pasting a new device token by hand.
CONF_STORE_CREDENTIALS = "store_credentials"

# Companion web page that mints a device token from EcoFlow credentials, for users
# who prefer not to enter their login in Home Assistant.
TOKEN_GENERATOR_URL = "https://gnox.github.io/device_token"
CONF_UPDATE_PERIOD = "update_period"
CONF_CONNECTION_TIMEOUT = "connection_timeout"
CONF_PACKET_VERSION = "packet_version"
CONF_COLLECT_PACKETS = "collect_packets"
CONF_COLLECT_PACKETS_AMOUNT = "collect_packets_amount"
CONF_EXTRA_BATTERY = "extra_battery"

CONF_ADVANCED_CONNECTION_OPTIONS = "advanced_connection_options"
CONF_BLUEZ_START_NOTIFY = "bluez_start_notify"

CONF_DIAGNOSTICS_OPTIONS = "diagnostics_options"
CONF_DIAGNOSTICS_ENCRYPT = "diagnostics_encrypt"
CONF_DIAGNOSTICS_ON_EXCEPTION = "diagnostics_on_exception"

CONF_LOG_MASKED = "log_masked"
CONF_LOG_PACKETS = "log_packets"
CONF_LOG_ENCRYPTED_PAYLOADS = "log_encrypted_payloads"
CONF_LOG_PAYLOADS = "log_payloads"
CONF_LOG_MESSAGES = "log_messages"
CONF_LOG_CONNECTION = "log_connection"
CONF_LOG_BLEAK = "log_bleak"


DEFAULT_UPDATE_PERIOD = 10
DEFAULT_CONNECTION_TIMEOUT = 20


LINK_WIKI_SUPPORTING_NEW_DEVICES = (
    "https://github.com/rabits/ha-ef-ble/wiki/Requesting-Support-for-New-Devices"
)
