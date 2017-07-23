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

import pipdated
if pipdated.needs_checking(__name__):
    print(pipdated.check(__name__, __version__))
