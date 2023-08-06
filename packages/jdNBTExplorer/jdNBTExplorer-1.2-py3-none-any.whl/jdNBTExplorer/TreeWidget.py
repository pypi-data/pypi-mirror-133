from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QInputDialog, QHeaderView
from .Functions import showMessageBox, stringToList
from PyQt6.QtGui import QCursor
import copy
import nbt
import os

class TagItem(QTreeWidgetItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.tag_type = None
        self.file_path = None
        self.file_type = None
        self.pos_x = None
        self.pos_z = None

    def setTagType(self, name):
        self.tag_type = name

    def tagType(self):
        return self.tag_type

    def updateTypeText(self):
        if self.tag_type == "int":
            self.setText(2,"Int")
        elif self.tag_type == "int_array":
            self.setText(2,"IntArray")
        elif self.tag_type == "long":
            self.setText(2,"Long")
        elif self.tag_type == "long_array":
            self.setText(2,"LongArray")
        elif self.tag_type == "double":
            self.setText(2,"Double")
        elif self.tag_type == "float":
            self.setText(2,"Float")
        elif self.tag_type == "byte":
            self.setText(2,"Byte")
        elif self.tag_type == "byte_array":
            self.setText(2,"ByteArray")
        elif self.tag_type == "string":
            self.setText(2,"String")
        elif self.tag_type == "short":
            self.setText(2,"Short")
        elif self.tag_type == "compound":
            self.setText(2,"Compound")
        elif self.tag_type == "list":
            self.setText(2,"List")
        elif self.tag_type == "none":
            self.setText(2,"None")
        elif self.tag_type == "chunk":
            self.setText(2,"Chunk")

    def setPath(self, path):
        self.file_path = path

    def getPath(self):
        return self.file_path

    def setFileType(self, filetype):
        self.file_type = filetype

    def getFileType(self):
        return self.file_type

    def setChunkCords(self, x, z):
        self.pos_x = x
        self.pos_z = z

    def getChunkCords(self):
        return self.pos_x, self.pos_z

class TreeWidget(QTreeWidget):
    def __init__(self, env):
        super().__init__()
        self.setAcceptDrops(True)
        self.env = env
        self.NoneTag = None
        self.setHeaderLabels((env.translate("treeWidget.header.name"), env.translate("treeWidget.header.value"),env.translate("treeWidget.header.type")))
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.itemDoubleClicked.connect(self.editTag)
        self.currentItemChanged.connect(self.updateMenu)
         # self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        #self.setAcceptDrops(True)
        #self.setDragEnabled(True)
        #self.setAllowDrag(True)

    def updateMenu(self, item):
        if item == None:
            return
        if item.tagType() == "compound" or item.tagType() == "root":
            self.env.mainWindow.editTagAction.setEnabled(False)
        else:
            self.env.mainWindow.editTagAction.setEnabled(True)
        if item.tagType() != "root":
            if item.parent().tagType() != "list":
                self.env.mainWindow.renameCompoundAction.setEnabled(True)
            else:
                self.env.mainWindow.renameCompoundAction.setEnabled(False)
        else:
            self.env.mainWindow.renameCompoundAction.setEnabled(False)
        if item.tagType() == "root":
            self.env.mainWindow.removeTagAction.setEnabled(False)
        else:
            self.env.mainWindow.removeTagAction.setEnabled(True)
        self.env.mainWindow.newTagAction.setEnabled(True)
        self.env.mainWindow.newCompoundAction.setEnabled(True)
        self.env.mainWindow.newListAction.setEnabled(True)

    def newFile(self, path):
        rootItem = TagItem(0)
        rootItem.setText(0,os.path.basename(path))
        rootItem.setPath(path)
        rootItem.setTagType("root")
        rootItem.setFileType("nbt")
        self.addTopLevelItem(rootItem)

    def openNBTFile(self, path):
        try:
            nbtfile = nbt.nbt.NBTFile(path,"rb")
        except:
            print("FFF")
            showMessageBox(self.env.translate("treeWidget.messageBox.cantRead.title"),self.env.translate("treeWidget.messageBox.cantRead.text") % path)
            return
        rootItem = TagItem(0)
        rootItem.setText(0,os.path.basename(path))
        rootItem.setPath(path)
        rootItem.setTagType("root")
        rootItem.setFileType("nbt")
        self.parseCombound(rootItem,nbtfile)
        self.addTopLevelItem(rootItem)

    def openRegionFile(self,path):
        region = nbt.region.RegionFile(path,"rb")
        rootItem = TagItem(0)
        rootItem.setText(0,os.path.basename(path))
        rootItem.setPath(path)
        rootItem.setTagType("root")
        rootItem.setFileType("region")
        for i in region.get_chunks():
            lengthItem = TagItem(rootItem)
            lengthItem.setText(0,f'X:{i["x"]}Z:{i["z"]}')
            lengthItem.setChunkCords(i["x"],i["z"])
            lengthItem.setTagType("chunk")
            lengthItem.updateTypeText()
            nbtdata = region.get_nbt(i["x"],i["z"])
            self.parseCombound(lengthItem,nbtdata)
        self.addTopLevelItem(rootItem)

    def parseData(self, name, value, parentItem, data):
        item = TagItem(parentItem)
        item.setText(0,name)
        if isinstance(value,nbt.nbt.TAG_Int):
            item.setTagType("int")
        elif isinstance(value,nbt.nbt.TAG_Int_Array):
            item.setTagType("int_array")
        elif isinstance(value,nbt.nbt.TAG_Long):
            item.setTagType("long")
        elif isinstance(value,nbt.nbt.TAG_Long_Array):
            item.setTagType("long_array")
        elif isinstance(value,nbt.nbt.TAG_Double):
            item.setTagType("double")
        elif isinstance(value,nbt.nbt.TAG_Float):
            item.setTagType("float")
        elif isinstance(value,nbt.nbt.TAG_Byte):
            item.setTagType("byte")
        elif isinstance(value,nbt.nbt.TAG_Byte_Array):
            item.setTagType("byte_array")
        elif isinstance(value,nbt.nbt.TAG_String):
            item.setTagType("string")
        elif isinstance(value,nbt.nbt.TAG_Short):
            item.setTagType("short")
        elif isinstance(value,nbt.nbt.TAG_Compound):
            item.setTagType("compound")
        elif isinstance(value,nbt.nbt.TAG_List):
            item.setTagType("list")
        elif value.value == None:
            item.setTagType("none")
            self.NoneTag = value
        else:
            print(type(value))
        item.updateTypeText()
        if hasattr(value,"items"):
            self.parseCombound(item,value)
        elif isinstance(value,nbt.nbt.TAG_List):
            self.parseList(item,value)
        elif  isinstance(value,nbt.nbt.TAG_Byte_Array):
            s = "["
            for i in value:
                s += f"{i},"
            s = s[:-1] + "]"
            item.setText(1,s)
        else:
            item.setText(1,str(value.value))

    def parseCombound(self, parentItem, data):
        for key, value in data.items():
            self.parseData(key,value,parentItem,data)

    def parseList(self,parentItem,data):
        for count, i in enumerate(data):
             self.parseData(str(count),i,parentItem,data)

    def saveData(self):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.getFileType() == "nbt":
                f = nbt.nbt.NBTFile()
                self.getSaveList(item,f.tags)
                f.write_file(item.getPath())
            elif item.getFileType() == "region":
                showMessageBox("Not supported","Saving a region file is currently not supported")
                #region = nbt.region.RegionFile(item.getPath(),"rb")
                #for i in range(item.childCount()):
                    #x, z = item.child(i).getChunkCords()
                   # self.getItems(item.child(i),region.get_nbt(x,z).tags)
                    #self.getSaveList(item.child(i),region.get_nbt(x,z).tags)
                    #f = nbt.nbt.NBTFile()
                    #region.write_chunk(x,z,f)
                #region.close()
                #region.close()
            self.env.modified = False

    def getTag(self, child):
        tagType = child.tagType()
        if tagType == "int":
            data = nbt.nbt.TAG_Int(int(child.text(1)),name=child.text(0))
        elif tagType == "int_array":
            array = stringToList(child.text(1),int)
            data = nbt.nbt.TAG_Int_Array(name=child.text(0))
            data.value = array
        elif tagType == "long":
            data = nbt.nbt.TAG_Long(int(child.text(1)),name=child.text(0))
        elif tagType == "long_array":
            array = stringToList(child.text(1),int)
            data = nbt.nbt.TAG_Long_Array(name=child.text(0))
            data.value = array
        elif tagType == "double":
            data = nbt.nbt.TAG_Double(float(child.text(1)),name=child.text(0))
        elif tagType == "float":
            data = nbt.nbt.TAG_Float(float(child.text(1)),name=child.text(0))
        elif tagType == "byte":
            data = nbt.nbt.TAG_Byte(int(child.text(1)),name=child.text(0))
        elif tagType == "byte_array":
            array = stringToList(child.text(1),int)
            data = nbt.nbt.TAG_Byte_Array(name=child.text(0))
            data.value = array
        elif tagType == "string":
            data = nbt.nbt.TAG_String(child.text(1),name=child.text(0))
        elif tagType == "short":
            data = nbt.nbt.TAG_Short(int(child.text(1)),name=child.text(0))
        elif tagType == "compound":
            data = nbt.nbt.TAG_Compound()
            self.getSaveCompound(child,data)
        elif tagType == "list":
            if child.childCount() == 0:
                data = nbt.nbt.TAG_List(type=nbt.nbt.TAG_Int,name=child.text(0))
            else:
                list_tag_type = self.getTag(child.child(0)).__class__
                data =nbt.nbt.TAG_List(type=list_tag_type,name=child.text(0))
                self.getSaveList(child,data)
        elif tagType == "none":
            data = copy.copy(self.NoneTag)
        else:
            data = nbt.nbt.TAG_String("Error",name=child.text(0))
        data.name = child.text(0)
        return data

    def getSaveList(self,item,tags):
        for i in range(item.childCount()):
            child = item.child(i)
            tagType = child.tagType()
            tags.append(self.getTag(child))

    def getSaveCompound(self,item,tags):
        for i in range(item.childCount()):
            child = item.child(i)
            tagType = child.tagType()
            tag = self.getTag(child)
            tags[tag.name] = tag

    def newTag(self):
        item = self.currentItem()
        if item:
            if item.tagType() == "compound" or item.tagType() == "root":
                self.env.editWindow.openWindow(True,item)
            elif item.tagType() == "list":
                 self.env.editWindow.openWindow(True,item,taglist=True,name=str(item.childCount()))
            elif item.parent().tagType() == "list":
                 self.env.editWindow.openWindow(True,item.parent(),taglist=True,name=str(item.parent().childCount()))
            else:
                self.env.editWindow.openWindow(True,item.parent())

    def editTag(self):
        item = self.currentItem()
        if item:
            if item.tagType() != "compound" and  item.tagType() != "list" and item.tagType() != "chunk" and item.tagType() != "root":
                if item.parent().tagType() == "list":
                    self.env.editWindow.openWindow(False,item,taglist=True)
                else:
                    self.env.editWindow.openWindow(False,item)

    def newCompound(self):
        item = self.currentItem()
        if item:
            name, ok = QInputDialog.getText(self,self.env.translate("treeWidget.messageBox.newCompound.title"),self.env.translate("treeWidget.messageBox.newCompound.text"))
            if not ok or name == '':
                return
            if item.tagType() == "compound" or item.tagType() == "list" or item.tagType() == "root":
                newComp = TagItem(item)
            else:
                newComp = TagItem(item.parent())
            newComp.setText(0,name)
            newComp.setTagType("compound")
            newComp.updateTypeText()
            self.env.modified = True

    def newList(self):
        item = self.currentItem()
        if item:
            name, ok = QInputDialog.getText(self,self.env.translate("treeWidget.messageBox.newCompound.title"),self.env.translate("treeWidget.messageBox.newCompound.text"))
            if not ok or name == '':
                return
            if item.tagType() == "compound" or item.tagType() == "list" or item.tagType() == "root":
                newComp = TagItem(item)
            else:
                newComp = TagItem(item.parent())
            newComp.setText(0,name)
            newComp.setTagType("list")
            newComp.updateTypeText()
            self.env.modified = True

    def renameItem(self):
        item = self.currentItem()
        if item:
            name, ok = QInputDialog.getText(self,self.env.translate("treeWidget.messageBox.rename.title"),self.env.translate("treeWidget.messageBox.rename.text"),text=item.text(0))
            if ok and name != '':
                item.setText(0,name)
                self.env.modified = True

    def removeTag(self):
        item = self.currentItem()
        if item:
            if item.tagType() != "root":
                parent = item.parent()
                parent.removeChild(item)
                self.env.modified = True
                if parent.tagType() == "list":
                    for count,i in enumerate(range(parent.childCount())):
                        child = parent.child(i)
                        child.setText(0,str(count))

    def clearItems(self):
        for i in range(self.topLevelItemCount()):
            self.takeTopLevelItem(i)

    def contextMenuEvent(self, event):
        self.env.mainWindow.tagMenu.popup(QCursor.pos())

    def dropEvent(self, event):
        event.accept()
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            path = mimeData.urls()[0].toLocalFile()
            if os.path.isdir(path):
                self.treeWidget.clearItems()
                self.env.mainWindow.openDirectory(path)
            else:
                self.env.mainWindow.openFile(path)

    def mimeTypes(self):
        # This is needed for dropping files in a QTreeWidget
        return ['text/uri-list']
