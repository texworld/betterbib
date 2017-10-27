# -*- coding: utf-8 -*-
#
from __future__ import print_function

import pybtex
import pybtex.database
import requests

from .errors import NotFoundError, HttpError
from .tools import pybtex_to_dict, latex_to_unicode, heuristic_unique_result


def _to_bibtex_type(entry):
    # The difficulty here: Translating book-chapter. If the book is a
    # monograph (all chapters written by the same set of authors), then
    # return inbook, if all chapters are by different authors, return
    # incollection.
    assert entry['type'] == 'Journal Articles'
    return 'article'


def _dblp_to_pybtex(data):
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
    bibtex_type = _to_bibtex_type(data)

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


class Dblp(object):
    '''
    Documentation of the DBLP Search API:
    <http://dblp.uni-trier.de/faq/How+to+use+the+dblp+search+API.html>.
    '''

    def __init__(self):
        self.api_url = 'https://dblp.org/search/publ/api'
        return

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
            return _dblp_to_pybtex(results[0]['info'])

        return _dblp_to_pybtex(
            heuristic_unique_result(results, d)['info']
            )
