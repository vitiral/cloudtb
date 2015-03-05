# -*- coding: utf-8 -*-
'''
additional pprint functions, like printing a list
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from cloudtb.sys import hascolor


def pplist(l, cols=4, indent=0):
    if not isinstance(l, list):
        l = list(l)
    while len(l) % cols != 0:
        l.append(" ")
    step = len(l) // cols
    step = step if step != 0 else 1
    split = [l[i:i + len(l) // cols] for i in range(0, len(l), step)]
    for row in zip(*split):
        print(' ' * indent + "".join(str.ljust(i, 20) for i in row))


def ppcolors(colorized, color=None):
    '''pprints out colorized string

    This function autodetects whether the terminal in use supports colors with
    cloudtb.sys.hascolor. If the terminal does not support colors, it prints
    out plain text

    Arguments:
        colorized -- list of (text, color_function) tuples
            color_function should be None (do nothing) or
            a function that colorizes the input text. It is recommended to use
            the python package ansicolors.
            Example:
                from colors import red, green, blue
                ppcolors([ ('red', red), (' green ', green), ('blue', blue) ])
            Will print out "red green blue" in their respective colors
        color -- if None, do default (use detection), if False never print
            colors, if True always print colors
    '''
    print(fcolors(colorized, color))


def fcolors(colorized, color=None):
    '''Same as ppcolors but returns the formatted string'''
    if color is None:
        color = hascolor
    if color:
        out = (text if color is None else color(text) for
               text, color in colorized)
    else:
        out = (text for text, color in colorized)
    return ''.join(out)
