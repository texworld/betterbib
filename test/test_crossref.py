# -*- coding: utf-8 -*-
#
import betterbib

import pybtex
import pybtex.database
import pytest


def test_crossref_article0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'article',
        fields={
            'title': 'Framework Deflation Krylov Augmented',
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
            'number': u'2',
            'pages': u'495-518',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1137/110820713',
            'journal': u'SIAM J. Matrix Anal. & Appl.',
            'publisher':
                u'Society for Industrial & Applied Mathematics (SIAM)',
            'title': u'A Framework for Deflated and Augmented ' +
                     'Krylov Subspace Methods',
            'volume': u'34',
            'issn': u'0895-4798, 1095-7162',
            'year': 2013,
            'month': 1,
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

    assert betterbib.tools.get_short_doi(
        betterbib.tools.doi_from_url(bt.fields['url'])
        ) == '10/f44kd7'

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
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1002/0470868279',
            'publisher': u'John Wiley & Sons, Ltd',
            'title': u'Numerical Methods for Ordinary Differential Equations',
            'isbn': '9780470868270, 9780471967583',
            'year': 2003,
            'month': 6,
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
            'doi': '10.1515/9781400833887',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1515/9781400833887',
            'publisher': u'Princeton University Press',
            'title': u'Matrices, Moments and Quadrature with Applications',
            'isbn': '9781400833887',
            'year': 2009,
            'month': 1,
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
            'pages': '1-44',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1002/0470868279.ch1',
            'booktitle': u'Numerical Methods ' +
                         'for Ordinary Differential Equations',
            'publisher': u'John Wiley & Sons, Ltd',
            'chapter': u'Differential and Difference Equations',
            'isbn': '9780470868270, 9780471967583',
            'year': 2005,
            'month': 1,
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
            'doi': u'10.1016/s1874-575x(02)80025-x',
            'pages': u'149-219',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1016/s1874-575x(02)80025-x',
            'booktitle': 'Handbook of Dynamical Systems',
            'publisher': 'Elsevier',
            'title': 'Numerical Continuation, and Computation of Normal Forms',
            'issn': u'1874-575X',
            'isbn': u'9780444501684',
            'year': 2002,
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
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.2172/15014765',
            'institution': 'Office of Scientific ' +
                           'and Technical Information  (OSTI)',
            'title': 'CT Scan of NASA Booster Nozzle',
            'year': 2004,
            'month': 7,
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
            'doi': u'10.1109/aero.2008.4526230',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1109/aero.2008.4526230',
            'booktitle': '2008 IEEE Aerospace Conference',
            'publisher': 'IEEE',
            'title': 'Global Warming is Unequivocal',
            'issn': u'1095-323X',
            'isbn': u'9781424414871, 9781424414888',
            'year': 2008,
            'month': 3,
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
            'doi': u'10.15611/amse.2014.17',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.15611/amse.2014.17',
            'publisher': u'Wydawnictwo Uniwersytetu Ekonomicznego ' +
                         u'we Wrocławiu',
            'title': 'International Scientific Conference',
            'year': 2014,
            }
        )

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_doi_only():
    source = betterbib.Crossref(prefer_long_journal_name=True)

    bt = source.get_by_doi(u'10.1137/110820713')
    reference = pybtex.database.Entry(
        'article',
        fields={
            'doi': u'10.1137/110820713',
            'number': u'2',
            'pages': u'495-518',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1137/110820713',
            'journal': u'SIAM Journal on Matrix Analysis and Applications',
            'publisher':
                u'Society for Industrial & Applied Mathematics (SIAM)',
            'title': u'A Framework for Deflated and Augmented ' +
                     'Krylov Subspace Methods',
            'volume': u'34',
            'issn': u'0895-4798, 1095-7162',
            'year': 2013,
            'month': 1,
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


def test_standard():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'misc',
        fields={
            'title': (
                '{STD 42}: {A} Standard for the transmission of {IP} '
                'datagrams over experimental {Ethernet} Networks'
                ),
            'doi': '10.5594/s9781614827788',
            },
        )

    reference = pybtex.database.Entry(
        'misc',
        fields={
            'doi': u'10.5594/s9781614827788',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.5594/s9781614827788',
            'publisher': (
                'The Society of Motion Picture '
                'and Television Engineers'
                ),
            'title': (
                '{ST} 2022-7:2013 : {Seamless} Protection Switching '
                'of {SMPTE} {ST} 2022 {IP} Datagrams'
                ),
            'isbn': '9781614827788',
            }
        )

    bt = source.find_unique(test_entry)

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


def test_crossref_no_title():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        'article',
        fields={
            # 'title': 'Stratified atmospheric boundary layers',
            'journal': 'Boundary-Layer Meteorology',
            'pages': '375--396',
            },
        persons={'author': [
            pybtex.database.Person('Mahrt'),
            ]}
        )

    # Make sure and exception is thrown when not finding a unique match
    with pytest.raises(betterbib.errors.UniqueError):
        source.find_unique(test_entry)

    return


def test_crossref_all_capitals():
    source = betterbib.Crossref()

    bt = source.get_by_doi(u'10.1142/s0218213009000366')
    reference = pybtex.database.Entry(
        'article',
        fields={
            'doi': u'10.1142/s0218213009000366',
            'number': u'05',
            'pages': u'697-716',
            'source': u'Crossref',
            'url': u'http://dx.doi.org/10.1142/s0218213009000366',
            'journal': u'Int. J. Artif. Intell. Tools',
            'publisher': u'World Scientific Pub Co Pte Lt',
            'title': u'Ontological Cognitive Map',
            'volume': u'18',
            'issn': u'0218-2130, 1793-6349',
            'year': 2009,
            'month': 10,
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'CHAUVIN, LIONEL'),
                pybtex.database.Person(u'GENEST, DAVID'),
                pybtex.database.Person(u'LOISEAU, STÉPHANE'),
                ]
            }))

    assert betterbib.pybtex_to_bibtex_string(bt, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return


if __name__ == '__main__':
    test_crossref_all_capitals()
