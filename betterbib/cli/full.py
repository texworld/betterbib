import argparse
import sys

from pybtex.database.input import bibtex

from .. import __about__, tools
from ..adapt_doi_urls import adapt_doi_urls
from ..journal_abbrev import journal_abbrev
from ..sync import sync


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    # As of Python 3.6, all dictionaries are ordered.
    data = bibtex.Parser().parse_file(args.infile)
    # Use an ordered dictionary to make sure that the entries are written out
    # sorted by their BibTeX key if demanded.
    tuples = data.entries.items()
    if args.sort_by_bibkey:
        tuples = sorted(data.entries.items())

    d = dict(tuples)

    d = tools.decode(d)

    d = sync(d, args.source, args.long_journal_names, args.num_concurrent_requests)
    d = adapt_doi_urls(d, args.doi_url_type)
    d = journal_abbrev(d, args.long_journal_names, args.extra_abbrev_file)

    tools.write(d, args.outfile, args.delimeter_type, tab_indent=args.tab_indent)
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
        "--long-journal-names",
        action="store_true",
        help="prefer long journal names (default: false)",
    )
    parser.add_argument(
        "--extra-abbrev-file",
        default=None,
        help="custom journal abbreviations, as JSON file",
    )
    parser.add_argument(
        "-c",
        "--num-concurrent-requests",
        type=int,
        default=10,
        metavar="N",
        help="number of concurrent HTTPS requests (default: 10)",
    )
    parser.add_argument(
        "-b",
        "--sort-by-bibkey",
        action="store_true",
        help="sort entries by BibTeX key (default: false)",
    )
    parser.add_argument(
        "-t",
        "--tab-indent",
        action="store_true",
        help="use tabs for indentation (default: false, use spaces)",
    )
    parser.add_argument(
        "-d",
        "--delimeter-type",
        choices=["braces", "quotes"],
        default="braces",
        help=("which delimeters to use in the output file " "(default: braces {...})"),
    )
    parser.add_argument(
        "-u",
        "--doi-url-type",
        choices=["unchanged", "new", "short"],
        default="new",
        help=(
            "DOI URL (new: https://doi.org/<DOI> (default), "
            "short: https://doi.org/abcde)"
        ),
    )
    return parser
