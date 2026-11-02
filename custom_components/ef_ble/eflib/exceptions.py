class UnsupportedBluetoothProtocol(Exception):
    """Raised when a Bluetooth characteristic set is not supported by the device."""

    def __init__(self, char_type: object, characteristics: object) -> None:
        self.char_type = char_type
        self.characteristics = characteristics
        super().__init__(
            f"Unsupported Bluetooth protocol for {char_type}: {characteristics}"
        )


class ConnectionTimeout(TimeoutError):
    """Raised when the connection handshake or request times out."""


class PacketParseError(ValueError):
    """Raised when a packet payload does not match the expected protocol layout."""


class NotConnectedError(RuntimeError):
    """Raised when an operation requires an active BLE link."""


class FailedToAuthenticate(RuntimeError):
    """Raised when the device rejects authentication."""


class MaxConnectionAttemptsReached(RuntimeError):
    """Raised after repeatedly failing to connect."""

    def __init__(self, attempts: int, last_error: Exception | None = None) -> None:
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"Reached max connection attempts ({attempts})")


class MaxReconnectAttemptsReached(RuntimeError):
    """Raised after exhausting automatic reconnect retries."""

    def __init__(self, attempts: int, last_error: Exception | None = None) -> None:
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"Reached max reconnect attempts ({attempts})")


class AuthErrors:
    """Authentication result codes returned by EcoFlow devices."""

    class BaseException(Exception):
        """Base class for authenticated-device failures."""

    class NeedRefreshToken(BaseException):
        """The app needs to refresh the OAuth token."""

    class DeviceInternalError(BaseException):
        """The device reported an internal error."""

    class DeviceAlreadyBound(BaseException):
        """The device is already bound to another account."""

    class NeedBindInstallFirst(BaseException):
        """The companion app installation/bind step is still required."""

    class AppSendDataError(BaseException):
        """The app failed to send required data to the device."""

    class WrongKey(BaseException):
        """The supplied key material is invalid."""

    class UnknownError(BaseException):
        """The device reported an unknown auth failure."""

    class KeyInfoReqFailed(BaseException):
        """The device rejected the key info request."""

    _ERRORS_BY_CODE: dict[int, type[BaseException]] = {
        0x01: NeedRefreshToken,
        0x02: DeviceInternalError,
        0x03: DeviceAlreadyBound,
        0x04: NeedBindInstallFirst,
        0x05: AppSendDataError,
        0x06: WrongKey,
        0x07: UnknownError,
        0x08: KeyInfoReqFailed,
    }

    @classmethod
    def from_payload(cls, payload: bytes | bytearray | memoryview | str) -> type[BaseException] | None:
        if payload is None:
            return None

        data = bytes(payload) if not isinstance(payload, (bytes, bytearray, memoryview)) else bytes(payload)
        if not data:
            return None

        code = data[0]
        return cls._ERRORS_BY_CODE.get(code)
