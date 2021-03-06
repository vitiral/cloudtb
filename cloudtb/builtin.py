# -*- coding: utf-8 -*-
'''
Functions that should be builtin to python

Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys
import imp
import math
import itertools
import collections
from six.moves import zip

# Some standard functions and objects that should be builtin
nan = float('nan')
isnan = math.isnan
sizeof = sys.getsizeof

try:
    from enum import Enum

    def enum(name, attrs=None):
        '''enum generator function to create an Enum more dynamically.

        Can be called in two forms:
            enum(name, attrs)
            OR
            enum(attrs)  # name will == 'enum'

        Attrs:
            name (str): the name of the enum.
            attrs (set, list, or tuplles, optional)
                - dictionaries and lists/tuples of the form
                    [(name, key), (name2, key2), ...] will behave as expected.
                    (dictionaries will have their items() method called
                - sets will be converted to
                    zip(sorted(attrs), range(len(attrs)))
                - lists/tuples without embeded tuples will do the same
                    without sorting
                The "name" values have to all be strings (like in any enum)
        '''
        if attrs is None:
            # use default name, attrs becomes first argument
            name, attrs = 'enum', name
        if isinstance(attrs, dict):
            attrs = attrs.items()
        elif isinstance(attrs, set):
            attrs = zip(sorted(attrs), range(len(attrs)))
        elif not isinstance(attrs[0], (tuple, list)):
            attrs = zip(attrs, range(len(attrs)))
        return Enum(name, attrs)
except ImportError:
    pass  # python 2


def importpath(name, path):
    '''Import the path. Return the module'''
    module = imp.find_module(path)
    return imp.load_module(name, *module)


def isiter(obj, exclude=(str, bytes, bytearray)):
    '''Returns True if object is an iterator.

    Arguments:
        exclude (tuple, optional): types to exclude from "iter" type
            In most applications you want to know whether something is a
            list, typle, generator, numpy array, etc... a string or bytes
            type is considered a constant, not an iterator.
    '''
    return (False if isinstance(obj, exclude)
            else True if hasattr(obj, '__iter__')
            else False)


def remove_duplicates(data, sort=True):
    ''' Remove duplicates from the data (normally a list).
        The data must be sortable and have an equality operator
    '''
    if not data:
        return data
    if sort:
        data = sorted(data)
    out = [data[0]]
    for i, n in enumerate(data[1:]):
        if data[i] != n:
            out.append(n)
    return out


def encode(data, encoding="utf-8", errors="strict"):
    '''Always outputs bytes if possible'''
    if isinstance(data, (bytes, bytearray)):
        return bytes(data)
    elif hasattr(data, 'encode'):
        return data.encode(encoding, errors)
    elif hasattr(data, 'decode'):
        return decode(encode(data, encoding, errors), encoding, errors)
    else:
        raise TypeError("Cannot encode data: {}".format(data))


def decode(data, encoding="utf-8", errors="strict"):
    '''Always outputs str if possible'''
    if isinstance(data, str):
        return data
    elif hasattr(data, 'decode'):
        return data.decode(encoding, errors)
    elif hasattr(data, 'encode'):
        return encode(decode(data, encoding, errors), encoding, errors)
    else:
        raise TypeError("Cannot decode data: {}".format(data))


def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iterator, n, n), None)


def throw(exception):
    '''Raises an exception. Can be used inside compressions'''
    raise exception


def catch(exception, default, function, *args, **kwargs):
    '''Call a function with *args, **kwargs. On exception, return default'''
    try:
        return function(*args, **kwargs)
    except exception:
        return default


def raises(exception, function, *args, **kwargs):
    '''runs function with *args, **kwargs. Returns True if it raised exception
    '''
    try:
        function(*args, **kwargs)
        return False
    except exception:
        return True
