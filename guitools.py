
'''
This module contains general use tools in GUI's or displaying data 
(i.e. matplotlib)

'''

from __future__ import division

def get_color_from_index(index, max_index, highest = 180):
    '''
    Returns a good spread of colors quickly
    Increase highest for brighter colors, decrease for darker. Absolute max
    is 256
    '''
#    Good color algorithm (gotten from playing with color bar in Qt)
#    RED HIGH    (start)
#    UP BLUE     (red high)    256
#    DOWN RED    (blue high)   512 
#    UP GREEN    (blue high)
#    DOWN BLUE   (green high)
#    UP RED      (green high)
#    DOWN GREEN (ENDS AT HIGH RED)
#    
#    or, to put into code, there are 6 * 256 possibilities 
#    (although I'd end at green == 70 to keep the last color orange so 6*256 - 70)
#    They can be arrived at through simple iteration through this algorithm, or
#    iteration plus jumping, or ... THIS CODE!
    if highest > 256:
        raise ValueError('highest: ' + str(highest))
    reserve = (70*highest/256)
    assert(reserve > 0)
    cindex = int((float(index) / (max_index + 1)) * (6*highest-reserve))
    cindex = cindex + 1
    red, blue, green = (0,)*3
    
    if cindex <= highest:
        red = highest - 1
        blue = cindex -  (         highest * 0) - 1
    elif cindex <= highest * 2:
        blue = highest - 1
        red = highest -  (cindex - highest * 1) - 1
    elif cindex <= highest * 3:
        blue = highest - 1
        green = cindex - (         highest * 2) - 1
    elif cindex <= highest * 4:
        green = highest - 1
        blue = highest - (cindex - highest * 3)
    else:
        assert(0)
    
    assert(0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255)
    
    return (red << 16) + (green << 8) + (blue)


'''Some fun general text tools'''
class SpellingCorrector(object):
    '''A very simple spelling corrector, used in GUIs to check user input.
    Short fast and simple, it doesn't always work -- but does it need to?'''
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
