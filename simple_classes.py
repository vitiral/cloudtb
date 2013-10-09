# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:56:57 2013

@author: user
"""
import os
import tempfile
import cPickle


class NotInitialized:
    pass

class File:
    def __init__(self, path, data = None, pickled_data = None):
        '''
        '''
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            raise ValueError('Path does not exist: ', self.path)
        
        self.data = data
        self._tempfile = None
        if pickled_data:
            self._pickle(pickled_data)
    
    def get_pickled_data(self):
        self._tempfile.seek(0)
        return cPickle.load(self._tempfile)
    
    def _pickle(self, data):
        if not self._tempfile:
            self._tempfile = tempfile.TemporaryFile()
        self._tempfile.truncate(0)  # delete file contents
        cPickle.dump(data, self._tempfile, 
                     protocol = cPickle.HIGHEST_PROTOCOL)

class Folder:
    def __init__(self, path, files):
        '''gets a list of files and folders and stores them.
        Also stores the os.path.abspath of it's path'''
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            raise ValueError('Path does not exist: ', self.path)
        self.files = files
        
