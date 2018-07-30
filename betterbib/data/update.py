#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""This tool is used for converting JabRef's journal name abbreviation files,
<https://github.com/JabRef/jabref/tree/master/src/main/resources/journals>,
into JSON.

Usage example:
```
python3 update.py
```
"""
import argparse

import json
import requests


def _main():
    _parse_cmd_arguments()

    urls = [
        "https://raw.githubusercontent.com/JabRef/jabref/master/src/main/resources/journals/IEEEJournalListText.txt",
        "https://raw.githubusercontent.com/JabRef/jabref/master/src/main/resources/journals/journalList.txt",
    ]

    out = {}
    for url in urls:
        r = requests.get(url)

        assert r.status_code == 200

        # read input file into dictionary
        for line in r.text.split("\n"):
            sline = line.strip()
            if sline is None:
                break
            if len(sline) == 0 or sline[0] == "#":
                continue
            k, v = sline.split("=")
            out[k.strip()] = v.strip()

    with open("journals.json", "w") as f:
        json.dump(out, f, indent=2)
    return


def _parse_cmd_arguments():
    parser = argparse.ArgumentParser(description="Update journals.json.")
    return parser.parse_args()


if __name__ == "__main__":
    _main()
