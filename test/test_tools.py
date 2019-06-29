# -*- coding: utf-8 -*-
#
import pybtex
import pybtex.database

import betterbib


def test_update():
    entry1 = pybtex.database.Entry(
        "article",
        fields={"title": "Yes", "year": 2000},
        persons={"author": [pybtex.database.Person("Doe, John")]},
    )
    entry2 = pybtex.database.Entry(
        "book",
        fields={"title": "No", "pages": "1-19"},
        persons={"author": [pybtex.database.Person("Doe, John")]},
    )
    reference = pybtex.database.Entry(
        "book",
        fields={"title": "No", "year": 2000, "pages": "1-19"},
        persons={"author": [pybtex.database.Person("Doe, John")]},
    )

    merged = betterbib.update(entry1, entry2)

    assert betterbib.pybtex_to_bibtex_string(
        merged, "key", sort=True
    ) == betterbib.pybtex_to_bibtex_string(reference, "key", sort=True)

    return


def test_journal_name():
    shrt = pybtex.database.Entry(
        "article", fields={"journal": u"SIAM J. Matrix Anal. Appl."}
    )
    lng = pybtex.database.Entry(
        "article",
        fields={"journal": u"SIAM Journal on Matrix Analysis and Applications"},
    )

    tmp = betterbib.journal_abbrev({"key": lng})
    assert tmp["key"].fields["journal"] == shrt.fields["journal"]

    lng = pybtex.database.Entry(
        "article",
        fields={"journal": u"SIAM Journal on Matrix Analysis and Applications"},
    )
    tmp = betterbib.journal_abbrev({"key": shrt}, long_journal_names=True)
    assert tmp["key"].fields["journal"] == lng.fields["journal"]
    return


def test_month_range():
    assert betterbib.translate_month("June-July") == 'jun # "-" # jul'
    return


def test_decode():
    url = "https://www.wolframalpha.com/input/?i=integrate+from+0+to+2pi+(cos(x)+e%5E(i+*+(m+-+n)+*+x))"
    d = {
        "wolframalphai1": pybtex.database.Entry(
            "misc", fields=[("url", url), ("note", "Online; accessed 19-February-2019")]
        )
    }
    out = betterbib.decode(d)
    assert out["wolframalphai1"].fields["url"] == url
    return


def test_decode_doi():
    doi = "10.1007/978-1-4615-7419-4_6"
    d = {
        "karwowski": pybtex.database.Entry(
            "misc", fields=[("doi", doi), ("note", "Online; accessed 19-February-2019")]
        )
    }
    out = betterbib.decode(d)
    assert out["karwowski"].fields["doi"] == doi
    return
