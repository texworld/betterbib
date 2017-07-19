# -*- coding: utf-8 -*-
#
import betterbib

import pybtex
import pybtex.database


def _serialize_bibtex(obj):
    string = ''''''
    for person_type, persons in obj.persons.iteritems():
        string += person_type + ': '
        string += ', '.join(' '.join(
            p.first_names +
            p.middle_names +
            p.prelast_names +
            p.last_names +
            p.lineage_names
            ) for p in persons)
        string += '.\n'

    sorted_keys = sorted(obj.fields.keys())

    string += '\n'.join(
        '{}: {}'.format(key, obj.fields[key])
        for key in sorted_keys
        )
    return string


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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    # The two tests are almost redundant. The second is more accurate, the
    # first shows errors more clearly.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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
            'journal': u'The Annals of Statistics',
            'number': u'2',
            'month': 4,
            'volume': u'42',
            'source': u'Crossref',
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
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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
            'publisher': 'Elsevier',
            'doi': u'10.1016/s1874-575x(02)80025-x',
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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

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
                         'we Wrocławiu',
            'doi': u'10.15611/amse.2014.17',
            'title': 'International Scientific Conference',
            'url': u'http://dx.doi.org/10.15611/amse.2014.17',
            'source': u'Crossref',
            'year': 2014,
            }
        )

    # Comparing the Entry object as a whole doesn't work, unfortunately.
    assert _serialize_bibtex(bt) == _serialize_bibtex(reference)

    return


if __name__ == '__main__':
    test_crossref_article0()
