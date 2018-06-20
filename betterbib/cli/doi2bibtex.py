# -*- coding: utf-8 -*-
#
from __future__ import print_function, unicode_literals

import sys

from .. import tools, Crossref, __about__


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)
    source = Crossref()
    entry = source.get_by_doi(args.doi)
    bibtex_key = "bibtex"
    print(tools.pybtex_to_bibtex_string(entry, bibtex_key))
    return


def _get_parser():
    import argparse

    parser = argparse.ArgumentParser(description="Turn a DOI into a BibTeX entry.")
    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version="betterbib {}, Python {}".format(__about__.__version__, sys.version),
    )
    parser.add_argument("doi", type=str, help="input DOI")
    return parser
