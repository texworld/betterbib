# -*- coding: utf-8 -*-
#
from __future__ import print_function

import codecs
import re

import pybtex
import pybtex.database
import requests
import requests_cache

from .__about__ import __version__, __website__, __author_email__
from .errors import NotFoundError, HttpError
from .tools import pybtex_to_dict, heuristic_unique_result


def _bibtex_to_crossref_type(bibtex_type):
    _bibtex_to_crossref_map = {
        "article": ["journal-article"],
        "book": ["book", "monograph"],
        "inbook": ["book-chapter"],
        "misc": ["other"],
        "incollection": ["book-chapter"],
        "inproceedings": ["proceedings-article"],
        "proceedings": ["proceedings"],
        "techreport": ["report"],
    }
    try:
        return _bibtex_to_crossref_map[bibtex_type]
    except KeyError:
        return []


class Crossref(object):
    """
    Documentation of the Crossref Search API:
    <https://github.com/Crossref/rest-api-doc/blob/master/rest_api.md>.
    """

    def __init__(self, prefer_long_journal_name=False):
        self.api_url = "https://api.crossref.org/works"
        self.prefer_long_journal_name = prefer_long_journal_name

        requests_cache.install_cache("betterbib_cache", expire_after=3600)
        # requests_cache.remove_expired_responses()
        return

    def _crossref_to_bibtex_type(self, entry):
        # The difficulty here: Translating book-chapter. If the book is a
        # monograph (all chapters written by the same set of authors), then
        # return inbook, if all chapters are by different authors, return
        # incollection.
        crossref_type = entry["type"]
        if crossref_type == "book-chapter":
            # Get the containing book, and see if it has authors or editors. If
            # authors, consider it a monograph and use inbook; otherwise
            # incollection.
            # To get the book, make use of the fact that the chapter DOIs are
            # the book DOI plus some appendix, e.g., .ch3, _3, etc. In other
            # words: Strip the last digits plus whatever is nondigit before it.
            a = re.match("(.*?)([^0-9]+[0-9]+)$", entry["DOI"])
            if a is None:
                # The DOI doesn't have that structure; assume 'incollection'.
                return "incollection"

            book_doi = a.group(1)

            headers = {
                "User-Agent": "betterbib/{} ({}; mailto:{})".format(
                    __version__, __website__, __author_email__
                )
            }

            # Try to get the book data
            r = requests.get(self.api_url + "/" + book_doi, headers=headers)
            if r.ok:
                book_data = r.json()
                if "author" in book_data["message"]:
                    return "inbook"
            # else
            return "incollection"

        # All other cases
        _crossref_to_bibtex_type = {
            "book": "book",
            "dataset": "misc",
            "journal-article": "article",
            "monograph": "book",
            "other": "misc",
            "proceedings": "proceedings",
            "proceedings-article": "inproceedings",
            "report": "techreport",
        }
        return _crossref_to_bibtex_type[crossref_type]

    def get_by_doi(self, doi):
        headers = {
            "User-Agent": "betterbib/{} ({}; mailto:{})".format(
                __version__, __website__, __author_email__
            )
        }
        # https://api.crossref.org/works/10.1137/110820713
        r = requests.get(self.api_url + "/" + doi, headers=headers)
        assert r.ok
        data = r.json()
        result = data["message"]
        return self._crossref_to_pybtex(result)

    def find_unique(self, entry):
        d = pybtex_to_dict(entry)

        if "title" not in d and "doi" not in d and "author" not in d:
            raise NotFoundError("Not enough input data")

        L = []

        keys = [
            "title",
            "journal",
            "doi",
            "pages",
            "year",
            "volume",
            "number",
            "publisher",
        ]
        for key in keys:
            try:
                L.append(d[key])
            except KeyError:
                pass

        names = ["first", "middle", "prelast", "last", "lineage"]
        try:
            for au in d["author"]:
                L.extend([" ".join(au[key]) for key in names])
        except KeyError:
            pass

        # kick out empty strings
        L = filter(None, L)

        # Simply plug the dict together to a search query. Typical query:
        # https://api.crossref.org/works?query=vanroose+schl%C3%B6mer&rows=5
        payload = codecs.decode(" ".join(L), "ulatex").replace(" ", "+")

        params = {"query": payload, "rows": 2}  # max number of results

        crossref_types = _bibtex_to_crossref_type(entry.type)
        if crossref_types:
            params["filter"] = ",".join("type:{}".format(ct) for ct in crossref_types)

        # crossref etiquette,
        # <https://github.com/CrossRef/rest-api-doc#good-manners--more-reliable-service>
        headers = {
            "User-Agent": "betterbib/{} ({}; mailto:{})".format(
                __version__, __website__, __author_email__
            )
        }

        r = requests.get(self.api_url, params=params, headers=headers)
        if not r.ok:
            raise HttpError("Failed request to {}".format(self.api_url))

        results = r.json()["message"]["items"]

        if not results:
            raise NotFoundError("No match")

        if len(results) == 1:
            return self._crossref_to_pybtex(results[0])

        return self._crossref_to_pybtex(heuristic_unique_result(results, d))

    def _crossref_to_pybtex(self, data):
        """Translate a given data set into the bibtex data structure.
        """
        # A typcial search result is
        #
        # {
        #   u'DOI': u'10.1137/110820713',
        #   u'subtitle': [],
        #   u'issued': {u'date-parts': [[2013, 4, 4]]},
        #   u'prefix': u'http://id.crossref.org/prefix/10.1137',
        #   u'author': [
        #     {u'affiliation': [], u'given': u'Andr\xe9', u'family': u'Gaul'},
        #     {u'affiliation': [], u'given': u'Martin', u'family': u'Gut'},
        #     {u'affiliation': [], u'given': u'J\xf6rg', u'family': u'Liesen'},
        #     {u'affiliation': [], u'given': u'Reinhard', u'family': u'Nabben'}
        #   ],
        #   u'reference-count': 55,
        #   u'ISSN': [u'0895-4798', u'1095-7162'],
        #   u'member': u'http://id.crossref.org/member/351',
        #   u'source': u'Crossref',
        #   u'score': 3.3665228,
        #   u'deposited': {
        #     u'timestamp': 1372345787000,
        #     u'date-time': u'2013-06-27T15:09:47Z',
        #     u'date-parts': [[2013, 6, 27]]
        #   },
        #   u'indexed': {
        #     u'timestamp': 1442739318395,
        #     u'date-time': u'2015-09-20T08:55:18Z',
        #     u'date-parts': [[2015, 9, 20]]
        #   },
        #   u'type': u'journal-article',
        #   u'URL': u'http://dx.doi.org/10.1137/110820713',
        #   u'volume': u'34',
        #   u'publisher': u'Soc. for Industrial & Applied Mathematics (SIAM)',
        #   u'created': {
        #     u'timestamp': 1368554571000,
        #     u'date-time': u'2013-05-14T18:02:51Z',
        #     u'date-parts': [[2013, 5, 14]]
        #   },
        #   u'issue': u'2',
        #   u'title': [u'A Framework for Deflated Krylov Subspace Methods'],
        #   u'alternative-id': [u'10.1137/110820713'],
        #   u'container-title': [
        #     u'SIAM. J. Matrix Anal. & Appl.',
        #     u'SIAM Journal on Matrix Analysis and Applications'
        #   ],
        #   u'page': u'495-518'
        # }
        #
        fields_dict = {}

        pairs = {
            "doi": "DOI",
            "number": "issue",
            "pages": "page",
            "source": "source",
            "url": "URL",
            "volume": "volume",
        }
        for key1, key2 in pairs.items():
            try:
                fields_dict[key1] = data[key2]
            except KeyError:
                pass

        container_title = None
        keys = ["short-container-title", "container-title"]
        if self.prefer_long_journal_name:
            keys = reversed(keys)
        for key in keys:
            if key in data and data[key]:
                container_title = data[key][0]
                break

        try:
            title = data["title"][0]
        except (KeyError, IndexError):
            title = None

        try:
            publisher = data["publisher"]
        except KeyError:
            publisher = None

        # translate the type
        bibtex_type = self._crossref_to_bibtex_type(data)
        if bibtex_type == "article":
            if container_title:
                fields_dict["journal"] = container_title
            if publisher:
                fields_dict["publisher"] = publisher
            if title:
                fields_dict["title"] = title
        elif bibtex_type == "book":
            if publisher:
                fields_dict["publisher"] = publisher
            if title:
                fields_dict["title"] = title
        elif bibtex_type == "inbook":
            if container_title:
                # or title?
                fields_dict["booktitle"] = container_title
            if publisher:
                fields_dict["publisher"] = publisher
            if title:
                fields_dict["chapter"] = title
        elif bibtex_type == "incollection":
            if container_title:
                fields_dict["booktitle"] = container_title
            if publisher:
                fields_dict["publisher"] = publisher
            if title:
                fields_dict["title"] = title
        elif bibtex_type == "inproceedings":
            if container_title:
                fields_dict["booktitle"] = container_title
            if publisher:
                fields_dict["publisher"] = publisher
            if title:
                fields_dict["title"] = title
        elif bibtex_type == "proceedings":
            if publisher:
                fields_dict["publisher"] = publisher
            if title:
                fields_dict["title"] = title
        elif bibtex_type == "techreport":
            if publisher:
                fields_dict["institution"] = publisher
            if title:
                fields_dict["title"] = title
        else:
            assert bibtex_type == "misc", "Unknown type '{}'".format(bibtex_type)
            if publisher:
                fields_dict["publisher"] = publisher
            # Standards have the title in container_title
            if title:
                fields_dict["title"] = title
            elif container_title:
                fields_dict["title"] = container_title

        try:
            if data["subtitle"][0]:
                fields_dict["subtitle"] = data["subtitle"][0]
        except (KeyError, IndexError):
            pass

        try:
            fields_dict["issn"] = ", ".join(data["ISSN"])
        except KeyError:
            pass

        try:
            fields_dict["isbn"] = ", ".join(data["ISBN"])
        except KeyError:
            pass

        try:
            year = data["issued"]["date-parts"][0][0]
            if year is not None:
                fields_dict["year"] = year
        except (KeyError, IndexError):
            pass

        try:
            month = data["issued"]["date-parts"][0][1]
            if month is not None:
                fields_dict["month"] = month
        except (IndexError, KeyError):
            pass

        try:
            persons = {
                "author": [
                    pybtex.database.Person(u"{}, {}".format(au["family"], au["given"]))
                    for au in data["author"]
                ]
            }
        except (KeyError, pybtex.database.InvalidNameString):
            persons = None

        return pybtex.database.Entry(bibtex_type, fields=fields_dict, persons=persons)
