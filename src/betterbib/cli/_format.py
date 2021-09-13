from ..adapt_doi_urls import adapt_doi_urls
from ..tools import bibtex_parser, filter_fields, to_string, write
from .helpers import add_file_parser_arguments, add_formatting_parser_arguments


def run(args):
    for infile in args.infiles:
        data = bibtex_parser(infile)

        if args.drop:
            data = filter_fields(data, args.drop)

        # Use an ordered dictionary to make sure that the entries are written out
        # sorted by their BibTeX key if demanded.
        tuples = data.entries.items()
        if args.sort_by_bibkey:
            tuples = sorted(data.entries.items())

        d = dict(tuples)
        d = adapt_doi_urls(d, args.doi_url_type)
        string = to_string(
            d, args.delimiter_type, tab_indent=args.tab_indent, preamble=data._preamble
        )

        write(string, infile if args.in_place else None)


def add_args(parser):
    add_file_parser_arguments(parser)
    add_formatting_parser_arguments(parser)

    parser.add_argument(
        "--drop",
        nargs="+",
        default=[],
        help="Drops fields from bibtex entry if they exist.",
    )
