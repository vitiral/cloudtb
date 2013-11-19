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
# -*- coding: utf-8 -*-

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
    try:
        import iteration, textools
    except ImportError:
        import sys
        sys.path.insert(1, '..')
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

EMPTY_PARAGRAPH = ('''<p style=" -qt-paragraph-type:empty; '''
'''margin-top:0px; margin-bottom:0px; '''
'''margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">'''
)

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
[r'"'    , r'&quot;'],
['\n'    , ''.join(PARAGRAPH_SPAN[::-1])], # ALWAYS make sure this 
                                           #is the last line!
]                                # The application depends on it!
         # NOTE: develper must handle first and last '\n' characters 
         # when subbing!

html_replace_str_dict = dict(html_replace_str_list)

html_replace_list = [(textools.convert_to_regexp(n[0], compile = True), n[1]) 
    for n in html_replace_str_list]
    
def get_str_formated_html(html_list):
    '''get the standard string of an html_list return'''
    return ''.join((n.html_text for n in html_list))

def get_str_formated_visible(html_list):
    return ''.join(n.visible_text for n in html_list)

def get_str_formated_true(html_list):
    return ''.join(n.true_text for n in html_list)

def get_str_plain_html(text):
    html_list = text_format_html(text, (HEADER, FOOTER))
    return get_str_formated_html(html_list)

def _check_html_text_equal(html, text):
    '''checks if an html and text string are identitical, taking into account
    special characters.'''
    if html == text:
        return True
    try:
        if html_replace_str_dict[text] == html:
            return True
    except KeyError:
        pass
    return False

def _get_text_positions(html_list, hpart_index, hpart_relpos, len_text):
    '''A more advanced function that can take the ouputs from get_position
    and reconstruct any text between some posiions'''
    pass

def get_position(html_list, true_position = None, html_position = None,
                 visible_position = None, return_list_index = None):
    '''given either a text position or html position, return the other
    position
    For instance, if you give the html_position, you will recieve the 
    true_position
    
    if return_list_index == True it returns:
        (true_pos, html_pos, vis_pos), (html_list_object_index, relative_index)
    Where relative index is the index of the data inside the list object
    '''
    # TODO: make it do an average for selecting decorator elements.
    check = (true_position, html_position, visible_position)
    if iteration.is_all_type(check, None):
        raise TypeError("Must find at least one position")
    if len([n for n in check if n != None]) > 1:
        raise TypeError("Can only find one position at a time")
    if not html_list:
        raise IndexError("0 length array")
    cur_html_pos, cur_true_pos, cur_vis_pos = 0, 0, 0
    prev_hpos, prev_tpos, prev_vpos = 0, 0, 0
    for index, textrp in enumerate(html_list):
        cur_html_pos += len(textrp.html_text)
        cur_true_pos += len(textrp.true_text)
        cur_vis_pos  += len(textrp.visible_text)
        if true_position != None and cur_true_pos > true_position:
            break
        elif html_position != None and cur_html_pos > html_position:
            break
        elif visible_position != None and cur_vis_pos > visible_position:
            break
        prev_hpos, prev_tpos, prev_vpos = (cur_html_pos, cur_true_pos, 
                                           cur_vis_pos)
    else:
        raise ValueError("Position is outside of text length " + 
            str((true_position, html_position, visible_position)))
    
    if true_position != None:
        out_true_pos = true_position
        relative_pos = true_position - prev_tpos
        if _check_html_text_equal(textrp.html_text, textrp.true_text):
            # position is in a plain text part
            out_html_pos = prev_hpos + relative_pos
            out_vis_pos = prev_vpos + relative_pos
#        elif textrp.html_text == textrp.visible_text: # same as above
        elif textrp.html_text > textrp.true_text:
            # position is inside of html, choose position before. This
            # is correct for visual as well because we only want true text
            out_html_pos = prev_hpos
            out_vis_pos = prev_vpos
        else:
            raise ValueError("Position is outside of text length " + 
                str(true_position))
    
    elif visible_position != None:
        out_vis_pos = visible_position
        relative_pos = (visible_position - prev_vpos)
        if _check_html_text_equal(textrp.html_text, textrp.true_text):
            # It occured inside of plain text
            out_true_pos = prev_tpos + relative_pos
            out_html_pos = prev_hpos + relative_pos
        elif _check_html_text_equal(textrp.html_text, textrp.visible_text):
            # it occured inside of visible text
            out_true_pos = prev_tpos
            out_html_pos = prev_hpos + relative_pos
        elif len(textrp.html_text) > len(textrp.true_text):
            # it occured inside of an html block
            out_true_pos = prev_tpos
            out_html_pos = prev_vpos
        else:
            raise ValueError("Position is outside of text length " + 
                str(html_position))
        
    elif html_position != None:
        out_html_pos = html_position - prev_hpos
        relative_pos = html_position - prev_hpos
        if _check_html_text_equal(textrp.html_text, textrp.true_text):
            out_true_pos = prev_tpos + relative_pos
            out_vis_pos = prev_vpos + relative_pos
        elif _check_html_text_equal(textrp.html_text, textrp.visible_text):
            out_true_pos = prev_tpos
            out_vis_pos = prev_vpos + relative_pos
        elif textrp.html_text > textrp.true_text:
            out_true_pos = prev_tpos
            out_vis_pos = prev_vpos
        else:
            raise ValueError("Position is outside of text length" + 
                str(html_position))
    else: assert(False)

    assert (out_true_pos <= out_vis_pos <= out_html_pos)
    
    if not return_list_index:    
        return out_true_pos, out_vis_pos, out_html_pos
    else:
        pos_tup = out_true_pos, out_vis_pos, out_html_pos
        return pos_tup, (index, relative_pos)

class COLOR:
    RED =   get_color_str(255,  0,      0)
    GREEN = get_color_str(0,    255,    0)
    BLUE =  get_color_str(0,    0,      255)
    BLACK = get_color_str(0,    0,      0)
    
KEEPIF = {
'black-bold': {'font-weight':'600', 'color':'#' + COLOR.BLACK},
'red-underlined-bold': {'font-weight':'600', 'color':'#' + COLOR.RED,
                        'text-decoration': 'underline'},
}

def deformat_html(html, keepif, keep_plain = True):
    '''
    "Deformats" an html into HtmlParts that are dependent on the keepif
        variable. This allows you to get absolute position of decorated text.
        (i.e. if you only want plain and black bold text, then 
        keepif = {'font-weight':'600', 'color':'#000000'})
    
    if keepif == True then all text (that isn't html tags) is kept
    if keepif == None, then none is kept unless it is plain
    
    otherwise, keepif is a dict of attributes to keep. 
    For the expression to be kept, it has to match either ALL
    these attributes or be plain text (unless keep_plain == False)
    
    returns HtmlParts with the .true_text and .html_text set
    appropriately
    '''
    header, footer = get_headfoot(html)
    
#    if KEEPIF['red-underlined-bold'] in keepif:
#        pdb.set_trace()
    bsoup = bs4.BeautifulSoup(html)
    next_el = bsoup.body.next_element
    html_list = [HtmlPart(header, '', '')]
    i = -1
    while next_el != None:
        i += 1
        if type(next_el) == bs4.element.NavigableString:
            # print 'Is String'
            # at first I was kind of upset that bsoup couldn't give
            # me the raw html. Then I realized that I can just use
            # my own function to get it... and everything else!
            html_list.extend(text_format_html(str(next_el), ('', ''),
                not_plain = not keep_plain, ignore_newlines = True))
        
        elif next_el.name == 'span':
            # print 'Is span'
            next_el, hlist = html_process_span(next_el, keepif, keep_plain)
            html_list.extend(hlist)
            
        elif next_el.name == 'p':
            # print 'Is paragraph'
            next_el, hlist = html_process_paragraph(next_el, keepif, 
                                                    keep_plain)
            html_list.extend(hlist)
        else:
            raise IOError("unrecognized element: " + next_el)
        
#        for i, n in enumerate(html_list):
#            if '<' in n.visible_text:
#                pdb.set_trace()
#            if '\n' in n.visible_text or '\n' in n.true_text:
#                pdb.set_trace()
        next_el = next_el.next_element
    html_list.append(HtmlPart(footer, '', ''))
    # remove empty HtmlParts
    html_list = (n for n in html_list if n.bool())
    return tuple(html_list)

class HtmlPart(object):
    '''object to differentiate between standard text and html data for 
    RegParts'''
    def __init__(self, html_text, true_text, visible_text):
        '''true_text is the base (non - decorative) text of RegPart
        objects'''
        args = (html_text, true_text, visible_text)
        types = (type(n) for n in args)
        assert(iteration.first_index_nin(types, (unicode, str)) == None)
        html_text, true_text, visible_text = (str(n) for n in args)
        self.html_text = html_text
        self.true_text = true_text
        self.visible_text = visible_text
    
    def __repr__(self):
        return '<Html Part {0}>'.format((self.html_text[:15], 
                  self.true_text, self.visible_text))
    
    def __eq__(self, other):
        if (self.html_text == other.html_text) and (self.true_text == 
                other.true_text):
            return True
        else:
            return False
    
    def bool(self):
        return bool(self.html_text + self.true_text + self.visible_text)
        
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

def get_html_converted_and_subfun(text, replace_html_list = None):
    if replace_html_list == None:
        replace_html_list = html_replace_list
        
    repl_or_re, repl_re = textools.get_rcmp_list(replace_html_list)
    replace_fun = textools.subfun(replace_list = repl_re)
    converted_text = repl_or_re.sub(replace_fun, text)
    return converted_text, replace_fun

def text_format_html(text, html_span_tags = html_span_std, not_plain = False,
                     ignore_newlines = False):
    '''Formats a text body taking care of special html characters.
    not_plain means that no text will be counted in the HtmlPart.true_text
    attribute.'''
    if not text:
        return ''
    tag_st, tag_end = html_span_tags
    html_list = [HtmlPart(tag_st, '', '')]
    
    if text[0] == '\n':
        add_html = ''.join(PARAGRAPH_SPAN[::-1])
        add_plain = '' if not_plain or ignore_newlines else text[0]
        html_list.append(HtmlPart(add_html, add_plain, 
                                  '' if ignore_newlines else text[0]))
        text = text[1:]
        
    add_end = None
    if text and text[-1] == '\n':
        add_end = True 
        end_html = ''.join(PARAGRAPH_SPAN[::-1])
        end_plain = text[-1]
        text = text[:-1]
    
    if ignore_newlines == True:
        # alter the str_replace_list to delete new lines
        # This is used when converting FROM html to text -- any newlines are
        # characters that shouldn't be there.
        my_replace_list = html_replace_list[:]
        my_replace_list.pop([n[0] for n in html_replace_str_list].index('\n'))
        my_replace_list.append((re.compile('\n'), ''))
    else:
        my_replace_list = html_replace_list
        
    converted_text, replace_fun  = get_html_converted_and_subfun(text,
                                        replace_html_list = my_replace_list)
    
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
        html_list.append(HtmlPart(add_html, add_plain, add_html))
        
        # now add own text
        add_plain = '' if not_plain else subbed[0]
        add_html = subbed[1]
        add_visible = subbed[0]
        if ignore_newlines and add_visible == '\n':
            add_visible = ''
            add_plain = ''
        if ignore_newlines:
            assert('\n' not in add_visible)
        
        html_list.append(HtmlPart(add_html, add_plain, add_visible))
        
        prev_reg = reg
    if not subbed_regs:# never entered loop! No special characters = no subbed!
        assert(converted_text == text)
        assert('\n' not in text)
        add_plain = '' if not_plain else text
        add_html = text
        html_list.append(HtmlPart(add_html, add_plain, text))
    else:
        # do final cleanup, add text that wasn't added
        final_text = text[subbed_regs[-1][1]:]
        add_plain = '' if not_plain else final_text
        html_list.append(HtmlPart(final_text, add_plain, final_text))
    
    if add_end:
        add_plain = '' if not_plain or ignore_newlines else end_plain
        add_html = end_html
        html_list.append(HtmlPart(add_html, add_plain, 
                                  '' if ignore_newlines else end_plain))
    
    html_list.append(HtmlPart(tag_end, '', ''))
    
    if ignore_newlines:
        for n in html_list:
            assert('\n' not in n.true_text and '\n' not in n.visible_text)
    html_list = list(n for n in html_list if n.bool())
#    html_list = handle_empty_paragraphs(html_list)
    return html_list

#def handle_empty_paragraphs(html_list):
#    for i, hpart in enumerate(html_list):
#        if PARAGRAPH_SPAN[0] in hpart.html_text:
#            if i == len(html_list) - 1:
##                assert(0)
#                break
#            if html_list[i+1].visible_text == '':
#                htext = ''
#                if PARAGRAPH_SPAN[1] in hpart.html_text:
#                    htext = PARAGRAPH_SPAN[1]
#                html_list[i].html_text = htext + EMPTY_PARAGRAPH
#    return html_list

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
    if keepif == True:
        do_keep = True
    elif not keepif:
        do_keep = False
    else:
        if type(keepif) not in (list, tuple):
            keepif = (keepif,)
        do_keep = False
        for kif in keepif:
            if len(kif) == len(style_attrs):
                for key, value in kif.iteritems():
                    key, value = key.strip(), value.strip()
                    if key not in style_attrs or style_attrs[key] != value:
                        break # break out of for loop, don't keep
                else:
                    # all keys match, it's good.
                    do_keep = True
                    break
    
    body, fback = get_named_body_frontback(str(bs_span), 'span')
    span_front, span_back = fback; del fback
    span_front, span_back = (HtmlPart(span_front, '', ''), 
                             HtmlPart(span_back, '', ''))
    html_list = [span_front]
    
    append_text = str(text_element) if text_element != None else ''
    html_list.extend(text_format_html(append_text, ('', ''), not_plain = 
        not do_keep, ignore_newlines = True))
    if text_element != None:
        out_elem = text_element
    else:
        out_elem = bs_span
    
    html_list.append(span_back)
    return out_elem, html_list

def html_process_paragraph(bs_paragraph, keepif, keep_plain):
#    pdb.set_trace()
    body, fback = get_named_body_frontback(str(bs_paragraph), 'p')
    front, back = fback; del fback
    style = bs_paragraph.attrs['style']
    style_attrs = get_style_attributes(style)
    no_newline = False
#    try:
#        # Apparently there is such a thing as an "empty paragraph" that
#        # doesn't trigger a line ending! What an annoying "feature"
#        if style_attrs['-qt-paragraph-type'] == 'empty':
#            no_newline = True
#    except KeyError:
#        pass
    front = HtmlPart(front, '', '')
    
#    -qt-paragraph-type:empty
    if no_newline:
        back = HtmlPart(back, '', '')
    else:
        back = HtmlPart(back, '\n', '\n')
    
    html_list = [front]
    prev_el = bs_paragraph; del bs_paragraph
    next_el = prev_el
    while True:
        next_el = next_el.next_element
        if type(next_el) != bs4.element.NavigableString and (
            next_el == None or next_el.name == 'p'):
            # next element is another paragraph! (or end of body)
            out_el = prev_el
            break
        elif type(next_el) == bs4.element.NavigableString:
            html_list.extend(text_format_html(str(next_el), ('', ''), 
                not_plain = not keep_plain, ignore_newlines = True))
            next_el = next_el
        elif next_el.name == 'br':
            pass
            html_list.append(HtmlPart(str(next_el), '', ''))
        else:
            assert(next_el.name == 'span')
            next_el, hlist = html_process_span(next_el, keepif, keep_plain)
            html_list.extend(hlist)
            next_el = next_el
        prev_el = next_el
        
    html_list.append(back)
    return out_el, html_list



HTML_LIST_EMPTY_PARAGRAPH = (
HtmlPart(
'''<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>'''
, '\n', '\n')
#HtmlPart('''</p><p style="-qt-paragraph-type:empty\
#; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bl\
#ock-indent:0; text-indent:0px;"><br />''', '\n', '\n')
)
