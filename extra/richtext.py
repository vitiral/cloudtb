# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 21:33:45 2013

@author: user
"""
range = xrange

import pdb
import re

import bs4  # Beautiful Soup 4

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

HEADER = ('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" '''
'''"http://www.w3.org/TR/REC-html40/strict.dtd"><html><head>'''
'''<meta name="qrichtext" content="1" /><style type="text/css">'''
'''p, li { white-space: pre-wrap; }</style></head><body style=" '''
'''font-family:'Sans Serif'; font-size:9pt; font-weight:400; '''
'''font-style:normal;">''') # no formatting

FOOTER = '''</body></html>'''

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

def str_html_formatted(html_list):
    return ''.join((str(n) for n in html_list))

def get_position(html_list, text_position = None, html_position = None):
    '''given either a text position or html position, return the other
    position
    So if you give the html_position, you will recieve the text_position
    '''
    # TODO: make it do an average for selecting decorator elements.
    if None not in (text_position, html_position):
        raise ValueError("Can only find one position at at ime")
    cur_html_pos, cur_text_pos = 0, 0
    prev_hpos, prev_tpos = 0, 0
    for textrp in html_list:
        cur_html_pos += len(textrp.html_text)
        cur_text_pos+= len(textrp.true_text)
        if text_position != None and cur_text_pos> text_position:
            break
        elif html_position != None and cur_html_pos > html_pos:
            break
        prev_hpos, prev_tpos = cur_html_pos, cur_text_pos
    
    if text_position:
        if textrp.html_text == textrp.true_text:
            # position is in a plain text part
            out_position = prev_hpos + (text_position - prev_tpos)
        elif textrp.html_text > textrp.true_text:
            # position is inside of html, choose position before.
            out_position = prev_hpos
        else:
            raise ValueError("Position is outside of text length" + 
                str(text_position))
    elif html_position:
        if textrp.html_text == textrp.true_text:
            out_position = prev_tpos + (html_position - prev_hpos)
        elif textrp.html_text > textrp.true_text:
            out_position = prev_tpos
        else:
            raise ValueError("Position is outside of text length" + 
                str(html_position))
    return out_position

class HtmlPart(object):
    '''object to differentiate between standard text and html data for 
    RegParts'''
    def __init__(self, html_text, true_text):
        '''true_text is the base (non - decorative) text of RegPart
        objects'''
        self.html_text = html_text
        self.true_text = true_text
    
    def __repr__(self):
        return self.html_text

def text_format_html(text, html_span_tags, not_plain = False):
    '''Formats a text body taking care of special html characters.
    not_plain means that no text will be counted in the HtmlPart.true_text
    attribute.'''
    if not text:
        return ''
    tag_st, tag_end = html_span_tags
    html_list = [HtmlPart(tag_st, '')]
        
    if text[0] == '\n':
        #TODO: is this the right way to do this?? kind of confusing
        add_html = ''.join(paragraph[::-1])
        add_plain = '' if not_plain else text[0]
        html_list.append(HtmlPart(add_html, add_plain))
        text = text[1:]
        
    add_end = None
    if text[-1] == '\n':
        add_end = True 
        end_html = ''.join(paragraph[::-1])
        end_plain = '' if not_plain else text[-1]
        text = text[:-1]
    
    converted_text, replace_fun  = get_html_converted_and_subfun(text)
    
    subbed_regs = replace_fun.regs
    prev_reg = 0,0
    for i, subbed in enumerate(replace_fun.subbed):
        reg = subbed_regs[i]
        # we now have what was replaced (subbed[0]), what replaced it
        # (subbed[1]) and can easily get the text before it from the
        # coordinates (reg and prev_reg).
     
        # first add the preceeding text
        add_html = text[prev_reg[1]: reg[0]]
        add_plain = '' if not_plain else add_html
        html_list.append(HtmlPart(add_html, add_plain))
        
        # now add own text
        
        add_plain = '' if not_plain else subbed[0]
        add_html = subbed[1]
        html_list.append(HtmlPart(add_html, add_plain))
        
        prev_reg = reg
    if not subbed_regs:# never entered loop! No special characters = no subbed!
        assert(converted_text == text)
        add_plain = '' if not_plain else text
        add_html = text
        html_list.append(HtmlPart(add_html, add_plain))
    
    if add_end:
        add_plain = '' if not_plain else end_plain
        add_html = end_html
        html_list.append(HtmlPart(add_html, add_plain))
    
    html_list.append(HtmlPart(tag_end, ''))
    
    return html_list


deformat_keepif_bold_black = ['font-weight:600', 'color:#000000']

'''
Can use soup.find_all('spans') to get all spans
can use soup.find_all('p') to get all paragrphs


>>> soup.span.strings
<generator object _all_strings at 0x1bae8c0>
>>> list(soup.span.strings)
[u'0:']
>>> s =list(soup.span.strings)
>>> s.index
<built-in method index of list object at 0x1bdc908>
>>> type(s)
<type 'list'>
>>> s = s[0]
>>> type(s)
<class 'bs4.element.NavigableString'>
>>> s.previous_element
<span style=" font-weight:600;  text-decoration: underline; vertical-align:sub;">0:</span>
'''
BODY_REGEXP = r'([\w\W]*<body [\w\W]*?>)([\w\W]*?)(</body>[\w\W]*)'
def get_body_and_span(text):
    ''' returns the body text and the (header, footer)'''
    match = re.match(BODY_REGEXP)
    header, body, footer = [match.group(n) for n in range(1,4)]
    return body, (header, footer)    

PARAGRAPH_REGEXP = '(<p[\w\W]*?>)([\w\W]*?)(</p>)'
def get_paragraphs_regtext(text):
    '''returns a list of paragraphs and regular text'''
    return textools.re_search(PARAGRAPH_REGEXP, text)
    
SPAN_REGEXP = '(<span[\w\W]*?>)([\w\W]*?)(</span>)'
def get_spans_regtext(text):
    '''returns a list of spans (as regparts) and regular text'''
    return textools.re_search(PARAGRAPH_REGEXP, text)

SPAN_ATTRIB_REGEXP = re.compile(r'([\w\W]*?):([\w\W]*?);')
def get_span_attributes(span_text):
    '''given the first element of the span (group(1)), return
    a dict of the attributes (i.e. color, etc)'''
    _dl, matches = textools.re_search(SPAN_ATTRIB_REGEXP, span_text,
                                   return_matches = True)
    span_attribs = dict(((n.group(1), n.group(2)) for n in matches))
    return span_attribs

def get_html_textparts(html, keepif, keep_plain = True):
    '''
    keepif is a dict of attributes to keep. The expression has to be
    either all these attributes or plain to be kept (unless keep_plain == False)
    returns HtmlParts with the .true_text and .html_text set
    appropriately
    
    keepif is a list of lists of regular expression strings to keep inside
    of the span. So keepif = [['color:#ff0000;', 'font-weight:600']] would only keep
    a span if it had both a red color and was bold and NO OTHER attributes.
    '''
    bsoup = bs4.BeautifulSoup(html)
    next_el = bsoup.body.next_element
    html_list = []
    while next_el != None:
        if type(next_el) == bs4.element.NavigableString:
            html_list.append(HtmlPart(next_el.abla))
            html_list.extend(text_format_html(next_el.text, ('', ''),
                not_plain = not keep_plain))
        elif next_el.name == 'span':
            pass
        elif next_el.name == 'p':
            pass
        else:
            raise IOError("unrecognized element: " + next_el)
        next_el = next_el.next_element
        
#    for paragraph in bsoup.find_all('p'):
#        pdb.set_trace()
    