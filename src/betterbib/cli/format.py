import argparse

from ..adapt_doi_urls import adapt_doi_urls
from ..tools import bibtex_parser, bibtex_writer, filter_fields, to_string
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
    data = bibtex_parser(infile)

    string = _format(args, data)

    bibtex_writer(string, infile, args.in_place)


def _format(args, data):
    """
    Formats a bibtex dictionary

        Parameters:
            args (dict): commandline arguments
            data (dict): bibtex entries

        Returns:
            string (String): Formatted multiline string of the entries
    """
    if args.drop:
        data = filter_fields(data, args.drop)

    # Use an ordered dictionary to make sure that the entries are written out
    # sorted by their BibTeX key if demanded.
    tuples = data.entries.items()
    if args.sort_by_bibkey:
        tuples = sorted(data.entries.items())

    d = dict(tuples)

    d = adapt_doi_urls(d, args.doi_url_type)

    string = to_string(d, args.delimiter_type, tab_indent=args.tab_indent)

    return string


def _get_parser():
    parser = argparse.ArgumentParser(description="Reformat BibTeX files.")

    parser = get_version_parser_arguments(parser)
    parser = get_file_parser_arguments(parser)
    parser = get_formatting_parser_arguments(parser)

    parser.add_argument(
        "--drop",
        nargs="+",
        default=[],
        help="Drops fields from bibtex entry if they exist.",
    )
    return parser
