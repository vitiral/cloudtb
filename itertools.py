'''
Extends on top of itertools additional functionality.
Note: Imports itertools namespace so can be used instead of itertools

'''

from itertools import *
import math

NUMPY = True
try:
    import numpy as np
except ImportError:
    NUMPY = False
    
class iter2(object):
    '''Takes in an object that is iterable.  Allows for the following method
    calls (that should be built into iterators anyway...)
    calls:
        - append - appends another iterable onto the iterator.
        - insert - only accepts inserting at the 0 place, inserts an iterable
         before other iterables.
        - adding.  an iter2 object can be added to another object that is
         iterable.  i.e. iter2 + iter (not iter + iter2).  It's best to make
         all objects iter2 objects to avoid syntax errors.  :D
    '''
    def __init__(self, iterable):
        self._iter = iter(iterable)
    
    def append(self, iterable):
        self._iter = chain(self._iter, iter(iterable))
        
    def insert(self, place, iterable):
        if place != 0:
            raise ValueError('Can only insert at index of 0')
        self._iter = chain(iter(iterable), self._iter)
    
    def __add__(self, iterable):
        return chain(self._iter, iter(iterable))
        
    def next(self):
        return self._iter.next()
    
    def __iter__(self):
        return self

def flatten(iterable):
    '''flatten an iterator of any depth'''
    iterable = iter2(iterable)
    for e in iterable:
        if hasattr(e, '__iter__'):
            iterable.insert(0, e)
        else:
            yield e

def columnize_rows(data):
    '''This does something similar to a Transpose, but on any set of data'''
    return np.fliplr(np.rot90(data, k=-1))
    
def find_depth(value):
     '''returns the depth of the array
     0 : strings, integers, floats, etc.
     1 : vectors (1d)
     2 : matrixies (2d)
     etc
     '''
     if not hasattr(value, '__iter__'):
          return 0, value
          
     if hasattr(value, 'next'): # if it is an itterator
          firstval = value.next()     # take a peek
          value = chain((firstval,), value)
     else: 
          firstval = value[0]

     if hasattr(firstval, '__iter__'): # then it is a matrix!
          return 2, value
     else:
          return 1, value
          
def get_first(value):
     '''returns the first element wihtout upsetting an iterator
     (must re-assign iterator to the second return value)'''
     if not hasattr(value, '__iter__'):
          return value, value
          
     if hasattr(value, 'next'): # if it is an itterator
          firstval = value.next()     # take a peek
          value = chain((firstval,), value)
          return firstval, value
     
     firstval = value[0]
     return firstval, value
          
def replace_all(input_string, replacements):
     '''replace the elements of the string defined in the iterable tuple.
     ex: ((' ', ''), ('_', '')) would get rid of spaces and underscores'''
     for before, after in replacements:
          input_string = input_string.replace(before, after)
     return input_string

def special_figt(data_list, value, start = 0):
    index = first_index_gt(data_list, value, start)
    if data_list[index + 1] > value: 
        return index + start
    else:
        return - 1

def first_index_gt(data_list, value, start = 0):
    '''return the first index greater than value from a given list like object'''
    data_list = islice(data_list, start, None)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] > value)
        return index + start
    except StopIteration: return - 1

def first_index_gtet(data_list, value, start = 0):
    '''return the first index greater than value from a given list like object'''
    data_list = islice(data_list, start, None)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] >= value)
        return index + start
    except StopIteration: return - 1

def first_index_lt(data_list, value, start = 0):
    '''return the first index less than value from a given list like object'''
    data_list = islice(data_list, start, None)    
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] < value)
        return index + start
    except StopIteration: return - 1

def first_index_ne(data_list, value, start = 0):
    '''returns first index not equal to the value from list'''
    data_list = islice(data_list, start, None)    
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] != value)
        return index + start
    except StopIteration: return - 1

def first_index_et(data_list, value, start = 0):
    '''same as data_list.index(value), except with exception handling
    Also finds 'nan' values '''
    data_list = islice(data_list, start, None)    
    try:
        if type(value) == float and math.isnan(value):
            floats = float,
            if NUMPY:
                floats = floats + (np.float64, np.float32, np.float96)
            isnan = math.isnan
            return next(data[0] for data in enumerate(data_list)
              if (type(data[1]) in floats
              and isnan(data[1])))  + start
        else:
            return next(data[0] for data in 
            enumerate(data_list) if data[1] == value) + start
    except (ValueError, StopIteration): return - 1

def index_to_coords(index, shape):
    '''convert index to coordinates given the shape'''
    coords = []
    for i in xrange(1, len(shape)):
        divisor = int(np.product(shape[i:]))
        value = index//divisor
        coords.append(value)
        index -= value * divisor
    coords.append(index)
    return tuple(coords)
    
def first_coords_et(data_matrix, value, start = 0):
    '''the first coordinates that are equal to the value'''
    index = first_index_et(data_matrix.flatten(), value, start)
    shape = data_matrix.shape
    return index_to_coords(index, shape)