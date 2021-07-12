import argparse

from pybtex.database.input import bibtex

from .. import tools
from ..adapt_doi_urls import adapt_doi_urls
from .default_parser import get_default_parser_arguments


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    for infile in args.infiles:
        try:
            data = bibtex.Parser().parse_file(infile)

            string = _format(args, data)

            if args.in_place:

                # Probably should raise error if trying in_place with stdin

                with open(infile.name, "w") as f:
                    f.write(string)

            else:

                # Maybe append to the outfile ?

                args.outfile.write(string)

        except Exception as e:
            print("There was an error when parsing " + infile.name)
            raise e


def _format(args, data):
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

    return string


def _get_parser():
    parser = argparse.ArgumentParser(description="Reformat BibTeX files.")

    parser = get_default_parser_arguments(parser)

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
