# -*- coding: utf-8 -*-
#
from betterbib.source import Source

from bs4 import BeautifulSoup
from pybtex.database.input import bibtex
import re
import requests
from distutils.version import StrictVersion
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class ZentralblattMref(Source):
    '''
    This class is a hack for the broken academic data politics.
    The most reliable bibiliographical data in mathematics is in MathSciNet,
    curated for free by university staff around the world. The service itself
    isn't free though, universities have to a pay a subscription fee. This
    means of course that you cannot use MathSciNet from outside a university
    network unless you're willing to pay for it. Or can you?

    The AMS offers a [web interface](http://www.ams.org/mref) that
    hooks up with MathSciNet and can be used from anywhere. Unfortunately, the
    search interface will only give you a meaningful result if there is
    _exactly_ one item in the database matching your query. If there are more,
    you'll just get a "query was not unique" type of message.

    To make sure we always submit unique search queries to MREF, we run a
    preliminary query through zbmath.org, a free and more complete search
    engine for math literature. The result thereof is then passed into MREF,
    hopefully giving the desired result.
    '''

    def __init__(self):
        return

    def find_unique(self, entry):
        result = self._mref(self._zbmath(entry))
        # parse the string into pybtex
        parser = bibtex.Parser()
        parsed_bibtex = \
            parser.parse_stream(StringIO(result))
        assert len(parsed_bibtex.entries) == 1
        entry = parsed_bibtex.entries[parsed_bibtex.entries.keys()[0]]
        return entry

    def _zbmath(self, entry):
        url = 'https://zbmath.org'

        # Typical search query:
        # https://zbmath.org?form=one-line&t=&s=0&c=100&q=au%3Aliesen+%26+ti%3Akrylov&any=&au=liesen&ti=krylov&so=&ab=&cc=&ut=&an=&la=&py=&rv=&sw=&dm=
        # None of the parameters seems to have any effect EXCEPT `q=...`, so
        # one can as well just
        # https://zbmath.org?q=au%3Aliesen+%26+ti%3Akrylov
        # Construct our request accordingly.
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
                    payload.append(['ti', entry.fields['title']])
                except KeyError:
                    continue

            if 'authors' in sc:
                try:
                    for au in entry.persons['author']:
                        payload.append(['au', ' '.join(au.last())])
                except KeyError:
                    continue

            if 'year' in sc:
                try:
                    payload.append(['py', entry.fields['year']])
                except KeyError:
                    continue

            # Search request.
            # Build the actual payload
            query = ' '.join(
                entry[0] + ':' + entry[1] for entry in payload
                )

            # For debugging, you can plug the `query` into the web interface at
            # <https://zbmath.org/>.

            # Verify the hostname certificate only for newer versions of
            # requests. For some reason, it otherwise fails on Ubuntu trusty
            # (with requests 2.2.1).
            verify = \
                StrictVersion(requests.__version__) >= StrictVersion('2.8.0')

            r = requests.get(
                    url,
                    params={'q': query},
                    verify=verify
                    )
            if not r.ok:
                raise RuntimeError(
                    'Could not fetch data (status code %d).' % r.status_code
                    )

            # Check how many documents we've found.
            m = re.search(b'Found ([0-9]+) documents', r.content)
            if m:
                num_matches = int(m.group(1))
                if num_matches in [0, 1]:
                    break
                # else len(m) > 1 .. try again with stricter criteria
            else:
                # If the string wasn't found, either have an article or no
                # match at all.
                break

        # We can here because the page doesn't contain the regex
        #    Found ([0-9]+) documents
        # This can mean that either we have an article or no results at all.
        # Test which it is.

        # Check if the website issues an error message.
        m = re.search(b'Your query produced no results', r.content)
        if m:
            raise RuntimeError(
                'No publication results on zbmath.org.'
                )

        soup = BeautifulSoup(r.content, 'lxml')

        articles = soup.find_all('article')
        if len(articles) == 1:
            # Extract data
            data = {}

            author_tags = \
                articles[0].find_all('a', {'title': 'Author Profile'})
            data['authors'] = []
            for author_tag in author_tags:
                data['authors'].append(author_tag.text)

            title_tags = \
                articles[0].find_all('div', {'class': 'title'})
            data['title'] = title_tags[0].text

            source_tags = \
                articles[0].find_all('div', {'class': 'source'})
            data['source'] = source_tags[0].text

            return data
        elif len(articles) > 1:
            raise RuntimeError(
                'Found more than one article on the page. Strange.'
                )
        else:
            raise RuntimeError('No articles found.')

    def _mref(self, data):
        '''Query AMS's MRef with the data from zbmath.
        '''
        # Typical Mref query:
        # http://www.ams.org/mref?ref=liesen&dataType=bibtex
        #
        url = 'http://www.ams.org/mref'
        search_query = \
            ' '.join(data['authors'] + [data['title']] + [data['source']])
        r = requests.get(url, params={
            'dataType': 'bibtex',
            'ref': search_query
            })

        if not r.ok:
            raise RuntimeError(
                'Could not fetch data from MRef (status code %d).' %
                r.status_code
                )

        soup = BeautifulSoup(r.content, 'lxml')
        bibtex = soup.find_all('pre')
        if len(bibtex) == 0:
            raise RuntimeError('Article not found on MRef.')
        elif len(bibtex) > 1:
            raise RuntimeError('Unexpected MRef return data.')

        return bibtex[0].contents[0]
