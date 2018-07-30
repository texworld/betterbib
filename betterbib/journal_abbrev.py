# -*- coding: utf-8 -*-
#
import json
import os


def journal_abbrev(d, long_journal_names=False):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(this_dir, "data/journals.json"), "r") as f:
        table = json.load(f)

    if long_journal_names:
        table = {v: k for k, v in table.items()}

    for value in d.values():
        try:
            value.fields["journal"] = table[value.fields["journal"]]
        except KeyError:
            pass

    return d
