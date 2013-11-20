# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 07:32:05 2013

@author: user
"""

from PyQt4 import QtGui

class BaseQtText(object):
    def getText(self):
        return self.toPlainText()
        
    # seting text functions
    def setText(self, text):
        plain_text_html = richtext.get_str_plain_html(text)
        self.setHtml(plain_text_html)

    def get_text_cursor(self):
        return self.textCursor()
    
    def get_text_cursor_pos(self):
        return self.get_text_cursor().position()
    def set_text_cursor_pos(self, value):
        tc = self.get_text_cursor()
        tc.setPosition(value)
        self.setTextCursor(tc)
        self.ensureCursorVisible()
        
    def get_text_selection(self):
        cursor = self.get_text_cursor()
        return cursor.selectionStart(), cursor.selectionEnd()
    def set_text_selection(self, start, end):
        cursor = self.get_text_cursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

class BTextEdit(QtGui.QTextEdit, BaseQtText):
    pass

class BTextBrowser(QtGui.QTextBrowser, BaseQtText):
    pass

    