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
#    all copies or substantial portions of the Softwainre.
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
        regs = searched.regs
        # overriding a very annoying feature of the re module where somehow
        # these can be different things depending on how the match turns out
#        if searched.lastindex != len(groups):
#            groups = (searched.group(0),) + groups
        get_group = searched.group
        
        # yup, with the re module this is the ONLY good way to get
        # every group item. groups() doesn't return it, 
        # last_index truncates with None Values... NOTHING is any good.
        # Comming to this solution was WAY more work than it should have
        # been. The re.search function has to be MASSIVELY re-worked.
        groups = tuple((get_group(i) for i in range(len(regs))))
        
        span = searched.span()
        start, stop = span
        
        data_list.append(text[prev_stop:start])
        
        index = iteration.first_index_ne(groups, None)
        new_RegGroupPart = RegGroupPart(groups, index, 
                                        match_data = (match, span, regexp))
        new_RegGroupPart.init(text, regs)
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
        '''
        - groups is all re.group(n)   NOTE: NOT re.search.groups()
        - index is the current group index
        - match_data is only given if this is the whole match
        '''
        self.groups = groups
        self.indexes = [index]
        self.text = groups[index]
#        self.match_start = match_start
        self.match_data = match_data
        if match_data:
            self.replace_str = None
        self.data_list = None
    
    def do_replace(self, replace_str):
        '''Mostly for use with compressions'''
        self.replace_str = replace_str
        return self
    
    def init(self, text, regs):
        '''
        - text is the outside text
        - regs is a view of the regs starting at itself. it is NOT
            the output of re.search.regs (has to be fixed for this object)
        '''
        groups = self.groups
        index = self.indexes[0]
        myreg = regs[index]
        mystart, myend = myreg
        ''' This works by going through the reg tuple and pulling out the strings
        that are relevant to it's own group -- the ones that fall within it's own
        start and end points
        It then stores them as new objects, and stores the text in between as well'''
        data_list = []
        index += 1
        len_regs = len(regs)
#        pdb.set_trace
        prev_end = mystart
        while index < len_regs:
#            if self.indexes[0] == 0:
#                pdb.set_trace()
            reg = regs[index]
            check_start, check_end = reg
            if check_start < 0:
                index += 1
                continue
            if reg == myreg:
                self.indexes.append(index)
                index += 1
                continue
            if check_start >= myend and check_end > myend:
                break
            assert(check_start >= mystart and check_end <= myend)
            cur_start, cur_end = check_start, check_end
            
            if not prev_end > cur_start and prev_end != cur_start:
                data_list.append(text[prev_end:cur_start])
            
            newregpart = RegGroupPart(groups, index)
            converted = newregpart.init(text, regs)
            data_list.append(newregpart)
            index += converted
            prev_end = regs[index-1][1]
            
        if not data_list:
            data_list.append(text[mystart:myend])
        else:
            if cur_end != myend:
                data_list.append(text[cur_end:myend])
        self.reg = myreg
        self.data_list = data_list
        return len(data_list)
   
    def __repr__(self):
        start, end = '', ''
        if self.match_data != None:
            match = self.match_data[0]
            start = '<*m{0}>[['.format(match)
            end = r']]'
            replace = self.replace
            if replace:
                end += r'==>[[{0}]]'.format(replace)
        str_data = ''.join([n if type(n) == str else repr(n) for n in self.data_list])
        return start + '{{{0}}}<g{1}>'.format(str_data, self.indexes) + end

    def __str__(self):
        return self.text
    
    def group(self, index):
        '''Function so that RegPart can interface with things that use 
        regexp match objects. IMPORTANT: cannot interface the same way with
        the "groups" call'''
        return self.groups[index]
        
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

def re_search_replace(researched, repl, preview = False):
    '''Given the results from re_search, replace text.
    If repl is a function, then it is called given the groups data
    if preview = True then it retuns a data_list with the 
    RegPart objects who's .replace_str member has been updated.
    
    format functions that handle re_searched data will format this visually
    
    returns an iterator with the replacements. If you just want text, 
    just call ''.join(output)
    '''
    if type(repl) in (str, unicode):
        if preview == False:
            return (n if type(n) in (str, unicode) else repl for n in researched)
        else:
            return (n if type(n) in (str, unicode) else n.do_replace(repl)
                for n in researched)
    raise NotImplemented()
    
def dev_research():
    import dbe
    text = ("""Researching my re search is really easy with this handy new tool!
 It shows me my matches and group number, I think it is great that
 they're seen in this new light!""")
    regexp = r'((R|r)e ?se\w*)|(((T|t)h)?is)'
#    text = '''talking about expecting the Spanish Inquisition in the text below: 
#    Chapman: I didn't expect a kind of Spanish Inquisition. 
#    (JARRING CHORD - the cardinals burst in) 
#    Ximinez: NOBODY expects the Spanish Inquisition! Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry...are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) 
#    '''
#    regexp = r'''([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish Inquisition(!|.)'''
    
    import sys
    researched = re_search(regexp, text)
#    print format_re_search(researched)
#    print '\n', 'HTML', '\n'
    
    get_repl = re_search_replace(researched, 'HELLO', preview = True)
    
    repl = list(get_repl)
    pdb.set_trace()
    print ''.join(get_repl)
    from extra.richtext import re_search_format_html
#    print re_search_format_html(researched)

if __name__ == '__main__':
    dev_research()
    