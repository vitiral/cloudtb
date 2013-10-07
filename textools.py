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

import pdb
import os
import re, collections
alphabet = 'abcdefghijklmnopqrstuvwxyz_'
CMP_TYPE = type(re.compile(''))

def re_in(txt, rcmp_iter):
    _len = len(txt)
    return bool([ri for ri in rcmp_iter if ri.match(txt, 0, _len)])

def ensure_parenthesis(reg_exp):
    if reg_exp == '':
        return reg_exp
    if reg_exp[0] != '(' or reg_exp[-1] != ')':
        reg_exp = '(' + reg_exp + ')'
    return reg_exp

def replace_first(txt, rcmp_list, replacements):
    '''returns the first replacement that has a positive match to
    text
        rcmp_list -- list of compiled expressions
        replacements -- list of expressions to replace with
    '''
    
    _len = len(txt)
    assert(len(rcmp_list) == len(replacements))
    try:
        return next((replace[1] for replace in enumerate(replacements)
            if rcmp_list[replace[0]].match(txt, 0, _len)))
    except StopIteration:
        raise ValueError("RegExp not found")

def get_rcmp_list(replacement_list):
    '''given a list of [[regex_str, replace_with], ...]
    returns the values ored together and the list to be 
    used with replace_first'''
    repl = replacement_list
    # format all subs to be in groups
    repl = [(ensure_parenthesis(n[0]), n[1]) for n in repl]
    # pull out the string format for or conversion
    repl_str = (n[0] for n in repl)
    # convert to or for sub matching
    repl_or_re =  re.compile('|'.join(repl_str))
    del repl_str
    
    # pre-compile for use with subfun
    repl_re = [re.compile(n[0]) for n in repl]
    
    # put back together in a replacement list [[re, replacement], ...]
    replace_re = [(repl_re[i], repl[i][1]) 
            for i in range(len(repl))]
    
    return repl_or_re, replace_re

def replace_text_with_list(replacement_list, text):
    '''Uses get_rcmp_list and replace_first to replace the first instances
    of a successful match with their coresponding index. I.e.
    [['a' : 'A'], ['b' : 'B']] would replace all 'a's with 'A's. It is more
    than this though, as the first value can be a regular expression, so you
    could use 'a*' to replace all repetative a's, while simultaniously only
    replacing one b.'''
    repl_or_re, relace_re = get_rcmp_list(replacement_list)
    subfun = subfun(replacement_list = replacement_list)
    return repl_or_re.sub(subfun, text)
    
def group_num(tup):
    '''returns group number of returned re from findall that is not == ""
    returns only first instance found.'''
    return next((n for n in tup if n != ''))

def convert_to_regexp(txt):
    '''converts text into a regexp, handling any special characters'''
    special_chars = r'. ^ $ * + ? { } [ ] \ | ( )'
    special = special_chars.split(' ')
    special_or = '(\\' + ')|(\\'.join(special) +')'
    sfun = subfun(match_set = set(special), prepend = '\\')
    return re.sub(special_or, sfun, txt)

class subfun(object):
    '''General use for use with re.sub. Instead of subsituting text it prepends
    or postpends text onto it and returns it whole. It also stores the text
    it is replacing 
    Input: subfun([replace, [match_set, [prepend, [postpend]]])
        replace == text you want to replace match with
        match_set == if None, prepends / postpends to all text. If a set
            only replaces text that is in this match set
        prepend == text you want to prepend -- only does so if it is in the match set
        postpend == text you want to postpend -- only does so if it is in the match set
    
    stores subbed text in:
        self.subbed
        in the form (text, sub)
        
        sfun = subfun(match_set, subtext, prepend, postpend)
        subbed_text = re.sub(pattern, sfun, text)
    '''
    def __init__(self, replace = None, prepend = '', postpend = '', 
                 match_set = None, replace_list = None):
        self.replace = replace
        self.prepend = prepend
        self.postpend = postpend
        self.match_set = match_set
        self.replace_list = replace_list
        self.subbed = []
        
    def __call__(self, matchobj):
        if matchobj:
            txt = matchobj.group(0)
            start_txt = txt
            if self.replace != None:
                txt = self.replace
            if self.replace_list != None:
                replace_list, replacements = zip(*self.replace_list)
                try:
                    txt = replace_first(txt, replace_list, replacements)
                except ValueError:
                    pass
            if self.match_set == None or txt in self.match_set:
                txt = self.prepend + txt + self.postpend
            self.subbed.append((start_txt, txt))
            return txt

def system_replace_regexp(path, regexp, replace):
    '''A powerful tool that is similar to searchmonkey or other tools...
    but actually works for python regexp! Does user output to make sure
    you want to actually replace everything you said you did.
    '''
    if os.path.isdir(path):
        for f in os.listdir(path):
            new_path = os.path.join(path, f)
            system_replace_regexp(new_path, regexp, replace)
        return
    
    with open(path) as f:
        text = f.read()
    
    rcmp = re.compile(regexp)
    if not rcmp.findall(text):
        print "-- Could not find string on path:", path
        return
    
    mysub = subfun(replace = '')
    start_text = text
    text = rcmp.sub(mysub, text)
    file_msg_start = ('##### About to operate on file < {path} > with the '
        'following Replacements:')
    replaceheader = '\n     --- REPLACE ITEM &&&&&&&&&&&&&&&&&&& \n{orig_text}'
    replace_mid =   '\n     --- WITH ---------------------\n{new_text}'
    
    print file_msg_start.format(path = path)
    for old, new in mysub.subbed:
        print replaceheader.format(orig_text = old),
        print replace_mid.format(new_text = new),
    uin = raw_input("-- IS THIS OK (Y/n):")
    if uin.lower() == 'y':
        print '...REPLACING',
        with open(path, 'w') as f:
            f.write(text)
        print 'DONE\n'
    else:
        print 'not replacing file\n'
    
    print '################################'    
    
'''Some fun general text tools'''
class SpellingCorrector(object):
    '''A very simple spelling corrector, used in GUIs to check user input.'''
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

if __name__ == '__main__':
    pass