# -*- coding: utf8 -*-
#
from pybtex.database.input import bibtex


def get_string_representation(entry):
    '''String representation of BibTeX entry.
    '''
    lst = []
    lst.append('@%s{%s' % (entry.type, entry.key))
    for key, persons in entry.persons.items():
        persons_str = ' and '.join([_get_person_str(p) for p in persons])
        lst.append('%s = {%s}' % (key, persons_str))
    for field, value in entry.fields.iteritems():
        lst.append('%s = {%s}' % (field, value))
    lst.append('}')
    return ',\n  '.join(lst)


def _get_person_str(p):
    person_str = []
    for s in [' '.join(p.prelast() + p.last()),
              ' '.join(p.lineage()),
              ' '.join(p.first() + p.middle())]:
        if s:
            person_str.append(s)
    return ', '.join(person_str)


def read_bibtex(filename):
    # Open file for parsing.
    parser = bibtex.Parser()
    data = parser.parse_file(filename)
    return data
