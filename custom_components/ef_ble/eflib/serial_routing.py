"""Addressing a device by serial number from inside a V4 payload"""

import dataclasses
from dataclasses import dataclass
from typing import ClassVar

from .packet import Packet, PacketV4


@dataclass(slots=True)
class RoutingEnvelope:
    """
    The envelope that follows the serial fragment in a serial-routed payload

    It carries the addressing the outer V4 header does not: the command the payload
    belongs to, and which module it came from or is meant for. `Packet` keeps the same
    four fields in its own header, which is why they are named to match
    """

    flags: int
    cmd_set: int
    cmd_id: int
    seq: int
    src: int
    dst: int
    dsrc: int = 1
    ddst: int = 1

    PREFIX: ClassVar[bytes] = b"\x21\x01\x40\x03\x03"
    LEN: ClassVar[int] = 13

    @classmethod
    def from_bytes(cls, data: bytes) -> "RoutingEnvelope | None":
        """Read the envelope, or `None` when `data` does not start with one"""
        if len(data) < cls.LEN or not data.startswith(cls.PREFIX):
            return None

        flags, cmd_set, cmd_id, seq, src, dsrc, dst, ddst = data[5 : cls.LEN]
        return cls(
            flags=flags,
            cmd_set=cmd_set,
            cmd_id=cmd_id,
            seq=seq,
            src=src,
            dst=dst,
            dsrc=dsrc,
            ddst=ddst,
        )

    def to_bytes(self) -> bytes:
        return self.PREFIX + bytes(
            [
                self.flags,
                self.cmd_set,
                self.cmd_id,
                self.seq,
                self.src,
                self.dsrc,
                self.dst,
                self.ddst,
            ]
        )


class SerialRouting:
    """
    Addresses a device by serial number, from inside the V4 payload

    The outer V4 header addresses the link, not the message: it is the payload that
    names the device and the command, which is what lets one link carry traffic for
    several units. Read it, never `packet.cmd_set` - on some devices the inner header
    holds serial characters where a plain frame keeps its addressing.

    Reads: the application payload is the device-side serial fragment, then a 13-byte
    envelope, then the protobuf.

    Writes: mirror the latest telemetry post's frame - reusing its session obfuscation,
    addressing and inner header via `dataclasses.replace` - and override only the
    command flags and the application payload, which is
    `serial9 + full_serial16 + envelope + protobuf`. Mirroring matters because the
    constant stretches of the frame are then the device's own bytes rather than ones we
    invented. Before any post is seen it falls back to a plain V3 frame.
    """

    HEADER_LEN: ClassVar[int] = 22
    SERIAL_FRAGMENT_LEN: ClassVar[int] = 9
    ADDRESSED_BY_SERIAL: ClassVar[int] = 1
    ADDRESSED_BY_MODULE: ClassVar[int] = 2
    _WRITE_CMD_FLAGS: ClassVar[int] = 0x10
    _WRITE_ENVELOPE_PREFIX: ClassVar[bytes] = bytes([0x40, 0x03, 0x03])

    def __init__(
        self,
        serial: str,
        *,
        cmd_set: int,
        cmd_id: int,
        dst: int,
        fallback_dst: int,
        src: int = 0x21,
        cmd_flags: int = _WRITE_CMD_FLAGS,
        sequenced_writes: bool = False,
    ) -> None:
        """
        Parameters
        ----------
        serial
            Serial of the device being addressed
        cmd_set, cmd_id
            Write command, e.g. `0xFE` / `0x11` for a config write
        dst
            Module the write is addressed to inside the envelope
        fallback_dst
            Module addressed by the plain V3 frame used before a post has been seen
        src, optional
            Module the write comes from - the app, unless a device says otherwise
        cmd_flags, optional
            The byte that opens the frame body and says how each end is addressed, as
            `destination << 4 | source`, each nibble either `ADDRESSED_BY_SERIAL` or
            `ADDRESSED_BY_MODULE`. A write carrying two serials is `0x11`; a device's own
            post, addressed from its serial to the app's module, reads back as `0x21`
        sequenced_writes, optional
            Whether to number writes in the envelope's sequence slot. The devices number
            their own posts there; leave it off where a device is known to accept a zero
        """
        self._serial = serial
        self._cmd_set = cmd_set
        self._cmd_id = cmd_id
        self._dst = dst
        self._fallback_dst = fallback_dst
        self._src = src
        self._cmd_flags = cmd_flags
        self._sequenced_writes = sequenced_writes
        self._post_template: PacketV4 | None = None
        self._envelope_template: bytes | None = None
        self._write_seq = 0x20

    @classmethod
    def split(cls, payload: bytes) -> tuple[str, bytes]:
        """Split an application payload into (device serial fragment, protobuf body)"""
        serial = payload[: cls.SERIAL_FRAGMENT_LEN].decode("ascii", errors="replace")
        return serial, payload[cls.HEADER_LEN :]

    @classmethod
    def envelope(cls, payload: bytes) -> RoutingEnvelope | None:
        """Read the envelope of an application payload"""
        return RoutingEnvelope.from_bytes(
            payload[cls.SERIAL_FRAGMENT_LEN : cls.HEADER_LEN]
        )

    def remember_post(self, packet: PacketV4) -> None:
        """Capture the post as the transport template + routing envelope (for seq)"""
        self._post_template = packet
        self._envelope_template = packet.payload[
            self.SERIAL_FRAGMENT_LEN : self.HEADER_LEN
        ]

    def _envelope_flags(self) -> int:
        # Constant per device across every captured post, so take the device's own value
        envelope = (
            RoutingEnvelope.from_bytes(self._envelope_template)
            if self._envelope_template is not None
            else None
        )
        return envelope.flags if envelope is not None else 0x00

    def _next_seq(self) -> int:
        if not self._sequenced_writes:
            return 0x00
        self._write_seq = (self._write_seq + 1) & 0xFF
        return self._write_seq

    def write_packet(self, body: bytes, cmd_id: int | None = None) -> Packet | PacketV4:
        """
        Build the control-write frame for a serialized protobuf

        `cmd_id` overrides the write command for a device whose commands are split over
        more than one, so that every frame still goes out through the one template
        """
        cmd_id = self._cmd_id if cmd_id is None else cmd_id
        if self._post_template is None:
            # No telemetry post captured yet: plain v3 fallback
            return Packet(
                self._src,
                self._fallback_dst,
                self._cmd_set,
                cmd_id,
                body,
                0x01,
                0x01,
                0x13,
            )

        envelope = (
            self._WRITE_ENVELOPE_PREFIX
            + bytes([self._envelope_flags(), self._cmd_set, cmd_id, self._next_seq()])
            + bytes([self._src, 0x01, self._dst, 0x01])
        )
        serial9 = self._serial[-self.SERIAL_FRAGMENT_LEN :].encode("ascii")
        serial16 = self._serial.encode("ascii")
        return dataclasses.replace(
            self._post_template,
            cmd_flags=self._cmd_flags,
            is_ack=True,
            is_rw_cmd=False,
            payload=serial9 + serial16 + envelope + body,
        )
