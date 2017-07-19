# -*- coding: utf-8 -*-
#
import pypandoc


def latex_to_unicode(latex_string):
    '''Convert a LaTeX string to unicode.
    '''
    return pypandoc.convert_text(latex_string, 'plain', format='latex')


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
                     'aug', 'sep', 'oct', 'nov', 'dec'])
    return month


_names = [
    'Arnoldi',
    'Chebyshev',
    'Krylov',
    'Kutta'
    'Magnus',
    'Lanczos',
    'Newton',
    'Peano',
    'Ritz',
    'Runge',
    'Sylvester',
    ]


def _translate_title(val):
    '''The capitalization of BibTeX entries is handled by the style, so names
    (Newton) or abbreviations (GMRES) may not be capitalized. This is unless
    they are wrapped in curly brackets.
    This function takes a raw title string as input and {}-protects those parts
    whose capitalization should not change.
    '''
    words = val.split()
    for k in range(len(words)):
        # Check if the word has a capital letter in a position other than the
        # first. If yes, protect it.
        if any(char.isupper() for char in words[k][1:]) \
                or words[k] in _names:
            words[k] = '{%s}' % words[k]
        elif k > 0 and words[k-1][-1] == ':':
            # Algorithm 694: {A} collection...
            words[k] = '{%s}' % words[k].capitalize()

    return ' '.join(words)


def pybtex_to_bibtex_string(entry, bibtex_key):
    '''String representation of BibTeX entry.
    '''
    out = '@%s{%s,\n  ' % (entry.type, bibtex_key)
    content = []
    for key, persons in entry.persons.items():
        persons_str = ' and '.join([_get_person_str(p) for p in persons])
        content.append('%s = {%s}' % (key, persons_str))
    for field, value in entry.fields.iteritems():
        if field == 'month':
            content.append('month = %s' % _translate_month(value))
        elif field == 'title':
            content.append('title = {%s}' % _translate_title(value))
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
