# -*- coding: utf8 -*-
#


class Checker(object):
    '''
    Abstract base class for all BibTeX checkers.
    '''
    def find(self, bibtex_entry):
        raise NotImplementedError
