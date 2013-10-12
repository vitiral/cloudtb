# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:36:13 2013

@author: user
"""
import pdb

import unittest
import re
import bs4

try:
    from .. import textools
    from ..extra import richtext, researched_richtext
    from .. import dectools
except ValueError:
    for n in xrange(2):
        try:
            import textools
            from extra import richtext, researched_richtext
            import dectools
            break
        except ImportError:
            import sys
            sys.path.insert(1, '..')
    else:
        raise ImportError
DEBUG = True


def text_setUp(self):
    # Note that all texts have a new line at the end
    # setup text 1
    text1 = '''talking about expecting the Spanish Inquisition in the \
text below: 
Chapman: I didn't expect a kind of Spanish Inquisition. 
(JARRING CHORD - the cardinals burst in) 
Ximinez: NOBODY expects the Spanish Inquisition! Our chief weapon is \
surprise...surprise and fear...fear and surprise.... Our two weapons are \
fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, \
surprise, and ruthless efficiency...and an almost fanatical devotion to the \
Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry... \
are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) 
'''
    text1_proper_formatted = '''<*m0>[[{talking {about }<g[1]>expect{ing }<g[2]>{the }<g[3]>Spanish Inquisition{ }<g[4]>}<g[0]>]]in the text below: 
Chapman: <*m1>[[{I {didn't }<g[1]>expect{ a kind of }<g[2]>Spanish Inquisition{.}<g[4]>}<g[0]>]] 
(JARRING CHORD - the cardinals burst in) 
Ximinez: <*m2>[[{{NOBODY }<g[1]>expect{s }<g[2]>{the }<g[3]>Spanish Inquisition{!}<g[4]>}<g[0]>]] Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry... are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) 
'''
    text1_proper_replaced = '''<*m0>[[{talking {about }<g[1]>expect{ing }<g[2]>{the }<g[3]>Spanish Inquisition{ }<g[4]>}<g[0]>]]==>[[What is this, the Spanish Inquisition?]]in the text below: 
Chapman: <*m1>[[{I {didn't }<g[1]>expect{ a kind of }<g[2]>Spanish Inquisition{.}<g[4]>}<g[0]>]]==>[[What is this, the Spanish Inquisition?]] 
(JARRING CHORD - the cardinals burst in) 
Ximinez: <*m2>[[{{NOBODY }<g[1]>expect{s }<g[2]>{the }<g[3]>Spanish Inquisition{!}<g[4]>}<g[0]>]]==>[[What is this, the Spanish Inquisition?]] Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry... are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) 
'''
    regexp1 = (r'''([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish ''' + 
                    r'''Inquisition(!|.)''')
    replace1 = r'What is this, the Spanish Inquisition?'
    
    # setup text 2
    text2 = ('''Researching my re search is really easy with this handy new tool! 
It shows me my matches and group number, I think it is great that they're seen\
 in this new light! 
''')
    text2_proper_formatted = '''<*m0>[[{{R}<g[2]>esearching}<g[0, 1]>]] my <*m1>[[{{r}<g[2]>e search}<g[0, 1]>]] <*m2>[[{is}<g[0, 3]>]] really easy with <*m3>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]] handy new tool! 
It shows me my matches and group number, I think it <*m4>[[{is}<g[0, 3]>]] great that they'<*m5>[[{{r}<g[2]>e seen}<g[0, 1]>]] in <*m6>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]] new light! 
'''
    text2_proper_replaced = '''<*m0>[[{{R}<g[2]>esearching}<g[0, 1]>]]==>[[New Research!]] my <*m1>[[{{r}<g[2]>e search}<g[0, 1]>]]==>[[New Research!]] <*m2>[[{is}<g[0, 3]>]]==>[[New Research!]] really easy with <*m3>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]]==>[[New Research!]] handy new tool! 
It shows me my matches and group number, I think it <*m4>[[{is}<g[0, 3]>]]==>[[New Research!]] great that they'<*m5>[[{{r}<g[2]>e seen}<g[0, 1]>]]==>[[New Research!]] in <*m6>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]]==>[[New Research!]] new light! 
'''
    regexp2 = r'''((R|r)e ?se\w*)|(((T|t)h)?is)'''
    replace2 = r'New Research!'
     
    self.text_list = (text1, text2)
    self.regexp_list = (regexp1, regexp2)
    self.replace_list = (replace1, replace2)
    self.proper_formatted = (text1_proper_formatted, text2_proper_formatted)
    self.proper_replaced = (text1_proper_replaced, text2_proper_replaced)
    self.all_list = tuple(zip(self.text_list, self.regexp_list, 
                              self.replace_list,
                              self.proper_formatted, self.proper_replaced))

def get_researched_str_recursive(data_list):
    outlist = []
    for regpart in data_list:
        if type(regpart) == str:
            outlist.append(regpart)
        else:
            outlist.append(get_researched_str_recursive(regpart.data_list))
    return ''.join(outlist)

class regPartTest(unittest.TestCase):
    def setUp(self):
        text_setUp(self)
    
    @dectools.debug(DEBUG)
    def test_re_search(self):
        for stuff in self.all_list:
            text, regexp, replace, prop_formatted, prop_replaced = stuff
            del stuff
            
            regcmp = re.compile(regexp)
            researched = textools.re_search(regexp, text)
            r_formatted = textools.format_re_search(researched)
            r_text = textools.get_str_researched(researched)
            self.assertEqual(r_text, text, 'Simple text not equal')
            self.assertEqual(r_formatted, prop_formatted, 'Formatted')
#            print 'PROPER FORMAT'
#            print r_formatted
#            print 'END PROPER'
#            print
            
            # go into a little more depth than just pulling the .text
            # attribute...
            r_text = get_researched_str_recursive(researched)
            self.assertEqual(r_text, text, 'Recursive text not equal')
            
            # testing substitutions
            researched_replace = textools.re_search_replace(researched, 
                                            replace, preview = True)
            std_replaced = regcmp.sub(replace, text)
            r_replaced = textools.get_str_researched(researched_replace)
            r_formatted_replaced = textools.format_re_search(
                                                        researched_replace)
#            print 'PROPER REPLACED'
#            print r_formatted_replaced
#            print 'END REPLACED'
#            print
            
            self.assertEqual(r_formatted_replaced, prop_replaced)
            self.assertEqual(r_replaced, std_replaced, 
                             'Replaced text not equal')
    
#    def test_html(self):
#        for text, regexp, replace in self.all_list:
#            regcmp = re.compile(regexp)
#            researched = textools.re_search(regexp, text)
#            richtext_list = researched_richtext.re_search_format_html(
#                                                researched)
#            richtext = richtext.get_str_html_formatted(richtext)
#            soup = bs4.BeautifulSoup(richtext)
#            
#            self.assertEqual(str(soup), richtext, 
#                             'Check proper html formatting')
            
            
            
if __name__ == '__main__':
    unittest.main()
    