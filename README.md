# RSCPGui
Das Programm fragt Daten per RSCP von einem E3/DC - Hauskraftwerk ab und stellt diese dar. Die über RSCP veränderbaren Einstellungen im USER-Modus können auch geschrieben werden. Auch Aktionen wie z.B. Notstrombetrieb oder Systemneustart können ausgelöst werden. Dabei wird versucht möglichst viele Daten richtig darzustellen. Mit dem Programm können die Daten auch "headless" zyklisch exportiert werden. Unterstützt werden csv, json, influxdb, mqtt. Darüberhinaus ist es möglich Benachrichtigungen über Telegram zu erhalten, wenn bestimmte Ereignisse eintreten oder Werte gelesen wurden. Über MQTT können auch bestimmte Werte wieder zurückgeschrieben werden.

**Das Programm befindet sich in einem frühen Entwicklungsstatus nicht alle Funktionen stehen zur Verfügung**
**Benutzung erfolgt auf eigene Gefahr, für Schäden kann der Author nicht haftbar gemacht werden**

Die Schnittstelle basiert auf der Library von MatrixCrawler (https://github.com/MatrixCrawler/python-e3dc-module).

# Abhängigkeiten

Getestet wurde mit Python 3.10/3.11, ältere Versionen bis 3.7 sollten ebenfalls funktionieren.
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

### Konfiguration

Beim ersten Start im Oberflächenmodus wird ein Assistent gestartet, über welchen eine Websocket-Verbindung mithilfe der Web-Zugangsdaten bequem hergestellt werden kann. Es ist jedoch zu empfehlen im Anschluss eine Direktverbindung einzurichten. Dazu muss dann im Einstellungs-Dialog das RSCP-Passwort hinterlegt werden, oder falls noch nicht geschehen gesetzt werden.

### manuelle Konfiguration

Um die RSCPGui manuell zu konfigurieren muss lediglich die Datei rscpe3dc.conf.default.ini zu rscpe3dc.conf.ini umbenannt werden und diese mit den ensprechenden Werten gefüllt werden.

Für eine korrekte Funktion der grundlegenden Programmeigenschaften sind mindestens folgende Einstellungen zu setzen:

> [Login]
> 
> username=mye3dportalusername
> 
> password=mypassword
> 
> rscppassword=myrscppassword
> 
> address=192.168.xxx.yyy
> 
> seriennummer=S10-xxxxxxxxxxxx

# Nutzung

Es werden mindestens Angaben zu Benutzername und Passwort benötigt. 
Weitere Informationen werden automatisch ermittelt sofern ein Internetzugriff besteht.
Soll ein lokaler Zugriff erfolgen muss das RSCP-Passwort angegeben werden. 
Dies kann aber auch vom Programm gesetzt werden.

### Export von Daten

Zum Export von Daten stehen CSV (historisch), JSON (Statusdatei), MQTT, Influx und ein URL-Post zur Verfügung. Die zu übertragenen Daten müssen vorher ausgewählt werden.
Achtung: Es werden die RAW-Werte übertragen! Der Bezeichner entspricht dabei dem TOPIC in MQTT, oder der Überschrift der CSV-Datei bzw. der Key in der JSON-Datei. Es können auch ganze Knoten mit ihren Unterknoten umbenannt werden. Beim Export sollten nicht unnötig viele Daten angewählt werden.

Um die Daten nun "headless" zu exportieren muss das Programm nach der Konfiguration mit **-e -c** gestartet werden. Dadurch wird (-e) der Export automatisch gestartet und das Programm startet im Konsolenmodus (-c).
Die Konfigurationsdatei kann dafür an einem anderen Rechner mit Oberfläche erzeugt werden und auf den Zielrechner kopiert werden. (rscpgui.conf.ini)

### Benachrichtigungen

Aktuell noch nicht ganz fertig! - Work in progess ;-)

### Werte über MQTT zurückschreiben

Über MQTT können Werte auch wieder an das Hauskraftwerk zurückübertragen werden. Aktuell unterstützt werden: 
**maximale Ladeleistung, maximale Entladeleistung und untere Schwelle Lade-/Entladung.**
Dies funktioniert nur bei aktiviertem Export. Zusätzlich müssen die zu ändernden Werte auch in den Exportdaten enthalten sein. Ein zurückschreiben der Werte ist nun mit dem angegebenen Bezeichner + /SET möglich.
Ohne Anpassung des Bezeichners ist dies z.B. für die maximale Ladeleistung: 
*E3DC/EMS_DATA/EMS_GET_POWER_SETTINGS/EMS_MAX_CHARGE_POWER/SET*

# Kommandozeilenparameter

Können mit rscpgui.exe -h angezeigt werden:

```sh

usage: rscpgui.exe [-h] [-e [EXPORT]] [-i] [-c [CONSOLE]] [-f [LOGFILE]]
                   [-v [{CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]] [-l] [-p]
...
```

# Screenshots

![Assistent zur vereinfachten Anmeldung](https://github.com/rxhan/RSCPGui/blob/master/images/RSCPGUI_Assistant.PNG)

![Übersicht der Batteriedaten](https://github.com/rxhan/RSCPGui/blob/master/images/RSCPGUI_BAT.png)

![Übersicht der Ladeeinstellungen](https://github.com/rxhan/RSCPGui/blob/master/images/RSCPGUI_Ladeeinstellungen.png)

![Übersicht der Wechselrichter](https://github.com/rxhan/RSCPGui/blob/master/images/RSCPGUI_Wechselrichter.png)

![Übersicht der Basisdaten / EMS](https://github.com/rxhan/RSCPGui/blob/master/images/RSCPGUI_EMS.png)

# Windows-Binary

Aktuelle stehen in den Releasen bereit.

https://github.com/rxhan/RSCPGui/releases

# 
