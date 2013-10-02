'''
Extends on top of itertools additional functionality for lists, iterators,
and numpy arrays.

Note: Imports itertools namespace so can be used instead of itertools
'''
from itertools import *
import math

NUMPY = True
try:
    import _NUMPY_ as np
except ImportError:
    _NUMPY_ = False

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

def read_xrange(xrange_object):
    '''returns the xrange object's start, stop, and step'''
    start = xrange_object[0]
    if len(xrange_object) > 1:
       step = xrange_object[1] - xrange_object[0]
    else:
        step = 1
    stop = xrange_object[-1] + step
    return start, stop, step

class Xrange(object):
    ''' creates an xrange-like object that supports slicing and indexing.
    ex: a = Xrange(20)
    a.index(10)
    will work

    Also a[:5]
    will return another Xrange object with the specified attributes

    Also allows for the conversion from an existing xrange object.

    Note: Designed to work VERY fast.
    '''
    def __init__(self, *inputs):
        # allow inputs of xrange objects
        if len(inputs) == 1:
            test, = inputs
            if type(test) == xrange:
                self.xrange = test
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

        self.xrange = xrange(self.start, self.stop, self.step)

    def __iter__(self):
        return iter(self.xrange)

    def __getitem__(self, item):
        if type(item) is int:
            if item < 0:
                item += len(self)

            return self.xrange[item]

        if type(item) is slice:
            # get the indexes, and then convert to the number
            start, stop, step = item.start, item.stop, item.step
            start = start if start != None else 0 # convert start = None to start = 0
            if start < 0:
                start += start
            start = self[start]
            if start < 0: raise IndexError(item)
            step = (self.step if self.step != None else 1) * (step if step != None else 1)
            stop = stop if stop is not None else self.xrange[-1]
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
            self.xrange[index]
        except (IndexError, TypeError):
            raise error
        return index

    def __len__(self):
        return len(self.xrange)

def flatten(iterable):
    '''flatten an iterator of any depth'''
    iterable = iter2(iterable)
    for e in iterable:
        if hasattr(e, '__iter__'):
            iterable.insert(0, e)
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
        value = chain((firstval,), value)
    else:
        firstval = value[0]

    if hasattr(firstval, '__iter__'): # then it is a matrix!
        return 2, value
    else:
        return 1, value

def get_first(data):
     '''returns the first element wihtout upsetting an iterator.
     Handles non-iterators by just returning them.
    returns firstval, original_data'''
     if not hasattr(data, '__iter__'):
          return data, data

     if hasattr(data, 'next'): # if it is an itterator
          firstval = data.next()     # take a peek
          data = chain((firstval,), data)
          return firstval, data

     firstval = data[0]
     return firstval, data

''' These functions are all fast list lookups not supported by any module in
python. They use iterators and compressors to do things as fast as possible in
native python'''

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
    '''same as data_list.index(value), except with exception handling (returns
    -1). Also finds 'nan' values '''
    data_list = islice(data_list, start, None)
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
    except (ValueError, StopIteration): return - 1


'''Numpy only functions
These functions can only be used with numpy
'''
if _NUMPY_:
    def np_index_to_coords(index, shape):
        '''convert index to coordinates given the shape'''
        coords = []
        for i in xrange(1, len(shape)):
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

if __name__ == '__main__':
    ab = np.arange(0, 30000)
    ab.shape = (20, 20, 30000/(20*20))
    value = ab[7][12][0]
    print first_coords_et(ab, value)

    import unittest
    import random
    class XrangeTest(unittest.TestCase):
        def test_basic(self):
            for _n in xrange(1000):
                stop = int(random.uniform(500, 2000))
                div = int(random.uniform(40, 200))
                start = int(stop/div)
                step = int(random.uniform(1, 5))

                ray = range(start, stop, step)
                xray = Xrange(start, stop, step)
                self.assertEqual(len(ray), len(xray.xrange))


                self.assert_all_equal(ray[2:20:4], xray[2:20:4])
                self.assert_all_equal(ray[10:30], xray[10:30])

        def assert_all_equal(self, ray1, ray2):
            self.assertEqual(len(ray1), len(ray2))
            [self.assertEqual(ray1[n], ray2[n]) for n in xrange(len(ray1))]

    x = xrange(5, 21, 3)
    xx = Xrange(x)
    x5 = xx[:5]
    print list(x5)


#    import timeit
#    a = [1, [[[[[[[xrange(2,10)]]]]]]], [xrange(10,20),xrange(20,30),[[[[[[[[[xrange(30,40)]]]]], xrange(40,50)]]], [xrange(50,60), xrange(60,70)]]]]
#    for _n in xrange(100):
#        a = [[a]]
#    print list(flatten(a))
#    print list(flatten(a)) == range(1,70)
#    print list(consume(a)) == range(1,70)
#
#    input_str = 'l=[[1, 2, 3], [4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7]] * 10'
#    input_str = 'l=' + str(a) + '\n'
##    print timeit.Timer(
##        '[item for sublist in l for item in sublist]',
##        input_str
##    ).timeit(1000)
#    print timeit.Timer(
#        'list(flatten(l))',
#        input_str + str_flatten
#    ).repeat(5, 1000)
#
#    print timeit.Timer(
#        'list(consume(l))',
#        input_str + str_consume
#    ).repeat(5, 1000)
