# -*- coding: utf-8 -*-
#


class Source(object):
    '''
    Abstract base class for all BibTeX sources.
    '''
    def find_unique(self, bibtex_entry):
        raise NotImplementedError
