import argparse

from ..adapt_doi_urls import adapt_doi_urls
from ..journal_abbrev import journal_abbrev
from ..sync import sync
from ..tools import bibtex_parser, bibtex_writer, sanitize_title, to_string
from .default_parser import (
    get_file_parser_arguments,
    get_formatting_parser_arguments,
    get_version_parser_arguments,
)


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    for infile in args.infiles:
        _handle_single(args, infile)


def _handle_single(args, infile):
    """
    Parse and handle a single file

        Parameters:
            args (dict): commandline arguments
            infile (FileType("r")): file to be handled
    """
    # Make sure that the entries are written out sorted by their BibTeX key if demanded.
    data = bibtex_parser(infile)
    tuples = data.entries.items()
    if args.sort_by_bibkey:
        tuples = sorted(data.entries.items())

    d = dict(tuples)

    d = sync(
        d,
        args.source,
        args.long_journal_names,
        args.num_concurrent_requests,
        not args.in_place,
    )
    d = adapt_doi_urls(d, args.doi_url_type)
    d = sanitize_title(d)
    d = journal_abbrev(d, args.long_journal_names, args.extra_abbrev_file)

    string = to_string(d, args.delimiter_type, tab_indent=args.tab_indent)

    bibtex_writer(string, infile, args.in_place)


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Sync BibTeX files with information from online sources."
    )

    parser = get_version_parser_arguments(parser)
    parser = get_file_parser_arguments(parser)
    parser = get_formatting_parser_arguments(parser)

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
    return parser
