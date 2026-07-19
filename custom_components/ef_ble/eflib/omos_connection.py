"""OMOS (per-device-token) connection variant"""

from collections.abc import Callable

from bleak.backends.characteristic import BleakGATTCharacteristic
from google.protobuf.message import DecodeError

from .connection import Connection, ConnectionState
from .exceptions import AuthErrors, FailedToAuthenticate
from .logging_util import LogOptions
from .packet import Packet
from .pb import iot_comm_pb2

# OMOS auth packets use this protocol version, distinct from a device's normal packet
# version. The current app (6.15.x) sends 0x13 for the REFRESH_TOKEN/AUTHENTICATION
# commands; a 0x14 packet is silently ignored by the device.
_OMOS_PACKET_VERSION = 0x13

# Raw AuthenticationAck.result values that mean the token is stale (TokenErr /
# TokenExpire); the app clears the cached token and refreshes on these.
_OMOS_TOKEN_STALE_RESULTS = (16, 20)
# How many times to re-mint/retry within one connection before giving up.
_OMOS_MAX_REAUTH = 2


class OmosConnection(Connection):
    """`Connection` that authenticates with a per-device (OMOS) token"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._omos_user_token: str | None = None
        self._omos_random_code: str | None = None
        self._omos_user_info_en: str | None = None
        self._omos_token_listener: Callable[[str | None], None] | None = None
        self._omos_reauth_attempts: int = 0

    def set_omos_credentials(
        self,
        *,
        user_token: str | None = None,
        random_code: str | None = None,
        user_info_en: str | None = None,
    ) -> None:
        """Provide the token / cloud bind material used by OMOS auth"""
        self._omos_user_token = user_token
        self._omos_random_code = random_code
        self._omos_user_info_en = user_info_en

    def set_omos_token_listener(
        self, listener: "Callable[[str | None], None] | None"
    ) -> None:
        """
        Register a callback fired whenever the minted `user_token` changes

        The token is minted once from the single-use bind material, so HA persists it to
        the config entry and passes it back on later connects instead of re-minting. A
        `None` value is delivered when a stale token is cleared so the stored copy drops.
        """
        self._omos_token_listener = listener

    def _store_omos_token(self, token: str | None) -> None:
        self._omos_user_token = token or None
        if self._omos_token_listener is not None:
            self._omos_token_listener(self._omos_user_token)

    def _select_auth_status_reply(self, packets: list[Packet]) -> bytes | None:
        reply = self._find_omos_reply(packets, 0x89)
        return reply.payload if reply is not None else None

    async def _dispatch_authentication(self, data: bytes) -> None:
        if len(data) > 1 and data[1] == 1:
            await self.omosAuthentication()
        else:
            await self.autoAuthentication()

    async def omosAuthentication(self):
        """
        Authenticate a per-device-secret (OMOS) device

        With a cached `user_token` go straight to `Authentication` (0xAB); otherwise
        send the cloud-issued `random_code`/`user_info_en` as `ConfirmBind` (0xAA) so
        the device mints a `user_token` we then authenticate with.
        """
        self._set_state(ConnectionState.AUTHENTICATING)
        self._omos_reauth_attempts = 0

        if self._omos_user_token:
            await self._omos_verify(self._omos_user_token)
            return

        await self._omos_confirm_bind()

    async def _omos_confirm_bind(self):
        """
        Send `ConfirmBind` (0xAA) with the cloud bind material to mint a `user_token`

        Signals `NeedRefreshToken` when no bind material is stored so the caller can
        fetch fresh material or ask the user for a new device token.
        """
        if not (self._omos_random_code and self._omos_user_info_en):
            await self._omos_fail_need_refresh(
                "OMOS bind material missing; a fresh device token is required"
            )
            return

        confirm = iot_comm_pb2.ConfirmBind(
            random_code=self._omos_random_code, user_info_en=self._omos_user_info_en
        )
        packet = Packet(
            0x21,
            self._auth_header_dst,
            0x35,
            0xAA,
            confirm.SerializeToString(),
            0x01,
            0x01,
            _OMOS_PACKET_VERSION,
        )
        await self.sendPacket(packet, self._omosRefreshTokenHandler)

    async def _omos_fail_need_refresh(self, message: str) -> None:
        exc = AuthErrors.NeedRefreshToken(message)
        self._set_state(ConnectionState.ERROR_AUTH_FAILED, exc)
        await self._disconnect_client()
        raise exc

    def _find_omos_reply(self, packets: list[Packet], cmd_id: int) -> Packet | None:
        """
        Return the iot_comm (cmd_set 0x35) reply with `cmd_id`, or None

        These devices stream telemetry eagerly, so an auth reply often shares a
        notification with unrelated packets (or arrives a notification later). Selecting
        by cmd set / id avoids mis-parsing telemetry as the auth response.
        """
        for packet in packets:
            if packet.cmd_set == 0x35 and packet.cmd_id == cmd_id:
                return packet
        if packets:
            self._logger.log_filtered(
                LogOptions.CONNECTION_DEBUG,
                "OMOS: awaiting 0x%02X reply, got %s",
                cmd_id,
                [(hex(p.src), hex(p.cmd_set), hex(p.cmd_id)) for p in packets],
            )
        return None

    @Connection._auth_handler(ConnectionState.AUTHENTICATING)
    async def _omosRefreshTokenHandler(
        self, characteristic: BleakGATTCharacteristic, recv_data: bytearray
    ):
        reply = self._find_omos_reply(
            await self.parseEncPackets(bytes(recv_data)), 0xAA
        )
        if reply is None:
            return

        await self._client.stop_notify(self._notify_characteristic)

        ack = iot_comm_pb2.RefreshTokenAck()
        try:
            ack.ParseFromString(reply.payload)
        except DecodeError as e:
            raise FailedToAuthenticate(
                f"OMOS refresh reply is not a RefreshTokenAck: {reply.payload.hex()}"
            ) from e
        if not ack.user_token:
            await self._omos_fail_need_refresh(
                f"OMOS bind material rejected (result={ack.result}); "
                f"a fresh device token is required"
            )
            return

        self._store_omos_token(ack.user_token)
        await self._omos_verify(ack.user_token)

    async def _omos_verify(self, user_token: str):
        auth = iot_comm_pb2.Authentication()
        auth.user_role = iot_comm_pb2.UserRoleNormal
        auth.user_token = user_token
        packet = Packet(
            0x21,
            self._auth_header_dst,
            0x35,
            0xAB,
            auth.SerializeToString(),
            0x01,
            0x01,
            _OMOS_PACKET_VERSION,
        )
        await self.sendPacket(packet, self._omosVerifyHandler)

    @Connection._auth_handler(ConnectionState.AUTHENTICATING)
    async def _omosVerifyHandler(
        self, characteristic: BleakGATTCharacteristic, recv_data: bytearray
    ):
        reply = self._find_omos_reply(
            await self.parseEncPackets(bytes(recv_data)), 0xAB
        )
        if reply is None:
            return

        ack = iot_comm_pb2.AuthenticationAck()
        try:
            ack.ParseFromString(reply.payload)
        except DecodeError as e:
            exc = FailedToAuthenticate(
                f"OMOS auth reply is not an AuthenticationAck: {reply.payload.hex()}"
            )
            self._set_state(ConnectionState.ERROR_AUTH_FAILED, exc)
            await self._disconnect_client()
            raise exc from e
        if ack.result != 0:
            await self._omos_handle_auth_failure(ack.result, reply.payload)
            return

        await self._client.stop_notify(self._notify_characteristic)
        self._connection_attempt = 0
        self._reconnect_attempt = 0
        self._logger.info("OMOS auth completed, everything is fine")
        self._set_state(ConnectionState.AUTHENTICATED)
        self._connected.set()

        # Hand the link to the normal data listener for ongoing telemetry.
        await self._start_notify(self.listenForDataHandler)

    async def _omos_handle_auth_failure(self, result: int, payload: bytes) -> None:
        """
        React to a non-zero `AuthenticationAck.result`

        A stale-token result (`TokenErr`/`TokenExpire`) clears the cached token and
        re-mints from the bind material, mirroring the app's refresh-and-retry; the
        cleared token propagates to HA so the persisted copy is dropped. Any other
        result, or exhausting the retry budget, fails the auth.
        """
        if (
            result in _OMOS_TOKEN_STALE_RESULTS
            and self._omos_reauth_attempts < _OMOS_MAX_REAUTH
        ):
            self._omos_reauth_attempts += 1
            self._store_omos_token(None)
            await self._client.stop_notify(self._notify_characteristic)
            self._logger.info(
                "OMOS token stale (result=%d); re-minting (attempt %d/%d)",
                result,
                self._omos_reauth_attempts,
                _OMOS_MAX_REAUTH,
            )
            await self._omos_confirm_bind()
            return

        exc = FailedToAuthenticate(
            f"OMOS auth failed (result={result}, payload={payload.hex()})"
        )
        self._set_state(ConnectionState.ERROR_AUTH_FAILED, exc)
        await self._disconnect_client()
        raise exc
