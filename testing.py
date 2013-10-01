#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
 * Summary :
 * 
 * Created on 2011-04-01
 * @author: garrett
'''

import pdb
from decorator_functions import IgnoreExceptions, standardErrCall, standardExceptionLog

def dev1():
   a = 'hello from testing'
   print a
   #v = 1 / 0
   #print v
   
   
   @IgnoreExceptions([Exception], -1, standardErrCall)
   @IgnoreExceptions([ZeroDivisionError])
   def divide(x):
      return 1.0 / x
   
   print divide
   print divide.__name__
   
   print divide(4)
   print divide(0)
   print divide('23')
   
   
   print 'hello'
   print 'hello'
   
   print 'hello'
   print 'hello'
   
   x = 343
   
   z = 23
   
   class mydatatype(object):
      def __init__(self, initdata = None):
         if inidata == None: self.initdata = []
         else: self.initdata = initdata
   
   
   from easy_log import getLogger
   
   log = getLogger(__name__)
   log.info('here')
   
   
   @IgnoreExceptions([ZeroDivisionError], None, standardExceptionLog(log))
   def divide2(x):
      return 1.0 / x
   
   print divide2(4)
   print divide2(0)
      
   from functions import special_figt
   print special_figt
   
   import traceback, os, sys
   def lala():
      print 'in lala'
      stack = traceback.extract_stack()
   
      print 'HERE', sys.exc_traceback
      fname = stack[-1][2]
      mname = ''.join(os.path.basename(stack[-1][0]).split('.')[:-1])
      print stack
      print stack[-1]
      print fname, mname
   
   def lalala():
      print 'in lalala'
      lala()
   
   lstr = 'I AM LONG.' * 100
   for n in range(1000):
      log.info(lstr)
   
   print 'done'
   

def cython_speedtest():
    import cfunctions
    import timeit
    import numpy as np
    setup_txt = '''import numpy as np
import functions, cfunctions
a = np.arange(3000, dtype = np.float)'''
    a = np.arange(3000, dtype = np.float)
    cfunctions.c_first_index_gt(a, 2500.0)
    print timeit.timeit('cfunctions.c_first_index_gt(a, 2500.0)', setup_txt, number = 1000)
    print timeit.timeit('functions.first_index_gt(a, 2500.0)', setup_txt, number = 1000)
    
    
if __name__ == '__main__':
    import dbe
    pass
    
