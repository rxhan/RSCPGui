import logging
import os
import traceback

from e3dc._rscp_dto import RSCPDTO

logger = logging.getLogger(__name__)

from socket import setdefaulttimeout
import csv
import re
import random
import base64
import hashlib
import configparser
import time
import json
import requests
import sys
import datetime
import threading
from e3dc._rscp_exceptions import RSCPCommunicationError
from e3dc.rscp_helper import rscp_helper
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType
from e3dcwebgui import E3DCWebGui

try:
    import paho.mqtt.client as paho
except:
    logger.warning('Paho-Libary (paho) nicht gefunden, MQTT wird nicht zur Verfügung stehen')

try:
    import influxdb
    from influxdb.exceptions import InfluxDBClientError
except:
    logger.warning('Influxdb-Libary nicht gefunden, Influx wird nicht zur Verfügung stehen')

try:
    import telegram
except Exception as e:
    logger.warning('Telegram-Libary (python-telegram-bot) nicht gefunden, Telegram-Benachrichtigungen stehen nicht zur Verfügung')

try:
    import thread
except ImportError:
    import _thread as thread

class E3DCGui(rscp_helper):
    pass

class RSCPGuiMain():
    _extsrcavailable = 0
    _gui = None
    _connected = None
    _mbsSettings = {}
    debug = False
    _AutoExportStarted = False
    _args = None
    _updateRunning = None
    _try_connect = False
    _notificationblocker = {}
    _mqttclient = None
    _exportcache = None

    def __init__(self, args):
        logger.info('Main initialisiert')
        self._args = args
        self.clear_values()
        self.ConfigFilename = 'rscpe3dc.conf.ini'

        self._config = None
        self._gui = None

        self._cached = {}

        setdefaulttimeout(2)

    def clear_values(self):
        self._data_bat = []
        self._data_dcdc = []
        self._data_ems = None
        self._data_info = None
        self._data_pvi = {}
        self._data_pm = {}
        self._data_wb = []

    def tinycode(self, key, text, reverse=False):
        "(de)crypt stuff"
        rand = random.Random(key).randrange

        if reverse:
            text = base64.b64decode(text.encode('utf-8')).decode('utf-8', 'ignore')
        text = ''.join([chr(ord(elem) ^ rand(256)) for elem in text])

        if not reverse:
            text = base64.b64encode(text.encode('utf-8')).decode('utf-8', 'ignore')

        return text

    def StartExport(self):
        self._AutoExportStarted = True
        self._autoexportthread = threading.Thread(target=self.StartAutoExport, args=())
        self._autoexportthread.start()

    @property
    def config(self):
        if self._config is None:
            logger.info('Lade Konfigurationsdatei ' + self.ConfigFilename)
            self._config = configparser.ConfigParser()
            self._config.read(self.ConfigFilename)

        return self._config

    def __setattr__(self, key, value):
        if len(key) > 8 and key[0:8] == 'cfgLogin':
            name = key[8:]
            kat = 'Login'
        elif len(key) > 9 and key[0:9] == 'cfgExport':
            name = key[9:]
            kat = 'Export'
        elif len(key) > 15 and key[0:15] == 'cfgNotification':
            name = key[15:]
            kat = 'Notification'
        else:
            name = None
            kat = None

        if name and kat:
            if isinstance(value, dict):
                self._cached[name + kat] = value
                newvalue = []
                for k in value.keys():
                    newvalue.append(k + '|' + value[k])
                value = ','.join(newvalue)

            if isinstance(value, list):
                self._cached[name + kat] = value
                value = ','.join(value)

            if isinstance(value, int):
                value = str(value)

            if kat not in self._config:
                self._config[kat] = {}


            self._config[kat][name] = value
        else:
            super(RSCPGuiMain, self).__setattr__(key, value)


    def __getattr__(self, item):
        if len(item) > 8 and item[0:8] == 'cfgLogin':
            name = item[8:]
            kat = 'Login'
        elif len(item) > 9 and item[0:9] == 'cfgExport':
            name = item[9:]
            kat = 'Export'
        elif len(item) > 15 and item[0:15] == 'cfgNotification':
            name = item[15:]
            kat = 'Notification'
        else:
            raise AttributeError('Wert ' + item + ' existiert nicht (get)')

        if kat in self.config:
            if kat == 'Login':
                if name in self._config[kat]:
                    if name == 'password' and self._config[kat][name] != '' and self._config[kat][name][0] == '@':
                        return self.tinycode('rscpgui', self._config[kat][name][1:], True)
                    elif name == 'rscppassword' and self._config[kat][name] != '' and self._config[kat][name][0] == '@':
                        return self.tinycode('rscpgui_rscppass', self._config[kat][name][1:], True)
                    else:
                        return self._config[kat][name]
                else:
                    if name == 'websocketaddr':
                        return 'wss://s10.e3dc.com/ws'
                    elif name == 'connectiontype':
                        return 'auto'
            elif kat == 'Export':
                if name in self._config[kat]:
                    if name in ('csv', 'json', 'mqtt', 'http', 'mqttretain', 'mqttinsecure', 'influx', 'mqttsub'):
                        return True if self._config[kat][name].lower() in ('true', '1', 'ja') else False
                    elif name in ('mqttport', 'mqttqos', 'intervall', 'influxport', 'influxtimeout'):
                        if self._config[kat][name] != '':
                            return int(self._config[kat][name])
                    elif name == 'paths':
                        #if kat + name not in self._cached:
                        self._cached[kat + name] = self._config[kat][name].split(',')
                        return self._cached[kat + name]
                    elif name == 'mqttpassword' and self._config[kat][name] != '' and self._config[kat][name][0] == '@':
                        return self.tinycode('rscpgui_mqttpass', self._config[kat][name][1:], True)
                    elif name == 'pathnames':
                        items = self._config[kat][name].split(',')
                        ret = {}
                        for item in items:
                            if item:
                                tmp = item.split('|')
                                if len(tmp) == 2:
                                    ret[tmp[0]] = tmp[1]
                        self._cached[kat + name] = ret

                        return self._cached[kat + name]
                    else:
                        return self._config[kat][name]
            elif kat == 'Notification':
                if name in self._config[kat]:
                    if name == 'telegramtoken' and self._config[kat][name] != '' and self._config[kat][name][0] == '@':
                        return self.tinycode('telegramtoken', self._config[kat][name][1:], True)
                    elif name in ('telegram'):
                        return True if self._config[kat][name].lower() in ('true', '1', 'ja') else False
                    else:
                        return self._config[kat][name]

        return None

    @property
    def connected(self):
        return self._connected

    @property
    def connectiontype(self):
        if isinstance(self._gui, E3DCGui):
            return 'direkt'
        elif isinstance(self._gui, E3DCWebGui):
            return 'web'
        else:
            return None

    @property
    def gui(self):
        if self._try_connect:
            while self._try_connect:
                time.sleep(0.1)

            if self.connected:
                return self._gui

        self._try_connect = True

        def test_connection(testgui):
            requests = []
            requests.append(RSCPTag.INFO_REQ_SERIAL_NUMBER)
            requests.append(RSCPTag.INFO_REQ_IP_ADDRESS)
            return testgui.get_data(requests, True)

        if self.cfgLoginusername and self.cfgLoginpassword and self.cfgLoginconnectiontype == 'auto':
            logger.info("Ermittle beste Verbindungsart (Verbindungsart auto)")
            seriennummer = self.cfgLoginseriennummer
            address = self.cfgLoginaddress
            testgui = None
            testgui_web = None
            if self.cfgLoginusername and self.cfgLoginpassword and not seriennummer:
                if self.cfgLoginusername and self.cfgLoginpassword and address and self.cfgLoginrscppassword:
                    try:
                        testgui = E3DCGui(self.cfgLoginusername, self.cfgLoginpassword, address,
                                          self.cfgLoginrscppassword)
                        seriennummer = repr(test_connection(testgui)['INFO_SERIAL_NUMBER'])
                    except:
                        pass

                if not seriennummer:
                    ret = self.getSerialnoFromWeb(self.cfgLoginusername, self.cfgLoginpassword)
                    if len(ret) == 1:
                        seriennummer = self.getSNFromNumbers(ret[0]['serialno'])

            if self.cfgLoginusername and self.cfgLoginpassword and self.cfgLoginrscppassword and seriennummer and not address and self.cfgLoginwebsocketaddr:
                logger.debug('Versuche IP-Adresse zu ermitteln')
                try:
                    testgui = E3DCWebGui(self.cfgLoginusername, self.cfgLoginpassword, seriennummer)
                    ip = repr(test_connection(testgui)['INFO_IP_ADDRESS'])
                    if ip:
                        address = ip
                        logger.debug('IP-Adresse konnte ermittelt werden: ' + ip)
                        testgui_web = testgui
                    else:
                        raise Exception('IP-Adresse konnte nicht ermittelt werden, kein Inahlt')
                except:
                    testgui = None
                    logger.exception('Bei der Ermittlung der IP-Adresse ist ein Fehler aufgetreten')

            if self.cfgLoginusername and self.cfgLoginpassword and address and self.cfgLoginrscppassword:
                logger.info('Teste direkte Verbindungsart')

                if not isinstance(testgui, E3DCGui):
                    testgui = E3DCGui(self.cfgLoginusername, self.cfgLoginpassword, address, self.cfgLoginrscppassword)

                try:
                    result = test_connection(testgui)
                    if not seriennummer:
                        seriennummer = repr(result['INFO_SERIAL_NUMBER'])
                    logger.info('Verwende Direkte Verbindung / Verbindung mit System ' + repr(
                        result['INFO_SERIAL_NUMBER']) + ' / ' + repr(result['INFO_IP_ADDRESS']))

                    self.serialnumber = result['INFO_SERIAL_NUMBER']
                except ConnectionResetError as e:
                    logger.warning(
                        "Direkte Verbindung fehlgeschlagen (Socket) error({0}): {1}".format(e.errno, e.strerror))
                    testgui = None
                except RSCPCommunicationError as e:
                    logger.warning("Direkte Verbindung fehlgeschlagen (RSCP)")
                    testgui = None
                except:
                    logger.exception('Fehler beim Aufbau der direkten Verbindung')
                    testgui = None

            if self.cfgLoginusername and self.cfgLoginpassword and seriennummer and self.cfgLoginwebsocketaddr and not testgui:
                if testgui_web:
                    logger.info('Verwende Web Verbindung')
                    testgui = testgui_web
                else:
                    logger.info('Teste Web Verbindungsart')
                    testgui = E3DCWebGui(self.cfgLoginusername, self.cfgLoginpassword, seriennummer)
                    try:
                        result = test_connection(testgui)
                        if not address:
                            address = repr(result['INFO_IP_ADDRESS'])
                        logger.info('Verwende Web Verbindung / Verbindung mit System ' + repr(
                            result['INFO_SERIAL_NUMBER']) + ' / ' + repr(result['INFO_IP_ADDRESS']))

                        self.serialnumber = result['INFO_SERIAL_NUMBER']
                    except:
                        logger.exception('Fehler beim Aufbau der Web Verbindung')
                        testgui = None

            if not testgui:
                logger.error('Es konnte keine Verbindungsart ermittelt werden')
            else:
                if self.cfgLoginseriennummer != seriennummer:
                    self.cfgLoginseriennummer = seriennummer
                    self.txtConfigSeriennummer.SetValue(seriennummer)

                if self.cfgLoginaddress != address:
                    self.cfgLoginaddress = address
                    self.txtIP.SetValue(address)

                self._gui = testgui
        elif self.cfgLoginusername and self.cfgLoginpassword and self.cfgLoginaddress and self.cfgLoginrscppassword and self.cfgLoginconnectiontype == 'direkt':
            testgui = E3DCGui(self.cfgLoginusername, self.cfgLoginpassword, self.cfgLoginaddress,
                              self.cfgLoginrscppassword)
            try:
                result = test_connection(testgui)
                self._gui = testgui
                logger.info('Verwende Direkte Verbindung')
            except:
                self._gui = None
        elif self.cfgLoginusername and self.cfgLoginpassword and self.cfgLoginseriennummer and self.cfgLoginwebsocketaddr and self.cfgLoginconnectiontype == 'web':
            testgui = E3DCWebGui(self.cfgLoginusername, self.cfgLoginpassword, self.cfgLoginseriennummer)
            try:
                result = test_connection(testgui)
                self._gui = testgui
                logger.info('Verwende Websocket')
            except:
                self._gui = None
        else:
            self._gui = None

        if not self._gui:
            logger.info('Kein Verbindungstyp kann verwendet werden, es fehlen Verbindungsdaten')

        self._try_connect = False
        return self._gui

    def getSNFromNumbers(self, sn):
        if sn[0:2] == '70':
            return 'P10-' + sn
        elif sn[0:2] == '60':
            return 'Q10-' + sn
        else:
            return 'S10-' + sn

    def getSerialnoFromWeb(self, username, password):
        logger.debug('Ermittle Seriennummer über Webzugriff')
        userlevel = None

        try:
            r = requests.post('https://s10.e3dc.com/s10/phpcmd/cmd.php', data={'DO': 'LOGIN',
                                                                               'USERNAME': username,
                                                                               'PASSWD': hashlib.md5(password.encode()).hexdigest(),
                                                                               'DENV': 'E3DC'})
            r.raise_for_status()
            r_json = r.json()
            if r_json['ERRNO'] != 0:
                raise Exception('Abfrage Fehlerhaft #1, Fehlernummer ' + str(r_json['ERRNO']))
            userlevel = int(r_json['CONTENT']['USERLEVEL'])
            cookies = r.cookies
            if userlevel in (1, 128):
                r = requests.post('https://s10.e3dc.com/s10/phpcmd/cmd.php', data={'DO': 'GETCONTENT',
                                                                                   'MODID': 'IDOVERVIEWCOMMONTABLE',
                                                                                   'ARG0': 'undefined',
                                                                                   'TOS': -7200,
                                                                                   'DENV': 'E3DC'}, cookies=cookies)
                r.raise_for_status()
                r_json = r.json()

                if r_json['ERRNO'] != 0:
                    raise Exception('Abfrage fehlerhaft #2, Fehlernummer ' + str(r_json['ERRNO']))

                content = r_json['CONTENT']
                html = None
                for lst in content:
                    if 'HTML' in lst:
                        html = lst['HTML']
                        break

                if not html:
                    raise Exception('Abfrage Fehlerhaft #3, Daten nicht gefunden')

                regex = r"s10list = '(\[\{.*\}\])';"

                try:
                    match = re.search(regex, html, re.MULTILINE).group(1)
                    obj = json.loads(match)
                    return obj
                except:
                    raise Exception('Abfrage Fehlerhaft #4, Regex nicht erfolgreich')

        except:
            logger.exception('Fehler beim Abruf der Seriennummer, Zugangsdaten fehlerhaft?')

        return []

    def updateData(self):
        if not self._updateRunning:
            self._updateRunning = True
            try:
                if self.gui:
                    logger.info('Aktualisiere Daten')
                    self.clear_values()

                    try:
                        self.fill_info()
                    except:
                        logger.exception('Fehler beim Abruf der INFO-Daten')

                    try:
                        self.fill_bat()
                    except:
                        logger.exception('Fehler beim Abruf der BAT-Daten')

                    try:
                        self.fill_dcdc()
                    except:
                        logger.exception('Fehler beim Abruf der DCDC-Daten')

                    try:
                        self.fill_pvi()
                    except:
                        logger.exception('Fehler beim Abruf der PVI-Daten')

                    try:
                        self.fill_ems()
                        self.fill_mbs()
                    except:
                        logger.exception('Fehler beim Abruf der EMS-Daten')

                    try:
                        self.fill_pm()
                    except:
                        logger.exception('Fehler beim Abruf der PM-Daten')

                    try:
                        self.fill_wb()
                    except:
                        logger.exception('Fehler beim Abruf der WB-Daten')

                    try:
                        self.fill_mbs()
                    except:
                        logger.exception('Fehler beim Abruf der Modbus-Daten')

                else:
                    logger.warning('Konfiguration unvollständig, Verbindung nicht möglich')

            except:
                logger.exception('Fehler beim Aktualisieren der Daten')
            self._updateRunning = False


    def sammle_data(self, anon = True):
        logger.info('Sammle Daten')
        self.updateData()

        anonymize = ['DCDC_SERIAL_NUMBER', 'INFO_MAC_ADDRESS', 'BAT_DCB_SERIALNO', 'BAT_DCB_SERIALCODE', 'INFO_SERIAL_NUMBER',
                     'INFO_A35_SERIAL_NUMBER', 'PVI_SERIAL_NUMBER', 'INFO_PRODUCTION_DATE']
        remove = ['INFO_IP_ADDRESS']
        data = {}
        if self._data_bat:
            data['BAT_DATA'] = []
            for d in self._data_bat:
                data['BAT_DATA'].append(d.asDict())

        if self._data_dcdc:
            data['DCDC_DATA'] = []
            for d in self._data_dcdc:
                data['DCDC_DATA'].append(d.asDict())

        if self._data_ems:
            data['EMS_DATA'] = self._data_ems.asDict()

        if self._data_info:
            data['INFO_DATA'] = self._data_info.asDict()

        if self._data_pvi:
            data['PVI_DATA'] = {}
            for k in self._data_pvi:
                d = self._data_pvi[k]
                data['PVI_DATA'][k] = d.asDict()

        if self._data_pm:
            data['PM_DATA'] = {}
            for k in self._data_pm:
                d = self._data_pm[k]
                data['PM_DATA'][k] = d.asDict()

        if self._data_wb:
            data['WB_DATA'] = []
            for d in self._data_wb:
                data['WB_DATA'].append(d.asDict())
        if anon:
            logger.info('Anonymisiere Daten')
            data = self.anonymize_data(data, anonymize, remove)
            logger.info('Daten wurden anonymisiert')
        logger.info('Datensammlung beendet')
        return data

    def anonymize_data(self, data, anonymize, remove):
        if isinstance(data, dict):
            toremove = []
            for i in data.keys():
                if isinstance(data[i], dict) or isinstance(data[i], list):
                    data[i] = self.anonymize_data(data[i], anonymize, remove)
                elif i in anonymize:
                    if isinstance(data[i], int) or isinstance(data[i], float):
                        data[i] = str(data[i])
                    if len(data[i]) >= 6:
                        tmp = 'X' * (len(data[i])-6)
                        data[i] = data[i][:6] + tmp
                    else:
                        data[i] = 'X' * len(data[i])
                elif i in remove:
                    toremove.append(i)

            for r in toremove:
                del data[r]
        elif isinstance(data, list):
            nl = []
            for i in data:
                nl += [self.anonymize_data(i, anonymize, remove)]
            data = nl
        return data

    def setMaxChargePower(self, value):
        temp = [RSCPDTO(tag=RSCPTag.EMS_MAX_CHARGE_POWER, rscp_type=RSCPType.Uint32, data=int(value))]
        r = [RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, rscp_type=RSCPType.Container, data=temp)]

        res = self.gui.get_data(r, True)
        logger.info('Wert über setMaxChargePower auf ' + str(value) + ' geändert')

    def setMaxDischargePower(self, value):
        temp = [RSCPDTO(tag=RSCPTag.EMS_MAX_DISCHARGE_POWER, rscp_type=RSCPType.Uint32, data=int(value))]
        r = [RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, rscp_type=RSCPType.Container, data=temp)]

        res = self.gui.get_data(r, True)
        logger.info('Wert über setMaxDischargePower auf ' + str(value) + ' geändert') \

    def setDischargeStartPower(self, value):
        temp = [RSCPDTO(tag=RSCPTag.EMS_DISCHARGE_START_POWER, rscp_type=RSCPType.Uint32, data=int(value))]
        r = [RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, rscp_type=RSCPType.Container, data=temp)]

        res = self.gui.get_data(r, True)
        logger.info('Wert über setDischageStartPower auf ' + str(value) + ' geändert') \

    @property
    def mqttclient(self):
        #TODO: Weitere Möglichkeiten ergänzen
        sublist = {
                    'E3DC/EMS_DATA/EMS_GET_POWER_SETTINGS/EMS_MAX_CHARGE_POWER': self.setMaxChargePower,
                    'E3DC/EMS_DATA/EMS_GET_POWER_SETTINGS/EMS_MAX_DISCHARGE_POWER': self.setMaxDischargePower,
                    'E3DC/EMS_DATA/EMS_GET_POWER_SETTINGS/EMS_DISCHARGE_START_POWER': self.setDischargeStartPower

        }

        def on_message(client, userdata, message):
            topic = message.topic[1:]
            if topic[-4:] == '/SET':
                topic = topic[:-4]
                if topic in self.cfgExportpathnames.values():
                    path = list(self.cfgExportpathnames.keys())[list(self.cfgExportpathnames.values()).index(topic)]
                    if path in sublist.keys():
                        callback = sublist[path]
                        value = str(message.payload.decode("utf-8"))
                        try:
                            test = int(self._exportcache[topic])
                            if test != value:
                                callback(value)
                            else:
                                logger.debug(topic + ' Wert hat sich nicht geändert ' + str(value) + ' <-> ' + str(test))
                        except:
                            logger.exception('Fehler bei ' + topic + ' (' + value + ')')

        if self._mqttclient is not None:
            if self._mqttclient.is_connected():
                return self._mqttclient

        self._mqttclient = None

        if self.cfgExportmqtt if 'paho' in sys.modules.keys() else False:
            broker = self.cfgExportmqttbroker
            port = self.cfgExportmqttport
            sub = self.cfgExportmqttsub
            username = self.cfgExportmqttusername
            password = self.cfgExportmqttpassword
            zertifikat = self.cfgExportmqttzertifikat
            insecure = self.cfgExportmqttinsecure

            logger.debug('Verbinde mit MQTT-Broker ' + broker + ':' + str(port))

            self._mqttclient = paho.Client("RSCPGui")

            if username and password:
                self._mqttclient.username_pw_set(username, password)

            if insecure and zertifikat:
                if os.path.isfile(zertifikat):
                    self._mqttclient.tls_set(ca_certs=zertifikat)
                    self._mqttclient.tls_insecure_set(insecure)

            self._mqttclient.enable_logger(logger)

            self._mqttclient.on_message=on_message
            self._mqttclient.connect(broker, port)
            if sub:
                for path in sublist.keys():
                    if path in self.cfgExportpathnames.keys():
                        topic = '/' + self.cfgExportpathnames[path] + '/SET'
                        logger.debug('MQTT Subscribe: ' + topic)
                        self._mqttclient.subscribe(topic)
            self._mqttclient.loop_start()

        return self._mqttclient

    def StartAutoExport(self):

        def influx_connect(influxhost, influxport, influxtimeout, influxdatenbank):
            logger.debug('Verbinde mit Influxdb ' + influxhost + ':' + str(influxport) + '/' + influxdatenbank)
            influxclient = influxdb.InfluxDBClient(host=influxhost, port=influxport, timeout=influxtimeout)
            influxclient.switch_database(influxdatenbank)

            return influxclient

        try:
            logger.info('Starte automatischen Export')
            if len(self.cfgExportpaths) > 0:
                logger.debug('Es sind ' + str(len(self.cfgExportpaths)) + ' Datenfelder zum Export vorgesehen')
            else:
                logger.debug('Es wurden keine Exporfelder definiert!')

            csvwriter = None
            csvfile = None

            csvactive = self.cfgExportcsv
            csvfilename = self.cfgExportcsvfile

            jsonactive = self.cfgExportjson
            jsonfilename = self.cfgExportjsonfile

            mqttqos = self.cfgExportmqttqos
            mqttretain = self.cfgExportmqttretain

            httpactive = self.cfgExporthttp
            httpurl = self.cfgExporthttpurl

            influxactive = self.cfgExportinflux if 'influxdb' in sys.modules.keys() else False
            influxhost = self.cfgExportinfluxhost
            influxport = self.cfgExportinfluxport
            influxdatenbank = self.cfgExportinfluxdatenbank
            influxtimeout = self.cfgExportinfluxtimeout
            influxname = self.cfgExportinfluxname
            influxclient = influx_connect(influxhost, influxport, influxtimeout, influxdatenbank) if influxactive else None

            intervall = self.cfgExportintervall

            notificationactive = False
            if 'telegram' in sys.modules.keys():
                if self.cfgNotificationtelegram is True:
                    if not self.cfgNotificationtelegramtoken or not self.cfgNotificationtelegramempfaenger:
                        logger.warning('Benachrichtigung an Telegram nicht möglich, Token oder Empfänger sind nicht gefüllt')
                    else:
                        self.notificationblocker = {}
                        notificationactive = True

            if csvactive:
                csvfile = open(csvfilename, 'a', newline='')
                fields: list = self.cfgExportpaths.copy()

                for key,val in enumerate(fields):
                    if val in self.cfgExportpathnames:
                        fields[key] = self.cfgExportpathnames[val]

                fields.insert(0,'datetime')
                fields.insert(0,'ts')
                csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
                csvwriter.writeheader()

            while self._AutoExportStarted:
                laststart = time.time()
                logger.debug('Exportiere Daten (autoexport)')
                try:
                    values, value_path = self.getUploadDataFromPath()
                    values['ts'] = time.time()
                    values['datetime'] = datetime.datetime.now().isoformat()
                    self._exportcache = values
                    if csvactive:
                        threading.Thread(target=self.exportCSV, args=(csvfilename, csvwriter, csvfile, values)).start()

                    if jsonactive:
                        threading.Thread(target=self.exportJson, args=(jsonfilename, values)).start()

                    if self.mqttclient is not None:
                        threading.Thread(target=self.exportMQTT, args=(mqttqos, mqttretain, values)).start()

                    if httpactive:
                        threading.Thread(target=self.exportHTTP, args=(httpurl, values)).start()

                    if influxactive:
                        threading.Thread(target=self.exportInflux, args=(influxclient, influxname,values)).start()

                    if notificationactive:
                        self.notify(value_path)
                        #threading.Thread(target=self.notify, args={values}).start()
                except:
                    logger.exception('Fehler beim Abruf der Exportdaten')

                diff = time.time() - laststart
                if diff < intervall:
                    wait = intervall - diff
                    logger.debug('Warte ' + str(wait) + 's')
                    time.sleep(wait)

            if self._mqttclient is not None:
                self._mqttclient.loop_stop()
                self._mqttclient.disconnect()

            if csvactive:
                csvfile.close()


        except:
            logger.exception('Fehler beim automatischen Export')

        self._AutoExportStarted = False

    def exportCSV(self, csvfilename, csvwriter, csvfile, values):
        logger.info('Exportiere in CSV-Datei ' + csvfilename)
        try:
            csvwriter.writerow(values)
            csvfile.flush()
            logger.debug('Export in CSV-Datei erfolgreich')
        except:
            logger.exception('Fehler beim Export in CSV-Datei')

    def exportHTTP(self, httpurl, values):
        try:
            logger.info('Exportiere an Http-Url ' + httpurl)
            r = requests.post(httpurl, json=values)
            r.raise_for_status()
            logger.debug('Export an URL erfolgreich ' + str(r.status_code))
            logger.debug('Response: ' + r.text)
        except:
            logger.exception('Fehler beim Export in Http')

    def exportMQTT(self, mqttqos, mqttretain, values):
        try:
            logger.info('Exportiere nach MQTT')
            for key in values.keys():
                if key not in ('ts', 'datetime'):
                    topic = '/' + key
                    res, mid = self.mqttclient.publish(topic, values[key], mqttqos, mqttretain)
                    if res != 0:
                        self.mqttclient.disconnect()

            logger.debug('Export an MQTT abgeschlossen')
        except:
            logger.exception('Fehler beim Export nach MQTT')

    def exportJson(self, jsonfilename, values):
        try:
            logger.info('Exportiere in JSON-Datei ' + jsonfilename)
            with open(jsonfilename, 'w') as jsonfile:
                json.dump(values, jsonfile)
            logger.debug('Export an JSON-Datei erfolgreich')
        except:
            logger.exception('Fehler beim Export in JSON-Datei')

    def exportInflux(self, influxclient, influxname, fields):
        try:
            logger.info('Exportiere an Influxdb')
            values = {}
            for key in fields.keys():
                if key not in ('ts', 'datetime'):
                    values[key] = fields[key]

            if len(values) > 0:
                write_points = [{'measurement': influxname, 'fields': values}]
                influxclient.write_points(write_points)

                logger.debug('Export an Influxdb erfolgreich')
            else:
                logger.warning('Keine Daten zur Übergabe an Influxdb zur Verfügung')
        except:
            logger.exception('Fehler beim Export an Influxdb')

    def notify(self, values):
        # path|datatype|expression|notificationservice|text|waittime(seconds)
        #[Notification / Rules]
        #1 = E3DC / EMS_DATA / EMS_POWER_GRID | int | {value} < -2000 | telegram | Einspeiseleistung > 2000
        #W({value}) | 3600


        def execute_rule(value, datatype, expression, text):
            try:
                if datatype in ('int', 'integer', 'smallint', 'uint', 'int16', 'int32', 'int64'):
                    value = int(value)
                elif datatype in ('float', 'numeric', 'double'):
                    value = float(value)
                elif datatype in ('str','string',''):
                    value = str(value)
            except:
                logger.exception('Datenkonvertierung in notify fehlgeschlagen: ' + str(value) + ' Datentyp: ' + datatype)

            expression = expression.format(value=str(value))
            logger.debug('Validiere Daten ' + expression )
            try:
                if eval(expression):
                    text = text.format(value=str(value))

                    return text
            except:
                logger.exception('Fehler beim Ausführen der Expression: ' + expression)

            return ''

        def send_telegram(text):
            logger.debug('Sende Nachricht über Telegram: ' + text)
            try:
                bot = telegram.Bot(token=self.cfgNotificationtelegramtoken)
                bot.send_message(chat_id=self.cfgNotificationtelegramempfaenger, text=text)
            except:
                logger.exception('Fehler beim versand einer Telegram-Benachrichtigung')

        logger.debug('Sende Benachrichtigungen')
        rules = self._config['Notification/Rules']
        for rule in rules:
            path,datatype,expression,service,text,waittime = rules[rule].split('|')
            waittime = float(waittime)
            telegramactive = service == 'telegram'

            block = False
            if waittime > 0:
                if rule in self._notificationblocker:
                    if time.time() - self._notificationblocker[rule] < waittime:
                        logger.debug('Benachrichtigung nicht verschickt, Wartezeit nicht abgelaufen ' + str(time.time() - self._notificationblocker[rule]) + 'ts < ' + str(waittime))
                        block = True

            if not block:
                if path in values:
                    if values[path] is not None:
                        logger.debug('Regel (' + rule + ') für Path ' + path + ' gefunden mit Value: ' + str(values[path]))
                        if waittime == -1:
                            if rule not in self._notificationblocker:
                                pass
                            elif self._notificationblocker[rule] != values[path]:
                                text = execute_rule(values[path], datatype, expression, text)
                                if text != '':
                                    if telegramactive:
                                        send_telegram(text)
                            else:
                                logger.debug('Keine Benachrichtigung für ' + path + ' verschickt, Wert hat sich nicht geändert ' + str(values[path]))

                            self._notificationblocker[rule] = values[path]

                        else:
                            text = execute_rule(values[path], datatype, expression, text)
                            if text != '':
                                self._notificationblocker[rule] = time.time()
                                if telegramactive:
                                    send_telegram(text)
                    else:
                        logger.warning('Wert für Pfad ' + path + ' konnte nicht ermittelt werden, überspringe Benachrichtigung')


    def getUploadDataFromPath(self):
        def getDataFromPath(teile, data):
            if data is not None:
                if isinstance(data, dict):
                    if teile[0] in data.keys():
                        if len(teile) == 1:
                            return data[teile[0]]
                        else:
                            return getDataFromPath(teile[1:], data[teile[0]])
                elif isinstance(data, list):
                    if data[int(teile[0])] is not None:
                        if len(teile) == 1:
                            return data[int(teile[0])]
                        else:
                            return getDataFromPath(teile[1:], data[int(teile[0])])
                else:
                    logger.warning('Element not Found ' + '/'.join(teile))

        ems_data = None
        bat_data = None
        info_data = None
        dcdc_data = None
        pm_data = None
        pvi_data = None
        wb_data = None

        values = {}
        value_path = {}

        for path in self.cfgExportpaths:
            logger.debug('Ermittle Pfad aus ' + path)
            teile = path.split('/')
            if teile[0] == 'E3DC':
                newvalue = None
                if teile[1] == 'EMS_DATA':
                    try:
                        if not ems_data:
                            ems_data = self._fill_ems().asDict()

                        newvalue = getDataFromPath(teile[2:], ems_data)
                    except:
                        logger.exception('Fehler beim Abruf von EMS')
                elif teile[1] == 'BAT_DATA':
                    try:
                        if not bat_data:
                            bat_data = self.gui.get_data(self.gui.getBatDcbData(bat_index=int(teile[2])), True).asDict()
                        newvalue = getDataFromPath(teile[3:], bat_data)
                    except:
                        logger.exception('Fehler beim Abruf von BAT')
                elif teile[1] == 'INFO_DATA':
                    try:
                        if not info_data:
                            info_data = self._fill_info().asDict()
                        newvalue = getDataFromPath(teile[2:], info_data)
                    except:
                        logger.exception('Fehler beim Abruf von INFO')
                elif teile[1] == 'DCDC_DATA':
                    try:
                        if not dcdc_data:
                            dcdc_data = self.gui.get_data(self.gui.getDCDCData(dcdc_indexes=int(teile[2])), True).asDict()
                        newvalue = getDataFromPath(teile[3:], dcdc_data)
                    except:
                        logger.exception('Fehler beim Abruf von DCDC')
                elif teile[1] == 'PM_DATA':
                    try:
                        if not pm_data:
                            pm_data = self.gui.get_data(self.gui.getPMData(pm_index=int(teile[2])), True).asDict()
                        newvalue = getDataFromPath(teile[3:], pm_data)
                    except:
                        logger.exception('Fehler beim Abruf von PM')
                elif teile[1] == 'PVI_DATA':
                    try:
                        if not pvi_data:
                            pvi_data = self.gui.get_data(self.gui.getPVIData(pvi_index=int(teile[2])), True).asDict()
                        newvalue = getDataFromPath(teile[3:], pvi_data)
                    except:
                        logger.exception('Fehler beim Abruf von PVI')
                elif teile[1] == 'WB_DATA':
                    try:
                        if not wb_data:
                            wb_data = self.gui.get_data(self.gui.getWB(index=int(teile[2])), True).asDict()
                        newvalue = getDataFromPath(teile[3:], wb_data)
                    except:
                        logger.exception('Fehler beim Abruf von WB')

                if path in self.cfgExportpathnames:
                    key = self.cfgExportpathnames[path]
                    if key == '':
                        key = path
                else:
                    key = path
                value_path[path] = newvalue
                values[key] = newvalue
            else:
                logger.debug('Pfadangabe falsch: ' + path)

        return values, value_path

    def _fill_info(self):
        logger.debug('Rufe INFO-Daten ab')

        requests = self.gui.getInfo() + self.gui.getUpdateStatus()
        requests+=self.gui.getInfoAdditional()

        data = self.gui.get_data(requests, True, waittime=0.05)

        logger.debug('Abruf INFO-Daten abgeschlossen')
        return data

    def fill_info(self):
        self._data_info = self._fill_info()

    def _fill_ems(self):
        logger.debug('Rufe EMS-Daten ab')
        self._extsrcavailable = 0
        data = self.gui.get_data(self.gui.getEMSData(), True)
        logger.debug('Abruf EMS-Daten abgeschlossen')
        return data

    def fill_ems(self):
        self._data_ems = self._fill_ems()

    def _fill_mbs(self):
        logger.debug('Rufe Modbus-Daten ab')
        data = self.gui.get_data(self.gui.getModbus(), True)
        logger.debug('Abruf Modbus-Daten abgeschlossen')
        return data

    def fill_mbs(self):
        self._data_mbs = self._fill_mbs()

    def _fill_dcdc(self):
        logger.debug('Rufe DCDC-Daten ab')
        data = []
        for index in [0, 1, 2, 3]:
            try:
                d = self.gui.get_data(self.gui.getDCDCData(dcdc_indexes=[index]), True)
                index = int(d['DCDC_INDEX'])
                data.append(d)

                logger.info('DCDC #' + str(index) + ' wurde erfolgreich abgefragt.')
            except:
                logger.debug('DCDC #' + str(index) + ' konnte nicht abgefragt werden.')

        return data

    def fill_dcdc(self):
        self._data_dcdc = self._fill_dcdc()

    def _fill_pvi(self):
        logger.debug('Rufe PVI-Daten ab')
        data = {}
        for index in range(0,4):
            try:
                data[index] = self.gui.get_data(self.gui.getPVIData(pvi_index=index), True)
                logger.info('PVI #' + str(index) + ' wurde erfolgreich abgefragt.')
            except:
                logger.debug('PVI #' + str(index) + ' konnte nicht abgefragt werden.')

        logger.debug('Abruf PVI-Daten abgeschlossen')

        return data

    def fill_pvi(self):
        self._data_pvi = self._fill_pvi()

    def _fill_pm(self):
        logger.debug('Rufe PM-Daten ab')
        data = {}

        if self._extsrcavailable >= 0:
            indexes = range(0,8)
        else:
            indexes = None

        for index in indexes:
            try:
                d = self.gui.get_data(self.gui.getPMData(pm_index=index), True)

                if 'PM_DEVICE_STATE' not in d or d['PM_DEVICE_STATE'].type != RSCPType.Error:
                    index = d['PM_INDEX'].data
                    data[index] = d
                    logger.info('PM #' + str(index) + ' erfolgreich abgerufen')
            except:
                logger.exception('PM #' + str(index) + ' konnte nicht abgerufen werden.')

        logger.debug('Abruf PM-Daten abgeschlossen')

        return data

    def fill_pm(self):
        self._data_pm = self._fill_pm()

    def _fill_bat(self):
        logger.debug('Rufe BAT-Daten ab')
        data = []
        for index in [0,1]:
            try:
                requests = self.gui.getBatDcbData(bat_index=index)
                if len(requests) > 0:
                    f = self.gui.get_data(requests, True)
                    data.append(f)
                    logger.info('Erfolgreich BAT #' + str(index) + ' abgerufen')
            except:
                logger.debug('Fehler beim Abruf von BAT #' + str(index))

        logger.debug('BAT-Daten abgerufen')

        return data

    def fill_bat(self):
        self._data_bat = self._fill_bat()

    def _fill_wb(self):
        ddata = []
        logger.debug('Rufe WB-Daten ab')
        try:
            data = self.gui.get_data(self.gui.getWBCount(), True)
            if data.type == RSCPType.Error:
                raise RSCPCommunicationError('Error bei WB-Abruf', logger, data)
        except RSCPCommunicationError:
            logger.info('Keine Wallbox vorhanden')
            return ddata

        for index in data:
            logger.debug('Rufe Daten für Wallbox #' + str(index.data) + ' ab')
            d = self.gui.get_data(self.gui.getWB(index=index.data), True)

            ddata.append(d)

        logger.debug('Abruf WB-Daten abgeschlossen')

        return ddata

    def fill_wb(self):
        self._data_wb = self._fill_wb()

    def deleteFromPortal(self):
        logger.info('Lösche Daten aus Portal')
        try:
            data = {}
            if not self._data_info:
                self._data_info = self._fill_info()
                if not self._data_info:
                    raise Exception('Abruf nicht möglich')

            sn = self._data_info['INFO_SERIAL_NUMBER'].data
            mac = self._data_info['INFO_MAC_ADDRESS'].data
            snmac = sn+mac
            system = hashlib.md5(snmac.encode()).hexdigest()

            url = 'https://pv.pincrushers.de/rscpgui/' + system
            logger.debug('Lösche Portaldaten mit URL ' + url)

            r = requests.delete(url)

            logger.debug('Http Status Code: ' + str(r.status_code))
            logger.debug('Response: ' + r.text)

            response = r.json()
            r.raise_for_status()

            logger.info('Daten erfolgreich aus Portal gelöscht')
            return response
        except:
            logger.exception('Daten konnte nicht aus dem Portal gelöscht werden')
            return None

    def sendToPortalMin(self):
        logger.info('Sende Daten an Portal')
        try:
            data = {}
            if not self._data_info:
                self._data_info = self._fill_info()
                if not self._data_info:
                    raise Exception('Abruf nicht möglich')
            if not self._data_bat:
                self._data_bat = self._fill_bat()
                if not self._data_bat:
                    raise Exception('Abruf nicht möglich')

            sn = self._data_info['INFO_SERIAL_NUMBER'].data
            mac = self._data_info['INFO_MAC_ADDRESS'].data
            snmac = sn+mac
            system = hashlib.md5(snmac.encode()).hexdigest()
            proddate = self._data_info['INFO_PRODUCTION_DATE'].data
            if len(proddate) == 16:
                proddate = proddate[3:10]
            data['productiondate'] = proddate
            data['release'] = self._data_info['INFO_SW_RELEASE'].data
            data['model'] = sn[0:6]

            data['bat'] = []

            for bat in self._data_bat:
                databat = {}
                databat['capacity'] = bat['BAT_SPECIFICATION']['BAT_SPECIFIED_CAPACITY'].data
                databat['dcb'] = []

                dcbcount = int(bat['BAT_DCB_COUNT'])
                dcbinfo = bat['BAT_DCB_INFO'] if dcbcount > 1 else [bat['BAT_DCB_INFO']]

                for dcb in dcbinfo:
                    datadcb = {}
                    datadcb['cyclecount'] = dcb['BAT_DCB_CYCLE_COUNT'].data
                    datadcb['soh'] = dcb['BAT_DCB_SOH'].data
                    datadcb['maxchargevoltage'] = dcb['BAT_DCB_MAX_CHARGE_VOLTAGE'].data
                    datadcb['endofdischarge'] = dcb['BAT_DCB_END_OF_DISCHARGE'].data
                    datadcb['manufacture'] = dcb['BAT_DCB_MANUFACTURE_NAME'].data
                    datadcb['type'] = dcb['BAT_DCB_DEVICE_NAME'].data

                    databat['dcb'].append(datadcb)

                data['bat'].append(databat)
            logger.debug('Daten: ' + json.dumps(data))

            url = 'https://pv.pincrushers.de/rscpgui/' + system
            logger.debug('Sende Portaldaten an url ' + url)

            r = requests.put(url, json = data)

            logger.debug('Http Status Code: ' + str(r.status_code))
            logger.debug('Response: ' + r.text)

            response = r.json()
            r.raise_for_status()

            logger.info('Daten erfolgreich an Portal übermittelt')
            return response
        except:
            logger.exception('Daten konnten nicht an das Portal übermittelt werden')
            return None



