# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import sys


def supports_color():
    """Returns True if the running system's terminal supports color,
    and False otherwise.
    based on django.core.management.color
    """
    plat = sys.platform
    if plat == 'Pocket PC' or (plat == 'win32' and 'ANSICON' not in os.environ):
        return False
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return False
    return True


hascolor = supports_color()  # fast access
