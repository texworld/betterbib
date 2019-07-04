from .__about__ import __version__, __author__, __author_email__, __website__

from . import cli
from .tools import (
    create_dict,
    decode,
    pybtex_to_dict,
    pybtex_to_bibtex_string,
    write,
    update,
    translate_month,
)
from .crossref import Crossref
from .dblp import Dblp
from .sync import sync
from .journal_abbrev import journal_abbrev
from .adapt_doi_urls import adapt_doi_urls

__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__website__",
    "cli",
    "create_dict",
    "decode",
    "pybtex_to_dict",
    "pybtex_to_bibtex_string",
    "write",
    "update",
    "translate_month",
    "Crossref",
    "Dblp",
    "sync",
    "journal_abbrev",
    "adapt_doi_urls",
]
