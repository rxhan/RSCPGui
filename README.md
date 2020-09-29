# RSCPGui
RSCPGui für die Abfrage und Darstellung von Daten aus einem E3DC - System

** Das Programm befindet sich in einem frühen Entwicklungsstatus nicht alle Funktionen stehen zur Verfügung

Die Schnittstelle basiert auf der Library von fsantini (https://github.com/fsantini/python-e3dc).

# Abhängigkeiten

wxPython
py3rijndael
requests
websocket-client

Getestet wurde mit Python 3.8 und Python 3.7.
Grundsätzlich sollte das Programm Plattformunabhängig sein, es wurde jedoch ausschließlich mit Windows getestet.

# Installation
Python3 muss inklusive der oben genannten Abhängigkeiten installiert werden.
Aufruf dann mittels python3 main.py

# Nutzung

Es werden mindestens Angaben zu Benutzername und Passwort benötigt. 
Weitere Informationen werden automatisch ermittelt sofern ein Internetzugriff besteht.
Soll ein lokaler Zugriff erfolgen muss das RSCP-Passwort angegeben werden. 
Dies kanna auch vom Programm gesetzt werden.

# Windows-Binarys

Können hier heruntergeladen werden:

https://pv.pincrushers.de/rscpgui
