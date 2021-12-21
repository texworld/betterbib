from ..adapt_doi_urls import adapt_doi_urls
from ..tools import bibtex_parser, dict_to_string, filter_fields, write
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
        string = dict_to_string(
            d,
            args.delimiter_type,
            tab_indent=args.tab_indent,
            page_range_separator="--",
            # FIXME: use public argument when it becomes possible
            preamble=data._preamble,
        )

        write(string, infile if args.in_place else None)


def add_args(parser):
    add_file_parser_arguments(parser)
    add_formatting_parser_arguments(parser)

    parser.add_argument(
        "--drop",
        action="append",
        help="drops field from bibtex entry if they exist, can be passed multiple times",
    )
