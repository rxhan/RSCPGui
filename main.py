import configparser
import datetime
import hashlib
import json
import logging
import re
import threading
import time
import traceback

import pytz as pytz
import requests
import wx
import wx.dataview

from e3dc._rscp_dto import RSCPDTO
from e3dc._rscp_exceptions import RSCPCommunicationError
from e3dc.rscp_helper import rscp_helper
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType
from e3dcwebgui import E3DCWebGui
from gui import MainFrame

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

try:
    import thread
except ImportError:
    import _thread as thread


class E3DCGui(rscp_helper):
    pass

class MessageBox(wx.Dialog):
    def __init__(self, parent, title, value):
        wx.Dialog.__init__(self, parent, title=title)
        text = wx.TextCtrl(self, style=wx.TE_READONLY | wx.BORDER_NONE | wx.TE_MULTILINE)
        text.SetValue(value)
        text.SetBackgroundColour(self.GetBackgroundColour())
        self.ShowModal()
        self.Destroy()


class Frame(MainFrame):
    _serverApp = None
    _curpmcols = 0
    _extsrcavailable = 0
    _gui = None
    _time_format = '%d.%m.%Y %H:%M:%S.%f'

    def __init__(self, parent):
        self.clear_values()
        MainFrame.__init__(self, parent)

        self.ConfigFilename = 'rscpe3dc.conf.ini'

        for tz in pytz.all_timezones:
            self.cbTimezone.Append(str(tz))

        self.loadConfig()

        self.Bind(wx.EVT_BUTTON, self.bTestClick, self.bTest)
        self.Bind(wx.EVT_BUTTON, self.bSaveClick, self.bSave)
        self.Bind(wx.EVT_BUTTON, self.bUpdateClick, self.bUpdate)

        self.gDCB_row_voltages = None
        self.gDCB_row_temp = None

        self._gui = None

        self._wsthread = threading.Thread(target=self.check_e3dcwebgui, args=())
        self._wsthread.start()

        try:
            self.bUpdateClick(None)
        except:
            traceback.print_exc()

    def loadConfig(self):
        logger.info('Lade Konfigurationsdatei ' + self.ConfigFilename)

        config = configparser.ConfigParser()
        config.read(self.ConfigFilename)

        if 'Login' in config:

            if 'username' in config['Login']:
                self.txtUsername.SetValue(config['Login']['username'])
            if 'password' in config['Login']:
                self.txtPassword.SetValue(config['Login']['password'])
            if 'address' in config['Login']:
                self.txtIP.SetValue(config['Login']['address'])
            if 'rscppassword' in config['Login']:
                self.txtRSCPPassword.SetValue(config['Login']['rscppassword'])
            if 'seriennummer' in config['Login']:
                self.txtConfigSeriennummer.SetValue(config['Login']['seriennummer'])
            if 'websocketaddr' in config['Login']:
                self.txtConfigWebsocket.SetValue(config['Login']['websocketaddr'])

            if 'usewebsocket' in config['Login']:
                if config['Login']['usewebsocket'] in ('1','true','ja'):
                    usewebsocket = True
                else:
                    usewebsocket = False
                self.chConfigWebsocket.SetValue(usewebsocket)
                
        if self.txtConfigWebsocket.GetValue() == '':
            self.txtConfigWebsocket.SetValue('wss://s10.e3dc.com/ws')

    def saveConfig(self):
        logger.info('Speichere Konfigurationsdatei ' + self.ConfigFilename)

        config = configparser.ConfigParser()
        config.read(self.ConfigFilename)
        config['Login'] = {'username':self.txtUsername.GetValue(),
                           'password':self.txtPassword.GetValue(),
                           'address':self.txtIP.GetValue(),
                           'rscppassword':self.txtRSCPPassword.GetValue(),
                           'seriennummer':self.txtConfigSeriennummer.GetValue(),
                           'websocketaddr':self.txtConfigWebsocket.GetValue(),
                           'usewebsocket':'true' if self.chConfigWebsocket.GetValue() else 'false'}

        with open(self.ConfigFilename, 'w') as configfile:
            config.write(configfile)


    @property
    def gui(self):
        if self._gui:
            if self._username == self.txtUsername.GetValue() and self._password == self.txtPassword.GetValue() and \
                    self._address == self.txtIP.GetValue() and self._rscppass == self.txtRSCPPassword.GetValue() and \
                    self._seriennummer == self.txtConfigSeriennummer.GetValue() and self._websocketaddr == self.txtConfigWebsocket.GetValue() and \
                    self._usewebsocket == self.chConfigWebsocket.GetValue():
                return self._gui

        self._username = self.txtUsername.GetValue()
        self._password = self.txtPassword.GetValue()
        self._address = self.txtIP.GetValue()
        self._rscppass = self.txtRSCPPassword.GetValue()
        self._seriennummer = self.txtConfigSeriennummer.GetValue()
        self._websocketaddr = self.txtConfigWebsocket.GetValue()
        self._usewebsocket = self.chConfigWebsocket.GetValue()

        if isinstance(self._gui, E3DCWebGui):
            self._gui.e3dc.ws.close()

        if self._username and self._password and self._address and self._rscppass and not self._usewebsocket:
            self._gui = E3DCGui(self._username, self._password, self._address, self._rscppass)
            logger.info('Verwende Direkte Verbindung')
        elif self._username and self._password and self._seriennummer and self._websocketaddr and self._usewebsocket:
            self._gui = E3DCWebGui(self._username, self._password, self._seriennummer)
            logger.info('Verwende Websocket')
        else:
            self._gui = None
            logger.info('Kein Verbindungstyp kann verwendet werden, es fehlen Verbindungsdaten')

        self.gDCB_last_row = 28

        return self._gui

    def fill_info(self):
        d = self.gui.get_data(self.gui.getInfo() + self.gui.getUpdateStatus(), True)
        self._data_info = d

        self.txtProductionDate.SetValue(repr(d['INFO_PRODUCTION_DATE']))
        self.txtSerialnumber.SetValue(repr(d['INFO_SERIAL_NUMBER']))
        self.txtSwRelease.SetValue(repr(d['INFO_SW_RELEASE']))
        self.txtA35Serial.SetValue(repr(d['INFO_A35_SERIAL_NUMBER']))
        dd = datetime.datetime.utcfromtimestamp(float(d['INFO_TIME'].data))
        self.txtTime.SetValue(str(dd.strftime(self._time_format)))
        self.cbTimezone.SetValue(repr(d['INFO_TIME_ZONE']))
        dd = datetime.datetime.utcfromtimestamp(float(d['INFO_UTC_TIME'].data))
        self.txtTimeUTC.SetValue(str(dd))
        self.txtUpdateStatus.SetValue(repr(d['UM_UPDATE_STATUS']))
        self.txtIPAdress.SetValue(repr(d['INFO_IP_ADDRESS']))
        self.txtSubnetmask.SetValue(repr(d['INFO_SUBNET_MASK']))
        self.txtMacAddress.SetValue(repr(d['INFO_MAC_ADDRESS']))
        self.txtGateway.SetValue(repr(d['INFO_GATEWAY']))
        self.txtDNSServer.SetValue(repr(d['INFO_DNS']))
        self.chDHCP.SetValue(d['INFO_DHCP_STATUS'].data)
        self.chSRVIsOnline.SetValue(d['SRV_IS_ONLINE'].data)
        self.chSYSReboot.SetValue(d['SYS_IS_SYSTEM_REBOOTING'].data)
        self.txtRSCPUserLevel.SetValue(repr(d['RSCP_USER_LEVEL']))



    def bEMSUploadChangesOnClick( self, event ):
        r = []
        test = 1 if self.chEMSBatteryBeforeCarMode.GetValue() == False else 0
        if test != self._data_ems['EMS_BATTERY_BEFORE_CAR_MODE'].data:
            r.append(RSCPDTO(tag = RSCPTag.EMS_REQ_SET_BATTERY_BEFORE_CAR_MODE, rscp_type=RSCPType.UChar8, data=test))

        test = 0 if self.chEMSBatteryToCarMode.GetValue() == False else 1
        if test != self._data_ems['EMS_BATTERY_TO_CAR_MODE'].data:
            r.append(RSCPDTO(tag = RSCPTag.EMS_REQ_SET_BATTERY_TO_CAR_MODE, rscp_type=RSCPType.UChar8, data=test))

        temp = []

        test = self.chEMSPowerLimitsUsed.GetValue()
        if test != self._data_ems['EMS_GET_POWER_SETTINGS']['EMS_POWER_LIMITS_USED'].data:
            temp.append(RSCPDTO(tag=RSCPTag.EMS_POWER_LIMITS_USED, rscp_type=RSCPType.Bool, data=test))

        test = 1 if self.chEMSPowerSaveEnabled.GetValue() else 0
        if test != self._data_ems['EMS_GET_POWER_SETTINGS']['EMS_POWERSAVE_ENABLED'].data:
            temp.append(RSCPDTO(tag=RSCPTag.EMS_POWERSAVE_ENABLED, rscp_type=RSCPType.UChar8, data=test))

        test = 1 if self.chEMSWeatherRegulatedChargeEnabled.GetValue() else 0
        if test != self._data_ems['EMS_GET_POWER_SETTINGS']['EMS_WEATHER_REGULATED_CHARGE_ENABLED'].data:
            temp.append(RSCPDTO(tag=RSCPTag.EMS_WEATHER_REGULATED_CHARGE_ENABLED, rscp_type=RSCPType.UChar8, data=test))

        test = self.sEMSMaxChargePower.GetValue()
        if test != self._data_ems['EMS_GET_POWER_SETTINGS']['EMS_MAX_CHARGE_POWER'].data:
            temp.append(RSCPDTO(tag=RSCPTag.EMS_MAX_CHARGE_POWER, rscp_type=RSCPType.Uint32, data=test))

        test = self.sEMSMaxDischargePower.GetValue()
        if test != self._data_ems['EMS_GET_POWER_SETTINGS']['EMS_MAX_DISCHARGE_POWER'].data:
            temp.append(RSCPDTO(tag=RSCPTag.EMS_MAX_DISCHARGE_POWER, rscp_type=RSCPType.Uint32, data=test))

        test = self.sEMSMaxDischargeStartPower.GetValue()
        if test != self._data_ems['EMS_GET_POWER_SETTINGS']['EMS_DISCHARGE_START_POWER'].data:
            temp.append(RSCPDTO(tag=RSCPTag.EMS_DISCHARGE_START_POWER, rscp_type=RSCPType.Uint32, data=test))

        if len(temp) > 0:
            r.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, rscp_type = RSCPType.Container, data=temp))

        days = ['Mo','Di','Mi','Do','Fr','Sa','So']

        for idlePeriod in self._data_ems['EMS_GET_IDLE_PERIODS']['EMS_IDLE_PERIOD']:
            if idlePeriod['EMS_IDLE_PERIOD_TYPE'].data == 0:
                c = 'Charge'
            else:
                c = 'Discharge'

            day = days[int(idlePeriod['EMS_IDLE_PERIOD_DAY'])]
            von = 'tpEMS' + c + day + 'Von'
            bis = 'tpEMS' + c + day + 'Bis'
            ch = 'chEMS' + c + day

            ch_data = self.__getattribute__(ch).GetValue()
            von_data = self.__getattribute__(von).GetValue().split(':')
            if len(von_data) == 2:
                von_data_hour = int(von_data[0])
                von_data_minute = int(von_data[1])
            else:
                raise Exception('Dateneingabe im Feld ' + von + ' falsch')

            self.__getattribute__(bis).SetValue(str(idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_HOUR'].data).zfill(2) + ':' + str(idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_MINUTE'].data).zfill(2))

            bis_data = self.__getattribute__(bis).GetValue().split(':')
            if len(bis_data) == 2:
                bis_data_hour = int(bis_data[0])
                bis_data_minute = int(bis_data[1])
            else:
                raise Exception('Dateneingabe im Feld ' + bis + ' falsch')

            if idlePeriod['EMS_IDLE_PERIOD_ACTIVE'].data != ch_data or \
                    idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_HOUR'].data != von_data_hour or \
                    idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_MINUTE'].data != von_data_minute or \
                    idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_HOUR'].data != bis_data_hour or \
                    idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_MINUTE'].data != bis_data_minute:
                res = self.gui.setIdlePeriod(type = idlePeriod['EMS_IDLE_PERIOD_TYPE'].data,
                                       active = ch_data,
                                       day = idlePeriod['EMS_IDLE_PERIOD_DAY'].data,
                                       start = str(von_data_hour).zfill(2) + ':' + str(von_data_minute).zfill(2),
                                       end = str(bis_data_hour).zfill(2) + ':' + str(bis_data_minute).zfill(2))
                r += res

        if len(r) > 0:
            try:
                res = self.gui.get_data(r, True)
                wx.MessageBox('Übertragung abgeschlossen')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')
        else:
            res = wx.MessageBox('Es wurden keine Änderungen gemacht, aktuelle Einstellungen trotzdem übertragen?', 'Ladeeinstellungen speichern', wx.YES_NO)
            if res == wx.YES:
                test = 1 if self.chEMSBatteryBeforeCarMode.GetValue() == False else 0
                r.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_BATTERY_BEFORE_CAR_MODE, rscp_type=RSCPType.UChar8, data=test))

                test = 0 if self.chEMSBatteryToCarMode.GetValue() == False else 1
                r.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_BATTERY_TO_CAR_MODE, rscp_type=RSCPType.UChar8, data=test))

                temp = []

                test = self.chEMSPowerLimitsUsed.GetValue()
                temp.append(RSCPDTO(tag=RSCPTag.EMS_POWER_LIMITS_USED, rscp_type=RSCPType.Bool, data=test))

                test = 1 if self.chEMSPowerSaveEnabled.GetValue() else 0
                temp.append(RSCPDTO(tag=RSCPTag.EMS_POWERSAVE_ENABLED, rscp_type=RSCPType.UChar8, data=test))

                test = 1 if self.chEMSWeatherRegulatedChargeEnabled.GetValue() else 0
                temp.append(RSCPDTO(tag=RSCPTag.EMS_WEATHER_REGULATED_CHARGE_ENABLED, rscp_type=RSCPType.UChar8, data=test))

                test = self.sEMSMaxChargePower.GetValue()
                temp.append(RSCPDTO(tag=RSCPTag.EMS_MAX_CHARGE_POWER, rscp_type=RSCPType.Uint32, data=test))

                test = self.sEMSMaxDischargePower.GetValue()
                temp.append(RSCPDTO(tag=RSCPTag.EMS_MAX_DISCHARGE_POWER, rscp_type=RSCPType.Uint32, data=test))

                test = self.sEMSMaxDischargeStartPower.GetValue()
                temp.append(RSCPDTO(tag=RSCPTag.EMS_DISCHARGE_START_POWER, rscp_type=RSCPType.Uint32, data=test))

                r.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, rscp_type=RSCPType.Container, data=temp))

                try:
                    res = self.gui.get_data(r, True)
                    wx.MessageBox('Übertragung abgeschlossen')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')
        self.bUpdateClick(None)

    def fill_wb(self):
        d = self.gui.get_data(self.gui.getWB(), True)
        print(d)

    def fill_ems(self):
        self._extsrcavailable = 0
        d = self.gui.get_data(self.gui.getEMSData(), True)
        self._data_ems = d

        self.txtEMSPowerPV.SetValue(repr(d['EMS_POWER_PV']) + ' W')
        self.txtEMSPowerHome.SetValue(repr(d['EMS_POWER_HOME']) + ' W')
        self.txtEMSPowerBat.SetValue(repr(d['EMS_POWER_BAT']) + ' W')
        self.txtEMSPowerGrid.SetValue(repr(d['EMS_POWER_GRID']) + ' W')
        self.txtEMSPowerAdd.SetValue(repr(d['EMS_POWER_ADD']) + ' W')
        self.txtEMSAutarkie.SetValue(str(round(d['EMS_AUTARKY'],2)) + ' %')
        self.gEMSAutarkie.SetValue(int(round(d['EMS_AUTARKY'],0)))
        self.txtEMSSelfConsumption.SetValue(str(round(d['EMS_SELF_CONSUMPTION'],2)) + ' %')
        self.gEMSSelfConsumption.SetValue(int(round(d['EMS_SELF_CONSUMPTION'],0)))
        self.txtEMSBatSoc.SetValue(str(round(d['EMS_BAT_SOC'],2)) + ' %')
        self.mgEMSBatSoc.SetValue(round(d['EMS_BAT_SOC'],0))
        self.txtEMSCouplingMode.SetValue(repr(d['EMS_COUPLING_MODE']))
        self.txtEMSMode.SetValue(repr(d['EMS_MODE']))
        if d['EMS_BATTERY_BEFORE_CAR_MODE'].data == 1:
            self.chEMSBatteryBeforeCarMode.SetValue(False)
        else:
            self.chEMSBatteryBeforeCarMode.SetValue(True)
        if d['EMS_BATTERY_TO_CAR_MODE'].data == 1:
            self.chEMSBatteryToCarMode.SetValue(True)
        else:
            self.chEMSBatteryToCarMode.SetValue(False)
        balancedphases = "{0:b}".format(d['EMS_BALANCED_PHASES'].data).replace('1','X ').replace('0','0 ')

        self.txtEMSBalancedPhases.SetValue(balancedphases)
        self.txtEMSExtSrcAvailable.SetValue(repr(d['EMS_EXT_SRC_AVAILABLE']))
        self._extsrcavailable = d['EMS_EXT_SRC_AVAILABLE'].data
        self.txtEMSInstalledPeakPower.SetValue(repr(d['EMS_INSTALLED_PEAK_POWER']) + ' Wp')
        self.txtEMSDerateAtPercent.SetValue(str(round(d['EMS_DERATE_AT_PERCENT_VALUE'],3)*100) + ' %')
        self.txtEMSDerateAtPower.SetValue(repr(d['EMS_DERATE_AT_POWER_VALUE']) + ' W')
        self.txtEMSUsedChargeLimit.SetValue(repr(d['EMS_USED_CHARGE_LIMIT']) + ' W')
        self.txtEMSUserChargeLimit.SetValue(repr(d['EMS_USER_CHARGE_LIMIT']) + ' W')
        self.txtEMSBatChargeLimit.SetValue(repr(d['EMS_BAT_CHARGE_LIMIT']) + ' W')
        self.txtEMSDCDCChargeLimit.SetValue(repr(d['EMS_DCDC_CHARGE_LIMIT']) + ' W')
        self.txtEMSRemainingBatChargePower.SetValue(repr(d['EMS_REMAINING_BAT_CHARGE_POWER']) + ' W')
        self.txtEMSUsedDischargeLimit.SetValue(repr(d['EMS_USED_DISCHARGE_LIMIT']) + ' W')
        self.txtEMSUserDischargeLimit.SetValue(repr(d['EMS_USER_DISCHARGE_LIMIT']) + ' W')
        self.txtEMSBatDischargeLimit.SetValue(repr(d['EMS_BAT_DISCHARGE_LIMIT']) + ' W')
        self.txtEMSDCDCDischargeLimit.SetValue(repr(d['EMS_DCDC_DISCHARGE_LIMIT']) + ' W')
        self.txtEMSRemainingBatDischargePower.SetValue(repr(d['EMS_REMAINING_BAT_DISCHARGE_POWER']) + ' W')
        self.txtEMSEmergencyPowerStatus.SetValue(repr(d['EMS_EMERGENCY_POWER_STATUS']))
        self.chEMSPowerLimitsUsed.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_POWER_LIMITS_USED'].data)
        self.chEMSPowerSaveEnabled.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_POWERSAVE_ENABLED'].data)
        self.chEMSWeatherRegulatedChargeEnabled.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_WEATHER_REGULATED_CHARGE_ENABLED'].data)
        self.txtEMSStatus.SetValue(repr(d['EMS_STATUS']))
        eptest = d['EMS_EMERGENCYPOWER_TEST_STATUS']['EMS_EPTEST_RUNNING'].data
        if eptest:
            self.bEMSEPTest.Enable(False)
        else:
            self.bEMSEPTest.Enable(True)
        self.chEMSEPTestRunning.SetValue(eptest)
        self.txtEMSEPTestCounter.SetValue(repr(d['EMS_EMERGENCYPOWER_TEST_STATUS']['EMS_EPTEST_START_COUNTER']))
        self.txtEMSEPTestTimestamp.SetValue(repr(d['EMS_EMERGENCYPOWER_TEST_STATUS']['EMS_EPTEST_NEXT_TESTSTART']))

        self.txtEMSPowerWBAll.SetValue(repr(d['EMS_POWER_WB_ALL']) + ' W')
        self.txtEMSPowerWBSolar.SetValue(repr(d['EMS_POWER_WB_SOLAR']) + ' W')
        self.chEMSAlive.SetValue(d['EMS_ALIVE'].data)

        manChargeActive = d['EMS_GET_MANUAL_CHARGE']['EMS_MANUAL_CHARGE_ACTIVE'].data

        self.chEMSGetManualCharge.SetValue(manChargeActive)
        if manChargeActive:
            self.bEMSManualChargeStart.Enable(False)
        else:
            self.bEMSManualChargeStart.Enable(True)

        startcounter = d['EMS_GET_MANUAL_CHARGE']['EMS_MANUAL_CHARGE_START_COUNTER'].data/1000
        dd = datetime.datetime.fromtimestamp(startcounter)
        self.txtEMSManualChargeStartCounter.SetValue(dd.strftime(self._time_format))

        self.txtEMSManualChargeEnergyCounter.SetValue(str(round(d['EMS_GET_MANUAL_CHARGE']['EMS_MANUAL_CHARGE_ENERGY_COUNTER'],5)) + ' kWh') # TODO: Einheit anfügen

        laststart = d['EMS_GET_MANUAL_CHARGE']['EMS_MANUAL_CHARGE_LASTSTART'].data
        dd = datetime.datetime.fromtimestamp(laststart)
        self.txtEMSManualChargeLaststart.SetValue(dd.strftime(self._time_format))

        for sysspec in d['EMS_GET_SYS_SPECS']['EMS_SYS_SPEC']:
            if sysspec['EMS_SYS_SPEC_NAME'].data == 'hybridModeSupported':
                self.txtEMSHybridModeSupported.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'] .data== 'installedBatteryCapacity':
                self.txtEMSInstalledBatteryCapacity.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxAcPower':
                self.txtEMSMaxAcPower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxBatChargePower':
                self.txtEMSMaxBatChargePower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxBatDischargPower':
                self.txtEMSMaxBatDischargePower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxChargePower':
                self.txtEMSMaxChargePowerSys.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxDischargePower':
                self.txtEMSMaxDischargePowerSys.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxFbcChargePower':
                self.txtEMSMaxFbcDischargePower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxPvPower':
                self.txtEMSMaxPVPower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxStartChargePower':
                self.txtEMSMaxStartChargePower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
                maxStartChargePower = int(sysspec['EMS_SYS_SPEC_VALUE_INT'])
                self.sEMSMaxChargePower.Max = maxStartChargePower
                self.sEMSMaxDischargeStartPower.Max = maxStartChargePower
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxStartDischargePower':
                self.txtEMSMaxStartDischargePower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
                maxStartDischargePower = int(sysspec['EMS_SYS_SPEC_VALUE_INT'])
                self.sEMSMaxDischargePower.Max = maxStartDischargePower
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'minStartChargePower':
                self.txtEMSMinStartChargePower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
                minStartChargePower = int(sysspec['EMS_SYS_SPEC_VALUE_INT'])
                self.sEMSMaxChargePower.Min = minStartChargePower
                self.sEMSMaxDischargeStartPower.Min = minStartChargePower
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'minStartDischargePower':
                self.txtEMSMinStartDischargePower.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
                minStartDischargePower = int(sysspec['EMS_SYS_SPEC_VALUE_INT'])
                self.sEMSMaxDischargePower.Min = minStartDischargePower
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'recommendedMinChargeLimit':
                self.txtEMSRecommendedMinChargeLimit.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'recommendedMinDischargeLimit':
                self.txtEMSRecommendedMinDischargeLimit.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'startChargeDefault':
                self.txtEMSstartChargeDefault.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'startDischargeDefault':
                self.txtEMSstartDischargeDefault.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))

        self.sEMSMaxChargePower.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_CHARGE_POWER'].data)
        self.txtEMSMaxChargePower.SetValue(repr(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_CHARGE_POWER']) + ' W')
        self.sEMSMaxDischargePower.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_DISCHARGE_POWER'].data)
        self.txtEMSMaxDischargePower.SetValue(repr(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_DISCHARGE_POWER']) + ' W')
        self.sEMSMaxDischargeStartPower.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_DISCHARGE_START_POWER'].data)
        self.txtEMSMaxDischargeStartPower.SetValue(repr(d['EMS_GET_POWER_SETTINGS']['EMS_DISCHARGE_START_POWER']) + ' W')

        self.chEPIsland.SetValue(d['EP_IS_ISLAND_GRID'].data)
        self.chEPReadyForSwitch.SetValue(d['EP_IS_READY_FOR_SWITCH'].data)
        self.chEPISGridConnected.SetValue(d['EP_IS_GRID_CONNECTED'].data)
        self.chEPPossible.SetValue(d['EP_IS_POSSIBLE'].data)
        self.chEPInvalid.SetValue(d['EP_IS_INVALID_STATE'].data)

        days = ['Mo','Di','Mi','Do','Fr','Sa','So']

        for idlePeriod in d['EMS_GET_IDLE_PERIODS']['EMS_IDLE_PERIOD']:
            if idlePeriod['EMS_IDLE_PERIOD_TYPE'].data == 0:
                c = 'Charge'
            else:
                c = 'Discharge'

            day = days[int(idlePeriod['EMS_IDLE_PERIOD_DAY'])]
            von = 'tpEMS' + c + day + 'Von'
            bis = 'tpEMS' + c + day + 'Bis'
            ch = 'chEMS' + c + day

            self.__getattribute__(ch).SetValue(idlePeriod['EMS_IDLE_PERIOD_ACTIVE'].data)
            self.__getattribute__(von).SetValue(str(idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_HOUR'].data).zfill(2) + ':' + str(idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_MINUTE'].data).zfill(2))
            self.__getattribute__(bis).SetValue(str(idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_HOUR'].data).zfill(2) + ':' + str(idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_MINUTE'].data).zfill(2))

    def sEMSMaxChargePowerOnScroll(self, event):
        self.txtEMSMaxChargePower.SetValue(str(self.sEMSMaxChargePower.GetValue()) + ' W')

    def sEMSMaxDischargePowerOnScroll(self, event):
        self.txtEMSMaxDischargePower.SetValue(str(self.sEMSMaxDischargePower.GetValue()) + ' W')

    def sEMSMaxDischargeStartPowerOnScroll(self, event):
        self.txtEMSMaxDischargeStartPower.SetValue(str(self.sEMSMaxDischargeStartPower.GetValue()) + ' W')

    def fill_pm(self):
        def get_einheit(value):
            if abs(value) > 10000:
                if abs(value) > 10000000:
                    return value / 1000000, 'MWh'
                else:
                    return value / 1000, 'kWh'
            else:
                return value, 'Wh'

        if self._extsrcavailable >= 0:
            indexes = range(0,8)
        else:
            indexes = None

        self._curpmcols = -1
        self.gPM.DeleteCols()

        for index in indexes:
            try:
                d = self.gui.get_data(self.gui.getPMData(pm_index=index), True)
                self._data_pm.append(d)
                if 'PM_DEVICE_STATE' not in d or d['PM_DEVICE_STATE'].type != RSCPType.Error:
                    index = d['PM_INDEX'].data
                    if index > self._curpmcols:
                        if index >= self.gPM.GetNumberCols():
                            self.gPM.AppendCols(1)
                        self.gPM.SetColLabelValue(index, 'LM #' + str(index))
                        self._curpmcols += 1
                    self.gPM.SetCellValue(0, index, str(round(d['PM_POWER_L1'], 3)) + ' W')
                    self.gPM.SetCellValue(1, index, str(round(d['PM_POWER_L2'], 3)) + ' W')
                    self.gPM.SetCellValue(2, index, str(round(d['PM_POWER_L3'], 3)) + ' W')
                    self.gPM.SetCellValue(3, index, str(round(d['PM_POWER_L1'].data+d['PM_POWER_L2'].data+d['PM_POWER_L3'].data, 3)) + ' W')
                    self.gPM.SetCellValue(4, index, str(round(d['PM_VOLTAGE_L1'], 3)) + ' V')
                    self.gPM.SetCellValue(5, index, str(round(d['PM_VOLTAGE_L2'], 3)) + ' V')
                    self.gPM.SetCellValue(6, index, str(round(d['PM_VOLTAGE_L3'], 3)) + ' V')

                    energy, einheit = get_einheit(d['PM_ENERGY_L1'].data)
                    self.gPM.SetCellValue(7, index, str(round(energy, 3)) + ' ' + einheit)
                    energy, einheit = get_einheit(d['PM_ENERGY_L2'].data)
                    self.gPM.SetCellValue(8, index, str(round(energy, 3)) + ' ' + einheit)
                    energy, einheit = get_einheit(d['PM_ENERGY_L3'].data)
                    self.gPM.SetCellValue(9, index, str(round(energy, 3)) + ' ' + einheit)
                    energy, einheit = get_einheit(d['PM_ENERGY_L1'].data+d['PM_ENERGY_L2'].data+d['PM_ENERGY_L3'].data)
                    self.gPM.SetCellValue(10, index, str(round(energy, 3)) + ' ' + einheit)

                    self.gPM.SetCellValue(11, index, repr(d['PM_FIRMWARE_VERSION']))
                    self.gPM.SetCellValue(12, index, repr(d['PM_ACTIVE_PHASES']))
                    self.gPM.SetCellValue(13, index, repr(d['PM_MODE']))
                    self.gPM.SetCellValue(14, index, repr(d['PM_ERROR_CODE']))
                    self.gPM.SetCellValue(15, index, repr(d['PM_TYPE']))
                    self.gPM.SetCellValue(16, index, repr(d['PM_DEVICE_ID']))
                    self.gPM.SetCellValue(17, index, repr(d['PM_IS_CAN_SILENCE']))
                    self.gPM.SetCellValue(28, index, repr(d['PM_DEVICE_STATE']['PM_DEVICE_CONNECTED']))
                    self.gPM.SetCellValue(29, index, repr(d['PM_DEVICE_STATE']['PM_DEVICE_WORKING']))
                    self.gPM.SetCellValue(30, index, repr(d['PM_DEVICE_STATE']['PM_DEVICE_IN_SERVICE']))

                    if 'PM_COMM_STATE' in d:
                        d = d['PM_COMM_STATE']
                        self.gPM.SetCellValue(18, index, repr(d['PM_CS_START_TIME']))
                        self.gPM.SetCellValue(19, index, repr(d['PM_CS_LAST_TIME']))
                        self.gPM.SetCellValue(20, index, repr(d['PM_CS_SUCC_FRAMES_ALL']))
                        self.gPM.SetCellValue(21, index, repr(d['PM_CS_SUCC_FRAMES_100']))
                        self.gPM.SetCellValue(22, index, repr(d['PM_CS_EXP_FRAMES_ALL']))
                        self.gPM.SetCellValue(23, index, repr(d['PM_CS_EXP_FRAMES_100']))
                        self.gPM.SetCellValue(24, index, repr(d['PM_CS_ERR_FRAMES_ALL']))
                        self.gPM.SetCellValue(25, index, repr(d['PM_CS_ERR_FRAMES_100']))
                        self.gPM.SetCellValue(26, index, repr(d['PM_CS_UNK_FRAMES']))
                        self.gPM.SetCellValue(27, index, repr(d['PM_CS_ERR_FRAME']))

                    logger.info('PM #' + str(index) + ' erfolgreich abgerufen')
            except:
                logger.exception('PM #' + str(index) + ' konnte nicht abgerufen werden.')

        self.gPM.AutoSize()

    def fill_dcdc(self):
        for index in [0,1,2,3]:
            try:
                data = self.gui.get_data(self.gui.getDCDCData(dcdc_indexes=[index]), True)
                self._data_dcdc.append(data)
                d = data

                index = int(d['DCDC_INDEX'])

                self.gDCDC.SetCellValue(0,index, str(round(d['DCDC_I_BAT'].data,5)) + ' A')
                self.gDCDC.SetCellValue(1,index, str(round(d['DCDC_U_BAT'].data,2)) + ' V')
                self.gDCDC.SetCellValue(2,index, str(round(d['DCDC_P_BAT'].data,2)) + ' W')
                self.gDCDC.SetCellValue(3,index, str(round(d['DCDC_I_DCL'].data,5)) + ' A')
                self.gDCDC.SetCellValue(4,index, str(round(d['DCDC_U_DCL'].data,2)) + ' V')
                self.gDCDC.SetCellValue(5,index, str(round(d['DCDC_P_DCL'].data,2)) + ' W')
                self.gDCDC.SetCellValue(6,index, repr(d['DCDC_FIRMWARE_VERSION']))
                self.gDCDC.SetCellValue(7,index, repr(d['DCDC_FPGA_FIRMWARE']))
                self.gDCDC.SetCellValue(8,index, repr(d['DCDC_SERIAL_NUMBER']))
                self.gDCDC.SetCellValue(9,index, str(repr(d['DCDC_BOARD_VERSION'])))
                self.gDCDC.SetCellValue(10,index, repr(d['DCDC_STATUS_AS_STRING']['DCDC_STATE_AS_STRING']))
                self.gDCDC.SetCellValue(11,index, repr(d['DCDC_STATUS_AS_STRING']['DCDC_SUBSTATE_AS_STRING']))
                logger.info('DCDC #' + str(index) + ' wurde erfolgreich abgefragt.')
            except:
                logger.exception('DCDC #' + str(index) + ' konnte nicht abgefragt werden.')

        self.gDCDC.AutoSizeColumns()

    def fill_pvi(self):
        data = self.gui.get_data(self.gui.getPVIData(), True)
        self._data_pvi = data

        self.txtPVISerialNumber.SetValue(repr(data['PVI_SERIAL_NUMBER']))
        self.txtPVIType.SetValue(repr(data['PVI_TYPE']))
        self.txtPVIVersionMain.SetValue(repr(data['PVI_VERSION']['PVI_VERSION_MAIN']))
        self.txtPVIVersionPic.SetValue(repr(data['PVI_VERSION']['PVI_VERSION_PIC']))
        self.txtPVITempCount.SetValue(repr(data['PVI_TEMPERATURE_COUNT']))
        self.chPVIOnGrid.SetValue(data['PVI_ON_GRID'].data)
        self.txtPVIStatus.SetValue(repr(data['PVI_STATE']))
        self.txtPVILastError.SetValue(repr(data['PVI_LAST_ERROR']))
        self.chPVICosPhiActive.SetValue(data['PVI_COS_PHI']['PVI_COS_PHI_IS_AKTIV'].data)
        self.txtPVICosPhiValue.SetValue(repr(data['PVI_COS_PHI']['PVI_COS_PHI_VALUE']))
        self.txtPVICosPhiExcited.SetValue(repr(data['PVI_COS_PHI']['PVI_COS_PHI_EXCITED']))
        self.txtPVIVoltageTrTop.SetValue(repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_THRESHOLD_TOP']))
        self.txtPVIVoltageTrBottom.SetValue(repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_THRESHOLD_BOTTOM']))
        self.txtPVIVoltageSlUp.SetValue(repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_SLOPE_UP']))
        self.txtPVIVoltageSlDown.SetValue(repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_SLOPE_DOWN']))
        self.txtPVIPowerMode.SetValue(repr(data['PVI_POWER_MODE']))
        self.txtPVISystemMode.SetValue(repr(data['PVI_SYSTEM_MODE']))
        self.txtPVIMaxTemperature.SetValue(repr(data['PVI_MAX_TEMPERATURE']['PVI_VALUE']))
        self.txtPVIMinTemperature.SetValue(repr(data['PVI_MIN_TEMPERATURE']['PVI_VALUE']))
        self.txtPVIMaxApparentpower.SetValue(repr(data['PVI_AC_MAX_APPARENTPOWER']['PVI_VALUE']))
        self.txtPVIFreqMin.SetValue(repr(data['PVI_FREQUENCY_UNDER_OVER']['PVI_FREQUENCY_UNDER']))
        self.txtPVIMaxFreq.SetValue(repr(data['PVI_FREQUENCY_UNDER_OVER']['PVI_FREQUENCY_OVER']))

        self.chPVIDeviceConnected.SetValue(data['PVI_DEVICE_STATE']['PVI_DEVICE_CONNECTED'].data)
        self.chPVIDeviceWorking.SetValue(data['PVI_DEVICE_STATE']['PVI_DEVICE_WORKING'].data)
        self.chPVIDeviceInService.SetValue(data['PVI_DEVICE_STATE']['PVI_DEVICE_IN_SERVICE'].data)

        values = [{},{},{}]
        for d in data:
            if d.name in ['PVI_AC_POWER','PVI_AC_VOLTAGE','PVI_AC_CURRENT','PVI_AC_APPARENTPOWER','PVI_AC_REACTIVEPOWER','PVI_AC_ENERGY_ALL','PVI_AC_ENERGY_GRID_CONSUMPTION']:
                index = d['PVI_INDEX'].data
                values[index][d.name] = d['PVI_VALUE']
        sum_ac_power = sum_ac_energy_all = sum_ac_energy_grid = 0
        for i in range(0,3):
            self.gPVIAC.SetCellValue(0, i, repr(values[i]['PVI_AC_POWER']) + ' W')
            sum_ac_power+=values[i]['PVI_AC_POWER'].data
            self.gPVIAC.SetCellValue(1, i, repr(round(values[i]['PVI_AC_VOLTAGE'],3)) + ' V')
            self.gPVIAC.SetCellValue(2, i, repr(round(values[i]['PVI_AC_CURRENT'],5)) + ' A')
            self.gPVIAC.SetCellValue(3, i, repr(round(values[i]['PVI_AC_APPARENTPOWER'],3)) + ' VA')
            self.gPVIAC.SetCellValue(4, i, repr(round(values[i]['PVI_AC_REACTIVEPOWER'],3)) + ' VAr')
            self.gPVIAC.SetCellValue(5, i, repr(values[i]['PVI_AC_ENERGY_ALL']) + ' kWh')
            sum_ac_energy_all+=values[i]['PVI_AC_ENERGY_ALL'].data
            self.gPVIAC.SetCellValue(6, i, repr(values[i]['PVI_AC_ENERGY_GRID_CONSUMPTION']) + ' kWh')
            sum_ac_energy_grid+=values[i]['PVI_AC_ENERGY_GRID_CONSUMPTION'].data

        self.gPVIAC.SetCellValue(0,3,str(round(sum_ac_power,3)) + ' W')
        self.gPVIAC.SetCellValue(5,3,str(round(sum_ac_energy_all,3)) + ' kWh')
        self.gPVIAC.SetCellValue(6,3,str(round(sum_ac_energy_grid,3)) + ' kWh')
        self.gPVIAC.AutoSize()

        values = [{},{}]
        for d in data:
            if d.name in ['PVI_DC_POWER','PVI_DC_VOLTAGE','PVI_DC_CURRENT','PVI_DC_STRING_ENERGY_ALL']:
                index = d['PVI_INDEX'].data
                values[index][d.name] = d['PVI_VALUE']
        sum_dc_power = sum_dc_energy = 0
        for i in range(0,2):
            self.gPVIDC.SetCellValue(0, i, repr(values[i]['PVI_DC_POWER']) + ' W')
            sum_dc_power += values[i]['PVI_DC_POWER'].data
            self.gPVIDC.SetCellValue(1, i, repr(values[i]['PVI_DC_VOLTAGE']) + ' V')
            self.gPVIDC.SetCellValue(2, i, str(round(values[i]['PVI_DC_CURRENT'],5)) + ' A')
            self.gPVIDC.SetCellValue(3, i, str(round(values[i]['PVI_DC_STRING_ENERGY_ALL'])/1000) + ' kWh')
            sum_dc_energy += values[i]['PVI_DC_STRING_ENERGY_ALL'].data

        self.gPVIDC.SetCellValue(0,2,str(round(sum_dc_power,3)) + ' W')
        self.gPVIDC.SetCellValue(3,2,str(round(sum_dc_energy,3)/1000) + ' kWh')
        self.gPVIDC.AutoSize()
        self.gPVITemps.ClearGrid()
        self.gPVITemps.DeleteRows(numRows=self.gPVITemps.GetNumberRows())
        self.gPVITemps.AppendRows(data['PVI_TEMPERATURE_COUNT'].data)
        for d in data:
            if d.name == 'PVI_TEMPERATURE':
                index = d['PVI_INDEX'].data
                self.gPVITemps.SetCellValue(index,0,str(round(d['PVI_VALUE'],3)) + ' °C')
                self.gPVITemps.SetRowLabelValue(index, u"Temperatur #" + str(index))

        self.gPVITemps.AutoSize()



    def fill_bat(self):
        for index in [0,1]:
            try:
                requests = self.gui.getBatDcbData(bat_index=index)
                if len(requests) > 0:
                    f = self.gui.get_data(requests, True)
                    self._data_bat.append(f)
                    logger.exception('Erfolgreich BAT #' + str(index) + ' abgerufen')
            except:
                logger.exception('Fehler beim Abruf von BAT #' + str(index))

        self.cbBATIndex.Clear()

        for bat in self._data_bat:
            self.cbBATIndex.Append('BAT #' + str(bat['BAT_INDEX'].data))

    def fill_bat_index(self, index):
        self.gDCB_row_voltages = None
        self.gDCB_row_temp = None
        self.gDCB_last_row = 28

        f = self._data_bat[index]

        dcbcount = int(f['BAT_DCB_COUNT'])
        self.gDCB.DeleteCols(pos=0, numCols=self.gDCB.GetNumberCols())
        self.txtUsableCapacity.SetValue(str(round(f['BAT_USABLE_CAPACITY'], 5)) + ' Ah')
        self.txtUsableRemainingCapacity.SetValue(str(round(f['BAT_USABLE_REMAINING_CAPACITY'], 5)) + ' Ah')
        self.txtASOC.SetValue(str(round(f['BAT_ASOC'], 1)) + '%')
        self.txtFCC.SetValue(str(round(f['BAT_FCC'], 3)))
        self.txtRC.SetValue(str(round(f['BAT_RC'], 1)) + '%')
        self.txtRSOC.SetValue(str(round(f['BAT_INFO']['BAT_RSOC'], 1)) + '%')
        self.txtRSOCREAL.SetValue(str(round(f['BAT_RSOC_REAL'], 1)) + '%')
        self.txtModuleVoltage.SetValue(str(round(f['BAT_INFO']['BAT_MODULE_VOLTAGE'], 3)) + ' V')
        self.txtCurrent.SetValue(str(round(f['BAT_INFO']['BAT_CURRENT'], 5)) + ' A')
        self.txtBatStatusCode.SetValue(repr(f['BAT_INFO']['BAT_STATUS_CODE']))
        self.txtErrorCode.SetValue(repr(f['BAT_INFO']['BAT_ERROR_CODE']))
        self.txtDcbCount.SetValue(repr(f['BAT_DCB_COUNT']))
        self.gDCB.AppendCols(dcbcount)
        for i in range(0, dcbcount):
            self.gDCB.SetColLabelValue(i, 'DCB #' + str(i))
        self.txtMaxBatVoltage.SetValue(repr(f['BAT_MAX_BAT_VOLTAGE']) + ' V')
        self.txtMaxChargeCurrent.SetValue(repr(f['BAT_MAX_CHARGE_CURRENT']) + ' A')
        self.txtEodVoltage.SetValue(repr(f['BAT_EOD_VOLTAGE']) + ' V')
        self.txtMaxDischargeCurrent.SetValue(repr(f['BAT_MAX_DISCHARGE_CURRENT']) + ' A')
        self.txtChargeCycles.SetValue(repr(f['BAT_CHARGE_CYCLES']))
        self.txtTerminalVoltage.SetValue(repr(f['BAT_TERMINAL_VOLTAGE']) + ' V')
        self.txtMaxDcbCellTemperature.SetValue(str(round(f['BAT_MAX_DCB_CELL_TEMPERATURE'], 2)) + ' °C')
        self.txtMinDcbCellTemperature.SetValue(str(round(f['BAT_MIN_DCB_CELL_TEMPERATURE'], 2)) + ' °C')

        self.chBATDeviceConnected.SetValue(f['BAT_DEVICE_STATE']['BAT_DEVICE_CONNECTED'].data)
        self.chBATDeviceWorking.SetValue(f['BAT_DEVICE_STATE']['BAT_DEVICE_WORKING'].data)
        self.chBATDeviceInService.SetValue(f['BAT_DEVICE_STATE']['BAT_DEVICE_IN_SERVICE'].data)

        self.txtBATMaxDCBCount.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_MAX_DCB_COUNT']))
        self.txtBATCapacity.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_CAPACITY']) + ' Wh')
        self.txtBATMaxChargePower.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_CHARGE_POWER']) + ' W')
        self.txtBATMaxDischargePower.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_DSCHARGE_POWER']) + ' W')

        self.txtBATMeasuredResistance.SetValue(repr(f['BAT_INTERNALS']['BAT_MEASURED_RESISTANCE']))
        self.txtBATRunMeasuredResistance.SetValue(repr(f['BAT_INTERNALS']['BAT_RUN_MEASURED_RESISTANCE']))

        if f['BAT_TRAINING_MODE'].data == 0:
            s = 'Nicht im Training'
        elif f['BAT_TRAINING_MODE'].data == 1:
            s = 'Trainingsmodus Entladen'
        elif f['BAT_TRAINING_MODE'].data == 2:
            s = 'Trainingsmodus Laden'
        else:
            s = ' - '
        self.txtBatTrainingMode.SetValue(s)
        self.txtBatDeviceName.SetValue(repr(f['BAT_DEVICE_NAME']))

        for d in f['BAT_DCB_ALL_CELL_VOLTAGES']:
            if d.type == RSCPType.Error:
                logger.warning('BAT_DCB_ALL_CELL_VOLTAGES konnte nicht abgerufen werden')
            else:
                index = int(d['BAT_DCB_INDEX'])
                if index < dcbcount:
                    if index == 0 and not self.gDCB_row_voltages:
                        rows = self.gDCB.GetNumberRows()
                        if rows < self.gDCB_last_row + len(d['BAT_DATA']):
                            self.gDCB.AppendRows(len(d['BAT_DATA']))
                        self.gDCB_row_voltages = self.gDCB_last_row
                        self.gDCB_last_row += len(d['BAT_DATA'])

                    i = 1
                    for volt in d['BAT_DATA']:
                        self.gDCB.SetRowLabelValue(self.gDCB_row_voltages + i, u"Spannung #" + str(i))
                        self.gDCB.SetCellValue(self.gDCB_row_voltages + i, index, str(round(volt, 4)) + ' V')
                        i += 1

        for d in f['BAT_DCB_ALL_CELL_TEMPERATURES']:
            if d.type == RSCPType.Error:
                logger.warning('BAT_DCB_ALL_CELL_TEMPERATURES konnte nicht abgerufen werden')
            else:
                index = int(d['BAT_DCB_INDEX'])
                if index < dcbcount:
                    if index == 0 and not self.gDCB_row_temp:
                        rows = self.gDCB.GetNumberRows()
                        if rows < self.gDCB_last_row + len(d['BAT_DATA']):
                            self.gDCB.AppendRows(len(d['BAT_DATA']))
                        self.gDCB_row_temp = self.gDCB_last_row
                        self.gDCB_last_row += len(d['BAT_DATA'])

                    i = 1
                    for temp in d['BAT_DATA']:
                        self.gDCB.SetRowLabelValue(self.gDCB_row_temp + i, u"Temperatur #" + str(i))
                        self.gDCB.SetCellValue(self.gDCB_row_temp + i, index, str(round(temp, 4)) + ' °C')
                        i += 1

        for d in f['BAT_DCB_INFO']:
            if d.type == RSCPType.Error:
                logger.warning('BAT_DCB_INFO konnte nicht abgerufen werden')
            else:
                index = int(d['BAT_DCB_INDEX'])
                if index < dcbcount:
                    dd = datetime.datetime.fromtimestamp(int(d['BAT_DCB_LAST_MESSAGE_TIMESTAMP']) / 1000)
                    self.gDCB.SetCellValue(0, index, str(dd))
                    self.gDCB.SetCellValue(1, index, repr(d['BAT_DCB_MAX_CHARGE_VOLTAGE']) + ' V')
                    self.gDCB.SetCellValue(2, index, repr(d['BAT_DCB_MAX_CHARGE_CURRENT']) + ' A')
                    self.gDCB.SetCellValue(3, index, repr(d['BAT_DCB_END_OF_DISCHARGE']) + ' V')
                    self.gDCB.SetCellValue(4, index, repr(d['BAT_DCB_MAX_DISCHARGE_CURRENT']) + ' A')
                    self.gDCB.SetCellValue(5, index, str(round(d['BAT_DCB_FULL_CHARGE_CAPACITY'], 5)) + ' Ah')
                    self.gDCB.SetCellValue(6, index, str(round(d['BAT_DCB_REMAINING_CAPACITY'], 5)) + ' Ah')
                    self.gDCB.SetCellValue(7, index, repr(d['BAT_DCB_SOC']) + '%')
                    self.gDCB.SetCellValue(8, index, repr(d['BAT_DCB_SOH']) + '%')
                    self.gDCB.SetCellValue(9, index, repr(d['BAT_DCB_CYCLE_COUNT']))
                    self.gDCB.SetCellValue(10, index, str(round(d['BAT_DCB_CURRENT'], 5)) + ' A')
                    self.gDCB.SetCellValue(11, index, str(round(d['BAT_DCB_VOLTAGE'], 2)) + ' V')
                    self.gDCB.SetCellValue(12, index, str(round(d['BAT_DCB_CURRENT_AVG_30S'], 5)) + ' A')
                    self.gDCB.SetCellValue(13, index, str(round(d['BAT_DCB_VOLTAGE_AVG_30S'], 2)) + ' V')
                    self.gDCB.SetCellValue(14, index, str(round(d['BAT_DCB_DESIGN_CAPACITY'], 5)) + ' Ah')
                    self.gDCB.SetCellValue(15, index, repr(d['BAT_DCB_DESIGN_VOLTAGE']) + ' V')
                    self.gDCB.SetCellValue(16, index, repr(d['BAT_DCB_CHARGE_LOW_TEMPERATURE']) + ' °C')
                    self.gDCB.SetCellValue(17, index, repr(d['BAT_DCB_CHARGE_HIGH_TEMPERATURE']) + ' °C')
                    self.gDCB.SetCellValue(18, index, repr(d['BAT_DCB_MANUFACTURE_DATE']))
                    self.gDCB.SetCellValue(19, index, repr(d['BAT_DCB_SERIALNO']))
                    self.gDCB.SetCellValue(20, index, repr(d['BAT_DCB_FW_VERSION']))
                    self.gDCB.SetCellValue(21, index, repr(d['BAT_DCB_PCB_VERSION']))
                    self.gDCB.SetCellValue(22, index, repr(d['BAT_DCB_DATA_TABLE_VERSION']))
                    self.gDCB.SetCellValue(23, index, repr(d['BAT_DCB_PROTOCOL_VERSION']))
                    self.gDCB.SetCellValue(24, index, repr(d['BAT_DCB_NR_SERIES_CELL']))
                    self.gDCB.SetCellValue(25, index, repr(d['BAT_DCB_NR_PARALLEL_CELL']))
                    self.gDCB.SetCellValue(26, index, repr(d['BAT_DCB_SERIALCODE']))
                    self.gDCB.SetCellValue(27, index, repr(d['BAT_DCB_NR_SENSOR']))
                    self.gDCB.SetCellValue(28, index, repr(d['BAT_DCB_STATUS']))

        self.gDCB.AutoSizeColumns()

    def bSaveClick(self, event):
        self.saveConfig()

        #rscp = self.gui.get_data(self.gui.getUserLevel(), True)
        #ems = self.gui.get_data(self.gui.getEMSData() + self.gui.getUserLevel(), True)

    def bSYSRebootOnClick( self, event ):
        res = wx.MessageBox('Soll das gesamte E3/DC - System wirklich neu gestartet werden?', 'Systemneustart', wx.YES_NO | wx.ICON_WARNING)
        if res == wx.YES:
            try:
                r = RSCPTag.SYS_REQ_SYSTEM_REBOOT
                print(r)
                res = self.gui.get_data([r], True)
                print(res)
                wx.MessageBox('System wird neu gestartet')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')

    def bSYSApplicationRestartOnClick( self, event ):
        res = wx.MessageBox('Soll die Anwendung im E3/DC wirklich neu gestartet werden?', 'Applikations - Neustart', wx.YES_NO | wx.ICON_WARNING)
        if res == wx.YES:
            try:
                r = RSCPTag.SYS_REQ_RESTART_APPLICATION
                print(r)
                res = self.gui.get_data([r], True)
                print(res)
                wx.MessageBox('Anwendung wird neu gestartet')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')

    def bEMSEPTestOnClick( self, event ):
        res = wx.MessageBox('Beim Notstromtest wird kurz der Hausstrom gekappt.\nNach etwa 10-15 Sekunden sollte dann '
                            'der Notstrom einspringen und\nStrom wieder zur Verfügung stehen.\nEs wird dann auf Notstrom'
                            ' umgestellt. Nach dem Test wird der\nNotstrom wieder beendet, der Hausstrom wird wieder '
                            'getrennt für ca. 2 Sekunden.\n\nSoll der Notstrom-Test wirklich durchgeführt werden?',
                            'Notstrom-Test', wx.YES_NO | wx.ICON_WARNING)
        if res == wx.YES:
            try:
                r = RSCPDTO(tag = RSCPTag.REQ_START_EMERGENCYPOWER_TEST, rscp_type=RSCPType.Bool, data = True)
                print(r)
                res = self.gui.get_data([r], True)
                print(res)
                wx.MessageBox('Notstromtest wird durchgeführt')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')

    def bEMSManualChargeStartOnClick( self, event ):
        try:
            val = int(self.txtEMSManualChargeValue.GetValue())
        except:
            val = 0
        if val > 0:
            res = wx.MessageBox('Die manuelle Ladung ist auf die Ausführung einmal am Tag begrenzt, steht nicht genügend PV-Leistung zur Verfügung, wird Netzstrom bezogen! Fortfahren?', 'Manuelle Ladung', wx.YES_NO | wx.ICON_QUESTION)
            if res == wx.YES:
                try:
                    r = RSCPDTO(tag = RSCPTag.EMS_REQ_START_MANUAL_CHARGE, rscp_type = RSCPType.Uint32, data = val)
                    print(r)
                    res = self.gui.get_data([r], True)
                    print(res)
                    if res.name == 'EMS_START_MANUAL_CHARGE' and res.data:
                        wx.MessageBox('Manuelle Ladung gestartet')
                    else:
                        wx.MessageBox('Fehler beim Start der manuellen Ladung, heute bereits durchgeführt?')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')
        else:
            wx.MessageBox('Die Ladung von (' + self.txtEMSManualChargeValue.GetValue() + ') Wh ist nicht zulässig, bitte anderen Ganzzahl-Wert wählen', 'Manuelle Ladung', wx.ICON_WARNING)

    def bTestClick(self, event, method = 'auto'):
        try:
            if not self.gui:
                self.bConfigGetIPAddressOnClick(event)

            if method == 'ws':
                self.chConfigWebsocket.SetValue(True)
            elif method == 'direct':
                self.chConfigWebsocket.SetValue(False)
            elif method == 'auto':
                if self.txtRSCPPassword.GetValue() == '':
                    self.chConfigWebsocket.SetValue(True)
                else:
                    self.chConfigWebsocket.SetValue(False)

            result = self.gui.get_data(self.gui.getInfo(), True)

            sn = repr(result['INFO_SERIAL_NUMBER'])
            if self.txtConfigSeriennummer.GetValue() == '' and sn:
                self.txtConfigSeriennummer.SetValue(sn)

            ip = repr(result['INFO_IP_ADDRESS'])
            if self.txtIP.GetValue() == '' and ip:
                self.txtIP.SetValue(ip)

            rel = repr(result['INFO_SW_RELEASE'])

            if isinstance(self.gui, E3DCWebGui) and self.txtRSCPPassword.GetValue() == '':
                msg = wx.MessageBox('Verbindung mit System ' + sn + ' / ' + rel + ' konnte nur über WebSockets hergestellt werden, da kein RSCP-Passwort vergeben wurde.\nDiese Verbindung ist langsamer und auf das Internet angewiesen.\n', 'Info',
                                    wx.OK | wx.ICON_WARNING)
            elif isinstance(self.gui, E3DCWebGui) and self.txtRSCPPassword.GetValue() != '':
                msg = wx.MessageBox(
                    'Verbindung mit System ' + sn + ' / ' + rel + ' konnte nur über WebSockets hergestellt werden, da das angegebene RSCP-Passwort falsch ist oder das E3DC nicht direkt erreichbar ist.\nDiese Verbindung ist langsamer und auf das Internet angewiesen.',
                    'Info',
                    wx.OK | wx.ICON_WARNING)
            else:
                msg = wx.MessageBox('Verbindung mit System ' + sn + ' / ' + rel + ' hergestellt', 'Info',
                          wx.OK | wx.ICON_INFORMATION)
        except RSCPCommunicationError:
            if isinstance(self.gui, E3DCGui) and method == 'auto':
                self.bTestClick(event, method = 'ws')
            else:
                traceback.print_exc()
                msg = wx.MessageBox('Verbindung konnte nicht aufgebaut werden', 'Error',
                              wx.OK | wx.ICON_ERROR)
        except:
            traceback.print_exc()
            msg = wx.MessageBox('Verbindung konnte nicht aufgebaut werden', 'Error',
                                wx.OK | wx.ICON_ERROR)

    def bUpdateCheckClick(self, event):
        try:
            result = self.gui.get_data(self.gui.getCheckForUpdates(), True)
            status = result.data
        except:
            traceback.print_exc()
            status = 0

        if status == 1:
            wx.MessageBox('Updatecheck wird ausgeführt, wenn eine neue Version zur Verfügung steht wird diese installiert.')
        else:
            wx.MessageBox('Updatecheck konnte nicht ausgeführt werden')

    def clear_values(self):
        self._data_bat = []
        self._data_dcdc = []
        self._data_ems = None
        self._data_info = None
        self._data_pvi = None
        self._data_pm = []
        self._data_wb = None

    def bUpdateClick(self, event):
        if self.gui:
            self.clear_values()

            try:
                self.fill_info()
            except:
                logger.exception('Fehler beim Abruf der INFO-Daten')

            try:
                selected = self.cbBATIndex.GetSelection()
                if selected in [wx.NOT_FOUND, '', None, False]:
                    selected = 0

                self.fill_bat()

                if selected != wx.NOT_FOUND:
                    if self.cbBATIndex.GetCount() > selected:
                        self.cbBATIndex.SetSelection(selected)
                        self.fill_bat_index(selected)
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

    def bSaveRSCPDataOnClick( self, event ):
        with wx.FileDialog(self, "als JSON speichern", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                data = self.sammle_data()

                with open(pathname, 'w') as file:
                    json.dump(data, file)

            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)


        event.Skip()

    def sendToServer(self, event):
        ret = wx.MessageBox('Achtung, es werden alle angezeigten Daten an externe Stelle übermittelt.\nSeriennummern werden in anonymisierter Form übermittelt.\nZugangsdaten werden nicht übermittelt.\nDie Datenübertragung erfolgt verschlüsselt.\nWirklich fortfahren?',
                            caption = 'Ausgelesene Daten übermitteln',
                            style=wx.YES_NO)
        if ret == wx.YES:
            status = 'NO CODE'
            try:
                data = self.sammle_data()

                r = requests.post(url = self.txtDBServer.GetValue(), json = data)
                status = r.status_code
                r.raise_for_status()
                res = r.json()
                if 'error' in res:
                    raise Exception('Fehler bei Datenübermittlung' + res['error'])

                if 'success' in res:
                    MessageBox(self, 'Übermittlung Erfolgreich', 'Daten wurden erfolgreich übermittelt!\nSpeicherpfad:\n\n' + res['success'])


            except:
                traceback.print_exc()
                wx.MessageBox('Es gab einen Fehler bei der Übermittlung. (HTTP-Status: ' + str(r.status_code) + ')')

    def sammle_data(self):
        anonymize = ['DCDC_SERIAL_NUMBER', 'INFO_MAC_ADDRESS', 'BAT_DCB_SERIALNO', 'BAT_DCB_SERIALCODE', 'INFO_SERIAL_NUMBER',
                     'INFO_A35_SERIAL_NUMBER', 'PVI_SERIAL_NUMBER', 'INFO_PRODUCTION_DATE']
        remove = ['INFO_IP_ADDRESS']
        data = {}
        if self._data_bat:
            data['BAT_DATA'] = []
            print(data)
            print(type(data['BAT_DATA']))
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
            data['PVI_DATA'] = self._data_pvi.asDict()

        if self._data_pm:
            data['PM_DATA'] = []
            for d in self._data_pm:
                data['PM_DATA'].append(d.asDict())

        if self._data_wb:
            data['WB_DATA'] = self._data_wb.asDict()

        data = self.anonymize_data(data, anonymize, remove)

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


    def mainOnClose(self, event):
        if isinstance(self._gui, E3DCWebGui):
            self._gui.e3dc.ws.close()

        event.Skip()


    def getSerialnoFromWeb(self, username, password):
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
                try:
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
                    traceback.print_exc()
        except:
            traceback.print_exc()

        return []

    def bConfigGetSerialNoOnClick( self, event ):
        username = self.txtUsername.GetValue()
        password = self.txtPassword.GetValue()

        if username and password:
            ret = self.getSerialnoFromWeb(username, password)
            if len(ret) == 1:
                serial = 'S10-' + ret[0]['serialno']
                self.txtConfigSeriennummer.SetValue(serial)
                wx.MessageBox('Seriennummer konnte ermittelt werden (WEB): ' + serial, 'Ermittlung Seriennummer')
            elif len(ret) > 1:
                sns = '\n'
                for sn in ret:
                    sns += '\nS10-' + sn['serialno']
                wx.MessageBox('Es wurde mehr als eine Seriennummer ermittelt (WEB):' + sns, 'Ermittlung Seriennummer')
            else:
                wx.MessageBox('Es konnte keine Seriennummer ermittelt werden (WEB). Zugangsdaten falsch?', 'Ermittlung Seriennummer', wx.ICON_ERROR)
        else:
            wx.MessageBox('Zur Ermittlung der Seriennummer sind mindestens Benutzername und Passwort erforderlich!', 'Ermittlung Seriennummer', wx.ICON_WARNING)

        event.Skip()

    def bConfigGetIPAddressOnClick( self, event ):
        username = self.txtUsername.GetValue()
        password = self.txtPassword.GetValue()
        serial = self.txtConfigSeriennummer.GetValue()
        if username and password:
            if not serial:
                try:
                    ret = self.getSerialnoFromWeb(username, password)
                    if len(ret) > 0:
                        serial = 'S10-' + ret[0]['serialno']
                        self.txtConfigSeriennummer.SetValue(serial)
                except:
                    wx.MessageBox('Seriennummer fehlt und konnte nicht ermittelt werden', 'Ermittlung IP-Adresse', wx.ICON_ERROR)

        if username and password and serial:
            self.chConfigWebsocket.SetValue(True)

        if isinstance(self.gui, E3DCWebGui):
            try:
                ip = repr(self.gui.get_data(self.gui.getInfo(), True)['INFO_IP_ADDRESS'])
                if ip:
                    self.txtIP.SetValue(ip)
                    self.chConfigWebsocket.SetValue(False)
                    wx.MessageBox('IP-Adresse konnte ermittelt werden: ' + ip, 'Ermittlung IP-Adresse')
                else:
                    wx.MessageBox('IP-Adresse konnte nicht ermittelt werden, kein Inahlt', 'Ermittlung IP-Adresse', wx.ICON_ERROR)

            except:
                wx.MessageBox('Bei der Ermittlung der IP-Adresse ist ein Fehler aufgetreten #2', 'Ermittlung IP-Adresse', wx.ICON_ERROR)

        event.Skip()

    def bConfigSetRSCPPasswordOnClick( self, event ):
        ret = wx.MessageBox('Soll das angegebene RSCP-Kennwort mit dem bisherigen überschrieben werden?', 'RSCP-Passwort ändern', wx.YES_NO | wx.ICON_WARNING)
        if ret == wx.YES:
            try:
                password = self.txtRSCPPassword.GetValue()
                requests = [RSCPDTO(tag = RSCPTag.RSCP_REQ_SET_ENCRYPTION_PASSPHRASE, rscp_type = RSCPType.CString, data = password)]
                res = self.gui.get_data(requests, True)
                if res.data:
                    wx.MessageBox('RSCP-Passwort wurde erfolgreich geändert', 'RSCP-Passwort ändern', wx.ICON_INFORMATION)
                else:
                    raise Exception('RSCP-Passwort wurde nicht akzeptiert!')
            except:
                wx.MessageBox('Fehler beim Ändern des RSCP-Passworts', 'RSCP-Passwort ändern', wx.ICON_ERROR)


        event.Skip()

    def setWSConnected(self):
        self.rConfigWebsocketConnected.SetValue(True)

    def setWSDisconnected(self):
        self.rConfigWebsocketConnected.SetValue(False)

    def check_e3dcwebgui(self):
        while True:
            if isinstance(self.gui, E3DCWebGui) and self.gui.e3dc.connected:
                self.setWSConnected()
            else:
                self.setWSDisconnected()

            time.sleep(1)

    def cbBATIndexOnCombobox( self, event ):
        selected = self.cbBATIndex.GetSelection()
        if selected != wx.NOT_FOUND:
            self.fill_bat_index(selected)

        event.Skip()

    def bINFOSaveOnClick( self, event ):
        r = []
        test = self.cbTimezone.GetValue()
        if test != self._data_info['INFO_TIME_ZONE'].data:
            r.append(RSCPDTO(tag = RSCPTag.INFO_REQ_SET_TIME_ZONE, rscp_type=RSCPType.CString, data=test))

        test = self.txtIPAdress.GetValue()
        if test != self._data_info['INFO_IP_ADDRESS'].data:
            r.append(RSCPDTO(tag = RSCPTag.INFO_REQ_SET_IP_ADDRESS, rscp_type=RSCPType.CString, data=test))

        test = self.txtSubnetmask.GetValue()
        if test != self._data_info['INFO_SUBNET_MASK'].data:
            r.append(RSCPDTO(tag = RSCPTag.INFO_REQ_SET_SUBNET_MASK, rscp_type=RSCPType.CString, data=test))

        test = self.txtGateway.GetValue()
        if test != self._data_info['INFO_GATEWAY'].data:
            r.append(RSCPDTO(tag = RSCPTag.INFO_REQ_SET_GATEWAY, rscp_type=RSCPType.CString, data=test))

        test = self.txtDNSServer.GetValue()
        if test != self._data_info['INFO_DNS'].data:
            r.append(RSCPDTO(tag = RSCPTag.INFO_REQ_SET_DNS, rscp_type=RSCPType.CString, data=test))

        test = self.chDHCP.GetValue()
        if test != self._data_info['INFO_DHCP_STATUS'].data:
            r.append(RSCPDTO(tag = RSCPTag.INFO_REQ_SET_DHCP_STATUS, rscp_type=RSCPType.Bool, data=test))

        if len(r) == 0:
            res = wx.MessageBox('Es wurden keine Änderungen gemacht, aktuelle Einstellungen trotzdem übertragen?', 'Info speichern', wx.YES_NO)
            if res == wx.YES:
                test = self.cbTimezone.GetValue()
                r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_TIME_ZONE, rscp_type=RSCPType.CString, data=test))

                test = self.txtIPAdress.GetValue()
                r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_IP_ADDRESS, rscp_type=RSCPType.CString, data=test))

                test = self.txtSubnetmask.GetValue()
                r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_SUBNET_MASK, rscp_type=RSCPType.CString, data=test))

                test = self.txtGateway.GetValue()
                r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_GATEWAY, rscp_type=RSCPType.CString, data=test))

                test = self.txtDNSServer.GetValue()
                r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_DNS, rscp_type=RSCPType.CString, data=test))

                test = self.chDHCP.GetValue()
                r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_DHCP_STATUS, rscp_type=RSCPType.Bool, data=test))

        if len(r) > 0:
            res = wx.MessageBox('Wichtig: Falsche Einstellungen können dazu führen, dass das E3DC nicht mehr oder nur noch per Websockets zu erreichen ist. Die Einstellungen müssen dann über das Display direkt geändert werden. Wirklich durchführen?', 'Hinweis', wx.ICON_WARNING + wx.YES_NO)
            if res == wx.YES:
                try:
                    res = self.gui.get_data(r, True)
                    wx.MessageBox('Übertragung abgeschlossen')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')

                self.bUpdateClick(event)


app = wx.App()
g = Frame(None)
g.Show()
app.MainLoop()