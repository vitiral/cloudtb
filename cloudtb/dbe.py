# -*- coding: utf-8 -*-
'''
Debug On Exception library. Import this to automatically go into the debugger
when there is a fatal exception. Can also be called by:
    python3 -m cloudtb.dbe myscript.py

Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys

try:
    import ipdb as pdb
except ImportError:
    import pdb


def except_hook(exctype, value, traceback):
    # if previous_except_hook:
    #     previous_except_hook(exctype, value, traceback)
    pdb.post_mortem(traceback)

_usage = ('call a script with this to enter debugger automatically on fatal'
          'exception')


def main():
    import sys
    if len(sys.argv) < 2:
        print(_usage)
        sys.exit(1)

    from bdb import BdbQuit
    try:
        import ipdb as pdb
    except ImportError:
        import pdb

    mainfile = sys.argv[1]
    sys.argv.pop(0)  # clear this script from argv

    #_runscript method: https://hg.python.org/cpython/file/3.4/Lib/pdb.py
    import __main__
    import builtins
    __main__.__dict__.clear()
    __main__.__dict__.update({"__name__": "__main__",
                              "__file__": mainfile,
                              "__builtins__": builtins,
                              })

    # run method: https://hg.python.org/cpython/file/3.4/Lib/bdb.py
    with open(mainfile, "rb") as fp:
        statement = "exec(compile(%r, %r, 'exec'))" % \
                    (fp.read(), mainfile)

    try:
        exec(compile(statement, "<string>", "exec"))
    except BdbQuit:
        pass
    except Exception as e:
        pdb.post_mortem(e.__traceback__)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
else:
    previous_except_hook = sys.excepthook
    sys.excepthook = except_hook

