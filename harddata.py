#! /usr/bin/python
"""
*** BEGIN PROJECT LICENSE ***
The MIT License (MIT)

Copyright (c) 2013 Garrett Berg cloudformdesign.com
An updated version of this file can be found at:
https://github.com/cloudformdesign/cloudtb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

http://opensource.org/licenses/MIT
*** END PROJECT LICENSE ***

"""
# -*- coding: utf-8 -*-
"""


This module was created to realize the potential of "hard data", or data
stored on the harddrive, for memory management and speed.

When I talk of speed, I am not talking computations per second in a
hypothetical universe. What I'm talking about is the same kind of speed
that python relies on -- the user of your program.

Most data is hardly ever accessed. For the rare instances you actually need
data RIGHT NOW (and lots of it), the best thing you can do is use iterators.
The module iterables.py aims to give that to you.

For other data you would be better off storing it in a file. I don't know
how many times I have written the code.

For local variales inside of functions, this doesn't really apply -- but for
most object variables they should almost ALWAYS be stored in a file instead.

Here's the wonderful thing about file access -- it's slow, and python knows
it's slow. While you're program is busy taking 100 times longer to pull your
large variable from a file, the rest of your computer can be operating that
much faster.


"""
import pdb
import cPickle

import tempfile
'''
mkdtemp(sufix = '.hd', prefix = 'pyhdd08234', dir = )
I want to use mkdtemp to create the temporary directory
a special file named 'timeout' will be created in it

f, path = mkstemp(suffix = '.hd', prefix='hd', dir = path)
'''

get_attr = object.__getattribute__
set_attr = object.__setattr__

class harddata(object):
    def __init__(self, data):
        set_attr(self, '__harddata__', data)
        set_attr(self, '__tmpfile__', tempfile.mkstemp(
        suffix = '.hd', prefix='hd', dir = path))

        
    def __getattribute__(self, name):
        print 'GetAttr:', name
        ga = get_attr
        data = ga(self, 'data')          
        try:
            return ga(self, name)
        except AttributeError:
            return data.__getattribute__(name)
    
    def __setattr__(self, name, value):
        print 'SetAttr', name, value
        data = self.data
        data.__setattr__(name, value)
    
    def __getitem__(self, item):
        return self.data.__getitem__(item)
    
    def __getdata__(self):
        
    
    def __storedata__(self):
        pass
    
    a = 'hello world'
    
hd = harddata(range(100))
print hd.data[10]
print hd[10]
