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

'''
This module contains general use tools in GUI's or displaying data 
(i.e. matplotlib)

'''

from __future__ import division

def get_color_from_index(index, max_index, highest = 180):
    '''
    Returns a good spread of colors quickly
    Increase highest for brighter colors, decrease for darker. Absolute max
    is 256
    '''
#    Good color algorithm (gotten from playing with color bar in Qt)
#    RED HIGH    (start)
#    UP BLUE     (red high)    256
#    DOWN RED    (blue high)   512 
#    UP GREEN    (blue high)
#    DOWN BLUE   (green high)
#    UP RED      (green high)
#    DOWN GREEN (ENDS AT HIGH RED)
#    
#    or, to put into code, there are 6 * 256 possibilities 
#    (although I'd end at green == 70 to keep the last color orange so 5*256 - 70)
#    They can be arrived at through simple iteration through this algorithm, or
#    iteration plus jumping, or ... THIS CODE!
    if highest > 256:
        raise ValueError('highest: ' + str(highest))
    reserve = (70*highest/256)
    assert(reserve > 0)
    cindex = int((float(index) / (max_index + 1)) * (5*highest-reserve))
    cindex = cindex + 1
    red, blue, green = (0,)*3
    
    if cindex <= highest:
        red = highest - 1
        blue = cindex -  (         highest * 0) - 1
    elif cindex <= highest * 2:
        blue = highest - 1
        red = highest -  (cindex - highest * 1) - 1
    elif cindex <= highest * 3:
        blue = highest - 1
        green = cindex - (         highest * 2) - 1
    elif cindex <= highest * 4:
        green = highest - 1
        blue = highest - (cindex - highest * 3)
    else:
        assert(0)

    return get_color(red, green, blue)

def get_color(red, green, blue):
    if not 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
        raise ValueError("a value is above 255 or less than 0: " 
            + str((red, green, blue)))
    return (red << 16) + (green << 8) + (blue)

def get_color_str(red = None, green = None, blue = None, color = None):
    if not color:
        color = get_color(red, green, blue)
    color = hex(color)[2:]
    return '0'*(6 - len(color)) + color

'''Some fun general text tools'''
class SpellingCorrector(object):
    '''A very simple spelling corrector, used in GUIs to check user input.
    Short fast and simple, it doesn't always work -- but does it need to?'''
    def __init__(self, all_words):
        if type(all_words) in (tuple, list, set):
            nw = [n.lower() for n in all_words]
            nw.sort()
            self.NWORDS = nw
        else:
            self.NWORDS = self.words(all_words)
        self.NWORDS = self.train(self.NWORDS)

    def words(self, text):
        ''' returns a list of words'''
        return re.findall('[a-z]+', text.lower())

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self, word):
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       deletes    = [a + b[1:] for a, b in splits if b]
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
       inserts    = [a + c + b     for a, b in splits for c in alphabet]
       return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word)
                   for e2 in self.edits1(e1) if e2
                   in self.NWORDS)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    def correct(self, word):
        candidates = (self.known([word]) or
                      self.known(self.edits1(word)) or
                      self.known_edits2(word) or
                      [word])
        return max(candidates, key=self.NWORDS.get)
