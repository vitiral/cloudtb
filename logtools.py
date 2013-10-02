#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
 * Summary :
 *
 * Created on 2011-04-11
 * @author: garrett
'''
import logging, tempfile, os, sys, time, traceback
#from logging import CRITICAL, DEBUG, ERROR, FATAL, WARN, WARNING, INFO
global IS_SETUP, MAX_SIZE, USE_DBE

IS_SETUP = False
MAX_SIZE = 10e6 # maximum size of std log file = 10MB
USE_DBE = False    # will use dbe when level == loggging.DEBUG.  If set to false, it will not.

def setuplogger(filename = 'python.log', directory = None, format =
                '%(levelname)s:%(name)s.%(funcName)s:%(message)s', level = logging.INFO, ignoresize = False, dbeDisabled = False):
   #'L:%(name)s M:%(module)s F:%(funcName)s T:%(asctime)s > %(levelname)s: %(message)s'
   global IS_SETUP
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
         import dbe
      log_fatal_exception()

   mylog = getLogger('LogStart')
   mylog.setLevel(level)
   mylog.info('\n{0:*^80}'.format(' ##$ LOGGING STARTED '
              + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + ' $## '))


def getLogger(logname = None, modname = None, funname = None, level = logging.INFO, dbeDisabled = False):
   '''returns a logger with logname that will print to the temporary directory.
   If level is == logging.DEBUG it will automatically do post-exception logging, and go into
   dbe (unless dbeDisabled is set).  In this way, the operation of all my debugging can be
   set by a single variable.'''
   if IS_SETUP == False:
      setuplogger(level = level, dbeDisabled = dbeDisabled)

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

      log = getLogger('FATAL_EXCEPTION')
      log.critical(str(exctype) + '\n' + str(value) + '\n' + ''.join(traceback.format_tb(tb)))

   previous_except_hook = sys.excepthook
   sys.excepthook = except_hook

def get_prev_exception_str(E = None, tb = None):
    '''#TODO: NOT USEABLE
    convinience function for logging in the print output and such
    It doesn't look like it does a whole lot of good at the moment though...'''
    if E != None:
        out = ['Exception [{0}] Occured:'.format(E)]
    else:
        out = ['Exception Occured:']
    if tb == None:
        tb = sys.exc_info()[2]
    out += traceback.format_tb(tb)
    if E != None:
        out += ['Exception: ' + str(E)]
    return '\n'.join(out)

if __name__ == '__main__':
   log = getLogger(__name__, level = logging.DEBUG)
   log.info('working?')
   log.info('yes, seems to be working')

   log2 = getLogger(__name__)
   log2.info('still working?')

   log_fatal_exception()
   x = 1 / 0
