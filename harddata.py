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

import time
import math
import cPickle

import tempfiles

import logtools
logtools.setup_logger(logtools.logging.DEBUG)
LOG = logtools.get_logger(__name__)

def harddata_base(object):
    MIN_KEEP_TIME = 0.5
    def __init__(self, data):
        self._data = data
        self._last_accessed = time.time()
        self._access_counter = 1
        self._THREAD_hold = False
        self._datafile = None        
        self._get_tempfile()
    
    def _get_tempfile(self):
        assert(self._datafile == None)
        self._datafile = tempfiles.get_temp_file()
    
    def _getdata(self):
        '''The primary magic that stores the data'''
        # TODO: need to figure out how threading works here with
        # data stuff. Can't have them fighting        
        self._last_accessed = time.time()
        self._access_counter += 1
        try:
            return self._data
        except AttributeError:
            self._data = self._load_data()
            return self._data
    
    def _load_data(self):
        '''loads the data from temp file'''
        self._data = cPickle.load(self._datafile)        
        
    def _store_data(self):
        '''Stores the data. Hasn't been accessed for a while'''
        self._access_counter = 0
        cPickle.dump(self._data, self._datafile, 
                     protocol = cPickle.HIGHEST_PROTOCOL)
        del self._data
        
    def _check(self):
        '''checks to see if it's data needs to be stored'''
        # TODO: Threading stuff, how to request lock?
        now = time.time()
        sroot = int(math.sqrt(self._access_counter)) + 1
        self._access_counter = sroot
        if now - self._last_accessed < self.MIN_KEEP_TIME:
            return
        
        if sroot > 100:
            return
        else:
            self._store_data()
