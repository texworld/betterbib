# -*- coding: utf-8 -*-
#
from __future__ import print_function

from .errors import NotFoundError, UniqueError, HttpError
from .tools import pybtex_to_dict, latex_to_unicode, doi_from_url

import pybtex
import pybtex.database
import requests


class Dblp(object):
    '''
    Documentation of the DBLP Search API:
    <http://dblp.uni-trier.de/faq/How+to+use+the+dblp+search+API.html>.
    '''

    def __init__(self, prefer_long_journal_name=False):
        self.api_url = 'https://dblp.org/search/publ/api'
        return

    def _to_bibtex_type(self, entry):
        # The difficulty here: Translating book-chapter. If the book is a
        # monograph (all chapters written by the same set of authors), then
        # return inbook, if all chapters are by different authors, return
        # incollection.
        assert entry['type'] == 'Journal Articles'
        return 'article'

    # pylint: disable=too-many-return-statements
    def find_unique(self, entry):
        d = pybtex_to_dict(entry)

        # Be stingy on the search terms. DBLP search is not fuzzy, so one
        # misspelled word results in 0 hits.
        L = []

        try:
            L.append(d['title'])
        except KeyError:
            pass

        try:
            for au in d['author']:
                L.append(' '.join(au['last']))
        except KeyError:
            pass

        # replace multiple whitespace by one, remove surrounding spaces
        for k in range(len(L)):
            L[k] = ' '.join(L[k].split())

        # kick out empty strings
        L = list(filter(None, L))

        # Simply plug the dict together to a search query. Typical query:
        # <api>?q=vanroose+schl%C3%B6mer&h=5
        payload = latex_to_unicode(' '.join(L)).replace(' ', '+')

        params = {
            'q': payload,
            'format': 'json',
            'h': 2  # max number of results (hits)
            }

        r = requests.get(self.api_url, params=params)
        if not r.ok:
            raise HttpError('Failed request to {}'.format(self.api_url))

        data = r.json()

        try:
            results = data['result']['hits']['hit']
        except KeyError:
            raise NotFoundError('No match')

        if len(results) == 1:
            return self._dblp_to_pybtex(results[0]['info'])

        # Q: How to we find the correct solution if there's more than one
        #    search result?
        # As a heuristic, assume that the top result is the unique answer if
        # its score is at least 1.5 times the score of the the second-best
        # result.
        if float(results[0]['@score']) > 1.5 * float(results[1]['@score']):
            return self._crossref_to_pybtex(results[0]['info'])

        # If that doesn't work, check if the DOI matches exactly with the
        # input.
        if 'doi' in d:
            # sometimes, the doi field contains a doi url
            doi = doi_from_url(d['doi'])
            if not doi:
                doi = d['doi']
            for result in results:
                if result['DOI'].lower() == doi.lower():
                    return self._crossref_to_pybtex(result['info'])

        # If that doesn't work, check if the title appears in the input.
        if 'title' in d:
            for result in results:
                if 'title' in result and result['title'] and \
                        result['title'][0].lower() in d['title'].lower():
                    return self._crossref_to_pybtex(result['info'])

        # If that doesn't work, check if the page range matches exactly
        # with the input.
        if 'pages' in d:
            for result in results:
                if 'page' in result and result['page'] == d['pages']:
                    return self._crossref_to_pybtex(result['info'])

        raise UniqueError('Could not find a positively unique match.')

    def _dblp_to_pybtex(self, data):
        '''Translate a given data set into the bibtex data structure.
        '''
        # A typcial search result is
        #
        #   'info': {
        #       'authors': {'author': [
        #                      'André Gaul',
        #                      'Martin H. Gutknecht',
        #                      'Jörg Liesen',
        #                      'Reinhard Nabben'
        #                      ]},
        #    'doi': '10.1137/110820713',
        #    'ee': 'https://doi.org/10.1137/110820713',
        #    'key': 'journals/siammax/GaulGLN13',
        #    'number': '2',
        #    'pages': '495-518',
        #    'title': 'A Framework for Deflated and Augmented Krylov '
        #             'Subspace Methods.',
        #    'type': 'Journal Articles',
        #    'url': 'http://dblp.org/rec/journals/siammax/GaulGLN13',
        #    'venue': 'SIAM J. Matrix Analysis Applications',
        #    'volume': '34',
        #    'year': '2013'
        #    },
        #
        # translate the type
        bibtex_type = self._to_bibtex_type(data)

        fields_dict = {}
        try:
            fields_dict['doi'] = data['doi']
        except KeyError:
            pass

        try:
            fields_dict['number'] = data['number']
        except KeyError:
            pass

        try:
            fields_dict['pages'] = data['pages']
        except KeyError:
            pass

        try:
            fields_dict['source'] = data['source']
        except KeyError:
            fields_dict['source'] = 'DBLP'

        try:
            fields_dict['url'] = data['ee']
        except KeyError:
            pass

        try:
            container_title = data['venue']
        except KeyError:
            container_title = None

        try:
            title = data['title']
        except KeyError:
            title = None

        assert bibtex_type == 'article'
        if container_title:
            fields_dict['journal'] = container_title
        if title:
            fields_dict['title'] = title

        try:
            fields_dict['volume'] = data['volume']
        except KeyError:
            pass

        try:
            fields_dict['year'] = data['year']
        except KeyError:
            pass

        try:
            persons = {'author': [
                pybtex.database.Person(au)
                for au in data['authors']['author']
                ]}
        except (KeyError, pybtex.database.InvalidNameString):
            persons = None

        return pybtex.database.Entry(
            bibtex_type,
            fields=fields_dict,
            persons=persons
            )
