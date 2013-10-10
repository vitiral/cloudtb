# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 21:33:45 2013

@author: user
"""
range = xrange

import pdb
import re

from guitools import get_color_from_index, get_color_str

try:
    from .. import iteration, textools
except ValueError:
    import iteration, textools

# replace list going from regular text to html
html_replace_list = [
[r'<'    ,r'&lt;'],
[r'>'    ,r'&gt;'],
[r'\&'   ,r'&amp;'],
[r'"'    , r'&quot'],
['\n'    , r'<\p><p>'], # develper must handle first and last '\n' characters 
                        #when subbing!
]
html_replace_list = [(textools.convert_to_regexp(n[0], compile = True), n[1]) 
    for n in html_replace_list]

header = ('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" '''
'''"http://www.w3.org/TR/REC-html40/strict.dtd"><html><head>'''
'''<meta name="qrichtext" content="1" /><style type="text/css">'''
'''p, li { white-space: pre-wrap; }</style></head><body style=" '''
'''font-family:'Sans Serif'; font-size:9pt; font-weight:400; '''
'''font-style:normal;">''') # no formatting

footer = '''</body></html>'''

paragraph = ('''<p style=" margin-top:0px; margin-bottom:0px; '''
'''margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">'''
, '''</p>''')

html_span_std = ('', '')

span_template = ('''<span style="{bold}{underlined}{color}'''
'''{lower}">''', '''</span>''')
bold_tplate = ''' font-weight:600; '''
underlined_tplate = ''' text-decoration: underline;'''
color_tplate = ''' color:#{color};'''
lower_tplate = ''' vertical-align:sub;'''

CMP_NEWLINE = re.compile('\n')

def get_html_span_tags(underlined = '', bold = '', color = '',
                    lower = ''):
    if bold:
        bold = bold_tplate
    if underlined:
        underlined = underlined_tplate
    if color:
        if type(color) != str:
            color = get_color_str(color = color)
        color = color_tplate.format(color = color)
    if lower:
        lower = lower_tplate
    return (span_template[0].format(bold = bold, underlined = underlined, 
              color = color, lower = lower), span_template[1])

def get_html_converted_and_subfun(text):
    repl_or_re, repl_re = textools.get_rcmp_list(html_replace_list)
    replace_fun = textools.subfun(replace_list = repl_re)
    converted_text = repl_or_re.sub(replace_fun, text)
    return converted_text, replace_fun
    
def text_format_html_find_true_position(text, true_position):
    '''May look a bit confusing but this function is doing alot. It:
        replaces text
        adds the replacement lengths until it gets above true pos
        finds the actual pos and updates the true_position input
    '''
    class StopAdding(Exception):
        pass
    
    def add_plain_html(add_plain, add_html):
        '''returns True when true position reached'''
        target, plain, html = true_position
        plain += add_plain
        if plain > target:
            raise StopAdding
        add_html += add_html
        true_position[1] = plain
        true_position[2] = html
    
    assert(len(true_position) != 1)
    
    set_true_pos = None
    converted_text = None
    try:
        end = ''
        if text[-1] == '\n':
            end = ''.join(paragraph[::-1])
            text = text[:-1]
            add_end = True
        start = ''
        if text[0] == '\n':
            start = ''.join(paragraph[::-1])
            text = text[1:]
            aplain, ahtml = 1, len(start)
            add_plain_html(aplain, ahtml)
        
        converted_text, replace_fun  = get_html_converted_and_subfun(text)
        
        subbed_regs = replace_fun.regs
        prev_reg = 0,0
#        pdb.set_trace()
        for i, subbed in enumerate(replace_fun.subbed):
            reg = subbed_regs[i]
            # we now have what was replaced (subbed[0]), what replaced it
            # (subbed[1]) and can easily get the text before it from the
            # coordinates (reg and prev_reg). We are trying to count plain 
            # until it is == find_position, then set the counted html to 
            # that variable. The process automatically br
         
            # first add the preceeding text
            toadd = reg[0] - prev_reg[1]       
            aplain, ahtml = toadd, toadd 
            add_plain_html(aplain, ahtml)
            
            # now add own text
            aplain, ahtml = len(subbed[0]), len(subbed[1])
            add_plain_html(aplain, ahtml)
            
            prev_reg = reg
        else:
            # never entered loop! No special characters = no subbed!
            assert(converted_text == text)
            aplain, ahtml = (len(text),) * 2
            add_plain_html(aplain, ahtml)
        
        if end:
            aplain, ahtml = 1, len(add_end)
            add_plain_html(aplain, ahtml)
            
    except StopAdding:
        if converted_text == None:
            converted_text = get_html_converted_and_subfun(text)[0]
        # find actual cursor with aplain and ahtml
        get_true_pos, prev_plain_pos, prev_html_pos = true_position
        if aplain == ahtml:
            # StopAdding occured while adding standard text
            attempted_pos_html = prev_html_pos + ahtml
            set_true_pos = attempted_pos_html - (get_true_pos - prev_plain_pos)
        elif ahtml > aplain:
            # StopAdding occured inside of html, choose position before.
            set_true_pos = prev_html_pos
        else:
            assert(pdb.set_trace())
    
    if set_true_pos:
        assert(len(true_position) == 3)
        true_position.pop()
        true_position[1] = set_true_pos
    return converted_text
    
def text_format_html(text, html_span_tags, true_position = None):
    '''formats raw text into html with the given html_span_tags.
    mostly created to properly handle new lines'''
    if not text:
        return ''
    
    if true_position and len(true_position) != 2:
        # len == 2 indicates it is done
        converted_text = text_format_html_find_true_position(text, 
                                                             true_position)
    else:
        converted_text = get_html_converted_and_subfun(text)[0]
    
    tag_st, tag_end = html_span_tags
    return tag_st + converted_text + tag_end

def regpart_format_html(regpart, show_tags_on_replace = False, 
                        true_position = None):
    data_list, indexes, groups, match_data = (regpart.data_list, regpart.indexes,
        regpart.groups, regpart.match_data)
    if regpart.match_data:
        replace = regpart.replace_str
        if replace:
            repl_color = get_color_str(0,0,0)
            std_color = get_color_str(255, 0, 0)
        else:
            std_color = get_color_str(0,0,0)
    else:
        replace = None
        std_color = get_color_str(0,0,0)
    
    colors = [get_color_from_index(i, len(groups)) for i in indexes]
    formatted = []
    
    # front formatting
    if (match_data != None and 
            (show_tags_on_replace == True or replace == None)):
        html_span_tags = get_html_span_tags(bold = True, underlined = True, lower = True)
        match = match_data[0]
        formatted.append(text_format_html('{0}:'.format(match), html_span_tags))

    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            formatted.append(text_format_html('(', get_html_span_tags(
                bold = True, color = colors[i])))
    if replace:
        formatted.append(text_format_html(
            regpart.text, get_html_span_tags(bold = True, color = std_color)))
    else:
        for data in data_list:
            if type(data) == str:
                formatted.append(text_format_html(data, get_html_span_tags(bold = True,
                                color = std_color), 
                                true_position = true_position))
            else:
                formatted.extend(regpart_format_html(data,
                                 true_position = true_position))
    
    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            formatted.append(text_format_html(')', get_html_span_tags(bold = True, 
                             color = colors[i])))
            formatted.append(text_format_html('{0}'.format(indexes[i]),
                             get_html_span_tags(bold = True, color = colors[i], lower = True)))
    
    if replace:
        formatted.append(text_format_html(replace,
            get_html_span_tags(bold = True, color = repl_color,
                     underlined = True)))
    
    return formatted

def re_search_format_html(data_list, true_position = None):
    '''true_position can be an array that contains a single integer. This
    function will keep track of the character lengths of raw (unformated)
    text and append the position in html code where len(raw_text) == 
    true_position onto true_position'''
    formatted = [header]
    if true_position:
        typeerror = TypeError("True position must be a list "
                    "with an int as first item")
        if type(true_position) != list:
            raise typeerror
        if len(true_position) != 1:
            raise ValueError("True position can only be a single item list")
        if type(true_position[0]) != int:
            raise typeerror
            
        # set up true position as needed_position, plain_text_pos, html_pos
        true_position.extend((0, len(header)))
    for data in data_list:
        if type(data) == str:
            formatted.append(text_format_html(data, html_span_std, 
                true_position = true_position))
        else:
            formatted.append(regpart_format_html(data,
                    true_position = true_position))
    formatted.append(footer)
    return ''.join(iteration.flatten(formatted))

