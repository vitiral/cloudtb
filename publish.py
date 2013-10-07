'''
*** BEGIN FILE LICENSE ***

The MIT License (MIT)

Copyright (c) 2013 Garrett Berg cloudformdesign.com
An updated version of this file can be found at:
https://github.com/cloudformdesign/cloudtb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

http://opensource.org/licenses/MIT

*** END FILE LICENSE ***

Documentation
This file performs the necessary actions for standard publishing of works in python.
Primarily it updates the License and hosts the file on the selected servers of the
global variables.

Change the global variables below to reflect your project
'''

PYTHON_VERSION = 2
'''Add your file types to list below -- comma separated'''

FILE_TYPES = '.c, .h, .cpp, .hpp, .txt, .py'

FIRST_LINE = '#! /usr/bin/python'

YOUR_LICENSE = '''
The MIT License (MIT)

Copyright (c) 2013 Garrett Berg cloudformdesign.com
An updated version of this file can be found at:
https://github.com/cloudformdesign/cloudtb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

http://opensource.org/licenses/MIT
'''

KEEP_LICENSE = '*** KEEP LICENSE ***'
BEGIN_LICENSE = '*** BEGIN PROJECT LICENSE ***'
END_LICENSE = '*** END PROJECT LICENSE ***'

##### CODE -- DON'T EDIT (unless you know what you are doing!) ####
import pdb
import re
import texttools
import os
import sys

YOUR_LICENSE = YOUR_LICENSE.strip()
FILE_TYPES_SET = set(FILE_TYPES.replace(' ', '').split(','))
reBEGIN = texttools.convert_to_regexp(BEGIN_LICENSE)
reEND = texttools.convert_to_regexp(END_LICENSE)

def update_license(path):
    '''updates the license information and the first line of the file
    for the file on the path'''
    print 'updating path for: ', path
    
    fext = os.path.splitext(path)[1]
    print "Extention: ", fext
    fname = os.path.split(path)[1]
    if fname[0] == '.':
        return
    elif fext == '' and os.path.isdir(path):
        pass
    elif fext not in FILE_TYPES_SET:
        return
        
    if os.path.isdir(path):
        for f in os.listdir(path):
            new_path = os.path.join(path, f)
            update_license(new_path)
        return
        
    tquotes = ("'''", '"""')
    with open(path, 'r') as f:
        text = f.readlines()

    for i, l in enumerate(text):
        if text[i][-1] == '\n':
            # take out new lines because they are annoying here
            text[i] = text[i][:-1]
        if KEEP_LICENSE in l:
            return 0

    if not len(text):
        text.append('')
        
    if text[0] != FIRST_LINE:
        text.insert(0, FIRST_LINE)

    license = '\n'.join((BEGIN_LICENSE, YOUR_LICENSE, END_LICENSE, ''))
    if text[1][:3] not in tquotes:
        # file doesn't even have tquotes! need those
        text.insert(1, tquotes[1])
        text.insert(1, tquotes[1])
    else:
        # Else tquotes stay where they are
        remaining_text = text[:2]
        tq = text[1][:3]
        
        #TODO: need to check they didn't do tq on same line
        
        flic = [] # file license
        for n in xrange(2, len(text)):
            line = text[n]
            if tq in line:
                text = remaining_text + text[n:]
                break
            flic.append(line)
        else:
            raise ValueError("could not find quote ending")

        flic = '\n'.join(flic)

        pattern = "({0})(.*?)({1})(.*)".format(reBEGIN, reEND)
        cmp = re.compile(pattern, re.DOTALL)
        found = cmp.findall(flic)
        if found:
            found = found[0]
            found = [i for i in found if i not in (None, '')]
            insert_next = False
            for i, item in enumerate(found):
                if insert_next == True:
                    found[i] = YOUR_LICENSE + '\n'
                    break
                elif item == BEGIN_LICENSE:
                    found[i] = item + '\n'
                    insert_next = True
            else:
                assert(0)
            license = ''.join(found)
        else:
            license = license + flic

    text.insert(2, license)
    text = '\n'.join(text)
    uin = raw_input("About to overwrite license for \n<" + path + '>\n. Press y '
        'if ok')
    if uin.lower() == 'y':
        with open(path, 'w') as f:
            f.write(text)

'''
Publish

publish is a general feature publishing tool for projects written in python.
It's current features are the ability to write over license files
automatically update itself to the pypy repository.

Future versions should hopefully contain the ability to quick-add to
repositories as well as other tools.

Syntax
    publish [directory] [--options[ word]]

publish [directory]
    - updates license and first line of all files in directory
    - if directory is left out, the working directory is used.

publish file
    - same as above but for a single file
'''

        
if __name__ == '__main__':
    import argparse
    if len(sys.argv) < 2:
        path = os.getcwd()
    else:
        parser = argparse.ArgumentParser(description = "Update License Files for "
        "python project")
        parser.add_argument('path', type = str, help='path to file or folder')
        args = parser.parse_args()
        path = args.path
        print path
    
    1/0
    update_license(path)





