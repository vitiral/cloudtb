#!/usr/bin/python
# -*- coding: utf-8 -*-
#    ******  The Cloud Toolbox v0.1.2******
#    This is the cloud toolbox -- a single module used in several packages
#    found at <https://github.com/cloudformdesign>
#    For more information see <cloudformdesign.com>
#
#    This module may be a part of a python package, and may be out of date.
#    This behavior is intentional, do NOT update it.
#    
#    You are encouraged to use this pacakge, or any code snippets in it, in
#    your own projects. Hopefully they will be helpful to you!
#        
#    This project is Licenced under The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    <https://github.com/cloudformdesign/cloudtb>
#    
#    Permission is hereby granted, free of charge, to any person obtaining a 
#    copy of this software and associated documentation files (the "Software"),
#    to deal in the Software without restriction, including without limitation 
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,
#    and/or sell copies of the Software, and to permit persons to whom the 
#    Software is furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#    DEALINGS IN THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT
"""
Run this function as main to calibrate your profile.OptionParser

TODO: save the file created into tmp automatically, and have the profile_function
automatically grab the value (and create it if necessary)

Some Notes:
    out = cProfile.runctx('self.function()', globals(),
                          locals(), 'development')
    self._profiler.strip_dirs().sort_stats('cumulative').print_stats()
    return out

"""

from __future__ import division

SHELVE = 'calibration.pcl'
CALIBRATION_VARIABLE = 'calibration'

import pdb
import shelve
import math
import cProfile, profile, pstats

def profile_function(function, name, *args, **kwargs):
    '''Run like this:
        profile_name = 'example'
        out = prilfe_function('myfunction', profile_name , globals(), locals(),
                             1,2,3,4,5,6, 'first keyword' = 'first')
        print_profile(profile_name)
        # do stuff with out
    '''
    prof = cProfile.Profile()
    retval = prof.runcall(function, *args, **kwargs)
    prof.dump_stats(name)
    print_profile(name)
    return retval

#    return cProfile.runctx(function_str, globals, locals, name)

def print_profile(name):
    p = pstats.Stats(name)
    p.strip_dirs().sort_stats('cumulative').print_stats()

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

        print "Are these numbers roughly the same? (y or n)"
        for n in a:
            print n

        an = raw_input("Answer: ")
        if an == 'y':
            break

    else:
        print 'Could not calibrate profiler'
        return

    d = shelve.open(SHELVE)
    d[CALIBRATION_VARIABLE] = sum(a) / len(a)

if __name__ == '__main__':
    calibrate_profiler()