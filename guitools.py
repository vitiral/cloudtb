
'''
This module contains general use tools in GUI's or displaying data 
(i.e. matplotlib)

'''

def get_color_from_index(index, max_index):
    '''
    Returns a good spread of bright and shiny colors quickly.
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
    
    cindex = int(index / max_index * (6*256-70))
    highest = 256
    cindex = cindex + 1
    red, blue, green = 0
    
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
        blue = highest - (cindex - highest * 3) - 1
    
    assert(0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255)
    
    return (red << 16) + (green << 8) + (blue)