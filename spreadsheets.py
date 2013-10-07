#!/usr/bin/python
# -*- coding: utf-8 -*-
#    The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    https://github.com/cloudformdesign/cloudtb
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT

class spreadsheet_index_counter(object):
    '''can keep track of incrementing an spreadsheet notated number.
    can also be used to increment pre-existing spreadsheet notation'''
    def __init__(self, letters = None, count = 0 ):
        self.count = count
        if letters == None:
            self.letters = [0]
        else:
            self.letters = letters

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

    def get_spreadsheet_counter(self):
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
    ec = spreadsheet_index_counter()
    ec.letters = num_list

    if num_list == []:
        return 'A', row
    else:
        ec.increment()
        return ec.get_spreadsheet_counter(), row

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

def dev1():
    e = spreadsheet_index_counter()
    num = int(1000)
    for n in xrange(num, num+100000):
        e_count = e.get_spreadsheet_counter()
        a = strindex_to_stdindex(e_count + '0')[1]
        if a != e.count:
            print 'ERROR1: ', e.count, e_count, a
        b = stdindex_to_strindex((0, e.count))[0]
        if b != e_count:
            print 'ERROR2: ', e.count, e_count, b
        e.increment()