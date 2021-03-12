import argparse
import sys

from pybtex.database.input import bibtex

from .. import tools
from ..__about__ import __version__


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    data = bibtex.Parser().parse_file(args.infile)

    od = data.entries

    # deduplicate
    for key in data.entries:
        if "url" in od[key].fields and "doi" in od[key].fields:
            doi = tools.doi_from_url(od[key].fields["url"])
            if doi == od[key].fields["doi"]:
                # Would be nicer to remove it completely; see
                # <https://bitbucket.org/pybtex-devs/pybtex/issues/104/implement>.
                if args.keep_doi:
                    od[key].fields["url"] = None
                else:
                    od[key].fields["doi"] = None

    _write(od, args.outfile, "curly")


def _write(od, out, delimiter_type):
    # Write header to the output file.
    out.write(f"%comment{{This file was created with betterbib v{__version__}.}}\n\n")

    # write the data out sequentially to respect ordering
    for bib_id, d in od.items():
        delimiters = ("{", "}") if delimiter_type == "curly" else ('"', '"')
        a = tools.pybtex_to_bibtex_string(d, bib_id, delimiters=delimiters)
        out.write(a + "\n\n")


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Removes one of DOI and URL in a BibTeX file "
        "if both are identical."
    )
    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version=f"betterbib {__version__}, Python {sys.version}",
    )
    parser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="input BibTeX file (default: stdin)",
    )
    parser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output BibTeX file (default: stdout)",
    )
    parser.add_argument(
        "-k",
        "--keep-doi",
        action="store_true",
        help="keep the DOI rather than the URL (default: false)",
    )
    return parser
