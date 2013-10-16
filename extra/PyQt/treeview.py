import pdb

from PyQt4 import QtCore, QtGui
import sys
import icons_rc

from cloudtb import dbe

class Node(object):
    '''I think some of these might be required definitions by PyQt. I'm not
    sure how else it would work!
    
    '''
    def __init__(self, name, parent=None, attrib_dict = None):
        
        self._name = name
        self._attrib = attrib_dict
        self._children = []
        self._parent = parent
        
        if parent is not None:
            parent.addChild(self)


    def typeInfo(self):
        return "NODE"

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        
        if position < 0 or position > len(self._children):
            return False
        
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None

        return True

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]
    
    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent
    
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)


    def log(self, tabLevel=-1):

        output     = ""
        tabLevel += 1
        
        for i in range(tabLevel):
            output += "\t"
        
        output += "|------" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)
        
        tabLevel -= 1
        output += "\n"
        
        return output

    def __repr__(self):
        return self.log()



class TableViewModel(QtCore.QAbstractItemModel):
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(TableViewModel, self).__init__(parent)
        self._rootNode = root

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 1
    
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):
        '''index is an object that contains a pointer to the item inside
        internPointer().  Note that this was set during the insertRows 
        method call, so you don't need to track them!
        '''
        if not index.isValid():
            return None
        
        
        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()
                
                if typeInfo == "LIGHT":
                    return QtGui.QIcon(QtGui.QPixmap(":/Light.png"))
                
                if typeInfo == "TRANSFORM":
                    return QtGui.QIcon(QtGui.QPixmap(":/Transform.png"))
                
                if typeInfo == "CAMERA":
                    return QtGui.QIcon(QtGui.QPixmap(":/Camera.png"))

    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setName(value)
                return True
        return False
    
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Typeinfo"
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return (QtCore.Qt.ItemIsEnabled | 
            QtCore.Qt.ItemIsSelectable #| 
#            QtCore.Qt.ItemIsEditable
            )

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, 
        column and parent node"""
    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode

    
    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + len(rows) - 1)
        
        for row in rows:
#            childCount = parentNode.childCount()
            childNode = row
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success
    
    def insertLights(self, position, rows, parent=QtCore.QModelIndex()):
        
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = LightNode("light" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success

    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            success = parentNode.removeChild(position)
            
        self.endRemoveRows()
        
        return success

def get_file_folder_node(fdata, parent):
    '''return the node structure of the data.
    [[(dir_name, path), 
      [dir_name, path), 
        [(file, path), 
        (file, path)]]
      ]
    ]    
    '''
    name, path = fdata[0]
    attrib_dict = {'path', path}
    if len(fdata) == 1:
        fileobj = Node(name, attrib_dict=attrib_dict, parent = parent)
        return fileobj
    folderobj = Node(name, attrib_dict=attrib_dict, parent = parent)
    for fobj in fdata[1]:
        get_file_folder_node(fobj, parent = folderobj)
    return folderobj
    
if __name__ == '__main__':
    from pprint import pprint
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    
    rootNode   = Node("Rootdir")
    dir1 = Node("Dir1", rootNode)
    file1 = Node("file1", dir1)
    file2 = Node("file2", dir1)
    dir1_1 = Node("dir1_1", dir1)
    file1_1 = Node('file1_1', dir1_1)
    
#    childNode0 = TransformNode("RightPirateLeg",        rootNode)
#    childNode1 = Node("RightPirateLeg_END",             childNode0)
#    childNode2 = CameraNode("LeftFemur",                rootNode)
#    childNode3 = Node("LeftTibia",                      childNode2)
#    childNode4 = Node("LeftFoot",                       childNode3)
#    childNode5 = LightNode("LeftFoot_END",              childNode4)

    print rootNode
    
    model = TableViewModel(rootNode)
    
    treeView = QtGui.QTreeView()
    treeView.show()
    
    treeView.setModel(model)
    
    file1 = [('file1', 'pfile1')]
    file2 = [('file2', 'pfile2')]
    file3 = [('file3', 'pfile3')]
    file4 = [('file4', 'pfile4')]    
    folder1 = [('folder1', 'pfolder1'), (file1, file2)]
    folder2 = [('folder2', 'pfolder2'), (file3,)]
    
    basefolder = [('base', 'pbase'), (folder1, folder2, file4)]
    
    pdb.set_trace()
    rows = get_file_folder_node(basefolder, None)
    pprint(rows)
    model.insertRows(1, [rows], QtCore.QModelIndex())
#    rightPirateLeg = model.index(0, 0, QtCore.QModelIndex())
#    
#    
#    model.insertRows(1, 5, rightPirateLeg)
#    model.insertLights(1, 5 , rightPirateLeg)

    sys.exit(app.exec_())