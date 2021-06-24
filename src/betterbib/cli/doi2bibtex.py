import argparse
import os
import sys

import slugify

from .. import __about__, crossref, tools


def _get_version_text():
    return "\n".join(
        [
            "betterbib {} [Python {}.{}.{}]".format(
                __about__.__version__,
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            "Copyright (c) 2013-2020, Nico Schlömer <{nico.schloemer@gmail.com}>",
        ]
    )


def _create_key_for_entry(entry):
    with open(
        os.path.dirname(os.path.realpath(__file__))
        + "/nltk_english_stop_words.txt",
        "r",
    ) as f:
        nltk_english_stop_words = set(f.readlines())
    bibtex_key = ""
    if entry.persons and entry.persons["author"]:
        bibtex_key += "_".join(entry.persons["author"][0].last()).lower()
    if entry.fields["year"]:
        bibtex_key += "_" + str(entry.fields["year"])
    if entry.fields["title"]:
        bibtex_key += "_" + slugify.slugify(
            entry.fields["title"],
            max_length=8,
            separator="_",
            stopwords=nltk_english_stop_words,
        )
    if not bibtex_key:
        bibtex_key = "key"
    return bibtex_key


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)
    source = crossref.Crossref()
    entry = source.get_by_doi(args.doi)

    if args.create_key:
        bibtex_key = _create_key_for_entry(entry)
    else:
        bibtex_key = "key"

    string = tools.pybtex_to_bibtex_string(entry, bibtex_key)
    args.outfile.write(string)
    return


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Turn a DOI into a BibTeX entry."
    )
    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version=_get_version_text(),
    )
    parser.add_argument("doi", type=str, help="input DOI")
    parser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output file (default: stdout)",
    )
    parser.add_argument(
        "--create-key",
        action="store_true",
        help=(
            "whether to create a key using the pattern "
            "{first_name}_{shortened_title}_{year}"
        ),
    )
    return parser
