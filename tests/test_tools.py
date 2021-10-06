from pathlib import Path

import pybtex
import pybtex.database
import pytest

import betterbib
from betterbib.cli._doi_to_bibtex import _create_citekey_for_entry

this_dir = Path(__file__).resolve().parent
data_file_exists = Path(this_dir / "../src/betterbib/data/journals.json").is_file()


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


@pytest.mark.skipif(not data_file_exists, reason="Data file missing")
def test_journal_name():
    shrt = pybtex.database.Entry(
        "article", fields={"journal": "SIAM J. Matrix Anal. Appl."}
    )
    lng = pybtex.database.Entry(
        "article",
        fields={"journal": "SIAM Journal on Matrix Analysis and Applications"},
    )

    tmp = betterbib.journal_abbrev({"key": lng})
    assert tmp["key"].fields["journal"] == shrt.fields["journal"]

    lng = pybtex.database.Entry(
        "article",
        fields={"journal": "SIAM Journal on Matrix Analysis and Applications"},
    )
    tmp = betterbib.journal_abbrev({"key": shrt}, long_journal_names=True)
    assert tmp["key"].fields["journal"] == lng.fields["journal"]


def test_month_range():
    assert betterbib.translate_month("June-July") == 'jun # "-" # jul'


def test_decode():
    url = "https://www.wolframalpha.com/input/?i=integrate+from+0+to+2pi+(cos(x)+e%5E(i+*+(m+-+n)+*+x))"
    entry = pybtex.database.Entry(
        "misc",
        fields=[("url", url), ("note", "Online; accessed 19-February-2019")],
    )
    out = betterbib.decode(entry)
    assert out.fields["url"] == url


def test_decode_doi():
    doi = "10.1007/978-1-4615-7419-4_6"
    d = pybtex.database.Entry(
        "misc",
        fields=[("doi", doi), ("note", "Online; accessed 19-February-2019")],
    )
    out = betterbib.decode(d)
    assert out.fields["doi"] == doi


def test_encode_url():
    url = "https://www.wolframalpha.com/input/?i=integrate+from+0+to+2pi+(cos(x)+e%5E(i+*+(m+-+n)+*+x))"
    d = {
        "wolframalphai1": pybtex.database.Entry(
            "misc",
            fields=[
                ("url", url),
                ("note", "Online; accessed 19-February-2019"),
            ],
        )
    }

    out = betterbib.pybtex_to_bibtex_string(d["wolframalphai1"], "wolframalphai1")

    # Split string and fetch entry with url
    url_entry = out.split()[3]
    # Remove braces and trailing comma
    url_entry = url_entry[1:-2]
    assert url_entry == url


def test_encode_doi():
    doi = "10.1007/978-1-4615-7419-4_6"
    d = {
        "karwowski": pybtex.database.Entry(
            "misc",
            fields=[
                ("doi", doi),
                ("note", "Online; accessed 19-February-2019"),
            ],
        )
    }
    out = betterbib.pybtex_to_bibtex_string(d["karwowski"], "karwowski")

    # Split string and fetch entry with doi
    doi_entry = out.split()[3]
    # Remove braces and trailing comma
    doi_entry = doi_entry[1:-2]
    assert doi_entry == doi


def test_first_name_space():
    d = {
        "doe": pybtex.database.Entry(
            "misc",
            persons={"author": [pybtex.database.Person("Doe, J. J.")]},
        )
    }
    out = betterbib.pybtex_to_bibtex_string(d["doe"], "doe")
    ref = """@misc{doe,
 author = {Doe, J. J.},
}"""

    assert out == ref


def test_create_citekey():
    entry = pybtex.database.Entry(
        "article",
        fields={
            "year": 2021,
            "title": "A fancy algorithm for generating citekeys",
        },
        persons=pybtex.database.OrderedCaseInsensitiveDict(
            {
                "author": [
                    pybtex.database.Person("Schlömer, Nico"),
                    pybtex.database.Person("Iovene, Valentin"),
                ]
            }
        ),
    )
    citekey = _create_citekey_for_entry(entry)
    assert citekey == "schlomer2021"
