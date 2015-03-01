import re


def groups(searched):
    '''returns groups as matched from searched.regs

    Arguments:
        searched -- object from re.search
    '''
    group = searched.group
    return tuple(group(i) for i in range(len(searched.regs)))


def research(exp, text, start=0, end=None, parseregex=True):
    '''Similar to re.search except it returns a tuple of Group objects.
    These are more interactive and more easy to glean data from.'''
    if isinstance(exp, (str, bytes)):
        exp = re.compile(exp)
    end = len(text) if end is None else end
    search = exp.search
    pos = start
    count = 0
    prev_stop = pos
    while pos < end:
        searched = search(text, pos, end)
        if searched is None:
            break
        count += 1
        if count > end:
            assert False
        start, stop = searched.span()
        # get the raw text (no match)
        t = text[prev_stop: start]
        if t is not '':
            yield t
        if start == stop:  # empty match
            prev_stop += 1
            continue

        yield Group(searched, groups(searched))
        prev_stop = stop


class Group:
    '''Regular expression object that better tracks information from what
    group it came from
    Attributes:
        index -- get the group index
    '''
    def __init__(self, text, searched, groups, index=0):
        indexes = []
        text = groups[index]
        matches = []
        myreg = searched.regs[index]
        mystart, myend = myreg
        prev_end = 0 if index is 0 else searched.regs[index][1]
        while index < len(searched.regs):
            reg = searched.regs[index]
            start, end = reg
            if reg == myreg:
                indexes.append(index)
                index += 1
                continue
            elif start >= myend and end > myend:
                # the reg does not fit in self
                break
            assert start >= mystart and end <= myend
            if prev_end < start:
                # store raw text
                matches.append(text[prev_end:start])
            matches.append(Group(text, searched, groups, index))
            index += len(matches[-1].indexes)
            prev_end = searched.regs[index - 1][1]

        self.text = text
        self.reg = myreg
        self.matches = matches
        self.indexes = indexes

    @property
    def index(self):
        '''Simplified index. Technically the match can be multiple
        indexes because it can contain embeded groups'''
        return self.indexes[0]

    def __str__(self):
        start, end = '', ''
        if self.matches:
            match = self.matches[0]
            start = '<*m{0}>[['.format(match)
            end = r']]'
        str_data = ''.join([str(n) for n in self.matches])
        return start + '{{{0}}}<g{1}>'.format(str_data, self.indexes) + end
