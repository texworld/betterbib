# -*- coding: utf8 -*-
#
from betterbib.source import Source

from bs4 import BeautifulSoup
import re
import requests


class ZentralblattMref(Source):
    '''
    This class is a hack for the broken academic data politics.
    The most reliable bibiliographical data in mathematics is in MathSciNet,
    curated for free by university staff around the world. The service itself
    isn't free though, universities have to a pay a subscription fee. This
    means of course that you cannot use MathSciNet from outside a university
    network unless you're willing to pay for it. Or can you?

    The AMS offers a [web interface](http://www.ams.org/mathscinet-mref) that
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

    def _test_connection(self):
        '''Test the connection with Zentralblatt/Mref.
        '''
        test_entry = {
                'title': 'Krylov subspace methods',
                'author': 'Liesen and Strakoš',
                'year': '2013'
                }

        # Define the expected return string. Note that special characters need
        # to be escaped.
        expected = '''@book {MR3024841,
    AUTHOR = {Liesen, J{\\"o}rg and Strako{\\v{s}}, Zden{\\v{e}}k},
     TITLE = {Krylov subspace methods},
    SERIES = {Numerical Mathematics and Scientific Computation},
      NOTE = {Principles and analysis},
 PUBLISHER = {Oxford University Press, Oxford},
      YEAR = {2013},
     PAGES = {xvi+391},
      ISBN = {978-0-19-965541-0},
   MRCLASS = {65F10 (65F15)},
  MRNUMBER = {3024841},
MRREVIEWER = {Melina A. Freitag},
}'''
        bt = self.find(test_entry)
        # Check the result.
        if bt != expected:
            diff = difflib.Differ().compare(bt, expected)
            diff = ''.join([
                '***' + i[2:] + '***' if i[:1] == '+'
                else i[2:] for i in diff if not i[:1] in '-?'
                ])
            print
            print('Unexpected test result. Differences:')
            print(diff)
            print
            raise RuntimeError(
                'Connection established, but wrong search result.'
                )
        return

    def find(self, entry):
        return self._mref(self._zbmath(entry))

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
                    payload.append(['ti', entry['title']])
                except:
                    continue

            if 'authors' in sc:
                try:
                    authors = entry['author'].split(' and ')
                    last_names = []
                    for author in authors:
                        # Extract everything up to the first comma of `author`
                        # which is hopefully the last name.
                        last_names.append(re.sub('([^,]+),.*', r'\1', author))
                except:
                    continue
                for last_name in last_names:
                    payload.append(['au', last_name])

            if 'year' in sc:
                try:
                    payload.append(['py', entry['year']])
                except:
                    continue

            # Search request.
            # Build the actual payload
            query = ' '.join(
                entry[0] + ':' + entry[1] for entry in payload
                )

            # For debugging, you can plug the `query` into the web interface at
            # <https://zbmath.org/>.

            r = requests.get(url, params={'q': query})
            if not r.ok:
                raise RuntimeError(
                    'Could not fetch data (status code %d).' % r.status_code
                    )

            # Check how many documents we've found.
            m = re.search('Found ([0-9]+) documents', r.content)
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
        m = re.search('Your query produced no results', r.content)
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
                data['authors'].append(author_tag.contents[0])

            title_tags = \
                articles[0].find_all('div', {'class': 'title'})
            data['title'] = title_tags[0].contents[0]

            source_tags = \
                articles[0].find_all('div', {'class': 'source'})
            data['source'] = source_tags[0].contents[0]

            return data
        elif len(articles) > 1:
            raise RuntimeError(
                'Found more than one article on the page. Strange.'
                )
        else:
            raise RuntimeError('No articles found.')

    def _mref(self, data):
        '''Query AMS's mref with the data from zbmath.
        '''
        # Typical Mref query:
        # http://www.ams.org/mathscinet-mref?ref=liesen&dataType=bibtex
        #
        url = 'http://www.ams.org/mathscinet-mref'
        search_query = \
            ' '.join(data['authors'] + [data['title']] + [data['source']])
        r = requests.get(url, params={
            'dataType': 'bibtex',
            'ref': search_query
            })

        if not r.ok:
            raise RuntimeError(
                'Could not fetch data from mref (status code %d).' %
                r.status_code
                )

        soup = BeautifulSoup(r.content, 'lxml')
        bibtex = soup.find_all('pre')
        if len(bibtex) == 0:
            raise RuntimeError('Article not found on mref.')
        elif len(bibtex) > 1:
            raise RuntimeError('Unexpected mref return data.')

        return bibtex[0].contents[0]
