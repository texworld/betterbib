import argparse
import sys


def add_file_parser_arguments(parser):
    """
    Adds the file handling arguments to an argparse parser

        Parameters:
            parser (argparse.ArgumentParser): ArgumentParser

        Returns:
            parser (argparse.ArgumentParser): Containing the default file handling arguments
    """
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


def add_formatting_parser_arguments(parser):
    """
    Adds the bibtex formatting arguments to an argparse parser

        Parameters:
            parser (argparse.ArgumentParser): ArgumentParser

        Returns:
            parser (argparse.ArgumentParser): Containing the formatting arguments
    """
    formatting_group = parser.add_argument_group("Formatting")
    formatting_group.add_argument(
        "-b",
        "--sort-by-bibkey",
        action="store_true",
        help="sort entries by BibTeX key (default: false)",
    )
    formatting_group.add_argument(
        "-t",
        "--tab-indent",
        action="store_true",
        help="use tabs for indentation (default: false)",
    )
    formatting_group.add_argument(
        "-d",
        "--delimiter-type",
        choices=["braces", "quotes"],
        default="braces",
        help=("which delimiters to use in the output file " "(default: braces {...})"),
    )
    formatting_group.add_argument(
        "--doi-url-type",
        choices=["unchanged", "new", "short"],
        default="new",
        help=(
            "DOI URL (new: https://doi.org/<DOI> (default), "
            "short: https://doi.org/abcde)"
        ),
    )
    formatting_group.add_argument(
        "-p",
        "--page-range-separator",
        type=str,
        default="--",
        help="page range separator (default: --)",
    )
