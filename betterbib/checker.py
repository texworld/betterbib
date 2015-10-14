# -*- coding: utf-8 -*-
#
class Checker(object):
    '''
    Abstract base class for all BibTeX checkers.
    '''
    def find(self, bibtex_entry):
        raise NotImplementedError
