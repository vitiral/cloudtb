#!/usr/bin/python3
'''
Useful tools for working with the python library pandas
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
import pandas as pd
from cloudtb import dictionary


def _dataframe_dict(data, index=None, filler='', header=None):
    if isinstance(data, dict):
        try:
            if dictionary.depth(data, isiter=True) < 2:
                return data
        except TypeError:
            return data
    if isinstance(data, dict):
        header = resolve_header(header)
        if header is None:
            header = dictionary.get_header(data)
    else:
        header = resolve_header(header)
        if header is None:
            header = dictionary.get_header(data[0])
        data = dictionary.unpack(data, header)
        data = dictionary.flatten(data)
    data = dictionary.fill_keys(data, filler)
    return data


def dataframe_dict(data, index=None, filler='', header=None):
    '''General loader of dataframes from python objects. Can either be a
    dict of lists or a list of dicts.
    Header is detected automatically and will be multiindex if the dict
    is nested'''
    data = _dataframe_dict(data, index, filler, header)
    data = pd.DataFrame.from_dict(data)
    if index is not None:
        data.set_index(index, inplace=True)
        data.sort_index(inplace=True)
    return data


# Helper funcitons
def resolve_header(header):
    if header is None:
        return None
    if isinstance(header, dict):
        return dictionary.get_header(header)
    else:
        return header


