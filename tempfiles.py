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
"""
This module is created to extend the module tempfile. It handles things better
than tempfile, automatically deleting previous processes files if they have
not been used for a long time.

It will also be eventually extended to a new type of data, harddata. This data
type will automatically store it's variable if it hasn't been used in a while.

It uses the threading module after the first call of get_temp_file. If your
applicationc cannot support threading, then:
    Define your own THREAD_LOCK object to handle locking, make sure to set
        the global variable to the object you are using.
    set THREAD_HANDLED = True
    call create_temp_directory
    call THREAD_manage_harddata about every .5 seconds
    
"""
import sys, os
import pdb
import dbe
import cPickle
import time
import shutil
import re
import tempfile

import errors
import system
import textools

THREAD_HANDLED = False
THREAD_LOCK = None          
THREAD_PERIOD = 30 # How often the therad runs in seconds
DELETE_TMP_AFTER = 60*60    # deletes unupdated temporary files if their
                            # timer file is not updated in an hour

#ga = harddata_base.__getattribute__
#sa = harddata_base.__setattr__
ga = object.__getattribute__
sa = object.__setattr__

# DO NOT MODIFY THESE
TIMER_FILE = 'pytimer.time'     # DO NOT CHANGE
TEMP_DIRECTORY = None
_HARDDATA = []      # not currently used

STR_TEMP_PREFIX = 'pyhdd08234'
STR_TEMP_SUFIX = '.hd'
tmp_regexp = r'^{0}(.*?){1}$'.format(textools.convert_to_regexp(STR_TEMP_PREFIX),
                                    textools.convert_to_regexp(STR_TEMP_SUFIX))

tmp_regexp = re.compile(tmp_regexp)

def get_temp_file():
    if not TEMP_DIRECTORY:
        create_temp_directory()
    tempfile.mkstemp(suffix = STR_TEMP_SUFIX, prefix = STR_TEMP_PREFIX,
                     dir = TEMP_DIRECTORY)

def create_harddata_thread():
    global THREAD_harddata
    global THREAD_lock
    global THREAD_HANDLED
    
    assert(not THREAD_HANDLED)
    
    from errors import ModuleError
    try:
        THREAD_harddata
        raise ModuleError("Thread already started")
    except NameError:
        pass

    from threading import Thread, Lock
    
    class harddata_thread(Thread):
        def __init__(self, harddata, lock):
            print "intializing thread"
            self.harddata = harddata
            self.lock = lock
            Thread.__init__(self)
            
        def run(self):
            while True:
                print "running thread"
                start_time = time.time()
                THREAD_manage_harddata()
                if time.time() - start_time > THREAD_PERIOD:
                    # the _check took longer than the thread period!
                    # TODO: change this to logging. Here for debug
                    assert(0)
                else:
                    print 'thread sleeping'
                    time.sleep(self.last_run - start_time)
                
                
    THREAD_lock = Lock()
    THREAD_harddata = harddata_thread(_HARDDATA, THREAD_lock)
    THREAD_HANDLED = True
    THREAD_harddata.run()

def create_temp_directory():
    global TEMP_DIRECTORY
    TEMP_DIRECTORY = tempfile.mkdtemp(suffix = '.hd', prefix = STR_TEMP_PREFIX, 
                              dir = tempfile.gettempdir())
    
    THREAD_manage_harddata()

    if not THREAD_HANDLED:
        create_harddata_thread()

def THREAD_manage_harddata():
    THREAD_LOCK.acquire()
    for hd in _HARDDATA:
        hd._check(time.time())
    _manage_temp_dirs()
    THREAD_LOCK.release()
    
def _manage_temp_dirs():
    update_timer_file()
    
    temp_folders = (tmpf for tmpf in os.listdir(tempfile.gettempdir()) 
            if os.path.isdir(tmpf) and tmp_regexp.match(tmpf, len(tmpf)))
    
    for tmpfold in temp_folders:
        tpath = os.path.join(tmpfold)
        if not check_timer(tpath):
            shutil.rmtree(tpath)            
#            shutil.rmtree(tpath, onerror = errors.print_prev_exception)
    
def update_timer_file():
    '''updates the file timer so that external python processes don't
    delete the temp data'''
    global TEMP_DIRECTORY
    with open(os.path.join(TEMP_DIRECTORY, TIMER_FILE), 'w') as f:
        f.write(time.ctime(time.time()))

def check_timer(folder_path):
    '''returns whether the data should be kept (True) or deleted (False)'''
    timer_path = os.path.join(TEMP_DIRECTORY, TIMER_FILE)
    if time.time() - os.path.getatime(timer_path) > DELETE_TMP_AFTER:
        return False
    return True
    
if __name__ == '__main__':
    pass
