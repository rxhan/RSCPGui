import logging
import argparse

parser = argparse.ArgumentParser(description='Ruft Daten von E3DC-Systemen mittels RSCP ab')
parser.add_argument('-e', '--export', const=True, default=False, nargs='?',
                    help='Exportstart mit Programmstart')
parser.add_argument('--hide', const=True, default=False, nargs='?',
                    help='Programm verstecken')
parser.add_argument("-v", "--verbose", const=True, default=False, nargs='?', help='Erhöhen des Loglevels')
parser.add_argument("-c", "--console", const=True, default=False, nargs='?', help='Verwendung als Konsolenprogramm')

args = parser.parse_args()
if args.verbose:
    loglevel = logging.DEBUG
else:
    loglevel = logging.ERROR

logger = logging.getLogger(__name__)
logger.setLevel(loglevel)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(loglevel)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

logger.debug('Programmstart')

try:
    import wx
except:
    logger.warning('wxPython steht nicht zur Verfügung, Programm beschränkt sich auf die Console')

logger.debug('Lade Module')

import sys

if 'wx' in sys.modules.keys() and not args.console:
    from rscpguiframe import RSCPGuiFrame

    logger.debug('Module geladen, initialisiere App')
    app = wx.App()
    logger.debug('App initialisiert, lade Fenster')
    g = RSCPGuiFrame(None, args)
    logger.debug('Fenster geladen')
    if not args.hide:
        logger.debug('zeichne Fenster')
        g.Show()
        logger.debug('Fenster gezeichnet, warte auf Events')
    app.MainLoop()
else:
    from rscpguiconsole import RSCPGuiConsole

    logger.debug('Module geladen, initialisiere Console')
    g = RSCPGuiConsole(args)
    g.MainLoop()


logger.debug('Programm beendet')