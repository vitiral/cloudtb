# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:41:49 2013

@author: user
"""
import pdb
from guitools import get_color_from_index, get_color_str

from richtext import (HEADER, FOOTER, html_span_std, get_html_span_tags, 
                      text_format_html, HtmlPart)

def re_search_format_html(data_list, show_tags_on_replace = False):
    html_list = [HtmlPart(HEADER, '')]

    for data in data_list:
        if type(data) == str:
            html_list.extend(text_format_html(data, html_span_std))
        else:
            html_list.extend(_regpart_format_html(data,
                show_tags_on_replace = show_tags_on_replace))
    html_list.append(HtmlPart(FOOTER, ''))
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
        
        html_list.extend(text_format_html('{0}:'.format(match), html_span_tags,
                                          not_plain = True))

    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            html_list.extend(text_format_html(
                '(', get_html_span_tags(bold = True, color = colors[i]),
                not_plain = True))
    if replace:
        html_list.extend(text_format_html(regpart.text, 
            get_html_span_tags(bold = True, color = std_color), 
            not_plain = False)) # want to clearly mark that this IS plain
            
    else:
        for data in data_list:
            if type(data) == str:
                html_list.extend(text_format_html(data, 
                    get_html_span_tags(bold = True, color = std_color), 
                    not_plain = False))
            else:
                html_list.extend(_regpart_format_html(data, 
                                                     show_tags_on_replace))
    
    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            html_list.extend(text_format_html(')', 
                get_html_span_tags(bold = True, color = colors[i]), 
                not_plain = True))
            html_list.extend(text_format_html('{0}'.format(indexes[i]),
                get_html_span_tags(bold = True, color = colors[i], 
                                   lower = True), not_plain = True))
    
    if replace:
        html_list.extend(text_format_html(replace,
            get_html_span_tags(bold = True, color = repl_color,
            underlined = True), not_plain = True))
    
    return html_list