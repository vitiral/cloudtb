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

import logging, tempfile, os, sys, time, traceback
#from logging import CRITICAL, DEBUG, ERROR, FATAL, WARN, WARNING, INFO
global IS_SETUP, MAX_SIZE, USE_DBE


MAX_SIZE = 10e6 # maximum size of std log file = 10MB
USE_DBE = False    # will use dbe when level == loggging.DEBUG.  
                   # If set to false, it will not.

# the Setup Logger automatically handles the level and everything else
IS_SETUP = False
LEVEL = None

def setup_logger(level = logging.INFO, filename = 'python.log', directory = None, format =
                '%(levelname)s:%(name)s.%(funcName)s:%(message)s', 
                ignoresize = False, dbeDisabled = False):
   #'L:%(name)s M:%(module)s F:%(funcName)s T:%(asctime)s > %(levelname)s: %(message)s'
   global IS_SETUP, LEVEL
   if IS_SETUP:
       return
   if directory == None:
#      fd, fname = tempfile.mkstemp()
#      directory = os.path.dirname(fname)
#      os.remove(fname)
      directory = tempfile.gettempdir()

   fullpath = os.path.join(directory, filename)
   size = 0
   try:
      size = os.path.getsize(fullpath)
   except OSError:
      pass

   if size > MAX_SIZE and ignoresize == False:
      os.remove(fullpath)

   logging.basicConfig(filename = fullpath, format = format)

   from logging import handlers
   socketHandler = handlers.SocketHandler('localhost',
                    handlers.DEFAULT_TCP_LOGGING_PORT)
   rootLog = logging.getLogger('')
   rootLog.addHandler(socketHandler)

   IS_SETUP = True
   if level == logging.DEBUG:
      print 'log at: ' + fullpath
      if dbeDisabled == False and USE_DBE == True:
          log_fatal_exception()

   mylog = get_logger('LogStart')
   mylog.setLevel(level)
   mylog.info('\n{0:*^80}'.format(' ##$ LOGGING STARTED '
              + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + ' $## '))

def get_logger(logname = None, modname = None, funname = None, 
              level = logging.INFO, dbeDisabled = False):
   '''returns a logger with logname that will print to the temporary directory.
   If level is == logging.DEBUG it will automatically do post-exception 
   logging, and go into dbe (unless dbeDisabled is set).  In this way, the 
   operation of all my debugging can be set by a single variable.'''
   if IS_SETUP == False:
      setup_logger(level = level, dbeDisabled = dbeDisabled)

   while logname == None:
      stack = traceback.extract_stack()
      if len(stack) < 2:
         funame, modname = ('unknown',) *2
      else:
         stack = stack[-2]

      if funname == None:
         funname = stack[2] if not None else 'unknown'
      if modname == None:
         modname = ''.join(os.path.basename(stack[0]).split('.')[:-1]) if not None else 'unknown'
      logname = modname + '.' + funname
      break

   mylog = logging.getLogger(logname)
   mylog.setLevel(level)
   return mylog

def log_fatal_exception():
   '''will log the exception on sys.excepthook'''

   def except_hook(exctype, value, tb):
      if previous_except_hook:
         previous_except_hook(exctype, value, tb)

      log = get_logger('FATAL_EXCEPTION')
      log.critical(str(exctype) + '\n' + str(value) + '\n' + 
          ''.join(traceback.format_tb(tb)))

   previous_except_hook = sys.excepthook
   sys.excepthook = except_hook

if __name__ == '__main__':
   log = get_logger(__name__, level = logging.DEBUG)
   log.info('working?')
   log.info('yes, seems to be working')

   log2 = get_logger(__name__)
   log2.info('still working?')

   x = 1 / 0