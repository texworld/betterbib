import codecs

import pybtex
import pybtex.database
import requests
import requests_cache

from .errors import HttpError, NotFoundError
from .tools import heuristic_unique_result, pybtex_to_dict


def _to_bibtex_type(entry):
    # The difficulty here: Translating book-chapter. If the book is a
    # monograph (all chapters written by the same set of authors), then
    # return inbook, if all chapters are by different authors, return
    # incollection.
    assert entry["type"] == "Journal Articles"
    return "article"


def _dblp_to_pybtex(data):
    """Translate a given data set into the bibtex data structure.
    """
    # A typcial search result is
    #
    #   'info': {
    #       'authors': {'author': [
    #                      'André Gaul',
    #                      'Martin H. Gutknecht',
    #                      'Jörg Liesen',
    #                      'Reinhard Nabben'
    #                      ]},
    #    'doi': '10.1137/110820713',
    #    'ee': 'https://doi.org/10.1137/110820713',
    #    'key': 'journals/siammax/GaulGLN13',
    #    'number': '2',
    #    'pages': '495-518',
    #    'title': 'A Framework for Deflated and Augmented Krylov '
    #             'Subspace Methods.',
    #    'type': 'Journal Articles',
    #    'url': 'http://dblp.org/rec/journals/siammax/GaulGLN13',
    #    'venue': 'SIAM J. Matrix Analysis Applications',
    #    'volume': '34',
    #    'year': '2013'
    #    },
    #
    # translate the type
    bibtex_type = _to_bibtex_type(data)

    fields_dict = {}

    pairs = {
        "doi": "doi",
        "number": "number",
        "pages": "pages",
        "url": "ee",
        "volume": "volume",
        "year": "year",
    }
    for key1, key2 in pairs.items():
        try:
            fields_dict[key1] = data[key2]
        except KeyError:
            pass

    try:
        fields_dict["source"] = data["source"]
    except KeyError:
        fields_dict["source"] = "DBLP"

    try:
        container_title = data["venue"]
    except KeyError:
        container_title = None

    try:
        title = data["title"]
    except KeyError:
        title = None

    assert bibtex_type == "article"
    if container_title:
        fields_dict["journal"] = container_title
    if title:
        fields_dict["title"] = title

    try:
        authors = data["authors"]["author"]
        if isinstance(authors, dict):
            authors = [authors]
        persons = {"author": [pybtex.database.Person(au["text"]) for au in authors]}
    except (KeyError, pybtex.database.InvalidNameString):
        persons = None

    return pybtex.database.Entry(bibtex_type, fields=fields_dict, persons=persons)


class Dblp:
    """
    Documentation of the DBLP Search API:
    <http://dblp.uni-trier.de/faq/How+to+use+the+dblp+search+API.html>.
    """

    def __init__(self):
        self.api_url = "https://dblp.org/search/publ/api"

        requests_cache.install_cache("betterbib_cache", expire_after=3600)
        # requests_cache.remove_expired_responses()
        return

    def find_unique(self, entry):
        d = pybtex_to_dict(entry)

        # Be stingy on the search terms. DBLP search is not fuzzy, so one
        # misspelled word results in 0 hits.
        L = []

        try:
            L.append(d["title"])
        except KeyError:
            pass

        try:
            for au in d["author"]:
                L.append(" ".join(au["last"]))
        except KeyError:
            pass

        # kick out empty strings
        L = list(filter(None, L))

        # Simply plug the dict together to a search query. Typical query:
        # <api>?q=vanroose+schl%C3%B6mer&h=5
        payload = codecs.decode(" ".join(L), "ulatex").replace(" ", "+")

        params = {
            "q": payload,
            "format": "json",
            "h": 2,  # max number of results (hits)
        }

        r = requests.get(self.api_url, params=params)
        if not r.ok:
            raise HttpError("Failed request to {}".format(self.api_url))

        data = r.json()

        try:
            results = data["result"]["hits"]["hit"]
        except KeyError:
            raise NotFoundError("No match")

        if len(results) == 1:
            return _dblp_to_pybtex(results[0]["info"])

        return _dblp_to_pybtex(heuristic_unique_result(results, d)["info"])
