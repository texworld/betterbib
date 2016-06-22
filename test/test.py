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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    # assert(bt == reference)
    assert(bt.persons == reference.persons)
    for key, value in bt.fields.iteritems():
        assert(key in reference.fields)
        assert(value == reference.fields[key])

    return


if __name__ == '__main__':
    test_crossref()
