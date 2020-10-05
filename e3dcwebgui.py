import binascii
import hashlib
import logging
import math
import struct
import threading
import traceback

from e3dc._rscp_utils import RSCPUtils
from e3dc.e3dc import E3DC
from e3dc.rscp_helper import rscp_helper

try:
    import thread
except ImportError:
    import _thread as thread
import time

import websocket

from e3dc._rscp_dto import RSCPDTO
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

class E3DCWebGui(rscp_helper):
    timeout = 5
    timeout_connect = 10

    def __init__(self, username, password, identifier, url = None):
        self.e3dc = E3DCWeb(username, password, identifier, url)
        self._wsthread = threading.Thread(target=self.e3dc.start_ws, args = ())
        self._wsthread.start()

    def __del__(self):
        del self.e3dc

    def get_data(self, requests, raw=False):
        start = time.time()
        while not self.e3dc.connected:
            if (time.time() - start) > self.timeout_connect:
                raise Exception('WebGui Verbindungsaufbau fehlgeschlagen, Timeout')
            time.sleep(0.1)

        r = self.e3dc.getRSCPToServer(requests)
        self.e3dc.register_next_response()
        self.e3dc.send_data(r)
        start = time.time()
        while self.e3dc.next_response:
            if (time.time() - start) > self.timeout:
                raise Exception('WebGui Datenabfrage fehlgeschlagen, Timeout')
            time.sleep(0.1)

        return self.e3dc.next_response_data


class E3DCWeb(E3DC):
    def __init__(self, username, password, identifier, url = None):
        logger.debug('Initialisiere E3DC-Websockets')
        if not url:
            url = 'wss://s10.e3dc.com/ws'
        self.password = password
        self.username = username
        self.rscp_utils = RSCPUtils()
        self.identifier = identifier
        self.url = url
        logger.debug('Init abgeschlossen')

    server_connection_id = None
    server_auth_level = None
    info_serial_number = None
    server_type = None
    ws = None

    next_response = None
    next_response_data = None

    def get_connected(self):
        if self.server_auth_level == 10 and self.server_connection_id and self.server_auth_level and self.identifier:
            return True
        else:
            return False

    connected = property(get_connected)


    def register_next_response(self):
        self.next_response = True
        self.next_response_data = None

    def getWeblogin(self):
        r = RSCPDTO(RSCPTag.SERVER_REQ_NEW_VIRTUAL_CONNECTION, rscp_type=RSCPType.Container)

        r += RSCPDTO(RSCPTag.SERVER_USER, RSCPType.CString, self.username)
        pass_md5 = hashlib.md5()
        pass_md5.update(self.password.encode('utf-8'))
        password = pass_md5.hexdigest()
        r += RSCPDTO(RSCPTag.SERVER_PASSWD, RSCPType.CString, password)

        r += RSCPDTO(RSCPTag.SERVER_IDENTIFIER, RSCPType.CString, self.identifier)
        r += RSCPDTO(RSCPTag.SERVER_TYPE, RSCPType.Int32, 4)
        r += RSCPDTO(RSCPTag.SERVER_HASH_CODE, RSCPType.Int32, 1234567890)

        return [r]

    def interpreter_serverdata(self, data):
        if not isinstance(data, list):
            data = [data]

        requests = []
        for res in data:
            if res.name == 'SERVER_REGISTER_CONNECTION':
                logger.debug(res.name)
                self.server_connection_id = res['SERVER_CONNECTION_ID'].data
                self.server_auth_level = res['SERVER_AUTH_LEVEL'].data
                self.server_type = res['SERVER_TYPE'].data

                r = RSCPDTO(tag=RSCPTag.SERVER_CONNECTION_REGISTERED, rscp_type=RSCPType.Container)

                r += RSCPDTO(tag=RSCPTag.SERVER_CONNECTION_ID, rscp_type=RSCPType.Int64,
                             data=self.server_connection_id)
                r += RSCPDTO(tag=RSCPTag.SERVER_AUTH_LEVEL, rscp_type=RSCPType.UChar8,
                             data=self.server_auth_level)
                requests.append(r)

            if res.name == 'SERVER_UNREGISTER_CONNECTION':
                logger.debug(res.name)
                self.server_connection_id = None
                self.server_auth_level = None
                r = self.getWeblogin()
                requests += r

            elif res.name == 'SERVER_REQ_RSCP_CMD':
                if res['SERVER_RSCP_DATA']:
                    logger.debug(res.name)
                    p = []
                    rscp_data = res['SERVER_RSCP_DATA']

                    if self.next_response:
                        if isinstance(rscp_data.data, RSCPDTO):
                            self.next_response_data = rscp_data.data
                        else:
                            self.next_response_data = rscp_data
                        self.next_response = None
                    if 'INFO_SERIAL_NUMBER' in rscp_data:
                        self.info_serial_number = rscp_data['INFO_SERIAL_NUMBER'].data

                    if 'INFO_REQ_IP_ADDRESS' in rscp_data:
                        p.append(RSCPDTO(RSCPTag.INFO_IP_ADDRESS, rscp_type=RSCPType.CString, data='0.0.0.0'))
                    if 'INFO_REQ_SUBNET_MASK' in rscp_data:
                        p.append(RSCPDTO(RSCPTag.INFO_SUBNET_MASK, rscp_type=RSCPType.CString, data='0.0.0.0'))
                    if 'INFO_REQ_GATEWAY' in rscp_data:
                        p.append(RSCPDTO(RSCPTag.INFO_GATEWAY, rscp_type=RSCPType.CString, data='0.0.0.0'))
                    if 'INFO_REQ_DNS' in rscp_data:
                        p.append(RSCPDTO(RSCPTag.INFO_DNS, rscp_type=RSCPType.CString, data='0.0.0.0'))
                    if 'INFO_REQ_DHCP_STATUS' in rscp_data:
                        p.append(RSCPDTO(RSCPTag.INFO_DHCP_STATUS, rscp_type=RSCPType.Bool, data=False))

                    if 'INFO_REQ_TIME' in rscp_data:
                        # TODO: Zeitstempel korrekt bilden mit Berücksichtigung der Zeitzone
                        current_time = time.time()
                        seconds = math.ceil(current_time)
                        nanoseconds = round((current_time - int(current_time)) * 1000)
                        ts = struct.pack('<QI', seconds, nanoseconds)

                        p.append(RSCPDTO(RSCPTag.INFO_TIME, rscp_type=RSCPType.ByteArray, data=ts))
                    if 'INFO_REQ_TIME_ZONE' in rscp_data:
                        p.append(RSCPDTO(RSCPTag.INFO_TIME_ZONE, rscp_type=RSCPType.CString, data='GMT+2'))

                    if 'INFO_REQ_UTC_TIME' in rscp_data:
                        current_time = time.time() + 7200
                        seconds = math.ceil(current_time)
                        nanoseconds = round((current_time - int(current_time)) * 1000)
                        ts = struct.pack('<QI', seconds, nanoseconds)

                        p.append(RSCPDTO(RSCPTag.INFO_UTC_TIME, rscp_type=RSCPType.ByteArray, data=ts))

                    if 'INFO_REQ_A35_SERIAL_NUMBER' in rscp_data:
                        p.append(RSCPDTO(RSCPTag.INFO_A35_SERIAL_NUMBER, rscp_type=RSCPType.CString, data='123456'))

                    if 'INFO_REQ_INFO' in rscp_data:
                        info = RSCPDTO(RSCPTag.INFO_INFO, rscp_type=RSCPType.Container)
                        hsh = self.username + str(self.server_connection_id)
                        md5 = hashlib.md5(hsh.encode()).hexdigest()
                        info += RSCPDTO(RSCPTag.INFO_SERIAL_NUMBER, rscp_type=RSCPType.CString, data='WEB_' + md5)
                        info += RSCPDTO(RSCPTag.INFO_MAC_ADDRESS, rscp_type=RSCPType.CString, data='00:00:00:00:00:00')
                        p.append(info)

                    if len(p) > 0:
                        requests.append(self.getRSCPToServer(p))

            elif res.name == 'SERVER_REQ_PING':
                logger.debug(res.name)
                r = RSCPDTO(tag=RSCPTag.SERVER_PING)
                requests.append(r)

        return requests

    def getRSCPToServer(self, p):
        if not isinstance(p, list):
            p = [p]

        payload = b''
        for payload_element in p:
            if isinstance(payload_element, RSCPTag):
                x = RSCPDTO(payload_element)
            else:
                x = payload_element
            payload += self.rscp_utils.encode_data(x)

        payload = self.rscp_utils.encode_frame(payload)

        r = RSCPDTO(tag=RSCPTag.SERVER_REQ_RSCP_CMD, rscp_type=RSCPType.Container)
        r += RSCPDTO(tag=RSCPTag.SERVER_CONNECTION_ID, rscp_type=RSCPType.Int64, data=self.server_connection_id)
        r += RSCPDTO(tag=RSCPTag.SERVER_AUTH_LEVEL, rscp_type=RSCPType.UChar8, data=self.server_auth_level)
        r += RSCPDTO(tag=RSCPTag.SERVER_RSCP_DATA_LEN, rscp_type=RSCPType.Int32, data=len(payload))
        r += RSCPDTO(tag=RSCPTag.SERVER_RSCP_DATA, rscp_type=RSCPType.ByteArray, data=payload)
        return r

    def send_data(self, r, ws = None):
        if not ws:
            ws = self.ws
        dataframe = self.rscp_utils.encode_data(r)
        bindat = self.rscp_utils.encode_frame(dataframe, crc=True)
        logger.debug('Sende Daten ' + str(len(bindat)))
        ws.send(bindat, websocket.ABNF.OPCODE_BINARY)

    def start_ws(self):
        def on_message(ws, message):
            try:
                data = self.rscp_utils.decode_server_data(message)
                res = self.interpreter_serverdata(data)
                for r in res:
                    self.send_data(r, ws)

            except:
                traceback.print_exc()

        def on_error(ws, error):
            logger.info('Verbindungsfehler', error)

        def on_close(ws):
            logger.info('Verbindung geschlossen')

        #websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.url,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)

        self.ws = ws
        logger.debug('Starte Websocket-Verbindung mit ' + self.url)
        ws.run_forever()

    def __del__(self):
        self.ws.close()
