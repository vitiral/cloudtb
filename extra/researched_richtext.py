# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:41:49 2013

@author: user
"""
import pdb
from guitools import get_color_from_index, get_color_str

from richtext import (HEADER, FOOTER, paragraph, 
    html_span_std, get_html_span_tags,
    get_html_converted_and_subfun)

def re_search_format_html(data_list, show_tags_on_replace = False):
    html_list = [TextRegPart(HEADER, '')]

    for data in data_list:
        if type(data) == str:
            html_list.extend(_text_format_html(data, html_span_std))
        else:
            html_list.extend(_regpart_format_html(data,
                show_tags_on_replace = show_tags_on_replace))
    html_list.append(TextRegPart(FOOTER, ''))
    return html_list

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

class TextRegPart(object):
    '''object to differentiate between standard text and html data for 
    RegParts'''
    def __init__(self, html_text, true_text):
        '''true_text is the base (non - decorative) text of RegPart
        objects'''
        self.html_text = html_text
        self.true_text = true_text
    
    def __repr__(self):
        return self.html_text

def _text_format_html(text, html_span_tags, not_plain = False):
    '''Formats a text body taking care of special html characters.
    not_plain means that no text will be counted in the TextRegPart.true_text
    attribute.'''
    if not text:
        return ''
    tag_st, tag_end = html_span_tags
    html_list = [TextRegPart(tag_st, '')]
        
    if text[0] == '\n':
        #TODO: is this the right way to do this?? kind of confusing
        add_html = ''.join(paragraph[::-1])
        add_plain = '' if not_plain else text[0]
        html_list.append(TextRegPart(add_html, add_plain))
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
        html_list.append(TextRegPart(add_html, add_plain))
        
        # now add own text
        
        add_plain = '' if not_plain else subbed[0]
        add_html = subbed[1]
        html_list.append(TextRegPart(add_html, add_plain))
        
        prev_reg = reg
    if not subbed_regs:# never entered loop! No special characters = no subbed!
        assert(converted_text == text)
        add_plain = '' if not_plain else text
        add_html = text
        html_list.append(TextRegPart(add_html, add_plain))
    
    if add_end:
        add_plain = '' if not_plain else end_plain
        add_html = end_html
        html_list.append(TextRegPart(add_html, add_plain))
    
    html_list.append(TextRegPart(tag_end, ''))
    
    return html_list

def _regpart_format_html(regpart, show_tags_on_replace = False):
    '''Formats a reg_part'''
    data_list, indexes, groups, match_data = (regpart.data_list, regpart.indexes,
        regpart.groups, regpart.match_data)

    if match_data:
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

    html_list = []
    # front formatting
    if (match_data != None and 
            (show_tags_on_replace == True or replace == None)):
        html_span_tags = get_html_span_tags(bold = True, underlined = True, 
                                            lower = True)
        match = match_data[0]
        
        html_list.extend(_text_format_html('{0}:'.format(match), html_span_tags,
                                          not_plain = True))

    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            html_list.extend(_text_format_html(
                '(', get_html_span_tags(bold = True, color = colors[i]),
                not_plain = True))
    if replace:
        html_list.extend(_text_format_html(regpart.text, 
            get_html_span_tags(bold = True, color = std_color), 
            not_plain = False)) # want to clearly mark that this IS plain
            
    else:
        for data in data_list:
            if type(data) == str:
                html_list.extend(_text_format_html(data, 
                    get_html_span_tags(bold = True, color = std_color), 
                    not_plain = False))
            else:
                html_list.extend(_regpart_format_html(data, 
                                                     show_tags_on_replace))
    
    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            html_list.extend(_text_format_html(')', 
                get_html_span_tags(bold = True, color = colors[i]), 
                not_plain = True))
            html_list.extend(_text_format_html('{0}'.format(indexes[i]),
                get_html_span_tags(bold = True, color = colors[i], 
                                   lower = True), not_plain = True))
    
    if replace:
        html_list.extend(_text_format_html(replace,
            get_html_span_tags(bold = True, color = repl_color,
            underlined = True), not_plain = True))
    
    return html_list