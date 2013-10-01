# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 16:17:25 2011

@author: Berg_Garrett
"""
import sys
import threading

class KThread(threading.Thread):
    """A subclass of threading.Thread, with a kill()
    method.  Will run a little slower  from Connelly Barnes, 
    http://mail.python.org/pipermail/python-list/2004-May/896157.html"""
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        
    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run      # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
          return self.localtrace
        else:
          return None

    def localtrace(self, frame, why, arg):
        if self.killed:
          if why == 'line':
            raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
        
        
if __name__ == '__main__':
    from time import sleep
    def run_ever():
        while True:
            print 'still running'
            sleep(.2)
    
    a = KThread(target = run_ever)
    a.start()
    print 'is_alive', a.is_alive()
    raw_input('PRESS ENTER TO KILL')
    a.kill()
    print 'KILLED'
    print 'is_alive', a.is_alive()
    for n in range(10):
        sleep(float(n)/10)
        print 'is_alive', a.is_alive()