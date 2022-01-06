from __future__ import annotations

from typing import Callable

from pybtex.database import Entry

from . import tools


def adapt_doi_urls(d: dict[str, Entry], doi_url_type: str) -> None:
    if doi_url_type == "new":
        _update_doi_url(d, lambda doi: f"https://doi.org/{doi}")

    elif doi_url_type == "short":

        def update_to_short_doi(doi: str) -> str | None:
            short_doi = tools.get_short_doi(doi)
            if short_doi:
                return f"https://doi.org/{short_doi}"
            return None

        _update_doi_url(d, update_to_short_doi)

    else:
        assert doi_url_type == "unchanged"


def _update_doi_url(d: dict[str, Entry], url_from_doi: Callable[[str], str]) -> None:
    for bib_id, value in d:
        if "url" not in value.fields:
            continue

        doi = tools.doi_from_url(value.fields["url"])
        if doi:
            new_url = url_from_doi(doi)
            if new_url:
                d[bib_id].fields["url"] = new_url
