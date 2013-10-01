from __future__ import division

import sys, os

import inspect
import traceback



import pdb

def between(value, v_min, v_max):
    if v_min == None and v_max == None:
        raise ValueError

    if v_min == None:
        return value < v_max

    if v_max == None:
        return value > v_min

    return v_min < value < v_max

def consume(iterable):
    '''
    I really don't know what this is supposed to be for...
    '''
    iterable = iter(iterable)

    while 1:
        try:
            item = iterable.next()
        except StopIteration:
            break

        try:
            data = iter(item)
            iterable = itertools.chain(data, iterable)
        except:
            yield item

str_consume = """
import itertools

def consume(iterable):
    iterable = iter(iterable)

    while 1:
        try:
            item = iterable.next()
        except StopIteration:
            break

        try:
            data = iter(item)
            iterable = itertools.chain(data, iterable)
        except:
            yield item
"""






