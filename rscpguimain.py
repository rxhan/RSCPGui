import logging

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
    logger.warning('Paho-Libary nicht gefunden, MQTT wird nicht zur Verfügung stehen')

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

    def __init__(self, args):
        logger.debug('Main initialisiert')
        self._args = args
        self.clear_values()
        self.ConfigFilename = 'rscpe3dc.conf.ini'
        self._config = None
        self._gui = None

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
        else:
            name = None
            kat = None

        if name and kat:
            if isinstance(value, list):
                value = ','.join(value)
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
        else:
            raise AttributeError('Wert ' + item + ' existiert nicht (get)')

        if kat in self.config:
            if kat == 'Login':
                if name in self._config[kat]:
                    if name == 'password' and self._config[kat][name][0] == '@':
                        return self.tinycode('rscpgui', self._config[kat][name][1:], True)
                    elif name == 'rscppassword' and self._config[kat][name][0] == '@':
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
                    if name in ('csv', 'json', 'mqtt', 'http', 'mqttretain'):
                        return True if self._config[kat][name].lower() in ('true', '1', 'ja') else False
                    elif name in ('mqttport', 'mqttqos', 'intervall'):
                        return int(self._config[kat][name])
                    elif name == 'paths':
                        return self._config[kat][name].split(',')
                    else:
                        return self._config[kat][name]
                else:
                    if name == 'mqttbroker':
                        return 'localhost'
                    elif name == 'mqttport':
                        return 1883
                    elif name == 'mqttpos':
                        return 0

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
            logger.debug("Ermittle beste Verbindungsart (Verbindungsart auto)")
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
                logger.debug('Teste direkte Verbindungsart')

                if not isinstance(testgui, E3DCGui):
                    testgui = E3DCGui(self.cfgLoginusername, self.cfgLoginpassword, address, self.cfgLoginrscppassword)

                try:
                    result = test_connection(testgui)
                    if not seriennummer:
                        seriennummer = repr(result['INFO_SERIAL_NUMBER'])
                    logger.info('Verwende Direkte Verbindung / Verbindung mit System ' + repr(
                        result['INFO_SERIAL_NUMBER']) + ' / ' + repr(result['INFO_IP_ADDRESS']))
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
                    logger.debug('Teste Web Verbindungsart')
                    testgui = E3DCWebGui(self.cfgLoginusername, self.cfgLoginpassword, seriennummer)
                    try:
                        result = test_connection(testgui)
                        if not address:
                            address = repr(result['INFO_IP_ADDRESS'])
                        logger.info('Verwende Web Verbindung / Verbindung mit System ' + repr(
                            result['INFO_SERIAL_NUMBER']) + ' / ' + repr(result['INFO_IP_ADDRESS']))
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
        logger.debug('Sammle Daten')
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
            logger.debug('Anonymisiere Daten')
            data = self.anonymize_data(data, anonymize, remove)
            logger.debug('Daten wurden anonymisiert')
        logger.debug('Datensammlung beendet')
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

    def StartAutoExport(self):
        def mqtt_connect(broker,port):
            logger.debug('Verbinde mit MQTT-Broker ' + broker + ':' + str(port))
            mqttclient = paho.Client("RSCPGui")
            mqttclient.connect(broker, port)
            return mqttclient

        try:
            logger.debug('Starte automatischen Export')
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

            mqttactive = self.cfgExportmqtt if 'paho' in sys.modules.keys() else False
            mqttbroker = self.cfgExportmqttbroker
            mqttport = self.cfgExportmqttport
            mqttqos = self.cfgExportmqttqos
            mqttretain = self.cfgExportmqttretain
            mqttclient = mqtt_connect(mqttbroker, mqttport) if mqttactive else None

            httpactive = self.cfgExporthttp
            httpurl = self.cfgExporthttpurl

            intervall = self.cfgExportintervall


            if csvactive:
                csvfile = open(csvfilename, 'a', newline='')
                fields = self.cfgExportpaths.copy()
                fields.insert(0,'datetime')
                fields.insert(0,'ts')
                csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
                csvwriter.writeheader()

            while self._AutoExportStarted:
                laststart = time.time()
                logger.debug('Exportiere Daten (autoexport)')
                try:
                    values = self.getUploadDataFromPath()
                    values['ts'] = time.time()
                    values['datetime'] = datetime.datetime.now().isoformat()
                    if csvactive:
                        try:
                            logger.debug('Exportiere in CSV-Datei ' + csvfilename)
                            csvwriter.writerow(values)
                            csvfile.flush()
                        except:
                            logger.exception('Fehler beim Export in CSV-Datei')

                    if jsonactive:
                        try:
                            logger.debug('Exportiere in JSON-Datei ' + jsonfilename)
                            with open(jsonfilename, 'w') as jsonfile:
                                json.dump(values, jsonfile)
                        except:
                            logger.exception('Fehler beim Export in JSON-Datei')

                    if mqttactive:
                        try:
                            logger.debug('Exportiere nach MQTT')
                            for key in values.keys():
                                if key not in ('ts', 'datetime'):
                                    topic = '/' + key
                                    res,mid = mqttclient.publish(topic, values[key], mqttqos, mqttretain)
                                    if res != 0:
                                        mqttclient.disconnect()
                                        logger.error('Fehler bei Export an MQTT bei Topic ' + topic + ' Errorcode: ' + str(res))
                                        mqttclient = mqtt_connect(mqttbroker, mqttport)
                        except:
                            logger.exception('Fehler beim Export nach MQTT')

                    if httpactive:
                        try:
                            logger.debug('Exportiere an Http-Url ' + httpurl)
                            r = requests.post(httpurl, json=values)
                            r.raise_for_status()
                            logger.debug('Export an URL Erfolgreich ' + str(r.status_code))
                            logger.debug('Response: ' + r.text)
                        except:
                            logger.exception('Fehler beim Export in Http')


                except:
                    logger.exception('Fehler beim Abruf der Exportdaten')

                diff = time.time() - laststart
                if diff < intervall:
                    wait = intervall - diff
                    logger.debug('Warte ' + str(wait) + 's')
                    time.sleep(wait)

            if csvactive:
                csvfile.close()


        except:
            logger.exception('Fehler beim automatischen Export')

        self._AutoExportStarted = False

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

        for path in self.cfgExportpaths:
            logger.debug('Ermittle Pfad aus ' + path)
            teile = path.split('/')
            if teile[0] == 'E3DC':
                if teile[1] == 'EMS_DATA':
                    try:
                        if not ems_data:
                            ems_data = self._fill_ems().asDict()

                        values[path] = getDataFromPath(teile[2:], ems_data)
                    except:
                        logger.exception('Fehler beim Abruf von EMS')
                elif teile[1] == 'BAT_DATA':
                    try:
                        if not bat_data:
                            bat_data = self.gui.get_data(self.gui.getBatDcbData(bat_index=int(teile[2])), True).asDict()
                        values[path] = getDataFromPath(teile[3:], bat_data)
                    except:
                        logger.exception('Fehler beim Abruf von BAT')
                elif teile[1] == 'INFO_DATA':
                    try:
                        if not info_data:
                            info_data = self._fill_info().asDict()
                        values[path] = getDataFromPath(teile[2:], info_data)
                    except:
                        logger.exception('Fehler beim Abruf von INFO')
                elif teile[1] == 'DCDC_DATA':
                    try:
                        if not dcdc_data:
                            dcdc_data = self.gui.get_data(self.gui.getDCDCData(dcdc_indexes=int(teile[2])), True).asDict()
                        values[path] = getDataFromPath(teile[3:], dcdc_data)
                    except:
                        logger.exception('Fehler beim Abruf von DCDC')
                elif teile[1] == 'PM_DATA':
                    try:
                        if not pm_data:
                            pm_data = self.gui.get_data(self.gui.getPMData(pm_index=int(teile[2])), True).asDict()
                        values[path] = getDataFromPath(teile[3:], pm_data)
                    except:
                        logger.exception('Fehler beim Abruf von PM')
                elif teile[1] == 'PVI_DATA':
                    try:
                        if not pvi_data:
                            pvi_data = self.gui.get_data(self.gui.getPVIData(pvi_index=int(teile[2])), True).asDict()
                        values[path] = getDataFromPath(teile[3:], pvi_data)
                    except:
                        logger.exception('Fehler beim Abruf von PVI')
                elif teile[1] == 'WB_DATA':
                    try:
                        if not wb_data:
                            wb_data = self.gui.get_data(self.gui.getWB(index=int(teile[2])), True).asDict()
                        values[path] = getDataFromPath(teile[3:], wb_data)
                    except:
                        logger.exception('Fehler beim Abruf von WB')
            else:
                logger.debug('Pfadangabe falsch: ' + path)

        return values

    def _fill_info(self):
        logger.debug('Rufe INFO-Daten ab')
        data = self.gui.get_data(self.gui.getInfo() + self.gui.getUpdateStatus(), True)
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
                logger.info('DCDC #' + str(index) + ' konnte nicht abgefragt werden.')

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
                logger.exception('PVI #' + str(index) + ' konnte nicht abgefragt werden.')

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
                logger.exception('Fehler beim Abruf von BAT #' + str(index))

        logger.debug('BAT-Daten abgerufen')

        return data

    def fill_bat(self):
        self._data_bat = self._fill_bat()

    def _fill_wb(self):
        ddata = []
        logger.debug('Rufe WB-Daten ab')
        if self.debug:
            from e3dc._rscp_utils import RSCPUtils
            import binascii
            r = RSCPUtils()
        try:
            if self.debug:
                t = 'e3dc0011ff41805f00000000a833bf1912001c10840e0e0b000100040e06040000000000bac1b748'
                bin = binascii.unhexlify(t)
                data = r.decode_data(bin)
            else:
                data = self.gui.get_data(self.gui.getWBCount(), True)
            if data.type == RSCPType.Error:
                raise RSCPCommunicationError('Error bei WB-Abruf', logger)
        except RSCPCommunicationError:
            logger.debug('Keine Wallbox vorhanden')
            return ddata

        for index in data:
            logger.debug('Rufe Daten für Wallbox #' + str(index.data) + ' ab')
            if self.debug:
                t = 'e3dc0011ff41805f00000000d006f01ac0020000840e0eb9020100040e05020000000400800e030100000100800e07040083b600000200800e070400e5b300000300800e05020004000400800e030100000500800e030100000600800e030100900700800e030100000800800e030100000900800e030100000a00800e05020000000b00800e030100000000860e0e18000100860e010100010200860e010100010300860e010100000c00800e0b0800000000a0467095400d00800e0b08000000006055b90f400e00800e0b08000000006055b90f400f00800e030100071100800e030100001200800e0b0800e801068d6e137d401300800e0b0800aa58ab3dcf79fc3f1400800e0b0800aa58ab3dcf79fc3f1500800e070400000000001600800e030100002900800e0e18003000800e010100013100800e010100013200800e010100001700800e0301000a1800800e070400000000001900800e070400102700001a00800e05020000001b00800e030100061c00800e030100e61d00800e030100001e00800e030100001f00800e05020000002000800e05020000002100800e05020000002200800e030100002300800e030100002400800e030100432500800e030100142600800e030100002700800e010100012800800e010100014000800e0b080000000000000000004200800e0d0c004561737920436f6e6e6563740010040eff0400070000001110840e0e1a001120040e060400080000001020040e1008006405e5b3000004001210840e0e1a001120040e060400080000001020040e10080000009e02000000001310840e0e1a001120040e060400080000001020040e100800640583b6000000041410840e0e1a001120040e060400080000001020040e1008000401b006000000001b10840e0e1a001120040e060400080000001020040e10080000000600000000001a10840e0e1a001120040e060400080000001020040e1008000000000000000000020d6f'
                bin = binascii.unhexlify(t)
                d = r.decode_data(bin)
            else:
                d = self.gui.get_data(self.gui.getWB(index=index.data), True)

            ddata.append(d)

        logger.debug('Abruf WB-Daten abgeschlossen')

        return ddata

    def fill_wb(self):
        self._data_wb = self._fill_wb()
