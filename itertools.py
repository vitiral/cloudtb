'''
Extends on top of itertools additional functionality for lists, iterators,
and numpy arrays.

Note: Imports itertools namespace so can be used instead of itertools
'''
from itertools import *
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
        - getitem (iter2[1:3:4] syntax) including slicing and
            looking up referencing
        - next - standard way to deal with iterators

    In addition, if the variable lookahead = True (default) then using
    the index or iter2[item] notations will not exhaust the iterator. You
    can "look ahead" and then continue on, eventually getting to that value.

    '''
    def __init__(self, iterable, lookahead = True):
        self._iter = iter(iterable)
        self.lookahead = lookahead
        self.solid_iter = None

    def append(self, iterable):
        self._iter = chain(self._iter, iterable)

    def insert(self, place, iterable):
        if place != 0:
            raise ValueError('Can only insert at index of 0')
        self._iter = chain(iterable, self._iter)

    def __add__(self, iterable):
        self._iter = chain(self._iter, iterable)
        return self._iter

    def __next__(self):
        return self._iter.next()

    def __iter__(self):
        return self

    def __getitem__(self, item):
        if type(item) == int:
            if item < 0:
                raise IndexError('Cannot address iter2 with '
                    'negative index: ' + repr(item))
            if self.lookahead == False:
                return next(islice(self._iter, item))
            else:
                sl = islice_keep(self._iter, item)
                try:
                    out = next(sl)
                finally:

                    self._iter = chain(sl.construct_past(), self._iter)
                return out

        if type(item) == slice:
            # get the indexes, and then convert to the number
            start, stop, step = item.start, item.stop, item.step
            self._iter = itertools.islice(self._iter, item.start,
                    item.stop, item.step)
            return self._iter

    def index(self, value, start = 0, stop = None):
        ind = first_index_et(self._iter, value)
        if ind == -1:
            raise IndexError("Could not find Index: {0}".format(value))
        return ind

    def construct_past(self, past, future):
        pass

def isdone(iterator):
    '''tells you whether the iterator is out if items without harming it.
    returns the new rebuilt iterable
    returns isdone, iterator'''
    try:
        value = next(iterator)
    except StopIteration:
        return True, iterator
    return False, chain((value,), iterator)


class soliditer(object):
    '''creates a "solid iterable" that has lookahead functionality,
    but advancing the index still deletes data
    Made for the iter2 class -- use that.
    careful! data is in reverse order so that I can use pop as next (speeds things up)

    Ok, I think I may have screwed up a bit...
    what should happen is this should support slices, but have a "reserve" iter
    that it can always tap into and extend itself every step of the way.

    In fact... this should just replace iter2. Iter2 can be used as only for
    adding iterables. It's a bad idea to introduce (histories) solids into that mix. Just
    keep it with chain tools

    islice is still necessary though, but I need to pass solid_iter ITSELF as
    the iterator. That's where I screwed up.
    '''
    def __init__(self, iterable, length = None, default_len = 200,
                request_extend_multiply = 5):
        data = []
        self.append_iterable(iterable, length)
        self.__next__ = self.next
        self._future = []
        self.__next__ = self.next
        self.default_len = default_len

    def next(self):
        try:
            return data.pop(0)
        except IndexError:
            if not self.internal_extend(self.default_len):
                raise StopIteration

    def __len__(self):
        return len(self.data)

    def extend(self, iterable):
        '''adds data onto the end'''
        data._future.append(iterable)

    def internal_extend(self, to_length):
        '''consume one appended iter at a time
        until at correct length.
        return True if operation succeeds,
        False if it fails'''
        needed = to_length - len(self)
        while needed > 0:
            it = self.future[0]
            sliced = itertools.islice(it, 0, to_length)
            self.data.extend(sliced)
            done, it = isdone(it)
            needed = to_length - len(self)
            if done:
                self.future.pop(0)
            else:
                assert(needed == 0)

    def consume(self, n):
        '''removes the first n variables.'''
        self.internal_extend(n)
        del self.data[:n]

    def __getitem__(self, item):
        '''
        slices consume as if they were iterators (they are!)
        indexes don't consume.
        '''
        if type(item) == slice:
            return solidslice(self, slice)
        elif type(item) == int:
            self.internal_extend(item * self.request_extend_multiply)
            return self.data[int]
        else:
            raise TypeError("can only request slices or indexes")

    def __iter__(self):
        return self

class solidslice(object):
    def __init__(self, soliditer, start, *args):
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

    def __iter__(self):
        return self

    def next(self):
        start, stop, step = self.start, self.stop, self.step
        if not self.__started:
            out = self.soliditer[start]
            self.soliditer.consume(start)
            self.__started = True
            return out
        out = self.soliditer[step]
        self.soliditer.consume(step)
        return out

import classtools
class islice_keep(object):
    '''
    islice_keep(iterable, start, [stop[, step]])
    just like islice, but returns both the iterator and stores every element
    iterated into islice_keep.past
    if it encounters a StopIteration from the iterator, then the excess (before hand) is stored in
    islice_keep.extra and not appended to islice_keep.past
    islice_keep.past is an array of tupples -- each containing the history
    of one step. To regain the data use either itertools.chain(*islice_keep.past)
    or #TODO: I actually don't know a list concatenation tool...
    '''
    def __init__(self, iterable, *args):
        start, stop, step = classtools.slice_synatx(args)
        classtools.iterable_slice_error_check(start, stop, step)

        self._iter = iter(iterable)
        self.start, self.stop, self.step = start, stop, step
        self.past = []
        self.extra = None
        self._index = 0
        self.__started = False

    def construct_past(self):
        '''returns the current iterator of the past,
        including extra'''
        if self.extra:
            return chain(chain(*self.past), self.extra)
        else:
            return chain(*self.past)

    def __iter__(self):
        return self

    def __next__(self):
        start, stop, step = self.start, self.stop, self.step
        if not self.__started:
            out = self._advance(start+1)
            self.__started = True
            return out
        return self._advance(step)

    def next(self):
        return self.__next__()

    def _advance(self, amount):
        assert(amount > 0)
        self._index += amount
        if self.stop != None and self._index > self.stop:
            raise StopIteration

        prev = tuple((next(self._iter) for n in range(amount)))
        if len(prev) == 0 or len(prev) < amount:
            self.extra = prev
            raise IndexError("Call exceeded end of iterator. "
                "Result stored in islice.extra")
        self.past.append(prev)
        return prev[-1]

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
    Note: outdated in python3, range does these things.
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

from pprint import pprint
def print_full_isl(isl):
    print 'FULL ISLICE_KEEP'
    try:
        out = []
        for n in isl:
            out.append(n)
    except IndexError:
        print "ERROR: Got index error"
    except StopIteration:
        print "ERROR: Got StopIteration"
    print('OUTPUT', out)
    print(isl.past)
    print(isl.extra)

if __name__ == '__main__':
    import dbe
    a = range(100)
    b = islice_keep(a, 0, 70, 10)
    print_full_isl(b)
    c = islice_keep(a, 1, 10)
    print_full_isl(c)
    d = islice_keep(a, 1, 20, 3)
    print_full_isl(d)
    b = islice_keep(a, 0, None)
    print_full_isl(b)
    f = islice_keep(a, None, None, 3)
    print_full_isl(f)

    try:
        islice_keep(a, 5, 2, 2)
    except Exception as E:
        print(E)
    else: print('should have done something')


    '''
    i2 = iter2(range(10)) + iter2(range(30))
    print 'Testing i2 iter2(range(10)) + iter2(range(30))'
    print 'next', next(i2)

    print 'index 10 then 2', i2[10], i2[2]
    print 'reset'
    i2 = iter2(range(10)) + iter2(range(30))
    print 'slice [0:5:]', [n for n in i2[0:5:]]

    print 'reset and adding two with same slice'
    i2 = iter2(range(10)) + iter2(range(30))
    i3 = iter2(range(10)) + iter2(range(30))
    i2, i3 = i2[0:5:], i3[0:5:]
    print [n for n in (i2 + i3)]
    '''


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
