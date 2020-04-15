"""This tool is used for converting JabRef's journal name abbreviation files,
<https://github.com/JabRef/jabref/tree/master/src/main/resources/journals>,
into JSON.

Usage example:
```
python3 update.py
```
"""
import argparse
import csv
import json

import requests


def _main():
    _parse_cmd_arguments()

    urls = [
        "https://raw.githubusercontent.com/JabRef/jabref/master/src/main/resources/journals/IEEEJournalListText.csv",
        "https://raw.githubusercontent.com/JabRef/jabref/master/src/main/resources/journals/journalList.csv",
    ]

    out = {}
    for url in urls:
        r = requests.get(url)

        assert r.status_code == 200

        # read input file into dictionary
        # only take the first two entries per row
        new = {
            item[0]: item[1] for item in csv.reader(r.text.splitlines(), delimiter=";")
        }
        # merge dicts
        out = {**out, **new}

    with open("journals.json", "w") as f:
        json.dump(out, f, indent=2)
    return


def _parse_cmd_arguments():
    parser = argparse.ArgumentParser(description="Update journals.json.")
    return parser.parse_args()


if __name__ == "__main__":
    _main()
