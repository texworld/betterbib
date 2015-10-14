# -*- coding: utf-8 -*-
#
from betterbib.bibtex import get_string_representation, read_bibtex
from betterbib.connector import Connector
from betterbib.dictdiffer import adds_info
from betterbib.mathscinet import MathSciNet
from betterbib.progress_bar import ProgressBar

__all__ = [
    'bibtex',
    'connector',
    'dictdiffer',
    'mathscinet',
    'progress_bar'
    ]

__name__ = 'betterbib'
__version__ = '0.3.0'
__author__ = 'Nico Schlömer'
__author_email__ = 'nico.schloemer@gmail.com'
__website__ = 'https://github.com/nschloe/betterbib'
