import pybtex
import pybtex.database

import betterbib


def test_article0():

    source = betterbib.Dblp()

    test_entry = pybtex.database.Entry(
        "article",
        fields={"title": "Framework Deflated Krylov Augmented"},
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
            "doi": u"10.1137/110820713",
            "title": u"A Framework for Deflated and Augmented "
            + "Krylov Subspace Methods.",
            "url": u"https://doi.org/10.1137/110820713",
            "journal": u"SIAM J. Matrix Analysis Applications",
            "number": u"2",
            "volume": u"34",
            "source": u"DBLP",
            "year": 2013,
            "pages": u"495-518",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person(u"Gaul, Andr\xe9"),
                    pybtex.database.Person(u"Gutknecht, Martin H."),
                    pybtex.database.Person(u"Liesen, J\xf6rg"),
                    pybtex.database.Person(u"Nabben, Reinhard"),
                ]
            }
        ),
    )

    assert betterbib.pybtex_to_bibtex_string(
        bt, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)

    return


if __name__ == "__main__":
    test_article0()
