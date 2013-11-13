#!/usr/bin/python
# -*- coding: utf-8 -*-
#    ******  The Cloud Toolbox v0.1.2******
#    This is the cloud toolbox -- a single module used in several packages
#    found at <https://github.com/cloudformdesign>
#    For more information see <cloudformdesign.com>
#
#    This module may be a part of a python package, and may be out of date.
#    This behavior is intentional, do NOT update it.
#    
#    You are encouraged to use this pacakge, or any code snippets in it, in
#    your own projects. Hopefully they will be helpful to you!
#        
#    This project is Licenced under The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    <https://github.com/cloudformdesign/cloudtb>
#    
#    Permission is hereby granted, free of charge, to any person obtaining a 
#    copy of this software and associated documentation files (the "Software"),
#    to deal in the Software without restriction, including without limitation 
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,
#    and/or sell copies of the Software, and to permit persons to whom the 
#    Software is furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#    DEALINGS IN THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT
import pdb
import os

from PyQt4 import QtCore, QtGui
import sys
import icons_rc


from cloudtb import dbe

class Node(object):
    '''A general node stucture to be used in treeview
    the attrib_dict can store any information your overall treeview 
    needs it to store.
    
    '''
    def __init__(self, name, parent=None, icon = None, 
                 attrib_dict = None):
        
        self._name = name
        self._attrib = attrib_dict
        self._children = []
        self._parent = parent
        self.icon = icon
        
        if parent is not None:
            parent.addChild(self)

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
            output += "  "
        
        output += "|-" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)
        
        tabLevel -= 1
#        output += "\n"
        
        return output

    def __repr__(self):
        return self.log()

class TreeViewModel(QtCore.QAbstractItemModel):
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None, header_title = None):
        super(TreeViewModel, self).__init__(parent)
        self.is_editable = False
        self.is_selectable = True
        self.is_enabled = True
        self.set_flags()
        self._rootNode = root
        self.header_title = header_title

    # The following are created functions called in "data" -- which is a 
    # Qt defined funciton. This way of doing things is FAR more pythonic
    # and allows classes to inherit this one and not have to rewrite the
    # entire data method
    # all of them recieve an index and a node
    
    def role_display(self, index, node):
        if index.column() == 0:
                return node.name()
    
    def role_edit(self, index, node):
        return self.role_display(index, node)
    
    def role_tool_tip(self, index, node):
        return
        
    def role_check_state(self, index, node):
        return
    
    def role_decoration(self, index, node):            
        if index.column() == 0:
            icon = node.icon
            if icon == None:
                return False
            else:
                return icon
    
    def role_flags(self, index, node):
        '''While not technically a "role" it behaves in much the same way.
        This method is called by the "flags" method for all indexes with
        a node'''
        return self.BASE_FLAGS
    
    def set_flags(self, is_editable = None, is_selectable = None,
                  is_enabled = None):
        ''' Sets new flags to the BASE_FLAGS variable'''
        if is_editable != None:
            self.is_editable = is_editable
        if is_selectable != None:
            self.is_selectable = is_selectable
        if is_enabled != None:
            self.is_enabled = is_enabled
        self.BASE_FLAGS = QtCore.Qt.ItemFlags(
              (QtCore.Qt.ItemIsEnabled * bool(self.is_enabled))
            | (QtCore.Qt.ItemIsSelectable * bool(self.is_selectable))
            | (QtCore.Qt.ItemIsEditable * bool(self.is_editable))
            )
    
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
        
        if role == QtCore.Qt.EditRole:
            return self.role_edit(index, node)
        
        if role == QtCore.Qt.ToolTipRole:
            return self.role_tool_tip(index, node)
        
        if role == QtCore.Qt.CheckStateRole:
            return self.role_check_state(index, node)
        
        if role == QtCore.Qt.DisplayRole:
            return self.role_display(index, node)
            
        if role == QtCore.Qt.DecorationRole:
            return self.role_decoration(index, node)

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
            if self.header_title != None:
                return self.header_title
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
    def flags(self, index):
        if not index.isValid():
            return self.BASE_FLAGS
        
        node = index.internalPointer()
        return self.role_flags(index, node)

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
        # This is how Qt creates the nested (tree) list. It knows how many
        # rows it has because of insertRows, and it uses index and
        # createIndex to build the tree.
#        print 'Index called', row, column
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

    
    """INPUTS: int, List of Nodes, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + len(rows) - 1)
        
        for i, row in enumerate(rows):
#            childCount = parentNode.childCount()
            childNode = row
            success = parentNode.insertChild(position + i, childNode)
        
        self.endInsertRows()

        return success
    
    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        if rows == 0:
            return
        
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            success = parentNode.removeChild(position)
            # TODO: break if not success?
            
        self.endRemoveRows()
        
        return success
    
    def clear_rows(self):
        return self.removeRows(0, self._rootNode.childCount())

# TODO: doesn't work. Not sure how to get icons
ICON_FOLDER = QtGui.QIcon.fromTheme('folder')

def _node_compare(a, b):
    return b.isdir - a.isdir
    
def get_file_folder_node(fdata, parent):
    '''return the node structure of the data.
    [[(dir_name, path), 
      [dir_name, path), 
        [(file, path), 
        (file, path)]]
      ]
    ]    
    '''
    # TODO: set icons correctly
    
    nodes = []
    for fobj in fdata:
        path = fobj[0]
        name = os.path.split(path)[1]
        
        if len(fobj) == 1:
            fileobj = Node(name, parent = parent, icon = None)
            fileobj.full_path = path
            fileobj.isdir = False
            nodes.append(fileobj)
            continue
        folderobj = Node(name, parent = parent, icon = ICON_FOLDER,
                         )
        folderobj.full_path = path
        folderobj.isdir = True
        
        get_file_folder_node(fobj[1], parent = folderobj)
        nodes.append(folderobj)
    nodes.sort(cmp = _node_compare)
    return nodes
import itertools

def _get_filelist_nodes(iter_file_list, dir_path = ''):
    '''Takes a sorted file list iterator and returns the files in a 
    format that can be converted'''
    files = []
    dir_path = os.path.join(dir_path, '')   # Put into directory syntax
    len_dp = len(dir_path)
    while True:
        try:
            fpath = next(iter_file_list)
        except StopIteration:
            break
        if dir_path != fpath[:len_dp]:
            iter_file_list = itertools.chain((fpath,), iter_file_list)
            break
        
        if os.path.isdir(fpath):
            iter_file_list, new_files = _get_filelist_nodes(iter_file_list,
                    dir_path = fpath)
            files.append((fpath, new_files))
        else:
            files.append((fpath,))
    return iter_file_list, files

def get_filelist_nodes(file_list, parent = None):
    file_list = sorted(file_list)
    file_tuples = _get_filelist_nodes(iter(file_list))[1]
    return get_file_folder_node(file_tuples, parent)

def dev_show_file_list(file_objects):
    '''For developemnet'''
    
    app = QtGui.QApplication(sys.argv)
    
    rootNode   = Node("Rootdir")
    model = TreeViewModel(rootNode)
    
    treeView = QtGui.QTreeView()
    treeView.show()
    
    treeView.setModel(model)
    model.insertRows(0, file_objects, QtCore.QModelIndex())
    sys.exit(app.exec_())

    
if __name__ == '__main__':
    from pprint import pprint

    files = '''/home/user/Projects/Learning/LearningQt/LearningQt.pro.user
/home/user/Projects/Learning/LearningQt/LearningQt.pro
/home/user/Projects/Learning/LearningQt/qmlapplicationviewer/qmlapplicationviewer.h
/home/user/Projects/Learning/LearningQt/qmlapplicationviewer/qmlapplicationviewer.cpp
/home/user/Projects/Learning/LearningQt/qmlapplicationviewer/qmlapplicationviewer.pri
/home/user/Projects/Learning/LearningQt/qmlapplicationviewer
/home/user/Projects/Learning/LearningQt/LearningQt64.png
/home/user/Projects/Learning/LearningQt/LearningQt_harmattan.desktop
/home/user/Projects/Learning/LearningQt/LearningQt.svg
/home/user/Projects/Learning/LearningQt/main.cpp
/home/user/Projects/Learning/LearningQt/LearningQt.desktop
/home/user/Projects/Learning/LearningQt/qml/LearningQt/main.qml
/home/user/Projects/Learning/LearningQt/qml/LearningQt
/home/user/Projects/Learning/LearningQt/qml
/home/user/Projects/Learning/LearningQt/LearningQt80.png'''    
    nodes = get_filelist_nodes(files.split('\n'))
    for n in nodes:
        print n
    dev_show_file_list(nodes)

