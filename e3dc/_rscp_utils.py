import binascii
import logging
import math
import struct
import time
import traceback
import zlib

from e3dc._rscp_dto import RSCPDTO
from e3dc._rscp_exceptions import RSCPFrameError, RSCPDataError
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType

logger = logging.getLogger(__name__)

class RSCPUtils:
    _FRAME_HEADER_FORMAT = "<HHQIH"
    _FRAME_CRC_FORMAT = "I"
    _DATA_HEADER_FORMAT = "<IBH"
    _MAGIC_CHECK_FORMAT = ">H"

    def encode_frame(self, data: bytes, crc: bool = True) -> bytes:
        magic_byte = self._endian_swap_uint16(0xe3dc)
        if crc:
            ctrl_byte = self._endian_swap_uint16(0x11)
        else:
            ctrl_byte = self._endian_swap_uint16(0x01)
        current_time = time.time()
        seconds = math.ceil(current_time)
        nanoseconds = round((current_time - int(current_time)) * 1000)
        length = len(data)
        frame = struct.pack(self._FRAME_HEADER_FORMAT + str(length) + "s", magic_byte, ctrl_byte, seconds, nanoseconds,
                            length, data)
        if crc:
            checksum = zlib.crc32(frame) % (1 << 32)
            frame += struct.pack(self._FRAME_CRC_FORMAT, checksum)
        return frame

    def encode_data(self, rscp_dto: RSCPDTO) -> bytes:
        pack_format = self._DATA_HEADER_FORMAT
        data_header_length = struct.calcsize(self._DATA_HEADER_FORMAT)
        if rscp_dto.type == RSCPType.Nil:
            return struct.pack(self._DATA_HEADER_FORMAT, rscp_dto.tag.value, rscp_dto.type.value, 0)
        elif rscp_dto.type == RSCPType.Timestamp:
            timestamp = int(rscp_dto.data / 1000)
            milliseconds = int((rscp_dto.data - timestamp * 1000) * 1e6)
            high = timestamp >> 32
            low = timestamp & 0xffffffff
            length = struct.calcsize("iii") - data_header_length
            return struct.pack(self._DATA_HEADER_FORMAT + "iii", rscp_dto.tag.value, rscp_dto.type.value, length, high, low, milliseconds)
        elif rscp_dto.type == RSCPType.Container:
            if isinstance(rscp_dto.data, list):
                new_data = b''
                for data_chunk in rscp_dto.data:
                    new_data += self.encode_data(data_chunk)
                rscp_dto.set_data(new_data)
                pack_format += str(len(rscp_dto.data)) + rscp_dto.type.mapping
        elif rscp_dto.type.mapping in ("s","r"):
            if isinstance(rscp_dto.data, str):
                # We do expect a string object. Make it to bytes array
                rscp_dto.set_data(bytes(rscp_dto.data, encoding="latin_1"))
            pack_format += str(len(rscp_dto.data)) + "s"
        elif rscp_dto.type.mapping != "s":
            pack_format += rscp_dto.type.mapping

        data_length = struct.calcsize(pack_format) - data_header_length
        logger.debug("pack_format: " + pack_format)
        logger.debug("data: " + str(rscp_dto.data))
        try:
            res = struct.pack(pack_format, rscp_dto.tag.value, rscp_dto.type.value, data_length, rscp_dto.data)
        except:
            traceback.print_exc()

        return res

    def _decode_frame(self, frame_data) -> tuple:
        """

        :param frame_data:
        :return:
        """
        crc = None
        magic, ctrl, seconds, nanoseconds, length = struct.unpack(self._FRAME_HEADER_FORMAT, frame_data[
                                                                                             :struct.calcsize(
                                                                                                 self._FRAME_HEADER_FORMAT)])

        if ctrl & 0x10:
            logger.debug("CRC is enabled")
            total_length = struct.calcsize(self._FRAME_HEADER_FORMAT) + length + struct.calcsize(self._FRAME_CRC_FORMAT)
            data, crc = struct.unpack("<" + str(length) + "s" + self._FRAME_CRC_FORMAT,
                                      frame_data[struct.calcsize(self._FRAME_HEADER_FORMAT):total_length])
        else:
            total_length = struct.calcsize(self._FRAME_HEADER_FORMAT) + length
            data = \
                struct.unpack("<" + str(length) + "s",
                              frame_data[struct.calcsize(self._FRAME_HEADER_FORMAT):total_length])[
                    0]
            logger.debug("CRC is disabled")

        self._check_crc_validity(crc, frame_data)
        timestamp = seconds + float(nanoseconds) / 1000
        return data, timestamp

    def decode_server_data(self, data) -> RSCPDTO:
        if isinstance(data, str):
            data = binascii.unhexlify(data)

        rscp_dto = self.decode_data(data)

        f = rscp_dto['SERVER_RSCP_DATA']
        if f:
            b = f.data
            res, timestamp = self._decode_frame(b)
            f.type = RSCPType.Container
            data = self.decode_data(res)
            f.data = data

        return rscp_dto

    def decode_data(self, data: bytes) -> RSCPDTO:
        magic_byte = struct.unpack(self._MAGIC_CHECK_FORMAT, data[:struct.calcsize(self._MAGIC_CHECK_FORMAT)])[0]
        if magic_byte == 0xe3dc:
            decode_frame_result = self._decode_frame(data)
            return self.decode_data(decode_frame_result[0])

        data_header_size = struct.calcsize(self._DATA_HEADER_FORMAT)
        data_tag_hex, data_type_hex, data_length = struct.unpack(self._DATA_HEADER_FORMAT,
                                                                 data[:data_header_size])
        data_tag = RSCPTag(data_tag_hex)
        data_type = RSCPType(data_type_hex)

        # Check the data type name to handle the values accordingly
        if data_type == RSCPType.Container:
            container_data = []
            current_byte = data_header_size
            while current_byte < data_header_size + data_length:
                # inner_data, used_length = self.decode_data(data[current_byte:])
                data_tag_hex_c, data_type_hex_c, data_length_c = struct.unpack(self._DATA_HEADER_FORMAT,
                                                                         data[current_byte:current_byte + data_header_size])
                inner_rscp_dto = self.decode_data(data[current_byte:data_header_size + current_byte + data_length_c])
                current_byte += inner_rscp_dto.size
                container_data.append(inner_rscp_dto)
            return RSCPDTO(data_tag, data_type, container_data, current_byte)
        # Für Datensammlungen ohne Container, es wird ein Dummy gebildet
        elif data_header_size + data_length != len(data):
            container_data = []
            current_byte = 0
            while current_byte < len(data):
                data_tag_hex_c, data_type_hex_c, data_length_c = struct.unpack(self._DATA_HEADER_FORMAT,
                                                                               data[
                                                                               current_byte:current_byte + data_header_size])
                inner_rscp_dto = self.decode_data(data[current_byte:data_header_size + current_byte + data_length_c])
                current_byte += inner_rscp_dto.size
                container_data.append(inner_rscp_dto)
            return RSCPDTO(RSCPTag.LIST_TYPE, RSCPType.Container, container_data, current_byte)
        elif data_type == RSCPType.Timestamp:
            data_format = "<iii"
            high, low, ms = struct.unpack(data_format,
                                          data[data_header_size:data_header_size + struct.calcsize(data_format)])
            timestamp = float(high + low) + (float(ms) * 1e-9)
            return RSCPDTO(data_tag, data_type, timestamp, data_header_size + struct.calcsize(data_format))
        elif data_type.name == "Nil":
            return RSCPDTO(data_tag, data_type, None, data_header_size)
        elif data_type.mapping == 'r':
            data_format = str(data_length) + "s"
        elif data_type.mapping != "s":
            data_format = "<" + data_type.mapping
        elif data_type.mapping == "s":
            data_format = "<" + str(data_length) + data_type.mapping
        else:
            raise RSCPDataError("Unknown data type: " + str(data_type_hex), logger)

        value = struct.unpack(data_format, data[data_header_size:data_header_size + struct.calcsize(data_format)])[0]
        if data_type.mapping == "s":
            try:
                value = value.decode()
            except:
                value = value.decode("utf-8", "ignore")
        return RSCPDTO(data_tag, data_type, value, data_header_size + struct.calcsize(data_format))

    def _check_crc_validity(self, crc: str, frame_data: bytes):
        if crc is not None:
            frame_data_without_crc = frame_data[:-struct.calcsize("<" + self._FRAME_CRC_FORMAT)]
            calculated_crc = zlib.crc32(frame_data_without_crc) % (1 << 32)
            if calculated_crc != crc:
                raise RSCPFrameError("CRC32 not valid", logger)

    def _endian_swap_uint16(self, val: int) -> tuple:
        return struct.unpack("<H", struct.pack(">H", val))[0]
