from ..journal_abbrev import journal_abbrev
from ..tools import bibtex_parser, to_string, write
from .helpers import add_file_parser_arguments, add_formatting_parser_arguments


def run(args):
    for infile in args.infiles:
        data = bibtex_parser(infile)
        d = dict(data.entries.items())

        d = journal_abbrev(d, args.long_journal_names, args.extra_abbrev_file)

        string = to_string(d, "braces", tab_indent=False)

        write(string, infile if args.in_place else None)


def add_args(parser):
    add_file_parser_arguments(parser)
    add_formatting_parser_arguments(parser)

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
