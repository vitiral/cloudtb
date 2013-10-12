# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 21:33:45 2013

@author: user
"""
range = xrange

import pdb
import re

try:
    import bs4  # Beautiful Soup 4
except ImportError:
    pass        # some functions will work without bsoup. It is up to
                # developers to make sure dependencies are met

from guitools import get_color_from_index, get_color_str

try:
    from .. import iteration, textools
except ValueError:
    import iteration, textools

# replace list going from regular text to html

HEADER = ('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" '''
'''"http://www.w3.org/TR/REC-html40/strict.dtd"><html><head>'''
'''<meta name="qrichtext" content="1" /><style type="text/css">'''
'''p, li { white-space: pre-wrap; }</style></head><body style=" '''
'''font-family:'Sans Serif'; font-size:9pt; font-weight:400; '''
'''font-style:normal;">''') # no formatting

FOOTER = '''</body></html>'''

PARAGRAPH_SPAN = ('''<p style=" margin-top:0px; margin-bottom:0px; '''
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

#TODO: removed wordtex compatibility with the & symbol!
html_replace_str_list = [
[r'<'    ,r'&lt;'],
[r'>'    ,r'&gt;'],
#[r'\&'  ,r'&amp;'],
[r'&'    ,r'&amp;'],
[r'"'    , r'&quot'],
['\n'    , ''.join(PARAGRAPH_SPAN[::-1])], 
         # NOTE: develper must handle first and last '\n' characters 
         # when subbing!
]
html_replace_list = [(textools.convert_to_regexp(n[0], compile = True), n[1]) 
    for n in html_replace_str_list]
    
def get_str_html_formatted(html_list):
    '''get the standard string of an html_list return'''
    return ''.join((str(n) for n in html_list))
    
def get_position(html_list, text_position = None, html_position = None):
    '''given either a text position or html position, return the other
    position
    For instance, if you give the html_position, you will recieve the 
    text_position
    '''
    # TODO: make it do an average for selecting decorator elements.
    if text_position == None and html_position == None:
        raise TypeError("Must find at least one position")
    if text_position != None and html_position != None:
        raise TypeError("Can only find one position at a time")
    cur_html_pos, cur_text_pos = 0, 0
    prev_hpos, prev_tpos = 0, 0
    for textrp in html_list:
        cur_html_pos += len(textrp.html_text)
        cur_text_pos+= len(textrp.true_text)
        if text_position != None and cur_text_pos> text_position:
            break
        elif html_position != None and cur_html_pos > html_position:
            break
        prev_hpos, prev_tpos = cur_html_pos, cur_text_pos
    
    if text_position != None:
        if textrp.html_text == textrp.true_text:
            # position is in a plain text part
            out_position = prev_hpos + (text_position - prev_tpos)
        elif textrp.html_text > textrp.true_text:
            # position is inside of html, choose position before.
            out_position = prev_hpos
        else:
            raise ValueError("Position is outside of text length" + 
                str(text_position))
    elif html_position != None:
        if textrp.html_text == textrp.true_text:
            out_position = prev_tpos + (html_position - prev_hpos)
        elif textrp.html_text > textrp.true_text:
            out_position = prev_tpos
        else:
            raise ValueError("Position is outside of text length" + 
                str(html_position))
    else: assert(False)    

    return out_position

KEEPIF = {
'black-bold': {'font-weight':'600', 'color':'#000000'},

}
def deformat_html(html, keepif, keep_plain = True):
    '''
    "Deformats" an html into HtmlParts that are dependent on the keepif
        variable. This allows you to get absolute position of decorated text.
        (i.e. if you only want plain and black bold text, then 
        keepif = {'font-weight':'600', 'color':'#000000'})
        
    keepif is a dict of attributes to keep. 
    For the expression to be kept, it has to match either ALL
    these attributes or be plain text (unless keep_plain == False)
    
    returns HtmlParts with the .true_text and .html_text set
    appropriately
    '''
    header, footer = get_headfoot(html)
    
    bsoup = bs4.BeautifulSoup(html)
    next_el = bsoup.body.next_element
    html_list = [HtmlPart(header, '')]
    while next_el != None:
        if type(next_el) == bs4.element.NavigableString:
            # at first I was kind of upset that bsoup couldn't give
            # me the raw html. Then I realized that I can just use
            # my own function to get it... and everything else!
            html_list.extend(text_format_html(str(next_el), ('', ''),
                not_plain = not keep_plain))
        
        elif next_el.name == 'span':
            next_el, hlist = html_process_span(next_el, keepif, keep_plain)
            html_list.extend(hlist)
            
        elif next_el.name == 'p':
            next_el, hlist = html_process_paragraph(next_el, keepif, 
                                                    keep_plain)
            html_list.extend(hlist)
        else:
            raise IOError("unrecognized element: " + next_el)
        next_el = next_el.next_element
    html_list.append(HtmlPart(footer, ''))
    # remove empty HtmlParts
    html_list = (n for n in html_list if bool(n))
    return tuple(html_list)

class HtmlPart(object):
    '''object to differentiate between standard text and html data for 
    RegParts'''
    def __init__(self, html_text, true_text):
        '''true_text is the base (non - decorative) text of RegPart
        objects'''
        self.html_text = html_text
        self.true_text = true_text
    
    def __str__(self):
        return self.html_text
    
    def __eq__(self, other):
        if (self.html_text == other.html_text) and (self.true_text == 
                other.true_text):
            return True
        else:
            return False
    
    def __bool__(self):
        return bool(self.html_text + self.true_text)
        
''' Internal functions'''
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

def text_format_html(text, html_span_tags, not_plain = False):
    '''Formats a text body taking care of special html characters.
    not_plain means that no text will be counted in the HtmlPart.true_text
    attribute.'''
    if not text:
        return ''
    tag_st, tag_end = html_span_tags
    html_list = [HtmlPart(tag_st, '')]
        
    if text[0] == '\n':
        add_html = ''.join(PARAGRAPH_SPAN[::-1])
        add_plain = '' if not_plain else text[0]
        html_list.append(HtmlPart(add_html, add_plain))
        text = text[1:]
        
    add_end = None
    if text[-1] == '\n':
        add_end = True 
        end_html = ''.join(PARAGRAPH_SPAN[::-1])
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

BODY_REGEXP = r'([\w\W]*<body [\w\W]*?>)([\w\W]*?)(</body>[\w\W]*)'
def get_headfoot(text):
    ''' returns the body text and the (header, footer)'''
    match = re.match(BODY_REGEXP, text)
    header, body, footer = [match.group(n) for n in range(1,4)]
    return header, footer   

NAMED_FRONT_BACK_REGEXP = '(<{name}[\w\W]*?>)([\w\W]*?)(</{name}>)'
def get_named_body_frontback(text, name):
    regcmp = re.compile(NAMED_FRONT_BACK_REGEXP.format(name = name))
    match =  regcmp.match(text)
    front, body, back = [match.group(n) for n in range(1,4)]
    return body, (front, back)
    
SPAN_ATTRIB_REGEXP = re.compile(r'([\w\W]*?):([\w\W]*?);')
def get_style_attributes(span_text):
    '''given the first element of the span (group(1)), return
    a dict of the attributes (i.e. color, etc)'''
    _dl, matches = textools.re_search(SPAN_ATTRIB_REGEXP, span_text,
                                   return_matches = True)
    span_attribs = dict(((str(n.group(1).strip()), 
                          str(n.group(2).strip())) 
                          for n in matches))
    return span_attribs

def html_process_span(bs_span, keepif, keep_plain):
    '''proceses the span given the span element. Returns the 
    the next element to call .next_element on and html_list'''
    text_element = bs_span.next_element
    if type(text_element) != bs4.element.NavigableString:
        text_element = None
    
    style = bs_span.attrs['style']
    style_attrs = get_style_attributes(style)
    if len(keepif) != len(style_attrs):
        do_keep = False
    else:
        for key, value in keepif.iteritems():
            key, value = key.strip(), value.strip()
            if key not in style_attrs or style_attrs[key] != value:
                do_keep = False
                break
        else:
            do_keep = True
    
    body, fback = get_named_body_frontback(str(bs_span), 'span')
    span_front, span_back = fback; del fback
    span_front, span_back = HtmlPart(span_front, ''), HtmlPart(span_back, '')
    html_list = [span_front]
    
    append_text = text_element if text_element != None else ''
    html_list.extend(text_format_html(append_text, ('', ''), not_plain = 
        not do_keep))
    if text_element != None:
        out_elem = text_element
    else:
        out_elem = bs_span
    
    html_list.append(span_back)
    return out_elem, html_list

def html_process_paragraph(bs_paragraph, keepif, keep_plain):
    body, fback = get_named_body_frontback(str(bs_paragraph), 'p')
    front, back = fback; del fback
    front = HtmlPart(front, '')
    back = HtmlPart(back, '\n')
    
    html_list = [front]
    prev_el = bs_paragraph; del bs_paragraph
    next_el = prev_el
    while True:
        next_el = next_el.next_element
        if type(next_el) != bs4.element.NavigableString and (
            next_el == None or next_el.name == 'p'):
            # next element is another paragraph! (or end of body)
            out_el = prev_el
            html_list.append(back)
            break
        elif type(next_el) == bs4.element.NavigableString:
            html_list.extend(text_format_html(str(next_el), ('', ''), not_plain =
                not keep_plain))
            next_el = next_el
        else:
            assert(next_el.name == 'span')
            next_el, hlist = html_process_span(next_el, keepif, keep_plain)
            html_list.extend(hlist)
            next_el = next_el
        prev_el = next_el
        
    html_list.append(back)
    return out_el, html_list
