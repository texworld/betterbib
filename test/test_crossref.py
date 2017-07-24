# -*- coding: utf-8 -*-
#
import betterbib

import pybtex
import pybtex.database


def test_crossref_article0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'article',
        fields={
            'title': 'Framework Deflation Krylov Augmented'
            },
        persons={'author': [
            pybtex.database.Person('Liesen'),
            pybtex.database.Person('Gaul'),
            pybtex.database.Person('Nabben'),
            ]}
        )

    bt = source.find_unique(test_entry)
    reference = pybtex.database.Entry(
        'article',
        fields={
            'doi': u'10.1137/110820713',
            'issn': u'0895-4798, 1095-7162',
            'publisher':
                u'Society for Industrial & Applied Mathematics (SIAM)',
            'title': u'A Framework for Deflated and Augmented ' +
                     'Krylov Subspace Methods',
            'url': u'http://dx.doi.org/10.1137/110820713',
            'journal': u'SIAM Journal on Matrix Analysis and Applications',
            'number': u'2',
            'month': 1,
            'volume': u'34',
            'source': u'Crossref',
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

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


# This test is unreliable.
# def test_crossref_article1():
#     '''This entry has two very close matches.
#     '''
#     source = betterbib.Crossref()
#
#     test_entry = pybtex.database.Entry(
#         'article',
#         fields={
#             'title': 'A significance test for the lasso',
#             'doi': '10.1214/13-AOS1175'
#             },
#         persons={'author': [
#             pybtex.database.Person('Tibshirani')
#             ]}
#         )
#
#     import pytest
#     with pytest.raises(RuntimeError):
#         # No unique match found!
#         source.find_unique(test_entry)
#
#     return


def test_crossref_book0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'book',
        fields={
            'title': 'Numerical Ordinary Differential Equations',
            'doi': '10.1002/0470868279',
        },
        persons={'author': [
            pybtex.database.Person('Butcher'),
            ]}
        )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'book',
        fields={
            'doi': u'10.1002/0470868279',
            'publisher': u'John Wiley & Sons, Ltd',
            'title': u'Numerical Methods for Ordinary Differential Equations',
            'url': u'http://dx.doi.org/10.1002/0470868279',
            'month': 6,
            'source': u'Crossref',
            'year': 2003,
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Butcher, J.C.'),
                ]
            }))

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_crossref_book1():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'book',
        fields={
            'title': 'Matrices, Moments and Quadrature with Applications',
        },
        persons={'author': [
            pybtex.database.Person('Golub'),
            pybtex.database.Person('Meurant'),
            ]}
        )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'book',
        fields={
            'title': u'Matrices, Moments and Quadrature with Applications',
            'source': u'Crossref',
            'publisher': u'Princeton University Press',
            'year': 2009,
            'month': 1,
            'doi': '10.1515/9781400833887',
            'url': u'http://dx.doi.org/10.1515/9781400833887',
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Golub, Gene H.'),
                pybtex.database.Person(u'Meurant, G\xe9rard'),
                ]
            }))

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_crossref_inbook0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'inbook',
        fields={
            'title': 'Differential and Difference Equations Ordinary'
            },
        persons={'author': [
            pybtex.database.Person('Butcher'),
            ]}
        )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'inbook',
        fields={
            'doi': u'10.1002/0470868279.ch1',
            'publisher': u'John Wiley & Sons, Ltd',
            'chapter': u'Differential and Difference Equations',
            'url': u'http://dx.doi.org/10.1002/0470868279.ch1',
            'booktitle': u'Numerical Methods ' +
                         'for Ordinary Differential Equations',
            'month': 1,
            'source': u'Crossref',
            'year': 2005,
            'pages': '1-44'
            }
        )

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_crossref_incollection0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'incollection',
        fields={
            'title': 'Numerical continuation, ' +
                     'and computation of normal forms'
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Beyn'),
                pybtex.database.Person(u'Champneys'),
                ]
            }))

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'incollection',
        fields={
            'publisher': 'Elsevier',
            'doi': u'10.1016/s1874-575x(02)80025-x',
            'issn': u'1874-575X',
            'title': 'Numerical Continuation, and Computation of Normal Forms',
            'url': u'http://dx.doi.org/10.1016/s1874-575x(02)80025-x',
            'booktitle': 'Handbook of Dynamical Systems',
            'source': u'Crossref',
            'year': 2002,
            'pages': u'149-219'
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Beyn, Wolf-J\xfcrgen'),
                pybtex.database.Person(u'Champneys, Alan'),
                pybtex.database.Person(u'Doedel, Eusebius'),
                pybtex.database.Person(u'Govaerts, Willy'),
                pybtex.database.Person(u'Kuznetsov, Yuri A.'),
                pybtex.database.Person(u'Sandstede, Bj\xf6rn')
                ]})
        )

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_crossref_techreport0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'techreport',
        fields={
            'title': 'CT Scan of NASA Booster Nozzle'
            }
        )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'techreport',
        fields={
            'doi': u'10.2172/15014765',
            'title': 'CT Scan of NASA Booster Nozzle',
            'url': u'http://dx.doi.org/10.2172/15014765',
            'month': 7,
            'source': u'Crossref',
            'year': 2004,
            'institution': 'Office of Scientific ' +
                           'and Technical Information  (OSTI)'
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Schneberk, D'),
                pybtex.database.Person(u'Perry, R'),
                pybtex.database.Person(u'Thompson, R'),
                ]})
        )

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_crossref_inproceedings0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'inproceedings',
        fields={
            'title': 'Global Warming is Unequivocal'
            }
        )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'inproceedings',
        fields={
            'publisher': 'IEEE',
            'doi': u'10.1109/aero.2008.4526230',
            'issn': u'1095-323X',
            'title': 'Global Warming is Unequivocal',
            'url': u'http://dx.doi.org/10.1109/aero.2008.4526230',
            'booktitle': '2008 IEEE Aerospace Conference',
            'month': 3,
            'source': u'Crossref',
            'year': 2008,
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Trenberth, Kevin E.'),
                ]})
        )

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_crossref_proceedings0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'proceedings',
        fields={
            'title': 'International Scientific Conference',
            'doi': '10.15611/amse.2014.17'
            }
        )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'proceedings',
        fields={
            'publisher': u'Wydawnictwo Uniwersytetu Ekonomicznego ' +
                         u'we Wrocławiu',
            'doi': u'10.15611/amse.2014.17',
            'title': 'International Scientific Conference',
            'url': u'http://dx.doi.org/10.15611/amse.2014.17',
            'source': u'Crossref',
            'year': 2014,
            }
        )

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_doi_only():
    source = betterbib.Crossref()

    bt = source.get_by_doi(u'10.1137/110820713')
    reference = pybtex.database.Entry(
        'article',
        fields={
            'doi': u'10.1137/110820713',
            'issn': u'0895-4798, 1095-7162',
            'publisher':
                u'Society for Industrial & Applied Mathematics (SIAM)',
            'title': u'A Framework for Deflated and Augmented ' +
                     'Krylov Subspace Methods',
            'url': u'http://dx.doi.org/10.1137/110820713',
            'journal': u'SIAM Journal on Matrix Analysis and Applications',
            'number': u'2',
            'month': 1,
            'volume': u'34',
            'source': u'Crossref',
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

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


if __name__ == '__main__':
    test_doi_only()
