from __future__ import annotations

import json
from pathlib import Path

from pybtex.database import Entry


def journal_abbrev(
    d: dict[str, Entry],
    long_journal_names: bool = False,
    custom_abbrev: str | None = None,
) -> dict[str, Entry]:
    this_dir = Path(__file__).resolve().parent
    with open(this_dir / "data/journals.json") as f:
        table = json.load(f)

    if custom_abbrev is not None:
        with open(custom_abbrev) as f:
            table.update(json.load(f))

    if long_journal_names:
        table = {v: k for k, v in table.items()}

    # fallback option
    table_keys_lower = {k.lower(): v for k, v in table.items()}

    for value in d.values():
        if "journal" not in value.fields:
            continue

        journal = value.fields["journal"]
        try:
            value.fields["journal"] = table[journal]
        except KeyError:
            try:
                value.fields["journal"] = table_keys_lower[journal.lower()]
            except KeyError:
                pass

    return d
