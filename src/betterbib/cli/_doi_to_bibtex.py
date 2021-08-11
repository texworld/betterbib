from unidecode import unidecode

from .. import crossref
from ..tools import to_string, write
from .helpers import add_formatting_parser_arguments


def run(args):
    source = crossref.Crossref()
    entry = source.get_by_doi(args.doi)

    # Create a citekey for entry using the [author:lower][year] JabRef pattern.
    # See https://retorque.re/zotero-better-bibtex/citing/
    bibtex_key = ""
    if (
        entry.persons
        and "author" in entry.persons
        and entry.persons["author"]
        and entry.persons["author"][0].last_names
    ):
        bibtex_key += unidecode(entry.persons["author"][0].last_names[0].lower())
    if "year" in entry.fields and entry.fields["year"]:
        bibtex_key += str(entry.fields["year"])
    if not bibtex_key:
        bibtex_key = "key"

    string = to_string(
        {bibtex_key: entry}, args.delimiter_type, tab_indent=args.tab_indent
    )

    write(string)


def add_args(parser):
    add_formatting_parser_arguments(parser)
    parser.add_argument("doi", type=str, help="input DOI")
