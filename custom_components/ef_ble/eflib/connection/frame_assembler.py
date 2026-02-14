import abc
import logging
import struct

from Crypto.Cipher import AES

from .crc import crc8
from .encpacket import EncPacket
from .packet import Packet

_LOGGER = logging.getLogger(__name__)


class FrameReassembler(abc.ABC):
    """Base class for reassembling BLE notification fragments into frames"""

    FRAME_HEADER_LEN: int
    PACKET_PREFIX: bytes

    def __init__(self, block_size: int = AES.block_size):
        self._buffer = b""
        self._block_size = block_size

    def _skip_to_next_frame(self) -> None:
        """
        Skip current invalid data and advance to next potential frame

        Searches for the next packet prefix and updates the buffer. If no prefix found,
        clears the entire buffer.
        """
        next_packet_idx = self._buffer.find(self.PACKET_PREFIX, 1)
        if next_packet_idx != -1:
            self._buffer = self._buffer[next_packet_idx:]
        else:
            self._buffer = b""

    def add(self, data: bytes) -> list[bytes]:
        """
        Add data to buffer and extract complete frames

        Returns a list of complete frames found in the buffer. Incomplete frames remain
        in the buffer for next call.
        """
        self._buffer += data

        frames = []

        while len(self._buffer) >= self.FRAME_HEADER_LEN:
            if not self._buffer.startswith(self.PACKET_PREFIX):
                _LOGGER.debug(
                    "Skipping to next frame, current buffer: %r", self._buffer
                )
                self._skip_to_next_frame()
                continue

            if not self._validate_header_crc(self._buffer):
                _LOGGER.debug(
                    "Invalid header CRC, skipping: %r",
                    self._buffer[: self.FRAME_HEADER_LEN],
                )
                self._skip_to_next_frame()
                continue

            frame_size = self._get_frame_size(self._buffer)

            if frame_size is None:
                _LOGGER.error(
                    "Unable to determine frame size, invalid header: %r",
                    self._buffer[: self.FRAME_HEADER_LEN],
                )
                self._skip_to_next_frame()
                continue

            if len(self._buffer) < frame_size:
                # Incomplete frame, wait for more data
                break

            # Extract complete frame
            frames.append(self._buffer[:frame_size])
            self._buffer = self._buffer[frame_size:]

        return frames

    @abc.abstractmethod
    def _validate_header_crc(self, packet: bytes) -> bool:
        """Validate the header CRC to confirm this is a real frame start"""
        ...

    @abc.abstractmethod
    def _get_frame_size(self, packet: bytes) -> int | None:
        """
        Calculate the total frame size from the packet header

        Returns
        -------
            Frame size in bytes, or None if header is invalid
        """
        ...


class Type1Reassembler(FrameReassembler):
    """Reassembler for type 1 encryption packet frames"""

    PACKET_PREFIX = Packet.PREFIX
    FRAME_HEADER_LEN = 5

    def _validate_header_crc(self, packet: bytes) -> bool:
        """Validate CRC8 of header bytes [0:4]"""
        if len(packet) < 5:
            return False
        return crc8(packet[:4]) == packet[4]

    def _get_frame_size(self, packet: bytes) -> int | None:
        """
        Calculate frame size for Type1 encrypted packet

        Accounts for AES-CBC zero-padding to block_size-byte blocks.
        """
        if len(packet) < 4:
            return None

        try:
            version = packet[1]
            payload_length = struct.unpack("<H", packet[2:4])[0]

            if version == 0x02:
                inner_raw = 13 + payload_length
            else:  # v3, v19
                inner_raw = 15 + payload_length

            # Encrypted length is zero-padded to AES block size
            block_size = self._block_size
            encrypted_len = ((inner_raw + block_size - 1) // block_size) * block_size

            return self.FRAME_HEADER_LEN + encrypted_len
        except struct.error:
            _LOGGER.error("Failed to unpack payload length from packet: %r", packet[:4])
            return None


class SessionReassembler(FrameReassembler):
    """Reassembler for type 7 encrypted session frames (EncPacket)"""

    PACKET_PREFIX = EncPacket.PREFIX
    FRAME_HEADER_LEN = 6  # PREFIX (2) + header (2) + payload_length (2)

    def _validate_header_crc(self, packet: bytes) -> bool:
        """
        EncPacket header has no CRC field - just validate it's long enough.

        The CRC16 is at the end of the complete frame, not in the header.
        We validate structure by checking prefix and reasonable payload length.
        """
        if len(packet) < self.FRAME_HEADER_LEN:
            return False

        try:
            # Sanity check: payload length should be reasonable (< 1MB)
            payload_length = struct.unpack("<H", packet[4:6])[0]
        except struct.error:
            return False
        else:
            return payload_length <= 1_000_000

    def _get_frame_size(self, packet: bytes) -> int | None:
        """Calculate frame size for encrypted session packet."""
        if len(packet) < self.FRAME_HEADER_LEN:
            return None

        try:
            payload_with_crc_length = struct.unpack("<H", packet[4:6])[0]
            return self.FRAME_HEADER_LEN + payload_with_crc_length
        except struct.error:
            _LOGGER.error(
                "Failed to unpack payload length from packet: %r",
                packet[: self.FRAME_HEADER_LEN],
            )
            return None
