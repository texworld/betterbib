# -*- coding: utf8 -*-
#


class Source(object):
    '''
    Abstract base class for all BibTeX sources.
    '''
    def find(self, bibtex_entry):
        raise NotImplementedError
