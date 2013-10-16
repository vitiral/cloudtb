#!/usr/bin/python
# -*- coding: utf-8 -*-
#    The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    https://github.com/cloudformdesign/cloudtb
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT
'''
Extends on top of itertools additional functionality for lists, iterators,
and numpy arrays.

Note: Imports itertools namespace so can be used instead of itertools
'''
import itertools as itools
import math
import sys

VERSION = sys.version_info.major
if VERSION == 2:
    range = xrange

NUMPY = True
try:
    import _NUMPY_ as np
except ImportError:
    _NUMPY_ = False

import classtools

class biter(object):
    '''Takes in an object that is iterable.  Allows for the following method
    calls (that should be built into iterators anyway...)
    calls:
        - append - appends another iterable onto the iterator.
        - insert - only accepts inserting at the 0 place, inserts an iterable
            before other iterables.
        - adding.  an biter object can be added to another object that is
            iterable.  i.e. biter + iter (not iter + biter).  It's best to make
            all objects biter objects to avoid syntax errors.  :D
        - getitem (biter[1:3:4] syntax) including slicing and
            looking up referencing
        - next - standard way to deal with iterators

    note:
        biter[n] is the same as:
        for n in biter:
            pass
        or
        next(itools.itools.islice(biter, item))
        
    Usage:
        # want to extend my iterator
        myiter = biter(myiter)
        bi2 = biter(range(100)) # use xrange in python2
        myiter = myiter + bi2
        # ... other stuff
        
        # now I only want every 5th element
        myiter = myiter[::5]
        
        # ... other stuff
        # Now I just want the 20th element (note: removes elements before.
                # if you want to keep these elements use soliditer)
        el20 = myiter[20]
        
        
    Note: if you need to iterate directly, pull out the iter with
        myiter = iter(biter)
    this will use all c code and be super fast
    '''
    def __init__(self, iterable):
        self._iter = iter(iterable)
        self.solid_iter = None

    def append(self, value):
        self._iter = itools.chain(self._iter, (value,))
    
    def insert(self, position, value):
        if position not in (0, -1):
            raise ValueError("can only insert in front or back")
        if position == 0:
            self._iter = itools.chain((value,), self._iter)
        elif position == -1:
            self.append(value)
        else:
            assert(0)
        
    def extend(self, iterable):
        self._iter = itools.chain(self._iter, iterable)

    def front_extend(self, iterable):
        '''extends in front of the iterator'''
        self._iter = itools.chain(iterable, self._iter)

    def __add__(self, iterable):
        self._iter = itools.chain(self._iter, iterable)
        return self._iter

    def __next__(self):
        return next(self._iter)
        
    def next(self):
        return next(self._iter)
        
    def __iter__(self):
        return self

    def __getitem__(self, item):
        if type(item) == int:
            if item < 0:
                raise IndexError('Cannot address biter with '
                    'negative index: ' + repr(item))
            return next(itools.islice(self._iter, item, item + 1))

        if type(item) == slice:
            # get the indexes, and then convert to the number
            self._iter = itools.islice(self._iter, item.start,
                    item.stop, item.step)
            return self._iter

    def index(self, value, start = 0, stop = None):
        ind = first_index_et(self._iter, value)
        if ind == -1:
            raise IndexError("Could not find Index: {0}".format(value))
        return ind

from errors import RequestError

class soliditer(object):
    '''
    I have tested this fairly extensively and it should work on python 2 and 3.
    I don't know how many times I've been given a piece of data and not 
    known whether it is an iterator, list, xrange... whatever. I've wanted 
    to do things do it like look ahead by 10 indexes, but there was never a 
    convienient way to do that. Well, now there is!    
    
    creates a "solid iterable" that has lookahead functionality,
    but advancing the index still deletes data.
    Use the biter class if you have all iterators
    This function is intended to work with iterators as chunks,
    it is pure python (would like to write it in c soon) so it is
    not as fast as biter.

    Inputs:
        iterator, default_buf, request_extend_muliply, slicetype

    iterator: the first iterator soliditer is based on. Can be extended with
        extend

    default_buf: the default buffer size kept on hand
    request_extend_multiply: if a user makes a request for data, this extends
        this much times as far. Default is 5
    request_soft_limit: places a soft limit on the request for more data.
        default is 1000
    request_hard_limit: raises an RequestError error if the request for more
        data goes above this value. Default is None (no limit)
    slicetype: default type returned on slices is a tuple. For list use
        slicetype = list. For numpy, slicetype = np.array, etc.

    USAGE:
        myiter = iter(range(1000)) # an iterator you can't peek into
        siter = soliditer(myiter)
        v = siter[30]   # peek in and see
        ...             # do something with v or more with siter
        s = siter[:30]  # take a look at whole slice (does not consume)
        ... do some stuff
        s.consume(30)   # dumps the data that we were looking at.

    In situations where you need speed, you will want to do it in the "chunkwise" format.
    Using next(siter) is extremely slow compared to standard iterators --
    although obviusly if you don't care about speed you can feel free to.

    If you are ever DONE with soliditer and just want access to a high speed
    iterable, use soliditer.iterize -- doing so sets the internal variable
    self._been_iterized = True, which will raise an assertion error if you try
    to use soliditer again (don't, it's a bad idea!)

    Note:
    Watch out on using too many itertools.chains with hard data that you are
    re-integrating. You can create a memory leak!
    '''
    def __init__(self, iterable, default_buf = 10,
                request_extend_multiply = 1, request_soft_limit = 1000,
                request_hard_limit = None, slicetype = tuple):
        self._been_iterized = False
        self.__next__ = self.next

        self._databuf = []
        self._iterbuf = []
        self.default_buf = default_buf
        self.request_extend_multiply = request_extend_multiply
        self.request_soft_limit = request_soft_limit
        self.request_hard_limit = request_hard_limit
        self.slicetype = slicetype
        self.extend(iterable)

    def buffer_size(self):
        return len(self._databuf)

    def next(self):
        assert(not self._been_iterized)
        try:
            return self._databuf.pop(0)
        except IndexError:
            self.internal_extend(1, self.default_buf)
            if self.buffer_size() == 0:
                raise StopIteration

    def __iter__(self):
        return self

    def iterize(self):
        '''return the high speed iterator built through
        iterbuff and self._databuf. NOT RECOMMENDED to use soliditer
        and the output from iterize simultaniously (they will affect
        eachother)'''
        self._been_iterized = True
        return itools.chain(self._databuf, *self._iterbuf)

    def front_extend(self, iterable):
        '''adds data onto the front'''
        assert(not self._been_iterized)
        self._databuf = list(iterable) + self._databuf
    
    def extend(self, iterable):
        '''adds data onto the end'''
        assert(not self._been_iterized)
        self._iterbuf.append(iter(iterable))

    def append(self, item):
        assert(not self._been_iterized)
        self.extend((item,))
    
    def insert(self, index, item):
        assert(not self._been_iterized)
        self.internal_extend(index)
        self._databuf.insert(index, item)

    def internal_extend(self, need_length, want_length = None):
        '''consume one iter at a time until at correct length.
        return True if operation succeeds,
        False if it fails
        min_len is the minimum needed (not ammendable by soft limit)
        By default all is needed (min_len = None)
        '''
        assert(not self._been_iterized)
        if need_length < self.default_buf:
            need_length = self.default_buf

        hlimit = self.request_hard_limit
        needed = need_length - self.buffer_size()
        wanted = needed if want_length == None else (
            want_length - self.buffer_size())
        want_length = want_length if want_length != None else need_length
        
        if hlimit != None and needed > hlimit:
            raise RequestError("extend higher than hard limit", needed)

        while wanted > 0:
            if len(self._iterbuf) == 0:
                return False
            it = self._iterbuf[0]
            sliced = itools.islice(it, 0, need_length)
            self._databuf.extend(sliced)
            iter_done, it = isdone(it)
            self._iterbuf[0] = it
            bufsize = self.buffer_size()
            wanted = want_length - bufsize
            needed = need_length - bufsize
            if iter_done:
                self._iterbuf.pop(0)
            if needed > 0 and not self._iterbuf:
                raise IndexError("Index outside of existing extend")
            elif wanted > 0 and not self._iterbuf:
                # You can't always get what you want... but if you try 
                # sometimes, you just might find.... YOU GET WHAT YOU NEED!
                break
        return True

    def consume(self, n):
        assert(not self._been_iterized)
        '''removes the first n variables.'''
        self.internal_extend(n)
        del self._databuf[:n]

    def __getitem__(self, item):
        '''
        neither slices nor indexes consume the iterator'''
        assert(not self._been_iterized)
        if type(item) == slice:
            return self.slicetype(solidslice(self, item, consume = False))
        elif type(item) == int:
            self.internal_extend(item + 1)
            return self._databuf[item]
        else:
            raise TypeError("can only request slices or indexes")

    def index(self, value, *args):
        try:
            return self._databuf.index(value, *args)
        except ValueError:
            start = self.buffer_size()
            # extend buffer, try again.
            self.internal_extend(1, request_length = self.default_buf + start)
            # syntax stuff is pretty odd for index. It is [start], stop            
            if len(args) == 2:
                return self.index(value, start, args[1])
            else:
                # for this one, start actually == stop
                return self.index(value, start)

class solidslice(object):
    '''object for handling slicing in soliditer
    default is for slices to act like iterator (consuming data)
    set consume = False to change behavior'''
    def __init__(self, soliditer, start, *args, **kwargs):
        con = 'consume'
        if con in kwargs:
            self.consume = kwargs[con]
        else:
            self.consume = False
        self.__next__ = next
        if type(start) == slice:
            args = start
        else:
            args = (start,) + args
        myslice = classtools.slice_synatx(args)
        classtools.iterable_slice_error_check(*myslice)
        self.start, self.stop, self.step = myslice
        self.soliditer = soliditer
        self.__started = False
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        start, stop, step = self.start, self.stop, self.step
        if not self.__started:
            out = self.soliditer[start]
            if self.consume:
                self.soliditer.consume(start)
            self.index += start
            self.__started = True
            return out

        if self.stop != None and self.index + step >= self.stop:
            raise StopIteration

        getindex = step
        if not self.consume:
            getindex += self.index
        try:
            out = self.soliditer[getindex]
        except IndexError:
            raise StopIteration
        finally:
            self.index += step
            if self.consume:
                self.soliditer.consume(step)
        return out

def isdone(iterator):
    '''tells you whether the iterator is out if items without harming it.
    returns the new rebuilt iterable
    returns isdone, iterator'''
    try:
        value = next(iterator)
        return False, itools.chain((value,), iterator)
    except StopIteration:
        return True, iterator

if VERSION == 3:
    def read_xrange(xrange_object):
        '''returns the xrange object's start, stop, and step'''
        start = xrange_object[0]
        if len(xrange_object) > 1:
           step = xrange_object[1] - xrange_object[0]
        else:
            step = 1
        stop = xrange_object[-1] + step
        return start, stop, step

class brange(object):
    ''' "better range"
    creates an xrange-like object that supports slicing and indexing.
    ex: a = Xrange(20)
    a.index(10)
    will work

    Also a[:5]
    will return another Xrange object with the specified attributes

    Also allows for the conversion from an existing xrange object.

    Note: Designed to work VERY fast.
    Note: outdated in python3, range does these things. Automatically
    just returns a range
    '''
    def __init__(self, *inputs):
        if VERSION == 3:
            return range(*inputs)
        # allow inputs of xrange objects
        if len(inputs) == 1:
            test, = inputs
            if type(test) == xrange:
                self.range = test
                self.start, self.stop, self.step = read_xrange(test)
                return

        # or create one from start, stop, step
        self.start, self.step = 0, None
        if len(inputs) == 1:
            self.stop, = inputs
        elif len(inputs) == 2:
            self.start, self.stop = inputs
        elif len(inputs) == 3:
            self.start, self.stop, self.step = inputs
        else:
            raise ValueError(inputs)

        self.range = range(self.start, self.stop, self.step)

    def __iter__(self):
        return iter(self.range)

    def __len__(self):
        return len(self.range)

    def __getitem__(self, item):
        if type(item) is int:
            if item < 0:
                item += len(self)

            return self.range[item]

        if type(item) is slice:
            # get the indexes, and then convert to the number
            start, stop, step = item.start, item.stop, item.step
            start = start if start != None else 0 # convert start = None to start = 0
            if start < 0:
                start += start
            start = self[start]
            if start < 0: raise IndexError(item)
            step = (self.step if self.step != None else 1) * (step if step != None else 1)
            stop = stop if stop is not None else self.range[-1]
            if stop < 0:
                stop += stop

            stop = self[stop]
            stop = stop

            if stop > self.stop:
                raise IndexError
            if start < self.start:
                raise IndexError
            return Xrange(start, stop, step)

    def index(self, value):
        error = ValueError('object.index({0}): {0} not in object'.format(value))
        index = (value - self.start)/self.step
        if index % 1 != 0:
            raise error
        index = int(index)

        try:
            self.range[index]
        except (IndexError, TypeError):
            raise error
        return index

def flatten(iterable):
    '''flatten an iterator of any depth'''
    iterable = biter(iterable)
    for e in iterable:
        if hasattr(e, '__iter__'):
            iterable.front_extend(e)
        else:
            yield e

def find_depth(value):
    '''
    IMPORTANT: make SURE you call like:
        depth, iterable = find_depth(iterable)
    your starting iterable may be changed!

    returns the depth of the array
    0 : strings, integers, floats, etc.
    : vectors (1d)
    2 : matrixies (2d)
    etc
    Assumes every element has same depth (dives into the 0th element)
    '''
    if not hasattr(value, '__iter__'):
        return 0, value

    if hasattr(value, 'next'): # if it is an itterator
        firstval = value.next()     # take a peek
        value = itools.chain((firstval,), value)
    else:
        firstval = value[0]

    if hasattr(firstval, '__iter__'): # then it is a matrix!
        return 2, value
    else:
        return 1, value

def bslice(data, *args, **kwargs):
    '''returns an iterator that can slice backwards.
    IMPORTANT: uses the data's __getitem__ method. Doesn't work on
    "true" iterators'''
    # After thinking about it for a second I realized this is REALLY easy,
    # still worth having an iterating slice though.
    return (data[n] for n in xrange(*args, **kwargs))
    
def get_first(data):
     '''returns the first element wihtout upsetting an iterator.
     Handles non-iterators by just returning them.
    returns firstval, original_data'''
     if not hasattr(data, '__iter__'):
          return data, data

     if hasattr(data, 'next'): # if it is an itterator
          firstval = data.next()     # take a peek
          data = itools.chain((firstval,), data)
          return firstval, data

     firstval = data[0]
     return firstval, data

''' These functions are all fast list lookups not supported by any module in
python. They use iterators and compressors to do things as fast as possible in
native python'''
def is_all_type(data_list, dtype, start = 0, stop = None, step = 1):
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        next((n for n in data_list if type(n) != dtype))
        return False
    except StopIteration:
        return True

def special_figt(data_list, value, start = 0, stop = None, step = 1):
    index = first_index_gt(data_list, value, start, stop, step)
    if data_list[index + 1] > value:
        return index + start
    else:
        return None

def first_index_gt(data_list, value, start = 0, stop = None, step = 1):
    '''return the first index greater than value from a given list like object'''
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] > value)
        return index + start
    except StopIteration: return None

def first_index_gtet(data_list, value, start = 0, stop = None, step = 1):
    '''return the first index greater than value from a given list like object'''
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] >= value)
        return index + start
    except StopIteration: return None

def first_index_lt(data_list, value, start = 0, stop = None, step = 1):
    '''return the first index less than value from a given list like object'''
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] < value)
        return index + start
    except StopIteration: return None

def first_index_ne(data_list, value, start = 0, stop = None, step = 1):
    '''returns first index not equal to the value from list'''
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] != value)
        return index + start
    except StopIteration: return None

def first_index_et(data_list, value, start = 0, stop = None, step = 1):
    '''same as data_list.index(value), except with exception handling (returns
    -1). Also finds 'nan' values '''
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        if type(value) == float and math.isnan(value):
            floats = set(float,)
            if _NUMPY_:
                floats.update((np.float64, np.float32, np.float96))
            isnan = math.isnan
            return next(data[0] for data in enumerate(data_list)
              if (type(data[1]) in floats
              and isnan(data[1])))  + start
        else:
            return next(data[0] for data in
            enumerate(data_list) if data[1] == value) + start
    except (ValueError, StopIteration): return None

def first_index_in(data_list, in_set, start = 0, stop = None, step = 1):
    '''finds the first index that is in a given set of any iterator'''
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if 
            data[1] in in_set)
        return index + start
    except StopIteration: return None

def first_index_nin(data_list, notin_set, start = 0, stop = None, step = 1):
    '''finds the first index that is not in a given set of any iterator'''
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if 
            data[1] not in notin_set)
        return index + start
    except StopIteration: return None

def first_index_is(data_list, identity, start = 0, stop = None, step = 1):
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if 
            data[1] is identity)
        return index + start
    except StopIteration: return None

def first_index_nis(data_list, identity, start = 0, stop = None, step = 1):
    if step == None or step > 0:
        data_list = itools.islice(data_list, start, stop, step)
    else:
        data_list = bslice(data_list, start, stop, step)
    try:
        index = next(data[0] for data in enumerate(data_list) if 
            data[1] is not identity)
        return index + start
    except StopIteration: return None

'''Numpy only functions
These functions can only be used with numpy
'''
if _NUMPY_:
    def np_index_to_coords(index, shape):
        '''convert index to coordinates given the shape'''
        coords = []
        for i in range(1, len(shape)):
            divisor = int(np.product(shape[i:]))
            value = index//divisor
            coords.append(value)
            index -= value * divisor
        coords.append(index)
        return tuple(coords)

    def np_first_coords_et(data_matrix, value, start = 0):
        '''the first coordinates that are equal to the value'''
        index = first_index_et(data_matrix.flatten(), value, start)
        shape = data_matrix.shape
        return np_index_to_coords(index, shape)

    def np_sort_together(data):
        '''sorts a multi row array by keeping the rows together.
        Sorts only first row
        untested!
        '''
        x, y = data
        ndx = np.argsort(data[0])
        data = np.dstack([n[ndx] for n in data])
        data = np.transpose(data)
        return data

    def np_columnize_rows(data):
        '''This does something similar to a Transpose, but on any set of data'''
        return np.fliplr(np.rot90(data, k=-1))

    def np_std_repeat(data, times):
        '''repeats an array of data several times.
        np_std_repeat([1,2,3], 2)
        >>> [[1,2,3],[1,2,3]]'''
        return np.tile(data, (times, 1))

'''
    i2 = biter(range(10)) + biter(range(30))
    print 'Testing i2 biter(range(10)) + biter(range(30))'
    print 'next', next(i2)

    print 'index 10 then 2', i2[10], i2[2]
    print 'reset'
    i2 = biter(range(10)) + biter(range(30))
    print 'slice [0:5:]', [n for n in i2[0:5:]]

    print 'reset and adding two with same slice'
    i2 = biter(range(10)) + biter(range(30))
    i3 = biter(range(10)) + biter(range(30))
    i2, i3 = i2[0:5:], i3[0:5:]
    print [n for n in (i2 + i3)]
    '''

if __name__ == '__main__':
    pass
    import pdb
    pdb.set_trace()
    mylist = [range(10), [range(20), range(15)]]
    print tuple(flatten(mylist))
#    import dbe
#    import pdb
#
#    car = '>>>'
#
#    print('''
#    >>>
#    si = soliditer(iter(range(300)))
#    si.extend(range(1250, 1350))
#    si.extend(range(-200, 0))
#    si.insert(5, 'inserted')
#    si.append('appended')
#    >>>
#    ''')
#    si = soliditer(iter(range(300)))
#    si.extend(range(1250, 1350))
#    si.extend(range(-200, 0))
#    si.insert(5, 'inserted')
#    si.append('appended')
#
#    print (car, "si[10], si[5], si[105]")
#    print (si[10], si[5], si[105])
#    print(car, "list(si[0:20:3])")
#    print(list(si[0:20:3]))
#    print (car, "si[10], si[5], si[105]")
#    print (si[10], si[5], si[105])
#    print "note len data buffer:", len(si._databuf)
#    print "index of inserted", si.index('inserted')
#    print si.index('appended')
#    print 'consume a bunch of data', si.consume(500)
#    print 'print out everything'
#    print si[0:]
#    print 'and do some basic operations'
#    print "si[1], si[10], si.index('appended'), si.index(-58)"
#    print si[1], si[10], si.index('appended'), si.index(-58)
#
#    print '\n\nreseting'
#    si = soliditer(iter(range(300)))
#    si.extend(range(1250, 1350))
#    si.extend(range(-200, 0))
#    si.insert(5, 'inserted')
#    si.append('appended')
#
#    print 'iterizing'
#    it = si.iterize()
#    print 'overriding si._been_iterized for demonstration, otherwise this casues an Assertion Error'
#    si._been_iterized = False
#    print 'si[4]', si[4]
#    print 'Note how it stores only some data'
#    print 'si._databuf', si._databuf
#    print "list(it)"
#    print list(it)
#    print
#
#    print 'list(si) -- note bad idea they are not the same. Only the data was kept'
#    print (list(si))