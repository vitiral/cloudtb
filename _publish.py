'''
*** BEGIN FILE LICENSE ***

The MIT License (MIT)

Copyright (c) <year> <copyright holders>

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

Copyright 2013 Garrett Berg cloudformdesign.com

An updated version of this file can be found at:
#TODO: Git link

*** END FILE LICENSE ***

Documentation
This file performs the necessary actions for standard publishing of works in python.
Primarily it updates the License and hosts the file on the selected servers of the
global variables.

Change the global variables below to reflect your project
'''

PYTHON_VERSION = 2
FIRST_LINE = '#! /usr/bin/python{version}'

YOUR_LICENSE = """
 Copyright 2013 Garrett Berg cloudformdesign.com
 Copyright 2009 Luca Trevisan

 Additional contributors: Radu Grigore

 LaTeX2WP version 0.6.2

 This file is part of LaTeX2WP, a program that converts
 a LaTeX document into a format that is ready to be
 copied and pasted into WordPress.

 You are free to redistribute and/or modify LaTeX2WP under the
 terms of the GNU General Public License (GPL), version 3
 or (at your option) any later version.

 I hope you will find LaTeX2WP useful, but be advised that
 it comes WITHOUT ANY WARRANTY; without even the implied warranty
 of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GPL for more details.

 You should have received a copy of the GNU General Public
 License along with LaTeX2WP.  If you can't find it,
 see <http://www.gnu.org/licenses/>.
"""

BEGIN_LICENSE = '*** BEGIN LICENSE ***\n'
END_LICENSE = '*** END LICENSE ***\n'

    
##### CODE ####
import re
import retools
import os
import sys


def convert_to_regexp(txt):
    special = '. ^ $ * + ? { } [ ] \ | ( )'.split(' ')
    special_or = '(\\' + ')|(\\'.join(special) +')'
    print special_or
    
    sfun = retools.subfun(set(special), prepend = '\\')
    
    print re.sub(special_or, sfun, txt)
    
    


def update_license(path):
    '''updates the license information for the file on the path'''
    tquotes = ("'''", '"""')
    
    with open(path, 'r') as f:
        text = f.readlines()
    
    if text[0] != FIRST_LINE:
        text.insert(0, FIRST_LINE)
    
    if text[1][:3] not in tquotes:
        text = [text[0]] + [tquotes[1], YOUR_LICENSE, tquotes[1]] + text[1:]
    else:
        tq = text[1]
        license = []
        for n in xrange(2):
            line = text[n]
            license.append(line)
            if tq in line:
                break
        else:
            raise ValueError("could not find quote ending")
        
        license = '\n'.join(license)
        cmp = re.compile('{0}.*{1}'.format(BEGIN_LICENSE, END_LICENSE))
        cmp.find(YOUR_LICENSE, BEGIN_LICENSE + '\n' + END_LICENSE)
        
    
    a = 1
    
        
    
    
    
    startquotes = False
    
    
    cmp = re.compile('({0})|({1})'.format(*trip_quotes))
    start = False
    for p in cmp.split(text):
        if p in trip_quotes and start == False:
            start == True
        else:
            license
        prev = p
            
    
    
        
    
if __name__ == '__main__':
    print convert_to_regexp(BEGIN_LICENSE)

