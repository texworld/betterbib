# -*- coding: utf-8 -*-
#
import betterbib

import pybtex
import pybtex.database


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

    assert betterbib.pybtex_to_bibtex_string(merged, 'key') \
        == betterbib.pybtex_to_bibtex_string(reference, 'key')

    return
