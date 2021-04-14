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
    BUFFER_SIZE = 1024*32

    def __init__(self, username, password, ip, key):
        self.password = password
        self.username = username
        self.ip = ip
        self.socket = None
        self.key = key
        self.waittime = 0.01
        self.rscp_utils = RSCPUtils()

    def create_encrypt(self):
        self.encrypt_decrypt = RSCPEncryptDecrypt(self.key)

    def send_requests2(self, payload: [Union[RSCPDTO, RSCPTag]], waittime = 0.0) -> [RSCPDTO]:
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
        logger.debug("Sending " + str(len(dto_list)) + " requests to " + str(self.ip))
        responses: [RSCPDTO] = []
        dto: RSCPDTO
        for dto in dto_list:
            response = self.send_request(dto, True, waittime=waittime)
            responses.append(response)
        return responses

    def send_requests(self, payload: [Union[RSCPDTO, RSCPTag]], waittime = 0.0) -> [RSCPDTO]:
        payload_all = bytes()
        for payload_element in payload:
            if isinstance(payload_element, RSCPTag):
                dto = RSCPDTO(payload_element)
            else:
                dto = payload_element

            payload_all+=self.rscp_utils.encode_data(dto)

        prepared_data = self.rscp_utils.encode_frame(payload_all)
        response =  self.send_request(prepared_data, True, waittime)

        responses: [RSCPDTO] = []
        if response.type == RSCPType.Container:
            data: RSCPDTO
            for data in response:
                responses.append(data)
        else:
            responses.append(response)

        return responses

    def send_request(self, payload: Union[RSCPDTO, RSCPTag, bytes], keep_connection_alive: bool = False, waittime: float = 0.0) -> RSCPDTO:
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
            
        #rawdata = binascii.hexlify(prepared_data)
        #logger.debug('Send RAW: ' + str(rawdata))
        logger.debug('Send ' + str(len(prepared_data)) + ' Bytes')
        encrypted_data = self.encrypt_decrypt.encrypt(prepared_data)
        try:
            self.socket.send(encrypted_data)
        except:
            self._disconnect()
            raise

        wait = self.waittime + waittime
        if wait > 0.0:
            time.sleep(wait)

        response = self._receive()
        if response.type == RSCPType.Error:
            logger.debug("Error type returned: " + str(response.data))
            raise (RSCPCommunicationError('Error type returned: ' + str(response.data), logger, response))
        if not keep_connection_alive:
            self._disconnect()
        return response
        
    def _connect(self):
        if self.socket is None:
            logger.info("Trying to establish connection to " + str(self.ip))
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.PORT))
            self.socket.setblocking(False)
            rscp_dto = RSCPDTO(RSCPTag.RSCP_REQ_AUTHENTICATION, RSCPType.Container,
                               [RSCPDTO(RSCPTag.RSCP_AUTHENTICATION_USER, RSCPType.CString, self.username),
                                RSCPDTO(RSCPTag.RSCP_AUTHENTICATION_PASSWORD, RSCPType.CString, self.password)], None)
            self.create_encrypt()
            result = self.send_request(rscp_dto, True)
            if result.type == RSCPType.Error:
                self._disconnect()
                raise RSCPAuthenticationError("Invalid username or password", logger)

    def _disconnect(self):
        logger.info("Closing connection to " + str(self.ip))
        self.socket.close()
        self.socket = None

    def _receive(self) -> RSCPDTO:
        logger.debug("Waiting for response from " + str(self.ip))
        decrypted_data = None
        wait = 0.01
        while not decrypted_data:
            try:
                data = self.socket.recv(self.BUFFER_SIZE)
                logger.debug('Received ' + str(len(data)) + ' Bytes')
                if len(data) == 0:
                    self.socket.close()
                    raise RSCPCommunicationError("Did not receive data from e3dc", logger)
                self.rscp_utils = RSCPUtils()

                decrypted_data = self.encrypt_decrypt.decrypt(data)
            except BlockingIOError:
                logger.debug('Keine Daten empfangen, warte ' + str(wait) + 's')
                time.sleep(wait)
                wait*=2
                if wait > 2:
                    raise


        #rawdata = binascii.hexlify(decrypted_data)
        #logger.debug('Response RAW: ' + str(rawdata))
        rscp_dto = self.rscp_utils.decode_data(decrypted_data)
        logger.debug("Received DTO Type: " + rscp_dto.type.name + ", DTO Tag: " + rscp_dto.tag.name)
        return rscp_dto
