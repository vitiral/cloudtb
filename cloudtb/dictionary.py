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


def dict_depth(d, depth=0):
    '''Find the depth of a nested dictionary'''
    if not isinstance(d, dict) or not d:
        return depth
    return max(dict_depth(v, depth + 1) for k, v in d.items())


def get_header(item, extra_levels=None, filler=''):
    '''Returns the header of a nested dictionary
    The header is a list of tuples detailing the structure of the dictionary
    Very useful in pandas'''
    levels = extra_levels
    if levels is None:
        levels = dict_depth(item)
    keys = []
    for key, value in item.items():
        if isinstance(value, dict):
            keys.extend((key,) + v for v in
                        get_header(value, levels - 1, filler))
        else:
            keys.append((key,))
    return keys


def get_item(dic, item):
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
            out[h].append(get_item(d, h))
    return out
