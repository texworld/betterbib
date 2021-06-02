import json
import os


def journal_abbrev(d, long_journal_names: bool = False, custom_abbrev=None):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(this_dir, "data/journals.json")) as f:
        table = json.load(f)

    if custom_abbrev is not None:
        with open(custom_abbrev) as f:
            custom_table = json.load(f)
    else:
        custom_table = {}

    if long_journal_names:
        custom_table = {v: k for k, v in custom_table.items()}
        table = {v: k for k, v in table.items()}

    table.update(custom_table)

    # fallback option
    table_keys_lower = {k.lower(): v for k, v in table.items()}

    for value in d.values():
        try:
            value.fields["journal"] = table[value.fields["journal"]]
        except KeyError:
            try:
                value.fields["journal"] = table_keys_lower[
                    value.fields["journal"].lower()
                ]
            except KeyError:
                pass

    return d
