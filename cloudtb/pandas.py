# -*- coding: utf-8 -*-
'''
Useful tools for working with the python library pandas
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas as pd
from cloudtb.dictionary import get_header, pack, flatten, fill_keys, depth
from . import builtin


def _dataframe_dict(data, index=None, filler='', header=None):
    if isinstance(data, dict):
        try:
            if depth(data, isiter=True) < 2:
                return data
        except TypeError:
            return data
    if not isinstance(data, dict):
        header = resolve_header(header)
        if header is None:
            header = get_header(data[0])
        data = pack(data, header)
    data = flatten(data)
    data = fill_keys(data, filler)
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
        return get_header(header)
    else:
        return header


def add_level(df, level, name=None):
    '''Adds a level onto a dataframe's column index'''
    if builtin.isiter(level):
        raise NotImplementedError
    else:
        cols = df.columns
        if isinstance(cols, pd.MultiIndex):
            levels = cols.levels + [[level]]
            labels = cols.labels + [[0] * len(cols.labels[0])]
            names = cols.names + [name]
            cols = pd.MultiIndex(levels=levels, labels=labels, names=names)
        else:
            cols = pd.MultiIndex.from_tuples(
                tuple(zip(cols, (level,) * len(cols))))
        df.columns = cols
    return df
