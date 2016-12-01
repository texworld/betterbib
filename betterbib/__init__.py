# -*- coding: utf-8 -*-
#
from betterbib.bibtex import pybtex_to_dict, \
        pybtex_to_bibtex_string, \
        latex_to_unicode
from betterbib.crossref import Crossref

__all__ = [
    'bibtex',
    'crossref',
    ]

__version__ = '2.1.4'
__author__ = 'Nico Schlömer'
__author_email__ = 'nico.schloemer@gmail.com'
__website__ = 'https://github.com/nschloe/betterbib'
