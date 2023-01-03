'''
Author @ Nikesh Bajaj
Version : 1.0.7
Contact: n.bajaj@qmul.ac.uk
       : n.bajaj@imperial.ac.uk
       : http://nikeshbajaj.in
-----changelog-------------------
first created : Date: 22 Oct 2017
Updated on : 29 Apr 2021 (version:1.0.6)
           : fixed bugs (1) not counting first outbit correctly (2) Exception in info method
		   : added test properties (1) Balance (2) Runlength (3) Autocorrelation
           : improved functionalities
           : added Viz function
           : added A5/1 and Geffe Generator
Updated on : 03 Jan 2023 (version:1.0.7)
           : Added Galois Configuration for LFSR
           : fixed bugs, improved documentation
'''

from __future__ import absolute_import, division, print_function

name = "Linear Feedback Shift Register"

__version__ = '1.0.7'
__author__ = 'Nikesh Bajaj'

import sys, os

sys.path.append(os.path.dirname(__file__))

from .pylfsr import (LFSR, PlotLFSR, dispLFSR)
from .seq_generators import (A5_1, Geffe, Geffe3)
from .utils import (lempel_ziv_patterns, lempel_ziv_complexity, get_fpolyList, get_Ifpoly)
from .utils import (pretty_print, print_list, progbar, deprecated)
