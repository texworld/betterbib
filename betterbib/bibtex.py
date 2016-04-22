# -*- coding: utf-8 -*-
#
from pybtex.database.input import bibtex
import subprocess


def latex_to_unicode(latex_string):
    '''Convert a LaTeX string to unicode.
    '''
    # Use pandoc for the job
    try:
        # This works in Python 3.4+
        return subprocess.check_output(
            ['pandoc', '-f', 'latex', '-t', 'plain'],
            input=latex_string,
            universal_newlines=True
            )
    except TypeError:  # unexpected keyword 'input'
        p = subprocess.Popen(
            ['pandoc', '-f', 'latex', '-t', 'plain'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        stdout, _ = p.communicate(latex_string.encode('utf-8'))
        return stdout.replace('\n', ' ').strip().decode('utf-8')


def pybtex_to_dict(entry):
    '''String representation of BibTeX entry.
    '''
    d = {}
    d['genre'] = entry.type
    for key, persons in entry.persons.items():
        d[key.lower()] = [{
            'first': p.first(),
            'middle': p.middle(),
            'prelast': p.prelast(),
            'last': p.last(),
            'lineage': p.lineage()
            } for p in persons]
    for field, value in entry.fields.iteritems():
        d[field.lower()] = value
    return d


def _translate_month(month):
    '''The month value can take weird forms. Sometimes, it's given as an int,
    sometimes as a string representing an int, and sometimes the name of the
    month is spelled out. Try to handle most of this here.
    '''
    try:
        index_to_month = {
            1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun',
            7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'
            }
        return index_to_month[int(month)]
    except ValueError:
        # ValueError: invalid literal for int() with base 10: 'Nov'
        pass

    month = month[:3].lower()
    assert(month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
                     'aug', 'sep', 'nov', 'dec'])
    return month


def pybtex_to_bibtex_string(entry, key):
    '''String representation of BibTeX entry.
    '''
    out = '@%s{%s,\n  ' % (entry.type, key)
    content = []
    for key, persons in entry.persons.items():
        persons_str = ' and '.join([_get_person_str(p) for p in persons])
        content.append('%s = {%s}' % (key, persons_str))
    for field, value in entry.fields.iteritems():
        if field == 'month':
            content.append('%s = %s' % (field, _translate_month(value)))
        else:
            content.append('%s = {%s}' % (field, value))
    out += ',\n  '.join(content)
    out += '\n}'
    return out


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
