import concurrent.futures

from rich.progress import track

from . import crossref, dblp, errors, tools


def sync(
    d: dict, source: str, long_journal_name: bool, max_workers: int, verbose: bool
):
    """
    Sync a bibtex dict with an external source

        Parameters:
            d (dict): bibtex dict
            source (str): data source to sync against
            long_journal_name (bool): use the long journal name instead of short
            max_workers (int): number of concurrent workers to use
            verbose (bool): print additional information to stdout

        Returns:
            synced dict
    """

    if source == "crossref":
        source = crossref.Crossref(long_journal_name)
    else:
        assert source == "dblp", "Illegal source."
        source = dblp.Dblp()

    num_success = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        responses = {
            executor.submit(source.find_unique, entry): (bib_id, tools.decode(entry))
            for bib_id, entry in d.items()
        }
        for future in track(
            concurrent.futures.as_completed(responses),
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
                d[bib_id] = tools.update(entry, data)
    if verbose:
        print(f"\n\nTotal number of entries: {len(d)}")
        print(f"Found: {num_success}")

    return d
