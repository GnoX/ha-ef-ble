"""
Shared base for EcoFlow V4 smart-panel devices (SHP3, OCEAN Pro)

These devices authenticate over V3 but stream telemetry as V4 (`PacketV4`) frames whose
application payload is a routing header followed by a `dev_apl_comm` protobuf. They also
share the one-time user-id registration, RTC keepalive and liveness-ping handshake.
"""

import dataclasses
import time
from abc import abstractmethod
from enum import IntEnum

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from google.protobuf.message import Message

from ..commands import TimeCommands
from ..devicebase import DeviceBase
from ..packet import Packet, PacketV4
from ..pb import dev_apl_comm_pb2
from ..props import ProtobufProps, pb_indexed_attr, proto_attr_mapper
from ..props.enums import IntFieldValue

pb_cfg = proto_attr_mapper(dev_apl_comm_pb2.ConfigWrite)


class CircuitControl(IntEnum):
    ON = 1
    OFF = 2


class GridStatus(IntFieldValue):
    UNKNOWN = -1

    NOT_VALID = 0
    GRID_IN = 1
    GRID_OFFLINE = 2
    FEED_GRID = 3


class CircuitStatus(IntFieldValue):
    """Per-circuit relay status from `LoadChSta.load_sta` (`LOAD_CH_STA`)"""

    UNKNOWN = -1  # LOAD_CH_UNKNOWN_STA (4) and any unrecognized value

    OFF = 0
    ON_GRID = 1
    ON_BACK = 2
    EM_STOP = 3


class V4PanelRouting:
    """
    V4 panel routing layer that wraps the protobuf inside the v4 payload

    Reads: the v4 application payload is a routing header (the device-side SN fragment
    plus a 13-byte envelope) followed by the protobuf body.

    Writes: mirror the latest telemetry post's v4 frame - reusing its session
    obfuscation, addressing and inner header via `dataclasses.replace` - and only
    override cmd_flags / is_ack / is_rw_cmd and the application payload. The payload is
    `serial9 + full_serial16 + envelope + ConfigWrite`, where the envelope is `40 03 03
    <seq> FE 11 00 21 01 0B 01` (FE 11 = PROPERTY_WRITE). Before any post is seen it
    falls back to a plain v3 frame.
    """

    HEADER_LEN = 22  # device SN fragment (9) + envelope (13), on reads
    _SERIAL_FRAGMENT_LEN = 9
    _WRITE_CMD_FLAGS = 0x10
    _WRITE_ENVELOPE_PREFIX = bytes([0x40, 0x03, 0x03])
    _WRITE_ENVELOPE_MID = bytes(
        [0xFE, 0x11, 0x00]
    )  # cmd_set 0xFE, cmd_id 0x11, reserved
    _WRITE_ENVELOPE_SUFFIX = bytes([0x21, 0x01, 0x0B, 0x01])

    def __init__(self, serial: str) -> None:
        self._serial = serial
        self._post_template: PacketV4 | None = None
        self._envelope_template: bytes | None = None
        self._write_seq = 0x20

    @classmethod
    def split(cls, payload: bytes) -> tuple[str, bytes]:
        """Split a v4 application payload into (device SN fragment, protobuf body)"""
        serial = payload[: cls._SERIAL_FRAGMENT_LEN].decode("ascii", errors="replace")
        return serial, payload[cls.HEADER_LEN :]

    def remember_post(self, packet: PacketV4) -> None:
        """Capture the post as the transport template + routing envelope (for seq)"""
        self._post_template = packet
        self._envelope_template = packet.payload[
            self._SERIAL_FRAGMENT_LEN : self.HEADER_LEN
        ]

    def _next_seq(self) -> int:
        # Track the device's session seq from the latest post, else a local counter.
        if self._envelope_template is not None and len(self._envelope_template) > 5:
            return self._envelope_template[5]
        self._write_seq = (self._write_seq + 1) & 0xFF
        return self._write_seq

    def write_packet(self, config_bytes: bytes) -> Packet | PacketV4:
        """Build the control-write frame for a serialized `ConfigWrite`"""
        if self._post_template is None:
            # No telemetry post captured yet: plain v3 fallback.
            return Packet(0x21, 0x60, 0xFE, 0x11, config_bytes, 0x01, 0x01, 0x13)
        envelope = (
            self._WRITE_ENVELOPE_PREFIX
            + bytes([self._next_seq()])
            + self._WRITE_ENVELOPE_MID
            + self._WRITE_ENVELOPE_SUFFIX
        )
        serial9 = self._serial[-self._SERIAL_FRAGMENT_LEN :].encode("ascii")
        serial16 = self._serial.encode("ascii")
        payload = serial9 + serial16 + envelope + config_bytes
        return dataclasses.replace(
            self._post_template,
            cmd_flags=self._WRITE_CMD_FLAGS,
            is_ack=True,
            is_rw_cmd=False,
            payload=payload,
        )


class V4PanelDevice(DeviceBase, ProtobufProps):
    """
    Base for EcoFlow V4 smart-panel devices

    Subclasses set `SN_PREFIX`, `_TELEMETRY_SRC` (the module address the device streams
    its own uploads from) and implement `_parse_telemetry` to decode the protobuf body.
    """

    _KEEPALIVE_INTERVAL = 20
    _USERID_FIELD_LEN = 64

    # Module address the device streams its own telemetry from (uploads from any other
    # source are sub-device frames forwarded by the device).
    _TELEMETRY_SRC: int

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)
        self._time_commands = TimeCommands(self)
        self._routing = V4PanelRouting(sn)
        self.add_timer_task(self._send_keepalive, interval=self._KEEPALIVE_INTERVAL)
        self._userid_sent = False

    @classmethod
    def check(cls, sn):
        return sn[:4] in cls.SN_PREFIX

    @abstractmethod
    def _parse_telemetry(self, body: bytes) -> None:
        """Decode a deobfuscated protobuf body into device fields"""

    async def _send_keepalive(self) -> None:
        await self._time_commands.sendRTCCheck()

    async def _send_userid_registration(self) -> None:
        user_id = (getattr(self._conn, "_user_id", "") or "").encode("ascii")
        payload = (
            bytes([0x01])
            + user_id[: self._USERID_FIELD_LEN].ljust(self._USERID_FIELD_LEN, b"\x00")
            + int(time.time()).to_bytes(4, "little")
        )
        packet = Packet(
            src=0x21,
            dst=0x35,
            cmd_set=0x35,
            cmd_id=0xA8,
            payload=payload,
            dsrc=0x01,
            ddst=0x01,
            version=0x03,
        )
        await self._conn.sendPacket(packet, wait_for_response=False)

    async def _send_config_packet(self, message: Message):
        packet = self._routing.write_packet(message.SerializeToString())
        await self._conn.sendPacket(packet)

    def _build_circuit_power_config(self, circuit_id: int, enable: bool):
        """
        Build a `ConfigWrite` turning a load circuit on or off, ganging split-phase

        A split-phase (240 V) circuit spans two breaker slots; the panel reports the
        paired slot in `load_ch{n}_sta.splitphase.link_ch`, so both legs are switched
        together. Returns `None` (and logs) when split info is missing or the reported
        link is out of range, so the caller skips the write.
        """
        split_link = self.circuit_split_link[circuit_id]
        if split_link is None:
            self._logger.warning(
                "Cannot set circuit power for circuit %d: split info not available",
                circuit_id,
            )
            return None

        is_split = split_link != 0
        if is_split and not (1 <= split_link <= self.NUM_OF_CIRCUITS):
            self._logger.warning(
                "Cannot set circuit power for circuit %d: split link %d is invalid",
                circuit_id,
                split_link,
            )
            return None

        config = dev_apl_comm_pb2.ConfigWrite()
        state = CircuitControl.ON if enable else CircuitControl.OFF
        ctrl = pb_indexed_attr(
            config, pb_cfg.cfg_load_ch1_ctrl_info, "cfg_load_ch{n}_ctrl_info"
        )
        for slot in (circuit_id, split_link) if is_split else (circuit_id,):
            ch = ctrl[slot]
            ch.chanel_enable_ctrl = state
            ch.ctrl_mode = dev_apl_comm_pb2.LOAD_RLY_CTRL_MODE_HAND
        return config

    async def packet_parse(self, data: bytes):
        return Packet.from_bytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        match packet.version, packet.src, packet.cmd_set, packet.cmd_id:
            case 0x04, src, 0x40, 0x30:
                if src == self._TELEMETRY_SRC:
                    if isinstance(packet, PacketV4):
                        self._routing.remember_post(packet)
                    _, body = self._routing.split(packet.payload)
                    self._parse_telemetry(body)
                # any other source is sub-device telemetry forwarded by the device
                processed = True
            case _, 0x35, 0x01, Packet.NET_BLE_COMMAND_CMD_SET_RET_TIME:
                if len(packet.payload) == 0:
                    self._time_commands.async_send_all()
                    if not self._userid_sent:
                        self._userid_sent = True
                        await self._send_userid_registration()
                processed = True
            case _, 0x35, 0x35, 0x20:
                await self._conn.replyPacket(packet)
                processed = True

        self._notify_updated()
        return processed
