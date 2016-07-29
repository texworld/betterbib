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
    reference_str = u'''@article{ABC,
  author = {Gaul, Andr\xe9 and Gutknecht, Martin H. and Liesen, J\xf6rg and Nabben, Reinhard},
  journal = {SIAM. J. Matrix Anal. & Appl.},
  number = {2},
  month = may,
  volume = {34},
  year = {2013},
  pages = {495-518},
  publisher = {Society for Industrial & Applied Mathematics (SIAM)},
  doi = {10.1137/110820713},
  title = {A Framework for Deflated and Augmented Krylov Subspace Methods},
  url = {http://dx.doi.org/10.1137/110820713},
  source = {CrossRef}
}'''

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    # assert(bt == reference)
    assert(bt.persons == reference.persons)
    for key, value in bt.fields.iteritems():
        assert(key in reference.fields)
        assert(value == reference.fields[key])

    string = betterbib.pybtex_to_bibtex_string(reference, 'ABC')
    assert string == reference_str

    return


if __name__ == '__main__':
    test_crossref()
