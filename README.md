# RSCPGui
RSCPGui für die Abfrage und Darstellung von Daten aus einem E3DC - System

**Das Programm befindet sich in einem frühen Entwicklungsstatus nicht alle Funktionen stehen zur Verfügung**
**Benutzung erfolgt auf eigene Gefahr, für Schäden kann der Author nicht haftbar gemacht werden**

Die Schnittstelle basiert auf der Library von MatrixCrawler (https://github.com/MatrixCrawler/python-e3dc-module).

# Abhängigkeiten

Getestet wurde mit Python 3.9, Python 3.8 und Python 3.7.
Grundsätzlich sollte das Programm Plattformunabhängig sein, es wurde jedoch ausschließlich mit Windows getestet.


# Installation

### Windows:

Keine Installation notwendig, die Binary (RSCPGui.exe) kann direkt ausgeführt werden. 

Falls ohne Binary ausgeführt werden soll:
Python3 muss inklusive der in requirements.txt beschriebenen Abhängigkeiten installiert sein.
Aufruf dann mittels python3 main.py
  
### Linux:

Voraussetzungen (für GUI-Betrieb)

    apt-get install git python3-dev libgtk-3-dev libpulse-dev python3-venv wheel
    pip3 install -r requirements.txt
    
Für Konsolenbetrieb wenn z.B. nur Export der Daten genügt

    pip3 install -r requirements.txt
    
Die Installation von wxPython wird dann fehlschlagen, dieses wird für den Konsolenbetrieb aber nicht benötigt.

# Nutzung

Es werden mindestens Angaben zu Benutzername und Passwort benötigt. 
Weitere Informationen werden automatisch ermittelt sofern ein Internetzugriff besteht.
Soll ein lokaler Zugriff erfolgen muss das RSCP-Passwort angegeben werden. 
Dies kann aber auch vom Programm gesetzt werden.

# Windows-Binary

Aktuelle stehen in den Releasen bereit:

https://github.com/rxhan/RSCPGui/releases
