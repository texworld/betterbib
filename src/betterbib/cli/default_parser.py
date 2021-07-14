import argparse
import sys

from ..__about__ import __version__


def get_default_parser_arguments(parser):
    """
    Adds the default arguments to an argparse parser
    """
    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version=f"betterbib {__version__}, Python {sys.version}",
    )
    parser.add_argument(
        "infiles",
        nargs="+",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="input BibTeX files (default: stdin)",
    )
    parser.add_argument(
        "-i", "--in-place", action="store_true", help="modify infile in place"
    )
    return parser
