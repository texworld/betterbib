# -*- coding: utf-8 -*-
#
import betterbib

import pybtex


def test_crossref():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
            'article',
            fields={
                'title': 'A Framework for Deflated and Augmented ' +
                'Krylov Subspace Methods',
                'year': '2013'
            },
            persons={'author': [
                pybtex.database.Person('Gaul'),
                pybtex.database.Person('Liesen'),
                pybtex.database.Person('Gutknecht'),
                pybtex.database.Person('Nabben'),
                ]}
            )

    bt = source.find_unique(test_entry)
    reference = pybtex.database.Entry(
        'article',
        fields={
            'doi': u'10.1137/110820713',
            'publisher':
                u'Society for Industrial & Applied Mathematics (SIAM)',
            'title': u'A Framework for Deflated and Augmented ' +
                'Krylov Subspace Methods',
            'url': u'http://dx.doi.org/10.1137/110820713',
            'journal': u'SIAM. J. Matrix Anal. & Appl.',
            'number': u'2',
            'month': 5,
            'volume': u'34',
            'source': u'CrossRef',
            'year': 2013,
            'pages': u'495-518'
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Gaul, Andr\xe9'),
                pybtex.database.Person(u'Gutknecht, Martin H.'),
                pybtex.database.Person(u'Liesen, J\xf6rg'),
                pybtex.database.Person(u'Nabben, Reinhard')
                ]
            }))

    assert(bt == reference)
    return


def test_zentralblattmref():

    source = betterbib.ZentralblattMref()

    test_entry = pybtex.database.Entry(
            'article',
            fields={
                'title': 'A Framework for Deflated and Augmented ' +
                'Krylov Subspace Methods',
                'year': '2013'
            },
            persons={'author': [
                pybtex.database.Person('Gaul'),
                pybtex.database.Person('Liesen'),
                pybtex.database.Person('Gutknecht'),
                pybtex.database.Person('Nabben'),
                ]}
            )

    reference = pybtex.database.Entry(
        u'article',
        fields={
            u'TITLE': u'A framework for deflated and augmented {K}rylov '
                      'subspace methods',
            u'JOURNAL': u'SIAM J. Matrix Anal. Appl.',
            u'FJOURNAL': u'SIAM Journal on Matrix Analysis and Applications',
            u'VOLUME': u'34',
            u'YEAR': u'2013',
            u'NUMBER': u'2',
            u'PAGES': u'495--518',
            u'ISSN': u'0895-4798',
            u'MRCLASS': u'65F10',
            u'MRNUMBER': u'3054589',
            u'MRREVIEWER': u'Josef Dan{\\v{e}}k',
            u'DOI': u'10.1137/110820713',
            u'URL': u'http://dx.doi.org/10.1137/110820713'
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            u'AUTHOR': [
                pybtex.database.Person(u'Gaul, Andr{\\\'e}'),
                pybtex.database.Person(u'Gutknecht, Martin H.'),
                pybtex.database.Person(u'Liesen, J{\\"o}rg'),
                pybtex.database.Person(u'Nabben, Reinhard')
                ]
            })
        )

    bt = source.find_unique(test_entry)

    assert(bt == reference)
    return

if __name__ == '__main__':
    test_crossref()
    test_zentralblattmref()
