from . import tools


def adapt_doi_urls(d, doi_url_type):
    if doi_url_type == "new":
        d = _update_doi_url(d, lambda doi: "https://doi.org/" + doi)
    elif doi_url_type == "short":

        def update_to_short_doi(doi):
            short_doi = tools.get_short_doi(doi)
            if short_doi:
                return "https://doi.org/" + short_doi
            return None

        d = _update_doi_url(d, update_to_short_doi)
    else:
        assert doi_url_type == "unchanged"

    return d


def _update_doi_url(d, url_from_doi):
    for bib_id in d:
        if "url" in d[bib_id].fields:
            doi = tools.doi_from_url(d[bib_id].fields["url"])
            if doi:
                new_url = url_from_doi(doi)
                if new_url:
                    d[bib_id].fields["url"] = new_url
    return d
