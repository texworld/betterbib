# -*- coding: utf-8 -*-
#
import betterbib

import pybtex
import pybtex.database


def _bibtex_equals(obj0, obj1):
    if obj0.persons != obj1.persons:
        return False

    for key, value in obj0.fields.iteritems():
        if key not in obj1.fields:
            return False
        if value != obj1.fields[key]:
            return False

    return True


def test_crossref_article0():

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
    assert _bibtex_equals(bt, reference)

    # test string conversion
    betterbib.pybtex_to_bibtex_string(reference, 'ABC')
    # No assertions here yet.
    # What we'd like to do: Take the string, parse it back into a PybTeX entry,
    # and make sure it's the original. This doesn't quite work yet since
    # months are transposed from, e.g., 5, to "May" by PybTeX; see
    # <https://bitbucket.org/pybtex-devs/pybtex/issues/84/handling-of-month-year-in-bibtex-entry>.

    return


def test_crossref_article1():
    '''This entry has two very close matches.
    '''

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
            'article',
            fields={
                'title': 'A significance test for the lasso',
                'doi': '10.1214/13-AOS1175'
            },
            persons={'author': [
                pybtex.database.Person('Tibshirani')
                ]}
            )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        'article',
        fields={
            'doi': u'10.1214/13-aos1175',
            'publisher': u'Institute of Mathematical Statistics',
            'title': u'A significance test for the lasso',
            'url': u'http://dx.doi.org/10.1214/13-aos1175',
            'journal': u'Ann. Statist.',
            'number': u'2',
            'month': 4,
            'volume': u'42',
            'source': u'CrossRef',
            'year': 2014,
            'pages': u'413-468'
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Lockhart, Richard'),
                pybtex.database.Person(u'Taylor, Jonathan'),
                pybtex.database.Person(u'Tibshirani, Ryan J.'),
                pybtex.database.Person(u'Tibshirani, Robert'),
                ]
            }))

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _bibtex_equals(bt, reference)

    # test string conversion
    betterbib.pybtex_to_bibtex_string(reference, 'ABC')
    # No assertions here yet.
    # What we'd like to do: Take the string, parse it back into a PybTeX entry,
    # and make sure it's the original. This doesn't quite work yet since
    # months are transposed from, e.g., 5, to "May" by PybTeX; see
    # <https://bitbucket.org/pybtex-devs/pybtex/issues/84/handling-of-month-year-in-bibtex-entry>.

    return


def test_crossref_book0():

    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
            'book',
            fields={
                'title': 'Numerical Ordinary Differential Equations'
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
            'publisher': u'Wiley-Blackwell',
            'title': u'Numerical Methods for Ordinary Differential Equations',
            'url': u'http://dx.doi.org/10.1002/0470868279',
            'month': 6,
            'source': u'CrossRef',
            'year': 2003,
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Butcher, J.C.'),
                ]
            }))

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _bibtex_equals(bt, reference)

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
            'publisher': u'Wiley-Blackwell',
            'chapter': u'Differential and Difference Equations',
            'url': u'http://dx.doi.org/10.1002/0470868279.ch1',
            'booktitle': u'Numerical Methods ' +
                         'for Ordinary Differential Equations',
            'month': 1,
            'source': u'CrossRef',
            'year': 2005,
            'pages': '1-44'
            }
        )

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _bibtex_equals(bt, reference)

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
        'inproceedings',
        fields={
            'publisher': 'Elsevier BV',
            'doi': u'10.1016/s1874-575x(02)80025-x',
            'title': 'Numerical Continuation, and Computation of Normal Forms',
            'url': u'http://dx.doi.org/10.1016/s1874-575x(02)80025-x',
            'booktitle': 'Handbook of Dynamical Systems',
            'source': u'CrossRef',
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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _bibtex_equals(bt, reference)

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
            'source': u'CrossRef',
            'year': 2004,
            'institution': 'Office of Scientific ' +
                           'and Technical Information (OSTI)',
            'pages': '1-44'
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Schneberk, D'),
                pybtex.database.Person(u'Perry, R'),
                pybtex.database.Person(u'Thompson, R'),
                ]})
        )

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _bibtex_equals(bt, reference)

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
            'publisher': 'Institute of Electrical & ' +
                         'Electronics Engineers (IEEE)',
            'doi': u'10.1109/aero.2008.4526230',
            'title': 'Global Warming is Unequivocal',
            'url': u'http://dx.doi.org/10.1109/aero.2008.4526230',
            'booktitle': '2008 IEEE Aerospace Conference',
            'month': 3,
            'source': u'CrossRef',
            'year': 2008,
            },
        persons=pybtex.database.OrderedCaseInsensitiveDict({
            'author': [
                pybtex.database.Person(u'Trenberth, Kevin E.'),
                ]})
        )

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _bibtex_equals(bt, reference)

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
            'publisher': 'Wroclaw University of Economics',
            'doi': u'10.15611/amse.2014.17',
            'title': 'International Scientific Conference',
            'url': u'http://dx.doi.org/10.15611/amse.2014.17',
            'source': u'CrossRef',
            'year': 2014,
            }
        )

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _bibtex_equals(bt, reference)

    return


if __name__ == '__main__':
    test_crossref_article0()
