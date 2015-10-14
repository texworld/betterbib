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


def _get_maps():
    import xml.etree.ElementTree
    tree = xml.etree.ElementTree.parse('unicode.xml')
    root = tree.getroot()

    u2l = {}
    l2u = {}
    for char in root.iter('character'):
        try:
            uni = unichr(int(char.attrib['dec'])).encode('utf-8')
            for sub in char.iter('latex'):
                lat = sub.text
                u2l[uni] = lat
                l2u[lat] = uni
        except ValueError:
            pass
    return u2l, l2u


def _preprocess_latex(s):
    # list: https://en.wikibooks.org/wiki/LaTeX/Special_Characters
    import re
    return re.sub(r'\\([\'"`\^\~=\.])([a-zA-Z])',
                  r'\\\1{\2}',
                  s)
