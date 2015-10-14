# -*- coding: utf8 -*-
#
from betterbib.connector import Connector

import difflib
import time
import re
import requests
import sys


class MathSciNet(Connector):
    '''
    BibTeX resource from MathSciNet, http://www.ams.org/mathscinet/.
    Unfortunately, access to MathSciNet is restricted and typically only
    accessible from university campuses.
    '''
    def __init__(self):
        servers = ['http://www.ams.org/mathscinet/',
                   'http://ams.rice.edu/mathscinet/',
                   'http://ams.impa.br/mathscinet/',
                   'http://ams.math.uni-bielefeld.de/mathscinet/',
                   'http://ams.mpim-bonn.mpg.de/mathscinet/',
                   'http://ams.u-strasbg.fr/mathscinet/'
                   ]

        self.server = servers[0]

        sys.stdout.write('Checking connection with %s... ' % self.server)
        try:
            t = time.time()
            self._test_connection()
            elapsed = time.time() - t
            sys.stdout.write('ok (%gs).\n\n' % elapsed)
        except:
            sys.stdout.write('failed.\n\n')
            message = ('Unable to establish connection with %s. '
                       'Make sure that you have access to the site and that '
                       'the search function returns valid results.\n\n') \
                % self.server
            sys.stdout.write(message)
            raise
        return

    def _test_connection(self):
        '''Test the connection with MathSkyNet. ;)
        '''
        test_entry = {'title': 'Krylov subspace methods',
                      'author': 'Liesen and Strakoš'
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
            print(diff)
            print
            raise RuntimeError(
                'Connection established, but wrong search result.'
                )
        return

    def find(self, entry):
        url = self.server + '/search/publications.html'

        # Typical search query line:
        # http://www.ams.org/MathSciNet/search/publications.html?pg4=AUCN&s4=&co4=AND&pg5=TI&s5=ggg&co5=AND&pg6=PC&s6=&co6=AND&pg7=ALLF&s7=&co7=AND&Submit=Search&dr=all&yrop=eq&arg3=&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=html
        #
        # Specify the search criteria.
        # The loop below will first search for title only, then title and
        # author, and so forth, until a unique match is found.
        #
        search_criteria = ['title', 'author', 'year', 'journal']
        success = False
        # default (empty) payload
        payload = {'pg4': 'AUCN', 's4': '', 'co4': 'AND',
                   'pg5': 'TI',   's5': '', 'co5': 'AND',
                   'pg6': 'PC',   's6': '', 'co6': 'AND',
                   'pg7': 'ALLF', 's7': '', 'co7': 'AND',
                   'Submit': 'Search',
                   'dr': 'all',
                   'yrop': 'eq',
                   'arg3': '',
                   'yearRangeFirst': '',
                   'yearRangeSecond': '',
                   'pg8': 'ET',
                   's8': 'All',
                   'review_format': 'html',
                   'fmt': 'bibtex'  # immediately jump to BibTeX
                   }
        for sc in search_criteria:
            # Add a search criterion.
            if sc == 'title':
                try:
                    title = entry['title']
                except Exception:
                    continue
                # Remove everything starting from the first dollar sign (math
                # mode). Removing only what is enclosed in the dollar signs
                # does not work with MathSciNet's search mask, unfortunately.
                p = '\$.*'
                title = re.sub(p, '', title)
                # Remove some tokens that make MathSciNet fail.
                title = title.replace('{', '')
                title = title.replace('}', '')
                title = title.replace('(', '')
                title = title.replace(')', '')
                # Replacing some common TeX symbols.
                title = title.replace('\\"a', u'ä')
                title = title.replace('\\"o', u'ö')
                title = title.replace('\\"u', u'ü')
                title = title.replace('\\"A', u'Ä')
                title = title.replace('\\"O', u'Ö')
                title = title.replace('\\"U', u'Ü')
                payload['pg4'] = 'TI'
                payload['s4'] = title
            elif sc == 'author':
                try:
                    authors = entry['author'].split(' and ')
                    last_names = []
                    for author in authors:
                        # Extract everything up to the first comma of `author`
                        # which is hopefully the last name.
                        last_names.append(re.sub('([^,]+),.*', r'\1', author))
                except Exception:
                    continue
                last_names = ' and '.join(last_names)
                payload['pg5'] = 'AUCN'
                payload['s5'] = last_names
            elif sc == 'year':
                payload['dr'] = 'pubyear'
                try:
                    payload['arg3'] = entry['year']
                except Exception:
                    continue
            elif sc == 'journal':
                payload['pg6'] = 'JOUR'
                try:
                    payload['s6'] = entry['journal']
                except Exception:
                    continue
            else:
                ValueError('Illegal search criterion \'%s\'.' % sc)

            # Search request.
            r = requests.get(url, params=payload)
            if not r.ok:
                raise RuntimeError('Could not fetch data (status code %d).'
                                   % r.status_code)

            # Find the BibTeX entry and extract it.
            a = '@[a-zA-Z]+\s*{'
            m = re.findall(a, r.content)
            if len(m) == 1:
                success = True
                break
            elif len(m) == 0:
                # Check if the website issues an error message.
                a = 'No publications results for'
                m = re.search(a, r.content)
                if m:
                    raise RuntimeError('No publication results on MathSciNet.')
                else:
                    raise RuntimeError('Unknown error on MathSciNet.')
            # else len(m) > 1 .. try again with stricter criteria

        if not success:
            raise RuntimeError('Found %d matches with full criteria.' % len(m))

        # Now we know that there is exactly one matching entry in the string.
        # If there's a way to extract the corresponding MatchObject directly
        # from findall, that'd be great. For now, just to another search().
        m = re.search(a, r.content)

        # Find matching closing bracket.
        i0 = m.end()
        num_open_brackets = 1
        i1 = i0
        while num_open_brackets > 0:
            if r.content[i1] == '{':
                num_open_brackets += 1
            elif r.content[i1] == '}':
                num_open_brackets -= 1
            i1 += 1
        bibtex_entry = r.content[m.start():i1]

        return bibtex_entry
