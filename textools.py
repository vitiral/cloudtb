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
import iteration
import StringIO

from simple_classes import File, Folder
alphabet = 'abcdefghijklmnopqrstuvwxyz_'
CMP_TYPE = type(re.compile(''))

import itertools

def format_re_search(list_data):
    return ''.join([n if type(n) == str else repr(n) for n in list_data])

def get_original_str(re_searched):
    return ''.join([str(n) for n in re_searched])

def get_matches(researched):
    '''returns an iterator of only the matches from a re_search output'''
    return (m for m in researched if type(m) != str)
    
class ReseachedInfo:
    # reduces the re_search output to it's core important data
    # mostly used for gui functions.
    def __init__(self, researched, original_text):
        self.matches = tuple((ReducedRegPart(m, original_text) 
            for m in get_matches(researched)))

def get_line(text, position, start = 0):
    '''
    returns what line the position is on in the text between the start
    and position'''
    pos = start
    find = text.find
    line = 0
    while pos != -1:
        pos =  find('\n', pos) + 1
        if pos > position:
            return line
        line += 1
    if position > len(text):
        raise IndexError("position is outside of bounds of text")
    return line - 1
    
class ReducedRegPart:
    def __init__(self, regpart, original_text, 
                 last_line = 0, last_end = 0):
        self.text = regpart.text
        self.start = regpart.span[0]
    
    def update_line(self, original_text, last_line = 0,
                    last_end = 0):
        self.line = get_line(original_text, self.start, 
                             start = last_end)
        return self.start + len(self.text) # return end for next call.

def get_match_paths(folder_path, 
                    file_regexp = None, text_regexp = None, 
                    recurse = True, 
                    max_len_searched = None,
                    watchers = None):
    '''get the file paths in a folder that have text which matches
    the regular expression.
    Watchers should be a list of watchers to be called on each new file name
    '''
    if (file_regexp, text_regexp) == (None, None):
        raise ValueError('Must specify at least one regex!')
    if file_regexp != None:
        if type(file_regexp) in (str, unicode):
            file_regexp = re.compile(file_regexp)
        file_fnd = file_regexp.finditer
    if text_regexp != None:
        if type(text_regexp) in (str, unicode):
            text_regexp = re.compile(text_regexp)
        text_fnd = text_regexp.finditer
        
    folder_path = os.path.abspath(folder_path)
    
    fpaths = []
    for fname in os.listdir(folder_path):
        path = os.path.join(folder_path, fname)
        if watchers:
            [w(path) for w in watchers]

        if os.path.isdir(path):
            fpaths.extend(get_match_paths(folder_path,
                file_regexp, text_regexp, recurse, 
                max_len_searched))

        if file_regexp:
            try:
                next(file_fnd(fname))
            except StopIteration:
                continue
        
        if text_regexp:
            with open(path) as f:
                #TODO: check if file is a text file
                try:
                    next(text_fnd(f.read(), 0, max_len_searched))
                    fpaths.append(path)
                except StopIteration:
                    continue
        else:
            fpaths.append(path)
    
    return fpaths
        
def re_search(regexp, text, start = 0, end = None, return_matches = False):
    '''Research your re!
    
    The same as re.search except returns a list of text and objects.
    These objects give you much more information on how your regexp
    processed the text.
    
    EXAMPLE:
    >>> text = """Researching my re search is really easy with this handy new \
tool! It shows me my matches and group number, I think it is great that  \
they're seen in this new light!"""
    >>> regexp = r'([Rr]e ?se\w*)|(([Tt]h)?is)'  # matches any capitalization
        # of "re se..." where the space is optional, and also will match This, 
        # this, or is
    >>> researched = re_search(regexp, text)
    >>> print format_re_search(researched)
<*m0>[[{Researching}<g0>]] my <*m1>[[{re search}<g0>]] <*m2>[[{is}<g1>]] really
 easy with <*m3>[[{this}<g1>]] handy new tool! It shows me my matches and group
 number, I think it <*m4>[[{is}<g1>]] great that  they'<*m5>[[{re seen}<g0>]]
 in <*m6>[[{this}<g1>]] new light!
     
    Analyzing Output:
        The re_search function formats the output into a (semi) easy to read
        format as follows:
        <*m#>[[match_text]] - This is the text you would get from re.findall, 
                                where the # is the index you would get.
        {group_text}<g#>    - This is the text of the group inside the match, 
                                with the coresponding group number (#).
    
    The actual output of the funcion is a list containing strings and
    RegGroupPart objects of the searched text.
    
    If return_matches is set to true, it returns a list of only the 
    matches as the second variable -- data_list, matches
    
    For easier to read formating, use the GUI tool #TODO: name of gui tool
'''
    if end == None:
        end = len(text)
    absolute_end = end
    del end
    
    stop = start
    if type(regexp) == str:    
        regexp = re.compile(regexp)
    data_list = []
    matches_list = []
    match = 0
    prev_stop = stop
    while stop < absolute_end:
        searched = regexp.search(text, stop, absolute_end)
        if searched == None:
            if not data_list:   # no match found
                return None
            break
        group_0 = searched.group(0)
        groups = searched.groups()
        se = searched
        pdb.set_trace()
        if group_0 != groups[0]:
            # overriding a very annoying feature of the re module where somehow
            # these can be different things
            groups = (group_0,) + groups
        span = searched.span()
        start, stop = span
        
        data_list.append(text[prev_stop:start])
        
        index = iteration.first_index_ne(groups, None)
        new_RegGroupPart = RegGroupPart(groups, index, 
                                        match_data = (match, span, regexp))
        
        upd_val, null = new_RegGroupPart.update()
        assert(upd_val == len(groups))
        matches_list.append(new_RegGroupPart)
        data_list.append(new_RegGroupPart)
        assert(get_original_str(data_list) == text[:stop])
        prev_stop = stop
        match += 1
    
    data_list.append(text[stop:])
    if return_matches:
        return data_list, matches_list
    else:
        return data_list
    
class RegGroupPart(object):
    def __init__(self, groups, index, match_data = None):
        ''' match_data = match_num, span (in outside tex), and regcmp 
        it only exists for the outside match (not internal groups)'''
        self.groups = groups
        self.index = index
        self.text = groups[index]
        self.data_list = None
        self.match_data = match_data
        self.is_updated = False
    
    def update(self):
        '''Goes through it's own text and figures out if there
        are any groups inside of itself. Returns the index + 1 of the
        last group it finds'''
        assert(not self.is_updated)
        text, groups = self.text, self.groups
        data_list = []
        end_i = 0
        # recursive function. The index increments on each call to itself
        index = self.index + 1
        while index < len(groups):
            if self.match_data:
                pdb.set_trace()
            gtxt = groups[index]
            if gtxt == None:
                index += 1
                continue
            begin_i = text.find(gtxt, end_i) #+1 if end_i != 0 else 0)
            if begin_i == -1:
                assert(end_i == 0)
                assert(len(data_list) == 0)
                if text == '.':
                    pdb.set_trace()
                data_list = [text]
                end_i = len(text)
                break
            data_list.append(text[end_i:begin_i]) # append raw text in between
            end_i = begin_i
            new_RegGroupPart = RegGroupPart(groups, index)
            index, end_i_obj = new_RegGroupPart.update()
            end_i += end_i_obj
            data_list.append(new_RegGroupPart)
        else:   # loop ended on it's own, cleanup.
            if not data_list:   # you never even entered the loop
                data_list = [text]
            else:# need to add final bits of text.
                data_list.append(text[end_i:])
            end_i = len(text)   # all text processed
            
        self.is_updated = True
        self.data_list = [n for n in data_list if n != '']
        assert(get_original_str(self.data_list) == self.text)
        return index, end_i
    
    def __repr__(self):
        start, end = '', ''
        if self.match_data != None:
            match = self.match_data[0]
            start = '<*m{0}>[['.format(match)
            end = r']]'
        str_data = ''.join([str(n) for n in self.data_list])
        return start + '{{{0}}}<g{1}>'.format(str_data, self.index) + end

    def __str__(self):
        return self.text

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

def dev_research():
    import dbe
    text = ("Researching my re search is really easy with this handy new tool! "
        "It shows me my matches and group number, I think it is great that  "
        "they're seen in this new light!")
    regexp = r'((R|r)e ?se\w*)|(((T|t)h)?is)'
    researched = re_search(regexp, text)
    print researched, '\n'
    print format_re_search(researched)
    print '\n', 'HTML', '\n'
    from richtext import re_search_format_html
    print re_search_format_html(researched)

if __name__ == '__main__':
    dev_research()
    