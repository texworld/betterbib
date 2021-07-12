import argparse

from pybtex.database.input import bibtex

from .. import tools
from ..journal_abbrev import journal_abbrev
from .default_parser import get_default_parser_arguments


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    for infile in args.infiles:

        data = bibtex.Parser().parse_file(infile)
        d = dict(data.entries.items())

        d = journal_abbrev(d, args.long_journal_names, args.extra_abbrev_file)

        string = tools.to_string(d, "braces", tab_indent=False)
        if args.in_place:
            with open(infile.name, "w") as f:
                f.write(string)
        else:
            args.outfile.write(string)


def _get_parser():
    parser = argparse.ArgumentParser(description="(Un)abbreviate journal names.")
    parser = get_default_parser_arguments(parser)
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
