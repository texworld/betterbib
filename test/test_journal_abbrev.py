import tempfile
from collections import namedtuple

import betterbib

FieldHolder = namedtuple("FieldHolder", "fields")

# the following are re-used in several tests
FULL_PNAS = (
    "Proceedings of the National academy of Sciences of the United States of America"
)
PNAS_ABBREV = "Proc. Natl. Acad. Sci. U.S.A."


def make_fake_entry(journal, citekey="foo"):
    contents = FieldHolder({"journal": journal})
    return {citekey: contents}


def test_standard_abbrev():
    journals = [FULL_PNAS]
    abbrevs = [PNAS_ABBREV]
    for journal, abbrev in zip(journals, abbrevs):
        entries = make_fake_entry(journal)
        abbreviated = betterbib.journal_abbrev(entries)
        assert abbreviated["foo"].fields["journal"] == abbrev


def test_custom_abbrev():
    infile = tempfile.NamedTemporaryFile().name
    super_short = '{"PNAS": "' + PNAS_ABBREV + '"}'
    with open(infile, "w") as f:
        f.write(super_short)

    entries = make_fake_entry("PNAS")
    abbreviated = betterbib.journal_abbrev(entries, custom_abbrev=infile)
    assert abbreviated["foo"].fields["journal"] == PNAS_ABBREV

    super_short = '{"' + FULL_PNAS + '": "PNAS"}'
    with open(infile, "w") as f:
        f.write(super_short)

    entries = make_fake_entry(FULL_PNAS)
    abbreviated = betterbib.journal_abbrev(entries, custom_abbrev=infile)
    assert abbreviated["foo"].fields["journal"] == "PNAS"


def test_standard_abbrev_long():
    journals = [FULL_PNAS]
    abbrevs = [PNAS_ABBREV]
    for journal, abbrev in zip(journals, abbrevs):
        entries = make_fake_entry(abbrev)
        abbreviated = betterbib.journal_abbrev(entries, long_journal_names=True)
        assert abbreviated["foo"].fields["journal"] == journal


def test_custom_abbrev_long():
    infile = tempfile.NamedTemporaryFile().name
    super_short = '{"' + FULL_PNAS + ': "PNAS"}'
    with open(infile, "w") as f:
        f.write(super_short)

    entries = make_fake_entry(PNAS_ABBREV)
    abbreviated = betterbib.journal_abbrev(entries, long_journal_names=True)
    assert abbreviated["foo"].fields["journal"] == FULL_PNAS
