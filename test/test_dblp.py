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
            "doi": "10.1137/110820713",
            "title": "A Framework for Deflated and Augmented "
            + "Krylov Subspace Methods.",
            "url": "https://doi.org/10.1137/110820713",
            "journal": "SIAM J. Matrix Analysis Applications",
            "number": "2",
            "volume": "34",
            "source": "DBLP",
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

    return


if __name__ == "__main__":
    test_article0()
