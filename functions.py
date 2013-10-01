from __future__ import division

import sys, os
import math
import inspect
import itertools
import traceback

SHELVE_FNAME = 'calibration.pcl'
CALIBRATION_VARIABLE = 'calibration'
CALIBRATE_VALUE = None

import pdb
import shelve
import cProfile, profile, pstats

def profile_function(name, function, *args, **kwargs):
    '''Run like this:
        profile_name = 'example'
        out = prilfe_function('myfunction', profile_name , globals(), locals(), 
                             1,2,3,4,5,6, 'first keyword' = 'first')
        print_profile(profile_name)
        # do stuff with out
    '''
    # This doesn't work! It doesn't return values
#    return cProfile.runctx(function_str, glob, loc, name)
    # http://stackoverflow.com/questions/1584425/return-value-while-using-cprofile
    get_calibrate_value()    
    prof = cProfile.Profile()
    out = prof.runcall(function, *args, **kwargs)
    prof.dump_stats(name)
    return out

class print_twice(object):
    '''replaces std_out to print to both a file object and the standard
    print location'''
    def __init__(self, fname):
        self.stdout = sys.stdout
        sys.stdout = self
        self.file = open(fname, 'w')
    
    def write(self, text):
        self.stdout.write(text)
        self.file.write(text)

def print_profile(name):
    p = pstats.Stats(name)
    p.strip_dirs().sort_stats('cumulative').print_stats()

def get_calibrate_value():
    d =  shelve.open(SHELVE_FNAME)
    try:
        cal = d[CALIBRATION_VARIABLE]
        profile.Profile.bias = cal
        return True
    except KeyError:
        return False
    finally:
        d.close()

def columnize_rows(data):
    '''This does something similar to a Transpose, but on any set of data'''
    return np.fliplr(np.rot90(data, k=-1))

def calibrate_profiler():
    '''The object of this exercise is to get a fairly consistent result. 
    If your computer is very fast, or your timer function has poor resolution, 
    you might have to pass 100000, or even 1000000, to get consistent results.
    http://docs.python.org/2/library/profile.html
    '''
    pr = profile.Profile()    
    for n in xrange(4, 6):
        times = 10**n
        
        a = []
        for i in range(5):
            a.append(pr.calibrate(times))
        
        print ("Are these numbers roughly the same? "
        "(+/- .3 order of magnitude) (y or n)")
        for n in a:
            print n
            
        an = raw_input("Answer: ")
        if an == 'y':
            break
    
    else:
        print 'Could not calibrate profiler'
        return
    
    d = shelve.open(SHELVE_FNAME)
    try:
        d[CALIBRATION_VARIABLE] = sum(a) / len(a)
    finally:
        d.close()

def between(value, v_min, v_max):
    if v_min == None and v_max == None:
        raise ValueError
    
    if v_min == None:
        return value < v_max
    
    if v_max == None:
        return value > v_min
    
    return v_min < value < v_max
    
class iter2(object):
    '''Takes in an object that is iterable.  Allows for the following method
    calls (that should be built into iterators anyway...)
    calls:
        - append - appends another iterable onto the iterator.
        - insert - only accepts inserting at the 0 place, inserts an iterable
         before other iterables.
        - adding.  an iter2 object can be added to another object that is
         iterable.  i.e. iter2 + iter (not iter + iter2).  It's best to make
         all objects iter2 objects to avoid syntax errors.  :D
    '''
    def __init__(self, iterable):
        self._iter = iter(iterable)
    
    def append(self, iterable):
        self._iter = itertools.chain(self._iter, iter(iterable))
        
    def insert(self, place, iterable):
        if place != 0:
            raise ValueError('Can only insert at index of 0')
        self._iter = itertools.chain(iter(iterable), self._iter)
    
    def __add__(self, iterable):
        return itertools.chain(self._iter, iter(iterable))
        
    def next(self):
        return self._iter.next()
    
    def __iter__(self):
        return self

def flatten(iterable):
    '''flatten a list of any depth'''
    iterable = iter2(iterable)
    for e in iterable:
        if hasattr(e, '__iter__'):
            iterable.insert(0, e)
        else:
            yield e
            
def import_path(fullpath, do_reload = False):
    """ 
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do. 
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.insert(0, path)
    module = __import__(filename)
    if do_reload:
        reload(module)
    del sys.path[0]
    return module
            
def set_priority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process to "below normal" but can take any valid process ID and priority. 
        http://code.activestate.com/recipes/496767-set-process-priority-in-windows/
        """
        
    import win32api,win32process,win32con
    
    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])
    
    
def find_depth(value):
     '''returns the depth of the array
     0 : strings, integers, floats, etc.
     1 : vectors (1d)
     2 : matrixies (2d)
     etc
     '''
     if not hasattr(value, '__iter__'):
          return 0, value
          
     if hasattr(value, 'next'): # if it is an itterator
          firstval = value.next()     # take a peek
          value = itertools.chain((firstval,), value)
     else: 
          firstval = value[0]

     if hasattr(firstval, '__iter__'): # then it is a matrix!
          return 2, value
     else:
          return 1, value
          
def get_first(value):
     '''returns the first element wihtout upsetting an iterator
     (must re-assign iterator to the second return value)'''
     if not hasattr(value, '__iter__'):
          return value, value
          
     if hasattr(value, 'next'): # if it is an itterator
          firstval = value.next()     # take a peek
          value = itertools.chain((firstval,), value)
          return firstval, value
     
     firstval = value[0]
     return firstval, value
          
def assign_to_self(self, assign_variables):
     if 'self' in assign_variables:
          del assign_variables['self']
     for name, value in assign_variables.iteritems():
          #print name, value
          exec('self.{0} = value'.format(name))
          #print eval('self.{0}'.format(name))
          
def replace_all(input_string, replacements):
     '''replace the elements of the string defined in the iterable tuple.
     ex: ((' ', ''), ('_', '')) would get rid of spaces and underscores'''
     for before, after in replacements:
          input_string = input_string.replace(before, after)
     return input_string

def special_figt(data_list, value, start = 0):
    index = first_index_gt(data_list, value, start)
    if data_list[index + 1] > value: 
        return index + start
    else:
        return - 1

def first_index_gt(data_list, value, start = 0):
    '''return the first index greater than value from a given list like object'''
    data_list = itertools.islice(data_list, start, None)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] > value)
        return index + start
    except StopIteration: return - 1

def first_index_gtet(data_list, value, start = 0):
    '''return the first index greater than value from a given list like object'''
    data_list = itertools.islice(data_list, start, None)
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] >= value)
        return index + start
    except StopIteration: return - 1

def first_index_lt(data_list, value, start = 0):
    '''return the first index less than value from a given list like object'''
    data_list = itertools.islice(data_list, start, None)    
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] < value)
        return index + start
    except StopIteration: return - 1

def first_index_ne(data_list, value, start = 0):
    '''returns first index not equal to the value from list'''
    data_list = itertools.islice(data_list, start, None)    
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] != value)
        return index + start
    except StopIteration: return - 1

def first_index_et(data_list, value, start = 0):
    '''same as data_list.index(value), except with exception handling
    Also finds 'nan' values '''
    data_list = itertools.islice(data_list, start, None)    
    try:
        if type(value) == float and math.isnan(value):
            floats = (float, np.float64, np.float32, np.float96)
            isnan = math.isnan
            return next(data[0] for data in enumerate(data_list)
              if (type(data[1]) in floats
              and isnan(data[1])))  + start
        else:
            return next(data[0] for data in 
            enumerate(data_list) if data[1] == value) + start
    except (ValueError, StopIteration): return - 1

def index_to_coords(index, shape):
    '''convert index to coordinates given the shape'''
    coords = []
    for i in xrange(1, len(shape)):
        divisor = int(np.product(shape[i:]))
        value = index//divisor
        coords.append(value)
        index -= value * divisor
    coords.append(index)
    return tuple(coords)
    
def first_coords_et(data_matrix, value, start = 0):
    '''the first coordinates that are equal to the value'''
    index = first_index_et(data_matrix.flatten(), value, start)
    shape = data_matrix.shape
    return index_to_coords(index, shape)
    
def npfirstindex(data, value):
    where = np.where(data == value)
    if len(where) == 0: return - 1
    return where[0][0]

if os.name in ("nt", "dos"):
     exefile = ".exe"
else:
     exefile = ""

def win_run(program, *args, **kw):
     mode = kw.get("mode", os.P_WAIT)
     for path in os.environ["PATH"].split(os.pathsep):
          file = os.path.join(path, program) + ".exe"
          try:
                return os.spawnv(mode, file, (file,) + args)
          except os.error:
                pass
     raise os.error, "cannot find executable"
 
def spawn(program, *args):
     try:
          # check if the os module provides a shortcut
          return os.spawnvp(program, (program,) + args)
     except AttributeError:
          pass
     try:
          spawnv = os.spawnv
     except AttributeError:
          # assume it's unix
          pid = os.fork()
          if not pid:
                os.execvp(program, (program,) + args)
          return os.wait()[0]
     else:
          # got spawnv but no spawnp: go look for an executable
          for path in os.environ["PATH"].split(os.pathsep):
                file = os.path.join(path, program) + exefile
                try:
                     return spawnv(os.P_WAIT, file, (file,) + args)
                except os.error:
                     pass
          raise IOError, "cannot find executable"

def module_path(local_function):
    ''' returns the module path without the use of __file__.  Requires a function defined 
    locally in the module.  This is necessary for some applications like IDLE.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(inspect.getsourcefile(local_function))


def dev1():
    win_run("python", "hello.py", mode = os.P_NOWAITO)
    
    from time import sleep
    for _n in range(3):
        print "still here"
        sleep(1)

def dev2():
    print replace_all('hello bob', ((' ', ''), ('b', 'II')))
    print replace_all('why hello', (' ', '')
    )
    #print module_path(dev1)

def consume(iterable):
    iterable = iter(iterable)

    while 1:
        try:
            item = iterable.next()
        except StopIteration:
            break

        try:
            data = iter(item)
            iterable = itertools.chain(data, iterable)
        except:
            yield item

str_consume = """
import itertools

def consume(iterable):
    iterable = iter(iterable)

    while 1:
        try:
            item = iterable.next()
        except StopIteration:
            break

        try:
            data = iter(item)
            iterable = itertools.chain(data, iterable)
        except:
            yield item
"""

class excel_index_counter(object):
    '''can keep track of incrementing an excel notated number.
    can also be used to increment pre-existing excel notation'''
    def __init__(self):
        self.count = 0
        self.letters = [0]
        
    def increment(self, position = -1):
        if position == -1:
            self.count += 1
        if self.letters[position] > 24:
            self.letters[position] = 0
            try:
                return self.increment(position -1)
            except IndexError:
                # roll over all letters
                self.letters.insert(0, 0)
                self.letters = [0 for n in self.letters]
        else:
            self.letters[position] += 1
    
    def get_excel_counter(self):
        return ''.join([chr(ord('A') + n) for n in self.letters])
    
    def get_count(self):
        return self.count
        
def stdindex_to_strindex(stdindex):
    '''stdindex is just a simple (row, col) index NOT generators'''
    row, col = stdindex
    row += 1
    num_list = []
    col2 = col
    
    while col2 > 0:
        col = col2
        num_list.insert(0, (col-1) % 26 )
        col2 = (col - 1) // 26
    ec = excel_index_counter()
    ec.letters = num_list
    
    if num_list == []:
        return 'A', row
    else:
        ec.increment()
        return ec.get_excel_counter(), row

def strindex_to_tuples(strindex):
        '''conviencience function for converting from a string index
        i.e. "A2:B20" into a tuple form ('A', 2), ('B', 20)'''
        start, end = strindex.split(':')
        i = first_index_lt(start, 'A')
        start = start[:i], int(start[i:])
        i = first_index_lt(end, 'A')
        end = end[:i], int(end[i:])
        return start, end

def strindex_to_stdindex(strindex):
    '''converts from standard spreadsheet string index into stdindex'''
    # log = easy_log.getLogger(level = LOGGING_LEVEL)
    strindex = strindex.upper().replace(' ', '')
    
    # strindex will be, say 'AA100'.  Find the break point
    n = first_index_lt(strindex, 'A')
    row = int(strindex[n:]) - 1
    
    col_list = list(strindex[:n])
    col_list.reverse()
    col = 0
    for n, c in enumerate(col_list):
        col += (ord(c) - ord('A') + 1) * (26 ** n)
    col -= 1
    return row, col

def sort_together(data):
    '''sorts a multi row array by keeping the rows together.
    Sorts only first row
    untested!
    '''
    x, y = data
    ndx = np.argsort(data[0])
    data = np.dstack([n[ndx] for n in data])
    data = np.transpose(data)
    return data

def safe_eval(eval_str, variable_dict = None):
    '''welll... mostly safe:
        http://lybniz2.sourceforge.net/safeeval.html
    '''
    if variable_dict == None:
        variable_dict = {}
    return eval(eval_str, {"__builtins__" : None}, variable_dict)

def get_user_folder():
    return os.environ['USERPROFILE']

def dev1():
    e = excel_index_counter()
    num = int(1000)
    for n in xrange(num, num+100000):
        e_count = e.get_excel_counter()
        a = strindex_to_stdindex(e_count + '0')[1]
        if a != e.count:
            print 'ERROR1: ', e.count, e_count, a
        b = stdindex_to_strindex((0, e.count))[0]
        if b != e_count:
            print 'ERROR2: ', e.count, e_count, b
        e.increment()

def get_prev_exception_str(E = None, tb = None):
    if E != None:
        out = ['Exception [{0}] Occured:'.format(E)]
    else:
        out = ['Exception Occured:']
    if tb == None:
        tb = sys.exc_info()[2]
    out += traceback.format_tb(tb)
    if E != None:
        out += ['Exception: ' + str(E)]
    return '\n'.join(out)

def np_std_repeat(data, times):
    '''repeats an array of data several times.
    np_std_repeat([1,2,3], 2)
    >>> [[1,2,3],[1,2,3]]'''
    return np.tile(data, (times, 1))
    
import pdb

if __name__ == '__main__':
    ab = np.arange(0, 30000)
    ab.shape = (20, 20, 30000/(20*20))
    value = ab[7][12][0]
    print first_coords_et(ab, value)
    
#    import timeit
#    a = [1, [[[[[[[xrange(2,10)]]]]]]], [xrange(10,20),xrange(20,30),[[[[[[[[[xrange(30,40)]]]]], xrange(40,50)]]], [xrange(50,60), xrange(60,70)]]]]
#    for _n in xrange(100):
#        a = [[a]]
#    print list(flatten(a))    
#    print list(flatten(a)) == range(1,70)
#    print list(consume(a)) == range(1,70)
#    
#    input_str = 'l=[[1, 2, 3], [4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7]] * 10'
#    input_str = 'l=' + str(a) + '\n'
##    print timeit.Timer(
##        '[item for sublist in l for item in sublist]',
##        input_str
##    ).timeit(1000)
#    print timeit.Timer(
#        'list(flatten(l))',
#        input_str + str_flatten
#    ).repeat(5, 1000)
#    
#    print timeit.Timer(
#        'list(consume(l))',
#        input_str + str_consume
#    ).repeat(5, 1000)
    
   
