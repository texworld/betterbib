from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from pybtex.database import Entry
from rich.progress import track

from . import crossref, dblp, errors, tools
from .journal_abbrev import journal_abbrev


def sync(
    d: dict[str, Entry],
    source: str,
    long_journal_names: bool,
    max_workers: int,
    verbose: bool,
) -> dict[str, Entry]:
    """
    Sync a bibtex dict with an external source

        Parameters:
            d (dict): bibtex dict
            source (str): data source to sync against
            long_journal_names (bool): use the long journal name instead of short
            max_workers (int): number of concurrent workers to use
            verbose (bool): print additional information to stdout

        Returns:
            synced dict
    """

    if source == "crossref":
        src = crossref.Crossref()
    else:
        assert source == "dblp", "Illegal source."
        src = dblp.Dblp()

    num_success = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        responses = {
            executor.submit(src.find_unique, entry): (bib_id, tools.decode(entry))
            for bib_id, entry in d.items()
        }
        for future in track(
            as_completed(responses),
            total=len(responses),
            description="Syncing...",
            disable=not verbose,
        ):
            bib_id, entry = responses[future]
            try:
                data = future.result()
            except (errors.NotFoundError, errors.UniqueError):
                pass
            except errors.HttpError as e:
                print(e.args[0])
            else:
                num_success += 1
                d[bib_id] = tools.merge(entry, data)

    # (un)abbreviate journal names
    journal_abbrev(d, long_journal_names)

    if verbose:
        print(f"\n\nTotal number of entries: {len(d)}")
        print(f"Found: {num_success}")

    return d
