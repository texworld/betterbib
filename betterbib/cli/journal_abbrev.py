# -*- coding: utf-8 -*-
#
from __future__ import print_function, unicode_literals

import argparse
import collections
import sys

from pybtex.database.input import bibtex

from .. import tools, __about__


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    updater = tools.JournalNameUpdater(args.long_journal_names)

    data = bibtex.Parser().parse_file(args.infile)
    for key in data.entries:
        updater.update(data.entries[key])

    od = tools.decode(collections.OrderedDict(data.entries.items()))
    tools.write(od, args.outfile, "braces", tab_indent=False)
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
