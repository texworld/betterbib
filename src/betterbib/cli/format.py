import argparse
import sys

from pybtex.database.input import bibtex

from .. import tools
from ..__about__ import __version__
from ..adapt_doi_urls import adapt_doi_urls


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    data = bibtex.Parser().parse_file(args.infile)

    if args.drop:
        data = tools.filter_fields(data, args.drop)

    # Use an ordered dictionary to make sure that the entries are written out
    # sorted by their BibTeX key if demanded.
    tuples = data.entries.items()
    if args.sort_by_bibkey:
        tuples = sorted(data.entries.items())

    d = dict(tuples)

    d = adapt_doi_urls(d, args.doi_url_type)

    string = tools.to_string(d, args.delimiter_type, tab_indent=args.tab_indent)

    if args.in_place:
        with open(args.infile.name, "w") as f:
            f.write(string)
    else:
        args.outfile.write(string)


def _get_parser():
    parser = argparse.ArgumentParser(description="Reformat BibTeX files.")

    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version=f"betterbib {__version__}, Python {sys.version}",
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
        "-i", "--in-place", action="store_true", help="modify infile in place"
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
        help="use tabs for indentation (default: false)",
    )
    parser.add_argument(
        "-d",
        "--delimiter-type",
        choices=["braces", "quotes"],
        default="braces",
        help=("which delimiters to use in the output file " "(default: braces {...})"),
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
    parser.add_argument(
        "--drop",
        nargs="+",
        default=[],
        help="Drops fields from bibtex entry if they exist.",
    )
    return parser
