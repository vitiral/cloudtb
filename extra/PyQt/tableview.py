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

class TableViewModel(QtCore.QAbstractTableModel):
    """Creates a tableview object.
    data -- the base data it starts with
    checkboxes -- if set to true, then the last column holds checkbox data
        and the first column is checkable (default)
    """
    dataWasChanged = QtCore.pyqtSignal()
    
    def __init__(self, data = None, headers = None,
                 parent=None, header_title = None,
                 checkboxes = False):
        super(TableViewModel, self).__init__(parent)
        self.checkboxes = checkboxes
        if data == None:
            self.data = [['']]
            if checkboxes:
                self.data[0].append(False)
        else:
            self.data = data
        self.headers = headers
        self.is_editable = False
        self.is_selectable = True
        self.is_enabled = True
        self.set_flags()
        self.header_title = header_title

    # The following are created functions called in "data" -- which is a 
    # Qt defined funciton. This way of doing things is FAR more pythonic
    # and allows classes to inherit this one and not have to rewrite the
    # entire data method
    # all of them recieve an index and a node
    
    def role_display(self, index):
        data = self.data[index.row()][index.column()]
        if data == None:
            data = ''
        return QtCore.QString(str(data))
    
    def role_edit(self, index):
        return self.role_display(index)
    
    def role_tool_tip(self, index):
        return
        
    def role_check_state(self, index):
        if self.checkboxes and index.column() == 0:
            value = self.data[index.row()][-1]
            if value:
                return QtCore.QVariant(QtCore.Qt.Checked)
            else:
                return QtCore.QVariant(QtCore.Qt.Unchecked)
    
    def role_decoration(self, index):            
        return False
    
    def role_flags(self, index):
        '''While not technically a "role" it behaves in much the same way.
        This method is called by the "flags" method for all indexes'''
        flags = self.BASE_FLAGS        
        if self.checkboxes and index.column() == 0:
            flags |= QtCore.Qt.ItemIsUserCheckable
        return flags
    
    def setData_role_edit(self, index, value):
        value = str(value.toString())
        try:
            value = float(value)
        except (ValueError, TypeError):
            pass
        self.data[index.row()][index.column()] = value
        return True
    
    def setData_role_checkstate(self, index, value):
        if self.checkboxes:
            self.data[index.row()][-1] = value.toBool()
            return True
    
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
        return len(self.data)
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent): 
        _len = len(self.data[0])
        if self.checkboxes:
            _len -= 1
        return _len
    
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):
        '''index is an object that contains a pointer to the item inside
        internPointer().  Note that this was set during the insertRows 
        method call, so you don't need to track them!
        '''
        if not index.isValid():
            return None
        
        if role == QtCore.Qt.EditRole:
            return self.role_edit(index)
        
        if role == QtCore.Qt.ToolTipRole:
            return self.role_tool_tip(index)
        
        if role == QtCore.Qt.CheckStateRole:
            return self.role_check_state(index)
        
        if role == QtCore.Qt.DisplayRole:
            return self.role_display(index)
            
        if role == QtCore.Qt.DecorationRole:
            return self.role_decoration(index)

    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return
        
        self.dataWasChanged.emit()
        
        if role == QtCore.Qt.EditRole:
            return self.setData_role_edit(index, value)
        
        if role == QtCore.Qt.CheckStateRole:
            return self.setData_role_checkstate(index, value)
        
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal and self.headers:
                if section < len(self.headers):
                    return QtCore.QString(self.headers[section])
                else:
                    return "not implemented"
            else:
                return QtCore.QString(" ")
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return self.role_flags(index)

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    """INPUTS: int, List of Nodes, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        
        self.beginInsertRows(parent, position, position + len(rows) - 1)
        
        for i, row in enumerate(rows):
            self.data.insert(position + i, row)
        
        self.endInsertRows()

        return True
    
    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        if rows == 0:
            return
        self.beginRemoveRows(parent, position, position + rows - 1)
        del self.data[position : position + rows]
        self.endRemoveRows()
        
        return True
    
    def moveRows(self, position, rows, 
                 end_position, parent = QtCore.QModelIndex()):
        try:
            assert(position >= 0 and position + rows <= len(self.data))
            assert(end_position >= 0 and end_position <= len(self.data))
        except AssertionError:
            return False
        
        self.beginMoveRows(parent, position, position + rows - 1,
                           parent, end_position)
        end = position + rows
        moved = []
        
        # remove rows
        for i in xrange(position, end):
            moved.append(self.data.pop(position))
        
        # put in None placemarkers
        for i in xrange(position, end):
            self.data.insert(position, None)
        
        # insert them into the correct place
        for i in xrange(len(moved)):
            self.data.insert(end_position, moved.pop())
        
        # remove placemarkers
        try:
            while True:
                i = self.data.index(None)
                self.data.pop(i)
        except ValueError:
            pass
        self.endMoveRows()
        return True
    
    def moveRowsUp(self, position, rows):
        return self.moveRows(position, rows, position - 1)
    
    def moveRowsDown(self, position, rows):
        return self.moveRows(position, rows, position + rows + 1)
    
    # DEV
    def insertColumns(self, position, columns, parent = QtCore.QModelIndex()):
        check = len(self.data[0])
        if self.checkboxes:
            check -= 1
        if not position < check:
            raise IndexError("Position is outside of data range")
        self.beginInsertColumns(parent, position, position + columns - 1)
        rowCount = len(self.data)
        for i in range(columns):
            for j in range(rowCount):
                self.data[j].insert(position, '')
        self.endInsertColumns()
        return True

def dev_tableview():
    '''For developemnet'''
    import pdb
    
    app = QtGui.QApplication(sys.argv)
    
    data = [range(n, n+10) for n in range(20)]
    model = TableViewModel(data, checkboxes=True, 
                headers = [str(n) for n in range(10)]) 
    model.set_flags(is_editable=True)
    Table = QtGui.QTableView()
    Table.setModel(model)
    Table.show()
    
#    model.insertRows(0, data, QtCore.QModelIndex())
    sys.exit(app.exec_())

if __name__ == '__main__':
    dev_tableview()