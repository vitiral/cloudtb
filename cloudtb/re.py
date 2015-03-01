import re


def groups(searched):
    '''returns groups as matched from searched.regs

    Arguments:
        searched -- object from re.search
    '''
    group = searched.group
    return tuple(group(i) for i in range(len(searched.regs)))


class research(tuple):
    def __new__(cls, exp, text, start=0, end=None):
        return tuple.__new__(cls, _research(exp, text, start, end))

    def __repr__(self):
        return ''.join(str(n) for n in self)


class Group:
    '''Regular expression object that better tracks information from what
    group it came from
    Attributes:
        index -- get the group index
    '''
    def __init__(self, text, searched, groups, index=0):
        indexes = [index]
        mytext = groups[index]
        matches = []
        myreg = searched.regs[index]
        mystart, myend = myreg
        # prev_end = 0 if index is 0 else searched.regs[index][1]
        prev_end = mystart
        index += 1
        while index < len(searched.regs):
            reg = searched.regs[index]
            start, end = reg
            if start >= myend and end > myend:
                # the reg does not fit in self
                break
            assert start >= mystart and end <= myend
            if prev_end < start:
                # store raw text
                matches.append(text[prev_end:start])
            if reg == myreg:
                indexes.append(index)
                index += 1
                continue
            matches.append(Group(text, searched, groups, index))
            index += len(matches[-1].indexes)
            prev_end = searched.regs[index - 1][1]

        self.text = mytext
        self.reg = myreg
        self.matches = matches
        self.indexes = indexes

    @property
    def index(self):
        '''Simplified index number

        Note: one regexp can be multiple group indexes
        '''
        return self.indexes[0]

    def __repr__(self):
        start, end = '[', '#{}]'.format(self.index)
        if self.matches:
            middle = ''.join(str(n) for n in self.matches)
        else:
            middle = self.text
        return start + middle + end


def _research(exp, text, start=0, end=None):
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

        yield Group(text, searched, groups(searched))
        pos = stop
    yield text[pos:]
