# -*- coding: utf8 -*-
#
from betterbib.source import Source

import re
import requests
import urlparse


class Crossref(Source):
    '''
    Documentation of the CrossRef Search API:
    <http://search.crossref.org/help/api>.
    '''

    def __init__(self):
        return

    def find_unique(self, entry):
        # Specify the search criteria. Start broad and narrow down until we
        # find exactly one result.
        #
        search_criteria = [
            ['title'],
            ['title', 'authors'],
            ['title', 'authors', 'genre'],
            ['title', 'authors', 'genre', 'year']
            ]

        # default (empty) payload
        for sc in search_criteria:
            out = self.find(sc, entry)
            if len(out) == 1:
                return out[0]

        print(len(out))
        print(out)
        raise RuntimeError('No unique match found')

    def find(self, sc, entry):
        url = 'http://search.crossref.org/dois'

        # Typical search query:
        # http://search.crossref.org/dois?q=%2bliesen+%2bgaul&year=2012
        #
        payload = []

        if 'title' in sc:
            payload.append(entry['title'])

        if 'authors' in sc:
            authors = entry['author'].split(' and ')
            # Extract everything up to the first comma of `author`
            # which is hopefully the last name.
            last_names = [
                re.sub('([^,]+),.*', r'\1', author)
                for author in authors
                ]
            for last_name in last_names:
                payload.append(last_name)

        # Search request.
        query = ' '.join(payload)
        # CrossRef: Add '+' to all required keywords
        query = '+' + query.replace(' ', ' +')
        params = {'q': query}

        if 'year' in sc:
            params['year'] = entry['year']

        if 'genre' in sc:
            if entry['genre'] == 'book':
                params['type'] = 'Monograph'
            else:
                raise RuntimeError('Unknown genre \'%s\'.' % entry['genre'])

        print(params)
        r = requests.get(
                url,
                params=params
                )
        if not r.ok:
            raise RuntimeError(
                'Could not fetch data (status code %d).' % r.status_code
                )
        data = r.json()

        return [self._translate_to_bibdata(item) for item in data]

    def _translate_to_bibdata(self, data):
        '''Translate a given data set into the bibtex data structure.
        '''
        bibdata = {}
        if 'doi' in data:
            bibdata['doi'] = data['doi']

        if 'title' in data:
            bibdata['title'] = data['title']

        if 'year' in data:
            bibdata['year'] = data['year']

        if 'coins' in data:
            coins = urlparse.parse_qs(data['coins'])

            if 'rft.spage' in coins:
                bibdata['spage'] = coins['rft.spage'][0]

            if 'rft.epage' in coins:
                bibdata['epage'] = coins['rft.epage'][0]

            if 'rft.au' in coins:
                bibdata['authors'] = coins['rft.au']

            if 'rft.volume' in coins:
                bibdata['volume'] = coins['rft.volume'][0]

            if 'rft.issue' in coins:
                bibdata['issue'] = coins['rft.issue'][0]

            if 'rft.date' in coins:
                bibdata['year'] = coins['rft.date'][0]

            if 'rft.atitle' in coins:
                bibdata['title'] = coins['rft.atitle'][0]

            if 'rft.ctx_ver' in coins:
                bibdata['ctx_ver'] = coins['rft.ctx_ver'][0]

            if 'rft.jtitle' in coins:
                bibdata['journal'] = coins['rft.jtitle'][0]

            if 'rft.genre' in coins:
                bibdata['genre'] = coins['rft.genre'][0]

        return bibdata
