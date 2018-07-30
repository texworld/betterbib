# -*- coding: utf-8 -*-
#
import collections
import concurrent.futures

from pybtex.database.input import bibtex
from tqdm import tqdm

from . import tools, crossref, dblp, errors


def sync(infile, outfile, source, long_journal_name, num_concurrent_requests):
    data = bibtex.Parser().parse_file(infile)

    # Use an ordered dictionary to make sure that the entries are written out
    # the way they came in.
    # data.entries.items() is a list of tuples, the first item being the BibTeX key.
    od = collections.OrderedDict(data.entries.items())
    od = tools.decode(od)

    if source == "crossref":
        source = crossref.Crossref(long_journal_name)
    else:
        assert source == "dblp", "Illegal source."
        source = dblp.Dblp()

    print()
    od, num_success = _update_from_source(od, source, num_concurrent_requests)

    print("\n\nTotal number of entries: {}".format(len(data.entries)))
    print("Found: {}".format(num_success))

    tools.write(od, outfile, "braces", tab_indent=False)
    return


def _update_from_source(od, source, num_concurrent_requests):
    num_success = 0
    # pylint: disable=bad-continuation
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=num_concurrent_requests
    ) as executor:
        responses = {
            executor.submit(source.find_unique, entry): (bib_id, entry)
            for bib_id, entry in od.items()
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

            od[bib_id] = tools.update(entry, data)

    return od, num_success
