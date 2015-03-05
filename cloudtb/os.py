# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from os import path as _path


def abspath(path):
    '''A better abspath. Automatically expands user'''
    return _path.abspath(_path.expanduser(path))


def split(path):
    '''A better split function. Completely splits a path'''
    _split = _path.split
    folders = []
    while 1:
        path, folder = _split(path)
        if folder:
            folders.append(folder)
        else:
            if path:
                folders.append(path)
            break

    folders.reverse()
    return folders
