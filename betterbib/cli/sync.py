# -*- coding: utf-8 -*-
#
from __future__ import print_function, unicode_literals

import argparse
import collections
import sys

from pybtex.database.input import bibtex

from .. import __about__
from ..sync import sync
from ..tools import decode, write


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    # Use an ordered dictionary to make sure that the entries are written out
    # the way they came in.
    data = bibtex.Parser().parse_file(args.infile)
    # data.entries.items() is a list of tuples, the first item being the BibTeX key.
    input_od = collections.OrderedDict(data.entries.items())
    input_od = decode(input_od)

    out = sync(
        input_od,
        args.source,
        args.long_journal_name,
        args.num_concurrent_requests,
    )

    write(out, args.outfile, "braces", tab_indent=False)
    return


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Sync BibTeX files with information from online sources."
    )
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
        "-s",
        "--source",
        choices=["crossref", "dblp"],
        default="crossref",
        help="data source (default: crossref)",
    )
    parser.add_argument(
        "-l",
        "--long-journal-name",
        action="store_true",
        help="prefer long journal names (default: false)",
    )
    parser.add_argument(
        "-c",
        "--num-concurrent-requests",
        type=int,
        default=10,
        metavar="N",
        help="number of concurrent HTTPS requests (default: 10)",
    )
    return parser
