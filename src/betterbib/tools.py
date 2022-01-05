from __future__ import annotations

import configparser
import re
import sys
from copy import deepcopy
from pathlib import Path
from warnings import warn

import appdirs
import enchant
import requests
import tomli

# for enhanced error messages when parsing
from pybtex.database import Entry
from pybtex.database.input import bibtex
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexencode import unicode_to_latex

from .__about__ import __version__
from .errors import UniqueError


def decode(entry: Entry) -> Entry:
    """Decode a dictionary with LaTeX strings into a dictionary with unicode strings."""
    translator = LatexNodes2Text()
    # Perform a deepcopy, otherwise the input entry will get altered
    out = deepcopy(entry)
    assert out.fields is not None
    for key, value in out.fields.items():
        if key == "url":
            # The url can contain special LaTeX characters (like %) and that's fine
            continue
        out.fields[key] = translator.latex_to_text(value)
    return out


def pybtex_to_dict(entry):
    """dict representation of BibTeX entry."""
    d = {}
    d["genre"] = entry.type
    transform = unicode_to_latex
    for key, persons in entry.persons.items():
        d[key.lower()] = [
            {
                "first": [transform(string) for string in p.first_names],
                "middle": [transform(string) for string in p.middle_names],
                "prelast": [transform(string) for string in p.prelast_names],
                "last": [transform(string) for string in p.last_names],
                "lineage": [transform(string) for string in p.lineage_names],
            }
            for p in persons
        ]
    for field, value in entry.fields.items():
        d[field.lower()] = value
    return d


def translate_month(key: str):
    """The month value can take weird forms. Sometimes, it's given as an int, sometimes
    as a string representing an int, and sometimes the name of the month is spelled out.
    Try to handle most of this here.
    """
    months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]

    # Sometimes, the key is just a month
    try:
        return months[int(key) - 1]
    except (TypeError, ValueError):
        # TypeError: unsupported operand type(s) for -: 'str' and 'int'
        pass

    # Split for entries like "March-April"
    strings = []
    for k in key.split("-"):
        month = k[:3].lower()

        # Month values like '????' appear -- skip them
        if month in months:
            strings.append(month)
        else:
            print(f"Unknown month value '{key}'. Skipping.")
            return None

    return ' # "-" # '.join(strings)


def _get_config_data() -> tuple[list[str], list[str]]:
    _config_dir = Path(appdirs.user_config_dir("betterbib"))

    ini_config = _config_dir / "config.ini"
    toml_config = _config_dir / "config.toml"

    add_list = []
    remove_list = []

    if toml_config.exists():
        with open(toml_config, "rb") as f:
            config_data = tomli.load(f)

        try:
            add_list = config_data["DICTIONARY"]["add"]
        except KeyError:
            pass

        try:
            remove_list = config_data["DICTIONARY"]["remove"]
        except KeyError:
            pass

    elif ini_config.exists():
        warn(
            f"betterbib INI ({ini_config}) config is deprecated. "
            + "Please convert to TOML."
        )

        config = configparser.ConfigParser()
        config.read(ini_config)
        try:
            add_list = config.get("DICTIONARY", "add").split(",")
        except (configparser.NoSectionError, configparser.NoOptionError):
            # No section: 'DICTIONARY', No option 'add' in section: 'DICTIONARY'
            pass

        try:
            remove_list = config.get("DICTIONARY", "remove").split(",")
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

    return add_list, remove_list


def create_dict():
    d = enchant.DictWithPWL("en_US")

    add_list, remove_list = _get_config_data()

    for word in add_list:
        word = word.strip()
        d.add(word)
        d.add(word + "'s")
        if word[-1] == "s":
            d.add(word + "'")

    for word in remove_list:
        d.remove(word.strip())

    return d


def _translate_word(word, d):
    # Check if the word needs to be protected by curly braces to prevent
    # recapitalization.
    if (
        not word
        or word.count("{") != word.count("}")
        or (word[0] == "{" and word[-1] == "}")
        or word[0] == "\\"
    ):
        needs_protection = False
    elif any([char.isupper() for char in word[1:]]):
        needs_protection = True
    else:
        needs_protection = (
            any([char.isupper() for char in word])
            and d.check(word)
            and not d.check(word.lower())
        )

    if needs_protection:
        return "{" + word + "}"
    return word


def _translate_title(val, dictionary=create_dict()):
    """The capitalization of BibTeX entries is handled by the style, so names (Newton)
    or abbreviations (GMRES) may not be capitalized. This is unless they are wrapped in
    curly braces.
    This function takes a raw title string as input and {}-protects those parts whose
    capitalization should not change.
    """
    # If the title is completely capitalized, it's probably by mistake.
    if val == val.upper():
        val = val.title()

    words = val.split()
    # Handle colons as in
    # ```
    # Algorithm 694: {A} collection...
    # ```
    for k in range(len(words)):
        if k > 0 and words[k - 1][-1] == ":" and words[k][0] != "{":
            words[k] = "{" + words[k].capitalize() + "}"

    words = [
        "-".join([_translate_word(w, dictionary) for w in word.split("-")])
        for word in words
    ]

    return " ".join(words)


def sanitize_title(d) -> None:
    for _, entry in d.items():
        try:
            title = entry.fields["title"]
            entry.fields["title"] = _translate_title(title)
        except KeyError:
            warn(f"'entry' {entry} has no title")


def pybtex_to_bibtex_string(
    entry: Entry,
    bibtex_key: str,
    delimiters: tuple[str, str] = ("{", "}"),
    page_range_separator: str = "--",
    indent: str = " ",
    sort: bool = False,
    unicode: bool = True,
) -> str:
    """String representation of BibTeX entry."""
    out = f"@{entry.type}{{{bibtex_key},\n{indent}"
    content = []

    left, right = delimiters

    assert entry.persons is not None
    for key, persons in entry.persons.items():
        persons_str = " and ".join([_get_person_str(p) for p in persons])
        if not unicode:
            persons_str = unicode_to_latex(persons_str)
        content.append(f"{key.lower()} = {left}{persons_str}{right}")

    assert entry.fields is not None
    keys = entry.fields.keys()
    if sort:
        keys = sorted(keys)

    # translator = LatexNodes2Text()

    for key in keys:
        value = entry.fields[key]

        try:
            value = value.replace("\N{REPLACEMENT CHARACTER}", "?")
        except AttributeError:
            pass

        try:
            if key not in ["url", "doi"]:
                # Parse the original value to get a unified version
                # value = translator.latex_to_text(value)
                # # back to latex to escape "&" etc.
                # value = unicode_to_latex(value)
                # Replace multiple spaces by one
                value = re.sub(" +", " ", value)
                # Remove trailing spaces
                value = value.rstrip()
        except TypeError:
            # expected unicode for encode input, but got int instead
            pass

        # Always make keys lowercase
        key = key.lower()

        if key == "pages":
            # Replace any number of `-` by page_range_separator; see
            # <https://tex.stackexchange.com/a/58671/13262>
            value = re.sub("-+", page_range_separator, value)

        if key == "month":
            month_string = translate_month(value)
            if month_string:
                content.append(f"{key} = {month_string}")
            continue

        if value is not None:
            content.append(f"{key} = {left}{value}{right}")

    # Make sure that every line ends with a comma
    out += indent.join([line + ",\n" for line in content])
    out += "}"
    return out


def doi_from_url(url):
    """See if this is a DOI URL and return the DOI."""
    m = re.match("https?://(?:dx\\.)?doi\\.org/(.*)", url)
    if m:
        return m.group(1)
    return None


def get_short_doi(doi):
    url = "http://shortdoi.org/" + doi
    r = requests.get(url, params={"format": "json"})
    if not r.ok:
        return None

    data = r.json()
    if "ShortDOI" not in data:
        return None

    return data["ShortDOI"]


def _get_person_str(p):
    out = ", ".join(
        filter(
            None,
            [
                " ".join(p.prelast_names + p.last_names),
                " ".join(p.lineage_names),
                # In plain English, you wouldn't put a full space between abbreviated
                # initials, see, e.g.,
                # <https://english.stackexchange.com/a/105529/23644>. In bib files,
                # though, it's useful, see
                # <https://github.com/nschloe/betterbib/issues/212> and
                # <https://clauswilke.com/blog/2015/10/02/bibtex/>.
                # See <https://tex.stackexchange.com/a/11083/13262> on how to configure
                # biber/biblatex to use thin spaces.
                " ".join(p.first_names + p.middle_names),
            ],
        )
    )
    # If the name is completely capitalized, it's probably by mistake.
    if out == out.upper():
        out = out.title()
    return out


def prettyprint_result(res):
    string = []
    if "score" in res:
        string.append(f"score:     {res['score']}")
    if "type" in res:
        string.append(f"type:      {res['type']}")
    if "title" in res:
        string.append(f"title:     {res['title'][0]}")
    if "DOI" in res:
        string.append(f"DOI:       {res['DOI']}")
    if "page" in res:
        string.append(f"page:      {res['page']}")
    if "publisher" in res:
        string.append(f"publisher: {res['publisher']}")
    if "container-title" in res:
        string.append(f"container: {res['container-title'][0]}")
    if "volume" in res:
        string.append(f"volume:    {res['volume']}")
    if "issue" in res:
        string.append(f"issue:     {res['issue']}")
    if "reference-count" in res:
        string.append(f"ref count: {res['reference-count']}")
    if "language" in res:
        string.append(f"language:  {res['language']}")
    return "\n".join(string)


def heuristic_unique_result(results, d):
    # Q: How to we find the correct solution if there's more than one search result?
    # As a heuristic, assume that the top result is the unique answer if its score is at
    # least 1.5 times the score of the the second-best result.
    for score in ["score", "@score"]:
        try:
            if float(results[0][score]) > 1.5 * float(results[1][score]):
                return results[0]
        except KeyError:
            pass

    # If that doesn't work, check if the DOI matches exactly with the input.
    if "doi" in d:
        # sometimes, the doi field contains a doi url
        doi = doi_from_url(d["doi"])
        if not doi:
            doi = d["doi"]
        for result in results:
            for doi_key in "doi", "DOI":
                try:
                    if result[doi_key].lower() == doi.lower():
                        return result
                except KeyError:
                    pass

    # If that doesn't work, check if the title appears in the input.
    if "title" in d:
        for result in results:
            if (
                "title" in result
                and result["title"]
                and result["title"][0].lower() in d["title"].lower()
            ):
                return result

    # If that doesn't work, check if the page range matches exactly with the input.
    if "pages" in d:
        for result in results:
            if "page" in result and result["page"] == d["pages"]:
                return result

    # If that doesn't work, check if the second entry is a JSTOR copy of the original
    # article -- yes, that happens --, and take the first one.
    if (
        "publisher" in results[1]
        and results[1]["publisher"] == "JSTOR"
        and "title" in results[0]
        and "title" in results[1]
        and results[0]["title"][0].lower() == results[1]["title"][0].lower()
    ):
        return results[0]

    pretty_res = [prettyprint_result(results[0]), prettyprint_result(results[1])]
    raise UniqueError(
        "Could not find a positively unique match. "
        f"Got\n\n{pretty_res[0]}\n\nand\n\n{pretty_res[1]}\n"
    )


# This used to be a write() function, but beware of exceptions! Files would get
# unintentionally overridden, see <https://github.com/nschloe/betterbib/issues/184>
def dict_to_string(
    od: dict[str, Entry],
    delimiter_type: str,
    page_range_separator: str,
    tab_indent: bool,
    preamble: list | None = None,
    unicode: bool = True,
) -> str:
    """
    Creates a string representing the bib entries

        Parameters:
            od (dict): dictionary of bibtex entries
            outfile (FileType("r")): file to write to (default: None)
            delimiter_type (str): delimiter to use to mark strings
            tab_indent (bool): whether to use tabs to indent the entries
            preamble (list): list of preamble commands

        Returns:
            string
    """
    # Write header to the output file.
    segments = [f"%comment{{This file was created with betterbib v{__version__}.}}\n"]

    delimiters = {"braces": ("{", "}"), "quotes": ('"', '"')}[delimiter_type]

    if preamble:
        # Add segments for each preamble entry
        segments.extend(
            [f'@preamble{{"{preamble_string}"}}' for preamble_string in preamble]
        )

    # Add segments for each bibtex entry in order
    segments.extend(
        [
            pybtex_to_bibtex_string(
                d,
                bib_id,
                delimiters=delimiters,
                page_range_separator=page_range_separator,
                indent="\t" if tab_indent else " ",
                unicode=unicode,
            )
            for bib_id, d in od.items()
        ]
    )
    return "\n\n".join(segments) + "\n"


def merge(entry1, entry2):
    """Create a merged BibTeX entry with the data from entry2 taking precedence."""
    out = entry1
    if entry2 is not None:
        if entry2.type:
            out.type = entry2.type

        if entry2.persons:
            for key, value in entry2.persons.items():
                if value:
                    out.persons[key] = value

        for key, value in entry2.fields.items():
            if value:
                out.fields[key] = value

    return out


def filter_fields(data, excludes=None):
    excludes = excludes or []
    for entry in data.entries.values():
        if entry.fields:
            entry.fields = {k: v for k, v in entry.fields.items() if k not in excludes}
    return data


def bibtex_parser(infile):
    """
    Returns the parsed bibtex data and adds context to the exception

        Parameters:
            infile (FileType("r")): file to be parsed

        Returns:
            data (dict): bibtex entries
    """
    try:
        data = bibtex.Parser().parse_file(infile)
        return data

    except Exception as e:
        print("There was an error when parsing " + infile.name)
        raise e


def write(string: str, outfile=None):
    """
    Writes a string to a BibTeX file

        Parameters:
            string (String): string to write
            outfile (FileType("r")): file to write to (default: None)
    """
    if outfile:
        with open(outfile.name, "w") as f:
            f.write(string)
    else:
        sys.stdout.write(string)
