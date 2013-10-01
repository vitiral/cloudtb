# -*- coding: utf-8 -*-
"""
Created on Thu Mar 01 10:04:35 2012

@author: Berg_Garrett
"""

import code
from threading import Thread

class Interact(Thread):
    def __init__(self, local):
        self.local = local
        Thread.__init__(self)
        
    def run(self):
        code.interact(local = self.local)
        
def interact(local):
    th = Interact(local)
    th.start()