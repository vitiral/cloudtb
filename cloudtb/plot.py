# -*- coding: utf-8 -*-
'''
General plotting tools like finding the average of bins of data

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
import colorsys


def get_hex(color):
    '''Convert a tuple (red, green, blue) color to a hex color'''
    color = tuple(int(n * 255) for n in color)
    return ('#' + '{:02x}' * 3).format(*color)


def get_colors(num_colors, hex=False):
    '''Get a range of visible colors'''
    colors = []
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i / 360
        lightness = (50 + np.random.rand() * 10) / 100
        saturation = (90 + np.random.rand() * 10) / 100
        color = colorsys.hls_to_rgb(hue, lightness, saturation)
        if hex:
            color = get_hex(color)
        colors.append(color)
    return colors


def get_bins(x, y, bins):
    '''Put data into semi-equal bins'''
    prev = 0
    assert len(x) == len(y)
    if len(y) <= bins:
        yield x, y
        raise StopIteration
    for i in range(len(y) // bins, len(y) - 1, len(y) // bins):
        yx, yy = x[prev:i], y[prev:i]
        assert len(yx) == len(yy)
        yield yx, yy
        prev = i
    if prev < len(x) - 1:
        yx, yy = x[prev:], y[prev:]
        assert len(yx) == len(yy)
        yield yx, yy


def get_time_bins(series, window):
    '''Returns data in time bins. Uses the index for time lengths'''
    start = min(series.index)
    end = max(series.index)
    prev = start
    print("Times:", start, end, window)
    for t in np.arange(start, end, window):
        yield series[prev:t]
        prev = t
    yield series[prev:]


def time_slopes(series, window):
    series = series.dropna()
    mx, my = [], []
    for s in get_time_bins(series, window):
        bx, by = s.index, s.values
        # print(bx, by)
        m, c = np.polyfit(bx, by, 1)
        # m, c, r_value, p_value, std_err = stats.linregress(bx, by)
        mx.append(np.mean(bx))
        my.append(m)
    return mx, my


def slopes(series, perbin=10):
    series = series.dropna()
    x, y = series.index, series.values
    bins = len(series) // perbin
    data = []
    mx = []
    for bx, by in get_bins(x, y, bins):
        m, c = np.polyfit(bx, by, 1)
        # m, c, r_value, p_value, std_err = stats.linregress(bx, by)
        data.append(m)
        mx.append(np.mean(bx))
    return mx, data


def linear_fit(x, y, bins=None):
    '''Split the data into bins and fit each bin with a line. Return
    the calculated bin lines'''
    if bins is None:
        # A = np.vstack([x, np.ones(len(x))]).T
        # m, c = np.linalg.lstsq(A, y)[0]
        # m, c, r_value, p_value, std_err = stats.linregress(x, y)
        m, c = np.polyfit(x, y, 1)
        return m * x + c
    else:
        data = []
        for bx, by in get_bins(x, y, bins):
            data.append(linear_fit(bx, by))
        return np.concatenate(data)


def mean_fit(x, y, bins=None):
    '''Useful for visualizing a good approximation of a data trend'''
    if bins is None:
        return np.mean(x), np.mean(y)
    else:
        dx = []
        dy = []
        for bx, by in get_bins(x, y, bins):
            bx, by = mean_fit(bx, by)
            dx.append(bx)
            dy.append(by)
        return np.array(dx), np.array(dy)


def linear_std(x, y, bins, line=None):
    '''Returns the normalized standard deviation of the data matched to
    *bins* lines'''
    # get unit mean
    unit_mean = np.mean(y - np.min(y))
    # normalize it to be around the center
    if line is None:
        line = linear_fit(x, y, bins)
    data = line - y
    # return the normalized linear standard deviation
    return np.std(data) / unit_mean
