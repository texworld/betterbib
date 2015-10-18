# -*- coding: utf-8 -*-
#
import betterbib

import difflib

def test_connection():

    # We can only test ZentralblettMref since MathSciNet is closed.
    source = betterbib.ZentralblattMref()

    test_entry = {
            'title': 'Krylov subspace methods',
            'author': 'Liesen and Strakoš',
            'year': '2013'
            }

    # Define the expected return string. Note that special characters need
    # to be escaped.
    reference = '''@book {MR3024841,
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

    bt = source.find(test_entry)

    if bt != reference:
        diff = difflib.Differ().compare(bt, reference)
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

    assert(bt == reference)
    return

if __name__ == '__main__':
    test_connection()
