import re, collections
alphabet = 'abcdefghijklmnopqrstuvwxyz_'

def group_num(tup):
    '''returns group number of returned re from findall that is not == ""
    returns only first instance found.'''
    return next((n for n in tup if n != ''))

def convert_to_regexp(txt):
    '''converts text into a regexp, handling any special characters'''
    special_chars = r'. ^ $ * + ? { } [ ] \ | ( )'
    special = special_chars.split(' ')
    special_or = '(\\' + ')|(\\'.join(special) +')'
    sfun = subfun(set(special), prepend = '\\')
    return re.sub(special_or, sfun, txt)

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
            txt = matchobj.group(0)
            if txt in self.ms:
                return self.pre + txt + self.post
            return txt

'''Some fun general text tools'''
class SpellingCorrector(object):
    '''A very simple spelling corrector, used in GUIs to check user input.'''
    def __init__(self, all_words):
        if type(all_words) in (tuple, list, set):
            nw = [n.lower() for n in all_words]
            nw.sort()
            self.NWORDS = nw
        else:
            self.NWORDS = self.words(all_words)
        self.NWORDS = self.train(self.NWORDS)

    def words(self, text):
        ''' returns a list of words'''
        return re.findall('[a-z]+', text.lower())

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self, word):
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       deletes    = [a + b[1:] for a, b in splits if b]
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
       inserts    = [a + c + b     for a, b in splits for c in alphabet]
       return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word)
                   for e2 in self.edits1(e1) if e2
                   in self.NWORDS)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    def correct(self, word):
        candidates = (self.known([word]) or
                      self.known(self.edits1(word)) or
                      self.known_edits2(word) or
                      [word])
        return max(candidates, key=self.NWORDS.get)
