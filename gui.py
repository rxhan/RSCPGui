# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.adv

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"E3/DC RSCPGui", pos = wx.Point( 100,100 ), size = wx.Size( 1073,796 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.pMainregister = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"EMS" )
		self.pMain = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"INFO" )
		fgSizer21 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer21.SetFlexibleDirection( wx.BOTH )
		fgSizer21.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText51 = wx.StaticText( self.pMain, wx.ID_ANY, u"Produktionsdatum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )

		gSizer2.Add( self.m_staticText51, 0, wx.ALL, 5 )

		self.txtProductionDate = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtProductionDate.Enable( False )

		gSizer2.Add( self.txtProductionDate, 0, wx.ALL, 5 )

		self.m_staticText61 = wx.StaticText( self.pMain, wx.ID_ANY, u"Seriennummer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )

		gSizer2.Add( self.m_staticText61, 0, wx.ALL, 5 )

		fgSizer462 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer462.SetFlexibleDirection( wx.BOTH )
		fgSizer462.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.txtSerialnumber = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.txtSerialnumber.Enable( False )

		fgSizer462.Add( self.txtSerialnumber, 0, wx.ALL, 5 )

		self.txtModelname = wx.StaticText( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtModelname.Wrap( -1 )

		fgSizer462.Add( self.txtModelname, 0, wx.ALL, 5 )


		gSizer2.Add( fgSizer462, 1, wx.EXPAND, 5 )

		self.m_staticText71 = wx.StaticText( self.pMain, wx.ID_ANY, u"Softwarerelease", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		gSizer2.Add( self.m_staticText71, 0, wx.ALL, 5 )

		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )

		self.txtSwRelease = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 90,-1 ), 0 )
		self.txtSwRelease.Enable( False )

		gSizer5.Add( self.txtSwRelease, 0, wx.ALL, 5 )

		self.btnUpdatecheck = wx.Button( self.pMain, wx.ID_ANY, u"Auf Updates prüfen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btnUpdatecheck, 0, wx.ALL, 5 )


		gSizer2.Add( gSizer5, 1, wx.EXPAND, 2 )

		self.m_staticText12 = wx.StaticText( self.pMain, wx.ID_ANY, u"Updatestatus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		gSizer2.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.txtUpdateStatus = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		self.txtUpdateStatus.Enable( False )

		gSizer2.Add( self.txtUpdateStatus, 0, wx.ALL, 5 )

		self.m_staticText81 = wx.StaticText( self.pMain, wx.ID_ANY, u"A35-Seriennummer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )

		gSizer2.Add( self.m_staticText81, 0, wx.ALL, 5 )

		self.txtA35Serial = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 170,-1 ), 0 )
		self.txtA35Serial.Enable( False )

		gSizer2.Add( self.txtA35Serial, 0, wx.ALL, 5 )

		self.m_staticText154 = wx.StaticText( self.pMain, wx.ID_ANY, u"System startet neu", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText154.Wrap( -1 )

		gSizer2.Add( self.m_staticText154, 0, wx.ALL, 5 )

		fgSizer16 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer16.SetFlexibleDirection( wx.BOTH )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.chSYSReboot = wx.CheckBox( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chSYSReboot.Enable( False )

		fgSizer16.Add( self.chSYSReboot, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.bSYSReboot = wx.Button( self.pMain, wx.ID_ANY, u"Reboot", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		fgSizer16.Add( self.bSYSReboot, 0, wx.ALL, 5 )

		self.bSYSApplicationRestart = wx.Button( self.pMain, wx.ID_ANY, u"Restart", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		fgSizer16.Add( self.bSYSApplicationRestart, 0, wx.ALL, 5 )


		gSizer2.Add( fgSizer16, 1, wx.EXPAND, 5 )

		self.m_staticText155 = wx.StaticText( self.pMain, wx.ID_ANY, u"Online", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText155.Wrap( -1 )

		gSizer2.Add( self.m_staticText155, 0, wx.ALL, 5 )

		self.chSRVIsOnline = wx.CheckBox( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chSRVIsOnline.Enable( False )

		gSizer2.Add( self.chSRVIsOnline, 0, wx.ALL, 5 )

		self.m_staticText156 = wx.StaticText( self.pMain, wx.ID_ANY, u"Benutzerlevel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText156.Wrap( -1 )

		gSizer2.Add( self.m_staticText156, 0, wx.ALL, 5 )

		self.txtRSCPUserLevel = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtRSCPUserLevel.Enable( False )

		gSizer2.Add( self.txtRSCPUserLevel, 0, wx.ALL, 5 )

		self.m_staticText9 = wx.StaticText( self.pMain, wx.ID_ANY, u"Systemzeit (lokal)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		gSizer2.Add( self.m_staticText9, 0, wx.ALL, 5 )

		self.txtTime = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		self.txtTime.Enable( False )

		gSizer2.Add( self.txtTime, 0, wx.ALL, 5 )

		self.m_staticText11 = wx.StaticText( self.pMain, wx.ID_ANY, u"Zeitzone", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gSizer2.Add( self.m_staticText11, 0, wx.ALL, 5 )

		cbTimezoneChoices = []
		self.cbTimezone = wx.ComboBox( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbTimezoneChoices, 0 )
		gSizer2.Add( self.cbTimezone, 0, wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self.pMain, wx.ID_ANY, u"Systemzeit (UTC)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		gSizer2.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.txtTimeUTC = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		self.txtTimeUTC.Enable( False )

		gSizer2.Add( self.txtTimeUTC, 0, wx.ALL, 5 )

		self.m_staticText64 = wx.StaticText( self.pMain, wx.ID_ANY, u"IP-Adresse", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText64.Wrap( -1 )

		gSizer2.Add( self.m_staticText64, 0, wx.ALL, 5 )

		self.txtIPAdress = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.txtIPAdress, 0, wx.ALL, 5 )

		self.m_staticText65 = wx.StaticText( self.pMain, wx.ID_ANY, u"Subnet", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText65.Wrap( -1 )

		gSizer2.Add( self.m_staticText65, 0, wx.ALL, 5 )

		self.txtSubnetmask = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.txtSubnetmask, 0, wx.ALL, 5 )

		self.m_staticText66 = wx.StaticText( self.pMain, wx.ID_ANY, u"MAC-Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText66.Wrap( -1 )

		gSizer2.Add( self.m_staticText66, 0, wx.ALL, 5 )

		self.txtMacAddress = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMacAddress.Enable( False )

		gSizer2.Add( self.txtMacAddress, 0, wx.ALL, 5 )

		self.m_staticText67 = wx.StaticText( self.pMain, wx.ID_ANY, u"Gateway", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText67.Wrap( -1 )

		gSizer2.Add( self.m_staticText67, 0, wx.ALL, 5 )

		self.txtGateway = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.txtGateway, 0, wx.ALL, 5 )

		self.m_staticText68 = wx.StaticText( self.pMain, wx.ID_ANY, u"DNS-Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText68.Wrap( -1 )

		gSizer2.Add( self.m_staticText68, 0, wx.ALL, 5 )

		self.txtDNSServer = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.txtDNSServer, 0, wx.ALL, 5 )

		self.m_staticText69 = wx.StaticText( self.pMain, wx.ID_ANY, u"DHCP Verwendet", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText69.Wrap( -1 )

		gSizer2.Add( self.m_staticText69, 0, wx.ALL, 5 )

		self.chDHCP = wx.CheckBox( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.chDHCP, 0, wx.ALL, 5 )

		self.m_staticText692 = wx.StaticText( self.pMain, wx.ID_ANY, u"UPNP aktiv", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText692.Wrap( -1 )

		gSizer2.Add( self.m_staticText692, 0, wx.ALL, 5 )

		self.chUPNP = wx.CheckBox( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.chUPNP, 0, wx.ALL, 5 )

		self.m_staticText6921 = wx.StaticText( self.pMain, wx.ID_ANY, u"RSCP Passwort gesetzt", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6921.Wrap( -1 )

		gSizer2.Add( self.m_staticText6921, 0, wx.ALL, 5 )

		self.chRSCPPasswordSet = wx.CheckBox( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chRSCPPasswordSet.Enable( False )

		gSizer2.Add( self.chRSCPPasswordSet, 0, wx.ALL, 5 )

		self.bINFOSave = wx.Button( self.pMain, wx.ID_ANY, u"Änderungen übertragen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.bINFOSave, 0, wx.ALL, 5 )


		fgSizer21.Add( gSizer2, 1, 0, 2 )

		bSizer21 = wx.BoxSizer( wx.VERTICAL )

		fgSizer461 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer461.SetFlexibleDirection( wx.BOTH )
		fgSizer461.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText221 = wx.StaticText( self.pMain, wx.ID_ANY, u"Dateisystem", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText221.Wrap( -1 )

		fgSizer461.Add( self.m_staticText221, 0, wx.ALL, 5 )

		fgSizer47 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer47.SetFlexibleDirection( wx.BOTH )
		fgSizer47.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.gInfoFilesystem = wx.Gauge( self.pMain, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.gInfoFilesystem.SetValue( 0 )
		fgSizer47.Add( self.gInfoFilesystem, 0, wx.ALL, 5 )

		self.txtFilesystemPercent = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txtFilesystemPercent.Enable( False )

		fgSizer47.Add( self.txtFilesystemPercent, 0, wx.ALL, 5 )


		fgSizer461.Add( fgSizer47, 1, wx.EXPAND, 5 )


		fgSizer461.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.txtFilesystem = wx.TextCtrl( self.pMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 250,-1 ), 0 )
		self.txtFilesystem.Enable( False )

		fgSizer461.Add( self.txtFilesystem, 0, wx.ALL, 5 )


		bSizer21.Add( fgSizer461, 1, 0, 5 )

		self.gSoftwaremodules = wx.grid.Grid( self.pMain, wx.ID_ANY, wx.DefaultPosition, wx.Size( 450,500 ), 0 )

		# Grid
		self.gSoftwaremodules.CreateGrid( 1, 4 )
		self.gSoftwaremodules.EnableEditing( True )
		self.gSoftwaremodules.EnableGridLines( False )
		self.gSoftwaremodules.EnableDragGridSize( False )
		self.gSoftwaremodules.SetMargins( 0, 0 )

		# Columns
		self.gSoftwaremodules.EnableDragColMove( False )
		self.gSoftwaremodules.EnableDragColSize( True )
		self.gSoftwaremodules.SetColLabelValue( 0, u"Modulname" )
		self.gSoftwaremodules.SetColLabelValue( 1, u"Version" )
		self.gSoftwaremodules.SetColLabelValue( 2, u"Datum" )
		self.gSoftwaremodules.SetColLabelValue( 3, u"SVN" )
		self.gSoftwaremodules.SetColLabelSize( 30 )
		self.gSoftwaremodules.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gSoftwaremodules.AutoSizeRows()
		self.gSoftwaremodules.EnableDragRowSize( True )
		self.gSoftwaremodules.SetRowLabelSize( 40 )
		self.gSoftwaremodules.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gSoftwaremodules.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer21.Add( self.gSoftwaremodules, 0, wx.EXPAND|wx.FIXED_MINSIZE, 5 )


		fgSizer21.Add( bSizer21, 1, wx.TOP, 5 )


		self.pMain.SetSizer( fgSizer21 )
		self.pMain.Layout()
		fgSizer21.Fit( self.pMain )
		self.pMainregister.AddPage( self.pMain, u"Allgemein", False )
		self.pEMS = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"EMS" )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook2 = wx.Notebook( self.pEMS, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel7 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer10 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer8 = wx.GridSizer( 0, 4, 0, 0 )

		self.m_staticText158 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Betriebsbereit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText158.Wrap( -1 )

		gSizer8.Add( self.m_staticText158, 0, wx.ALL, 5 )

		self.chEMSAlive = wx.CheckBox( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEMSAlive.Enable( False )

		gSizer8.Add( self.chEMSAlive, 0, wx.ALL, 5 )

		self.m_staticText661 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"PV-Leistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText661.Wrap( -1 )

		gSizer8.Add( self.m_staticText661, 0, wx.ALL, 5 )

		self.txtEMSPowerPV = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSPowerPV.Enable( False )

		gSizer8.Add( self.txtEMSPowerPV, 0, wx.ALL, 5 )

		self.m_staticText671 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Batterie Leistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText671.Wrap( -1 )

		gSizer8.Add( self.m_staticText671, 0, wx.ALL, 5 )

		self.txtEMSPowerBat = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSPowerBat.Enable( False )

		gSizer8.Add( self.txtEMSPowerBat, 0, wx.ALL, 5 )

		self.m_staticText681 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Hausverbrauch Leistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText681.Wrap( -1 )

		gSizer8.Add( self.m_staticText681, 0, wx.ALL, 5 )

		self.txtEMSPowerHome = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSPowerHome.Enable( False )

		gSizer8.Add( self.txtEMSPowerHome, 0, wx.ALL, 5 )

		self.m_staticText691 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Netzeinspeisepunkt Leistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText691.Wrap( -1 )

		gSizer8.Add( self.m_staticText691, 0, wx.ALL, 5 )

		self.txtEMSPowerGrid = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSPowerGrid.Enable( False )

		gSizer8.Add( self.txtEMSPowerGrid, 0, wx.ALL, 5 )

		self.m_staticText70 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"zusätzlicher Einspeiser Leistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText70.Wrap( -1 )

		gSizer8.Add( self.m_staticText70, 0, wx.ALL, 5 )

		self.txtEMSPowerAdd = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSPowerAdd.Enable( False )

		gSizer8.Add( self.txtEMSPowerAdd, 0, wx.ALL, 5 )

		self.m_staticText92 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"zusätzlicher Einspeiser vorhanden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92.Wrap( -1 )

		gSizer8.Add( self.m_staticText92, 0, wx.ALL, 5 )

		self.txtEMSExtSrcAvailable = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		self.txtEMSExtSrcAvailable.Enable( False )

		gSizer8.Add( self.txtEMSExtSrcAvailable, 0, wx.ALL, 5 )

		self.m_staticText1561 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Wallbox Leistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1561.Wrap( -1 )

		gSizer8.Add( self.m_staticText1561, 0, wx.ALL, 5 )

		self.txtEMSPowerWBAll = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSPowerWBAll.Enable( False )

		gSizer8.Add( self.txtEMSPowerWBAll, 0, wx.ALL, 5 )

		self.m_staticText157 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Wallbox Leistung Solar", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText157.Wrap( -1 )

		gSizer8.Add( self.m_staticText157, 0, wx.ALL, 5 )

		self.txtEMSPowerWBSolar = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSPowerWBSolar.Enable( False )

		gSizer8.Add( self.txtEMSPowerWBSolar, 0, wx.ALL, 5 )

		self.m_staticText711 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Autarkie", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText711.Wrap( -1 )

		gSizer8.Add( self.m_staticText711, 0, wx.ALL, 5 )

		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.gEMSAutarkie = wx.Gauge( self.m_panel7, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 110,-1 ), wx.GA_HORIZONTAL )
		self.gEMSAutarkie.SetValue( 0 )
		fgSizer3.Add( self.gEMSAutarkie, 0, wx.ALL, 5 )

		self.txtEMSAutarkie = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txtEMSAutarkie.Enable( False )

		fgSizer3.Add( self.txtEMSAutarkie, 0, wx.ALL, 5 )


		gSizer8.Add( fgSizer3, 1, wx.EXPAND, 5 )

		self.m_staticText72 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Eigenverbrauch", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText72.Wrap( -1 )

		gSizer8.Add( self.m_staticText72, 0, wx.ALL, 5 )

		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.gEMSSelfConsumption = wx.Gauge( self.m_panel7, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 110,-1 ), wx.GA_HORIZONTAL )
		self.gEMSSelfConsumption.SetValue( 0 )
		fgSizer4.Add( self.gEMSSelfConsumption, 0, wx.ALL, 5 )

		self.txtEMSSelfConsumption = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txtEMSSelfConsumption.Enable( False )

		fgSizer4.Add( self.txtEMSSelfConsumption, 0, wx.ALL, 5 )


		gSizer8.Add( fgSizer4, 1, wx.EXPAND, 5 )

		self.m_staticText73 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Batterieladestand", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText73.Wrap( -1 )

		gSizer8.Add( self.m_staticText73, 0, wx.ALL, 5 )

		fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.mgEMSBatSoc = wx.Gauge( self.m_panel7, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 110,-1 ), wx.GA_HORIZONTAL )
		self.mgEMSBatSoc.SetValue( 0 )
		fgSizer5.Add( self.mgEMSBatSoc, 0, wx.ALL, 5 )

		self.txtEMSBatSoc = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txtEMSBatSoc.Enable( False )

		fgSizer5.Add( self.txtEMSBatSoc, 0, wx.ALL, 5 )


		gSizer8.Add( fgSizer5, 1, wx.EXPAND, 5 )

		self.m_staticText74 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Betriebsmodus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText74.Wrap( -1 )

		gSizer8.Add( self.m_staticText74, 0, wx.ALL, 5 )

		self.txtEMSCouplingMode = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSCouplingMode.Enable( False )

		gSizer8.Add( self.txtEMSCouplingMode, 0, wx.ALL, 5 )

		self.m_staticText141 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Modus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText141.Wrap( -1 )

		gSizer8.Add( self.m_staticText141, 0, wx.ALL, 5 )

		self.txtEMSMode = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMode.Enable( False )

		gSizer8.Add( self.txtEMSMode, 0, wx.ALL, 5 )

		self.m_staticText144 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText144.Wrap( -1 )

		gSizer8.Add( self.m_staticText144, 0, wx.ALL, 5 )

		self.txtEMSStatus = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSStatus.Enable( False )

		gSizer8.Add( self.txtEMSStatus, 0, wx.ALL, 5 )

		self.m_staticText75 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Balanced Phases", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText75.Wrap( -1 )

		gSizer8.Add( self.m_staticText75, 0, wx.ALL, 5 )

		self.txtEMSBalancedPhases = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSBalancedPhases.Enable( False )

		gSizer8.Add( self.txtEMSBalancedPhases, 0, wx.ALL, 5 )

		self.m_staticText76 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Installierte Wp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText76.Wrap( -1 )

		gSizer8.Add( self.m_staticText76, 0, wx.ALL, 5 )

		self.txtEMSInstalledPeakPower = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSInstalledPeakPower.Enable( False )

		gSizer8.Add( self.txtEMSInstalledPeakPower, 0, wx.ALL, 5 )

		self.m_staticText77 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Maximale Einspeisung (%/kWp)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText77.Wrap( -1 )

		gSizer8.Add( self.m_staticText77, 0, wx.ALL, 5 )

		self.txtEMSDerateAtPercent = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSDerateAtPercent.Enable( False )

		gSizer8.Add( self.txtEMSDerateAtPercent, 0, wx.ALL, 5 )

		self.m_staticText78 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Maximale Einspeisung (W)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText78.Wrap( -1 )

		gSizer8.Add( self.m_staticText78, 0, wx.ALL, 5 )

		self.txtEMSDerateAtPower = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSDerateAtPower.Enable( False )

		gSizer8.Add( self.txtEMSDerateAtPower, 0, wx.ALL, 5 )

		self.m_staticline7 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.LI_HORIZONTAL )
		self.m_staticline7.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_staticline7.SetMinSize( wx.Size( 170,-1 ) )
		self.m_staticline7.SetMaxSize( wx.Size( 100,2 ) )

		gSizer8.Add( self.m_staticline7, 0, wx.ALIGN_BOTTOM, 5 )

		self.m_staticline8 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		self.m_staticline8.SetMinSize( wx.Size( 170,-1 ) )
		self.m_staticline8.SetMaxSize( wx.Size( -1,2 ) )

		gSizer8.Add( self.m_staticline8, 0, wx.ALIGN_BOTTOM, 5 )

		self.m_staticText85 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Notstrom Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText85.Wrap( -1 )

		gSizer8.Add( self.m_staticText85, 0, wx.ALL, 5 )

		self.txtEMSEmergencyPowerStatus = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSEmergencyPowerStatus.Enable( False )

		gSizer8.Add( self.txtEMSEmergencyPowerStatus, 0, wx.ALL, 5 )

		self.m_staticText145 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Notstrom-Test aktiv", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText145.Wrap( -1 )

		gSizer8.Add( self.m_staticText145, 0, wx.ALL, 5 )

		fgSizer14 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.chEMSEPTestRunning = wx.CheckBox( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEMSEPTestRunning.Enable( False )

		fgSizer14.Add( self.chEMSEPTestRunning, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.bEMSEPTest = wx.Button( self.m_panel7, wx.ID_ANY, u"Start!", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		fgSizer14.Add( self.bEMSEPTest, 0, wx.ALL, 5 )


		gSizer8.Add( fgSizer14, 1, wx.EXPAND, 5 )

		self.m_staticText146 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"durchgeführte Notstrom-Tests", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText146.Wrap( -1 )

		gSizer8.Add( self.m_staticText146, 0, wx.ALL, 5 )

		self.txtEMSEPTestCounter = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSEPTestCounter.Enable( False )

		gSizer8.Add( self.txtEMSEPTestCounter, 0, wx.ALL, 5 )

		self.m_staticText147 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"nächster Notstrom-Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText147.Wrap( -1 )

		gSizer8.Add( self.m_staticText147, 0, wx.ALL, 5 )

		self.txtEMSEPTestTimestamp = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSEPTestTimestamp.Enable( False )

		gSizer8.Add( self.txtEMSEPTestTimestamp, 0, wx.ALL, 5 )

		self.chEPISGridConnected = wx.CheckBox( self.m_panel7, wx.ID_ANY, u"mit Netz verbunden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEPISGridConnected.Enable( False )

		gSizer8.Add( self.chEPISGridConnected, 0, wx.ALL, 5 )

		self.chEPReadyForSwitch = wx.CheckBox( self.m_panel7, wx.ID_ANY, u"Bereit zum Wechsel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEPReadyForSwitch.Enable( False )

		gSizer8.Add( self.chEPReadyForSwitch, 0, wx.ALL, 5 )

		self.chEPIsland = wx.CheckBox( self.m_panel7, wx.ID_ANY, u"Netz im Inselbetrieb", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEPIsland.Enable( False )

		gSizer8.Add( self.chEPIsland, 0, wx.ALL, 5 )

		self.chEPPossible = wx.CheckBox( self.m_panel7, wx.ID_ANY, u"Notstrom möglich", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEPPossible.Enable( False )

		gSizer8.Add( self.chEPPossible, 0, wx.ALL, 5 )

		self.chEPInvalid = wx.CheckBox( self.m_panel7, wx.ID_ANY, u"Notstrom ungültig", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEPInvalid.Enable( False )

		gSizer8.Add( self.chEPInvalid, 0, wx.ALL, 5 )


		fgSizer10.Add( gSizer8, 1, wx.EXPAND, 5 )

		fgSizer15 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText79 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Verwendetes Ladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText79.Wrap( -1 )

		fgSizer15.Add( self.m_staticText79, 0, wx.ALL, 5 )

		self.txtEMSUsedChargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSUsedChargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSUsedChargeLimit, 0, wx.ALL, 5 )

		self.m_staticText80 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Benutzer Ladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText80.Wrap( -1 )

		fgSizer15.Add( self.m_staticText80, 0, wx.ALL, 5 )

		self.txtEMSUserChargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSUserChargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSUserChargeLimit, 0, wx.ALL, 5 )

		self.m_staticText82 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Batterie Ladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText82.Wrap( -1 )

		fgSizer15.Add( self.m_staticText82, 0, wx.ALL, 5 )

		self.txtEMSBatChargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSBatChargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSBatChargeLimit, 0, wx.ALL, 5 )

		self.m_staticText83 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"DCDC-Wandler Ladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText83.Wrap( -1 )

		fgSizer15.Add( self.m_staticText83, 0, wx.ALL, 5 )

		self.txtEMSDCDCChargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSDCDCChargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSDCDCChargeLimit, 0, wx.ALL, 5 )

		self.m_staticText84 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Verbleibende Ladeleistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText84.Wrap( -1 )

		fgSizer15.Add( self.m_staticText84, 0, wx.ALL, 5 )

		self.txtEMSRemainingBatChargePower = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSRemainingBatChargePower.Enable( False )

		fgSizer15.Add( self.txtEMSRemainingBatChargePower, 0, wx.ALL, 5 )

		self.m_staticText149 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Verwendetes Entladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText149.Wrap( -1 )

		fgSizer15.Add( self.m_staticText149, 0, wx.ALL, 5 )

		self.txtEMSUsedDischargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSUsedDischargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSUsedDischargeLimit, 0, wx.ALL, 5 )

		self.m_staticText150 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Benutzer Entladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText150.Wrap( -1 )

		fgSizer15.Add( self.m_staticText150, 0, wx.ALL, 5 )

		self.txtEMSUserDischargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSUserDischargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSUserDischargeLimit, 0, wx.ALL, 5 )

		self.m_staticText151 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Batterie Entladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText151.Wrap( -1 )

		fgSizer15.Add( self.m_staticText151, 0, wx.ALL, 5 )

		self.txtEMSBatDischargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSBatDischargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSBatDischargeLimit, 0, wx.ALL, 5 )

		self.m_staticText152 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"DCDC-Wandler Entladelimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText152.Wrap( -1 )

		fgSizer15.Add( self.m_staticText152, 0, wx.ALL, 5 )

		self.txtEMSDCDCDischargeLimit = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSDCDCDischargeLimit.Enable( False )

		fgSizer15.Add( self.txtEMSDCDCDischargeLimit, 0, wx.ALL, 5 )

		self.m_staticText153 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Verbleibende Entladeleistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText153.Wrap( -1 )

		fgSizer15.Add( self.m_staticText153, 0, wx.ALL, 5 )

		self.txtEMSRemainingBatDischargePower = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSRemainingBatDischargePower.Enable( False )

		fgSizer15.Add( self.txtEMSRemainingBatDischargePower, 0, wx.ALL, 5 )

		self.m_staticText159 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Manuelle Batterieladung aktiv", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText159.Wrap( -1 )

		fgSizer15.Add( self.m_staticText159, 0, wx.ALL, 5 )

		self.chEMSGetManualCharge = wx.CheckBox( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chEMSGetManualCharge.Enable( False )

		fgSizer15.Add( self.chEMSGetManualCharge, 0, wx.ALL, 5 )

		self.m_staticText161 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Manuell geladene Energiemenge", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText161.Wrap( -1 )

		fgSizer15.Add( self.m_staticText161, 0, wx.ALL, 5 )

		self.txtEMSManualChargeEnergyCounter = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSManualChargeEnergyCounter.Enable( False )

		fgSizer15.Add( self.txtEMSManualChargeEnergyCounter, 0, wx.ALL, 5 )

		self.m_staticText160 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"letzte manuelle Ladung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText160.Wrap( -1 )

		fgSizer15.Add( self.m_staticText160, 0, wx.ALL, 5 )

		self.txtEMSManualChargeStartCounter = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.txtEMSManualChargeStartCounter.Enable( False )

		fgSizer15.Add( self.txtEMSManualChargeStartCounter, 0, wx.ALL, 5 )

		self.m_staticText162 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"letzte manuelle Ladung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText162.Wrap( -1 )

		fgSizer15.Add( self.m_staticText162, 0, wx.ALL, 5 )

		self.txtEMSManualChargeLaststart = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.txtEMSManualChargeLaststart.Enable( False )

		fgSizer15.Add( self.txtEMSManualChargeLaststart, 0, wx.ALL, 5 )

		self.m_staticline131 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer15.Add( self.m_staticline131, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline14 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer15.Add( self.m_staticline14, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer24 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer24.SetFlexibleDirection( wx.BOTH )
		fgSizer24.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.txtEMSManualChargeValue = wx.TextCtrl( self.m_panel7, wx.ID_ANY, u"200", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		fgSizer24.Add( self.txtEMSManualChargeValue, 0, wx.ALL, 5 )

		self.m_staticText173 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Wh", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText173.Wrap( -1 )

		fgSizer24.Add( self.m_staticText173, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		fgSizer15.Add( fgSizer24, 1, wx.EXPAND, 5 )

		self.bEMSManualChargeStart = wx.Button( self.m_panel7, wx.ID_ANY, u"Manuelle Ladung starten", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer15.Add( self.bEMSManualChargeStart, 0, wx.ALL, 5 )


		fgSizer10.Add( fgSizer15, 1, wx.EXPAND, 5 )


		self.m_panel7.SetSizer( fgSizer10 )
		self.m_panel7.Layout()
		fgSizer10.Fit( self.m_panel7 )
		self.m_notebook2.AddPage( self.m_panel7, u"Basis", False )
		self.m_panel8 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		fgSizer26 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer26.SetFlexibleDirection( wx.BOTH )
		fgSizer26.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1731 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Ladeverhalten", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1731.Wrap( -1 )

		bSizer15.Add( self.m_staticText1731, 0, wx.ALL, 5 )

		self.m_staticline4 = wx.StaticLine( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer15.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer27 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer27.SetFlexibleDirection( wx.BOTH )
		fgSizer27.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText87 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Leistungslimit verwenden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText87.Wrap( -1 )

		fgSizer27.Add( self.m_staticText87, 0, wx.ALL, 5 )

		self.chEMSPowerLimitsUsed = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer27.Add( self.chEMSPowerLimitsUsed, 0, wx.ALL, 5 )

		self.m_staticText88 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Maximale Ladeleistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText88.Wrap( -1 )

		fgSizer27.Add( self.m_staticText88, 0, wx.ALL, 5 )

		fgSizer7 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.sEMSMaxChargePower = wx.Slider( self.m_panel8, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		fgSizer7.Add( self.sEMSMaxChargePower, 0, wx.ALL, 5 )

		self.txtEMSMaxChargePower = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txtEMSMaxChargePower.Enable( False )

		fgSizer7.Add( self.txtEMSMaxChargePower, 0, wx.ALL, 5 )


		fgSizer27.Add( fgSizer7, 1, wx.EXPAND, 5 )

		self.m_staticText89 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Maximale Entladeleistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText89.Wrap( -1 )

		fgSizer27.Add( self.m_staticText89, 0, wx.ALL, 5 )

		fgSizer8 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.sEMSMaxDischargePower = wx.Slider( self.m_panel8, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		fgSizer8.Add( self.sEMSMaxDischargePower, 0, wx.ALL, 5 )

		self.txtEMSMaxDischargePower = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txtEMSMaxDischargePower.Enable( False )

		fgSizer8.Add( self.txtEMSMaxDischargePower, 0, wx.ALL, 5 )


		fgSizer27.Add( fgSizer8, 1, wx.EXPAND, 5 )

		self.m_staticText142 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"untere Lade-/Entladeschwelle", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText142.Wrap( -1 )

		fgSizer27.Add( self.m_staticText142, 0, wx.ALL, 5 )

		fgSizer9 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.sEMSMaxDischargeStartPower = wx.Slider( self.m_panel8, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		fgSizer9.Add( self.sEMSMaxDischargeStartPower, 0, wx.ALL, 5 )

		self.txtEMSMaxDischargeStartPower = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txtEMSMaxDischargeStartPower.Enable( False )

		fgSizer9.Add( self.txtEMSMaxDischargeStartPower, 0, wx.ALL, 5 )


		fgSizer27.Add( fgSizer9, 1, wx.EXPAND, 5 )

		self.m_staticText90 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Stromsparen aktiviert", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText90.Wrap( -1 )

		fgSizer27.Add( self.m_staticText90, 0, wx.ALL, 5 )

		self.chEMSPowerSaveEnabled = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer27.Add( self.chEMSPowerSaveEnabled, 0, wx.ALL, 5 )

		self.m_staticText91 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Wetterprognose verwenden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )

		fgSizer27.Add( self.m_staticText91, 0, wx.ALL, 5 )

		self.chEMSWeatherRegulatedChargeEnabled = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer27.Add( self.chEMSWeatherRegulatedChargeEnabled, 0, wx.ALL, 5 )

		self.m_staticText139 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Wallbox priorisiert", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText139.Wrap( -1 )

		fgSizer27.Add( self.m_staticText139, 0, wx.ALL, 5 )

		self.chEMSBatteryBeforeCarMode = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer27.Add( self.chEMSBatteryBeforeCarMode, 0, wx.ALL, 5 )

		self.m_staticText140 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Batterieentladung durch Wallbox", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText140.Wrap( -1 )

		fgSizer27.Add( self.m_staticText140, 0, wx.ALL, 5 )

		self.chEMSBatteryToCarMode = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer27.Add( self.chEMSBatteryToCarMode, 0, wx.ALL, 5 )


		bSizer15.Add( fgSizer27, 1, wx.EXPAND, 5 )


		fgSizer26.Add( bSizer15, 1, wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText93 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Ladesperrzeiten", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )

		bSizer9.Add( self.m_staticText93, 0, wx.ALL, 5 )

		self.m_staticline5 = wx.StaticLine( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer9.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

		gSizer13 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText94 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Montag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText94.Wrap( -1 )

		gSizer13.Add( self.m_staticText94, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSChargeMo = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer13.Add( self.chEMSChargeMo, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeMoVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13.Add( self.tpEMSChargeMoVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText95 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText95.Wrap( -1 )

		gSizer13.Add( self.m_staticText95, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeMoBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13.Add( self.tpEMSChargeMoBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer9.Add( gSizer13, 1, wx.EXPAND, 2 )

		gSizer131 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText941 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Dienstag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText941.Wrap( -1 )

		gSizer131.Add( self.m_staticText941, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSChargeDi = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer131.Add( self.chEMSChargeDi, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeDiVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131.Add( self.tpEMSChargeDiVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText951 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText951.Wrap( -1 )

		gSizer131.Add( self.m_staticText951, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeDiBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131.Add( self.tpEMSChargeDiBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer9.Add( gSizer131, 1, wx.EXPAND, 2 )

		gSizer1311 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText9411 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Mittwoch", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9411.Wrap( -1 )

		gSizer1311.Add( self.m_staticText9411, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSChargeMi = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1311.Add( self.chEMSChargeMi, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeMiVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer1311.Add( self.tpEMSChargeMiVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText9511 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9511.Wrap( -1 )

		gSizer1311.Add( self.m_staticText9511, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeMiBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer1311.Add( self.tpEMSChargeMiBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer9.Add( gSizer1311, 1, wx.EXPAND, 5 )

		gSizer13111 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText94111 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Donnerstag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText94111.Wrap( -1 )

		gSizer13111.Add( self.m_staticText94111, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSChargeDo = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer13111.Add( self.chEMSChargeDo, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeDoVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13111.Add( self.tpEMSChargeDoVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText95111 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText95111.Wrap( -1 )

		gSizer13111.Add( self.m_staticText95111, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeDoBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13111.Add( self.tpEMSChargeDoBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer9.Add( gSizer13111, 1, wx.EXPAND, 5 )

		gSizer13112 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText94112 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Freitag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText94112.Wrap( -1 )

		gSizer13112.Add( self.m_staticText94112, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSChargeFr = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer13112.Add( self.chEMSChargeFr, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeFrVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13112.Add( self.tpEMSChargeFrVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText95112 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText95112.Wrap( -1 )

		gSizer13112.Add( self.m_staticText95112, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeFrBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13112.Add( self.tpEMSChargeFrBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer9.Add( gSizer13112, 1, wx.EXPAND, 5 )

		gSizer13113 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText94113 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Samstag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText94113.Wrap( -1 )

		gSizer13113.Add( self.m_staticText94113, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSChargeSa = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer13113.Add( self.chEMSChargeSa, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeSaVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13113.Add( self.tpEMSChargeSaVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText95113 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText95113.Wrap( -1 )

		gSizer13113.Add( self.m_staticText95113, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeSaBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13113.Add( self.tpEMSChargeSaBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer9.Add( gSizer13113, 1, wx.EXPAND, 5 )

		gSizer131131 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText941131 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Sonntag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText941131.Wrap( -1 )

		gSizer131131.Add( self.m_staticText941131, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSChargeSo = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer131131.Add( self.chEMSChargeSo, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeSoVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131131.Add( self.tpEMSChargeSoVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText951131 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText951131.Wrap( -1 )

		gSizer131131.Add( self.m_staticText951131, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSChargeSoBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131131.Add( self.tpEMSChargeSoBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer9.Add( gSizer131131, 1, wx.EXPAND, 5 )


		bSizer14.Add( bSizer9, 1, wx.EXPAND, 5 )


		fgSizer26.Add( bSizer14, 1, wx.EXPAND, 2 )

		bSizer22 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText931 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Entladesperrzeiten", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText931.Wrap( -1 )

		bSizer22.Add( self.m_staticText931, 0, wx.ALL, 5 )

		self.m_staticline31 = wx.StaticLine( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer22.Add( self.m_staticline31, 0, wx.EXPAND |wx.ALL, 5 )

		gSizer132 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText942 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Montag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText942.Wrap( -1 )

		gSizer132.Add( self.m_staticText942, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSDischargeMo = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer132.Add( self.chEMSDischargeMo, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeMoVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer132.Add( self.tpEMSDischargeMoVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText952 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText952.Wrap( -1 )

		gSizer132.Add( self.m_staticText952, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeMoBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer132.Add( self.tpEMSDischargeMoBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer22.Add( gSizer132, 1, wx.EXPAND, 2 )

		gSizer1312 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText9412 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Dienstag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9412.Wrap( -1 )

		gSizer1312.Add( self.m_staticText9412, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSDischargeDi = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1312.Add( self.chEMSDischargeDi, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeDiVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer1312.Add( self.tpEMSDischargeDiVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText9512 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9512.Wrap( -1 )

		gSizer1312.Add( self.m_staticText9512, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeDiBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer1312.Add( self.tpEMSDischargeDiBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer22.Add( gSizer1312, 1, wx.EXPAND, 2 )

		gSizer13114 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText94114 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Mittwoch", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText94114.Wrap( -1 )

		gSizer13114.Add( self.m_staticText94114, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSDischargeMi = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer13114.Add( self.chEMSDischargeMi, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeMiVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13114.Add( self.tpEMSDischargeMiVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText95114 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText95114.Wrap( -1 )

		gSizer13114.Add( self.m_staticText95114, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeMiBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer13114.Add( self.tpEMSDischargeMiBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer22.Add( gSizer13114, 1, wx.EXPAND, 5 )

		gSizer131111 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText941111 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Donnerstag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText941111.Wrap( -1 )

		gSizer131111.Add( self.m_staticText941111, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSDischargeDo = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer131111.Add( self.chEMSDischargeDo, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeDoVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131111.Add( self.tpEMSDischargeDoVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText951111 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText951111.Wrap( -1 )

		gSizer131111.Add( self.m_staticText951111, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeDoBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131111.Add( self.tpEMSDischargeDoBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer22.Add( gSizer131111, 1, wx.EXPAND, 5 )

		gSizer131121 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText941121 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Freitag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText941121.Wrap( -1 )

		gSizer131121.Add( self.m_staticText941121, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSDischargeFr = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer131121.Add( self.chEMSDischargeFr, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeFrVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131121.Add( self.tpEMSDischargeFrVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText951121 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText951121.Wrap( -1 )

		gSizer131121.Add( self.m_staticText951121, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeFrBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131121.Add( self.tpEMSDischargeFrBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer22.Add( gSizer131121, 1, wx.EXPAND, 5 )

		gSizer131132 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText941132 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Samstag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText941132.Wrap( -1 )

		gSizer131132.Add( self.m_staticText941132, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSDischargeSa = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer131132.Add( self.chEMSDischargeSa, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeSaVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131132.Add( self.tpEMSDischargeSaVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText951132 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText951132.Wrap( -1 )

		gSizer131132.Add( self.m_staticText951132, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeSaBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer131132.Add( self.tpEMSDischargeSaBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer22.Add( gSizer131132, 1, wx.EXPAND, 5 )

		gSizer1311311 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_staticText9411311 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Sonntag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9411311.Wrap( -1 )

		gSizer1311311.Add( self.m_staticText9411311, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.chEMSDischargeSo = wx.CheckBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1311311.Add( self.chEMSDischargeSo, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeSoVon = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer1311311.Add( self.tpEMSDischargeSoVon, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText9511311 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"bis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9511311.Wrap( -1 )

		gSizer1311311.Add( self.m_staticText9511311, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.tpEMSDischargeSoBis = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		gSizer1311311.Add( self.tpEMSDischargeSoBis, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer22.Add( gSizer1311311, 1, wx.EXPAND, 5 )


		fgSizer26.Add( bSizer22, 1, wx.EXPAND, 2 )


		bSizer7.Add( fgSizer26, 1, wx.EXPAND, 5 )

		self.bEMSUploadChanges = wx.Button( self.m_panel8, wx.ID_ANY, u"Änderungen übertragen", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.bEMSUploadChanges, 0, wx.ALL, 5 )


		self.m_panel8.SetSizer( bSizer7 )
		self.m_panel8.Layout()
		bSizer7.Fit( self.m_panel8 )
		self.m_notebook2.AddPage( self.m_panel8, u"Ladeeinstellungen", False )
		self.m_panel9 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer12 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer95 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText122 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"hybridModeSupported", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText122.Wrap( -1 )

		gSizer95.Add( self.m_staticText122, 0, wx.ALL, 5 )

		self.txtEMSHybridModeSupported = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSHybridModeSupported.Enable( False )

		gSizer95.Add( self.txtEMSHybridModeSupported, 0, wx.ALL, 5 )

		self.m_staticText123 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"installedBatteryCapacity", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText123.Wrap( -1 )

		gSizer95.Add( self.m_staticText123, 0, wx.ALL, 5 )

		self.txtEMSInstalledBatteryCapacity = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSInstalledBatteryCapacity.Enable( False )

		gSizer95.Add( self.txtEMSInstalledBatteryCapacity, 0, wx.ALL, 5 )

		self.m_staticText124 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxAcPower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText124.Wrap( -1 )

		gSizer95.Add( self.m_staticText124, 0, wx.ALL, 5 )

		self.txtEMSMaxAcPower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxAcPower.Enable( False )

		gSizer95.Add( self.txtEMSMaxAcPower, 0, wx.ALL, 5 )

		self.m_staticText125 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxBatChargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText125.Wrap( -1 )

		gSizer95.Add( self.m_staticText125, 0, wx.ALL, 5 )

		self.txtEMSMaxBatChargePower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxBatChargePower.Enable( False )

		gSizer95.Add( self.txtEMSMaxBatChargePower, 0, wx.ALL, 5 )

		self.m_staticText126 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxBatDischargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText126.Wrap( -1 )

		gSizer95.Add( self.m_staticText126, 0, wx.ALL, 5 )

		self.txtEMSMaxBatDischargePower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxBatDischargePower.Enable( False )

		gSizer95.Add( self.txtEMSMaxBatDischargePower, 0, wx.ALL, 5 )

		self.m_staticText127 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxChargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText127.Wrap( -1 )

		gSizer95.Add( self.m_staticText127, 0, wx.ALL, 5 )

		self.txtEMSMaxChargePowerSys = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxChargePowerSys.Enable( False )

		gSizer95.Add( self.txtEMSMaxChargePowerSys, 0, wx.ALL, 5 )

		self.m_staticText128 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxDischargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText128.Wrap( -1 )

		gSizer95.Add( self.m_staticText128, 0, wx.ALL, 5 )

		self.txtEMSMaxDischargePowerSys = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxDischargePowerSys.Enable( False )

		gSizer95.Add( self.txtEMSMaxDischargePowerSys, 0, wx.ALL, 5 )

		self.m_staticText129 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxFbcDischargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText129.Wrap( -1 )

		gSizer95.Add( self.m_staticText129, 0, wx.ALL, 5 )

		self.txtEMSMaxFbcDischargePower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxFbcDischargePower.Enable( False )

		gSizer95.Add( self.txtEMSMaxFbcDischargePower, 0, wx.ALL, 5 )

		self.m_staticText130 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxPvPower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText130.Wrap( -1 )

		gSizer95.Add( self.m_staticText130, 0, wx.ALL, 5 )

		self.txtEMSMaxPVPower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxPVPower.Enable( False )

		gSizer95.Add( self.txtEMSMaxPVPower, 0, wx.ALL, 5 )

		self.m_staticText131 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxStartChargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )

		gSizer95.Add( self.m_staticText131, 0, wx.ALL, 5 )

		self.txtEMSMaxStartChargePower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxStartChargePower.Enable( False )

		gSizer95.Add( self.txtEMSMaxStartChargePower, 0, wx.ALL, 5 )

		self.m_staticText132 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"maxStartDischargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText132.Wrap( -1 )

		gSizer95.Add( self.m_staticText132, 0, wx.ALL, 5 )

		self.txtEMSMaxStartDischargePower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMaxStartDischargePower.Enable( False )

		gSizer95.Add( self.txtEMSMaxStartDischargePower, 0, wx.ALL, 5 )

		self.m_staticText133 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"minStartChargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText133.Wrap( -1 )

		gSizer95.Add( self.m_staticText133, 0, wx.ALL, 5 )

		self.txtEMSMinStartChargePower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMinStartChargePower.Enable( False )

		gSizer95.Add( self.txtEMSMinStartChargePower, 0, wx.ALL, 5 )

		self.m_staticText134 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"minStartDischargePower", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText134.Wrap( -1 )

		gSizer95.Add( self.m_staticText134, 0, wx.ALL, 5 )

		self.txtEMSMinStartDischargePower = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSMinStartDischargePower.Enable( False )

		gSizer95.Add( self.txtEMSMinStartDischargePower, 0, wx.ALL, 5 )

		self.m_staticText135 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"recommendedMinChargeLimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText135.Wrap( -1 )

		gSizer95.Add( self.m_staticText135, 0, wx.ALL, 5 )

		self.txtEMSRecommendedMinChargeLimit = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSRecommendedMinChargeLimit.Enable( False )

		gSizer95.Add( self.txtEMSRecommendedMinChargeLimit, 0, wx.ALL, 5 )

		self.m_staticText136 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"recommendedMinDischargeLimit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText136.Wrap( -1 )

		gSizer95.Add( self.m_staticText136, 0, wx.ALL, 5 )

		self.txtEMSRecommendedMinDischargeLimit = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSRecommendedMinDischargeLimit.Enable( False )

		gSizer95.Add( self.txtEMSRecommendedMinDischargeLimit, 0, wx.ALL, 5 )

		self.m_staticText137 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"startChargeDefault", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText137.Wrap( -1 )

		gSizer95.Add( self.m_staticText137, 0, wx.ALL, 5 )

		self.txtEMSstartChargeDefault = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSstartChargeDefault.Enable( False )

		gSizer95.Add( self.txtEMSstartChargeDefault, 0, wx.ALL, 5 )

		self.m_staticText138 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"startDischargeDefault", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText138.Wrap( -1 )

		gSizer95.Add( self.m_staticText138, 0, wx.ALL, 5 )

		self.txtEMSstartDischargeDefault = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEMSstartDischargeDefault.Enable( False )

		gSizer95.Add( self.txtEMSstartDischargeDefault, 0, wx.ALL, 5 )


		fgSizer12.Add( gSizer95, 1, wx.EXPAND, 5 )


		self.m_panel9.SetSizer( fgSizer12 )
		self.m_panel9.Layout()
		fgSizer12.Fit( self.m_panel9 )
		self.m_notebook2.AddPage( self.m_panel9, u"SYS", False )
		self.m_panel11 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel11.Enable( False )

		fgSizer272 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer272.SetFlexibleDirection( wx.BOTH )
		fgSizer272.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1733 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"aktiv", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1733.Wrap( -1 )

		fgSizer272.Add( self.m_staticText1733, 0, wx.ALL, 5 )

		self.chMBSEnabled = wx.CheckBox( self.m_panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chMBSEnabled.SetValue(True)
		fgSizer272.Add( self.chMBSEnabled, 0, wx.ALL, 5 )

		self.m_staticText174 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText174.Wrap( -1 )

		fgSizer272.Add( self.m_staticText174, 0, wx.ALL, 5 )

		self.txtMBSName = wx.TextCtrl( self.m_panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMBSName.Enable( False )

		fgSizer272.Add( self.txtMBSName, 0, wx.ALL, 5 )

		self.m_staticText175 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"ID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText175.Wrap( -1 )

		fgSizer272.Add( self.m_staticText175, 0, wx.ALL, 5 )

		self.txtMBSID = wx.TextCtrl( self.m_panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMBSID.Enable( False )

		fgSizer272.Add( self.txtMBSID, 0, wx.ALL, 5 )

		self.m_staticText176 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"Protokoll", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText176.Wrap( -1 )

		fgSizer272.Add( self.m_staticText176, 0, wx.ALL, 5 )

		cbMBSProtokollChoices = []
		self.cbMBSProtokoll = wx.ComboBox( self.m_panel11, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, cbMBSProtokollChoices, 0 )
		self.cbMBSProtokoll.Enable( False )

		fgSizer272.Add( self.cbMBSProtokoll, 0, wx.ALL, 5 )

		self.m_staticText177 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"Gerät", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText177.Wrap( -1 )

		fgSizer272.Add( self.m_staticText177, 0, wx.ALL, 5 )

		self.txtMBSDevice = wx.TextCtrl( self.m_panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMBSDevice.Enable( False )

		fgSizer272.Add( self.txtMBSDevice, 0, wx.ALL, 5 )

		self.m_staticText178 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"TCP-Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText178.Wrap( -1 )

		fgSizer272.Add( self.m_staticText178, 0, wx.ALL, 5 )

		self.txtMBSPort = wx.TextCtrl( self.m_panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMBSPort.Enable( False )

		fgSizer272.Add( self.txtMBSPort, 0, wx.ALL, 5 )

		self.bMBSSave = wx.Button( self.m_panel11, wx.ID_ANY, u"Änderungen übertragen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer272.Add( self.bMBSSave, 0, wx.ALL, 5 )


		self.m_panel11.SetSizer( fgSizer272 )
		self.m_panel11.Layout()
		fgSizer272.Fit( self.m_panel11 )
		self.m_notebook2.AddPage( self.m_panel11, u"Modbus", False )
		self.m_panel15 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer201 = wx.BoxSizer( wx.VERTICAL )

		bSizer201.SetMinSize( wx.Size( 400,-1 ) )
		self.gStorederrors = wx.grid.Grid( self.m_panel15, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.gStorederrors.CreateGrid( 5, 5 )
		self.gStorederrors.EnableEditing( True )
		self.gStorederrors.EnableGridLines( True )
		self.gStorederrors.EnableDragGridSize( False )
		self.gStorederrors.SetMargins( 0, 0 )

		# Columns
		self.gStorederrors.EnableDragColMove( False )
		self.gStorederrors.EnableDragColSize( True )
		self.gStorederrors.SetColLabelValue( 0, u"Type" )
		self.gStorederrors.SetColLabelValue( 1, u"Quelle" )
		self.gStorederrors.SetColLabelValue( 2, u"Nachricht" )
		self.gStorederrors.SetColLabelValue( 3, u"Errorcode" )
		self.gStorederrors.SetColLabelValue( 4, u"Datum/Uhrzeit" )
		self.gStorederrors.SetColLabelValue( 5, wx.EmptyString )
		self.gStorederrors.SetColLabelValue( 6, wx.EmptyString )
		self.gStorederrors.SetColLabelValue( 7, wx.EmptyString )
		self.gStorederrors.SetColLabelSize( 30 )
		self.gStorederrors.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gStorederrors.EnableDragRowSize( True )
		self.gStorederrors.SetRowLabelSize( 80 )
		self.gStorederrors.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gStorederrors.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer201.Add( self.gStorederrors, 0, wx.ALL, 5 )


		self.m_panel15.SetSizer( bSizer201 )
		self.m_panel15.Layout()
		bSizer201.Fit( self.m_panel15 )
		self.m_notebook2.AddPage( self.m_panel15, u"Fehlermeldungen", True )

		bSizer12.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )


		self.pEMS.SetSizer( bSizer12 )
		self.pEMS.Layout()
		bSizer12.Fit( self.pEMS )
		self.pMainregister.AddPage( self.pEMS, u"E3DC", False )
		self.pDCDC = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"DCDC" )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )

		self.gDCDC = wx.grid.Grid( self.pDCDC, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,500 ), 0 )

		# Grid
		self.gDCDC.CreateGrid( 12, 2 )
		self.gDCDC.EnableEditing( True )
		self.gDCDC.EnableGridLines( True )
		self.gDCDC.EnableDragGridSize( False )
		self.gDCDC.SetMargins( 0, 0 )

		# Columns
		self.gDCDC.AutoSizeColumns()
		self.gDCDC.EnableDragColMove( False )
		self.gDCDC.EnableDragColSize( True )
		self.gDCDC.SetColLabelValue( 0, u"#0" )
		self.gDCDC.SetColLabelValue( 1, u"#1" )
		self.gDCDC.SetColLabelSize( 30 )
		self.gDCDC.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gDCDC.EnableDragRowSize( True )
		self.gDCDC.SetRowLabelValue( 0, u"Stromstärke BAT" )
		self.gDCDC.SetRowLabelValue( 1, u"Spannung BAT" )
		self.gDCDC.SetRowLabelValue( 2, u"Leistung BAT" )
		self.gDCDC.SetRowLabelValue( 3, u"Stromstärke DCL" )
		self.gDCDC.SetRowLabelValue( 4, u"Spannung DCL" )
		self.gDCDC.SetRowLabelValue( 5, u"Leistung DCL" )
		self.gDCDC.SetRowLabelValue( 6, u"Firmware Version" )
		self.gDCDC.SetRowLabelValue( 7, u"FPGA Version" )
		self.gDCDC.SetRowLabelValue( 8, u"Seriennummer" )
		self.gDCDC.SetRowLabelValue( 9, u"Board Version" )
		self.gDCDC.SetRowLabelValue( 10, u"State" )
		self.gDCDC.SetRowLabelValue( 11, u"Substatus" )
		self.gDCDC.SetRowLabelSize( 120 )
		self.gDCDC.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gDCDC.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer41.Add( self.gDCDC, 0, wx.ALL|wx.EXPAND, 5 )


		self.pDCDC.SetSizer( bSizer41 )
		self.pDCDC.Layout()
		bSizer41.Fit( self.pDCDC )
		self.pMainregister.AddPage( self.pDCDC, u"DCDC-Wandler", False )
		self.pBAT = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"BAT" )
		bSizer42 = wx.BoxSizer( wx.VERTICAL )

		cbBATIndexChoices = []
		self.cbBATIndex = wx.ComboBox( self.pBAT, wx.ID_ANY, u"BAT Index", wx.DefaultPosition, wx.DefaultSize, cbBATIndexChoices, 0 )
		bSizer42.Add( self.cbBATIndex, 0, wx.ALL, 5 )

		self.m_staticline15 = wx.StaticLine( self.pBAT, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer42.Add( self.m_staticline15, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer23 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer23.SetFlexibleDirection( wx.BOTH )
		fgSizer23.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer3 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText15 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Modulespannung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		gSizer3.Add( self.m_staticText15, 0, wx.ALL, 5 )

		self.txtModuleVoltage = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtModuleVoltage.Enable( False )

		gSizer3.Add( self.txtModuleVoltage, 0, wx.ALL, 5 )

		self.m_staticText17 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Maximale Modulspannung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		gSizer3.Add( self.m_staticText17, 0, wx.ALL, 5 )

		self.txtMaxBatVoltage = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMaxBatVoltage.Enable( False )

		gSizer3.Add( self.txtMaxBatVoltage, 0, wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Stromstärke", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		gSizer3.Add( self.m_staticText16, 0, wx.ALL, 5 )

		self.txtCurrent = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtCurrent.Enable( False )

		gSizer3.Add( self.txtCurrent, 0, wx.ALL, 5 )

		self.m_staticText18 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Maximaler Ladestrom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		gSizer3.Add( self.m_staticText18, 0, wx.ALL, 5 )

		self.txtMaxChargeCurrent = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMaxChargeCurrent.Enable( False )

		gSizer3.Add( self.txtMaxChargeCurrent, 0, wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Entladeschlussspannung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		gSizer3.Add( self.m_staticText19, 0, wx.ALL, 5 )

		self.txtEodVoltage = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtEodVoltage.Enable( False )

		gSizer3.Add( self.txtEodVoltage, 0, wx.ALL, 5 )

		self.m_staticText20 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Maximaler Entladestrom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		gSizer3.Add( self.m_staticText20, 0, wx.ALL, 5 )

		self.txtMaxDischargeCurrent = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMaxDischargeCurrent.Enable( False )

		gSizer3.Add( self.txtMaxDischargeCurrent, 0, wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Ladezyklen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		gSizer3.Add( self.m_staticText21, 0, wx.ALL, 5 )

		self.txtChargeCycles = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtChargeCycles.Enable( False )

		gSizer3.Add( self.txtChargeCycles, 0, wx.ALL, 5 )

		self.m_staticText22 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Terminalspannung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		gSizer3.Add( self.m_staticText22, 0, wx.ALL, 5 )

		self.txtTerminalVoltage = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtTerminalVoltage.Enable( False )

		gSizer3.Add( self.txtTerminalVoltage, 0, wx.ALL, 5 )

		self.m_staticText23 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Statuscode", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )

		gSizer3.Add( self.m_staticText23, 0, wx.ALL, 5 )

		self.txtBatStatusCode = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBatStatusCode.Enable( False )

		gSizer3.Add( self.txtBatStatusCode, 0, wx.ALL, 5 )

		self.m_staticText24 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Errorcode", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )

		gSizer3.Add( self.m_staticText24, 0, wx.ALL, 5 )

		self.txtErrorCode = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtErrorCode.Enable( False )

		gSizer3.Add( self.txtErrorCode, 0, wx.ALL, 5 )

		self.m_staticText25 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Gerätename", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )

		gSizer3.Add( self.m_staticText25, 0, wx.ALL, 5 )

		self.txtBatDeviceName = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBatDeviceName.Enable( False )

		gSizer3.Add( self.txtBatDeviceName, 0, wx.ALL, 5 )

		self.m_staticText26 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Anzahl Batteriemodule", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )

		gSizer3.Add( self.m_staticText26, 0, wx.ALL, 5 )

		self.txtDcbCount = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtDcbCount.Enable( False )

		gSizer3.Add( self.txtDcbCount, 0, wx.ALL, 5 )

		self.m_staticText163 = wx.StaticText( self.pBAT, wx.ID_ANY, u"maximale Anzahl Batteriemodule", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText163.Wrap( -1 )

		gSizer3.Add( self.m_staticText163, 0, wx.ALL, 5 )

		self.txtBATMaxDCBCount = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBATMaxDCBCount.Enable( False )

		gSizer3.Add( self.txtBATMaxDCBCount, 0, wx.ALL, 5 )

		self.m_staticText164 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Kapazität", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText164.Wrap( -1 )

		gSizer3.Add( self.m_staticText164, 0, wx.ALL, 5 )

		self.txtBATCapacity = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBATCapacity.Enable( False )

		gSizer3.Add( self.txtBATCapacity, 0, wx.ALL, 5 )

		self.m_staticText165 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Maximale Ladeleistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText165.Wrap( -1 )

		gSizer3.Add( self.m_staticText165, 0, wx.ALL, 5 )

		self.txtBATMaxChargePower = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBATMaxChargePower.Enable( False )

		gSizer3.Add( self.txtBATMaxChargePower, 0, wx.ALL, 5 )

		self.m_staticText166 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Maximale Entladeleistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText166.Wrap( -1 )

		gSizer3.Add( self.m_staticText166, 0, wx.ALL, 5 )

		self.txtBATMaxDischargePower = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBATMaxDischargePower.Enable( False )

		gSizer3.Add( self.txtBATMaxDischargePower, 0, wx.ALL, 5 )

		self.m_staticText167 = wx.StaticText( self.pBAT, wx.ID_ANY, u"gemessener Widerstand", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText167.Wrap( -1 )

		gSizer3.Add( self.m_staticText167, 0, wx.ALL, 5 )

		self.txtBATMeasuredResistance = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBATMeasuredResistance.Enable( False )

		gSizer3.Add( self.txtBATMeasuredResistance, 0, wx.ALL, 5 )

		self.m_staticText168 = wx.StaticText( self.pBAT, wx.ID_ANY, u"gemessener Widerstand (RUN)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText168.Wrap( -1 )

		gSizer3.Add( self.m_staticText168, 0, wx.ALL, 5 )

		self.txtBATRunMeasuredResistance = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBATRunMeasuredResistance.Enable( False )

		gSizer3.Add( self.txtBATRunMeasuredResistance, 0, wx.ALL, 5 )

		self.m_staticText27 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Maximale Modultemperatur", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		gSizer3.Add( self.m_staticText27, 0, wx.ALL, 5 )

		self.txtMaxDcbCellTemperature = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMaxDcbCellTemperature.Enable( False )

		gSizer3.Add( self.txtMaxDcbCellTemperature, 0, wx.ALL, 5 )

		self.m_staticText28 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Minimale Modultemperatur", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )

		gSizer3.Add( self.m_staticText28, 0, wx.ALL, 5 )

		self.txtMinDcbCellTemperature = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMinDcbCellTemperature.Enable( False )

		gSizer3.Add( self.txtMinDcbCellTemperature, 0, wx.ALL, 5 )

		self.m_staticText29 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Training Modus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		gSizer3.Add( self.m_staticText29, 0, wx.ALL, 5 )

		self.txtBatTrainingMode = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtBatTrainingMode.Enable( False )

		gSizer3.Add( self.txtBatTrainingMode, 0, wx.ALL, 5 )

		self.m_staticText30 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Nutzbare Kapazität", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )

		gSizer3.Add( self.m_staticText30, 0, wx.ALL, 5 )

		self.txtUsableCapacity = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtUsableCapacity.Enable( False )

		gSizer3.Add( self.txtUsableCapacity, 0, wx.ALL, 5 )

		self.m_staticText31 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Restliche nutzbare Kapazität", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		gSizer3.Add( self.m_staticText31, 0, wx.ALL, 5 )

		self.txtUsableRemainingCapacity = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtUsableRemainingCapacity.Enable( False )

		gSizer3.Add( self.txtUsableRemainingCapacity, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Maximale Kapazität", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		gSizer3.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.txtFCC = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtFCC.Enable( False )

		gSizer3.Add( self.txtFCC, 0, wx.ALL, 5 )

		self.m_staticText34 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Verbleibende Kapazität", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )

		gSizer3.Add( self.m_staticText34, 0, wx.ALL, 5 )

		self.txtRC = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtRC.Enable( False )

		gSizer3.Add( self.txtRC, 0, wx.ALL, 5 )

		self.m_staticText32 = wx.StaticText( self.pBAT, wx.ID_ANY, u"State of Health (SOH)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		gSizer3.Add( self.m_staticText32, 0, wx.ALL, 5 )

		self.txtASOC = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtASOC.Enable( False )

		gSizer3.Add( self.txtASOC, 0, wx.ALL, 5 )

		self.m_staticText14 = wx.StaticText( self.pBAT, wx.ID_ANY, u"SOC im Portal", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		gSizer3.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.txtRSOC = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtRSOC.Enable( False )

		gSizer3.Add( self.txtRSOC, 0, wx.ALL, 5 )

		self.m_staticText341 = wx.StaticText( self.pBAT, wx.ID_ANY, u"Tatsächlicher SOC", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText341.Wrap( -1 )

		gSizer3.Add( self.m_staticText341, 0, wx.ALL, 5 )

		self.txtRSOCREAL = wx.TextCtrl( self.pBAT, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtRSOCREAL.Enable( False )

		gSizer3.Add( self.txtRSOCREAL, 0, wx.ALL, 5 )

		self.chBATDeviceConnected = wx.CheckBox( self.pBAT, wx.ID_ANY, u"Gerät verbunden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chBATDeviceConnected.Enable( False )

		gSizer3.Add( self.chBATDeviceConnected, 0, wx.ALL, 5 )


		gSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.chBATDeviceWorking = wx.CheckBox( self.pBAT, wx.ID_ANY, u"Gerät arbeitet", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chBATDeviceWorking.Enable( False )

		gSizer3.Add( self.chBATDeviceWorking, 0, wx.ALL, 5 )


		gSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.chBATDeviceInService = wx.CheckBox( self.pBAT, wx.ID_ANY, u"Gerät in Wartung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chBATDeviceInService.Enable( False )

		gSizer3.Add( self.chBATDeviceInService, 0, wx.ALL, 5 )


		fgSizer23.Add( gSizer3, 1, wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.gDCB = wx.grid.Grid( self.pBAT, wx.ID_ANY, wx.DefaultPosition, wx.Size( 600,-1 ), 0 )

		# Grid
		self.gDCB.CreateGrid( 31, 2 )
		self.gDCB.EnableEditing( True )
		self.gDCB.EnableGridLines( True )
		self.gDCB.EnableDragGridSize( False )
		self.gDCB.SetMargins( 0, 0 )

		# Columns
		self.gDCB.EnableDragColMove( False )
		self.gDCB.EnableDragColSize( True )
		self.gDCB.SetColLabelSize( 30 )
		self.gDCB.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gDCB.EnableDragRowSize( True )
		self.gDCB.SetRowLabelValue( 0, u"Letzte Meldung" )
		self.gDCB.SetRowLabelValue( 1, u"Maximale Ladespannung" )
		self.gDCB.SetRowLabelValue( 2, u"Maximaler Ladestrom" )
		self.gDCB.SetRowLabelValue( 3, u"Entladeschlussspannung" )
		self.gDCB.SetRowLabelValue( 4, u"Maximaler Entladestrom" )
		self.gDCB.SetRowLabelValue( 5, u"Maximale Kapazität" )
		self.gDCB.SetRowLabelValue( 6, u"Verbleibende Kapazität" )
		self.gDCB.SetRowLabelValue( 7, u"State of Charge (SOC)" )
		self.gDCB.SetRowLabelValue( 8, u"State of Health (SOH)" )
		self.gDCB.SetRowLabelValue( 9, u"Ladezyklen" )
		self.gDCB.SetRowLabelValue( 10, u"Stromstärke" )
		self.gDCB.SetRowLabelValue( 11, u"Spannung" )
		self.gDCB.SetRowLabelValue( 12, u"Stromstärke 30s" )
		self.gDCB.SetRowLabelValue( 13, u"Spannung 30s" )
		self.gDCB.SetRowLabelValue( 14, u"Ursprüngliche Kapazität" )
		self.gDCB.SetRowLabelValue( 15, u"Ursprüngliche Spannung" )
		self.gDCB.SetRowLabelValue( 16, u"Minimale Ladetemperatur" )
		self.gDCB.SetRowLabelValue( 17, u"Maximale Ladetemperatur" )
		self.gDCB.SetRowLabelValue( 18, u"Hersteller" )
		self.gDCB.SetRowLabelValue( 19, u"Typ" )
		self.gDCB.SetRowLabelValue( 20, u"Herstellungsdatum" )
		self.gDCB.SetRowLabelValue( 21, u"Seriennummer" )
		self.gDCB.SetRowLabelValue( 22, u"Firmwareversion" )
		self.gDCB.SetRowLabelValue( 23, u"PCB Version" )
		self.gDCB.SetRowLabelValue( 24, u"Datatable Version" )
		self.gDCB.SetRowLabelValue( 25, u"Protokollversion" )
		self.gDCB.SetRowLabelValue( 26, u"Zellanzahl in Serie" )
		self.gDCB.SetRowLabelValue( 27, u"Zellanzahl in Parallel" )
		self.gDCB.SetRowLabelValue( 28, u"Serielcode" )
		self.gDCB.SetRowLabelValue( 29, u"Nr Sensor" )
		self.gDCB.SetRowLabelValue( 30, u"Seriencode" )
		self.gDCB.SetRowLabelValue( 31, u"Status" )
		self.gDCB.SetRowLabelSize( 160 )
		self.gDCB.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gDCB.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer5.Add( self.gDCB, 0, wx.ALL, 5 )


		fgSizer23.Add( bSizer5, 1, wx.EXPAND, 5 )


		bSizer42.Add( fgSizer23, 1, wx.EXPAND, 5 )


		self.pBAT.SetSizer( bSizer42 )
		self.pBAT.Layout()
		bSizer42.Fit( self.pBAT )
		self.pMainregister.AddPage( self.pBAT, u"Batterien", False )
		self.pPVI = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"PVI" )
		bSizer51 = wx.BoxSizer( wx.VERTICAL )

		chPVIIndexChoices = []
		self.chPVIIndex = wx.ComboBox( self.pPVI, wx.ID_ANY, u"PVI Index", wx.DefaultPosition, wx.DefaultSize, chPVIIndexChoices, 0 )
		bSizer51.Add( self.chPVIIndex, 0, wx.ALL, 5 )

		self.m_staticline16 = wx.StaticLine( self.pPVI, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer51.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )

		gSizer51 = wx.GridSizer( 0, 2, 0, 0 )

		fgSizer25 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer25.SetFlexibleDirection( wx.BOTH )
		fgSizer25.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer4 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText36 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Seriennummer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText36.Wrap( -1 )

		gSizer4.Add( self.m_staticText36, 0, wx.ALL, 5 )

		self.txtPVISerialNumber = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVISerialNumber.Enable( False )

		gSizer4.Add( self.txtPVISerialNumber, 0, wx.ALL, 5 )

		self.m_staticText37 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Wechselrichtertyp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText37.Wrap( -1 )

		gSizer4.Add( self.m_staticText37, 0, wx.ALL, 5 )

		self.txtPVIType = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIType.Enable( False )

		gSizer4.Add( self.txtPVIType, 0, wx.ALL, 5 )

		self.m_staticText38 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Version Main", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )

		gSizer4.Add( self.m_staticText38, 0, wx.ALL, 5 )

		self.txtPVIVersionMain = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIVersionMain.Enable( False )

		gSizer4.Add( self.txtPVIVersionMain, 0, wx.ALL, 5 )

		self.m_staticText39 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Version PIC", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )

		gSizer4.Add( self.m_staticText39, 0, wx.ALL, 5 )

		self.txtPVIVersionPic = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIVersionPic.Enable( False )

		gSizer4.Add( self.txtPVIVersionPic, 0, wx.ALL, 5 )

		self.m_staticText40 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Anzahl Temperatursensoren", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )

		gSizer4.Add( self.m_staticText40, 0, wx.ALL, 5 )

		self.txtPVITempCount = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVITempCount.Enable( False )

		gSizer4.Add( self.txtPVITempCount, 0, wx.ALL, 5 )

		self.m_staticText41 = wx.StaticText( self.pPVI, wx.ID_ANY, u"OnGrid", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )

		gSizer4.Add( self.m_staticText41, 0, wx.ALL, 5 )

		self.chPVIOnGrid = wx.CheckBox( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chPVIOnGrid.Enable( False )

		gSizer4.Add( self.chPVIOnGrid, 0, wx.ALL, 5 )

		self.m_staticText43 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )

		gSizer4.Add( self.m_staticText43, 0, wx.ALL, 5 )

		self.txtPVIStatus = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIStatus.Enable( False )

		gSizer4.Add( self.txtPVIStatus, 0, wx.ALL, 5 )

		self.label123535 = wx.StaticText( self.pPVI, wx.ID_ANY, u"letzter Fehler", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label123535.Wrap( -1 )

		gSizer4.Add( self.label123535, 0, wx.ALL, 5 )

		self.txtPVILastError = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVILastError.Enable( False )

		gSizer4.Add( self.txtPVILastError, 0, wx.ALL, 5 )

		self.m_staticText45 = wx.StaticText( self.pPVI, wx.ID_ANY, u"COS PHI aktiv", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )

		gSizer4.Add( self.m_staticText45, 0, wx.ALL, 5 )

		self.chPVICosPhiActive = wx.CheckBox( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chPVICosPhiActive.Enable( False )

		gSizer4.Add( self.chPVICosPhiActive, 0, wx.ALL, 5 )

		self.m_staticText47 = wx.StaticText( self.pPVI, wx.ID_ANY, u"COS PHI Wert", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )

		gSizer4.Add( self.m_staticText47, 0, wx.ALL, 5 )

		self.txtPVICosPhiValue = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVICosPhiValue.Enable( False )

		gSizer4.Add( self.txtPVICosPhiValue, 0, wx.ALL, 5 )

		self.m_staticText48 = wx.StaticText( self.pPVI, wx.ID_ANY, u"COS PHI erregt", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText48.Wrap( -1 )

		gSizer4.Add( self.m_staticText48, 0, wx.ALL, 5 )

		self.txtPVICosPhiExcited = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVICosPhiExcited.Enable( False )

		gSizer4.Add( self.txtPVICosPhiExcited, 0, wx.ALL, 5 )

		self.m_staticText49 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Spannung obere Schwelle ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )

		gSizer4.Add( self.m_staticText49, 0, wx.ALL, 5 )

		self.txtPVIVoltageTrTop = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIVoltageTrTop.Enable( False )

		gSizer4.Add( self.txtPVIVoltageTrTop, 0, wx.ALL, 5 )

		self.m_staticText50 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Spannung untere Schwelle", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText50.Wrap( -1 )

		gSizer4.Add( self.m_staticText50, 0, wx.ALL, 5 )

		self.txtPVIVoltageTrBottom = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIVoltageTrBottom.Enable( False )

		gSizer4.Add( self.txtPVIVoltageTrBottom, 0, wx.ALL, 5 )

		self.m_staticText511 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Spannung Steigung hoch", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511.Wrap( -1 )

		gSizer4.Add( self.m_staticText511, 0, wx.ALL, 5 )

		self.txtPVIVoltageSlUp = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIVoltageSlUp.Enable( False )

		gSizer4.Add( self.txtPVIVoltageSlUp, 0, wx.ALL, 5 )

		self.m_staticText52 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Spannung Steigung runter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )

		gSizer4.Add( self.m_staticText52, 0, wx.ALL, 5 )

		self.txtPVIVoltageSlDown = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIVoltageSlDown.Enable( False )

		gSizer4.Add( self.txtPVIVoltageSlDown, 0, wx.ALL, 5 )

		self.m_staticText53 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Powermodus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText53.Wrap( -1 )

		gSizer4.Add( self.m_staticText53, 0, wx.ALL, 5 )

		self.txtPVIPowerMode = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIPowerMode.Enable( False )

		gSizer4.Add( self.txtPVIPowerMode, 0, wx.ALL, 5 )

		self.m_staticText54 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Systemmodus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )

		gSizer4.Add( self.m_staticText54, 0, wx.ALL, 5 )

		self.txtPVISystemMode = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVISystemMode.Enable( False )

		gSizer4.Add( self.txtPVISystemMode, 0, wx.ALL, 5 )

		self.m_staticText56 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Temperatur Maximum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )

		gSizer4.Add( self.m_staticText56, 0, wx.ALL, 5 )

		self.txtPVIMaxTemperature = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIMaxTemperature.Enable( False )

		gSizer4.Add( self.txtPVIMaxTemperature, 0, wx.ALL, 5 )

		self.m_staticText57 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Temperatur Minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText57.Wrap( -1 )

		gSizer4.Add( self.m_staticText57, 0, wx.ALL, 5 )

		self.txtPVIMinTemperature = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIMinTemperature.Enable( False )

		gSizer4.Add( self.txtPVIMinTemperature, 0, wx.ALL, 5 )

		self.m_staticText58 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Maximale Scheinleistung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText58.Wrap( -1 )

		gSizer4.Add( self.m_staticText58, 0, wx.ALL, 5 )

		self.txtPVIMaxApparentpower = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIMaxApparentpower.Enable( False )

		gSizer4.Add( self.txtPVIMaxApparentpower, 0, wx.ALL, 5 )

		self.m_staticText59 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Maximale Frequenz", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText59.Wrap( -1 )

		gSizer4.Add( self.m_staticText59, 0, wx.ALL, 5 )

		self.txtPVIMaxFreq = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIMaxFreq.Enable( False )

		gSizer4.Add( self.txtPVIMaxFreq, 0, wx.ALL, 5 )

		self.m_staticText60 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Minimale Frequenz", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText60.Wrap( -1 )

		gSizer4.Add( self.m_staticText60, 0, wx.ALL, 5 )

		self.txtPVIFreqMin = wx.TextCtrl( self.pPVI, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPVIFreqMin.Enable( False )

		gSizer4.Add( self.txtPVIFreqMin, 0, wx.ALL, 5 )


		fgSizer25.Add( gSizer4, 1, wx.EXPAND, 5 )


		gSizer51.Add( fgSizer25, 1, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText62 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Messdaten Phasenbezogen (L1-L3)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )

		bSizer6.Add( self.m_staticText62, 0, wx.ALL, 5 )

		self.gPVIAC = wx.grid.Grid( self.pPVI, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.gPVIAC.CreateGrid( 7, 4 )
		self.gPVIAC.EnableEditing( True )
		self.gPVIAC.EnableGridLines( True )
		self.gPVIAC.EnableDragGridSize( False )
		self.gPVIAC.SetMargins( 0, 5 )

		# Columns
		self.gPVIAC.EnableDragColMove( False )
		self.gPVIAC.EnableDragColSize( True )
		self.gPVIAC.SetColLabelValue( 0, u"L1" )
		self.gPVIAC.SetColLabelValue( 1, u"L2" )
		self.gPVIAC.SetColLabelValue( 2, u"L3" )
		self.gPVIAC.SetColLabelValue( 3, u"Gesamt" )
		self.gPVIAC.SetColLabelSize( 30 )
		self.gPVIAC.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gPVIAC.EnableDragRowSize( True )
		self.gPVIAC.SetRowLabelValue( 0, u"Leistung" )
		self.gPVIAC.SetRowLabelValue( 1, u"Spannung" )
		self.gPVIAC.SetRowLabelValue( 2, u"Stromstärke" )
		self.gPVIAC.SetRowLabelValue( 3, u"Scheinleistung" )
		self.gPVIAC.SetRowLabelValue( 4, u"Blindleistung" )
		self.gPVIAC.SetRowLabelValue( 5, u"Energie (Einspeisung)" )
		self.gPVIAC.SetRowLabelValue( 6, u"Energie (Bezug)" )
		self.gPVIAC.SetRowLabelValue( 7, wx.EmptyString )
		self.gPVIAC.SetRowLabelSize( 100 )
		self.gPVIAC.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gPVIAC.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer6.Add( self.gPVIAC, 0, wx.ALL, 5 )

		self.m_staticline10 = wx.StaticLine( self.pPVI, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText611 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Messdaten Stringss", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611.Wrap( -1 )

		bSizer6.Add( self.m_staticText611, 0, wx.ALL, 5 )

		self.gPVIDC = wx.grid.Grid( self.pPVI, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.gPVIDC.CreateGrid( 4, 0 )
		self.gPVIDC.EnableEditing( True )
		self.gPVIDC.EnableGridLines( True )
		self.gPVIDC.EnableDragGridSize( False )
		self.gPVIDC.SetMargins( 0, 0 )

		# Columns
		self.gPVIDC.EnableDragColMove( False )
		self.gPVIDC.EnableDragColSize( True )
		self.gPVIDC.SetColLabelSize( 30 )
		self.gPVIDC.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gPVIDC.EnableDragRowSize( True )
		self.gPVIDC.SetRowLabelValue( 0, u"Leistung" )
		self.gPVIDC.SetRowLabelValue( 1, u"Spannung" )
		self.gPVIDC.SetRowLabelValue( 2, u"Stromstärke" )
		self.gPVIDC.SetRowLabelValue( 3, u"Energie" )
		self.gPVIDC.SetRowLabelSize( 100 )
		self.gPVIDC.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gPVIDC.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer6.Add( self.gPVIDC, 0, wx.ALL, 5 )

		self.m_staticline9 = wx.StaticLine( self.pPVI, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText63 = wx.StaticText( self.pPVI, wx.ID_ANY, u"Temperaturen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )

		bSizer6.Add( self.m_staticText63, 0, wx.ALL, 5 )

		self.gPVITemps = wx.grid.Grid( self.pPVI, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.gPVITemps.CreateGrid( 8, 1 )
		self.gPVITemps.EnableEditing( True )
		self.gPVITemps.EnableGridLines( True )
		self.gPVITemps.EnableDragGridSize( False )
		self.gPVITemps.SetMargins( 0, 0 )

		# Columns
		self.gPVITemps.EnableDragColMove( False )
		self.gPVITemps.EnableDragColSize( True )
		self.gPVITemps.SetColLabelValue( 0, u"Wert" )
		self.gPVITemps.SetColLabelSize( 30 )
		self.gPVITemps.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gPVITemps.EnableDragRowSize( True )
		self.gPVITemps.SetRowLabelSize( 100 )
		self.gPVITemps.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gPVITemps.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer6.Add( self.gPVITemps, 0, wx.ALL, 5 )

		self.m_staticline81 = wx.StaticLine( self.pPVI, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline81, 0, wx.EXPAND |wx.ALL, 5 )

		self.chPVIDeviceConnected = wx.CheckBox( self.pPVI, wx.ID_ANY, u"Gerät verbunden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chPVIDeviceConnected.Enable( False )

		bSizer6.Add( self.chPVIDeviceConnected, 0, wx.ALL, 5 )

		self.chPVIDeviceWorking = wx.CheckBox( self.pPVI, wx.ID_ANY, u"Gerät arbeitet", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chPVIDeviceWorking.Enable( False )

		bSizer6.Add( self.chPVIDeviceWorking, 0, wx.ALL, 5 )

		self.chPVIDeviceInService = wx.CheckBox( self.pPVI, wx.ID_ANY, u"Gerät in Wartung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chPVIDeviceInService.Enable( False )

		bSizer6.Add( self.chPVIDeviceInService, 0, wx.ALL, 5 )


		gSizer51.Add( bSizer6, 1, wx.EXPAND, 5 )


		bSizer51.Add( gSizer51, 1, wx.EXPAND, 5 )


		self.pPVI.SetSizer( bSizer51 )
		self.pPVI.Layout()
		bSizer51.Fit( self.pPVI )
		self.pMainregister.AddPage( self.pPVI, u"Wechselrichter", False )
		self.pPM = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"PM" )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )

		self.gPM = wx.grid.Grid( self.pPM, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.gPM.CreateGrid( 31, 1 )
		self.gPM.EnableEditing( True )
		self.gPM.EnableGridLines( True )
		self.gPM.EnableDragGridSize( False )
		self.gPM.SetMargins( 0, 0 )

		# Columns
		self.gPM.EnableDragColMove( False )
		self.gPM.EnableDragColSize( True )
		self.gPM.SetColLabelValue( 0, u"LM #0" )
		self.gPM.SetColLabelSize( 30 )
		self.gPM.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gPM.EnableDragRowSize( True )
		self.gPM.SetRowLabelValue( 0, u"Leistung L1" )
		self.gPM.SetRowLabelValue( 1, u"Leistung L2" )
		self.gPM.SetRowLabelValue( 2, u"Leistung L3" )
		self.gPM.SetRowLabelValue( 3, u"Leistung gesamt" )
		self.gPM.SetRowLabelValue( 4, u"Spannung L1" )
		self.gPM.SetRowLabelValue( 5, u"Spannung L2" )
		self.gPM.SetRowLabelValue( 6, u"Spannung L3" )
		self.gPM.SetRowLabelValue( 7, u"Energie L1" )
		self.gPM.SetRowLabelValue( 8, u"Energie L2" )
		self.gPM.SetRowLabelValue( 9, u"Energie L3" )
		self.gPM.SetRowLabelValue( 10, u"Energie gesamt" )
		self.gPM.SetRowLabelValue( 11, u"Firmware Version" )
		self.gPM.SetRowLabelValue( 12, u"aktive Phasen" )
		self.gPM.SetRowLabelValue( 13, u"Modus" )
		self.gPM.SetRowLabelValue( 14, u"Fehlercode" )
		self.gPM.SetRowLabelValue( 15, u"Type" )
		self.gPM.SetRowLabelValue( 16, u"Device ID" )
		self.gPM.SetRowLabelValue( 17, u"Is CAN silence" )
		self.gPM.SetRowLabelValue( 18, u"CS Start Time" )
		self.gPM.SetRowLabelValue( 19, u"CS Last Time" )
		self.gPM.SetRowLabelValue( 20, u"CS Success Frames All" )
		self.gPM.SetRowLabelValue( 21, u"CS Success Frames 100" )
		self.gPM.SetRowLabelValue( 22, u"CS Expected Frames All" )
		self.gPM.SetRowLabelValue( 23, u"CS Expected Frames 100" )
		self.gPM.SetRowLabelValue( 24, u"CS Error Frames All" )
		self.gPM.SetRowLabelValue( 25, u"CS Error Frames 100" )
		self.gPM.SetRowLabelValue( 26, u"CS Unknown Frames" )
		self.gPM.SetRowLabelValue( 27, u"CS Error Frame" )
		self.gPM.SetRowLabelValue( 28, u"Gerät verbunden" )
		self.gPM.SetRowLabelValue( 29, u"Gerät arbeitet" )
		self.gPM.SetRowLabelValue( 30, u"Gerät in Wartung" )
		self.gPM.SetRowLabelSize( 150 )
		self.gPM.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gPM.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer17.Add( self.gPM, 0, wx.ALL, 5 )


		self.pPM.SetSizer( bSizer17 )
		self.pPM.Layout()
		bSizer17.Fit( self.pPM )
		self.pMainregister.AddPage( self.pPM, u"Leistungsmesser", False )
		self.pWB = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"WB" )
		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		cbWallboxChoices = []
		self.cbWallbox = wx.ComboBox( self.pWB, wx.ID_ANY, u"WB", wx.DefaultPosition, wx.DefaultSize, cbWallboxChoices, 0 )
		bSizer16.Add( self.cbWallbox, 0, wx.ALL, 5 )

		self.m_staticline151 = wx.StaticLine( self.pWB, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer16.Add( self.m_staticline151, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline17 = wx.StaticLine( self.pWB, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer16.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer31 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer31.SetFlexibleDirection( wx.BOTH )
		fgSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer30 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer30.SetFlexibleDirection( wx.BOTH )
		fgSizer30.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText178 = wx.StaticText( self.pWB, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText178.Wrap( -1 )

		fgSizer30.Add( self.m_staticText178, 0, wx.ALL, 5 )

		self.txtWBStatus = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBStatus.Enable( False )

		fgSizer30.Add( self.txtWBStatus, 0, wx.ALL, 5 )

		self.m_staticText179 = wx.StaticText( self.pWB, wx.ID_ANY, u"Energie gesamt", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText179.Wrap( -1 )

		fgSizer30.Add( self.m_staticText179, 0, wx.ALL, 5 )

		self.txtWBEnergyAll = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBEnergyAll.Enable( False )

		fgSizer30.Add( self.txtWBEnergyAll, 0, wx.ALL, 5 )

		self.m_staticText180 = wx.StaticText( self.pWB, wx.ID_ANY, u"Energie Solar", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText180.Wrap( -1 )

		fgSizer30.Add( self.m_staticText180, 0, wx.ALL, 5 )

		self.txtWBEnergySolar = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBEnergySolar.Enable( False )

		fgSizer30.Add( self.txtWBEnergySolar, 0, wx.ALL, 5 )

		self.m_staticText181 = wx.StaticText( self.pWB, wx.ID_ANY, u"SOC", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText181.Wrap( -1 )

		fgSizer30.Add( self.m_staticText181, 0, wx.ALL, 5 )

		self.txtWBSOC = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBSOC.Enable( False )

		fgSizer30.Add( self.txtWBSOC, 0, wx.ALL, 5 )

		self.m_staticText182 = wx.StaticText( self.pWB, wx.ID_ANY, u"Errorcode", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText182.Wrap( -1 )

		fgSizer30.Add( self.m_staticText182, 0, wx.ALL, 5 )

		self.txtWBErrorCode = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBErrorCode.Enable( False )

		fgSizer30.Add( self.txtWBErrorCode, 0, wx.ALL, 5 )

		self.m_staticText183 = wx.StaticText( self.pWB, wx.ID_ANY, u"Gerätename", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText183.Wrap( -1 )

		fgSizer30.Add( self.m_staticText183, 0, wx.ALL, 5 )

		self.txtWBDeviceName = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBDeviceName.Enable( False )

		fgSizer30.Add( self.txtWBDeviceName, 0, wx.ALL, 5 )

		self.m_staticText184 = wx.StaticText( self.pWB, wx.ID_ANY, u"Modus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText184.Wrap( -1 )

		fgSizer30.Add( self.m_staticText184, 0, wx.ALL, 5 )

		fgSizer321 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer321.SetFlexibleDirection( wx.BOTH )
		fgSizer321.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.txtWBMode = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.txtWBMode.Enable( False )

		fgSizer321.Add( self.txtWBMode, 0, wx.ALL, 5 )

		self.bWBStopLoading = wx.Button( self.pWB, wx.ID_ANY, u"Ladevorgang abbrechen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer321.Add( self.bWBStopLoading, 0, wx.ALL, 5 )


		fgSizer30.Add( fgSizer321, 1, wx.EXPAND, 5 )

		self.m_staticText1871 = wx.StaticText( self.pWB, wx.ID_ANY, u"Ladeleistung aus PV", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1871.Wrap( -1 )

		fgSizer30.Add( self.m_staticText1871, 0, wx.ALL, 5 )

		self.txtWBSun = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBSun.Enable( False )

		fgSizer30.Add( self.txtWBSun, 0, wx.ALL, 5 )

		self.m_staticText188 = wx.StaticText( self.pWB, wx.ID_ANY, u"Ladeleistung aus Netz", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText188.Wrap( -1 )

		fgSizer30.Add( self.m_staticText188, 0, wx.ALL, 5 )

		self.txtWBNet = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBNet.Enable( False )

		fgSizer30.Add( self.txtWBNet, 0, wx.ALL, 5 )

		self.m_staticText189 = wx.StaticText( self.pWB, wx.ID_ANY, u"Ladeleistung Gesamt", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText189.Wrap( -1 )

		fgSizer30.Add( self.m_staticText189, 0, wx.ALL, 5 )

		self.txtWBLadeleistung = wx.TextCtrl( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtWBLadeleistung.Enable( False )

		fgSizer30.Add( self.txtWBLadeleistung, 0, wx.ALL, 5 )


		fgSizer31.Add( fgSizer30, 1, wx.EXPAND, 5 )

		bSizer18 = wx.BoxSizer( wx.VERTICAL )

		self.gWBData = wx.grid.Grid( self.pWB, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.gWBData.CreateGrid( 2, 4 )
		self.gWBData.EnableEditing( True )
		self.gWBData.EnableGridLines( True )
		self.gWBData.EnableDragGridSize( False )
		self.gWBData.SetMargins( 0, 0 )

		# Columns
		self.gWBData.EnableDragColMove( False )
		self.gWBData.EnableDragColSize( True )
		self.gWBData.SetColLabelValue( 0, u"L1" )
		self.gWBData.SetColLabelValue( 1, u"L2" )
		self.gWBData.SetColLabelValue( 2, u"L3" )
		self.gWBData.SetColLabelValue( 3, u"Gesamt" )
		self.gWBData.SetColLabelSize( 30 )
		self.gWBData.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gWBData.EnableDragRowSize( True )
		self.gWBData.SetRowLabelValue( 0, u"Leistung" )
		self.gWBData.SetRowLabelValue( 1, u"Energie" )
		self.gWBData.SetRowLabelSize( 80 )
		self.gWBData.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gWBData.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer18.Add( self.gWBData, 0, wx.ALL, 5 )

		fgSizer32 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer32.SetFlexibleDirection( wx.BOTH )
		fgSizer32.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText185 = wx.StaticText( self.pWB, wx.ID_ANY, u"Gerät verbunden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText185.Wrap( -1 )

		fgSizer32.Add( self.m_staticText185, 0, wx.ALL, 5 )

		self.chWBDeviceConnected = wx.CheckBox( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chWBDeviceConnected.Enable( False )

		fgSizer32.Add( self.chWBDeviceConnected, 0, wx.ALL, 5 )

		self.m_staticText186 = wx.StaticText( self.pWB, wx.ID_ANY, u"Gerät arbeitet", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText186.Wrap( -1 )

		fgSizer32.Add( self.m_staticText186, 0, wx.ALL, 5 )

		self.chWBDeviceWorking = wx.CheckBox( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chWBDeviceWorking.Enable( False )

		fgSizer32.Add( self.chWBDeviceWorking, 0, wx.ALL, 5 )

		self.m_staticText187 = wx.StaticText( self.pWB, wx.ID_ANY, u"Gerät in Service", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText187.Wrap( -1 )

		fgSizer32.Add( self.m_staticText187, 0, wx.ALL, 5 )

		self.chWBDeviceInService = wx.CheckBox( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chWBDeviceInService.Enable( False )

		fgSizer32.Add( self.chWBDeviceInService, 0, wx.ALL, 5 )


		bSizer18.Add( fgSizer32, 1, wx.EXPAND, 5 )


		fgSizer31.Add( bSizer18, 1, wx.EXPAND, 5 )


		bSizer16.Add( fgSizer31, 1, wx.EXPAND, 5 )

		fgSizer28 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer28.SetFlexibleDirection( wx.BOTH )
		fgSizer28.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1733 = wx.StaticText( self.pWB, wx.ID_ANY, u"Sonnenmodus", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1733.Wrap( -1 )

		fgSizer28.Add( self.m_staticText1733, 0, wx.ALL, 5 )

		self.chWBSunmode = wx.CheckBox( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer28.Add( self.chWBSunmode, 0, wx.ALL, 5 )

		self.m_staticText174 = wx.StaticText( self.pWB, wx.ID_ANY, u"Ladestrom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText174.Wrap( -1 )

		fgSizer28.Add( self.m_staticText174, 0, wx.ALL, 5 )

		fgSizer29 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer29.SetFlexibleDirection( wx.BOTH )
		fgSizer29.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.sWBLadestrom = wx.Slider( self.pWB, wx.ID_ANY, 6, 6, 32, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		fgSizer29.Add( self.sWBLadestrom, 0, wx.ALL, 5 )

		self.stWBLadestrom = wx.StaticText( self.pWB, wx.ID_ANY, u"6A", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stWBLadestrom.Wrap( -1 )

		fgSizer29.Add( self.stWBLadestrom, 0, wx.ALL, 5 )


		fgSizer28.Add( fgSizer29, 1, wx.EXPAND, 5 )

		self.m_staticText176 = wx.StaticText( self.pWB, wx.ID_ANY, u"1ph Laden", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText176.Wrap( -1 )

		fgSizer28.Add( self.m_staticText176, 0, wx.ALL, 5 )

		self.chWB1PH = wx.CheckBox( self.pWB, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer28.Add( self.chWB1PH, 0, wx.ALL, 5 )

		self.bWBSave = wx.Button( self.pWB, wx.ID_ANY, u"Änderungen übertragen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer28.Add( self.bWBSave, 0, wx.ALL, 5 )


		bSizer16.Add( fgSizer28, 1, wx.EXPAND, 5 )


		self.pWB.SetSizer( bSizer16 )
		self.pWB.Layout()
		bSizer16.Fit( self.pWB )
		self.pMainregister.AddPage( self.pWB, u"Wallbox", False )
		self.pEinstellungen = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"CONFIG" )
		fgSizer37 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer37.SetFlexibleDirection( wx.BOTH )
		fgSizer37.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.Basiseinstellungen = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Basiseinstellungen", wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_MIDDLE )
		self.Basiseinstellungen.Wrap( -1 )

		fgSizer1.Add( self.Basiseinstellungen, 0, wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticline20 = wx.StaticLine( self.pEinstellungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline20, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline21 = wx.StaticLine( self.pEinstellungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Web-Benutzername", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		fgSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.txtUsername = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		self.txtUsername.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )

		fgSizer1.Add( self.txtUsername, 0, wx.ALL, 5 )

		self.m_staticText6 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Web-Passwort", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.txtPassword = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PASSWORD )
		self.txtPassword.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )

		fgSizer1.Add( self.txtPassword, 0, wx.ALL, 5 )

		self.m_staticText8 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"RSCP-Passwort", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		fgSizer1.Add( self.m_staticText8, 0, wx.ALL, 5 )

		fgSizer22 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer22.SetFlexibleDirection( wx.BOTH )
		fgSizer22.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.txtRSCPPassword = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PASSWORD )
		self.txtRSCPPassword.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		fgSizer22.Add( self.txtRSCPPassword, 0, wx.ALL, 5 )

		self.bConfigSetRSCPPassword = wx.Button( self.pEinstellungen, wx.ID_ANY, u"setzen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer22.Add( self.bConfigSetRSCPPassword, 0, wx.ALL, 5 )


		fgSizer1.Add( fgSizer22, 1, wx.EXPAND, 5 )

		self.m_staticText171 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Verbindungsart", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText171.Wrap( -1 )

		fgSizer1.Add( self.m_staticText171, 0, wx.ALL, 5 )

		fgSizer271 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer271.SetFlexibleDirection( wx.BOTH )
		fgSizer271.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		cbConfigVerbindungsartChoices = [ u"auto", u"direkt", u"web" ]
		self.cbConfigVerbindungsart = wx.ComboBox( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbConfigVerbindungsartChoices, 0 )
		fgSizer271.Add( self.cbConfigVerbindungsart, 0, wx.ALL, 5 )

		self.bTest = wx.Button( self.pEinstellungen, wx.ID_ANY, u"Verbindungstest", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer271.Add( self.bTest, 0, wx.ALL, 5 )


		fgSizer1.Add( fgSizer271, 1, wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"IP-Adresse", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		fgSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )

		fgSizer211 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer211.SetFlexibleDirection( wx.BOTH )
		fgSizer211.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.txtIP = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer211.Add( self.txtIP, 0, wx.ALL, 5 )

		self.bConfigGetIPAddress = wx.Button( self.pEinstellungen, wx.ID_ANY, u"ermitteln", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer211.Add( self.bConfigGetIPAddress, 0, wx.ALL, 5 )


		fgSizer1.Add( fgSizer211, 1, wx.EXPAND, 5 )

		self.m_staticText169 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Seriennummer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText169.Wrap( -1 )

		fgSizer1.Add( self.m_staticText169, 0, wx.ALL, 5 )

		fgSizer20 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer20.SetFlexibleDirection( wx.BOTH )
		fgSizer20.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.txtConfigSeriennummer = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer20.Add( self.txtConfigSeriennummer, 0, wx.ALL, 5 )

		self.bConfigGetSerialNo = wx.Button( self.pEinstellungen, wx.ID_ANY, u"ermitteln", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer20.Add( self.bConfigGetSerialNo, 0, wx.ALL, 5 )


		fgSizer1.Add( fgSizer20, 1, wx.EXPAND, 5 )

		self.m_staticText1732 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"aktive Verbindung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1732.Wrap( -1 )

		fgSizer1.Add( self.m_staticText1732, 0, wx.ALL, 5 )

		self.txtConfigAktiveVerbindung = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtConfigAktiveVerbindung.Enable( False )

		fgSizer1.Add( self.txtConfigAktiveVerbindung, 0, wx.ALL, 5 )

		self.m_staticText17331 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Autoupdate (s)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17331.Wrap( -1 )

		fgSizer1.Add( self.m_staticText17331, 0, wx.ALL, 5 )

		self.scAutoUpdate = wx.SpinCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 3600, 0 )
		fgSizer1.Add( self.scAutoUpdate, 0, wx.ALL, 5 )

		self.bSave = wx.Button( self.pEinstellungen, wx.ID_ANY, u"Einstellungen speichern", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.bSave, 0, wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		fgSizer1.Add( ( 0, 50), 1, wx.EXPAND, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.pEinstellungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline3 = wx.StaticLine( self.pEinstellungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText86 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Upload-URL", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText86.Wrap( -1 )

		fgSizer1.Add( self.m_staticText86, 0, wx.ALL, 5 )

		self.txtDBServer = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, u"https://pv.pincrushers.de/rscpgui", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtDBServer.SetMinSize( wx.Size( 250,-1 ) )

		fgSizer1.Add( self.txtDBServer, 0, wx.ALL, 5 )


		fgSizer37.Add( fgSizer1, 1, wx.EXPAND, 5 )

		fgSizer40 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer40.SetFlexibleDirection( wx.BOTH )
		fgSizer40.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText202 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Exporteinstellungen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText202.Wrap( -1 )

		fgSizer40.Add( self.m_staticText202, 0, wx.ALL, 5 )


		fgSizer40.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticline171 = wx.StaticLine( self.pEinstellungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer40.Add( self.m_staticline171, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline19 = wx.StaticLine( self.pEinstellungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer40.Add( self.m_staticline19, 0, wx.EXPAND |wx.ALL, 5 )

		self.chUploadCSV = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"in CSV exportieren", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer40.Add( self.chUploadCSV, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.fpUploadCSV = wx.FilePickerCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, u"Datei auswählen", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
		fgSizer40.Add( self.fpUploadCSV, 0, wx.ALL, 5 )

		self.chUploadJSON = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"in JSON Datei exportieren", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer40.Add( self.chUploadJSON, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.fpUploadJSON = wx.FilePickerCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, u"JSON-File auswählen", u"*.json", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
		fgSizer40.Add( self.fpUploadJSON, 0, wx.ALL, 5 )

		self.chUploadMQTT = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"MQTT", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer40.Add( self.chUploadMQTT, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		fgSizer42 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer42.SetFlexibleDirection( wx.BOTH )
		fgSizer42.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText208 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Broker", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText208.Wrap( -1 )

		fgSizer42.Add( self.m_staticText208, 0, wx.ALL, 5 )

		self.txtUploadMQTTBroker = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer42.Add( self.txtUploadMQTTBroker, 0, wx.ALL, 5 )

		self.m_staticText209 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText209.Wrap( -1 )

		fgSizer42.Add( self.m_staticText209, 0, wx.ALL, 5 )

		self.txtUploadMQTTPort = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer42.Add( self.txtUploadMQTTPort, 0, wx.ALL, 5 )

		self.m_staticText2091 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Benutzername", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2091.Wrap( -1 )

		fgSizer42.Add( self.m_staticText2091, 0, wx.ALL, 5 )

		self.txtUploadMQTTUsername = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer42.Add( self.txtUploadMQTTUsername, 0, wx.ALL, 5 )

		self.m_staticText2101 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Passwort", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2101.Wrap( -1 )

		fgSizer42.Add( self.m_staticText2101, 0, wx.ALL, 5 )

		self.txtUploadMQTTPassword = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		fgSizer42.Add( self.txtUploadMQTTPassword, 0, wx.ALL, 5 )

		self.m_staticText214 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"SSL-Zertifikat", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText214.Wrap( -1 )

		fgSizer42.Add( self.m_staticText214, 0, wx.ALL, 5 )

		self.fpUploadMQTTZertifikat = wx.FilePickerCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		fgSizer42.Add( self.fpUploadMQTTZertifikat, 0, wx.ALL, 5 )

		self.cbUploadMQTTInsecure = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"TLS-Insecure", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer42.Add( self.cbUploadMQTTInsecure, 0, wx.ALL, 5 )


		fgSizer42.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText210 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"QOS", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText210.Wrap( -1 )

		fgSizer42.Add( self.m_staticText210, 0, wx.ALL, 5 )

		self.scUploadMQTTQos = wx.SpinCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 10, 0 )
		fgSizer42.Add( self.scUploadMQTTQos, 0, wx.ALL, 5 )

		self.chUploadMQTTRetain = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"Retain-Flag", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer42.Add( self.chUploadMQTTRetain, 0, wx.ALL, 5 )


		fgSizer42.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.chUploadMQTTSub = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"Werteänderung zulassen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer42.Add( self.chUploadMQTTSub, 0, wx.ALL, 5 )


		fgSizer40.Add( fgSizer42, 1, wx.EXPAND, 5 )

		self.chUploadHTTP = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"an URL senden (POST)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer40.Add( self.chUploadHTTP, 0, wx.ALL, 5 )

		self.txtUploadHTTPURL = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, u"https://pv.pincrushers.de/rscpgui", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer40.Add( self.txtUploadHTTPURL, 0, wx.ALL, 5 )

		self.chUploadInfluxdb = wx.CheckBox( self.pEinstellungen, wx.ID_ANY, u"Influx DB (v1)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer40.Add( self.chUploadInfluxdb, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		fgSizer411 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer411.SetFlexibleDirection( wx.BOTH )
		fgSizer411.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText213 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Host", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText213.Wrap( -1 )

		fgSizer411.Add( self.m_staticText213, 0, wx.ALL, 5 )

		self.txtUploadInfluxHost = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer411.Add( self.txtUploadInfluxHost, 0, wx.ALL, 5 )

		self.m_staticText215 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText215.Wrap( -1 )

		fgSizer411.Add( self.m_staticText215, 0, wx.ALL, 5 )

		self.txtUploadInfluxPort = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer411.Add( self.txtUploadInfluxPort, 0, wx.ALL, 5 )

		self.m_staticText217 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Datenbank", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText217.Wrap( -1 )

		fgSizer411.Add( self.m_staticText217, 0, wx.ALL, 5 )

		self.txtUploadInfluxDatenbank = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer411.Add( self.txtUploadInfluxDatenbank, 0, wx.ALL, 5 )

		self.m_staticText218 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText218.Wrap( -1 )

		fgSizer411.Add( self.m_staticText218, 0, wx.ALL, 5 )

		self.txtUploadInfluxName = wx.TextCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer411.Add( self.txtUploadInfluxName, 0, wx.ALL, 5 )

		self.m_staticText216 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Timeout", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText216.Wrap( -1 )

		fgSizer411.Add( self.m_staticText216, 0, wx.ALL, 5 )

		self.scUploadInfluxTimeout = wx.SpinCtrl( self.pEinstellungen, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 300, 1 )
		fgSizer411.Add( self.scUploadInfluxTimeout, 0, wx.ALL, 5 )


		fgSizer40.Add( fgSizer411, 1, wx.EXPAND, 5 )

		self.m_staticText206 = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"Intervall (s)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText206.Wrap( -1 )

		fgSizer40.Add( self.m_staticText206, 0, wx.ALL, 5 )

		self.scUploadIntervall = wx.SpinCtrl( self.pEinstellungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 1, 3600, 30 )
		fgSizer40.Add( self.scUploadIntervall, 0, wx.ALL, 5 )

		self.bUploadSetData = wx.Button( self.pEinstellungen, wx.ID_ANY, u"Daten auswählen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer40.Add( self.bUploadSetData, 0, wx.ALL, 5 )

		self.stUploadCount = wx.StaticText( self.pEinstellungen, wx.ID_ANY, u"keine Felder angewählt", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stUploadCount.Wrap( -1 )

		fgSizer40.Add( self.stUploadCount, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.bUploadStart = wx.Button( self.pEinstellungen, wx.ID_ANY, u"Export starten", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer40.Add( self.bUploadStart, 0, wx.ALL, 5 )


		fgSizer37.Add( fgSizer40, 1, wx.EXPAND, 5 )

		self.bUpload = wx.Button( self.pEinstellungen, wx.ID_ANY, u"anonymisierte Debugdaten an Entwickler senden", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer37.Add( self.bUpload, 0, wx.ALL, 5 )


		self.pEinstellungen.SetSizer( fgSizer37 )
		self.pEinstellungen.Layout()
		fgSizer37.Fit( self.pEinstellungen )
		self.pMainregister.AddPage( self.pEinstellungen, u"Einstellungen", True )
		self.pPortal = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		wSizer1 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		bSizer20 = wx.BoxSizer( wx.VERTICAL )

		bSizer20.SetMinSize( wx.Size( 700,200 ) )
		fgSizer39 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer39.SetFlexibleDirection( wx.BOTH )
		fgSizer39.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer41 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer41.SetFlexibleDirection( wx.BOTH )
		fgSizer41.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.bPortalUpload = wx.Button( self.pPortal, wx.ID_ANY, u"Eigene Daten hochladen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer41.Add( self.bPortalUpload, 0, wx.ALL, 5 )

		self.bPortalDelete = wx.Button( self.pPortal, wx.ID_ANY, u"Eigene Daten löschen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer41.Add( self.bPortalDelete, 0, wx.ALL, 5 )


		fgSizer39.Add( fgSizer41, 1, wx.EXPAND, 5 )


		bSizer20.Add( fgSizer39, 1, wx.EXPAND, 5 )

		self.m_staticText211 = wx.StaticText( self.pPortal, wx.ID_ANY, u"Mit der Portalfunktion können die Batteriesysteme über ihren SOH verglichen werden. Beim Hochladen werden nur Basisinformationen zu den Batteriemodulen übertragen. Es werden keine Zugangsdaten oder persönliche Daten des Systems übermittelt. Seriennummern etc. werden ebenfalls nicht übermittelt. Alle zur Verfügung gestellten Daten können jederzeit restlos gelöscht werden.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( 600 )

		bSizer20.Add( self.m_staticText211, 0, wx.ALL, 5 )

		self.m_hyperlink1 = wx.adv.HyperlinkCtrl( self.pPortal, wx.ID_ANY, u"https://pv.pincrushers.de/rscpgui/portal", u"https://pv.pincrushers.de/rscpgui/portal", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		bSizer20.Add( self.m_hyperlink1, 0, wx.ALL, 5 )

		self.gPortalList = wx.grid.Grid( self.pPortal, wx.ID_ANY, wx.DefaultPosition, wx.Size( 800,400 ), wx.HSCROLL )

		# Grid
		self.gPortalList.CreateGrid( 5, 5 )
		self.gPortalList.EnableEditing( True )
		self.gPortalList.EnableGridLines( True )
		self.gPortalList.EnableDragGridSize( True )
		self.gPortalList.SetMargins( 0, 0 )

		# Columns
		self.gPortalList.EnableDragColMove( True )
		self.gPortalList.EnableDragColSize( True )
		self.gPortalList.SetColLabelSize( 30 )
		self.gPortalList.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gPortalList.EnableDragRowSize( True )
		self.gPortalList.SetRowLabelSize( 40 )
		self.gPortalList.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gPortalList.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer20.Add( self.gPortalList, 0, wx.ALL, 5 )


		wSizer1.Add( bSizer20, 1, wx.EXPAND, 5 )


		self.pPortal.SetSizer( wSizer1 )
		self.pPortal.Layout()
		wSizer1.Fit( self.pPortal )
		self.pMainregister.AddPage( self.pPortal, u"Portal", False )
		self.pBenachrichtigungen = wx.Panel( self.pMainregister, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer46 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer46.SetFlexibleDirection( wx.BOTH )
		fgSizer46.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer421 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer421.SetFlexibleDirection( wx.BOTH )
		fgSizer421.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText2171 = wx.StaticText( self.pBenachrichtigungen, wx.ID_ANY, u"Ziele", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2171.Wrap( -1 )

		fgSizer421.Add( self.m_staticText2171, 0, wx.ALL, 5 )


		fgSizer421.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticline211 = wx.StaticLine( self.pBenachrichtigungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer421.Add( self.m_staticline211, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline22 = wx.StaticLine( self.pBenachrichtigungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer421.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )

		self.chBenachrichtigungTelegram = wx.CheckBox( self.pBenachrichtigungen, wx.ID_ANY, u"Telegram", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer421.Add( self.chBenachrichtigungTelegram, 0, wx.ALL, 5 )

		fgSizer44 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer44.SetFlexibleDirection( wx.BOTH )
		fgSizer44.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText2181 = wx.StaticText( self.pBenachrichtigungen, wx.ID_ANY, u"Token", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2181.Wrap( -1 )

		fgSizer44.Add( self.m_staticText2181, 0, wx.ALL, 5 )

		self.txtTelegramToken = wx.TextCtrl( self.pBenachrichtigungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer44.Add( self.txtTelegramToken, 0, wx.ALL, 5 )

		self.m_staticText219 = wx.StaticText( self.pBenachrichtigungen, wx.ID_ANY, u"EmpfängerID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText219.Wrap( -1 )

		fgSizer44.Add( self.m_staticText219, 0, wx.ALL, 5 )

		self.txtTelegramEmpfaenger = wx.TextCtrl( self.pBenachrichtigungen, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer44.Add( self.txtTelegramEmpfaenger, 0, wx.ALL, 5 )


		fgSizer421.Add( fgSizer44, 1, wx.EXPAND, 5 )


		fgSizer46.Add( fgSizer421, 1, wx.EXPAND, 5 )


		fgSizer46.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText220 = wx.StaticText( self.pBenachrichtigungen, wx.ID_ANY, u"Benachrichtigungseinstellungen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText220.Wrap( -1 )

		fgSizer46.Add( self.m_staticText220, 0, wx.ALL, 5 )


		fgSizer46.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.gBenachrichtigungen = wx.grid.Grid( self.pBenachrichtigungen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.gBenachrichtigungen.CreateGrid( 5, 6 )
		self.gBenachrichtigungen.EnableEditing( True )
		self.gBenachrichtigungen.EnableGridLines( True )
		self.gBenachrichtigungen.EnableDragGridSize( False )
		self.gBenachrichtigungen.SetMargins( 0, 0 )

		# Columns
		self.gBenachrichtigungen.EnableDragColMove( False )
		self.gBenachrichtigungen.EnableDragColSize( True )
		self.gBenachrichtigungen.SetColLabelValue( 0, u"Pfad" )
		self.gBenachrichtigungen.SetColLabelValue( 1, u"Datentyp" )
		self.gBenachrichtigungen.SetColLabelValue( 2, u"Ausdruck" )
		self.gBenachrichtigungen.SetColLabelValue( 3, u"Dienst" )
		self.gBenachrichtigungen.SetColLabelValue( 4, u"Text" )
		self.gBenachrichtigungen.SetColLabelValue( 5, u"Sendeintervall" )
		self.gBenachrichtigungen.SetColLabelSize( 30 )
		self.gBenachrichtigungen.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.gBenachrichtigungen.EnableDragRowSize( True )
		self.gBenachrichtigungen.SetRowLabelSize( 40 )
		self.gBenachrichtigungen.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.gBenachrichtigungen.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer46.Add( self.gBenachrichtigungen, 0, wx.ALL, 5 )


		fgSizer46.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.bSaveBenachrichtigungen = wx.Button( self.pBenachrichtigungen, wx.ID_ANY, u"Änderungen speichern", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer46.Add( self.bSaveBenachrichtigungen, 0, wx.ALL, 5 )


		self.pBenachrichtigungen.SetSizer( fgSizer46 )
		self.pBenachrichtigungen.Layout()
		fgSizer46.Fit( self.pBenachrichtigungen )
		self.pMainregister.AddPage( self.pBenachrichtigungen, u"Benachrichtigungen", False )

		bSizer1.Add( self.pMainregister, 1, wx.EXPAND |wx.ALL, 5 )

		fgSizer43 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer43.SetFlexibleDirection( wx.BOTH )
		fgSizer43.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		bSizer1.Add( fgSizer43, 1, wx.EXPAND, 5 )

		self.bUpdate = wx.Button( self, wx.ID_ANY, u"aktualisieren", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.bUpdate, 0, wx.ALL, 5 )

		self.gaUpdate = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.gaUpdate.SetValue( 0 )
		bSizer1.Add( self.gaUpdate, 0, wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.mainOnClose )
		self.pMainregister.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.pMainChanged )
		self.btnUpdatecheck.Bind( wx.EVT_BUTTON, self.bUpdateCheckClick )
		self.bSYSReboot.Bind( wx.EVT_BUTTON, self.bSYSRebootOnClick )
		self.bSYSApplicationRestart.Bind( wx.EVT_BUTTON, self.bSYSApplicationRestartOnClick )
		self.bINFOSave.Bind( wx.EVT_BUTTON, self.bINFOSaveOnClick )
		self.bEMSEPTest.Bind( wx.EVT_BUTTON, self.bEMSEPTestOnClick )
		self.bEMSManualChargeStart.Bind( wx.EVT_BUTTON, self.bEMSManualChargeStartOnClick )
		self.sEMSMaxChargePower.Bind( wx.EVT_SCROLL, self.sEMSMaxChargePowerOnScroll )
		self.sEMSMaxDischargePower.Bind( wx.EVT_SCROLL, self.sEMSMaxDischargePowerOnScroll )
		self.sEMSMaxDischargeStartPower.Bind( wx.EVT_SCROLL, self.sEMSMaxDischargeStartPowerOnScroll )
		self.bEMSUploadChanges.Bind( wx.EVT_BUTTON, self.bEMSUploadChangesOnClick )
		self.bMBSSave.Bind( wx.EVT_BUTTON, self.bMBSSaveOnClick )
		self.cbBATIndex.Bind( wx.EVT_COMBOBOX, self.cbBATIndexOnCombobox )
		self.chPVIIndex.Bind( wx.EVT_COMBOBOX, self.chPVIIndexOnCombobox )
		self.bWBStopLoading.Bind( wx.EVT_BUTTON, self.bWBStopLoadingClick )
		self.sWBLadestrom.Bind( wx.EVT_SCROLL, self.sWBLadestromOnScroll )
		self.bWBSave.Bind( wx.EVT_BUTTON, self.bWBSaveOnClick )
		self.bConfigSetRSCPPassword.Bind( wx.EVT_BUTTON, self.bConfigSetRSCPPasswordOnClick )
		self.bConfigGetIPAddress.Bind( wx.EVT_BUTTON, self.bConfigGetIPAddressOnClick )
		self.bConfigGetSerialNo.Bind( wx.EVT_BUTTON, self.bConfigGetSerialNoOnClick )
		self.scAutoUpdate.Bind( wx.EVT_SPINCTRL, self.scAutoUpdateOnChange )
		self.chUploadMQTT.Bind( wx.EVT_CHECKBOX, self.chUploadMQTTOnCheck )
		self.chUploadInfluxdb.Bind( wx.EVT_CHECKBOX, self.chUploadInfluxOnCheck )
		self.bUploadSetData.Bind( wx.EVT_BUTTON, self.bUploadSetDataOnClick )
		self.bUploadStart.Bind( wx.EVT_BUTTON, self.bUploadStartOnClick )
		self.bUpload.Bind( wx.EVT_BUTTON, self.sendToServer )
		self.bPortalUpload.Bind( wx.EVT_BUTTON, self.bPortalUploadOnClick )
		self.bPortalDelete.Bind( wx.EVT_BUTTON, self.bPortalDeleteOnClick )
		self.gPortalList.Bind( wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.gPortalListOnLabelLeftClick )
		self.bSaveBenachrichtigungen.Bind( wx.EVT_BUTTON, self.bSaveBenachrichtigungenOnClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def mainOnClose( self, event ):
		event.Skip()

	def pMainChanged( self, event ):
		event.Skip()

	def bUpdateCheckClick( self, event ):
		event.Skip()

	def bSYSRebootOnClick( self, event ):
		event.Skip()

	def bSYSApplicationRestartOnClick( self, event ):
		event.Skip()

	def bINFOSaveOnClick( self, event ):
		event.Skip()

	def bEMSEPTestOnClick( self, event ):
		event.Skip()

	def bEMSManualChargeStartOnClick( self, event ):
		event.Skip()

	def sEMSMaxChargePowerOnScroll( self, event ):
		event.Skip()

	def sEMSMaxDischargePowerOnScroll( self, event ):
		event.Skip()

	def sEMSMaxDischargeStartPowerOnScroll( self, event ):
		event.Skip()

	def bEMSUploadChangesOnClick( self, event ):
		event.Skip()

	def bMBSSaveOnClick( self, event ):
		event.Skip()

	def cbBATIndexOnCombobox( self, event ):
		event.Skip()

	def chPVIIndexOnCombobox( self, event ):
		event.Skip()

	def bWBStopLoadingClick( self, event ):
		event.Skip()

	def sWBLadestromOnScroll( self, event ):
		event.Skip()

	def bWBSaveOnClick( self, event ):
		event.Skip()

	def bConfigSetRSCPPasswordOnClick( self, event ):
		event.Skip()

	def bConfigGetIPAddressOnClick( self, event ):
		event.Skip()

	def bConfigGetSerialNoOnClick( self, event ):
		event.Skip()

	def scAutoUpdateOnChange( self, event ):
		event.Skip()

	def chUploadMQTTOnCheck( self, event ):
		event.Skip()

	def chUploadInfluxOnCheck( self, event ):
		event.Skip()

	def bUploadSetDataOnClick( self, event ):
		event.Skip()

	def bUploadStartOnClick( self, event ):
		event.Skip()

	def sendToServer( self, event ):
		event.Skip()

	def bPortalUploadOnClick( self, event ):
		event.Skip()

	def bPortalDeleteOnClick( self, event ):
		event.Skip()

	def gPortalListOnLabelLeftClick( self, event ):
		event.Skip()

	def bSaveBenachrichtigungenOnClick( self, event ):
		event.Skip()


###########################################################################
## Class ExportFrame
###########################################################################

class ExportFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Exportdialog", pos = wx.DefaultPosition, size = wx.Size( 522,609 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer181 = wx.BoxSizer( wx.VERTICAL )

		self.tcUpload = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,400 ), wx.TR_DEFAULT_STYLE )
		bSizer181.Add( self.tcUpload, 0, wx.ALL, 5 )

		fgSizer35 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer35.SetFlexibleDirection( wx.BOTH )
		fgSizer35.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer19 = wx.BoxSizer( wx.VERTICAL )


		fgSizer35.Add( bSizer19, 1, wx.EXPAND, 5 )

		fgSizer36 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer36.SetFlexibleDirection( wx.BOTH )
		fgSizer36.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText197 = wx.StaticText( self, wx.ID_ANY, u"Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText197.Wrap( -1 )

		fgSizer36.Add( self.m_staticText197, 0, wx.ALL, 5 )

		self.txtUploadData = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer36.Add( self.txtUploadData, 0, wx.ALL, 5 )

		self.m_staticText198 = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText198.Wrap( -1 )

		fgSizer36.Add( self.m_staticText198, 0, wx.ALL, 5 )

		self.txtUploadName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer36.Add( self.txtUploadName, 0, wx.ALL, 5 )

		self.m_staticText199 = wx.StaticText( self, wx.ID_ANY, u"Pfad", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText199.Wrap( -1 )

		fgSizer36.Add( self.m_staticText199, 0, wx.ALL, 5 )

		self.txtUploadPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer36.Add( self.txtUploadPath, 0, wx.ALL, 5 )

		self.m_staticText200 = wx.StaticText( self, wx.ID_ANY, u"Bezeichner", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText200.Wrap( -1 )

		fgSizer36.Add( self.m_staticText200, 0, wx.ALL, 5 )

		self.txtUploadCustom = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer36.Add( self.txtUploadCustom, 0, wx.ALL, 5 )


		fgSizer35.Add( fgSizer36, 1, wx.EXPAND, 5 )


		bSizer181.Add( fgSizer35, 1, wx.EXPAND, 5 )

		self.bSave = wx.Button( self, wx.ID_ANY, u"speichern", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"UPLOAD" )
		bSizer181.Add( self.bSave, 0, wx.ALL, 5 )


		self.SetSizer( bSizer181 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.tcUpload.Bind( wx.EVT_TREE_SEL_CHANGED, self.tcUploadOnSelChanged )
		self.tcUpload.Bind( wx.EVT_TREE_SEL_CHANGING, self.tcUploadOnSelChanging )
		self.bSave.Bind( wx.EVT_BUTTON, self.bSaveOnClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def tcUploadOnSelChanged( self, event ):
		event.Skip()

	def tcUploadOnSelChanging( self, event ):
		event.Skip()

	def bSaveOnClick( self, event ):
		event.Skip()


###########################################################################
## Class AssistantFrame
###########################################################################

class AssistantFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"RSCPGui - Startassistent", pos = wx.DefaultPosition, size = wx.Size( 501,275 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer27 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel16 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer22 = wx.BoxSizer( wx.VERTICAL )

		self.lblStartassistant = wx.StaticText( self.m_panel16, wx.ID_ANY, u"Dieser Assistent hilft bei der ersten Verbindung mit deinem E3DC. Es werden die\nZugangsdaten für das Webportal benötigt, alles weitere vesucht \nRSCPGui automatisch zu ermitteln.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblStartassistant.Wrap( -1 )

		bSizer22.Add( self.lblStartassistant, 0, wx.ALL, 5 )

		self.m_staticline23 = wx.StaticLine( self.m_panel16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer22.Add( self.m_staticline23, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer45 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer45.SetFlexibleDirection( wx.BOTH )
		fgSizer45.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText223 = wx.StaticText( self.m_panel16, wx.ID_ANY, u"Benutzername:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText223.Wrap( -1 )

		fgSizer45.Add( self.m_staticText223, 0, wx.ALL, 5 )

		self.txtAssistantUsername = wx.TextCtrl( self.m_panel16, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer45.Add( self.txtAssistantUsername, 0, wx.ALL, 5 )

		self.m_staticText224 = wx.StaticText( self.m_panel16, wx.ID_ANY, u"Kennwort:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText224.Wrap( -1 )

		fgSizer45.Add( self.m_staticText224, 0, wx.ALL, 5 )

		self.txtAssistantPassword = wx.TextCtrl( self.m_panel16, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_PASSWORD )
		fgSizer45.Add( self.txtAssistantPassword, 0, wx.ALL, 5 )


		bSizer22.Add( fgSizer45, 1, wx.ALL|wx.EXPAND, 5 )

		fgSizer46 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer46.SetFlexibleDirection( wx.BOTH )
		fgSizer46.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.btnAssistantCancel = wx.Button( self.m_panel16, wx.ID_ANY, u"Assistent überspringen", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer46.Add( self.btnAssistantCancel, 0, wx.ALL, 5 )

		self.btnAssistantOK = wx.Button( self.m_panel16, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer46.Add( self.btnAssistantOK, 0, wx.ALL, 5 )

		self.chkAsistantNoShow = wx.CheckBox( self.m_panel16, wx.ID_ANY, u"Assistent nicht mehr anzeigen!", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer46.Add( self.chkAsistantNoShow, 0, wx.ALL, 5 )


		bSizer22.Add( fgSizer46, 1, wx.EXPAND, 5 )


		self.m_panel16.SetSizer( bSizer22 )
		self.m_panel16.Layout()
		bSizer22.Fit( self.m_panel16 )
		bSizer27.Add( self.m_panel16, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer27 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


