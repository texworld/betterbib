import argparse

from ..tools import bibtex_parser, doi_from_url, to_string, write
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

    od = data.entries

    # deduplicate
    for key in data.entries:
        if "url" in od[key].fields and "doi" in od[key].fields:
            doi = doi_from_url(od[key].fields["url"])
            if doi == od[key].fields["doi"]:
                # Would be nicer to remove it completely; see
                # <https://bitbucket.org/pybtex-devs/pybtex/issues/104/implement>.
                if args.keep_doi:
                    od[key].fields["url"] = None
                else:
                    od[key].fields["doi"] = None

    string = to_string(od, args.delimiter_type, tab_indent=args.tab_indent)
    write(string, infile, args.in_place)


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Removes one of DOI and URL in a BibTeX file "
        "if both are identical."
    )

    parser = get_version_parser_arguments(parser)
    parser = get_file_parser_arguments(parser)
    parser = get_formatting_parser_arguments(parser)

    parser.add_argument(
        "-k",
        "--keep-doi",
        action="store_true",
        help="keep the DOI rather than the URL (default: false)",
    )
    return parser
