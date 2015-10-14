# -*- coding: utf8 -*-
#


class Connector(object):
    '''
    Abstract base class for all BibTeX connectors.
    '''
    def find(self, bibtex_entry):
        raise NotImplementedError
