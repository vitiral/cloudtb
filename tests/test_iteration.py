# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:36:51 2013

@author: user
"""
try:
    from .. import iteration
except ValueError:
    try:
        import iteration
        print 'Running from within cloudtb'
    except:
        import sys
        sys.path.insert(1, '..')
        import iteration
        print 'Running as outside module'

import unittest
import random

def get_ranges(number):
        return (range(n, n + 100) for n in range(number))
    
def assert_all_equal(iter1, iter2):
    try:
        next(next(iter1) != n for n in iter2)
    except StopIteration:
        assert(0)

def test_add(self):
    a1, a2 = get_ranges(2)
    assert_all_equal(a1 + a2, self.get_object(a1) 
        + self.get_object(a2))
    
def test_extend_front(self):
    a1, a2 = self.get_ranges(2)
    b1 = self.get_object(a1)
    b1.front_extend(a2)
    assert_all_equal(a2 + a1, b1)

def test_slice(self, recreate = True):
    a1 = range(-100, 1000)
    b1 = self.get_object(a1)
    start, stop, step = 0, 100, 5
    assert_all_equal(a1[start:stop:step],
                           b1[start:stop:step])
    
    start = 100
    if recreate: b1 = self.get_object(a1)
    assert_all_equal(a1[start:stop:step],
                           b1[start:stop:step])
    
    stop = 450
    if recreate: b1 = self.get_object(a1)
    assert_all_equal(a1[start:stop:step],
                           b1[start:stop:step])

    step = 1
    if recreate: b1 = self.get_object(a1)
    assert_all_equal(a1[start:stop:step],
                           b1[start:stop:step])
    
def test_slice_repeat(self):
    st, end = 100, 1233
    a1 = range(st, end)
    b1 = self.get_object(a1)
    start, stop, step = 0, end, 5
    a1 = a1[start:stop:step]
    b1 = b1[start:stop:step]
    
    start, stop, step = 0, end / 10, 12
    a1 = a1[start:stop:step]
    b1 = b1[start:stop:step]
    assert_all_equal(a1, b1)
    
def test_getitem(self, recreate = True):
    a1 = range(-100, 1000)
    b1 = self.get_object(a1)
    for n in xrange(-100, 1000, 33):
        if recreate:
            b1 = self.get_object(a1)
        self.assert_equal(a1[n], b1[n])
        
class bitterTest(unittest.TestCase):
    def get_object(self, *args, **kwargs):
        return iteration.biter(*args, **kwargs)

    def test_add(self):
        return test_add(self)
    def test_extend_front(self):
        return test_extend_front(self)
    def test_slice(self):
        return test_slice(self)
    def test_slice_repeat(self):
        return test_slice_repeat(self)
    def test_getitem(self):
        return test_getitem(self)

class soliditerTest(unittest.TestCase):
    def get_object(self, *args, **kwargs):
        return iteration.soliditer(*args, **kwargs)
    
    def test_add(self):
        return test_add(self)
    def test_extend_front(self):
        return test_extend_front(self)
    def test_slice(self):
        return test_slice(self)
    def test_slice_repeat(self):
        return test_slice_repeat(self)
    def test_getitem(self):
        return test_getitem(self, recreate = False)
    
if __name__ == '__main__':
    unittest.main()        