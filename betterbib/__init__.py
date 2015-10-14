# -*- coding: utf-8 -*-
#
from betterbib.bibtex import get_string_representation, read_bibtex
from betterbib.checker import Checker
from betterbib.dictdiffer import adds_info
from betterbib.mathscinet import MathSciNet
from betterbib.progress_bar import ProgressBar

__all__ = [
    'bibtex',
    'checker',
    'dictdiffer',
    'mathscinet',
    'progress_bar'
    ]

__name__ = 'betterbib'
__version__ = '0.2.0'
__author__ = 'Nico Schlömer'
__author_email__ = 'nico.schloemer@gmail.com'
__website__ = 'https://github.com/nschloe/betterbib'
