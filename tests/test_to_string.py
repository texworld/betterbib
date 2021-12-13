import pybtex
import pytest

import betterbib

version_line = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
)


@pytest.mark.parametrize(
    "key,ref_entry,ref_str",
    [
        (
            "foobar",
            pybtex.database.Entry(
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
            "foobar",
            pybtex.database.Entry("article", fields={"title": "Foo \\& Bar"}),
            ["@article{foobar,", " title = {Foo \\& Bar},", "}"],
        ),
        # escape command:
        (
            "foobar",
            pybtex.database.Entry("article", fields={"title": "Foo on \\LaTeX"}),
            ["@article{foobar,", " title = {Foo on \\LaTeX},", "}"],
        ),
        # more escape:
        (
            "foobar",
            pybtex.database.Entry(
                "article", fields={"title": "Foo \\& on \\ @TheBridge"}
            ),
            ["@article{foobar,", " title = {Foo \\& on \\ @TheBridge},", "}"],
        ),
        (
            "foobar",
            pybtex.database.Entry(
                "article", fields={"title": "Foo \\& on \\LaTeX\\ @TheBridge"}
            ),
            ["@article{foobar,", " title = {Foo \\& on \\LaTeX\\ @TheBridge},", "}"],
        ),
        # # Keeping when unformatted
        # (
        #     TEST_BIBTEXT_PREAMBLE_UNFORMATTED,
        #     TEST_BIBTEXT_PREAMBLE_FORMATTED_KEEP,
        # ),
        # # Keeping when preamble and preformatted
        # (
        #     TEST_BIBTEXT_PREAMBLE_FORMATTED_KEEP,
        #     TEST_BIBTEXT_PREAMBLE_FORMATTED_KEEP,
        # ),
        # # Keeping when no preamble and preformatted
        # (
        #     TEST_BIBTEXT_PREAMBLE_FORMATTED_DROP,
        #     TEST_BIBTEXT_PREAMBLE_FORMATTED_DROP,
        # ),
    ],
)
def test_cli_format(key, ref_entry, ref_str):
    assert betterbib.pybtex_to_bibtex_string(ref_entry, key) == "\n".join(ref_str)
