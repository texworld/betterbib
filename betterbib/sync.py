import concurrent.futures

from rich.progress import track

from . import crossref, dblp, errors, tools


def sync(d, source, long_journal_name, max_workers):
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

    print(f"\n\nTotal number of entries: {len(d)}")
    print(f"Found: {num_success}")
    return d
