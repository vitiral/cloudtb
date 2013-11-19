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
import pdb

PYTHON_VERSION = 2
CLOUDTB_VERSION_URL = None
VERSION = '0.1.2'

'''Add your file types to list below -- comma separated'''
FILE_TYPES = '.c, .h, .cpp, .hpp, .txt, .py'

FIRST_LINE = '#!/usr/bin/python'
SECOND_LINE = '# -*- coding: utf-8 -*-'

YOUR_LICENSE = '''
#    ******  The Cloud Toolbox v{0}******
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
'''.format(VERSION)
LAST_LINE = '#    http://opensource.org/licenses/MIT'

KEEP_LICENSE = '*** KEEP LICENSE ***'

##### CODE -- DON'T EDIT (unless you know what you are doing!) ####
import pdb
import re
import os
import sys
import shutil

import textools

# for outside setup scripts
ctb_packages = ['cloudtb', 'cloudtb.extra', 'cloudtb.extra.PyQt', 
                  'cloudtb.tests', 'cloudtb.external',]
                  
PUBLISH_FOLDER = 'publish'
CLOUDTB_PACKAGE_STR = 'cloudtb'

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
    
#    uin = raw_input("About to overwrite license for \n<" + path + '>\n. Press y '
#        'if ok')
#    if uin.lower() == 'y':
    with open(path, 'w') as f:
        f.write(text)

def update_cloudtb(path):
    import urllib
    import zipfile
    
    ctb_path = os.path.join(path, PUBLISH_FOLDER)
    ctb_path = os.path.join(ctb_path, os.path.split(path)[1])
    ctb_path = os.path.join(ctb_path, CLOUDTB_PACKAGE_STR)
    if os.path.exists(ctb_path):
        shutil.rmtree(ctb_path)
    pubpath = os.path.join(path, PUBLISH_FOLDER)
    if not os.path.isdir(pubpath):
        os.mkdir(pubpath)
    
    if os.path.exists(CLOUDTB_VERSION_URL):
        # if it is a directory, just copy it.
        shutil.copytree(CLOUDTB_VERSION_URL, ctb_path)
        return
    
    urllib.urlretrieve(CLOUDTB_VERSION_URL,
                       filename=ctb_path + '.zip')
    
    with zipfile.ZipFile(ctb_path + '.zip') as zf:
        zf.extractall(ctb_path)
    bad_path = os.listdir(ctb_path)
    assert(len(bad_path) == 1)
    bad_path = os.path.join(ctb_path, bad_path[0])
    for f in os.listdir(bad_path):
        old_path = os.path.join(bad_path, f)
        new_path = os.path.join(ctb_path, f)
        shutil.move(old_path, new_path)
    os.rmdir(bad_path)
#    os.popen('unzip ' + )
#    for n in os.listdir(path):
#        p = os.path.join(path, n)
#        if n.find('cloudtb') == 0 and os.path.isdir(p):
#            os.rename(p, ctb_path)
#            break
#    files = os.listdir(pubpath)
#    zip_ctb_fname = next(f for f in files if PUBLISH_FOLDER in f)
#    zip_ctb_path = os.path.join(path, zip_ctb_fname)
#    os.popen('mv -r {0} {1}'.format(zip_ctb_path, ctb_path))

def copy_files(cur_dir = None):
    if cur_dir == None:
        cur_dir = os.getcwd()
    
    pubfolder = os.path.join(cur_dir, PUBLISH_FOLDER)
    if os.path.exists(pubfolder):
        if os.path.isdir(pubfolder):
            shutil.rmtree(pubfolder)
        else:
            print "removing _publish as file... odd"
            os.remove(pubfolder)
    os.mkdir(pubfolder)
    pubfolder = os.path.join(pubfolder, os.path.split(cur_dir)[1])
    os.mkdir(pubfolder)
    fnames = os.listdir(cur_dir)
    for f in fnames:
        path = os.path.join(cur_dir, f)
        print f,
        if f in (PUBLISH_FOLDER, '.git', 'dist'):
            print 'ignored'
            continue
        elif os.path.isdir(path):
            print 'copy dir'
            shutil.copytree(path, os.path.join(pubfolder, f))
        else:
            print 'copy file'
            shutil.copy2(path, pubfolder)
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
        parser = argparse.ArgumentParser(description = 
            "Update License Files for python project")
        parser.add_argument('path', type = str, help='path to file or folder')
        args = parser.parse_args()
        path = args.path
        print path
    
    update_license(path)
    copy_files(path)    
    if CLOUDTB_VERSION_URL:
        update_cloudtb(path)
    
if __name__ == '__main__':
    main()





