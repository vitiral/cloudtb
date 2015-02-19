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


def setitem(dic, item, value):
    '''Dictionary item setting with tuples'''
    for k, i in enumerate(item):
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


def unpack(data, header=None):
    '''Unpacks a list of dictionaries into a dictionary of lists
    according to the header'''
    if header is None:
        header = get_header(data[0])
    out = {key: [] for key in header}
    for d in data:
        for h in header:
            out[h].append(getitem(d, h))
    return out


def flatten(data, start=()):
    '''Flattens a dictionary so that the keys are all tuples of keys'''
    flat = {}
    for key, value in data.items():
        if isinstance(value, dict):
            flat.update(flatten(value, start=start + (key,)))
        else:
            flat[start + (key,)] = value
    return flat


def fill_dict(data, filler):
    '''Makes all dictionary keys tuples of the same length'''
    keys, values = zip(*data.items())
    # convert all keys to tuples
    keys = tuple(key if isinstance(key, tuple) else (key,) for key in keys)
    maxlen = max(map(len, keys))
    return {key + ((filler,) * (maxlen - len(key))): value for (key, value)
            in zip(keys, values)}


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
