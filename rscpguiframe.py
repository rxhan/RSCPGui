import logging
import re

logger = logging.getLogger(__name__)

logger.debug('Programmstart')

import locale

import datetime
import json
import os
import threading
import time
import traceback
import sys

import pytz as pytz
import requests

try:
    import paho.mqtt.client as paho
except:
    logger.warning('Paho-Libary (paho) nicht gefunden, MQTT wird nicht zur Verfügung stehen')

try:
    import wx
    import wx.dataview
    from export import E3DCExport
    from gui import MainFrame
except:
    logger.warning('wxPython steht nicht zur Verfügung, Programm beschränkt sich auf die Console')

try:
    import telegram
except Exception as e:
    logger.warning('Telegram-Libary (python-telegram-bot) nicht gefunden, Telegram-Benachrichtigungen stehen nicht zur Verfügung')

from e3dc._rscp_dto import RSCPDTO
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType, WB_TYPE, WB_MODE
from e3dcwebgui import E3DCWebGui
from rscpguimain import RSCPGuiMain

class RSCPGuiFrame(MainFrame, RSCPGuiMain):
    class MessageBox(wx.Dialog):
        def __init__(self, parent, title, value):
            wx.Dialog.__init__(self, parent, title=title)
            text = wx.TextCtrl(self, style=wx.TE_READONLY | wx.BORDER_NONE | wx.TE_MULTILINE)
            text.SetValue(value)
            text.SetBackgroundColour(self.GetBackgroundColour())
            self.ShowModal()
            self.Destroy()

    _time_format = '%d.%m.%Y %H:%M:%S.%f'
    _e3dcexportFrame = None

    def __init__(self, parent, args):
        logger.info('Frame initialisiert')
        RSCPGuiMain.__init__(self, args)

        MainFrame.__init__(self, parent)

        def t(col, ascending = True):
            logger.debug('Portal: Sortiere nach Spalte: ' + str(col) + ' Ascending: ' + str(ascending))
            if col < self.gPortalList.GetNumberCols():
                lst = []
                for currow in range(0, self.gPortalList.GetNumberRows()):
                    data = []
                    for curcol in range(0, self.gPortalList.GetNumberCols()):
                        data.append(self.gPortalList.GetCellValue(currow, curcol))
                    value = self.gPortalList.SortingRowsData[currow][self.gPortalList.SortingColNames[col]]
                    lst.append((currow, value, data))

                result = sorted(lst, key = lambda v: v[1], reverse = ascending)

                currow = 0
                newrowsdata = []
                for oldrow, value, data in result:
                    newrowsdata.append(self.gPortalList.SortingRowsData[oldrow])
                    curcol = 0
                    for value in data:
                        self.gPortalList.SetCellValue(currow, curcol, value)
                        curcol += 1
                    currow += 1

                self.gPortalList.SortingRowsData = newrowsdata
            else:
                return False

        self.gPortalList.SortColumn = t

        logger.info('Oberfläche geladen')

        self.loadConfig()

        def load_timezones():
            logger.debug('Lade Zeitzonen')
            for tz in pytz.common_timezones:
                self.cbTimezone.Append(str(tz))
            logger.info('Zeitzonen geladen')

        threading.Thread(target=load_timezones, args=()).start()

        self.cbConfigVerbindungsart.SetValue(self.cfgLoginconnectiontype)

        self.Bind(wx.EVT_BUTTON, self.bTestClick, self.bTest)
        self.Bind(wx.EVT_BUTTON, self.bSaveClick, self.bSave)
        self.Bind(wx.EVT_BUTTON, self.bUpdateClick, self.bUpdate)

        self.gDCB_row_voltages = None
        self.gDCB_row_temp = None

        self._wsthread = threading.Thread(target=self.check_e3dcwebgui, args=())
        self._wsthread.start()

        def preConnect():
            try:
                g = self.gui
                if self._args.export:
                    logger.debug('Export bei Programmstart aktiviert')
                    self.bUploadStartOnClick(None)
                if self._args.portal:
                    self.sendToPortalMin()


            except:
                pass

        threading.Thread(target=preConnect, args=()).start()

        self._autothread = threading.Thread(target=self.autoUpdate, args=())
        self._autothread.start()

        if 'paho' not in sys.modules.keys():
            logger.debug('Deaktiviere MQTT-Felder, da MQTT nicht zur Verfügung steht (paho nicht installiert)')
            self.enabledisableMQTT(False)

        if 'telegram' not in sys.modules.keys():
            logger.debug('Deaktiviere Telegram-Benachrichtigungen, da Telegram nicht zur Verfügung steht (python-telegram-bot nicht installiert)')
            self.enabledisableTelegram(False)

        self.chUploadMQTTOnCheck(None)
        self.chUploadInfluxOnCheck(None)

        locale.setlocale(locale.LC_ALL, '')

        logger.info('Init abgeschlossen')

    def enabledisableTelegram(self, value):
        self.chBenachrichtigungTelegram.Enable(value)
        self.txtTelegramToken.Enable(value)
        self.txtTelegramEmpfaenger.Enable(value)

    def enabledisableMQTT(self, value):
        self.scUploadMQTTQos.Enable(value)
        self.chUploadMQTT.Enable(value)
        self.chUploadMQTTRetain.Enable(value)
        self.txtUploadMQTTBroker.Enable(value)
        self.txtUploadMQTTPort.Enable(value)
        self.txtUploadMQTTUsername.Enable(value)
        self.txtUploadMQTTPassword.Enable(value)
        self.fpUploadMQTTZertifikat.Enable(value)
        self.cbUploadMQTTInsecure.Enable(value)
        self.chUploadMQTTSub.Enable(value)

    def hideMQTT(self, value = True):
        if value:
            self.scUploadMQTTQos.Hide()
            #self.chUploadMQTT.Hide()
            self.chUploadMQTTRetain.Hide()
            self.txtUploadMQTTBroker.Hide()
            self.txtUploadMQTTPort.Hide()
            self.txtUploadMQTTUsername.Hide()
            self.txtUploadMQTTPassword.Hide()
            self.fpUploadMQTTZertifikat.Hide()
            self.cbUploadMQTTInsecure.Hide()
            self.chUploadMQTTSub.Hide()
            self.m_staticText214.Hide()
            self.m_staticText208.Hide()
            self.m_staticText209.Hide()
            self.m_staticText2091.Hide()
            self.m_staticText2101.Hide()
            self.m_staticText210.Hide()
        else:
            self.scUploadMQTTQos.Show()
            #self.chUploadMQTT.Show()
            self.chUploadMQTTRetain.Show()
            self.txtUploadMQTTBroker.Show()
            self.txtUploadMQTTPort.Show()
            self.txtUploadMQTTUsername.Show()
            self.txtUploadMQTTPassword.Show()
            self.fpUploadMQTTZertifikat.Show()
            self.cbUploadMQTTInsecure.Show()
            self.chUploadMQTTSub.Show()
            self.m_staticText214.Show()
            self.m_staticText208.Show()
            self.m_staticText209.Show()
            self.m_staticText2091.Show()
            self.m_staticText2101.Show()
            self.m_staticText210.Show()

    def chUploadMQTTOnCheck(self, event):
        if self.chUploadMQTT.GetValue():
            self.hideMQTT(False)
        else:
            self.hideMQTT(True)

        parent = self.chUploadMQTT.Parent
        parent.GetSizer().Layout()

    def hideInflux(self, value = True):
        if value:
            self.m_staticText213.Hide()
            self.m_staticText215.Hide()
            self.m_staticText216.Hide()
            self.m_staticText217.Hide()
            self.m_staticText218.Hide()
            self.txtUploadInfluxHost.Hide()
            self.txtUploadInfluxPort.Hide()
            self.txtUploadInfluxDatenbank.Hide()
            self.scUploadInfluxTimeout.Hide()
            self.txtUploadInfluxName.Hide()
        else:
            self.m_staticText213.Show()
            self.m_staticText215.Show()
            self.m_staticText216.Show()
            self.m_staticText217.Show()
            self.m_staticText218.Show()
            self.txtUploadInfluxHost.Show()
            self.txtUploadInfluxPort.Show()
            self.txtUploadInfluxDatenbank.Show()
            self.scUploadInfluxTimeout.Show()
            self.txtUploadInfluxName.Show()

    def chUploadInfluxOnCheck(self, event):
        if self.chUploadInfluxdb.GetValue():
            self.hideInflux(False)
        else:
            self.hideInflux(True)

        parent = self.chUploadInfluxdb.Parent
        parent.GetSizer().Layout()

    def scAutoUpdateOnChange(self, event):
        autoupdate = self.scAutoUpdate.GetValue()
        if autoupdate > 0 and self._autothread is None:
            self._autothread = threading.Thread(target=self.autoUpdate, args=())
            self._autothread.start()

    def autoUpdate(self):
        while True:
            autoupdate = self.scAutoUpdate.GetValue()
            if autoupdate == 0:
                self._autothread = None
                return False
            else:
                self.pMainChanged()
                time.sleep(autoupdate)

    def bUploadStartOnClick(self, event):
        if not self._AutoExportStarted:
            self.refreshConfig()
            RSCPGuiMain.StartExport(self)
            self.bUploadStart.SetLabel('Export beenden')
        else:
            self._AutoExportStarted = False
            self.bUploadStart.Enable(False)
            RSCPGuiMain.StopExport(self)

    def StartAutoExport(self):
        RSCPGuiMain.StartAutoExport(self)
        self.bUploadStart.SetLabel('Export starten')
        self.bUploadStart.Enable(True)

    def bUploadSetDataOnClick(self, event):
        self.bUploadSetData.Enable(False)
        if self._e3dcexportFrame:
            try:
                logger.warning('Exportdialog scheinbar noch geöffnet, schließe Dialog')
                self._e3dcexportFrame.Close()
            except:
                logger.exception('Fehler beim schließen des Exportdialogs')


        self._e3dcexportFrame = E3DCExport(self, paths=self.cfgExportpaths, names = self.cfgExportpathnames)
        self._e3dcexportFrame.Bind(wx.EVT_CLOSE, self.ExportFrameOnClose)
        self._e3dcexportFrame.Show()

    def ExportFrameOnClose(self, event):
        logger.debug('Exportfenster wurde geschlossen')
        self.cfgExportpaths = self._e3dcexportFrame.getExportPaths()
        self.cfgExportpathnames = self._e3dcexportFrame.getCustomNames()
        if len(self.cfgExportpaths) != len(self.cfgExportpathnames):
            logger.error('Ausgewählte Pfadanzahl stimmt nicht mit Bezeichneranzahl überein')

        self.stUploadCount.SetLabel('Es wurden ' + str(len(self.cfgExportpaths)) + ' Datenfelder angewählt')


        for path in self.cfgExportpaths:
            if path in self._e3dcexportFrame._customNames:
                custom = self._e3dcexportFrame._customNames[path]
                logger.debug('Pfad: ' + path + ' angewählt und gespeichert unter dem Namen ' + custom)
            else:
                logger.debug('Pfad: ' + path + ' angewählt und gespeichert')



        self.bUploadSetData.Enable(True)
        self._e3dcexportFrame = None
        event.Skip()

    def pMainChanged(self, event=None):
        self.updateTab()


    def updateTab(self, page = None):
        if page is None:
            page = self.pMainregister.GetCurrentPage()

        if not self._updateRunning:
            self._updateRunning = True
            self.disableButtons()
            self.gaUpdate.SetValue(0)

            name = page.GetName()

            try:
                logger.debug('Aktualisiere ' + name)
                if page == self.pPortal:
                    try:
                        self.fill_portal()
                    except:
                        logger.exception('Fehler beim Darstellen der Portal-Daten')
                elif page == self.pBenachrichtigungen:
                    try:
                        self.fill_benachrichtigungen()
                    except:
                        logger.exception('Fehler beim Darstellen der Benachrichtigung')
                elif self.gui:
                    if page == self.pDCDC:
                        try:
                            self.fill_dcdc()
                        except:
                            logger.exception('Fehler beim Abruf der DCDC-Daten')
                    elif page == self.pMain:
                        try:
                            self.fill_info()
                        except:
                            logger.exception('Fehler beim Abruf der INFO-Daten')
                    elif page == self.pBAT:
                        try:
                            self.fill_bat()
                            self.gDCB.AutoSizeRows()
                            self.gDCB.AutoSizeColumns()
                        except:
                            logger.exception('Fehler beim Abruf der BAT-Daten')
                    elif page == self.pPVI:
                        try:
                            self.fill_pvi()
                        except:
                            logger.exception('Fehler beim Abruf der PVI-Daten')
                    elif page == self.pEMS:
                        try:
                            p2 = self.m_notebook2.GetCurrentPage()
                            if p2 == self.m_panel11: # Modbus
                                self.fill_mbs()
                            elif p2 == self.m_panel9: # SYS
                                self.fill_ems_sys()
                            elif p2 == self.m_panel8: # Ladeeinstellungen
                                self.fill_ems_power()
                            elif p2 == self.m_panel7: # Basis
                                self.fill_ems_basis()
                        except:
                            logger.exception('Fehler beim Abruf der EMS-Daten')
                    elif page == self.pPM:
                        try:
                            self.fill_pm()
                        except:
                            logger.exception('Fehler beim Abruf der PM-Daten')
                    elif page == self.pWB:
                        try:
                            self.fill_wb()
                        except:
                            logger.exception('Fehler beim Abruf der WB-Daten')
                else:
                    logger.warning('Konfiguration unvollständig, Verbindung nicht möglich')
            except:
                logger.exception('Fehler beim Aktualisieren von ' + name)
            self.gaUpdate.SetValue(100)
            self.enableButtons()
            self._updateRunning = False

    @property
    def gui(self):
        if self._gui:
            if self.cfgLoginusername == self.txtUsername.GetValue() and self.cfgLoginpassword == self.txtPassword.GetValue() and \
                    self.cfgLoginaddress == self.txtIP.GetValue() and self.cfgLoginrscppassword == self.txtRSCPPassword.GetValue() and \
                    self.cfgLoginseriennummer == self.txtConfigSeriennummer.GetValue() and \
                    self.cfgLoginconnectiontype == self.cbConfigVerbindungsart.GetValue():
                return self._gui

        self.cfgLoginusername = self.txtUsername.GetValue()
        self.cfgLoginpassword = self.txtPassword.GetValue()
        self.cfgLoginaddress = self.txtIP.GetValue()
        self.cfgLoginrscppassword = self.txtRSCPPassword.GetValue()
        self.cfgLoginseriennummer = self.txtConfigSeriennummer.GetValue()
        self.cfgLoginconnectiontype = self.cbConfigVerbindungsart.GetValue()

        if isinstance(self._gui, E3DCWebGui):
            self._gui.e3dc.ws.close()

        return RSCPGuiMain.gui.fget(self)

    def bEMSUploadChangesOnClick(self, event):
        if self._data_ems is None:
            RSCPGuiMain.fill_ems(self)

        r = []
        test = 1 if self.chEMSBatteryBeforeCarMode.GetValue() == False else 0
        if test != self._data_ems['EMS_BATTERY_BEFORE_CAR_MODE'].data:
            r.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_BATTERY_BEFORE_CAR_MODE, rscp_type=RSCPType.UChar8, data=test))

        test = 0 if self.chEMSBatteryToCarMode.GetValue() == False else 1
        if test != self._data_ems['EMS_BATTERY_TO_CAR_MODE'].data:
            r.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_BATTERY_TO_CAR_MODE, rscp_type=RSCPType.UChar8, data=test))

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
            r.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, rscp_type=RSCPType.Container, data=temp))

        days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

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
                wx.MessageBox('Dateneingabe im Feld ' + von + ' ist falsch', 'Ladeeinstellungen speichern', wx.ICON_WARNING)
                raise Exception('Dateneingabe im Feld ' + von + ' falsch')

            bis_data = self.__getattribute__(bis).GetValue().split(':')
            if len(bis_data) == 2:
                bis_data_hour = int(bis_data[0])
                bis_data_minute = int(bis_data[1])
            else:
                wx.MessageBox('Dateneingabe im Feld ' + bis + ' ist falsch', 'Ladeeinstellungen speichern', wx.ICON_WARNING)
                raise Exception('Dateneingabe im Feld ' + bis + ' falsch')

            if idlePeriod['EMS_IDLE_PERIOD_ACTIVE'].data != ch_data or \
                    idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_HOUR'].data != von_data_hour or \
                    idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_MINUTE'].data != von_data_minute or \
                    idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_HOUR'].data != bis_data_hour or \
                    idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_MINUTE'].data != bis_data_minute:
                res = self.gui.setIdlePeriod(type=idlePeriod['EMS_IDLE_PERIOD_TYPE'].data,
                                             active=ch_data,
                                             day=idlePeriod['EMS_IDLE_PERIOD_DAY'].data,
                                             start=str(von_data_hour).zfill(2) + ':' + str(von_data_minute).zfill(2),
                                             end=str(bis_data_hour).zfill(2) + ':' + str(bis_data_minute).zfill(2))
                r += res

        if len(r) > 0:
            try:
                res = self.gui.get_data(r, True)
                wx.MessageBox('Übertragung abgeschlossen')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')
        else:
            res = wx.MessageBox('Es wurden keine Änderungen gemacht, aktuelle Einstellungen trotzdem übertragen?',
                                'Ladeeinstellungen speichern', wx.YES_NO)
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
                temp.append(
                    RSCPDTO(tag=RSCPTag.EMS_WEATHER_REGULATED_CHARGE_ENABLED, rscp_type=RSCPType.UChar8, data=test))

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
        self.fill_ems()

    def set_wb_enabled(self):
        def set_wb_enableddisabled(value):
            self.bWBSave.Enable(value)
            self.chWB1PH.Enable(value)
            self.chWBSunmode.Enable(value)
            self.sWBLadestrom.Enable(value)
            self.bWBStopLoading.Enable(value)

        if len(self._data_wb) > 0:
            set_wb_enableddisabled(True)
        else:
            set_wb_enableddisabled(False)

        if self.txtWBMode.GetValue() == 'LOADING':
            self.bWBStopLoading.SetLabel('Ladevorgang abbrechen')
        else:
            self.bWBStopLoading.SetLabel('Ladevorgang starten')

    def bWBStopLoadingClick(self, event):
        index = self.cbWallbox.GetSelection()
        if len(self._data_wb) > index:
            res = wx.MessageBox('Soll der Ladevorgang in WB#' + str(index) + ' wirklich abgebrochen werden?',
                                'Wallbox Ladevorgang abbrechen', wx.YES_NO | wx.ICON_QUESTION)
            if res == wx.YES:
                try:
                    ba = bytearray(6)
                    ba[4] = 1
                    req_data = RSCPDTO(tag=RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
                    req_data += RSCPDTO(tag=RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data=index)
                    req_data += RSCPDTO(tag=RSCPTag.WB_REQ_SET_EXTERN, rscp_type=RSCPType.Container, data=
                    [RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA, rscp_type=RSCPType.ByteArray, data=ba),
                     RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA_LEN, rscp_type=RSCPType.UChar8, data=6)]
                                        )

                    print(req_data)
                    res = self.gui.get_data([req_data], True)
                    print(res)
                    wx.MessageBox('Übertragung durchgeführt')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')
        else:
            wx.MessageBox('Wallbox #' + str(index) + ' existiert nicht, dieser Fehler sollte nicht auftreten!')
            logger.error('Wallbox #' + str(index) + ' existiert nicht!')

        self.pMainChanged()

    def bWBSaveOnClick(self, event):
        index = self.cbWallbox.GetSelection()

        data = self._data_wb[index]

        index = data['WB_INDEX'].data

        r = []
        test_changed = self.chWBSunmode.GetValue()
        test_orig = (data['WB_EXTERN_DATA_ALG']['WB_EXTERN_DATA'].data[2] & 128) == 128
        if test_changed != test_orig:
            ba = bytearray(6)
            ba[0] = 1 if test_changed else 2
            req_data = RSCPDTO(tag=RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
            req_data += RSCPDTO(tag=RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data=index)
            req_data += RSCPDTO(tag=RSCPTag.WB_REQ_SET_EXTERN, rscp_type=RSCPType.Container, data=
            [RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA, rscp_type=RSCPType.ByteArray, data=ba),
             RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA_LEN, rscp_type=RSCPType.UChar8, data=6)]
                                )
            r.append(req_data)

        test_changed = self.chWB1PH.GetValue()
        test_orig = (data['WB_EXTERN_DATA_ALG']['WB_EXTERN_DATA'].data[1] == 1)
        if test_changed != test_orig:
            ba = bytearray(6)
            ba[3] = 1 if test_changed else 3
            req_data = RSCPDTO(tag=RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
            req_data += RSCPDTO(tag=RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data=index)
            req_data += RSCPDTO(tag=RSCPTag.WB_REQ_SET_EXTERN, rscp_type=RSCPType.Container, data=
            [RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA, rscp_type=RSCPType.ByteArray, data=ba),
             RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA_LEN, rscp_type=RSCPType.UChar8, data=6)]
                                )
            r.append(req_data)

        test_changed = self.sWBLadestrom.GetValue()
        param_1 = bytearray(data['WB_RSP_PARAM_1']['WB_EXTERN_DATA'].data)
        if test_changed != param_1[2]:
            param_1[2] = test_changed
            req_data = RSCPDTO(tag=RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
            req_data += RSCPDTO(tag=RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data=index)
            req_data += RSCPDTO(tag=RSCPTag.WB_REQ_SET_PARAM_1, rscp_type=RSCPType.Container, data=
            [RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA, rscp_type=RSCPType.ByteArray, data=param_1),
             RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA_LEN, rscp_type=RSCPType.UChar8, data=6)]
                                )
            r.append(req_data)

        for i in r:
            print(i)

        if len(r) > 0:
            try:
                res = self.gui.get_data(r, True)
                print(res)
                wx.MessageBox('Übertragung abgeschlossen')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')
        else:
            res = wx.MessageBox('Es wurden keine Änderungen gemacht, aktuelle Einstellungen trotzdem übertragen?',
                                'Wallbox speichern', wx.YES_NO)
            if res == wx.YES:
                r = []
                test_changed = self.chWBSunmode.GetValue()
                ba = bytearray(6)
                ba[0] = 1 if test_changed else 2
                req_data = RSCPDTO(tag=RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
                req_data += RSCPDTO(tag=RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data=index)
                req_data += RSCPDTO(tag=RSCPTag.WB_REQ_SET_EXTERN, rscp_type=RSCPType.Container, data=
                [RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA, rscp_type=RSCPType.ByteArray, data=ba),
                 RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA_LEN, rscp_type=RSCPType.UChar8, data=6)]
                                    )
                r.append(req_data)

                test_changed = self.chWB1PH.GetValue()
                ba = bytearray(6)
                ba[3] = 1 if test_changed else 3
                req_data = RSCPDTO(tag=RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
                req_data += RSCPDTO(tag=RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data=index)
                req_data += RSCPDTO(tag=RSCPTag.WB_REQ_SET_EXTERN, rscp_type=RSCPType.Container, data=
                [RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA, rscp_type=RSCPType.ByteArray, data=ba),
                 RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA_LEN, rscp_type=RSCPType.UChar8, data=6)]
                                    )
                r.append(req_data)

                test_changed = self.sWBLadestrom.GetValue()
                param_1[2] = test_changed
                req_data = RSCPDTO(tag=RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
                req_data += RSCPDTO(tag=RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data=index)
                req_data += RSCPDTO(tag=RSCPTag.WB_REQ_SET_PARAM_1, rscp_type=RSCPType.Container, data=
                [RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA, rscp_type=RSCPType.ByteArray, data=param_1),
                 RSCPDTO(tag=RSCPTag.WB_EXTERN_DATA_LEN, rscp_type=RSCPType.UChar8, data=6)]
                                    )
                r.append(req_data)

                for i in r:
                    print(i)

                try:
                    res = self.gui.get_data(r, True)
                    print(res)
                    wx.MessageBox('Übertragung abgeschlossen')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')

        self.pMainChanged()

    def sEMSMaxChargePowerOnScroll(self, event):
        self.txtEMSMaxChargePower.SetValue(str(self.sEMSMaxChargePower.GetValue()) + ' W')

    def sEMSMaxDischargePowerOnScroll(self, event):
        self.txtEMSMaxDischargePower.SetValue(str(self.sEMSMaxDischargePower.GetValue()) + ' W')

    def sEMSMaxDischargeStartPowerOnScroll(self, event):
        self.txtEMSMaxDischargeStartPower.SetValue(str(self.sEMSMaxDischargeStartPower.GetValue()) + ' W')

    def fill_info(self):
        RSCPGuiMain.fill_info(self)
        d = self._data_info

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
        self.gInfoFilesystem.SetValue(int(d['INFO_GET_FS_USAGE']['INFO_FS_USE_PERCENT'].data[:-1]))
        self.txtFilesystemPercent.SetValue(repr(d['INFO_GET_FS_USAGE']['INFO_FS_USE_PERCENT']))
        ts = repr(d['INFO_GET_FS_USAGE']['INFO_FS_USED']) + ' von ' + repr(d['INFO_GET_FS_USAGE']['INFO_FS_SIZE']) + ' in Verwendung, ' + repr(d['INFO_GET_FS_USAGE']['INFO_FS_AVAILABLE']) + ' frei'
        self.txtFilesystem.SetValue(ts)

        if 'INFO_MODULES_SW_VERSIONS' in d:
            self.gSoftwaremodules.Show()
            self.gSoftwaremodules.DeleteRows(0, self.gSoftwaremodules.GetNumberRows())
            self.gSoftwaremodules.AppendRows(len(d['INFO_MODULES_SW_VERSIONS']))
            row = 0
            regex = r"([\d\.]*) \[(.*)\] \(SVN:([\da-zA-Z]*)\)"

            for moduleversion in d['INFO_MODULES_SW_VERSIONS']:
                module = moduleversion['INFO_MODULE'].data
                self.gSoftwaremodules.SetCellValue(row, 0, module)
                versiondata = moduleversion['INFO_VERSION'].data
                try:

                    matches = re.findall(regex, versiondata)[0]
                    version = matches[0]
                    dt = matches[1]
                    svn = matches[2]
                    self.gSoftwaremodules.SetCellValue(row, 1, version)
                    self.gSoftwaremodules.SetCellValue(row, 2, dt)
                    self.gSoftwaremodules.SetCellValue(row, 3, svn)
                except Exception as e:
                    self.gSoftwaremodules.SetCellValue(row, 1, versiondata)
                    logger.error('Fehler beim Parsen der Modul-Software-Versionen (' + str(module) + ' / ' + str(versiondata) + '): ' + str(e))
                row+=1
            self.gSoftwaremodules.AutoSizeColumns()
        else:
            self.gSoftwaremodules.Hide()



    def fill_ems(self):
        RSCPGuiMain.fill_ems(self)
        d = self._data_ems

        self.fill_ems_basis(d)
        self.fill_ems_sys(d['EMS_GET_SYS_SPECS'])
        self.fill_ems_power(d)
        self.fill_ems_errors(d)

    def fill_ems_errors(self, d):
        logger.info(f'{d}')
        if 'EMS_STORED_ERRORS' in d:
            self.gStorederrors.Show()
            self.gStorederrors.DeleteRows(0, self.gStorederrors.GetNumberRows())
            self.gStorederrors.AppendRows(len(d['EMS_STORED_ERRORS']))
            row = 0
            for err in d['EMS_ERROR_CONTAINER']:
                type = err['EMS_ERROR_TYPE'].data
                self.gStorederrors.SetCellValue(row, 0, type)
                source = err['EMS_ERROR_SOURCE'].data
                self.gStorederrors.SetCellValue(row, 1, source)
                msg = err['EMS_ERROR_MESSAGE'].data
                self.gStorederrors.SetCellValue(row, 2, msg)
                code = err['EMS_ERROR_CODE'].data
                self.gStorederrors.SetCellValue(row, 3, str(code))
                ts = err['EMS_ERROR_TIMESTAMP'].data
                dd = datetime.datetime.fromtimestamp(ts)
                self.gStorederrors.SetCellValue(row, 4, dd.strftime(self._time_format))
                row+=1
            self.gStorederrors.AutoSizeColumns()
        else:
            self.gStorederrors.Hide()

    def fill_ems_basis(self, d = None):
        if not d:
            d = self.gui.get_data(self.gui.getEMSBasis(), True)

        self.txtEMSPowerPV.SetValue(repr(d['EMS_POWER_PV']) + ' W')
        self.txtEMSPowerHome.SetValue(repr(d['EMS_POWER_HOME']) + ' W')
        self.txtEMSPowerBat.SetValue(repr(d['EMS_POWER_BAT']) + ' W')
        self.txtEMSPowerGrid.SetValue(repr(d['EMS_POWER_GRID']) + ' W')
        self.txtEMSPowerAdd.SetValue(repr(d['EMS_POWER_ADD']) + ' W')
        self.txtEMSAutarkie.SetValue(str(round(d['EMS_AUTARKY'], 2)) + ' %')
        self.gEMSAutarkie.SetValue(int(round(d['EMS_AUTARKY'], 0)))
        self.txtEMSSelfConsumption.SetValue(str(round(d['EMS_SELF_CONSUMPTION'], 2)) + ' %')
        self.gEMSSelfConsumption.SetValue(int(round(d['EMS_SELF_CONSUMPTION'], 0)))
        self.txtEMSBatSoc.SetValue(str(round(d['EMS_BAT_SOC'], 2)) + ' %')
        self.mgEMSBatSoc.SetValue(round(d['EMS_BAT_SOC'], 0))
        self.txtEMSCouplingMode.SetValue(repr(d['EMS_COUPLING_MODE']))
        self.txtEMSMode.SetValue(repr(d['EMS_MODE']))
        balancedphases = "{0:b}".format(d['EMS_BALANCED_PHASES'].data).replace('1', 'X ').replace('0', '0 ')

        self.txtEMSBalancedPhases.SetValue(balancedphases)
        self.txtEMSExtSrcAvailable.SetValue(repr(d['EMS_EXT_SRC_AVAILABLE']))
        self._extsrcavailable = d['EMS_EXT_SRC_AVAILABLE'].data
        self.txtEMSInstalledPeakPower.SetValue(repr(d['EMS_INSTALLED_PEAK_POWER']) + ' Wp')
        self.txtEMSDerateAtPercent.SetValue(str(round(d['EMS_DERATE_AT_PERCENT_VALUE'], 3) * 100) + ' %')
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

        startcounter = d['EMS_GET_MANUAL_CHARGE']['EMS_MANUAL_CHARGE_START_COUNTER'].data / 1000
        dd = datetime.datetime.fromtimestamp(startcounter)
        self.txtEMSManualChargeStartCounter.SetValue(dd.strftime(self._time_format))

        self.txtEMSManualChargeEnergyCounter.SetValue(str(
            round(d['EMS_GET_MANUAL_CHARGE']['EMS_MANUAL_CHARGE_ENERGY_COUNTER'], 5)) + ' kWh')  # TODO: Einheit anfügen

        laststart = d['EMS_GET_MANUAL_CHARGE']['EMS_MANUAL_CHARGE_LASTSTART'].data
        dd = datetime.datetime.fromtimestamp(laststart)
        self.txtEMSManualChargeLaststart.SetValue(dd.strftime(self._time_format))

        self.chEPIsland.SetValue(d['EP_IS_ISLAND_GRID'].data)
        self.chEPReadyForSwitch.SetValue(d['EP_IS_READY_FOR_SWITCH'].data)
        self.chEPISGridConnected.SetValue(d['EP_IS_GRID_CONNECTED'].data)
        self.chEPPossible.SetValue(d['EP_IS_POSSIBLE'].data)
        self.chEPInvalid.SetValue(d['EP_IS_INVALID_STATE'].data)

    def fill_ems_power(self, d = None):

        if not d:
            d = self.gui.get_data(self.gui.getEMSPowerSettings() + self.gui.getEMSIdlePeriods() + self.gui.getEMSSysSpecs(), True)

        for sysspec in d['EMS_GET_SYS_SPECS']['EMS_SYS_SPEC']:
            if sysspec['EMS_SYS_SPEC_NAME'].data == 'maxStartChargePower':
                self.sEMSMaxDischargeStartPower.SetMax(sysspec['EMS_SYS_SPEC_VALUE_INT'].data)
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxChargePower':
                self.sEMSMaxChargePower.SetMax(sysspec['EMS_SYS_SPEC_VALUE_INT'].data)
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'maxDischargePower':
                self.sEMSMaxDischargePower.SetMax(sysspec['EMS_SYS_SPEC_VALUE_INT'].data)

        self.sEMSMaxChargePower.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_CHARGE_POWER'].data)
        self.txtEMSMaxChargePower.SetValue(repr(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_CHARGE_POWER']) + ' W')
        self.sEMSMaxDischargePower.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_DISCHARGE_POWER'].data)
        self.txtEMSMaxDischargePower.SetValue(repr(d['EMS_GET_POWER_SETTINGS']['EMS_MAX_DISCHARGE_POWER']) + ' W')
        self.sEMSMaxDischargeStartPower.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_DISCHARGE_START_POWER'].data)
        self.txtEMSMaxDischargeStartPower.SetValue(repr(d['EMS_GET_POWER_SETTINGS']['EMS_DISCHARGE_START_POWER']) + ' W')
        self.chEMSPowerLimitsUsed.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_POWER_LIMITS_USED'].data)
        self.chEMSPowerSaveEnabled.SetValue(d['EMS_GET_POWER_SETTINGS']['EMS_POWERSAVE_ENABLED'].data)
        self.chEMSWeatherRegulatedChargeEnabled.SetValue(
            d['EMS_GET_POWER_SETTINGS']['EMS_WEATHER_REGULATED_CHARGE_ENABLED'].data)

        if d['EMS_BATTERY_BEFORE_CAR_MODE'].data == 1:
            self.chEMSBatteryBeforeCarMode.SetValue(False)
        else:
            self.chEMSBatteryBeforeCarMode.SetValue(True)

        if d['EMS_BATTERY_TO_CAR_MODE'].data == 1:
            self.chEMSBatteryToCarMode.SetValue(True)
        else:
            self.chEMSBatteryToCarMode.SetValue(False)

        days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

        if 'EMS_GET_IDLE_PERIODS' in d and 'EMS_IDLE_PERIOD' in d['EMS_GET_IDLE_PERIODS']:
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
                self.__getattribute__(von).SetValue(
                    str(idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_HOUR'].data).zfill(2) + ':' + str(
                        idlePeriod['EMS_IDLE_PERIOD_START']['EMS_IDLE_PERIOD_MINUTE'].data).zfill(2))
                self.__getattribute__(bis).SetValue(
                    str(idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_HOUR'].data).zfill(2) + ':' + str(
                        idlePeriod['EMS_IDLE_PERIOD_END']['EMS_IDLE_PERIOD_MINUTE'].data).zfill(2))


    def fill_ems_sys(self, d = None):
        if not d:
            d = self.gui.get_data(self.gui.getEMSSysSpecs(), True)

        for sysspec in d['EMS_SYS_SPEC']:
            if sysspec['EMS_SYS_SPEC_NAME'].data == 'hybridModeSupported':
                self.txtEMSHybridModeSupported.SetValue(repr(sysspec['EMS_SYS_SPEC_VALUE_INT']))
            elif sysspec['EMS_SYS_SPEC_NAME'].data == 'installedBatteryCapacity':
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

    def fill_mbs(self):
        RSCPGuiMain.fill_mbs(self)
        d = self._data_mbs

        self.cbMBSProtokoll.Clear()

        self._mbsSettings = {}

        self.chMBSEnabled.SetValue(d['MBS_MODBUS_ENABLED'].data)
        if d['MBS_MODBUS_CONNECTORS']:
            for mbs in d['MBS_MODBUS_CONNECTORS']:
                if mbs.name == 'MBS_MODBUS_CONNECTOR_CONTAINER':
                    self.txtMBSName.SetValue(mbs['MBS_MODBUS_CONNECTOR_NAME'].data)
                    self.txtMBSID.SetValue(repr(mbs['MBS_MODBUS_CONNECTOR_ID']))

                    for setup in mbs['MBS_MODBUS_CONNECTOR_SETUP']:
                        if setup:
                            if setup['MBS_MODBUS_SETUP_NAME'].data == 'Protocol':
                                for value in setup['MBS_MODBUS_SETUP_VALUES']:
                                    self.cbMBSProtokoll.Append(value.data)
                                self.cbMBSProtokoll.SetValue(setup['MBS_MODBUS_SETUP_VALUE'].data)
                            elif setup['MBS_MODBUS_SETUP_NAME'].data == 'Device':
                                self.txtMBSDevice.SetValue(setup['MBS_MODBUS_SETUP_VALUE'].data)
                            elif setup['MBS_MODBUS_SETUP_NAME'].data == 'Port':
                                self.txtMBSPort.SetValue(setup['MBS_MODBUS_SETUP_VALUE'].data)

                            self._mbsSettings[setup['MBS_MODBUS_SETUP_NAME'].data] = setup['MBS_MODBUS_SETUP_VALUE']

    def fill_dcdc(self):
        RSCPGuiMain.fill_dcdc(self)

        for d in self._data_dcdc:
            index = int(d['DCDC_INDEX'])

            self.gDCDC.SetCellValue(0, index, str(round(d['DCDC_I_BAT'].data, 5)) + ' A')
            self.gDCDC.SetCellValue(1, index, str(round(d['DCDC_U_BAT'].data, 2)) + ' V')
            self.gDCDC.SetCellValue(2, index, str(round(d['DCDC_P_BAT'].data, 2)) + ' W')
            self.gDCDC.SetCellValue(3, index, str(round(d['DCDC_I_DCL'].data, 5)) + ' A')
            self.gDCDC.SetCellValue(4, index, str(round(d['DCDC_U_DCL'].data, 2)) + ' V')
            self.gDCDC.SetCellValue(5, index, str(round(d['DCDC_P_DCL'].data, 2)) + ' W')
            self.gDCDC.SetCellValue(6, index, repr(d['DCDC_FIRMWARE_VERSION']))
            self.gDCDC.SetCellValue(7, index, repr(d['DCDC_FPGA_FIRMWARE']))
            self.gDCDC.SetCellValue(8, index, repr(d['DCDC_SERIAL_NUMBER']))
            self.gDCDC.SetCellValue(9, index, str(repr(d['DCDC_BOARD_VERSION'])))
            self.gDCDC.SetCellValue(10, index, repr(d['DCDC_STATUS_AS_STRING']['DCDC_STATE_AS_STRING']))
            self.gDCDC.SetCellValue(11, index, repr(d['DCDC_STATUS_AS_STRING']['DCDC_SUBSTATE_AS_STRING']))
        self.gDCDC.AutoSize()
        logger.debug('Abruf DCDC-Daten abgeschlossen')

    def fill_pvi(self):
        selected = self.chPVIIndex.GetSelection()
        if selected in [wx.NOT_FOUND, '', None, False]:
            selected = 0

        self.chPVIIndex.Clear()

        RSCPGuiMain.fill_pvi(self)

        for k in self._data_pvi:
            pvi = self._data_pvi[k]
            self.chPVIIndex.Append('PVI #' + str(pvi['PVI_INDEX'].data))

        if selected != wx.NOT_FOUND:
            if self.chPVIIndex.GetCount() > selected:
                self.chPVIIndex.SetSelection(selected)
                self.fill_pvi_index(selected)

    def fill_pvi_index(self, index):
        data = self._data_pvi[index]

        self.txtPVISerialNumber.SetValue(repr(data['PVI_SERIAL_NUMBER']))
        self.txtPVIType.SetValue(repr(data['PVI_TYPE']))
        self.txtPVIVersionMain.SetValue(repr(data['PVI_VERSION']['PVI_VERSION_MAIN']))
        self.txtPVIVersionPic.SetValue(repr(data['PVI_VERSION']['PVI_VERSION_PIC']))
        self.txtPVITempCount.SetValue(repr(data['PVI_TEMPERATURE_COUNT']))
        self.chPVIOnGrid.SetValue(data['PVI_ON_GRID'].data)
        self.txtPVIStatus.SetValue(repr(data['PVI_STATE']))
        self.txtPVILastError.SetValue(repr(data['PVI_LAST_ERROR']))
        try:
            self.chPVICosPhiActive.SetValue(data['PVI_COS_PHI']['PVI_COS_PHI_IS_AKTIV'].data)
            self.txtPVICosPhiValue.SetValue(repr(data['PVI_COS_PHI']['PVI_COS_PHI_VALUE']))
            self.txtPVICosPhiExcited.SetValue(repr(data['PVI_COS_PHI']['PVI_COS_PHI_EXCITED']))
        except:
            logger.info('Keine COS-PHI-Werte verfügbar in PVI #' + str(index))
        self.txtPVIVoltageTrTop.SetValue(repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_THRESHOLD_TOP']))
        self.txtPVIVoltageTrBottom.SetValue(
            repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_THRESHOLD_BOTTOM']))
        self.txtPVIVoltageSlUp.SetValue(repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_SLOPE_UP']))
        self.txtPVIVoltageSlDown.SetValue(repr(data['PVI_VOLTAGE_MONITORING']['PVI_VOLTAGE_MONITORING_SLOPE_DOWN']))
        self.txtPVIPowerMode.SetValue(repr(data['PVI_POWER_MODE']))
        self.txtPVISystemMode.SetValue(repr(data['PVI_SYSTEM_MODE']))
        self.txtPVIMaxTemperature.SetValue(repr(data['PVI_MAX_TEMPERATURE']['PVI_VALUE']))
        self.txtPVIMinTemperature.SetValue(repr(data['PVI_MIN_TEMPERATURE']['PVI_VALUE']))
        self.txtPVIMaxApparentpower.SetValue(repr(data['PVI_AC_MAX_APPARENTPOWER']['PVI_VALUE']))
        if 'PVI_FREQUENCY_UNDER_OVER' in data:
            self.txtPVIFreqMin.SetValue(repr(data['PVI_FREQUENCY_UNDER_OVER']['PVI_FREQUENCY_UNDER']))
            self.txtPVIMaxFreq.SetValue(repr(data['PVI_FREQUENCY_UNDER_OVER']['PVI_FREQUENCY_OVER']))
        else:
            self.txtPVIFreqMin.SetValue('n/a')
            self.txtPVIMaxFreq.SetValue('n/a')

        self.chPVIDeviceConnected.SetValue(data['PVI_DEVICE_STATE']['PVI_DEVICE_CONNECTED'].data)
        self.chPVIDeviceWorking.SetValue(data['PVI_DEVICE_STATE']['PVI_DEVICE_WORKING'].data)
        self.chPVIDeviceInService.SetValue(data['PVI_DEVICE_STATE']['PVI_DEVICE_IN_SERVICE'].data)

        values = [{}, {}, {}]
        for d in data:
            if d.name in ['PVI_AC_POWER', 'PVI_AC_VOLTAGE', 'PVI_AC_CURRENT', 'PVI_AC_APPARENTPOWER',
                          'PVI_AC_REACTIVEPOWER', 'PVI_AC_ENERGY_ALL', 'PVI_AC_ENERGY_GRID_CONSUMPTION']:
                index = d['PVI_INDEX'].data
                values[index][d.name] = d['PVI_VALUE']
        sum_ac_power = sum_ac_energy_all = sum_ac_energy_grid = 0
        for i in range(0, 3):
            self.gPVIAC.SetCellValue(0, i, repr(values[i]['PVI_AC_POWER']) + ' W')
            sum_ac_power += values[i]['PVI_AC_POWER'].data
            self.gPVIAC.SetCellValue(1, i, repr(round(values[i]['PVI_AC_VOLTAGE'], 3)) + ' V')
            self.gPVIAC.SetCellValue(2, i, repr(round(values[i]['PVI_AC_CURRENT'], 5)) + ' A')
            self.gPVIAC.SetCellValue(3, i, repr(round(values[i]['PVI_AC_APPARENTPOWER'], 3)) + ' VA')
            self.gPVIAC.SetCellValue(4, i, repr(round(values[i]['PVI_AC_REACTIVEPOWER'], 3)) + ' VAr')
            self.gPVIAC.SetCellValue(5, i, repr(values[i]['PVI_AC_ENERGY_ALL']) + ' kWh')
            sum_ac_energy_all += values[i]['PVI_AC_ENERGY_ALL'].data
            self.gPVIAC.SetCellValue(6, i, repr(values[i]['PVI_AC_ENERGY_GRID_CONSUMPTION']) + ' kWh')
            sum_ac_energy_grid += values[i]['PVI_AC_ENERGY_GRID_CONSUMPTION'].data

        self.gPVIAC.SetCellValue(0, 3, str(round(sum_ac_power, 3)) + ' W')
        self.gPVIAC.SetCellValue(5, 3, str(round(sum_ac_energy_all, 3)) + ' kWh')
        self.gPVIAC.SetCellValue(6, 3, str(round(sum_ac_energy_grid, 3)) + ' kWh')

        values = [{}, {}]
        for d in data:
            if d.name in ['PVI_DC_POWER', 'PVI_DC_VOLTAGE', 'PVI_DC_CURRENT', 'PVI_DC_STRING_ENERGY_ALL']:
                index = d['PVI_INDEX'].data
                values[index][d.name] = d['PVI_VALUE']
        sum_dc_power = sum_dc_energy = 0
        for i in range(0, 2):
            self.gPVIDC.SetCellValue(0, i, repr(values[i]['PVI_DC_POWER']) + ' W')
            sum_dc_power += values[i]['PVI_DC_POWER'].data
            self.gPVIDC.SetCellValue(1, i, repr(values[i]['PVI_DC_VOLTAGE']) + ' V')
            self.gPVIDC.SetCellValue(2, i, str(round(values[i]['PVI_DC_CURRENT'], 5)) + ' A')
            self.gPVIDC.SetCellValue(3, i, str(round(values[i]['PVI_DC_STRING_ENERGY_ALL']) / 1000) + ' kWh')
            sum_dc_energy += values[i]['PVI_DC_STRING_ENERGY_ALL'].data

        self.gPVIDC.SetCellValue(0, 2, str(round(sum_dc_power, 3)) + ' W')
        self.gPVIDC.SetCellValue(3, 2, str(round(sum_dc_energy, 3) / 1000) + ' kWh')

        update = False
        if self.gPVITemps.GetNumberRows() != data['PVI_TEMPERATURE_COUNT'].data:
            self.gPVITemps.ClearGrid()
            self.gPVITemps.DeleteRows(numRows=self.gPVITemps.GetNumberRows())
            self.gPVITemps.AppendRows(data['PVI_TEMPERATURE_COUNT'].data)
            update = True

        for d in data:
            if d.name == 'PVI_TEMPERATURE':
                index = d['PVI_INDEX'].data
                self.gPVITemps.SetCellValue(index, 0, str(round(d['PVI_VALUE'], 3)) + ' °C')
                if update:
                    self.gPVITemps.SetRowLabelValue(index, u"Temperatur #" + str(index))

        if update:
            logger.debug('Autosize gPVI')
            self.gPVIAC.AutoSize()
            self.gPVIDC.AutoSize()
            self.gPVITemps.AutoSize()

    def fill_bat(self):
        selected = self.cbBATIndex.GetSelection()
        if selected in [wx.NOT_FOUND, '', None, False]:
            selected = 0

        self.cbBATIndex.Clear()
        RSCPGuiMain.fill_bat(self)
        for bat in self._data_bat:
            self.cbBATIndex.Append('BAT #' + str(bat['BAT_INDEX'].data))

        if selected != wx.NOT_FOUND:
            if self.cbBATIndex.GetCount() > selected:
                self.cbBATIndex.SetSelection(selected)
                self.fill_bat_index(selected)

    def fill_bat_index(self, index):
        logger.debug('Fülle BAT-Datenfelder')

        self.gDCB_row_voltages = None
        self.gDCB_row_temp = None
        self.gDCB_last_row = 30

        f = self._data_bat[index]

        # if index == 1:
        #    f['BAT_DCB_COUNT'].data = 1

        dcbcount = int(f['BAT_DCB_COUNT'])
        self.gDCB.DeleteCols(pos=0, numCols=self.gDCB.GetNumberCols())
        self.txtUsableCapacity.SetValue(str(round(f['BAT_USABLE_CAPACITY'], 5)) + ' Ah')
        self.txtUsableRemainingCapacity.SetValue(str(round(f['BAT_USABLE_REMAINING_CAPACITY'], 5)) + ' Ah')
        self.txtASOC.SetValue(str(round(f['BAT_ASOC'], 1)) + '%')
        self.txtFCC.SetValue(str(round(f['BAT_FCC'], 5)) + ' Ah')
        self.txtRC.SetValue(str(round(f['BAT_RC'], 5)) + ' Ah')
        self.txtRSOC.SetValue(str(round(f['BAT_INFO']['BAT_RSOC'], 1)) + '%')
        self.txtRSOCREAL.SetValue(str(round(f['BAT_RSOC_REAL'], 1)) + '%')
        self.txtModuleVoltage.SetValue(str(round(f['BAT_INFO']['BAT_MODULE_VOLTAGE'], 3)) + ' V')
        self.txtCurrent.SetValue(str(round(f['BAT_INFO']['BAT_CURRENT'], 5)) + ' A')
        self.txtBatStatusCode.SetValue(repr(f['BAT_INFO']['BAT_STATUS_CODE']))
        self.txtErrorCode.SetValue(repr(f['BAT_INFO']['BAT_ERROR_CODE']))
        self.txtDcbCount.SetValue(repr(f['BAT_DCB_COUNT']))
        logger.debug('Es müssen ' + str(dcbcount) + ' DCB-Spalten gefüllt werden')
        self.gDCB.AppendCols(dcbcount)
        for i in range(0, dcbcount):
            self.gDCB.SetColLabelValue(i, 'DCB #' + str(i))
        self.txtMaxBatVoltage.SetValue(str(round(f['BAT_MAX_BAT_VOLTAGE'],2)) + ' V')
        self.txtMaxChargeCurrent.SetValue(repr(f['BAT_MAX_CHARGE_CURRENT']) + ' A')
        self.txtEodVoltage.SetValue(repr(f['BAT_EOD_VOLTAGE']) + ' V')
        self.txtMaxDischargeCurrent.SetValue(repr(f['BAT_MAX_DISCHARGE_CURRENT']) + ' A')
        self.txtChargeCycles.SetValue(repr(f['BAT_CHARGE_CYCLES']))
        self.txtTerminalVoltage.SetValue(str(round(f['BAT_TERMINAL_VOLTAGE'],2)) + ' V')
        self.txtMaxDcbCellTemperature.SetValue(str(round(f['BAT_MAX_DCB_CELL_TEMPERATURE'], 2)) + ' °C')
        self.txtMinDcbCellTemperature.SetValue(str(round(f['BAT_MIN_DCB_CELL_TEMPERATURE'], 2)) + ' °C')

        self.chBATDeviceConnected.SetValue(f['BAT_DEVICE_STATE']['BAT_DEVICE_CONNECTED'].data)
        self.chBATDeviceWorking.SetValue(f['BAT_DEVICE_STATE']['BAT_DEVICE_WORKING'].data)
        self.chBATDeviceInService.SetValue(f['BAT_DEVICE_STATE']['BAT_DEVICE_IN_SERVICE'].data)

        self.txtBATMaxDCBCount.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_MAX_DCB_COUNT']))
        self.txtBATCapacity.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_CAPACITY']) + ' Wh')
        self.txtBATMaxChargePower.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_CHARGE_POWER']) + ' W')
        self.txtBATMaxDischargePower.SetValue(repr(f['BAT_SPECIFICATION']['BAT_SPECIFIED_DSCHARGE_POWER']) + ' W')

        self.txtBATMeasuredResistance.SetValue(str(round(f['BAT_INTERNALS']['BAT_MEASURED_RESISTANCE'],5)))
        self.txtBATRunMeasuredResistance.SetValue(str(round(f['BAT_INTERNALS']['BAT_RUN_MEASURED_RESISTANCE'],5)))

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

        logger.debug('BAT Datenfelder gefüllt')

        def set_voltages(d):
            if d.type == RSCPType.Error:
                logger.warning('BAT_DCB_ALL_CELL_VOLTAGES konnte nicht abgerufen werden')
            else:
                index = int(d['BAT_DCB_INDEX'])
                if index < dcbcount:
                    logger.debug('Fülle Spannungen für DCB #' + str(index))
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
                    logger.debug('Spannungen für DCB #' + str(index) + ' gefüllt')

        def set_temperatures(d):
            if d.type == RSCPType.Error:
                logger.warning('BAT_DCB_ALL_CELL_TEMPERATURES konnte nicht abgerufen werden')
            else:
                index = int(d['BAT_DCB_INDEX'])
                if index < dcbcount:
                    logger.debug('Fülle Temperaturen für DCB #' + str(index))
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

                    logger.debug('Temperaturen für DCB #' + str(index) + ' gefüllt')

        def set_info(d):
            if d.type == RSCPType.Error:
                logger.warning('BAT_DCB_INFO konnte nicht abgerufen werden')
            else:
                index = int(d['BAT_DCB_INDEX'])
                if index < dcbcount:
                    logger.debug('Fülle weitere Infos für DCB #' + str(index))
                    dd = datetime.datetime.fromtimestamp(int(d['BAT_DCB_LAST_MESSAGE_TIMESTAMP']) / 1000)
                    self.gDCB.SetCellValue(0, index, str(dd))
                    self.gDCB.SetCellValue(1, index, str(round(d['BAT_DCB_MAX_CHARGE_VOLTAGE'],3)) + ' V')
                    self.gDCB.SetCellValue(2, index, str(round(d['BAT_DCB_MAX_CHARGE_CURRENT'],5)) + ' A')
                    self.gDCB.SetCellValue(3, index, str(round(d['BAT_DCB_END_OF_DISCHARGE'],3)) + ' V')
                    self.gDCB.SetCellValue(4, index, str(round(d['BAT_DCB_MAX_DISCHARGE_CURRENT'],5)) + ' A')
                    self.gDCB.SetCellValue(5, index, str(round(d['BAT_DCB_FULL_CHARGE_CAPACITY'], 5)) + ' Ah')
                    self.gDCB.SetCellValue(6, index, str(round(d['BAT_DCB_REMAINING_CAPACITY'], 5)) + ' Ah')
                    self.gDCB.SetCellValue(7, index, str(round(d['BAT_DCB_SOC'],2)) + '%')
                    self.gDCB.SetCellValue(8, index, str(round(d['BAT_DCB_SOH'],2)) + '%')
                    self.gDCB.SetCellValue(9, index, str(round(d['BAT_DCB_CYCLE_COUNT'],0)))
                    self.gDCB.SetCellValue(10, index, str(round(d['BAT_DCB_CURRENT'], 5)) + ' A')
                    self.gDCB.SetCellValue(11, index, str(round(d['BAT_DCB_VOLTAGE'], 2)) + ' V')
                    self.gDCB.SetCellValue(12, index, str(round(d['BAT_DCB_CURRENT_AVG_30S'], 5)) + ' A')
                    self.gDCB.SetCellValue(13, index, str(round(d['BAT_DCB_VOLTAGE_AVG_30S'], 2)) + ' V')
                    self.gDCB.SetCellValue(14, index, str(round(d['BAT_DCB_DESIGN_CAPACITY'], 5)) + ' Ah')
                    self.gDCB.SetCellValue(15, index, str(round(d['BAT_DCB_DESIGN_VOLTAGE'],2)) + ' V')
                    self.gDCB.SetCellValue(16, index, str(round(d['BAT_DCB_CHARGE_LOW_TEMPERATURE'],3)) + ' °C')
                    self.gDCB.SetCellValue(17, index, str(round(d['BAT_DCB_CHARGE_HIGH_TEMPERATURE'],3)) + ' °C')
                    self.gDCB.SetCellValue(18, index, repr(d['BAT_DCB_MANUFACTURE_NAME']))
                    self.gDCB.SetCellValue(19, index, repr(d['BAT_DCB_DEVICE_NAME']))
                    self.gDCB.SetCellValue(20, index, repr(d['BAT_DCB_MANUFACTURE_DATE']))
                    self.gDCB.SetCellValue(21, index, repr(d['BAT_DCB_SERIALNO']))
                    self.gDCB.SetCellValue(22, index, repr(d['BAT_DCB_FW_VERSION']))
                    self.gDCB.SetCellValue(23, index, repr(d['BAT_DCB_PCB_VERSION']))
                    self.gDCB.SetCellValue(24, index, repr(d['BAT_DCB_DATA_TABLE_VERSION']))
                    self.gDCB.SetCellValue(25, index, repr(d['BAT_DCB_PROTOCOL_VERSION']))
                    self.gDCB.SetCellValue(26, index, repr(d['BAT_DCB_NR_SERIES_CELL']))
                    self.gDCB.SetCellValue(27, index, repr(d['BAT_DCB_NR_PARALLEL_CELL']))
                    self.gDCB.SetCellValue(28, index, repr(d['BAT_DCB_SERIALCODE']))
                    self.gDCB.SetCellValue(29, index, repr(d['BAT_DCB_NR_SENSOR']))
                    self.gDCB.SetCellValue(30, index, repr(d['BAT_DCB_STATUS']))
                    logger.debug('Weitere Infos für DCB #' + str(index) + ' gefüllt')

        if dcbcount > 1:
            for d in f['BAT_DCB_ALL_CELL_TEMPERATURES']:
                set_temperatures(d)
            for d in f['BAT_DCB_ALL_CELL_VOLTAGES']:
                set_voltages(d)
            for d in f['BAT_DCB_INFO']:
                set_info(d)
        else:
            set_temperatures(f['BAT_DCB_ALL_CELL_TEMPERATURES'])
            set_voltages(f['BAT_DCB_ALL_CELL_VOLTAGES'])
            set_info(f['BAT_DCB_INFO'])

        logger.debug('BAT-Datenfelder füllen abgeschlossen')

    def fill_pm(self):
        RSCPGuiMain.fill_pm(self)
        update = False

        if self.gPM.GetNumberCols() > len(self._data_pm):
            logger.debug('Lösche alle Spalten in gPM')
            self.gPM.DeleteCols(numCols=self.gPM.GetNumberCols())
            update = True

        while self.gPM.GetNumberCols() < len(self._data_pm.keys()):
            logger.debug('Füge eine Spalte in gPM hinzu')
            self.gPM.AppendCols(1)
            update = True

        curcol = 0
        for index in self._data_pm.keys():
            d = self._data_pm[index]

            self.gPM.SetColLabelValue(curcol, 'PM #' + str(index))
            self.gPM.SetCellValue(0, curcol, str(round(d['PM_POWER_L1'], 3)) + ' W')
            self.gPM.SetCellValue(1, curcol, str(round(d['PM_POWER_L2'], 3)) + ' W')
            self.gPM.SetCellValue(2, curcol, str(round(d['PM_POWER_L3'], 3)) + ' W')
            self.gPM.SetCellValue(3, curcol, str(
                round(d['PM_POWER_L1'].data + d['PM_POWER_L2'].data + d['PM_POWER_L3'].data, 3)) + ' W')
            self.gPM.SetCellValue(4, curcol, str(round(d['PM_VOLTAGE_L1'], 3)) + ' V')
            self.gPM.SetCellValue(5, curcol, str(round(d['PM_VOLTAGE_L2'], 3)) + ' V')
            self.gPM.SetCellValue(6, curcol, str(round(d['PM_VOLTAGE_L3'], 3)) + ' V')

            energy, einheit = self.get_einheit(d['PM_ENERGY_L1'].data)
            self.gPM.SetCellValue(7, curcol, str(round(energy, 3)) + ' ' + einheit)
            energy, einheit = self.get_einheit(d['PM_ENERGY_L2'].data)
            self.gPM.SetCellValue(8, curcol, str(round(energy, 3)) + ' ' + einheit)
            energy, einheit = self.get_einheit(d['PM_ENERGY_L3'].data)
            self.gPM.SetCellValue(9, curcol, str(round(energy, 3)) + ' ' + einheit)
            energy, einheit = self.get_einheit(d['PM_ENERGY_L1'].data + d['PM_ENERGY_L2'].data + d['PM_ENERGY_L3'].data)
            self.gPM.SetCellValue(10, curcol, str(round(energy, 3)) + ' ' + einheit)

            self.gPM.SetCellValue(11, curcol, repr(d['PM_FIRMWARE_VERSION']))
            self.gPM.SetCellValue(12, curcol, repr(d['PM_ACTIVE_PHASES']))
            self.gPM.SetCellValue(13, curcol, repr(d['PM_MODE']))
            self.gPM.SetCellValue(14, curcol, repr(d['PM_ERROR_CODE']))
            self.gPM.SetCellValue(15, curcol, repr(d['PM_TYPE']))
            self.gPM.SetCellValue(16, curcol, repr(d['PM_DEVICE_ID']))
            if 'PM_IS_CAN_SILENCE' in d:
                self.gPM.SetCellValue(17, curcol, repr(d['PM_IS_CAN_SILENCE']))
            else:
                self.gPM.SetCellValue(17, curcol, 'n/a')
            self.gPM.SetCellValue(28, curcol, repr(d['PM_DEVICE_STATE']['PM_DEVICE_CONNECTED']))
            self.gPM.SetCellValue(29, curcol, repr(d['PM_DEVICE_STATE']['PM_DEVICE_WORKING']))
            self.gPM.SetCellValue(30, curcol, repr(d['PM_DEVICE_STATE']['PM_DEVICE_IN_SERVICE']))

            if 'PM_COMM_STATE' in d:
                d = d['PM_COMM_STATE']
                self.gPM.SetCellValue(18, curcol, repr(d['PM_CS_START_TIME']))
                self.gPM.SetCellValue(19, curcol, repr(d['PM_CS_LAST_TIME']))
                self.gPM.SetCellValue(20, curcol, repr(d['PM_CS_SUCC_FRAMES_ALL']))
                self.gPM.SetCellValue(21, curcol, repr(d['PM_CS_SUCC_FRAMES_100']))
                self.gPM.SetCellValue(22, curcol, repr(d['PM_CS_EXP_FRAMES_ALL']))
                self.gPM.SetCellValue(23, curcol, repr(d['PM_CS_EXP_FRAMES_100']))
                self.gPM.SetCellValue(24, curcol, repr(d['PM_CS_ERR_FRAMES_ALL']))
                self.gPM.SetCellValue(25, curcol, repr(d['PM_CS_ERR_FRAMES_100']))
                self.gPM.SetCellValue(26, curcol, repr(d['PM_CS_UNK_FRAMES']))
                self.gPM.SetCellValue(27, curcol, repr(d['PM_CS_ERR_FRAME']))
            curcol+=1

        if update:
            self.gPM.AutoSize()

    def get_einheit(self, value):
        if abs(value) > 10000:
            if abs(value) > 10000000:
                return round(value / 1000000,3), 'MWh'
            else:
                return round(value / 1000,3), 'kWh'
        else:
            return round(value,3), 'Wh'

    def fill_wb(self):
        selected = self.cbWallbox.GetSelection()
        if selected in [wx.NOT_FOUND, '', None, False]:
            selected = 0

        self.cbWallbox.Clear()

        RSCPGuiMain.fill_wb(self)

        if len(self._data_wb) == 0:
            self.cbWallbox.Append('keine Wallbox vorhanden')
        else:
            for wb in self._data_wb:
                index = wb['WB_INDEX'].data
                self.cbWallbox.Append('WB #' + str(index))

            if selected != wx.NOT_FOUND:
                if self.cbWallbox.GetCount() > selected:
                    self.cbWallbox.SetSelection(selected)
                    self.fill_wb_index(selected)

    def fill_wb_index(self, index):
        if len(self._data_wb) > index:
            logger.debug('Stelle Daten der Wallbox #' + str(index) + ' dar')
            d = self._data_wb[index]
            for val in d:
                print(val)

            index = d['WB_INDEX'].data
            wallbox_type = WB_TYPE.E3DC if d['WB_DEVICE_NAME'].data != 'Easy Connect' else WB_TYPE.EASYCONNECT

            self.txtWBStatus.SetValue(repr(d['WB_STATUS']))
            energy, einheit = self.get_einheit(d['WB_ENERGY_ALL'].data)
            self.txtWBEnergyAll.SetValue(str(round(energy,3)) + ' ' + einheit)
            energy, einheit = self.get_einheit(d['WB_ENERGY_SOLAR'].data)
            self.txtWBEnergySolar.SetValue(str(round(energy,3)) + ' ' + einheit)
            self.txtWBSOC.SetValue(repr(d['WB_SOC']))
            self.txtWBErrorCode.SetValue(repr(d['WB_ERROR_CODE']))
            self.txtWBDeviceName.SetValue(repr(d['WB_DEVICE_NAME']))
            #self.txtWBMode.SetValue(repr(d['WB_MODE']))

            self.gWBData.SetCellValue(0, 0, str(round(d['WB_PM_POWER_L1'], 3)) + ' W')
            self.gWBData.SetCellValue(0, 1, str(round(d['WB_PM_POWER_L2'], 3)) + ' W')
            self.gWBData.SetCellValue(0, 2, str(round(d['WB_PM_POWER_L3'], 3)) + ' W')
            self.gWBData.SetCellValue(0, 3, str(
                round(d['WB_PM_POWER_L1'].data + d['WB_PM_POWER_L2'].data + d['WB_PM_POWER_L3'].data, 3)) + ' W')

            energy, einheit = self.get_einheit(d['WB_PM_ENERGY_L1'].data)
            self.gWBData.SetCellValue(1, 0, str(round(energy,3)) + ' ' + einheit)
            energy, einheit = self.get_einheit(d['WB_PM_ENERGY_L1'].data)
            self.gWBData.SetCellValue(1, 1, str(round(energy,3)) + ' ' + einheit)
            energy, einheit = self.get_einheit(d['WB_PM_ENERGY_L2'].data)
            self.gWBData.SetCellValue(1, 2, str(round(energy,3)) + ' ' + einheit)
            energy, einheit = self.get_einheit(d['WB_PM_ENERGY_L1'].data + d['WB_PM_ENERGY_L2'].data + d['WB_PM_ENERGY_L3'].data)
            self.gWBData.SetCellValue(1, 3, str(round(energy,3)) + ' ' + einheit)

            self.chWBDeviceConnected.SetValue(d['WB_DEVICE_STATE']['WB_DEVICE_CONNECTED'].data)
            self.chWBDeviceInService.SetValue(d['WB_DEVICE_STATE']['WB_DEVICE_IN_SERVICE'].data)
            self.chWBDeviceWorking.SetValue(d['WB_DEVICE_STATE']['WB_DEVICE_WORKING'].data)

            alg_data = d['WB_EXTERN_DATA_ALG']['WB_EXTERN_DATA'].data
            sb = alg_data[2]
            if wallbox_type == WB_TYPE.E3DC:
                self.sWBLadestrom.SetValue(alg_data[3])
            else:
                self.sWBLadestrom.SetValue(alg_data[4])

            self.chWB1PH.SetValue(alg_data[1] == 1)
            self.sWBLadestromOnScroll(None)

            status = []

            if (sb & 64) == 64:
                logger.debug('WB charging canceled True')
                status.append('Ladenvorgang abgebrochen')
            else:
                logger.debug('WB charging canceled False')
            if (sb & 32) == 32:
                logger.debug('WB charging active True')
                status.append('Ladevorgang aktiv')
            else:
                logger.debug('WB charging active False')

            if sb == 0:
                status.append('Kein Auto angesteckt')

            self.chWBSunmode.SetValue((sb & 128) == 128)

            def get_load(data):
                return data[1] << 8 | data[0]

            sunload = get_load(d['WB_EXTERN_DATA_SUN']['WB_EXTERN_DATA'].data)
            self.txtWBSun.SetValue(str(sunload) + ' W')

            netload = get_load(d['WB_EXTERN_DATA_NET']['WB_EXTERN_DATA'].data)
            self.txtWBNet.SetValue(str(netload) + ' W')

            wbload = sunload+netload
            self.txtWBLadeleistung.SetValue(str(wbload) + ' W')

            if wallbox_type == WB_TYPE.E3DC:
                if len(status) > 0:
                    self.txtWBMode.SetValue(','.join(status))
                else:
                    if wbload > 0:
                        self.txtWBMode.SetValue(WB_MODE.LOADING.name)
                    else:
                        self.txtWBMode.SetValue(WB_MODE.NOT_LOADING.name)
            else:
                self.txtWBMode.SetValue(repr(d['WB_MODE']))

            logger.debug('Darstellung Wallbox abgeschlossen')
        else:
            logger.debug('Daten für Wallbox #' + str(index) + ' existieren nicht, Darstellung abgebrochen')

    def bSaveClick(self, event):
        self.saveConfig()

        # rscp = self.gui.get_data(self.gui.getUserLevel(), True)
        # ems = self.gui.get_data(self.gui.getEMSData() + self.gui.getUserLevel(), True)

    def bSYSRebootOnClick(self, event):
        res = wx.MessageBox("Soll das gesamte E3/DC - System wirklich neu gestartet werden?\nEs wird das gesamte System neu gestartet, dieser Vorgang dauert etwa 5 Minuten, während dieser Zeit ist das System nicht erreichbar.", "Systemneustart",
                            wx.YES_NO | wx.ICON_WARNING)
        if res == wx.YES:
            try:
                r = RSCPTag.SYS_REQ_SYSTEM_REBOOT
                res = self.gui.get_data([r], True)
                wx.MessageBox('System wird neu gestartet')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')

    def bSYSApplicationRestartOnClick(self, event):
        res = wx.MessageBox("Soll die Anwendung im E3/DC wirklich neu gestartet werden?\nDas System ist dabei für etwa eine Minute nicht erreichbar.", 'Applikations - Neustart',
                            wx.YES_NO | wx.ICON_WARNING)
        if res == wx.YES:
            try:
                r = RSCPTag.SYS_REQ_RESTART_APPLICATION
                res = self.gui.get_data([r], True)
                wx.MessageBox('Anwendung wird neu gestartet')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')

    def bEMSEPTestOnClick(self, event):
        res = wx.MessageBox('Beim Notstromtest wird kurz der Hausstrom gekappt.\nNach etwa 10-15 Sekunden sollte dann '
                            'der Notstrom einspringen und\nStrom wieder zur Verfügung stehen.\nEs wird dann auf Notstrom'
                            ' umgestellt. Nach dem Test wird der\nNotstrom wieder beendet, der Hausstrom wird wieder '
                            'getrennt für ca. 2 Sekunden.\n\nSoll der Notstrom-Test wirklich durchgeführt werden?',
                            'Notstrom-Test', wx.YES_NO | wx.ICON_WARNING)
        if res == wx.YES:
            try:
                r = RSCPDTO(tag=RSCPTag.EMS_REQ_START_EMERGENCYPOWER_TEST, rscp_type=RSCPType.Bool, data=True)
                print(r)
                res = self.gui.get_data([r], True)
                print(res)
                wx.MessageBox('Notstromtest wird durchgeführt')
            except:
                traceback.print_exc()
                wx.MessageBox('Übertragung fehlgeschlagen')

    def bEMSManualChargeStartOnClick(self, event):
        try:
            val = int(self.txtEMSManualChargeValue.GetValue())
        except:
            val = 0
        if val > 0:
            res = wx.MessageBox(
                'Die manuelle Ladung ist auf die Ausführung einmal am Tag begrenzt, steht nicht genügend PV-Leistung zur Verfügung, wird Netzstrom bezogen! Fortfahren?',
                'Manuelle Ladung', wx.YES_NO | wx.ICON_QUESTION)
            if res == wx.YES:
                try:
                    r = RSCPDTO(tag=RSCPTag.EMS_REQ_START_MANUAL_CHARGE, rscp_type=RSCPType.Uint32, data=val)
                    res = self.gui.get_data([r], True)
                    if res.name == 'EMS_START_MANUAL_CHARGE' and res.data:
                        wx.MessageBox('Manuelle Ladung gestartet')
                    else:
                        wx.MessageBox('Fehler beim Start der manuellen Ladung, heute bereits durchgeführt?')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')
        else:
            wx.MessageBox(
                'Die Ladung von (' + self.txtEMSManualChargeValue.GetValue() + ') Wh ist nicht zulässig, bitte anderen Ganzzahl-Wert wählen',
                'Manuelle Ladung', wx.ICON_WARNING)

    def bTestClick(self, event):
        self.disableButtons()

        try:
            if not self.gui:
                raise Exception('Keine Verbindungsart möglich')

            logger.debug('Teste Verbindung')
            result = self.gui.get_data(self.gui.getInfo(), True)

            sn = repr(result['INFO_SERIAL_NUMBER'])
            ip = repr(result['INFO_IP_ADDRESS'])
            rel = repr(result['INFO_SW_RELEASE'])

            if isinstance(self.gui, E3DCWebGui) and self.cfgLoginconnectiontype == 'web':
                msg = wx.MessageBox('Verbindung per Web mit System ' + sn + ' / ' + rel + ' hergestellt', 'Info',
                                    wx.OK | wx.ICON_INFORMATION)
            elif isinstance(self.gui, E3DCWebGui) and self.txtRSCPPassword.GetValue() == '':
                msg = wx.MessageBox(
                    'Verbindung mit System ' + sn + ' / ' + rel + ' konnte nur über WebSockets hergestellt werden, da kein RSCP-Passwort vergeben wurde.\nDiese Verbindung ist langsamer und auf das Internet angewiesen.\n',
                    'Info',
                    wx.OK | wx.ICON_WARNING)
            elif isinstance(self.gui, E3DCWebGui) and self.txtRSCPPassword.GetValue() != '':
                msg = wx.MessageBox(
                    'Verbindung mit System ' + sn + ' / ' + rel + ' konnte nur über WebSockets hergestellt werden, da das angegebene RSCP-Passwort falsch ist oder das E3DC nicht direkt erreichbar ist.\nDiese Verbindung ist langsamer und auf das Internet angewiesen.',
                    'Info',
                    wx.OK | wx.ICON_WARNING)
            else:
                msg = wx.MessageBox('Verbindung direkt mit System  ' + sn + ' / ' + rel + ' hergestellt', 'Info',
                                    wx.OK | wx.ICON_INFORMATION)

            logger.debug('Verbindungstest erfolgreich. Verbindungsart: ' + self.connectiontype)
        except:
            logger.exception('Verbindungstest nicht erfolgreich')
            msg = wx.MessageBox('Verbindung konnte nicht aufgebaut werden', 'Error',
                                wx.OK | wx.ICON_ERROR)

        self.enableButtons()

    def bUpdateCheckClick(self, event):
        try:
            result = self.gui.get_data(self.gui.getCheckForUpdates(), True)
            status = result.data
        except:
            traceback.print_exc()
            status = 0

        if status == 1:
            wx.MessageBox(
                'Updatecheck wird ausgeführt, wenn eine neue Version zur Verfügung steht wird diese installiert.')
        else:
            wx.MessageBox('Updatecheck konnte nicht ausgeführt werden')

    def disableButtons(self):
        logger.debug('Deaktiviere Buttons')
        self.enableDisableButtons(False)

    def enableButtons(self):
        logger.debug('Aktiviere Buttons')
        self.enableDisableButtons(True)
        self.set_wb_enabled()

    def enableDisableButtons(self, value=True):
        self.bUpdate.Enable(value)
        self.bEMSEPTest.Enable(value)
        self.bEMSManualChargeStart.Enable(value)
        self.bSave.Enable(value)
        self.bTest.Enable(value)
        self.bConfigGetIPAddress.Enable(value)
        self.bConfigGetSerialNo.Enable(value)
        self.bConfigSetRSCPPassword.Enable(value)
        self.bEMSUploadChanges.Enable(value)
        self.bINFOSave.Enable(value)
        self.bSYSApplicationRestart.Enable(value)
        self.bSYSReboot.Enable(value)
        self.btnUpdatecheck.Enable(value)
        self.bUpload.Enable(value)
        self.bWBSave.Enable(value)
        self.bWBStopLoading.Enable(value)
        self.bUploadStart.Enable(value)
        if not self._e3dcexportFrame:
            self.bUploadSetData.Enable(value)
        self.cbBATIndex.Enable(value)
        self.cbWallbox.Enable(value)
        self.chPVIIndex.Enable(value)


    def sWBLadestromOnScroll(self, event):
        self.stWBLadestrom.SetLabel(str(self.sWBLadestrom.GetValue()) + ' A')

    def bUpdateClick(self, event=None):
        page = self.pMainregister.GetCurrentPage()
        name = page.GetName()
        if name == 'CONFIG':
            self._updatethread = threading.Thread(target=self.updateData, args=())
            self._updatethread.start()
        else:
            self.pMainChanged()

    def updateData(self):
        if not self._updateRunning:
            self._updateRunning = True
            self.disableButtons()
            self.gaUpdate.SetValue(0)
            try:
                self.gaUpdate.SetValue(5)
                if self.gui:
                    self.gaUpdate.SetValue(10)
                    logger.info('Aktualisiere Daten')
                    self.clear_values()

                    try:
                        self.fill_info()
                    except:
                        logger.exception('Fehler beim Abruf der INFO-Daten')

                    self.gaUpdate.SetValue(20)
                    try:
                        self.fill_bat()
                    except:
                        logger.exception('Fehler beim Abruf der BAT-Daten')

                    self.gaUpdate.SetValue(35)
                    try:
                        self.fill_dcdc()
                    except:
                        logger.exception('Fehler beim Abruf der DCDC-Daten')

                    self.gaUpdate.SetValue(45)
                    try:
                        selected = self.chPVIIndex.GetSelection()
                        if selected in [wx.NOT_FOUND, '', None, False]:
                            selected = 0

                        self.fill_pvi()

                        if selected != wx.NOT_FOUND:
                            if self.chPVIIndex.GetCount() > selected:
                                self.chPVIIndex.SetSelection(selected)
                                self.fill_pvi_index(selected)
                    except:
                        logger.exception('Fehler beim Abruf der PVI-Daten')

                    self.gaUpdate.SetValue(55)
                    try:
                        self.fill_ems()
                        self.fill_mbs()
                    except:
                        logger.exception('Fehler beim Abruf der EMS-Daten')

                    self.gaUpdate.SetValue(70)
                    try:
                        self.fill_pm()
                    except:
                        logger.exception('Fehler beim Abruf der PM-Daten')

                    self.gaUpdate.SetValue(85)
                    try:
                        self.fill_wb()
                    except:
                        logger.exception('Fehler beim Abruf der WB-Daten')

                    try:
                        self.fill_mbs()
                    except:
                        logger.exception('Fehler beim Abruf der Modbus-Daten')

                    self.gaUpdate.SetValue(90)
                else:
                    logger.warning('Konfiguration unvollständig, Verbindung nicht möglich')

            except:
                logger.exception('Fehler beim Aktualisieren der Daten')
            self.gaUpdate.SetValue(100)
            self.enableButtons()
            self._updateRunning = False

    def bMBSSaveOnClick(self, event):
        r = []
        test = self.chMBSEnabled.GetValue()
        if test != self._data_mbs['MBS_MODBUS_ENABLED'].data:
            r.append(RSCPDTO(tag=RSCPTag.MBS_REQ_SET_MODBUS_ENABLED, rscp_type=RSCPType.Bool, data=test))

        if len(r) == 0:
            res = wx.MessageBox('Es wurden keine Änderungen gemacht, aktuelle Einstellungen trotzdem übertragen?',
                                'Modbus-Einstellungen speichern', wx.YES_NO)
            if res == wx.YES:
                test = self.chMBSEnabled.GetValue()
                r.append(RSCPDTO(tag=RSCPTag.MBS_REQ_SET_MODBUS_ENABLED, rscp_type=RSCPType.Bool, data=test))

        if len(r) > 0:
            res = wx.MessageBox(
                'Eine Änderung der Modbus-Einstellungen unterbricht kurz die Kommunikation, laufende RSCP-Verbindungen werden direkt beendet. Fortfahren?',
                'Modbus-Einstellungen speichern', wx.YES_NO | wx.ICON_WARNING)
            if res == wx.YES:
                try:
                    res = self.gui.get_data(r, True)
                    wx.MessageBox('Übertragung abgeschlossen')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')

                self.pMainChanged()

        event.Skip()

    def bSaveRSCPDataOnClick(self, event):
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
                logger.exception('Daten konnten nicht in Datei gespeichert werden ' + pathname)
                wx.LogError("Cannot save current data in file '%s'." % pathname)

        event.Skip()

    def sendToServer(self, event):
        ret = wx.MessageBox(
            'Achtung, es werden alle angezeigten Daten an externe Stelle übermittelt.\nSeriennummern werden in anonymisierter Form übermittelt.\nZugangsdaten werden nicht übermittelt.\nDie Datenübertragung erfolgt verschlüsselt.\nWirklich fortfahren?',
            caption='Ausgelesene Daten übermitteln',
            style=wx.YES_NO)
        if ret == wx.YES:
            logger.debug('Sende Daten an Server')
            status = 'NO CODE'
            try:
                data = self.sammle_data()

                r = requests.post(url=self.txtDBServer.GetValue(), json=data)
                r.raise_for_status()
                res = r.json()
                if 'error' in res:
                    raise Exception('Fehler bei Datenübermittlung' + res['error'])

                if 'success' in res:
                    logger.debug('Datenübertragung erfolgreich Speicherpfad: ' + res['success'])
                    self.MessageBox(self, 'Übermittlung Erfolgreich',
                                    'Daten wurden erfolgreich übermittelt!\nSpeicherpfad:\n\n' + res['success'])


            except:
                logger.exception('Fehler bei der Datenübertragung an Server ' + self.txtDBServer.GetValue())
                wx.MessageBox('Es gab einen Fehler bei der Übermittlung. (HTTP-Status: ' + str(r.status_code) + ')')

    def mainOnClose(self, event):
        if isinstance(self._gui, E3DCWebGui):
            self._gui.e3dc.ws.close()

        event.Skip()

    def bPortalUploadOnClick(self, event):
        response = self.sendToPortalMin()
        if response:
            self.fill_portal()
            if response['msg'] == 'success':
                link = 'https://pv.pincrushers.de/rscpgui/' + response['filename']
                logger.info('Daten abgelegt unter: ' + link)

                wx.MessageBox('Daten an Server übermittelt. Datenlink: ' + link)
            else:
                wx.MessageBox('Daten konnte nicht übermittelt werden, Response: ' + response['hint'])
        else:
            wx.MessageBox('Daten konnten nicht übermittelt werden')

    def bPortalDeleteOnClick(self, event):
        response = self.deleteFromPortal()
        if response:
            self.fill_portal()
            if response['msg'] == 'success':
                logger.info('Daten gelöscht')

                wx.MessageBox('Alle Datensätze zu deinem System wurden gelöscht')

            else:
                wx.MessageBox('Datensätze konnten nicht gelöscht werden, Response: ' + response['hint'])
        else:
            wx.MessageBox('Datensätze konnten nicht gelöscht werden')

    def gPortalListOnLabelLeftClick( self, event ):
        self.gPortalSortColumn(event.Col)

    def gPortalSortColumn(self, col):
        scol = self.gPortalList.GetSortingColumn()
        if scol == col:
            ascending = not self.gPortalList.IsSortOrderAscending()
            self.gPortalList.SetSortingColumn(col, ascending)
            logger.debug('Portal: Ändere Sortierungsrichtung für ' + str(col) + ' : ' + str(ascending))
        else:
            self.gPortalList.SetSortingColumn(col)
            ascending= True
        self.gPortalList.SortColumn(col, ascending)

    def fill_benachrichtigungen(self):
        logger.debug('Benachrichtigungen: Lade Seite')

    def fill_portal(self):
        logger.debug('Portal: Rufe Geräteliste ab')

        self.gPortalList.DeleteRows(numRows=self.gPortalList.GetNumberRows())

        update = False
        if self.gPortalList.GetNumberCols() != 10:
            self.gPortalList.ClearGrid()
            self.gPortalList.DeleteCols(numCols = self.gPortalList.GetNumberCols())
            self.gPortalList.AppendCols(10)
            self.gPortalList.SetColLabelValue(0, 'Modell')
            self.gPortalList.SetColLabelValue(1, 'Produktionsdatum')
            self.gPortalList.SetColLabelValue(2, 'Softwarerelease')
            self.gPortalList.SetColLabelValue(3, 'Zyklen')
            self.gPortalList.SetColLabelValue(4, 'Kapazität')
            self.gPortalList.SetColLabelValue(5, 'Energiemenge')
            self.gPortalList.SetColLabelValue(6, 'SOH')
            self.gPortalList.SetColLabelValue(7, 'Module')
            self.gPortalList.SetColLabelValue(8, 'Batterietyp(en)')
            self.gPortalList.SetColLabelValue(9, 'Letztes Update')
            self.gPortalList.SortingColTypes = [str, str, str, int, int, int, int, int, str, datetime]
            self.gPortalList.SortingColNames = ['model','productiondate','release','cyclecount','capacity','energy','soh','dcbcount','types','time']
            update = True

        try:
            r = requests.get('https://pv.pincrushers.de/rscpgui/list.json?f=2')

            logger.debug('Geräteliste abgerufen, Response: ' + r.text)

            response = r.json()

            r.raise_for_status()

            r.close()

            self.gPortalList.SortingRowsData = []



            for curdata in response['data']:
                self.gPortalList.AppendRows(1)

                currow = self.gPortalList.GetNumberRows() - 1
                self.gPortalList.SetRowLabelValue(currow, curdata['id'])
                self.gPortalList.SetCellValue(currow, 0, curdata['model'])
                self.gPortalList.SetCellValue(currow, 1, curdata['productiondate'])
                self.gPortalList.SetCellValue(currow, 2, curdata['release'])
                self.gPortalList.SetCellValue(currow, 3, str(curdata['cyclecount']))
                value, einheit = self.get_einheit(curdata['capacity'])
                self.gPortalList.SetCellValue(currow, 4, str(value) + ' ' + einheit)
                value, einheit = self.get_einheit(curdata['energy'])
                self.gPortalList.SetCellValue(currow, 5, str(value) + ' ' + einheit)
                self.gPortalList.SetCellValue(currow, 6, str(curdata['soh']) + '%')
                self.gPortalList.SetCellValue(currow, 7, str(curdata['dcbcount']))
                self.gPortalList.SetCellValue(currow, 8, curdata['types'])
                self.gPortalList.SetCellValue(currow, 9, curdata['time'])

                i = 0
                for name in self.gPortalList.SortingColNames:
                    if self.gPortalList.SortingColTypes[i] == int:
                        curdata[name] = int(curdata[name])
                    elif self.gPortalList.SortingColTypes[i] == datetime:
                        curdata[name] = datetime.datetime.strptime(curdata['time'], '%d.%m.%Y %H:%M:%S')
                    i+=1

                self.gPortalList.SortingRowsData.append(curdata)

            if update:
                self.gPortalList.AutoSizeColumns()
                self.gPortalSortColumn(9)

            self.gPortalList.AutoSizeRows()

            logger.debug('Abruf der Geräteliste aus Portal erfolgreich')
        except:
            logger.exception('Fehler beim Abruf der Geräteliste aus Portal')



    def bConfigGetSerialNoOnClick(self, event):
        username = self.txtUsername.GetValue()
        password = self.txtPassword.GetValue()
        if not username and not password:
            wx.MessageBox('Zur Ermittlung der Seriennummer sind mindestens Benutzername und Passwort erforderlich!',
                          'Ermittlung Seriennummer', wx.ICON_WARNING)
        else:
            serial = None

            if self.gui:
                try:
                    requests = []
                    requests.append(RSCPTag.INFO_REQ_SERIAL_NUMBER)
                    result = self.gui.get_data(requests, True)
                    if result.name == 'INFO_SERIAL_NUMBER':
                        serial = result.data
                        self.txtConfigSeriennummer.SetValue(serial)
                        wx.MessageBox('Seriennummer konnte ermittelt werden (RSCP): ' + serial,
                                      'Ermittlung Seriennummer')
                except:
                    logger.exception('Fehler beim Abruf der Seriennummer')

            if username and password and not serial:
                ret = self.getSerialnoFromWeb(username, password)
                if len(ret) == 1:
                    serial = self.getSNFromNumbers(ret[0]['serialno'])
                    self.txtConfigSeriennummer.SetValue(serial)
                    wx.MessageBox('Seriennummer konnte ermittelt werden (WEB): ' + serial, 'Ermittlung Seriennummer')
                elif len(ret) > 1:
                    sns = '\n'
                    for sn in ret:
                        sns += '\n' + self.getSNFromNumbers(sn['serialno'])
                    wx.MessageBox('Es wurde mehr als eine Seriennummer ermittelt (WEB):' + sns,
                                  'Ermittlung Seriennummer')
                    serial = len(ret)

            if not serial:
                wx.MessageBox('Es konnte keine Seriennummer ermittelt werden (WEB). Zugangsdaten falsch?',
                              'Ermittlung Seriennummer', wx.ICON_ERROR)

        event.Skip()

    def bConfigGetIPAddressOnClick(self, event):
        try:
            ip = repr(self.gui.get_data(self.gui.getInfo(), True)['INFO_IP_ADDRESS'])
            if ip:
                self.txtIP.SetValue(ip)
                wx.MessageBox('IP-Adresse konnte ermittelt werden: ' + ip, 'Ermittlung IP-Adresse')
            else:
                wx.MessageBox('IP-Adresse konnte nicht ermittelt werden, kein Inhalt', 'Ermittlung IP-Adresse',
                              wx.ICON_ERROR)

        except:
            wx.MessageBox('Bei der Ermittlung der IP-Adresse ist ein Fehler aufgetreten #2', 'Ermittlung IP-Adresse',
                          wx.ICON_ERROR)

    def bConfigSetRSCPPasswordOnClick(self, event):
        ret = wx.MessageBox('Soll das angegebene RSCP-Kennwort mit dem bisherigen überschrieben werden?',
                            'RSCP-Passwort ändern', wx.YES_NO | wx.ICON_WARNING)
        if ret == wx.YES:
            try:
                password = self.txtRSCPPassword.GetValue()
                requests = [
                    RSCPDTO(tag=RSCPTag.RSCP_REQ_SET_ENCRYPTION_PASSPHRASE, rscp_type=RSCPType.CString, data=password)]
                res = self.gui.get_data(requests, True)
                if res.data:
                    wx.MessageBox('RSCP-Passwort wurde erfolgreich geändert', 'RSCP-Passwort ändern',
                                  wx.ICON_INFORMATION)
                else:
                    raise Exception('RSCP-Passwort wurde nicht akzeptiert!')
            except:
                wx.MessageBox('Fehler beim Ändern des RSCP-Passworts', 'RSCP-Passwort ändern', wx.ICON_ERROR)

        event.Skip()

    def check_e3dcwebgui(self):
        while True:
            try:
                if self.connectiontype == 'web':
                    try:
                        if self.gui.e3dc.connected:
                            self._connected = True
                            self.txtConfigAktiveVerbindung.SetValue('web - active')
                        else:
                            self._connected = False
                            self.txtConfigAktiveVerbindung.SetValue('web - inactive')
                    except:
                        self._connected = None
                        self.txtConfigAktiveVerbindung.SetValue('unknown')
                elif self.connectiontype == 'direkt':
                    self._connected = True
                    self.txtConfigAktiveVerbindung.SetValue('direct')
                else:
                    self._connected = False
                    self.txtConfigAktiveVerbindung.SetValue('no con')
            except RuntimeError:
                logger.debug('Beende check_e3dcwebgui')
                os._exit(1)
            except:
                self._connected = None
                logger.exception('check_e3dcwebgui')

            time.sleep(2)

    def cbBATIndexOnCombobox(self, event):
        if not self._updateRunning:
            self._updateRunning = True
            selected = self.cbBATIndex.GetSelection()
            if selected != wx.NOT_FOUND:
                self.fill_bat_index(selected)
            self._updateRunning = False

        event.Skip()

    def chPVIIndexOnCombobox(self, event):
        if not self._updateRunning:
            self._updateRunning = True
            selected = self.chPVIIndex.GetSelection()
            if selected != wx.NOT_FOUND:
                self.fill_pvi_index(selected)
            self._updateRunning = False

        event.Skip()

    def bINFOSaveOnClick(self, event):
        r = []
        test = self.cbTimezone.GetValue()
        if test != self._data_info['INFO_TIME_ZONE'].data:
            r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_TIME_ZONE, rscp_type=RSCPType.CString, data=test))

        test = self.txtIPAdress.GetValue()
        if test != self._data_info['INFO_IP_ADDRESS'].data:
            r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_IP_ADDRESS, rscp_type=RSCPType.CString, data=test))

        test = self.txtSubnetmask.GetValue()
        if test != self._data_info['INFO_SUBNET_MASK'].data:
            r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_SUBNET_MASK, rscp_type=RSCPType.CString, data=test))

        test = self.txtGateway.GetValue()
        if test != self._data_info['INFO_GATEWAY'].data:
            r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_GATEWAY, rscp_type=RSCPType.CString, data=test))

        test = self.txtDNSServer.GetValue()
        if test != self._data_info['INFO_DNS'].data:
            r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_DNS, rscp_type=RSCPType.CString, data=test))

        test = self.chDHCP.GetValue()
        if test != self._data_info['INFO_DHCP_STATUS'].data:
            r.append(RSCPDTO(tag=RSCPTag.INFO_REQ_SET_DHCP_STATUS, rscp_type=RSCPType.Bool, data=test))

        if len(r) == 0:
            res = wx.MessageBox('Es wurden keine Änderungen gemacht, aktuelle Einstellungen trotzdem übertragen?',
                                'Info speichern', wx.YES_NO)
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
            res = wx.MessageBox(
                'Wichtig: Falsche Einstellungen können dazu führen, dass das E3DC nicht mehr oder nur noch per Websockets zu erreichen ist. Die Einstellungen müssen dann über das Display direkt geändert werden. Wirklich durchführen?',
                'Hinweis', wx.ICON_WARNING + wx.YES_NO)
            if res == wx.YES:
                try:
                    res = self.gui.get_data(r, True)
                    wx.MessageBox('Übertragung abgeschlossen')
                except:
                    traceback.print_exc()
                    wx.MessageBox('Übertragung fehlgeschlagen')

                self.pMainChanged()

    def refreshConfig(self):
        self.config['Login'] = {'username': self.txtUsername.GetValue(),
                           'password': '@' + self.tinycode('rscpgui', self.txtPassword.GetValue()),
                           'address': self.txtIP.GetValue(),
                           'rscppassword': '@' + self.tinycode('rscpgui_rscppass', self.txtRSCPPassword.GetValue()),
                           'seriennummer': self.txtConfigSeriennummer.GetValue(),
                           'websocketaddr': self.cfgLoginwebsocketaddr,
                           'connectiontype': self.cfgLoginconnectiontype,
                           'autoupdate': self.scAutoUpdate.GetValue()}

        self.config['Notification'] = {'telegram': self.chBenachrichtigungTelegram.GetValue(),
                                       'telegramtoken': '@' + self.tinycode('telegramtoken', self.txtTelegramToken.GetValue()),
                                       'telegramempfaenger': self.txtTelegramEmpfaenger.GetValue()}

        self.config['Export'] = {'csv': self.chUploadCSV.GetValue(),
                            'csvfile': self.fpUploadCSV.GetPath(),
                            'json': self.chUploadJSON.GetValue(),
                            'jsonfile': self.fpUploadJSON.GetPath(),
                            'mqtt': self.chUploadMQTT.GetValue(),
                            'mqttbroker': self.txtUploadMQTTBroker.GetValue(),
                            'mqttport': self.txtUploadMQTTPort.GetValue(),
                            'mqttqos': self.scUploadMQTTQos.GetValue(),
                            'mqttretain': self.chUploadMQTTRetain.GetValue(),
                            'mqttsub': self.chUploadMQTTSub.GetValue(),
                            'mqttusername': self.txtUploadMQTTUsername.GetValue(),
                            'mqttpassword': '@' + self.tinycode('rscpgui_mqttpass', self.txtUploadMQTTPassword.GetValue()),
                            'mqttzertifikat' : self.fpUploadMQTTZertifikat.GetPath(),
                            'mqttinsecure' : self.cbUploadMQTTInsecure.GetValue(),
                            'influx' : self.chUploadInfluxdb.GetValue(),
                            'influxhost' : self.txtUploadInfluxHost.GetValue(),
                            'influxport' : self.txtUploadInfluxPort.GetValue(),
                            'influxdatenbank' : self.txtUploadInfluxDatenbank.GetValue(),
                            'influxtimeout' : self.scUploadInfluxTimeout.GetValue(),
                            'influxname' : self.txtUploadInfluxName.GetValue(),
                            'http': self.chUploadHTTP.GetValue(),
                            'httpurl': self.txtUploadHTTPURL.GetValue(),
                            'intervall': self.scUploadIntervall.GetValue(),
                            'paths': self._config['Export'].get('paths', ''),
                            'pathnames' : self._config['Export'].get('pathnames', '')}

        self.config['Notification/Rules'] = {}

        for currow in range(0,self.gBenachrichtigungen.GetNumberRows()):
            path = self.gBenachrichtigungen.GetCellValue(currow, 0)
            datatype = self.gBenachrichtigungen.GetCellValue(currow, 1)
            expression = self.gBenachrichtigungen.GetCellValue(currow, 2)
            service = self.gBenachrichtigungen.GetCellValue(currow, 3)
            text = self.gBenachrichtigungen.GetCellValue(currow, 4)
            waittime = self.gBenachrichtigungen.GetCellValue(currow, 5)
            data = '|'.join([path,datatype,expression,service,text,waittime])
            if len(data) > 8:
                self.config['Notification/Rules'][str(currow+1)] = data


    def saveConfig(self):
        logger.info('Speichere Konfigurationsdatei ' + self.ConfigFilename)

        self.refreshConfig()



        with open(self.ConfigFilename, 'w') as configfile:
            self.config.write(configfile)

        logger.info('Konfigurationsdatei gespeichert')

    def loadConfig(self):
        logger.info('Lade Konfigurationsdaten in Oberfläche')
        # Defaults

        if self.cfgLoginwebsocketaddr in ('', None):
            self.cfgLoginwebsocketaddr = 'wss://s10.e3dc.com/ws'

        if self.cfgLoginconnectiontype not in ('auto', 'direkt', 'web'):
            self.cfgLoginconnectiontype = 'auto'

        if self.cfgLoginusername is not None:
            self.txtUsername.SetValue(self.cfgLoginusername)
        if self.cfgLoginusername is not None:
            self.txtPassword.SetValue(self.cfgLoginpassword)
        if self.cfgLoginaddress is not None:
            self.txtIP.SetValue(self.cfgLoginaddress)
        if self.cfgLoginrscppassword is not None:
            self.txtRSCPPassword.SetValue(self.cfgLoginrscppassword)
        if self.cfgLoginseriennummer is not None:
            self.txtConfigSeriennummer.SetValue(self.cfgLoginseriennummer)
        if self.cfgLoginautoupdate is not None:
            self.scAutoUpdate.SetValue(self.cfgLoginautoupdate)

        if self.cfgExportmqttbroker in ('', None):
            self.cfgExportmqttbroker = 'localhost'

        if self.cfgExportmqttport in ('', None, 0):
            self.cfgExportmqttport = 1883

        if self.cfgExportmqttqos in ('', None):
            self.cfgExportmqttqos = 0

        if self.cfgExportinfluxhost in ('', None):
            self.cfgExportinfluxhost = 'localhost'

        if self.cfgExportinfluxport in ('', None, 0):
            self.cfgExportinfluxport = 8086

        if self.cfgExportinfluxtimeout in ('', None):
            self.cfgExportinfluxtimeout = 0

        if self.cfgExportinfluxname in ('', None):
            self.cfgExportinfluxname = 'rscpgui'

        if self.cfgExportinfluxhost is not None:
            self.txtUploadInfluxHost.SetValue(self.cfgExportinfluxhost)
        if self.cfgExportinfluxdatenbank is not None:
            self.txtUploadInfluxDatenbank.SetValue(self.cfgExportinfluxdatenbank)
        if self.cfgExportinfluxport is not None:
            self.txtUploadInfluxPort.SetValue(str(self.cfgExportinfluxport))
        if self.cfgExportinfluxtimeout is not None:
            self.scUploadInfluxTimeout.SetValue(self.cfgExportinfluxtimeout)
        if self.cfgExportinflux is not None:
            self.chUploadInfluxdb.SetValue(self.cfgExportinflux)
        if self.cfgExportinfluxname is not None:
            self.txtUploadInfluxName.SetValue(self.cfgExportinfluxname)

        if self.cfgExportcsv is not None:
            self.chUploadCSV.SetValue(self.cfgExportcsv)
        if self.cfgExportcsvfile is not None:
            self.fpUploadCSV.SetPath(self.cfgExportcsvfile)
        if self.cfgExportjson is not None:
            self.chUploadJSON.SetValue(self.cfgExportjson)
        if self.cfgExportjsonfile is not None:
            self.fpUploadJSON.SetPath(self.cfgExportjsonfile)
        if self.cfgExportmqtt is not None:
            self.chUploadMQTT.SetValue(self.cfgExportmqtt)
        if self.cfgExportmqttbroker is not None:
            self.txtUploadMQTTBroker.SetValue(self.cfgExportmqttbroker)
        if self.cfgExportmqttport is not None:
            self.txtUploadMQTTPort.SetValue(str(self.cfgExportmqttport))
        if self.cfgExportmqttpos is not None:
            self.scUploadMQTTQos.SetValue(self.cfgExportmqttpos)
        if self.cfgExportmqttretain is not None:
            self.chUploadMQTTRetain.SetValue(self.cfgExportmqttretain)
        if self.cfgExportmqttsub is not None:
            self.chUploadMQTTSub.SetValue(self.cfgExportmqttsub)
        if self.cfgExportmqttpassword is not None:
            self.txtUploadMQTTPassword.SetValue(self.cfgExportmqttpassword)
        if self.cfgExportmqttusername is not None:
            self.txtUploadMQTTUsername.SetValue(self.cfgExportmqttusername)
        if self.cfgExportmqttzertifikat is not None:
            self.fpUploadMQTTZertifikat.SetPath(self.cfgExportmqttzertifikat)
        if self.cfgExportmqttinsecure is not None:
            self.cbUploadMQTTInsecure.SetValue(self.cfgExportmqttinsecure)
        if self.cfgExporthttp is not None:
            self.chUploadHTTP.SetValue(self.cfgExporthttp)
        if self.cfgExporthttpurl is not None:
            self.txtUploadHTTPURL.SetValue(self.cfgExporthttpurl)
        if self.cfgExportintervall is not None:
            self.scUploadIntervall.SetValue(self.cfgExportintervall)
        if self.cfgNotificationtelegram is not None:
            self.chBenachrichtigungTelegram.SetValue(self.cfgNotificationtelegram)
        if self.cfgNotificationtelegramtoken is not None:
            self.txtTelegramToken.SetValue(self.cfgNotificationtelegramtoken)
        if self.cfgNotificationtelegramempfaenger is not None:
            self.txtTelegramEmpfaenger.SetValue(self.cfgNotificationtelegramempfaenger)

        if self.cfgExportpaths is not None and len(self.cfgExportpaths) > 0:
            self.stUploadCount.SetLabel('Es wurden ' + str(len(self.cfgExportpaths)) + ' Datenfelder angewählt')
        else:
            self.stUploadCount.SetLabel('Keine Datenfelder angewählt')

        self.gBenachrichtigungen.DeleteRows(numRows=self.gBenachrichtigungen.GetNumberRows())
        if 'Notification/Rules' not in self._config:
            self._config['Notification/Rules'] = {}

        if len(self._config['Notification/Rules']) == 0:
            self._config['Notification/Rules']['1'] = 'E3DC/EMS_DATA/EMS_POWER_GRID|int|{value}<-2000|telegram|Einspeiseleistung > 2000W ({value})|3600'
            self._config['Notification/Rules']['2'] = 'E3DC/EMS_DATA/EMS_EMERGENCY_POWER_STATUS|int|{value}==0|telegram|Notstrom nicht möglich|-1'
            self._config['Notification/Rules']['3'] = 'E3DC/EMS_DATA/EMS_EMERGENCY_POWER_STATUS|int|{value}==1|telegram|Notstrom aktiv|-1'
            self._config['Notification/Rules']['4'] = 'E3DC/EMS_DATA/EMS_EMERGENCY_POWER_STATUS|int|{value}==2|telegram|Notstrom nicht aktiv|-1'
            self._config['Notification/Rules']['5'] = 'E3DC/EMS_DATA/EMS_EMERGENCY_POWER_STATUS|int|{value}==3|telegram|Notstrom derzeit nicht verfügbar|-1'
            self._config['Notification/Rules']['6'] = 'E3DC/EMS_DATA/EMS_EMERGENCY_POWER_STATUS|int|{value}==4|telegram|Motorschalter in Inselbetrieb|-1'
            self._config['Notification/Rules']['7'] = 'E3DC/PVI_DATA/0/PVI_DATA/PVI_SYSTEM_MODE|int|{value}==0|telegram|Wechselrichter in IDLE geschaltet|-1'
            self._config['Notification/Rules']['8'] = 'E3DC/PVI_DATA/0/PVI_DATA/PVI_SYSTEM_MODE|int|{value}==1|telegram|Wechselrichter in Normal geschaltet|-1'
            self._config['Notification/Rules']['9'] = 'E3DC/PVI_DATA/0/PVI_DATA/PVI_SYSTEM_MODE|int|{value}==2|telegram|Wechselrichter in Gridcharge geschaltet|-1'
            self._config['Notification/Rules']['10'] = 'E3DC/PVI_DATA/0/PVI_DATA/PVI_SYSTEM_MODE|int|{value}==3|telegram|Wechselrichter in Backuppower geschaltet|-1'
            self._config['Notification/Rules']['11'] = 'E3DC/PVI_DATA/0/PVI_DATA/PVI_SYSTEM_MODE|int|{value}>3|telegram|Wechselrichter - Mode unbekannt (PVI_SYSTEM_MODE={value})|-1'

        rules = self._config['Notification/Rules']
        for rule in rules:
            try:
                path, datatype, expression, service, text, waittime = rules[rule].split('|')
                self.gBenachrichtigungen.AppendRows(1, False)
                currow = self.gBenachrichtigungen.GetNumberRows()-1
                self.gBenachrichtigungen.SetCellValue(currow, 0, path)
                self.gBenachrichtigungen.SetCellValue(currow, 1, datatype)
                self.gBenachrichtigungen.SetCellValue(currow, 2, expression)
                self.gBenachrichtigungen.SetCellValue(currow, 3, service)
                self.gBenachrichtigungen.SetCellValue(currow, 4, text)
                self.gBenachrichtigungen.SetCellValue(currow, 5, waittime)
            except ValueError:
                logger.error('Konfigurationsdatei nicht lesbar, Bereich Notification/Rules falsch gefüllt, Beispiel: path|datatype|expression|service|text|waittime')

        self.gBenachrichtigungen.AppendRows(1, False)

        self.gBenachrichtigungen.AutoSize()

        logger.info('Konfigurationsdatei geladen')