# -*- coding: utf-8 -*-
#
from __future__ import print_function, unicode_literals

import argparse
import sys

from pybtex.database.input import bibtex

from .. import __about__, tools
from ..journal_abbrev import journal_abbrev


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    data = bibtex.Parser().parse_file(args.infile)
    d = tools.decode(dict(data.entries.items()))

    d = journal_abbrev(d, args.long_journal_names)

    tools.write(d, args.outfile, "braces", tab_indent=False)
    return


def _get_parser():
    parser = argparse.ArgumentParser(description="(Un)abbreviate journal names.")
    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version="betterbib {}, Python {}".format(__about__.__version__, sys.version),
    )
    parser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="input BibTeX file (default: stdin)",
    )
    parser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output BibTeX file (default: stdout)",
    )
    parser.add_argument(
        "-l",
        "--long-journal-names",
        action="store_true",
        help="use long journal names (default: false)",
    )
    return parser
