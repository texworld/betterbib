import pytest
from pybtex.database import Entry, Person

import betterbib


@pytest.mark.parametrize(
    "ref_entry,ref_str",
    [
        (
            Entry(
                "article",
                fields={
                    "doi": "foobar",
                    "url": "https://doi.org/foobar",
                },
            ),
            [
                "@article{foobar,",
                " doi = {foobar},",
                " url = {https://doi.org/foobar},",
                "}",
            ],
        ),
        # escape ampersand:
        (
            Entry("article", fields={"title": "Foo \\& Bar"}),
            ["@article{foobar,", " title = {Foo \\& Bar},", "}"],
        ),
        # escape command:
        (
            Entry("article", fields={"title": "Foo on \\LaTeX"}),
            ["@article{foobar,", " title = {Foo on \\LaTeX},", "}"],
        ),
        # more empty space
        (
            Entry("article", fields={"title": "Foo \\ Bridge"}),
            ["@article{foobar,", " title = {Foo \\ Bridge},", "}"],
        ),
        # encode url
        (
            Entry(
                "misc",
                fields={
                    "url": "https://www.wolframalpha.com/input/?i=integrate+from+0+to+2pi+(cos(x)+e%5E(i+*+(m+-+n)+*+x))",
                    "note": "Online; accessed 19-February-2019",
                },
            ),
            [
                "@misc{foobar,",
                " url = {https://www.wolframalpha.com/input/?i=integrate+from+0+to+2pi+(cos(x)+e%5E(i+*+(m+-+n)+*+x))},",
                " note = {Online; accessed 19-February-2019},",
                "}",
            ],
        ),
        (
            Entry(
                "misc",
                fields={"doi": "10.1007/978-1-4615-7419-4_6"},
            ),
            [
                "@misc{foobar,",
                " doi = {10.1007/978-1-4615-7419-4_6},",
                "}",
            ],
        ),
        (
            Entry(
                "misc",
                persons={"author": [Person("Doe, J. J.")]},
            ),
            [
                "@misc{foobar,",
                " author = {Doe, J. J.},",
                "}",
            ],
        ),
    ],
)
def test_cli_format(ref_entry, ref_str):
    assert betterbib.pybtex_to_bibtex_string(ref_entry, "foobar") == "\n".join(ref_str)
