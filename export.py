import logging

logger = logging.getLogger(__name__)

logger.debug('Programmstart')

from gui import ExportFrame
import wx.lib.agw.customtreectrl as CT
import wx

class CustomTreeCtrl(CT.CustomTreeCtrl):
    _checked_items = []

    def DeleteAllItems(self):
        self._checked_items = []
        CT.CustomTreeCtrl.DeleteAllItems(self)

    def GetCheckedItems(self):
        return self._checked_items

    def GetAllItems(self, item = None):
        if not item:
            item = self.GetRootItem()
        items = []
        (child, cookie) = self.GetFirstChild(item)
        while child and child.IsOk():
            items.append(child)
            items += self.GetAllItems(child)

            (child, cookie) = self.GetNextChild(item, cookie)

        return items

    def CheckItem2(self, item, checked=True, torefresh=False):
        dat = self.GetItemData(item)
        if dat is not None and not isinstance(dat, list) and not isinstance(dat, dict):
            font = self.GetItemFont(item)
            if checked:
                self.SetItemFont(item, font.Bold())
                if item not in self._checked_items:
                    self._checked_items.append(item)
            elif not checked:
                font.SetWeight(wx.FONTWEIGHT_NORMAL)
                self.SetItemFont(item, font)
                if item in self._checked_items:
                    self._checked_items.remove(item)

        CT.CustomTreeCtrl.CheckItem2(self, item, checked, torefresh)


class E3DCExport(ExportFrame):
    _UploadStarted = False


    def __init__(self, parent, paths = None, names = None):
        if not paths:
            self._paths = []
        else:
            self._paths = paths

        self._customNames = {}

        self._parent = parent
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 522,609 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer181 = wx.BoxSizer(wx.VERTICAL)

        self.tcUpload = CustomTreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(500, 400), wx.TR_DEFAULT_STYLE)

        bSizer181.Add(self.tcUpload, 0, wx.ALL, 5)

        fgSizer35 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer35.SetFlexibleDirection(wx.BOTH)
        fgSizer35.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        fgSizer35.Add(bSizer19, 1, wx.EXPAND, 5)

        fgSizer36 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer36.SetFlexibleDirection(wx.BOTH)
        fgSizer36.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText197 = wx.StaticText(self, wx.ID_ANY, u"Data", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText197.Wrap(-1)

        fgSizer36.Add(self.m_staticText197, 0, wx.ALL, 5)

        self.txtUploadData = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        fgSizer36.Add(self.txtUploadData, 0, wx.ALL, 5)

        self.m_staticText198 = wx.StaticText(self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText198.Wrap(-1)

        fgSizer36.Add(self.m_staticText198, 0, wx.ALL, 5)

        self.txtUploadName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        fgSizer36.Add(self.txtUploadName, 0, wx.ALL, 5)

        self.m_staticText199 = wx.StaticText(self, wx.ID_ANY, u"Pfad", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText199.Wrap(-1)

        fgSizer36.Add(self.m_staticText199, 0, wx.ALL, 5)

        self.txtUploadPath = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        fgSizer36.Add(self.txtUploadPath, 0, wx.ALL, 5)

        self.m_staticText200 = wx.StaticText(self, wx.ID_ANY, u"Bezeichner", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText200.Wrap(-1)

        fgSizer36.Add(self.m_staticText200, 0, wx.ALL, 5)

        self.txtUploadCustom = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        fgSizer36.Add(self.txtUploadCustom, 0, wx.ALL, 5)

        fgSizer35.Add(fgSizer36, 1, wx.EXPAND, 5)

        bSizer181.Add(fgSizer35, 1, wx.EXPAND, 5)

        self.bSave = wx.Button(self, wx.ID_ANY, u"speichern", wx.DefaultPosition, wx.DefaultSize, 0,
                               wx.DefaultValidator, u"UPLOAD")
        bSizer181.Add(self.bSave, 0, wx.ALL, 5)

        self.SetSizer(bSizer181)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.tcUpload.Bind(wx.EVT_TREE_SEL_CHANGED, self.tcUploadOnSelChanged)
        self.bSave.Bind(wx.EVT_BUTTON, self.bSaveOnClick)

        self.tcUpload.Bind(CT.EVT_TREE_ITEM_CHECKED, self.bUploadLoadItemChecked)
        self.tcUpload.Bind(wx.EVT_TREE_SEL_CHANGING, self.tcUploadOnSelChanging)

        self.txtUploadData.Enable(False)
        self.txtUploadName.Enable(False)
        self.txtUploadPath.Enable(False)

        self.loadData()

        if names:
            self.setCustomNames(names)

    def bSaveOnClick( self, event ):
        self.saveCustomName()
        self.Close()

    def bUploadLoadItemChecked(self, event):
        item = event.GetItem()
        checked = item.GetValue()

        self.tcUpload.CheckItem2(item, checked)
        self.tcUpload.AutoCheckChild(item, checked)

        logger.debug('Checked Items: ' + str(len(self.tcUpload.GetCheckedItems())))

    def loadData(self):
        data = self._parent.sammle_data(anon = False)

        self.tcUpload.DeleteAllItems()

        logger.debug('Lade Datenbaum')
        try:

            def loadInCtrl(data, parent: wx.TreeItemId = None, name: str = None):
                ct_type = 1
                if parent == None:
                    new = self.tcUpload.AddRoot('E3DC',ct_type=ct_type)
                else:
                    new = self.tcUpload.AppendItem(parent,
                                                   text=name,
                                                   data=data,
                                                   ct_type=ct_type)
                    for path in self._paths:
                        if self.getUploadPath(new) == path:
                            self.tcUpload.CheckItem2(new, checked=True)
                if isinstance(data, list):
                    i = 0
                    for d in data:
                        loadInCtrl(d, new, name = str(i))
                        i += 1
                elif isinstance(data, dict):
                    for name in data.keys():
                        loadInCtrl(data[name], new, name = str(name))

            #reduziert = {'EMS_DATA': data['EMS_DATA'], 'BAT_DATA': data['BAT_DATA']}
            loadInCtrl(data)
            logger.debug('Datenbaum erfolgreich geladen')

            self.tcUpload.ExpandAll()
        except:
            logger.exception('Datenbaum konnte nicht geladen werden')

    def tcUploadOnSelChanged( self, event ):
        ret: wx.TreeItemId = self.tcUpload.GetSelection()

        data = self.tcUpload.GetItemData(ret)
        text = self.tcUpload.GetItemText(ret)
        logger.debug('Item ' + text + ' mit Data ' + str(data) + ' markiert')
        if data is not None and not isinstance(data, dict) and not isinstance(data, list):
            self.txtUploadData.SetValue(str(data))
        elif data is None:
            self.txtUploadData.SetValue('none')
        else:
            self.txtUploadData.SetValue(' - ')
        self.txtUploadName.SetValue(text)

        path = self.getUploadPath(ret)
        self.txtUploadPath.SetValue(path)

        if path in self._customNames:
            self.txtUploadCustom.SetValue(self._customNames[path])
        else:
            self.txtUploadCustom.SetValue(path)

    def tcUploadOnSelChanging( self, event ):
        self.saveCustomName()

    def saveCustomName(self):
        ret: wx.TreeItemId = self.tcUpload.GetSelection()
        custom = self.txtUploadCustom.GetValue()
        path = self.getUploadPath(ret)

        if path not in self._customNames or self._customNames[path] != custom:
            self.changeCustomName(ret, custom, path)

            if custom != path:
                data = self.tcUpload.GetItemData(ret)
                if isinstance(data, dict) or isinstance(data, list):
                    res = wx.MessageBox(
                        'Der Bezeichner eines Knoten wurde geändert, soll für alle untergeordneten markierten Einträge der Knotenname angepasst werden?',
                        'Knotenname geändert', wx.YES_NO)
                    if res == wx.YES:
                        logger.debug('Unterknoten von ' + path + ' werden geändert')
                        changed = self.changeCustomNames(ret, custom)
                        logger.debug('Es wurden ' + str(changed) + ' Einträge geändert')

    def changeCustomName(self, item, custom, path=None):
        if not path:
            path = self.getUploadPath(item)

        if path not in self._customNames or self._customNames[path] != custom:
            logger.debug('Individueller Bezeichner für ' + path + ' geändert auf ' + custom)
            self._customNames[path] = custom

        if custom != path:
            self.tcUpload.SetItemTextColour(item, wx.Colour( 0xff, 0x80, 0x80 ))
        else:
            self.tcUpload.SetItemTextColour(item, wx.Colour( 0x00, 0x00, 0x00 ))


    def changeCustomNames(self, item, custom, all=True):
        path = self.getUploadPath(item)
        name = self.tcUpload.GetItemText(item)

        replace_path = path
        changed = 0

        (child, cookie) = self.tcUpload.GetFirstChild(item)
        while child and child.IsOk():
            p = self.getUploadPath(child)
            if all or (p not in self._customNames or self._customNames[p] == p):
                newname = custom + p[len(replace_path):]
                self.changeCustomName(child, newname, p)
                changed += 1
                data = self.tcUpload.GetItemData(child)
                if isinstance(data, dict) or isinstance(data, list):
                    changed += self.changeCustomNames(child, newname)

            (child, cookie) = self.tcUpload.GetNextChild(item, cookie)

        return changed


    def getUploadPath(self, item):
        try:
            path = self.tcUpload.GetItemText(item)
            parent = self.tcUpload.GetItemParent(item)
            if parent:
                path = self.getUploadPath(parent) + '/' + path
        except:
            logger.exception('Fehler beim Ermitteln des Pfades: ')
            print(item, type(item))
            return ''

        return path

    def getExportPaths(self):
        items = self.tcUpload.GetCheckedItems()

        paths = []
        for item in items:
            paths.append(self.getUploadPath(item))

        return paths

    def getCustomNames(self):
        items = self.tcUpload.GetCheckedItems()

        result = {}
        for item in items:
            path = self.getUploadPath(item)
            if path in self._customNames:
                result[path] = self._customNames[path]
            else:
                result[path] = path
        return result

    def setCustomNames(self, value):
        items = self.tcUpload.GetAllItems()
        logger.debug('Alle items ' + str(len(items)))
        for item in items:
            path = self.getUploadPath(item)
            if path in value:
                self.changeCustomName(item, value[path], path)





