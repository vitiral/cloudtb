# -*- coding: utf-8 -*-
'''
Convenience functions for python's standard platform module
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import platform as _platform
import ctypes
import re
import subprocess
import psutil


def processor():
    '''Get type of processor
    http://stackoverflow.com/questions/4842448/getting-processor-information-in-python
    '''
    out = None
    if _platform.system() == "Windows":
        out = _platform.processor()
    elif _platform.system() == "Darwin":
        path = os.environ['PATH']
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        try:
            command = "sysctl -n machdep.cpu.brand_string"
            out = subprocess.check_output(command, shell=True).strip().decode()
        finally:
            os.environ['PATH'] = path
    elif _platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip().decode()
        for line in all_info.split("\n"):
            if "model name" in line:
                out = re.sub(".*model name.*:", "", line, 1)

    if out is None:
        return _platform.processor()
    else:
        return out


def platform():
    '''Returns all platform data in a dictionary'''
    out = {key: getattr(_platform, key)() for key in
           ('machine', 'version', 'platform', 'dist', 'system')}
    out['python'] = {
        key: getattr(_platform, "python_" + key)() for key in
        ('implementation', 'compiler', 'version', 'version_tuple')
    }
    out['python']['architecture'] = int(ctypes.sizeof(ctypes.c_voidp) * 8)
    out['processor'] = processor()
    out['cores'] = len(psutil.cpu_percent(percpu=True))
    return out


if __name__ == '__main__':
    from pprint import pprint
    print("Processor")
    print(processor())
    print("\nPlatform")
    pprint(platform())
