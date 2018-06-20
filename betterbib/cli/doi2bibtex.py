# -*- coding: utf-8 -*-
#
from __future__ import print_function, unicode_literals

import argparse
import sys

from .. import tools, crossref, __about__


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)
    source = crossref.Crossref()
    entry = source.get_by_doi(args.doi)

    bibtex_key = "key"
    string = tools.pybtex_to_bibtex_string(entry, bibtex_key)
    args.outfile.write(string)
    return


def _get_parser():
    parser = argparse.ArgumentParser(description="Turn a DOI into a BibTeX entry.")
    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version="betterbib {}, Python {}".format(__about__.__version__, sys.version),
    )
    parser.add_argument("doi", type=str, help="input DOI")
    parser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output file (default: stdout)",
    )
    return parser
