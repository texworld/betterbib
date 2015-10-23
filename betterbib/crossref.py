# -*- coding: utf8 -*-
#
from betterbib.source import Source
from betterbib.bibtex import pybtex_to_bibtex_string, pybtex_to_dict

import pybtex.core
import re
import requests


class Crossref(Source):
    '''
    Documentation of the CrossRef Search API:
    <http://search.crossref.org/help/api>.
    '''

    def __init__(self):
        return

    def find_unique(self, entry):
        url = 'https://api.crossref.org/works'

        d = pybtex_to_dict(entry)

        # add title with '+' instead of spaces
        l = ['+'.join(d['title'].split())]

        # add authors
        for au in d['author']:
            l.extend([
                ' '.join(au['first']), ' '.join(au['middle']),
                ' '.join(au['prelast']), ' '.join(au['last']),
                ' '.join(au['lineage'])
                ])

        # kick out empty strings
        l = filter(None, l)

        # Simply plug the dict together to a search query. Typical query:
        # https://api.crossref.org/works?query=vanroose+schl%C3%B6mer&rows=5
        payload = '+'.join(l)

        params = {
            'query': payload,
            'rows': 5  # get at most 5 search results
            }

        r = requests.get(
                url,
                params=params
                )
        if not r.ok:
            raise RuntimeError(
                'Could not fetch data (status code %d).' % r.status_code
                )
        data = r.json()

        results = data['message']['items']

        if results[0]['score'] > 2 * results[1]['score']:
            # Q: When do we treat a search result as unique?
            # As a heuristic, assume that the top result is the unique answer
            # if its score is at least double the score of the the second-best
            # result.
            bibtex_key = 'testkey'
            entry = self._crossref_to_pybtex(results[0])
            return pybtex_to_bibtex_string(entry, bibtex_key)
        else:
            raise RuntimeError('Could not find a positively unique match.')

    def _crossref_to_pybtex(self, data):
        '''Translate a given data set into the bibtex data structure.
        '''
        # A typcial search result is
        #
        # {
        #   u'DOI': u'10.1137/110820713',
        #   u'subtitle': [],
        #   u'issued': {u'date-parts': [[2013, 4, 4]]},
        #   u'prefix': u'http://id.crossref.org/prefix/10.1137',
        #   u'author': [
        #     {u'affiliation': [], u'given': u'Andr\xe9', u'family': u'Gaul'},
        #     {u'affiliation': [], u'given': u'Martin H.', u'family': u'Gutknecht'},
        #     {u'affiliation': [], u'given': u'J\xf6rg', u'family': u'Liesen'},
        #     {u'affiliation': [], u'given': u'Reinhard', u'family': u'Nabben'}
        #   ],
        #   u'reference-count': 55,
        #   u'ISSN': [u'0895-4798', u'1095-7162'],
        #   u'member': u'http://id.crossref.org/member/351',
        #   u'source': u'CrossRef',
        #   u'score': 3.3665228,
        #   u'deposited': {
        #     u'timestamp': 1372345787000,
        #     u'date-time': u'2013-06-27T15:09:47Z',
        #     u'date-parts': [[2013, 6, 27]]
        #   },
        #   u'indexed': {
        #     u'timestamp': 1442739318395,
        #     u'date-time': u'2015-09-20T08:55:18Z',
        #     u'date-parts': [[2015, 9, 20]]
        #   },
        #   u'type': u'journal-article',
        #   u'URL': u'http://dx.doi.org/10.1137/110820713',
        #   u'volume': u'34',
        #   u'publisher': u'Society for Industrial & Applied Mathematics (SIAM)',
        #   u'created': {
        #     u'timestamp': 1368554571000,
        #     u'date-time': u'2013-05-14T18:02:51Z',
        #     u'date-parts': [[2013, 5, 14]]
        #   },
        #   u'issue': u'2',
        #   u'title': [u'A Framework for Deflated and Augmented Krylov Subspace Methods'],
        #   u'alternative-id': [u'10.1137/110820713'],
        #   u'container-title': [u'SIAM. J. Matrix Anal. & Appl.', u'SIAM Journal on Matrix Analysis and Applications'],
        #   u'page': u'495-518'
        # }
        #
        return pybtex.core.Entry(
            'article',
            fields={
                'doi': data['DOI'],
                'issue': data['issue'],
                # take the shortest of the journal names
                'journal': min(data['container-title'], key=len),
                'pages': data['page'],
                'title': data['title'][0],
                'volume': data['volume'],
                'year': data['issued']['date-parts'][0][0]
            },
            persons={'author': [
                pybtex.core.Person('%s, %s' % (au['family'], au['given']))
                for au in data['author']
                ]}
            )
