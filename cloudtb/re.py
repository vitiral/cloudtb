# -*- coding: utf-8 -*-
'''
add `research` object to have more interactive searches
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import re

from .pprint import fcolors
try:
    from colors import cyan, red, magenta
except ImportError:
    cyan, red, magenta = None, None, None
colors = dict(markup=cyan, match=magenta, replace=red)


def groups(searched):
    '''returns groups as matched from searched.regs (re.search.groups doesn't)

    Arguments:
        searched -- object from re.search
    '''
    group = searched.group
    return tuple(group(i) for i in range(len(searched.regs)))


class research(tuple):
    '''Use instead of re.search to get more interactive matches
    It is itself a tuple that contains Group and str objects representing
    the matched and unmatched sections of the text, respectively

    Properties:
        matches -- only the matches of the search
        repr(self) -- helpful formatted string showing matched text inside
            of original text

    Example:
        exp = '(foo).*?(bar)'
        text = 'so foo is the opposite of bar but without foo there is no bar?'
        searched = research(exp, text)
        print(searched)
        print(searched[0])
        print(repr(searched.matches[0]))  # item access
        print(repr(searched.matches[0][0])) # groups have item access too
        searched.sub('zaz', 2)  # replace group 2 with 'zaz'
        print(searched.str)
    Output:
        so [[foo#1] is the opposite of [bar#2]#0] but without [[foo#1] there
        is no [bar#2]#0]?
        'so '
        '[[foo#1] is the opposite of [bar#2]#0]'
        '[foo#1]'
        'so foo is the opposite of zaz but without foo there is no zaz?'
    '''
    def __new__(cls, exp, text, start=0, end=None):
        return tuple.__new__(cls, cls._construct(exp, text, start, end))

    def __init__(self, exp, text, start=0, end=None):
        self.matches = tuple(m for m in self if isinstance(m, Group))

    def sub(self, text, index):
        '''Substitute the text for the group index.
        Remeber that the whole match object is group 0
        '''
        for m in self.matches:
            try:
                m.sub(text, index)
            except ValueError:
                pass

    @property
    def repr(self):
        return ''.join(n if isinstance(n, str) else n.repr for n in self)

    @property
    def str(self):
        return ''.join(n if isinstance(n, str) else n.str for n in self)

    @staticmethod
    def _construct(exp, text, start=0, end=None):
        if isinstance(exp, (str, bytes)):
            exp = re.compile(exp)
        end = len(text) if end is None else end
        search = exp.search
        pos = start
        count = 0
        # import ipdb; ipdb.set_trace()
        while pos <= end:
            searched = search(text, pos, end)
            if searched is None:
                break
            count += 1
            if count > end:
                assert False
            start, stop = searched.span()
            # get the raw text (no match)
            t = text[pos: start]
            if t is not '':
                yield t
            if start == stop:  # empty match
                pos += 1
                continue

            yield Group(text, searched)
            pos = stop
        yield text[pos:]

    def __repr__(self):
        return ''.join(str(n) for n in self)


class Group(list):
    '''Regular expression object that better tracks information from what
    group it came from

    Properties:
        __getitem__ -- items are stored in the order they are matched.
            Raw text is stored as a str, Group objects and their children
            are stored as Group
        matches -- same as item access, except only the Group objects
        reg -- (start, stop) within the outside text. Same idea as
            re.search(*).regs
        text -- the base text of the whole match
        repr(self) -- helpful formatted string showing self and all internal
            matches
        index -- the main group index
        indexes -- all group indexes that match the group
    '''
    def __init__(self, text, searched, sgroups=None, index=0):
        if sgroups is None:
            sgroups = groups(searched)
        mytext = sgroups[index]
        indexes = [index]
        data = []
        myreg = searched.regs[index]
        mystart, myend = myreg
        # prev_end = 0 if index is 0 else searched.regs[index][1]
        prev_end = mystart
        istart = index
        index += 1
        while index < len(searched.regs):
            reg = searched.regs[index]
            start, end = reg
            if start < 0:
                assert sgroups[index] is None
                index += 1
                continue
            if start >= myend and end > myend:
                # the reg does not fit in self
                break
            assert start >= mystart and end <= myend
            if prev_end < start:
                # store raw text
                data.append(text[prev_end:start])
            if reg == myreg:
                indexes.append(index)
                index += 1
                continue
            data.append(Group(text, searched, sgroups, index))
            index += data[-1]._iconsumed
            prev_end = searched.regs[index - 1][1]

        list.__init__(self, data)
        self.text = mytext
        self.replaced = None
        self.reg = myreg
        self.index = (indexes[0] if (len(indexes) < 2 or indexes[0] is not 0)
                      else indexes[1])
        self.indexes = set(indexes)
        self.matches = tuple(m for m in data if isinstance(m, Group))
        for m in self.matches:
            indexes.extend(m._mindexes)
        self._mindexes = set(indexes)  # all self and child match indexes
        self._iconsumed = index - istart

    def _repr(self, colorize=None):
        col = colors
        if colorize is False:
            markup, match, replace = None, None, None
        else:
            markup, match, replace = col['markup'], col['match'], col['replace']
        represent = [('[', markup)]
        if self.matches and self.replaced is None:
            for n in self:
                if isinstance(n, str):
                    represent.append((n, match))
                else:
                    represent.extend(n._repr())
        else:
            represent.append((self.text, match) if self.replaced is None else
                             (self.replaced, replace))
        represent.append(('#{}]'.format(self.index), markup))
        return represent

    def __repr__(self):
        return fcolors(self._repr())

    @property
    def str(self):
        '''get the full text, including all replacements'''
        if self.matches:
            return ''.join(n if isinstance(n, str) else n.str for n in self)
        else:
            return self.text if self.replaced is None else self.replaced

    @property
    def repr(self):
        '''Returns pure utf8 of repr (no colors)'''
        return fcolors(self._repr(), color=False)

    def sub(self, text, index=None):
        if index is None or index in self.indexes:
            self.replaced = text
        elif index in self._mindexes:
            for m in self.matches:
                try:
                    return m.sub(text, index)
                except ValueError:
                    pass
            assert False
        else:
            raise ValueError("index {} not in Group. Indexes: {}".
                             format(index, self.indexes))
