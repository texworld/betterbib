# -*- coding: utf-8 -*-
#
import pybtex
import pybtex.database

import betterbib


def test_update():

    entry1 = pybtex.database.Entry(
        'article',
        fields={
            'title': 'Yes',
            'year': 2000,
            },
        persons={'author': [pybtex.database.Person('Doe, John')]}
        )
    entry2 = pybtex.database.Entry(
        'book',
        fields={
            'title': 'No',
            'pages': '1-19',
            },
        persons={'author': [pybtex.database.Person('Doe, John')]}
        )
    reference = pybtex.database.Entry(
        'book',
        fields={
            'title': 'No',
            'year': 2000,
            'pages': '1-19',
            },
        persons={'author': [pybtex.database.Person('Doe, John')]}
        )

    merged = betterbib.update(entry1, entry2)

    assert betterbib.pybtex_to_bibtex_string(merged, 'key', sort=True) \
        == betterbib.pybtex_to_bibtex_string(reference, 'key', sort=True)

    return


def test_journal_name():
    shrt = pybtex.database.Entry(
        'article',
        fields={'journal': u'SIAM J. Matrix Anal. Appl.'}
        )
    lng = pybtex.database.Entry(
        'article',
        fields={'journal': u'SIAM Journal on Matrix Analysis and Applications'}
        )

    tmp = lng
    updater = betterbib.JournalNameUpdater()
    updater.update(tmp)
    assert tmp.fields['journal'] == shrt.fields['journal']

    lng = pybtex.database.Entry(
        'article',
        fields={'journal': u'SIAM Journal on Matrix Analysis and Applications'}
        )
    tmp = shrt
    updater = betterbib.JournalNameUpdater(long_journal_names=True)
    updater.update(tmp)
    assert tmp.fields['journal'] == lng.fields['journal']
    return
