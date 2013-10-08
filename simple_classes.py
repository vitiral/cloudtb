# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:56:57 2013

@author: user
"""
import os

class NotInitialized:
    pass

class File:
    def __init__(self, path, data = NotInitialized):
        '''Stores the path and data. If data is not given,
        automatically opens the specified path when
        self.get_data() is called.
        
        If data is not_initilized, returns f.read() from the file
        
        if data is initialized, the data is automatically pickled and
        get_data returns the unpickled data.
        '''
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            raise ValueError('Path does not exist: ', self.path)
        self.pickled = False
        
        if data != NotInitialized:
            self._data = data
    
    def get_data(self):
        try:
            return self._data
        except AttributeError:
            with open(self.path) as f:
                return f.read()
        
class Folder:
    def __init__(self, path, files):
        '''gets a list of files and folders and stores them.
        Also stores the os.path.abspath of it's path'''
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            raise ValueError('Path does not exist: ', self.path)
        self.files = files
        
