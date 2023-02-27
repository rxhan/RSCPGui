import logging

from e3dc.rscp_tag import RSCPTag
from e3dcwebgui import E3DCWebGui

logger = logging.getLogger(__name__)

logger.debug('Programmstart')

from gui import AssistantFrame
import wx

class Assistant(AssistantFrame):

    def __init__(self, parent):
        self._parent = parent
        self._test_serial = None
        self._test_ip = None
        self._test_successfull = False
        self._testgui = None
        AssistantFrame.__init__(self, parent=parent)

        if self._parent.cfgLoginusername:
            self.txtAssistantUsername.SetValue(self._parent.cfgLoginusername)
        if self._parent.cfgLoginpassword:
            self.txtAssistantPassword.SetValue(self._parent.cfgLoginpassword)

        # Connect Events
        self.btnAssistantOK.Bind(wx.EVT_BUTTON, self.btnAssistantOKOnClick)
        self.btnAssistantCancel.Bind(wx.EVT_BUTTON, self.btnAssistantCancelOnClick)

    def btnAssistantOKOnClick( self, event ):
        pwd = self.txtAssistantPassword.GetValue()
        user = self.txtAssistantUsername.GetValue()

        if not pwd or not user:
            logger.warning('Passwort oder Benutzer fehlen, kein Login möglich')
        else:
            ret = self.tryWeblogin(user, pwd)
            if ret:
                logger.info('Assistent bestätigt, Zugangsdaten erfolgreich')
                self.Close()
            else:
                logger.info('Zugangsdaten falsch, Assistent offen halten')

    def btnAssistantCancelOnClick( self, event ):
        logger.info('Assistent beendet')

        self.Close()

    @property
    def username(self):
        return self.txtAssistantUsername.GetValue()

    @property
    def password(self):
        return self.txtAssistantPassword.GetValue()

    @property
    def no_show(self):
        return self.chkAsistantNoShow.GetValue()

    @property
    def serial(self):
        return self._test_serial

    @property
    def ip(self):
        return self._test_ip

    @property
    def testresult(self):
        return self._test_successfull

    @property
    def testgui(self):
        return self._testgui

    def tryWeblogin(self, username, password):
        def test_connection(testgui):
            requests = []
            requests.append(RSCPTag.INFO_REQ_SERIAL_NUMBER)
            requests.append(RSCPTag.INFO_REQ_IP_ADDRESS)
            return testgui.get_data(requests, True)

        try:
            ret = self._parent.getSerialnoFromWeb(username, password)
            if len(ret) == 1:
                seriennummer = [self._parent.getSNFromNumbers(ret[0]['serialno'])]
                logger.debug(f'Seriennummer konnte ermittelt werden (WEB): {seriennummer}')
                logger.debug('Versuche IP-Adresse zu ermitteln')
                try:
                    self._testgui = E3DCWebGui(username, password, seriennummer[0])
                    ip = repr(test_connection(self._testgui)['INFO_IP_ADDRESS'])
                    if ip:
                        logger.debug('IP-Adresse konnte ermittelt werden: ' + ip)
                    else:
                        raise Exception('IP-Adresse konnte nicht ermittelt werden, kein Inhalt')
                except:
                    logger.exception('Bei der Ermittlung der IP-Adresse ist ein Fehler aufgetreten')
                    self._testgui = None
                    wx.MessageBox(f'Websocket-Verbindung zu E3DC nicht möglich.\nFirewalleinstellungen prüfen oder es später erneut versuchen.\nErmittelte Seriennummer: {seriennummer[0]}', 'Verbindungsfehler', wx.ICON_ERROR)
                else:
                    self._test_serial = seriennummer[0]
                    self._test_ip = ip
                    self._test_successfull = True
                    #wx.MessageBox(f'Zugriff erfolgreich, ermitteltes System:\nSeriennummer: {seriennummer[0]}\nIP: {ip}', 'Zugriff hergestellt', wx.ICON_INFORMATION)
                    return True

            elif len(ret) > 1:
                seriennummer = [self._parent.getSNFromNumbers(sn['serialno']) for sn in ret]
                logger.debug('Es wurde mehr als eine Seriennummer ermittelt (WEB):' + '\n'.join(seriennummer))
                wx.MessageBox(f'Es wurden mehrere Seriennummer zu dem Webzugang ermittelt.\nBitte Einstellungen benutzen.', 'Mehrere Seriennummern', wx.ICON_INFORMATION)
            else:
                wx.MessageBox('Verbindung nicht möglich, Zugangsdaten falsch?', 'Zugangsdaten falsch?', wx.ICON_ERROR)
        except:
            logger.exception('Ermittlung von IP und Seriennummer nicht möglich. Zugangsdaten falsch?')
            wx.MessageBox('Verbindung nicht möglich, Zugangsdaten falsch?', 'Zugangsdaten falsch?', wx.ICON_ERROR)


        return False

