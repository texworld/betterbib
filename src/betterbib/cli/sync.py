import argparse

from ..sync import sync
from ..tools import bibtex_parser, to_string, write
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
    # data.entries.items() is a list of tuples, the first item being the BibTeX key.
    input_dict = dict(data.entries.items())

    out = sync(
        input_dict,
        args.source,
        args.long_journal_name,
        args.num_concurrent_requests,
        args.in_place,
    )

    string = to_string(out, args.delimiter_type, tab_indent=args.tab_indent)

    write(string, infile if args.in_place else None)


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
        "--long-journal-name",
        action="store_true",
        default=False,
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
