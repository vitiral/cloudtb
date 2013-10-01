from __future__ import division

import sys, os

import inspect
import traceback

SHELVE_FNAME = 'calibration.pcl'
CALIBRATION_VARIABLE = 'calibration'
CALIBRATE_VALUE = None

import pdb

def assign_to_self(self, assign_variables):
     if 'self' in assign_variables:
          del assign_variables['self']
     for name, value in assign_variables.iteritems():
          #print name, value
          exec('self.{0} = value'.format(name))
          #print eval('self.{0}'.format(name))

def between(value, v_min, v_max):
    if v_min == None and v_max == None:
        raise ValueError
    
    if v_min == None:
        return value < v_max
    
    if v_max == None:
        return value > v_min
    
    return v_min < value < v_max

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
    
   
