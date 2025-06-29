class PacketParseError(Exception):
    """Error during parsing Packet"""


class EncPacketParseError(Exception):
    """Error during parsing EncPacket"""


class PacketReceiveError(Exception):
    """Error during receiving packet"""


class AuthFailedError(Exception):
    """Error during authentificating"""


class FailedToAuthenticate(Exception):
    """Failed to connect"""


class ConnectionTimeout(TimeoutError):
    """Connection timeout reached"""


class MaxConnectionAttemptsReached(Exception):
    """Device could not complete initial connection after maximum attempts"""

    def __init__(
        self, last_error: Exception | type[Exception] | None = None, attempts: int = 8
    ):
        super().__init__()
        self.last_error = last_error
        self.attempts = attempts


class MaxReconnectAttemptsReached(Exception):
    """Device could not reconnect after maximum attempts"""

    def __init__(self, last_error: Exception | type[Exception], attempts: int = 2):
        super().__init__(
            f"Could not connect to device after {attempts} unsuccessful attempts"
        )
        self.last_error = last_error
        self.attempts = attempts
