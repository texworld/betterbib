import argparse

from pybtex.database.input import bibtex

from .. import tools
from ..adapt_doi_urls import adapt_doi_urls
from ..journal_abbrev import journal_abbrev
from ..sync import sync
from .default_parser import get_default_parser_arguments


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    for infile in args.infiles:

        # Make sure that the entries are written out sorted by their BibTeX key if demanded.
        data = bibtex.Parser().parse_file(infile)
        tuples = data.entries.items()
        if args.sort_by_bibkey:
            tuples = sorted(data.entries.items())

        d = dict(tuples)

        d = sync(d, args.source, args.long_journal_names, args.num_concurrent_requests)
        d = adapt_doi_urls(d, args.doi_url_type)
        d = tools.sanitize_title(d)
        d = journal_abbrev(d, args.long_journal_names, args.extra_abbrev_file)

        string = tools.to_string(d, args.delimiter_type, tab_indent=args.tab_indent)

        if args.in_place:
            with open(infile.name, "w") as f:
                f.write(string)
        else:
            args.outfile.write(string)


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Sync BibTeX files with information from online sources."
    )

    parser = get_default_parser_arguments(parser)

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
        default=False,
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
    return parser
