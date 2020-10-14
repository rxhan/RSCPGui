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

import os
from rscpguimain import RSCPGuiMain
import time


class RSCPGuiConsole(RSCPGuiMain):
    def __init__(self, args):
        RSCPGuiMain.__init__(self, args)

    def check_e3dcwebgui(self):
        while True:
            try:
                if self.connectiontype == 'web':
                    try:
                        if self.gui.e3dc.connected:
                            self._connected = True
                        else:
                            self._connected = False
                    except:
                        self._connected = None
                elif self.connectiontype == 'direkt':
                    self._connected = True
                else:
                    self._connected = False
            except RuntimeError:
                logger.debug('Beende check_e3dcwebgui')
                os._exit(1)
            except:
                self._connected = None
                logger.exception('check_e3dcwebgui')
            time.sleep(2)

    def MainLoop(self):
        if self._args.export:
            g = self.gui
            logger.debug('Export bei Programmstart aktiviert')
            self.StartExport()

            # Loop forever
            try:
                self.check_e3dcwebgui()
            except:
                self._AutoExportStarted = False
        else:
            logger.debug('Nichts zu tun, versuche -h')


    @property
    def gui(self):
        if self._gui:
            return self._gui
        else:
            return RSCPGuiMain.gui.fget(self)