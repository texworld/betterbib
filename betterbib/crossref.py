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

    def find(self, entry):
        url = 'http://search.crossref.org/dois'

        # Typical search query:
        # http://search.crossref.org/dois?q=%2bliesen+%2bgaul&year=2012
        #
        # Specify the search criteria. Start broad and narrow down until we
        # find exactly one result.
        #
        search_criteria = [
            ['title'],
            ['title', 'authors'],
            ['title', 'authors', 'year']
            ]

        # default (empty) payload
        for sc in search_criteria:
            payload = []
            # Add a search criterion.
            if 'title' in sc:
                try:
                    # Prefix all necessary keywords with '+'
                    payload.append(entry['title'])
                except KeyError:
                    continue

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

            r = requests.get(
                    url,
                    params={'q': query}
                    )
            if not r.ok:
                raise RuntimeError(
                    'Could not fetch data (status code %d).' % r.status_code
                    )
            data = r.json()

            if len(data) == 0:
                raise RuntimeError('Seach query unsuccessful.')
            elif len(data) == 1:
                break

        if len(data) > 1:
            raise RuntimeError('No unique match found on CrossRef')

        # Now construct a bibdata dict from the data.
        bibdata = {}

        if 'doi' in data[0]:
            bibdata['doi'] = data[0]['doi']

        if 'title' in data[0]:
            bibdata['title'] = data[0]['title']

        if 'year' in data[0]:
            bibdata['year'] = data[0]['year']

        if 'coins' in data[0]:
            coins = urlparse.parse_qs(data[0]['coins'])

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

        return
