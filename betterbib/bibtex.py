# -*- coding: utf-8 -*-
#
from __future__ import print_function

import re

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


def _translate_month(key):
    '''The month value can take weird forms. Sometimes, it's given as an int,
    sometimes as a string representing an int, and sometimes the name of the
    month is spelled out. Try to handle most of this here.
    '''
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
              'aug', 'sep', 'oct', 'nov', 'dec']
    try:
        return months[key-1]
    except TypeError:
        # TypeError: unsupported operand type(s) for -: 'str' and 'int'
        pass

    month = key[:3].lower()

    # Month values like '????' appear -- skip them
    if month not in months:
        print('Unknown month value \'{}\'. Skipping.'.format(key))
        return None

    return month


_names = [
    'Abrikosov',
    'Arnoldi',
    'Banach',
    'Bernstein',
    'Bose',
    'Cauchy',
    'Caputo',
    'Chebyshev',
    'Davidson',
    'Einstein',
    'Euler',
    'Fourier',
    'Galerkin',
    'Gauss',
    'Gross',
    'Ginzburg',
    'Hermite',
    'Jacobi',
    'Jordan',
    'Kronrod',
    'Krylov',
    'Kutta',
    'Landau',
    'Laplace',
    'Magnus',
    'Navier',
    'Lanczos',
    'Lie',
    'Magnus',
    'Neumann',
    'Newton',
    'Peano',
    'Pitaevskii',
    'Richardson',
    'Ritz',
    'Runge',
    u'Schrödinger',
    'Schur',
    'Stokes',
    'Sylvester',
    'Toeplitz',
    #
    'I',
    'II',
    'III',
    'IV',
    'V',
    'VI',
    'VII',
    'VIII',
    'IX',
    'X'
    ]


def _translate_word(word):
    # Check if the word has a capital letter in a position other than
    # the first. If yes, protect it.
    if not word:
        out = word
    elif word[0] == '{' and word[-1] == '}':
        out = word
    elif any(char.isupper() for char in word[1:]):
        out = '{' + word + '}'
    elif word in _names:
        # Einstein
        out = '{' + word + '}'
    elif len(word) > 2 and word[-2:] == '\'s' and word[:-2] in _names:
        # Peano's
        out = '{' + word + '}'
    elif len(word) > 3 and word[-3:] == 'ian' and word[:-3] in _names:
        # Gaussian
        out = '{' + word + '}'
    elif len(word) > 3 and word[-3:] == 'ian' and word[:-3] + 'e' in _names:
        # Laplacian
        out = '{' + word + '}'
    elif len(word) > 3 and word[-3:] == 'ian' and word[:-2] in _names:
        # Jacobian
        out = '{' + word + '}'
    else:
        out = word
    return out


def _translate_title(val):
    '''The capitalization of BibTeX entries is handled by the style, so names
    (Newton) or abbreviations (GMRES) may not be capitalized. This is unless
    they are wrapped in curly brackets.
    This function takes a raw title string as input and {}-protects those parts
    whose capitalization should not change.
    '''
    words = val.split()
    # pylint: disable=consider-using-enumerate
    for k in range(len(words)):
        if k > 0 and words[k-1][-1] == ':':
            # Algorithm 694: {A} collection...
            words[k] = '{' + words[k].capitalize() + '}'

    for k in range(len(words)):
        words[k] = '-'.join([_translate_word(w) for w in words[k].split('-')])

    return ' '.join(words)


# pylint: disable=too-many-locals
def pybtex_to_bibtex_string(entry, bibtex_key, bracket_delimeters=True):
    '''String representation of BibTeX entry.
    '''
    out = '@{}{{{},\n '.format(entry.type, bibtex_key)
    content = []

    left, right = ['{', '}'] if bracket_delimeters else ['"', '"']

    for key, persons in entry.persons.items():
        persons_str = ' and '.join([_get_person_str(p) for p in persons])
        content.append(u'{} = {}{}{}'.format(key, left, persons_str, right))

    # Make sure the fields always come out in the same order
    sorted_fields = sorted(entry.fields.keys())
    for field in sorted_fields:
        value = entry.fields[field]
        if field == 'month':
            month_string = _translate_month(value)
            if month_string:
                content.append('month = {}'.format(month_string))
        elif field == 'title':
            content.append(u'title = {}{}{}'.format(
                left, _translate_title(value), right
                ))
        else:
            content.append(u'{} = {}{}{}'.format(field, left, value, right))

    # Make sure that every line ends with a comma
    out += ' '.join([line + ',\n' for line in content])
    out += '}'
    return out


def doi_from_url(url):
    '''See if this is a DOI URL and return the DOI.
    '''
    m = re.match('https?://(?:dx\\.)?doi\\.org/(.*)', url)
    if m:
        return m.group(1)
    return None


def _get_person_str(p):
    person_str = []
    for s in [' '.join(p.prelast() + p.last()),
              ' '.join(p.lineage()),
              ' '.join(p.first() + p.middle())]:
        if s:
            person_str.append(s)
    return ', '.join(person_str)
