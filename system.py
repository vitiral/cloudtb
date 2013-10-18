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

import sys, os
import csv
import StringIO
import inspect


'''
Some on useful modules not included:
    - The module "atexit" can be used to write data on an exit
    - the module tempfile with gettempdir

'''

def guess_is_acii_text(path, ext):
    pass

    
def is_file_ext(path, ext):
    n, fext = os.path.splitext(path)

def import_path(fullpath, do_reload = False):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.insert(0, path)
    try:
        module = __import__(filename)
        if do_reload:
            reload(module)
    finally:
        del sys.path[0]
    return module

def set_priority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process to "below normal" but can take any valid process ID and priority.
        http://code.activestate.com/recipes/496767-set-process-priority-in-windows/
        """

    import win32api,win32process,win32con

    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])

class print_twice(object):
    '''replaces std_out to print to both a file object and the standard
    print location'''
    def __init__(self, fname):
        self.stdout = sys.stdout
        sys.stdout = self
        self.file = open(fname, 'w')

    def write(self, text):
        self.stdout.write(text)
        self.file.write(text)

if os.name in ("nt", "dos"):
     exefile = ".exe"
else:
     exefile = ""

def win_run(program, *args, **kw):
    '''For running stuff on Windows. Used in spawn'''
    mode = kw.get("mode", os.P_WAIT)
    for path in os.environ["PATH"].split(os.pathsep):
        fpath = os.path.join(path, program) + ".exe"
        try:
            return os.spawnv(mode, fpath, (fpath,) + args)
        except os.error:
            pass
    raise os.error, "cannot find executable"

def spawn(program, *args):
    '''Forgot for sure what this does but I think it spawns a new process
    that is not dependent on the python one'''
    try:
        # check if the os module provides a shortcut
        return os.spawnvp(program, (program,) + args)
    except AttributeError:
        pass
    try:
        spawnv = os.spawnv
    except AttributeError:
        # assume it's unix
        pid = os.fork()
        if not pid:
             os.execvp(program, (program,) + args)
        return os.wait()[0]
    else:
        # got spawnv but no spawnp: go look for an executable
        for path in os.environ["PATH"].split(os.pathsep):
             fpath = os.path.join(path, program) + exefile
             try:
                 return spawnv(os.P_WAIT, fpath, (fpath,) + args)
             except os.error:
                 pass
        raise IOError, "cannot find executable"

def module_path(local_function):
    ''' returns the module path without the use of __file__.  Requires a function defined
    locally in the module.  This is necessary for some applications like IDLE.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(inspect.getsourcefile(local_function))

def safe_eval(eval_str, variable_dict = None):
    '''Can evaluate expressions without passing in anything the user could use
    to "screw up" the program.

    It is almost completely safe. It is CERTAINLY safe from user error.
    However it is not safe from a complete hacker
    See:  http://lybniz2.sourceforge.net/safeeval.html
    '''
    if variable_dict == None:
        variable_dict = {}
    return eval(eval_str, {"__builtins__" : None}, variable_dict)

def get_user_directory():
    try:
        return os.environ['USERPROFILE']
    except KeyError:
        return os.environ['HOME']

def std_strf_time():
    '''Gets a standard datetime string'''
    return time.strftime('%b %d,%Y %X', time.localtime())

''' Copy Pasting functionality to-from python'''
from external import pyperclip
def user_copy_array(data):
    '''Puts a 2D array into the copy buffer, split by tabs'''
    #TODO make this work for either 1D or 2D arrays
    buf = StringIO.StringIO()
    writer = csv.writer(buf, 'excel-tab')
    depth, data = iteration.find_depth(data)
    if depth == 0:
        data = ((data,),)
    elif depth == 1:
        data = (tuple((str(c) if c != '' else '' for c in r),))
    elif depth == 2:
        data = tuple((tuple((str(c) if c != '' else '' for c in r)) for r in data))

    writer.writerows(data)
    buf.seek(0)
    #TODO: is this really valid??? why did I replace the \n?
    copystr = buf.read().replace('\n', '')
    user_copy_str(copystr)

def user_copy_str(copy_str):
    pyperclip.copy(copy_str)

def user_get_clipboard():
    out = pyperclip.paste()
    return out

def user_get_clipboard_data():
    data_str = user_get_clipboard()
    return get_data_from_csvtab(data_str)

def dev1():
    win_run("python", "hello.py", mode = os.P_NOWAITO)

    from time import sleep
    for _n in range(3):
        print "still here"
        sleep(1)