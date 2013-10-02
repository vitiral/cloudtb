from __future__ import division

def assign_to_self(self, assign_variables):
     if 'self' in assign_variables:
          del assign_variables['self']
     for name, value in assign_variables.iteritems():
          #print name, value
          exec('self.{0} = value'.format(name))
          #print eval('self.{0}'.format(name))



def slice_synatx(args):
    '''figures out most of slice syntax for you.
    Built to mimic itertools.islice -- can also just
    input the slice object gotten during __getitem__'''
    if type(args) == slice:
        start, stop, step = args.start, args.stop, args.step
    elif len(args) == 0:
        raise TypeError("islice_keep takes at least 2 arguments")
    elif len(args) == 1:
        start, stop, step = None, args[0], None
    elif len(args) == 2:
        start, stop = args
        step = None
    elif len(args) == 3:
        start, stop, step = args
    else:
        raise TypeError("islice_keep takes at max 4 arguments")

    if start == None and stop == None and step == None:
        raise ValueError

    start = 0 if start == None else start
    step = 1 if step == None else step

    return start, stop, step


def iterable_slice_error_check(start, stop, step):
    if start < 0 or (stop < 0 and stop != None) or step < 0:
        raise IndexError("No negative indexes: " + repr([start, stop, step]))
    if stop != None:
        if start >= stop:
            raise IndexError("start greater than or equal to stop")
        if step >= stop - start:
            raise IndexError("step larger than stop - start")

