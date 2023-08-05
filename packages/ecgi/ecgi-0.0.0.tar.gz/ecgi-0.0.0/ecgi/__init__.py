from __future__ import absolute_import, division, print_function

name = "ECGI toolkit"
__version__ = '0.0.0'
__author__ = 'Nikesh Bajaj'


import sys, os

sys.path.append(os.path.dirname(__file__))


#LFSR
#from .pylfsr import LFSR

from .processing import *
