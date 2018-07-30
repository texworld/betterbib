# -*- coding: utf-8 -*-
#
import json
import os


def journal_abbrev(d, long_journal_names):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(this_dir, "data/journals.json"), "r") as f:
        table = json.load(f)

    if long_journal_names:
        table = {v: k for k, v in table.items()}

    for value in d.values():
        try:
            journal_name = value.fields["journal"]
            value.fields["journal"] = table[journal_name]
        except KeyError:
            pass

    return d
