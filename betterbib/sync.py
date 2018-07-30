# -*- coding: utf-8 -*-
#
import concurrent.futures

from tqdm import tqdm

from . import tools, crossref, dblp, errors


def sync(d, source, long_journal_name, max_workers):
    if source == "crossref":
        source = crossref.Crossref(long_journal_name)
    else:
        assert source == "dblp", "Illegal source."
        source = dblp.Dblp()

    print()
    num_success = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        responses = {
            executor.submit(source.find_unique, entry): (bib_id, entry)
            for bib_id, entry in d.items()
        }
        for future in tqdm(
            concurrent.futures.as_completed(responses), total=len(responses)
        ):
            bib_id, entry = responses[future]
            data = None
            try:
                data = future.result()
            except (errors.NotFoundError, errors.UniqueError):
                pass
            except errors.HttpError as e:
                print(e.args[0])
            else:
                num_success += 1

            d[bib_id] = tools.update(entry, data)

    print("\n\nTotal number of entries: {}".format(len(d)))
    print("Found: {}".format(num_success))

    return d
