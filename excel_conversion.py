# -*- coding: utf-8 -*-

from functions import first_index_lt
from objects import excel_index_counter
        
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
        
if __name__ == '__main__':
    e = excel_index_counter()
    num = int(1000)
    for n in xrange(1000):
        e_count = e.get_excel_counter()
        a = strindex_to_stdindex(e_count + '0')[1]
        print e.count, a, e_count
        if a != e.count:
            print 'ERROR1: ', e.count, e_count, a
        b = stdindex_to_strindex((0, e.count))[0]
        if b != e_count:
            print 'ERROR2: ', e.count, e_count, b
        e.increment()