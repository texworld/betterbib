from ..adapt_doi_urls import adapt_doi_urls
from ..journal_abbrev import journal_abbrev
from ..sync import sync
from ..tools import bibtex_parser, sanitize_title, to_string, write
from .helpers import add_file_parser_arguments, add_formatting_parser_arguments


def run(args):
    for infile in args.infiles:
        # Make sure that the entries are written out sorted by their BibTeX key if
        # demanded.
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
            args.in_place,
        )
        d = adapt_doi_urls(d, args.doi_url_type)
        sanitize_title(d)
        d = journal_abbrev(d, args.long_journal_names, args.extra_abbrev_file)

        string = to_string(
            d,
            args.delimiter_type,
            tab_indent=args.tab_indent,
            unicode=not args.latex_output,
        )

        write(string, infile if args.in_place else None)


def add_args(parser):
    add_file_parser_arguments(parser)
    add_formatting_parser_arguments(parser)

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
        "-a",
        "--latex-output",
        action="store_true",
        default=False,
        help="force LaTeX output (default: unicode)",
    )
    return parser
