import binascii
import logging
import platform
import socket
import time
from typing import Union

from e3dc._rscp_dto import RSCPDTO
from e3dc._rscp_encrypt_decrypt import RSCPEncryptDecrypt
from e3dc._rscp_exceptions import RSCPAuthenticationError, RSCPCommunicationError
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType
from e3dc._rscp_utils import RSCPUtils

logger = logging.getLogger(__name__)

class E3DC:
    PORT = 5033
    BUFFER_SIZE = 1024 * 32

    def __init__(self, username, password, ip, key):
        self.password = password
        self.username = username
        self.encrypt_decrypt = RSCPEncryptDecrypt(key)
        self.ip = ip
        self.socket = None
        self.rscp_utils = RSCPUtils()

    def send_requests(self, payload: [Union[RSCPDTO, RSCPTag]]) -> [RSCPDTO]:
        """
        This function will send a list of requests consisting of RSCPDTO's oder RSCPTag's to the e3dc
        and returns a list of responses.

        i.e. responses = send_requests([RSCPTag.EMS_REQ_BAT_SOC, RSCPTag.EMS_REQ_POWER_PV,
                                            RSCPTag.EMS_REQ_POWER_BAT, RSCPTag.EMS_REQ_POWER_GRID,
                                            RSCPTag.EMS_REQ_POWER_WB_ALL])
        :param payload: A list of requests
        :return: A list of responses in form of RSCPDTO's
        """
        dto_list: [RSCPDTO] = []
        for payload_element in payload:
            if isinstance(payload_element, RSCPTag):
                dto_list.append(RSCPDTO(payload_element))
            else:
                dto_list.append(payload_element)
        logger.info("Sending " + str(len(dto_list)) + " requests to " + str(self.ip))
        responses: [RSCPDTO] = []
        dto: RSCPDTO
        for dto in dto_list:
            responses.append(self.send_request(dto, True))
        return responses

    def send_request(self, payload: Union[RSCPDTO, RSCPTag, bytes], keep_connection_alive: bool = False) -> RSCPDTO:
        """
        This will perform a single request.

        :param payload: The payload that defines the request
        :param keep_connection_alive: A flag whether to keep the connection alive or not
        :return: A response object as RSCPDTO
        """
        if isinstance(payload, RSCPTag):
            payload = RSCPDTO(payload)
        if self.socket is None:
            self._connect()
            
        if isinstance(payload, bytes):
            prepared_data = payload
        else:
            encode_data = self.rscp_utils.encode_data(payload)
            prepared_data = self.rscp_utils.encode_frame(encode_data)
            
        rawdata = binascii.hexlify(prepared_data)
        logger.debug('Send RAW: ' + str(rawdata))
        encrypted_data = self.encrypt_decrypt.encrypt(prepared_data)
        self.socket.send(encrypted_data)
        # Fix for MAC-Connectionerrors @eba
        if platform.system() == 'Darwin':
            time.sleep(0.05)
        else:
            time.sleep(0.01)
        response = self._receive()
        if response.type == RSCPType.Error:
            logger.error("Error type returned")
            raise (RSCPCommunicationError(None, logger))
        if not keep_connection_alive:
            self._disconnect()
        return response
        
    def _connect(self):
        if self.socket is None:
            logger.info("Trying to establish connection to " + str(self.ip))
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.PORT))
            rscp_dto = RSCPDTO(RSCPTag.RSCP_REQ_AUTHENTICATION, RSCPType.Container,
                               [RSCPDTO(RSCPTag.RSCP_AUTHENTICATION_USER, RSCPType.CString, self.username),
                                RSCPDTO(RSCPTag.RSCP_AUTHENTICATION_PASSWORD, RSCPType.CString, self.password)], None)
            result = self.send_request(rscp_dto, True)
            if result.type == RSCPType.Error:
                self._disconnect()
                raise RSCPAuthenticationError("Invalid username or password", logger)

    def _disconnect(self):
        logger.info("Closing connection to " + str(self.ip))
        self.socket.close()
        self.socket = None

    def _receive(self) -> RSCPDTO:
        logger.info("Waiting for response from " + str(self.ip))
        data = self.socket.recv(self.BUFFER_SIZE)
        if len(data) == 0:
            self.socket.close()
            raise RSCPCommunicationError("Did not receive data from e3dc", logger)
        self.rscp_utils = RSCPUtils()
        decrypted_data = self.encrypt_decrypt.decrypt(data)
        rawdata = binascii.hexlify(decrypted_data)
        logger.debug('Response RAW: ' + str(rawdata))
        rscp_dto = self.rscp_utils.decode_data(decrypted_data)
        logger.debug("Received DTO Type: " + rscp_dto.type.name + ", DTO Tag: " + rscp_dto.tag.name)
        return rscp_dto
