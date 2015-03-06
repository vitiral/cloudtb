# -*- coding: utf-8 -*-
'''
Useful tools to inspect and work with dictionaries
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import itertools

try: import numpy as np
except ImportError: pass
from cloudtb import builtin
from cloudtb.builtin import zip
from six import iteritems


def depth(d, deep=0, isiter=False):
    '''Find the depth of a nested dictionary'''
    if not isinstance(d, dict) or not d:  # not a dict or an empty dict
        builtin.throw(TypeError) if isiter and \
            not builtin.isiter(d) else None
        return deep
    return max(depth(v, deep + 1, isiter) for k, v in iteritems(d))


def get_header(item, extra_levels=None, filler=''):
    '''Returns the header of a nested dictionary
    The header is a list of tuples detailing the structure of the dictionary
    Very useful in pandas'''
    levels = extra_levels
    if levels is None:
        levels = depth(item)
    keys = []
    for key, value in iteritems(item):
        if isinstance(value, dict):
            keys.extend((key,) + v for v in
                        get_header(value, levels - 1, filler))
        else:
            keys.append((key,))
    return keys


def getitem(dic, item):
    '''Dictionary item access with tuples'''
    for i in item:
        dic = dic[i]
    return dic


def popitem(dic, item):
    '''Dictionary item pop with tuples'''
    for i in itertools.islice(item, 0, len(item) - 1):
        dic = dic[i]
    return dic.pop(item[-1])


def setitem(dic, item, value):
    '''Dictionary item setting with tuples'''
    for i, k in enumerate(item):
        if i < len(item) - 1:
            if k not in dic:
                dic[k] = {}
            dic = dic[k]
        else:
            dic[k] = value
            break
    else:
        assert False
    return dic


def pack(data, default=builtin.nan, header=None, dtype=list, verify=False):
    '''Pack a list of dictionaries into a dictionary of lists

    Args:
        data (dict): list of dictionaries. Dictionaries can be nested
        default (optional): default value for missing data. Defaults to
            float('nan')
        header (dict or list, optional): either a dictionary or a list of
            tuples that represents the data format. Defaults to data[0]
        dtype (optional): default is list
            dtype has several possible values:
                list:           (default) output as python lists
                numpy dtype:    all values have same numpy dtype
                dict of types:  must match header, select the dtype of each item
            When dtype is not list, numpy arrays will be outputed instead of
            lists for all values except for str and bytes types
        verify (bool, optional): if True, ValueError will be raised if data
            is wrong type. If False, default will be used instead. Defaults to
            False

            Notes:
                Ignored for dtype==list

    Returns:
        dict: a dictionary of the packed lists / arrays
            Missing values will == default

    >>> print('hi')
    hi
    '''
    if header is None and isinstance(dtype, dict):
        raise ValueError("Must include header for non list dtypes")
    header = get_header(data[0])
    packed = type(data[0])()  # preserve special types, like OrderedDicts

    # Construct format of output dictionary
    if dtype == list or isinstance(dtype, (str, bytes)):
        for key in header:
            setitem(packed, key, list(itertools.repeat(default, len(data))))
    elif not isinstance(dtype, dict):
        for key in header:
            setitem(packed, key, np.empty(len(data), dtype=dtype))
    else:
        for key in header:
            dt = getitem(dtype, key)
            if dt in {str, bytes}:
                setitem(packed, key, list(itertools.repeat(dt(), len(data))))
            else:
                setitem(packed, key, np.empty(len(data), dtype=dt))

    # store values
    if verify:
        for n, record in enumerate(data):
            for index in header:
                v = builtin.catch(KeyError, default, getitem, record, index)
                item = getitem(packed, index)
                try: item[n] = v
                except ValueError: item[n] = default
    else:
        for n, record in enumerate(data):
            for index in header:
                v = builtin.catch(KeyError, default, getitem, record, index)
                item = getitem(packed, index)
                item[n] = v
    return packed


def flatten(data, start=()):
    '''Flattens a dictionary so that the keys are all tuples of keys'''
    flat = type(data)()
    for key, value in iteritems(data):
        if isinstance(value, dict):
            flat.update(flatten(value, start=start + (key,)))
        else:
            flat[start + (key,)] = value
    return flat


def fill_keys(data, filler=None):
    '''Makes all dictionary keys tuples of the same length'''
    keys, values = zip(*data.items())
    # convert all keys to tuples
    keys = tuple(key if isinstance(key, tuple) else (key,) for key in keys)
    maxlen = max(map(len, keys))
    return type(data)({key + ((filler,) * (maxlen - len(key))): value for
                       (key, value) in zip(keys, values)})


def update(todict, fromdict, keys=None):
    '''Copy only keys from one dictionary to another

    keys=None is equivalent to todict.update(fromdict)
    '''
    todict.update(fromdict if keys is None else
                  {key: fromdict[key] for key in keys})


def remove(obj, keys, check=True):
    '''remove unwanted keys
    Arguments:
        obj -- object on which keys should be removed
        keys -- iterator of keys to remove
        check -- whether to check whether keys exist
        '''
    if check:
        builtin.consume(map(obj.pop, keys))
    else:
        builtin.consume(map(obj.pop, keys, itertools.repeat(None)))
