# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:07:58 2012

@author: Berg_Garrett
"""
from __future__ import division

def assign_to_self(self, assign_variables):
     if 'self' in assign_variables:
          del assign_variables['self']
     for name, value in assign_variables.iteritems():
          #print name, value
          exec('self.{0} = value'.format(name))
          #print eval('self.{0}'.format(name))







