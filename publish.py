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

# commiting a change from spyder
PYTHON_VERSION = 2
CLOUD_TB_VERSION = None

'''Add your file types to list below -- comma separated'''
FILE_TYPES = '.c, .h, .cpp, .hpp, .txt, .py'

FIRST_LINE = '#!/usr/bin/python'
SECOND_LINE = '# -*- coding: utf-8 -*-'

YOUR_LICENSE = '''
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
'''
LAST_LINE = '#    http://opensource.org/licenses/MIT'

KEEP_LICENSE = '*** KEEP LICENSE ***'

##### CODE -- DON'T EDIT (unless you know what you are doing!) ####
import pdb
import re
import os
import sys

import textools

def update_license(path):
    '''updates the license information and the first line of the file
    for the file on the path'''
    print 'updating path for: ', path
    
    fext = os.path.splitext(path)[1]
    print "Extention: ", fext
    fname = os.path.split(path)[1]
    FILE_TYPES_SET = set(FILE_TYPES.replace(' ', '').split(','))
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

    with open(path, 'r') as f:
        text = f.read()
    
    if KEEP_LICENSE in text:
        return
    
    your_license = YOUR_LICENSE.strip()
    
    
    full_header = '{fl}\n{sl}\n{license}\n{last_line}'.format(fl = FIRST_LINE,
                sl = SECOND_LINE, license = your_license, last_line = LAST_LINE)
        
    ctore = textools.convert_to_regexp
    sub_re = r'{fl}[\w\W]*?{last_line}'.format(fl = ctore(FIRST_LINE), 
            last_line = ctore(LAST_LINE))
    re_cmp = re.compile(sub_re)

    if re_cmp.match(text):
        text = re_cmp.sub(full_header, text, count = 1)
    else:
        text = full_header + '\n' + text
    
    uin = raw_input("About to overwrite license for \n<" + path + '>\n. Press y '
        'if ok')
    if uin.lower() == 'y':
        with open(path, 'w') as f:
            f.write(text)

def update_cloudtb(cloud_tb_version):
    # see http://stackoverflow.com/questions/791959/how-to-use-git-to-download-a-particular-tag
    git_archive = ('git archive --format=zip '
         '--remote=[{hostname}]:[{repo_path}][{tag_name}] '
         '> {out_file_path}')
    
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


def main():
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
    
    update_license(path)
    
if __name__ == '__main__':
    main()





