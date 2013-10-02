from __future__ import division

import sys, os

import inspect
import traceback

import pdb

def between(value, v_min, v_max):
    '''More useful than you mght think.
    Takes into account if v_min or v_max are None.
    If one of them is they are taken as -infinity or
    +infinity respectively.
    '''
    if v_min == None and v_max == None:
        raise ValueError
    if v_min == None:
        return value < v_max
    if v_max == None:
        return value > v_min
    return v_min < value < v_max




