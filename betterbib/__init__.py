# -*- coding: utf-8 -*-
#
from __future__ import print_function
from betterbib.bibtex import pybtex_to_dict, \
        pybtex_to_bibtex_string, \
        latex_to_unicode
from betterbib.crossref import Crossref

from betterbib.__about__ import (
    __version__,
    __author__,
    __author_email__,
    __website__,
    )

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__))
