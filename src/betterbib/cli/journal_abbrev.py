import argparse

from ..journal_abbrev import journal_abbrev
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
    d = dict(data.entries.items())

    d = journal_abbrev(d, args.long_journal_names, args.extra_abbrev_file)

    string = to_string(d, "braces", tab_indent=False)

    write(string, infile if args.in_place else None)


def _get_parser():
    parser = argparse.ArgumentParser(description="(Un)abbreviate journal names.")

    parser = get_version_parser_arguments(parser)
    parser = get_file_parser_arguments(parser)
    parser = get_formatting_parser_arguments(parser)

    parser.add_argument(
        "-l",
        "--long-journal-names",
        action="store_true",
        help="use long journal names (default: false)",
    )
    parser.add_argument(
        "--extra-abbrev-file",
        default=None,
        help="custom journal abbreviations, as JSON file",
    )
    return parser
