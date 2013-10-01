#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
  Any importing module will go to pdb on exception rather than going to nothing.  Title stands for
  DeBug on Exception, naming convention similar to pdb (python debugger)

  Thanks to: Lennart Regebro at http://stackoverflow.com/questions/5515940/trying-to-implement-import-debug-mode-module/5517696#5517696
'''

import sys, pdb

def except_hook(exctype, value, traceback):
    if previous_except_hook:
        previous_except_hook(exctype, value, traceback)
    pdb.post_mortem(traceback)

previous_except_hook = sys.excepthook
sys.excepthook = except_hook
