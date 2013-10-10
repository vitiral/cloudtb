# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 21:33:45 2013

@author: user
"""
range = xrange

import pdb


# when someone can tell me a better way of doing this, please let me know
from guitools import get_color_from_index, get_color_str
import iteration
import textools

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

span_std = ('', '')

span_template = ('''<span style="{bold}{underlined}{color}'''
'''{lower}">''', '''</span>''')
bold_tplate = ''' font-weight:600; '''
underlined_tplate = ''' text-decoration: underline;'''
color_tplate = ''' color:#{color};'''
lower_tplate = ''' vertical-align:sub;'''

def get_span(underlined = '', bold = '', color = '',
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

def text_format_html(text, span):
    '''formats raw text in html with the given span.
    mostly created to properly handle new lines'''
    if not text:
        return ''
    start = ''
    if text[0] == '\n':
        start = ''.join(paragraph[::-1])
        text = text[1:]
    end = ''
    if text[-1] == '\n':
        end = ''.join(paragraph[::-1])
        text = text[:-1]
    
    text = text.split('\n')
    fmat_front = [paragraph[0], span[0]]
    fmat_back = [span[1], paragraph[1]]
    text = (fmat_front + [t] + fmat_back for t in text)
    text = tuple((iteration.flatten(text)))[1:-1]
    
    return start + ''.join(text) + end

def regpart_format_html(regpart, show_tags_on_replace = False):
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
        span = get_span(bold = True, underlined = True, lower = True)
        match = match_data[0]
        formatted.append(text_format_html('{0}:'.format(match), span))

    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            formatted.append(text_format_html('(', get_span(bold = True, 
                color = colors[i])))
    if replace:
        formatted.append(text_format_html(
            regpart.text, get_span(bold = True, color = std_color)))
    else:
        for data in data_list:
            if type(data) == str:
                formatted.append(text_format_html(data, get_span(bold = True,
                                                        color = std_color)))
            else:
                formatted.extend(regpart_format_html(data))
    
    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            formatted.append(text_format_html(')', get_span(bold = True, 
                             color = colors[i])))
            formatted.append(text_format_html('{0}'.format(indexes[i]),
                             get_span(bold = True, color = colors[i], lower = True)))
    
    if replace:
        formatted.append(text_format_html(replace,
            get_span(bold = True, color = repl_color,
                     underlined = True)))
    
    return formatted

def re_search_format_html(data_list):
    formatted = [header]
    for data in data_list:
        if type(data) == str:
            formatted.append(text_format_html(data, span_std))
        else:
            formatted.append(regpart_format_html(data))
    formatted.append(footer)
    return ''.join(iteration.flatten(formatted))

def dev1():
    import dbe
    import pdb
    from textools import re_search, format_re_search, re_search_replace
    text = '''talking about expecting the Spanish Inquisition in the text below: 
    Chapman: I didn't expect a kind of Spanish Inquisition. 
    (JARRING CHORD - the cardinals burst in) 
    Ximinez: NOBODY expects the Spanish Inquisition! Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry...are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) 
    '''
    regexp = r'''([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish Inquisition(!|.)'''
    repl = r'What is this, the Spanish Inquisition?'
    researched = re_search(regexp, text)
#    replaced = re_search_replace(researched, repl, preview = True)
#    print format_re_search(researched)
    print re_search_format_html(researched)
#    print re_search_format_html(replaced)

