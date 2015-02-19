#!/usr/bin/python3
'''
Useful tools to inspect and work with dictionaries
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''

import itertools

from cloudtb import builtin


def depth(d, deep=0):
    '''Find the depth of a nested dictionary'''
    if not isinstance(d, dict) or not d:
        return deep
    return max(depth(v, deep + 1) for k, v in d.items())


def get_header(item, extra_levels=None, filler=''):
    '''Returns the header of a nested dictionary
    The header is a list of tuples detailing the structure of the dictionary
    Very useful in pandas'''
    levels = extra_levels
    if levels is None:
        levels = depth(item)
    keys = []
    for key, value in item.items():
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


def unpack_dicts(data, header):
    '''Unpacks a list of dictionaries into a dictionary of lists
    according to the header'''
    out = {key: [] for key in header}
    for d in data:
        for h in header:
            out[h].append(getitem(d, h))
    return out


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
