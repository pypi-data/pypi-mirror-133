'''
Author @ Nikesh Bajaj
Date: 22 Oct 2017
Contact: n.bajaj@imperial.ac.uk

Initiated on : 01 Jan 2022
Version : 0.0.0

'''

from __future__ import absolute_import, division, print_function
name = "ECGI toolkit"
import sys

if sys.version_info[:2] < (3, 3):
    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        if flush:
            file = kwargs.get('file', sys.stdout)
            # Why might file=None? IDK, but it works for print(i, file=None)
            file.flush() if file is not None else sys.stdout.flush()

import numpy as np


def read_bdf(file):
    print(file)
    return


def load_beat(file):
    print(file)
    return


def create_geom(X,T):
    geom = None
    print(X)
    print(T)
    return geom


def inverse_solution():
    print('hello')
    return

if __name__ == '__main__':
	import doctest
	doctest.testmod()
