import logging
import argparse
import socket
import sys

parser = argparse.ArgumentParser(description='Ruft Daten von E3DC-Systemen mittels RSCP ab')
parser.add_argument('-e', '--export', const=True, default=False, nargs='?',
                    help='Exportstart mit Programmstart')
parser.add_argument('-i', '--hide', action='store_true',
                    help='Programm verstecken')
parser.add_argument("-c", "--console", const=True, default=False, nargs='?', help='Verwendung als Konsolenprogramm, sonst mit Oberfläche')
parser.add_argument("-f", "--logfile", const='rscpgui.log', default=None, nargs='?', help='Ausgabe in eine Logdatei (Default bei Oberfläche)')
parser.add_argument("-v", "--verbose", const='INFO', choices=logging._nameToLevel.keys(), default='DEBUG', nargs='?', help='Anpassen des Loglevels')
parser.add_argument("-l", "--logconsole", action='store_true', help='Logausgabe auch auf der Console (nur sinnvoll ohne -c)')
parser.add_argument("-p", "--portal", action='store_true', help='Sende Batteriedaten an Portal')


args = parser.parse_args()
loglevel = args.verbose

# Patch für schnellere Namensauflösung in IPv6 - Netzwerken:

orig_getaddrinfo = socket.getaddrinfo

def _getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

socket.getaddrinfo = _getaddrinfo

def setLoglevel(loglevel, filename = None, console = True, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    loggernames = [__name__, 'rscpguiframe','rscpguimain','rscpguiconsole','export','e3dcwebgui','e3dc','assistant']
    for name in loggernames:
        l = logging.getLogger(name)
        l.setLevel(loglevel)

        formatter = logging.Formatter(format)

        if console:
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)

            ch.setFormatter(formatter)
            l.addHandler(ch)

        if filename:
            ch = logging.FileHandler(filename)
            ch.setLevel(loglevel)
            ch.setFormatter(formatter)
            l.addHandler(ch)

if not args.console and not args.logfile:
    logfile = 'rscpgui.log'
else:
    logfile = args.logfile

if args.console or args.logconsole:
    console = True
else:
    console = False

setLoglevel(args.verbose, logfile, console)

logger = logging.getLogger(__name__)
logger.debug('Programmstart')

try:
    import wx
except:
    logger.warning('wxPython steht nicht zur Verfügung, Programm beschränkt sich auf die Console')

logger.info('Lade Module')

if 'wx' in sys.modules.keys() and not args.console:
    from rscpguiframe import RSCPGuiFrame

    logger.info('Module geladen, initialisiere App')
    app = wx.App()
    app.InitLocale()
    logger.info('App initialisiert, lade Fenster')
    g = RSCPGuiFrame(None, args)
    logger.info('Fenster geladen')
    if not args.hide:
        logger.info('zeichne Fenster')
        if g.assistantFrame:
            g.assistantFrame.Show()
            g.assistantFrame.SetFocus()
        else:
            g.Show()

        logger.info('Fenster gezeichnet, warte auf Events')
    app.MainLoop()
else:
    from rscpguiconsole import RSCPGuiConsole

    logger.info('Module geladen, initialisiere Console')
    g = RSCPGuiConsole(args)
    g.MainLoop()

logger.info('Programm beendet')