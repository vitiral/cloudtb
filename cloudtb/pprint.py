#!/usr/bin/python3
'''
additional pprint functions, like printing a list
Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''


def pplist(l, cols=4, indent=0):
    if not isinstance(l, list):
        l = list(l)
    while len(l) % cols != 0:
        l.append(" ")
    step = len(l) // cols
    step = step if step != 0 else 1
    split = [l[i:i + len(l) // cols] for i in range(0, len(l), step)]
    for row in zip(*split):
        print(' ' * indent + "".join(str.ljust(i, 20) for i in row))
