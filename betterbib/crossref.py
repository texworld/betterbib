# -*- coding: utf-8 -*-
#
from betterbib.bibtex import pybtex_to_dict, latex_to_unicode

import pybtex
import re
import requests


class Crossref(object):
    '''
    Documentation of the CrossRef Search API:
    <https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md>.
    '''

    def __init__(self):
        self.api_url = 'https://api.crossref.org/works'
        return

    def _crossref_to_bibtex_type(self, entry):
        # The difficulty here: Translating book-chapter. If the book is a
        # monograph (all chapters written by the same set of authors), then
        # return inbook, if all chapters are by different authors, return
        # incollection.
        crossref_type = entry['type']
        if crossref_type == 'book-chapter':
            # Get the containing book, and see if it has authors or editors. If
            # authors, consider it a monograph and use inbook; otherwise
            # incollection.
            # To get the book, make use of the fact that the chapter DOIs are
            # the book DOI plus some appendix, e.g., .ch3, _3, etc. In other
            # words: Strip the last digits plus whatever is nondigit before it.
            a = re.match('(.*?)([^0-9]+[0-9]+)$', entry['DOI'])
            if a is None:
                # The DOI doesn't have that structure; assume 'incollection'.
                return 'incollection'

            book_doi = a.group(1)

            # Get the book data
            r = requests.get(self.api_url + '/' + book_doi)
            assert r.ok

            book_data = r.json()

            if 'author' in book_data['message']:
                return 'inbook'
            # else
            return 'incollection'

        # All other cases
        _crossref_to_bibtex_type = {
            'book': 'book',
            'journal-article': 'article',
            'proceedings-article': 'inproceedings',
            'report': 'techreport'
            }
        return _crossref_to_bibtex_type[crossref_type]

    def _bibtex_to_crossref_type(self, bibtex_type):
        _bibtex_to_crossref_type = {
            'article': 'journal-article',
            'book': 'book',
            'inbook': 'book-chapter',
            'incollection': 'book-chapter',
            'inproceedings': 'proceedings-article',
            'techreport': 'report'
            }
        return _bibtex_to_crossref_type[bibtex_type]

    def find_unique(self, entry):

        d = pybtex_to_dict(entry)

        l = []

        try:
            l.append(d['title'])
        except KeyError:
            pass

        try:
            for au in d['author']:
                l.extend([
                    ' '.join(au['first']), ' '.join(au['middle']),
                    ' '.join(au['prelast']), ' '.join(au['last']),
                    ' '.join(au['lineage'])
                    ])
        except KeyError:
            pass

        try:
            l.append(d['journal'])
        except KeyError:
            pass

        try:
            l.append(d['doi'])
        except KeyError:
            pass

        try:
            l.append(d['pages'])
        except KeyError:
            pass

        try:
            l.append(d['year'])
        except KeyError:
            pass

        try:
            l.append(d['volume'])
        except KeyError:
            pass

        try:
            l.append(d['number'])
        except KeyError:
            pass

        try:
            l.append(d['publisher'])
        except KeyError:
            pass

        # kick out empty strings
        l = filter(None, l)

        # Simply plug the dict together to a search query. Typical query:
        # https://api.crossref.org/works?query=vanroose+schl%C3%B6mer&rows=5
        payload = latex_to_unicode(' '.join(l)).replace(' ', '+')

        params = {
            'query': payload,
            'filter': 'type:%s' % self._bibtex_to_crossref_type(entry.type),
            'rows': 2  # max number of results
            }

        r = requests.get(self.api_url, params=params)
        assert r.ok

        data = r.json()

        results = data['message']['items']

        if len(results) == 1:
            return self._crossref_to_pybtex(results[0])

        # Q: How to we find the correct solution if there's more than one
        #    search result?
        # As a heuristic, assume that the top result is the unique answer if
        # its score is at least 1.5 times the score of the the second-best
        # result.
        # If that doesn't work, check if the DOI matches exactly with the
        # input.
        if len(results) > 1:
            if results[0]['score'] > 1.5 * results[1]['score']:
                return self._crossref_to_pybtex(results[0])

            # Check if any of the DOIs matches exactly
            if 'doi' in d:
                for result in results:
                    if result['DOI'].lower() == d['doi'].lower():
                        return self._crossref_to_pybtex(result)

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
        #     {u'affiliation': [], u'given': u'Martin', u'family': u'Gut'},
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
        #   u'publisher': u'Soc. for Industrial & Applied Mathematics (SIAM)',
        #   u'created': {
        #     u'timestamp': 1368554571000,
        #     u'date-time': u'2013-05-14T18:02:51Z',
        #     u'date-parts': [[2013, 5, 14]]
        #   },
        #   u'issue': u'2',
        #   u'title': [u'A Framework for Deflated Krylov Subspace Methods'],
        #   u'alternative-id': [u'10.1137/110820713'],
        #   u'container-title': [
        #     u'SIAM. J. Matrix Anal. & Appl.',
        #     u'SIAM Journal on Matrix Analysis and Applications'
        #   ],
        #   u'page': u'495-518'
        # }
        #
        # translate the type
        bibtex_type = self._crossref_to_bibtex_type(data)

        fields_dict = {}
        try:
            fields_dict['doi'] = data['DOI']
        except KeyError:
            pass

        try:
            fields_dict['number'] = data['issue']
        except KeyError:
            pass

        try:
            fields_dict['pages'] = data['page']
        except KeyError:
            pass

        try:
            fields_dict['source'] = data['source']
        except KeyError:
            pass

        try:
            fields_dict['url'] = data['URL']
        except KeyError:
            pass

        try:
            # Take the first container names.
            # This is typically the abbreviated journal name in case of a
            # journal, and the full book title in case of a book.
            if len(data['container-title']) > 0:
                container_title = data['container-title'][0]
            else:
                container_title = None
        except (KeyError, ValueError):
            container_title = None

        try:
            title = data['title'][0]
        except KeyError:
            title = None

        try:
            publisher = data['publisher']
        except KeyError:
            publisher = None

        if bibtex_type == 'article':
            if container_title:
                fields_dict['journal'] = container_title
            if publisher:
                fields_dict['publisher'] = publisher
            if title:
                fields_dict['title'] = title
        elif bibtex_type == 'book':
            if publisher:
                fields_dict['publisher'] = publisher
            if title:
                fields_dict['title'] = title
        elif bibtex_type == 'inbook':
            if container_title:
                # or title?
                fields_dict['booktitle'] = container_title
            if publisher:
                fields_dict['publisher'] = publisher
            if title:
                fields_dict['chapter'] = title
        elif bibtex_type == 'incollection':
            if container_title:
                fields_dict['booktitle'] = container_title
            if publisher:
                fields_dict['publisher'] = publisher
            if title:
                fields_dict['title'] = title
        elif bibtex_type == 'inproceedings':
            if container_title:
                fields_dict['booktitle'] = container_title
            if publisher:
                fields_dict['publisher'] = publisher
            if title:
                fields_dict['title'] = title
        elif bibtex_type == 'techreport':
            if publisher:
                fields_dict['institution'] = publisher
            if title:
                fields_dict['title'] = title
        else:
            raise ValueError('Unknown type \'%s\'' % bibtex_type)

        try:
            fields_dict['volume'] = data['volume']
        except KeyError:
            pass

        try:
            fields_dict['year'] = data['issued']['date-parts'][0][0]
        except KeyError:
            pass

        try:
            fields_dict['month'] = data['issued']['date-parts'][0][1]
        except (IndexError, KeyError):
            pass

        try:
            persons = {'author': [
                pybtex.database.Person('%s, %s' % (au['family'], au['given']))
                for au in data['author']
                ]}
        except KeyError:
            persons = None

        return pybtex.database.Entry(
            bibtex_type,
            fields=fields_dict,
            persons=persons
            )
