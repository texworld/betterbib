import pybtex
import pybtex.database
import pytest

import betterbib


def test_crossref_article0():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "article",
        fields={"title": "Framework Deflation Krylov Augmented"},
        persons={
            "author": [
                pybtex.database.Person("Liesen"),
                pybtex.database.Person("Gaul"),
                pybtex.database.Person("Nabben"),
            ]
        },
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "article",
        fields={
            "doi": "10.1137/110820713",
            "issn": "0895-4798, 1095-7162",
            "publisher": "Society for Industrial & Applied Mathematics (SIAM)",
            "title": "A Framework for Deflated and Augmented "
            + "Krylov Subspace Methods",
            "url": "http://dx.doi.org/10.1137/110820713",
            "journal": "SIAM J. Matrix Anal. & Appl.",
            "number": "2",
            "month": 1,
            "volume": "34",
            "source": "Crossref",
            "year": 2013,
            "pages": "495-518",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Gaul, Andr\xe9"),
                    pybtex.database.Person("Gutknecht, Martin H."),
                    pybtex.database.Person("Liesen, J\xf6rg"),
                    pybtex.database.Person("Nabben, Reinhard"),
                ]
            }
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)

    assert (
        betterbib.tools.get_short_doi(betterbib.tools.doi_from_url(bt.fields["url"]))
        == "10/f44kd7"
    )


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


def test_crossref_book0():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "book",
        fields={
            "title": "Numerical Ordinary Differential Equations",
            "doi": "10.1002/0470868279",
        },
        persons={"author": [pybtex.database.Person("Butcher")]},
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "book",
        fields={
            "doi": "10.1002/0470868279",
            "publisher": "John Wiley & Sons, Ltd",
            "title": "Numerical Methods for Ordinary Differential Equations",
            "subtitle": "Butcher/Numerical Methods",
            "url": "http://dx.doi.org/10.1002/0470868279",
            "month": 6,
            "source": "Crossref",
            "year": 2003,
            "isbn": "9780470868270, 9780471967583",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {"author": [pybtex.database.Person("Butcher, J.C.")]}
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_crossref_book1():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "book",
        fields={"title": "Matrices, Moments and Quadrature with Applications"},
        persons={
            "author": [
                pybtex.database.Person("Golub"),
                pybtex.database.Person("Meurant"),
            ]
        },
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "book",
        fields={
            "title": "Matrices, Moments and Quadrature with Applications",
            "source": "Crossref",
            "publisher": "Princeton University Press",
            "year": 2009,
            "month": 12,
            "doi": "10.1515/9781400833887",
            "url": "http://dx.doi.org/10.1515/9781400833887",
            "isbn": "9781400833887",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Golub, Gene H."),
                    pybtex.database.Person("Meurant, G\xe9rard"),
                ]
            }
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_crossref_inbook0():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "inbook",
        fields={"title": "Differential and Difference Equations Ordinary"},
        persons={"author": [pybtex.database.Person("Butcher")]},
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "inbook",
        fields={
            "doi": "10.1002/0470868279.ch1",
            "publisher": "John Wiley & Sons, Ltd",
            "chapter": "Differential and Difference Equations",
            "url": "http://dx.doi.org/10.1002/0470868279.ch1",
            "booktitle": "Numerical Methods " + "for Ordinary Differential Equations",
            "month": 1,
            "source": "Crossref",
            "year": 2005,
            "pages": "1-44",
            "isbn": "9780470868270, 9780471967583",
        },
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_crossref_incollection0():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "incollection",
        fields={
            "title": "Numerical continuation, " + "and computation of normal forms"
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Beyn"),
                    pybtex.database.Person("Champneys"),
                ]
            }
        ),
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "incollection",
        fields={
            "publisher": "Elsevier",
            "doi": "10.1016/s1874-575x(02)80025-x",
            "issn": "1874-575X",
            "title": "Numerical Continuation, and Computation of Normal Forms",
            "url": "http://dx.doi.org/10.1016/s1874-575x(02)80025-x",
            "booktitle": "Handbook of Dynamical Systems",
            "source": "Crossref",
            "year": 2002,
            "pages": "149-219",
            "isbn": "9780444501684",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Beyn, Wolf-J\xfcrgen"),
                    pybtex.database.Person("Champneys, Alan"),
                    pybtex.database.Person("Doedel, Eusebius"),
                    pybtex.database.Person("Govaerts, Willy"),
                    pybtex.database.Person("Kuznetsov, Yuri A."),
                    pybtex.database.Person("Sandstede, Bj\xf6rn"),
                ]
            }
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_crossref_techreport0():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "techreport", fields={"title": "CT Scan of NASA Booster Nozzle"}
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "techreport",
        fields={
            "doi": "10.2172/15014765",
            "title": "CT Scan of NASA Booster Nozzle",
            "url": "http://dx.doi.org/10.2172/15014765",
            "month": 7,
            "source": "Crossref",
            "year": 2004,
            "institution": "Office of Scientific and Technical Information (OSTI)",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Schneberk, D"),
                    pybtex.database.Person("Perry, R"),
                    pybtex.database.Person("Thompson, R"),
                ]
            }
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_crossref_inproceedings0():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "inproceedings", fields={"title": "Global Warming is Unequivocal"}
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "inproceedings",
        fields={
            "publisher": "IEEE",
            "doi": "10.1109/aero.2008.4526230",
            "isbn": "9781424414871, 9781424414888",
            "issn": "1095-323X",
            "title": "Global Warming is Unequivocal",
            "url": "http://dx.doi.org/10.1109/aero.2008.4526230",
            "booktitle": "2008 IEEE Aerospace Conference",
            "month": 3,
            "source": "Crossref",
            "year": 2008,
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {"author": [pybtex.database.Person("Trenberth, Kevin E.")]}
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_crossref_proceedings0():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "proceedings",
        fields={
            "title": "International Scientific Conference",
            "doi": "10.15611/amse.2014.17",
        },
    )

    bt = source.find_unique(test_entry)

    reference = pybtex.database.Entry(
        "proceedings",
        fields={
            "publisher": "Wydawnictwo Uniwersytetu Ekonomicznego " + "we Wrocławiu",
            "doi": "10.15611/amse.2014.17",
            "title": "International Scientific Conference",
            "url": "http://dx.doi.org/10.15611/amse.2014.17",
            "source": "Crossref",
            "year": 2014,
        },
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_doi_only():
    source = betterbib.Crossref(prefer_long_journal_name=True)

    bt = source.get_by_doi("10.1137/110820713")
    reference = pybtex.database.Entry(
        "article",
        fields={
            "doi": "10.1137/110820713",
            "issn": "0895-4798, 1095-7162",
            "publisher": "Society for Industrial & Applied Mathematics (SIAM)",
            "title": "A Framework for Deflated and Augmented "
            + "Krylov Subspace Methods",
            "url": "http://dx.doi.org/10.1137/110820713",
            "journal": "SIAM Journal on Matrix Analysis and Applications",
            "number": "2",
            "month": 1,
            "volume": "34",
            "source": "Crossref",
            "year": 2013,
            "pages": "495-518",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Gaul, Andr\xe9"),
                    pybtex.database.Person("Gutknecht, Martin H."),
                    pybtex.database.Person("Liesen, J\xf6rg"),
                    pybtex.database.Person("Nabben, Reinhard"),
                ]
            }
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_crossref_no_title():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "article",
        fields={
            # 'title': 'Stratified atmospheric boundary layers',
            "journal": "Boundary-Layer Meteorology",
            "pages": "375--396",
        },
        persons={"author": [pybtex.database.Person("Mahrt")]},
    )

    # Make sure and exception is thrown when not finding a unique match
    with pytest.raises(betterbib.errors.UniqueError):
        source.find_unique(test_entry)


def test_crossref_all_capitals():
    source = betterbib.Crossref()

    bt = source.get_by_doi("10.1142/s0218213009000366")
    reference = pybtex.database.Entry(
        "article",
        fields={
            "doi": "10.1142/s0218213009000366",
            "issn": "0218-2130, 1793-6349",
            "publisher": "World Scientific Pub Co Pte Lt",
            "title": "ONTOLOGICAL COGNITIVE MAP",
            "url": "http://dx.doi.org/10.1142/s0218213009000366",
            "journal": "Int. J. Artif. Intell. Tools",
            "number": "05",
            "month": 10,
            "volume": "18",
            "source": "Crossref",
            "year": 2009,
            "pages": "697-716",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("CHAUVIN, LIONEL"),
                    pybtex.database.Person("GENEST, DAVID"),
                    pybtex.database.Person("LOISEAU, STÉPHANE"),
                ]
            }
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


def test_subtitle():
    source = betterbib.Crossref()

    test_entry = pybtex.database.Entry(
        "article",
        fields={
            "title": "tube",
            "doi": "10.1145/2377677.2377723",
            "journal": "ACM SIGCOMM Computer Communication Review",
            "issn": "0146-4833",
        },
        persons={
            "author": [
                pybtex.database.Person("Ha, Sangtae"),
                pybtex.database.Person("Sen"),
                pybtex.database.Person("Joe-Wong"),
                pybtex.database.Person("Im"),
                pybtex.database.Person("Chiang, Mung"),
            ]
        },
    )

    reference = pybtex.database.Entry(
        "article",
        fields={
            "publisher": "Association for Computing Machinery (ACM)",
            "doi": "10.1145/2377677.2377723",
            "title": "TUBE",
            "subtitle": "time-dependent pricing for mobile data",
            "url": "http://dx.doi.org/10.1145/2377677.2377723",
            "journal": "SIGCOMM Comput. Commun. Rev.",
            "issn": "0146-4833",
            "number": "4",
            "month": 9,
            "volume": "42",
            "source": "Crossref",
            "year": 2012,
            "pages": "247-258",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Ha, Sangtae"),
                    pybtex.database.Person("Sen, Soumya"),
                    pybtex.database.Person("Joe-Wong, Carlee"),
                    pybtex.database.Person("Im, Youngbin"),
                    pybtex.database.Person("Chiang, Mung"),
                ]
            }
        ),
    )

    bt = source.find_unique(test_entry)
    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)


if __name__ == "__main__":
    test_subtitle()
