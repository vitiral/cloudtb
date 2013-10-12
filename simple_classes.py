#!/usr/bin/python
# -*- coding: utf-8 -*-
#    The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    https://github.com/cloudformdesign/cloudtb
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT
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
        
