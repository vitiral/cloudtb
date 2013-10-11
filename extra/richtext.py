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

HEADER = header = ('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" '''
'''"http://www.w3.org/TR/REC-html40/strict.dtd"><html><head>'''
'''<meta name="qrichtext" content="1" /><style type="text/css">'''
'''p, li { white-space: pre-wrap; }</style></head><body style=" '''
'''font-family:'Sans Serif'; font-size:9pt; font-weight:400; '''
'''font-style:normal;">''') # no formatting

FOOTER = footer = '''</body></html>'''

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



