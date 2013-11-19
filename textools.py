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

import pdb
import os
import re
import iteration
import functions

alphabet = 'abcdefghijklmnopqrstuvwxyz_'
CMP_TYPE = type(re.compile(''))

LOWER_LETTER_SET = set((chr(n) for n in xrange(ord('a'), ord('z') + 1)))
UPPER_LETTER_SET = set((chr(n) for n in xrange(ord('A'), ord('Z') + 1)))
WORD_SET = set(('_',))
WORD_SET.update(LOWER_LETTER_SET)
WORD_SET.update(UPPER_LETTER_SET)

def format_re_search(list_data, pretty = False):
    '''Returns a string of researched data that is semi-easy to read.
    If pretty == True then each item starts on it's own line with a '>>| '
    at the front (easier to read)'''
    strings = (str(n) for n in list_data)
    if pretty:
        return '\n>>|'.join(strings)
    else:
        return ''.join(strings)

def get_orig_researched(re_searched):
    '''get original text'''
    return ''.join((n if type(n) in (str, unicode) else n.text for n in 
        re_searched))

def get_str_researched(re_searched):
    '''returns the origional string if replace has not been called,
    else returns the replacement string'''
    return ''.join(get_iter_str_researched(re_searched))

def get_iter_str_researched(re_searched):
    return (n if type(n) in (str, unicode) else n.text if not n.replace_list 
        else n.get_replaced() for n in re_searched)
        
def get_matches(researched):
    '''returns an iterator of only the matches from a re_search output'''
    return (m for m in researched if type(m) != str)

def get_line(text, position, start = 0):
    ''' UNDER DEVELOPMENT
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

def _re_search_yield(regexp, text, start = 0, end = None, 
                     matches = None, no_groups = False):
    '''Internal implementation of re_search that allows for iteration. Use
    re_search with return_type = iter instead
    
    matches = [] if you want it to keep track of matches'''
    if type(regexp) in (str, tuple):
        pat = regexp
    else:
        pat = regexp.pattern

    if pat == '':
        yield text
        raise StopIteration
    
    if end == None:
        end = len(text)
    absolute_end = end
    del end
    
    stop = start
    if type(regexp) == str:    
        regexp = re.compile(regexp)
    if no_groups:
        regex_groups = None
    else:
        regex_groups = get_regex_groups(pat)
    match = 0
    count = 0
    prev_stop = stop
    while stop < absolute_end:
        searched = regexp.search(text, stop, absolute_end)
        
        if searched == None:
#            if not data_list:   # no match found
#r              return 
            break

        count += 1
        if count > absolute_end:
            assert(0)   # prevent infinite loop -- This happened to me and
                        # re_search kept building an infinite tuple.
                        # It ended up consuming almost a gig of memory and
                        # nearly crashed my computer!  Haha, goodtimes
            
        regs = searched.regs
        # overriding a very annoying feature of the re module where somehow
        # these can be different things depending on how the match turns out
        # With the re module this is the ONLY good way to get
        # every group item. groups() doesn't return it, 
        # last_index truncates with None Values... NOTHING is any good.
        # Coming to this solution was WAY more work than it should have
        # been. The re.search function should be MASSIVELY re-worked, it is
        # AWFUL
        get_group = searched.group
        groups = tuple((get_group(i) for i in range(len(regs))))
        span = searched.span()
        start, stop = span
        
        txt = text[prev_stop:start]
        if txt != '':
            yield txt
        if start == stop:
            # Empty match
            stop += 1
            continue
        
        index = iteration.first_index_ne(groups, None)
        new_RegGroupPart = RegGroupPart(groups, regex_groups, index, 
                                        match_data = (match, span, regexp))
        new_RegGroupPart.init(text, regs)
        if matches != None:
            matches.append(new_RegGroupPart)
        yield new_RegGroupPart
        prev_stop = stop
        match += 1

    yield text[stop:]

def re_search(regexp, text, start = 0, end = None, 
              return_matches = None, return_type = tuple,
              no_groups = False):
    '''Research your re!
    
    The same as re.search if you kept performing it after each match for
        the whole text.
    
    This returns a list of text and objects. These objects give you much 
    more information on how your regexp processed the text.
    
    EXAMPLE:
    >>> text = """Researching my re search is really easy with this handy new \
tool! It shows me my matches and group number, I think it is great that  \
they're seen in this new light!"""
    >>> regexp = r'([Rr]e ?se\w*)|(([Tt]h)?is)'  # matches any capitalization
        # of "re se..." where the space is optional, and also will match 
        # "This", "this", or "is"
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
    
    -- For an easier to read format use the function above with pretty = True,
        or use a GUI like Kiki or Search The Sky (Search the Sky uses this
        module and is developed by the same person.)
    
    The actual output of the funcion is a list containing strings and
    RegGroupPart objects of the searched text.
    
    If return_matches is set to true, it returns a list of only the 
    matches as the second variable -- data_list, matches
    
    For easier to read formating, use the GUI tool #TODO: name of gui too
    
    Other outputs:
        If the regexp pattern == '' it just returns the whole string, rather than
        empty strings separated by RegPart objects.
        
        If no match is found, returns None
        
        change return_type to change the output style. list, tuple, and iter
        are supported. If you choose iter and you want it to return the
        matches, then return_matches must equal an empty array (where the
            matches will be stored)
    '''
    if return_type not in (tuple, list, iter):
        raise TypeError("return_type must be tuple, list, or iter function")
        
    if return_type == iter:
        if return_matches or return_matches != []:
            raise TypeError("for iterator return, matches must be None or []")
        itresearch = _re_search_yield(regexp, text, start, end, return_matches,
                            no_groups = no_groups)
        return iter(itresearch)
    elif return_matches:
        matches = []
        itresearch = _re_search_yield(regexp, text, start, end, matches,
                                      no_groups = no_groups)
        return return_type(itresearch), matches
    else:
        return return_type(_re_search_yield(regexp, text, start, end,
                                            no_groups = no_groups))
    
class RegGroupPart(object):
    def __init__(self, groups, reg_groups, index, match_data = None):
        '''
        - groups is all re.group(n)   NOTE: NOT re.search.groups(). See 
            re_search for more information
        - index is the current group index
        - match_data is None unless this is this is the top level match
            match_data = (match_number, span, regexp)
                (group(0))
                - if match_data != None, there is also the text and replace_str
                    attributes.
        '''
        self.groups = groups
        self.reg_groups = reg_groups
        self.indexes = [index]
        self.match_data = match_data
        self.replace_list = None
        self.text = groups[index]
        self.data_list = None
    
    def do_replace(self, replace):
        '''Performs replacement.
        Note: if outside functions modify a value to a type other than None,
        str, or unicode then that group value will not be replaced. This is 
        useful if some function is "deselecting" in between replacement
        updates (like in a gui)'''
        if hasattr(replace, '__call__'):
            replace = replace(self)
        
        if type(replace) in (str, unicode):
            replace = (replace,)
        check_in = set((type(None), str, unicode))
        if self.replace_list != None:
            for i, r in enumerate(replace):
                if type(self.replace_list[i]) in check_in:
                    self.replace_list[i] = r
        else:
            self.replace_list = list(replace)   # make a copy
        [n.do_replace(replace) for n in self.data_list if type(n) != str]
        return self
    
    def get_replaced(self, only_self = False, get_index = False):
        '''get the string after the replacement function has been
        performed'''
        for i in self.indexes:
            if (self.replace_list and 
            type(self.replace_list[i]) in (str, unicode)):
                if get_index:
                    return i, self.replace_list[i]
                else:
                    return self.replace_list[i]
        
        if only_self:
            if get_index:
                return None, None
            else:
                return None
                
        out = ''.join(n if type(n) == str else n.get_replaced() for n in
                self.data_list)
        if get_index:
            return None, out
        else:
            return out
    
    def init(self, text, regs):
        '''
        - text is the outside text
        - regs is a view of the regs starting at itself. it is NOT
            the output of re.search.regs (has to be fixed for this object)
        
        This works by going through the reg tuple and pulling out the strings
        that are relevant to it's own group -- the ones that fall within it's own
        start and end points
        It then stores them as new objects, and stores the text in between as well
        '''
        groups = self.groups
        reg_groups = self.reg_groups
        index = self.indexes[0]
        myreg = regs[index]
        mystart, myend = myreg
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
            
            newregpart = RegGroupPart(groups, reg_groups, index)
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
   
    def __str__(self):
        start, end = '', ''
        if self.match_data != None:
            match = self.match_data[0]
            start = '<*m{0}>[['.format(match)
            end = r']]'
        if self.replace_list:
            replace = None
            len_rl = len(self.replace_list)
            for i in self.indexes:
                if i < len_rl and self.replace_list[i] != None:
                    replace = self.replace_list[i]
                    break
            if replace:
                end += r'==>[[{0}]]'.format(replace)
        str_data = ''.join([str(n) for n in self.data_list])
        return start + '{{{0}}}<g{1}>'.format(str_data, self.indexes) + end
    
    def __repr__(self):
        return object.__repr__(self) + '["""' + str(self) + '"""]'
    
    def group(self, index):
        '''Function so that RegPart can interface with things that use 
        regexp match objects. IMPORTANT: cannot interface the same way with
        the "groups" call'''
        return self.groups[index]
        
def re_in(txt, rcmp_iter):
    _len = len(txt)
    return bool([ri for ri in rcmp_iter if ri.match(txt, 0, _len)])

def ensure_parenthesis(reg_exp):
    if type(reg_exp) != str:
        reg_exp = reg_exp.pattern
    if reg_exp == '':
        return reg_exp
    if reg_exp[0] != '(' or reg_exp[-1] != ')':
        reg_exp = '(' + reg_exp + ')'
    return reg_exp

# TODO: refactor to "replace_all_first"
def replace_first(txt, rcmp_list, replacements):
    '''returns the first replacement that has a positive match to text
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

def _get_regex_groups(itsplit, is_pattern = True):
    '''is_pattern determines whether this level is the top level
    pattern'''
    named_regexp = re.compile('\?(?:P\<.*?\>)|=')    # named groups are the only exception
    glist = []
    parans = 0
    bracks = 0
    
    itsplit = iter(itsplit)
    prev_t = None
    while True:
        try:
            t = next(itsplit)
        except StopIteration:
            assert(is_pattern)
            return glist
        if type(t) in (str, unicode):
            if t:
                glist.append(t)
            continue
        t = t.text
        if t == '(' and prev_t != '\\':
            # We may be in a group
            glist.append(t)
            fit, itsplit = iteration.get_first(itsplit)
            if type(fit) not in (str, unicode):
                fit = fit.text
            if bracks > 0:
                # it is actually inside brackets, not a valid character
                pass
            elif (len(fit) > 0 and fit[0] == '?' and not 
                    named_regexp.match(fit)):
                # it is NOT a group, some special function
                parans += 1
            else:
                itsplit, gl = _get_regex_groups(itsplit, is_pattern = False)
                glist.append(gl)
                glist.append(')')
        elif t == ')' and prev_t != '\\':
            if bracks > 0:
                glist.append(t)
            else:
                assert(parans >= 0)
                if parans == 0:
                    if is_pattern:
                        # if we are the top level pattern then we shouldn't
                        # be encountereing this
                        assert(0)
                    else:
                        # Full group found -- done
                        return itsplit, functions.reform_text(glist)
                else:
                    glist.append(t)
                    parans -= 1
        elif t == '[' and prev_t != '\\':
            if bracks > 0:
                pass    # it is a bracket in a bracket... oh boy
            else:
                glist.append(t)
                bracks += 1
        elif t == ']' and prev_t != '\\':
            assert(bracks == 1)
            glist.append(t)
            bracks -= 1
        else:
            assert(t in ('\\', '\\\\'))
            glist.append(t)
            
def _convert_groups(itgroups, groups = None, top_level = True):
    '''Converts from a list in _get_regex_groups to the actual group list in
    order '''
    lgroups = []
    if top_level:
        assert(groups == None)
        itgroups = iter(itgroups)
        all_groups = []
        groups = []

    for item in itgroups:
        if type(item) in (str, unicode):
            lgroups.append(item)
        else:   # it is a list
            cg = _convert_groups(iter(item), groups = groups, 
                                           top_level= False)
            lgroups.extend(cg)
            if top_level:
                groups.reverse()
                all_groups.extend(groups)
                groups = []
    if top_level:
        all_groups.insert(0, ''.join(lgroups))
        lgroups = all_groups
    else:
        groups.append(''.join(lgroups))
    return lgroups

def get_regex_groups(regexp):
    assert(re.compile(regexp))
    lookahead = r'(?<!\\)'
#    accept_lookahead = r'(?<=\\\\)'
    start_paran = r'[(]'
    end_paran = r'[)]'
    start_brack = r'\['
    end_brack = r'\]'
    double_fslash = r'(\\\\)'
    single_fslash = r'(\\)'
#    fmat = '({0}{{reg}}|{1}{{reg}})'
#    fmat = fmat.format(lookahead, accept_lookahead)
#    fmat = '({0}{{reg}})'.format(lookahead)
    fmat = '({reg})'
    rlist = [double_fslash, single_fslash]    
    rlist.extend([fmat.format(reg = n) for n in 
        (start_paran, end_paran, start_brack, end_brack)])
    greg = ('|').join(rlist)
    greg = re.compile(greg)
        
#    split = greg.split(regexp)
#    list_groups = _get_regex_groups(split)
    researched = re_search(greg, regexp, no_groups = True)
    list_groups = _get_regex_groups(researched)
    return _convert_groups(list_groups)
    
def get_rcmp_list(replacement_list):
    '''given a list of [[regex_str, replace_with], ...]
    returns the values or'ed together and the list to be 
    used with replace_first
    
    returns repl_or_re (call the .sub method directly) 
    and repl_re to be used with subfun'''
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
    repl_or_re, replace_re = get_rcmp_list(replacement_list)
    mysubfun = subfun(replace_list = replace_re)
    return repl_or_re.sub(mysubfun, text)
    
def group_num(tup):
    '''returns group number of returned re from findall that is not == ""
    returns only first instance found.'''
    return next((n for n in tup if n != ''))

def convert_to_regexp(txt, compile = False):
    '''converts text into a regexp, handling any special characters'''
    special_chars = r'. ^ $ * + ? { } [ ] \ | ( )'
    special = special_chars.split(' ')
    special_or = '(\\' + ')|(\\'.join(special) +')'
    sfun = subfun(match_set = set(special), prepend = '\\')
    out = re.sub(special_or, sfun, txt)
    if compile:
        return re.compile(out)
    return out

class subfun(object):
    '''General use for use with re.sub. Instead of subsituting text it prepends
    or postpends text onto it and returns it whole. It also stores the text
    it is replacing 
    Input:
        replace 
            text you want to replace match with
        prepend 
            text you want to prepend -- only does so if it is in the match set
        postpend 
            text you want to postpend -- only does so if it is in the match set
        match_set
            if None, prepends / postpends to all text. If a set
            only replaces text that is in this match set
        replace_list
            a list of [[regexp, replacement], ...] The first item that matches
            regexp will be replaed with replacement
            
    stores subbed text in:
        self.subbed
        in the form (text, sub)
    stores subbed regs (the start_pos, end_pos of subbed text) in:
        self.regs
        
        sfun = subfun(match_set, subtext, prepend, postpend)
        subbed_text = re.sub(pattern, sfun, text)
    '''
    def __init__(self, replace = None, prepend = '', postpend = '', 
                 match_set = None, replace_list = None):
        self.replace = replace
        self.prepend = prepend
        self.postpend = postpend
        self.match_set = match_set
        if replace_list != None:
            self.replace_list, self.replacements = zip(*replace_list)
        else:
            self.replace_list = None
        self.subbed = []
        self.regs = []
        
    def __call__(self, matchobj):
        if matchobj:
            txt = matchobj.group(0)
            start_txt = txt
            if self.replace != None:
                txt = self.replace
            if self.replace_list != None:
                try:
                    txt = replace_first(txt, self.replace_list, 
                                        self.replacements)
                except ValueError:
                    pass
            if self.match_set == None or txt in self.match_set:
                txt = self.prepend + txt + self.postpend
            self.subbed.append((start_txt, txt))
            self.regs.append(matchobj.regs[0])
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

def re_search_replace(researched, repl, preview = True, remove_plain = False,
                      return_type = tuple):
    '''
    
    Given the results from re_search, replace text. Outputs an iterator for
        the results
    
    If repl is a function, then it is called given the RegGroupPart object
    
    if preview = True then it retuns a data_list with the 
        RegPart objects who's .replace_str member has been updated.
        NOTE: If preview = True, this function may affect the original data!!! 
        All it does is add data to the .replace_str values, but this will change 
        the string and formatting outputs.
    
    format functions that handle re_searched data will format this visually
    
    returns a tuple with the replacements. If you just want text, 
    just call ''.join(output).
    
    You can specifiy a different return type by changing return_type (
        iter for an iterator, list for a list, etc)
    '''
    if remove_plain:
        researched = (n for n in researched if type(n) not in (str, unicode))
    
    if preview == False: return_type = iter
    
    out = return_type(n if type(n) in (str, unicode) else n.do_replace(repl) for
            n in researched)
    
    if preview == False:
        return get_str_researched(out)
    
    return out
    
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
    print format_re_search(repl, pretty = True)
    print get_str_researched(repl)
    from extra.richtext import re_search_format_html
    print re_search_format_html(repl)

    
#    replaced = re_search_replace(researched, repl, preview = True)
#    print format_re_search(researched)
    
#    print re_search_format_html(replaced)

def dev_get_groups():
    import dbe
    from pprint import pprint
    regexp = r'\\\\\(not a group, just parans\) but the one here: \\(this is a group\\)'
    print '\n', regexp
    print "Converted:"
    for n in get_regex_groups(regexp):
        print n

def dev1():
    import dbe
    import pdb
    from extra.researched_richtext import re_search_format_html
    from extra.richtext import get_position, deformat_html
    from extra.richtext import get_str_formated_html
    from pprint import pprint
    global out, text, true_position
    text = '''talking about expecting the Spanish Inquisition in the text below: 
    Chapman: I didn't expect a kind of Spanish Inquisition. 
    (JARRING CHORD - the cardinals burst in) 
    Ximinez: NOBODY expects the Spanish Inquisition! Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry...are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) 
    '''
    regexp = r'''([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish Inquisition(!|.)'''
    repl = r'What is this, the Spanish Inquisition?'
    pdb.set_trace()
    researched = re_search(regexp, text)
    print text[10:30]
#    pdb.set_trace()
    out =  re_search_format_html(researched)
    out_str = get_str_formated_html(out)
#    pos = get_position(out, 10)
#    print out_str[pos: pos + 50]
    from bs4 import BeautifulSoup
    global soup, el, htp
    
    htp = deformat_html(out_str, {'font-weight':'600', 'color':'#000000'})
    hform = get_str_formated_html(htp)    
    soup = BeautifulSoup(hform)    
#    print soup.prettify()
    
if __name__ == '__main__':
    dev_get_groups()
    
    