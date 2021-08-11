import argparse
from sys import version_info

from ..__about__ import __version__
from . import _doi_to_bibtex, _format, _journal_abbrev, _update


def main(argv=None):
    parent_parser = argparse.ArgumentParser(
        description="Sync BibTeX files with information from online sources."
    )

    python_version = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    version_text = "\n".join(
        [
            f"betterbib {__version__} [Python {python_version}]",
            "Copyright (c) 2013-2021 Nico Schlömer",
        ]
    )
    parent_parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=version_text,
        help="display version information",
    )

    subparsers = parent_parser.add_subparsers(
        title="subcommands", dest="command", required=True
    )

    parser = subparsers.add_parser(
        "update",
        help="Sync BibTeX files with information from online sources",
        aliases=["up"],
    )
    _update.add_args(parser)
    parser.set_defaults(func=_update.run)

    parser = subparsers.add_parser(
        "format",
        help="Format BibTeX files",
        aliases=["f"],
    )
    _format.add_args(parser)
    parser.set_defaults(func=_format.run)

    parser = subparsers.add_parser(
        "abbreviate-journal-names",
        help="(Un)abbreviate journal names.",
        aliases=["aj"],
    )
    _journal_abbrev.add_args(parser)
    parser.set_defaults(func=_journal_abbrev.run)

    parser = subparsers.add_parser(
        "doi-to-bibtex",
        help="Turn a DOI into a BibTeX entry.",
        aliases=["db"],
    )
    _doi_to_bibtex.add_args(parser)
    parser.set_defaults(func=_doi_to_bibtex.run)

    args = parent_parser.parse_args(argv)

    return args.func(args)
