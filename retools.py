
import functions

def group_num(tup):
    '''returns group number of returned re from findall that is not == ""
    returns only first instance found.'''
    return next((n for n in tup if n != ''))

def check_brackets(match_list, text, line = '?'):
    '''Checks to make sure all brackets are completed (i.e. \iffalse or \(ifblog) or \iftex
    is completed by an \fi. 
    Match list uses first part as part of list, final part as end.
    
    Example input:
    found, gnumbers = check_brackets([r'(\\iffalse)', r'\\(ifblog)', r'\\(iftex)', r'\\(if), r'\\(fi)'],
                                      text)
    note: only returns the first group number found!
    raises ValueError on failure    
                  
    return match_compile, found, gnumbers             
    '''
    match_cmp = re.compile('|'.join(match_list))
    found = match_cmp.findall(m)
    gnumbers = [group_num(n) for n in found]
    fi = 0
    for n in gnumbers:
        if n != len(gnumbers):
            n += 1
        else:
            n -= 1
    if n != 0:
        raise ValueError("Brackets not matched")
    
    return match_compile, found, gnumbers

class subfun(object):
    '''For use with re.sub. Instead of subsituting text it prepends or 
    postpends text onto it and returns it whole
    USAGE:
        sfun = subfun(match_set, subtext, prepend, postpend)
        subbed_text = re.sub(pattern, sfun, text)
    '''
    def __init__(self, match_set, prepend = '', postpend = ''):
        self.ms = match_set
        self.pre = prepend
        self.post = postpend
    
    def __call__(self, matchobj):
        if matchobj:
            print 'GROUPS:', matchobj.groups()
            txt = matchobj.group(0)
            if txt in self.ms:
                return self.pre + txt + self.post
            return txt

    
    
    
    