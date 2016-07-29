# -*- coding: utf-8 -*-
#
from betterbib.bibtex import pybtex_to_dict, \
        pybtex_to_bibtex_string, read_bibtex, \
        latex_to_unicode
from betterbib.crossref import Crossref
from betterbib.dictdiffer import adds_info
from betterbib.progress_bar import ProgressBar

__all__ = [
    'bibtex',
    'crossref',
    'dictdiffer',
    'progress_bar',
    ]

__version__ = '1.1.2'
__author__ = 'Nico Schlömer'
__author_email__ = 'nico.schloemer@gmail.com'
__website__ = 'https://github.com/nschloe/betterbib'
