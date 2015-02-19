#!/usr/bin/python3
'''
Functions that should be builtin to python
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from enum import Enum
import imp


def importpath(name, path):
    module = imp.find_module(path)
    return imp.load_module(name, *module)


def enum(name, attrs=None):
    '''enum generator function
    Creates an Enum type. attrs can be: set, list, tuples or a dictionary.
    The behavior is as follows:
        - dictionaries and lists/tuples of the form
            [(name, key), (name2, key2), ...] will behave as expected.
            (dictionaries will have their items() method called
        - sets will be converted to zip(sorted(attrs), range(len(attrs)))
        - lists/tuples without embeded tuples will do the same without sorting

    Can be called in two forms:
        enum(name, attrs)
        OR
        enum(attrs)  # name will == 'enum'
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


def isiter(obj, exclude=(str, bytes, bytearray)):
    '''Returns True if object is an iterator.
    Returns False for str, bytes and bytearray objects
    by default'''
    return (False if isinstance(obj, exclude)
            else True if hasattr(obj, '__iter__')
            else False)


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