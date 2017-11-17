# -*- coding: utf-8 -*-
#
from __future__ import print_function

import re
import requests

import enchant
import pypandoc

from .__about__ import __version__
from .errors import UniqueError


def latex_to_unicode(latex_string):
    '''Convert a LaTeX string to unicode.
    '''
    out = pypandoc.convert_text(latex_string, 'plain', format='latex')
    # replace multiple whitespace by one, remove surrounding spaces
    return ' '.join(out.split())


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


def create_dict():
    extra_names = [
        'Abrikosov',
        'Arnoldi',
        'Bergman',
        'Bernstein',
        'Bruijn',
        'Chebyshev',
        'Danilewski',
        'Darboux',
        'Pezzo',
        'Galerkin',
        'Ginzburg',
        'Goldbach',
        'Hermite', 'Hermitian',
        'Hopf',
        'Hopfield',
        'Jacobi', 'Jacobian',
        'Kronrod',
        'Krylov',
        'Kuratowski',
        'Kutta',
        'Liouville',
        'Magnus'
        'Manin',
        'Navier',
        'Kolmogorov',
        'Lanczos',
        'Magnus',
        'Peano',
        'Pell',
        'Pitaevskii',
        u'Pólya',
        'Ramanujan',
        'Ricatti',
        'Runge',
        'Scholz',
        'Schur',
        'Siebeck',
        'Sommerfeld',
        'Stieltjes',
        'Tausworthe',
        'Tchebycheff',
        'Toeplitz',
        'Voronoi',
        u'Voronoï',
        'Wieland',
        'Wronski', 'Wronskian',
        ]

    d = enchant.DictWithPWL('en_US')

    for name in extra_names:
        d.add(name)
        d.add(name + '\'s')
        if name[-1] == 's':
            d.add(name + '\'')

    for word in ['boolean', 'hermitian']:
        d.remove(word)

    return d


def _translate_word(word, d):
    # Check if the word needs to be protected by curly braces to prevent
    # recapitalization.
    if not word:
        needs_protection = False
    elif word[0] == '{' and word[-1] == '}':
        needs_protection = False
    elif any([char.isupper() for char in word[1:]]):
        needs_protection = True
    else:
        needs_protection = (
            any([char.isupper() for char in word]) and
            d.check(word) and not d.check(word.lower())
            )

    if needs_protection:
        return '{' + word + '}'
    return word


def _translate_title(val, dictionary=create_dict()):
    '''The capitalization of BibTeX entries is handled by the style, so names
    (Newton) or abbreviations (GMRES) may not be capitalized. This is unless
    they are wrapped in curly braces.
    This function takes a raw title string as input and {}-protects those parts
    whose capitalization should not change.
    '''
    # If the title is completely capitalized, it's probably by mistake.
    if val == val.upper():
        val = val.title()

    words = val.split()
    # pylint: disable=consider-using-enumerate
    # Handle colons as in
    # ```
    # Algorithm 694: {A} collection...
    # ```
    for k in range(len(words)):
        if k > 0 and words[k-1][-1] == ':' and words[k][0] != '{':
            words[k] = '{' + words[k].capitalize() + '}'

    for k in range(len(words)):
        words[k] = '-'.join([
            _translate_word(w, dictionary) for w in words[k].split('-')
            ])

    return ' '.join(words)


# pylint: disable=too-many-locals
def pybtex_to_bibtex_string(
        entry, bibtex_key,
        brace_delimeters=True,
        tab_indent=False,
        dictionary=create_dict(),
        sort=False
        ):
    '''String representation of BibTeX entry.
    '''

    indent = '\t' if tab_indent else ' '
    out = '@{}{{{},\n{}'.format(entry.type, bibtex_key, indent)
    content = []

    left, right = ['{', '}'] if brace_delimeters else ['"', '"']

    for key, persons in entry.persons.items():
        persons_str = ' and '.join([_get_person_str(p) for p in persons])
        content.append(u'{} = {}{}{}'.format(key, left, persons_str, right))

    keys = entry.fields.keys()
    if sort:
        keys = sorted(keys)

    for key in keys:
        value = entry.fields[key]
        if key == 'month':
            month_string = _translate_month(value)
            if month_string:
                content.append('month = {}'.format(month_string))
        elif key == 'title':
            content.append(u'title = {}{}{}'.format(
                left, _translate_title(value, dictionary), right
                ))
        else:
            if value is not None:
                content.append(
                    u'{} = {}{}{}'.format(key, left, value, right)
                    )

    # Make sure that every line ends with a comma
    out += indent.join([line + ',\n' for line in content])
    out += '}'
    return out


def doi_from_url(url):
    '''See if this is a DOI URL and return the DOI.
    '''
    m = re.match('https?://(?:dx\\.)?doi\\.org/(.*)', url)
    if m:
        return m.group(1)
    return None


def get_short_doi(doi):
    url = 'http://shortdoi.org/' + doi
    r = requests.get(url, params={'format': 'json'})
    if not r.ok:
        return None

    data = r.json()
    if 'ShortDOI' not in data:
        return None

    return data['ShortDOI']


def _get_person_str(p):
    out = ', '.join(filter(None, [
        ' '.join(p.prelast() + p.last()),
        ' '.join(p.lineage()),
        ' '.join(p.first() + p.middle())
        ]))

    # If the name is completely capitalized, it's probably by mistake.
    if out == out.upper():
        out = out.title()

    return out


def heuristic_unique_result(results, d):
    # Q: How to we find the correct solution if there's more than one
    #    search result?
    # As a heuristic, assume that the top result is the unique answer if
    # its score is at least 1.5 times the score of the the second-best
    # result.
    for score in 'score', '@score':
        try:
            if float(results[0][score]) > 1.5 * float(results[1][score]):
                return results[0]
        except KeyError:
            pass

    # If that doesn't work, check if the DOI matches exactly with the
    # input.
    if 'doi' in d:
        # sometimes, the doi field contains a doi url
        doi = doi_from_url(d['doi'])
        if not doi:
            doi = d['doi']
        for result in results:
            for doi_key in 'doi', 'DOI':
                try:
                    if result[doi_key].lower() == doi.lower():
                        return result
                except KeyError:
                    pass

    # If that doesn't work, check if the title appears in the input.
    if 'title' in d:
        for result in results:
            if 'title' in result and result['title'] and \
                    result['title'][0].lower() in d['title'].lower():
                return result

    # If that doesn't work, check if the page range matches exactly
    # with the input.
    if 'pages' in d:
        for result in results:
            if 'page' in result and result['page'] == d['pages']:
                return result

    # If that doesn't work, check if the second entry is a JSTOR copy
    # of the original article -- yes, that happens --, and take the
    # first one.
    if 'publisher' in results[1] and results[1]['publisher'] == 'JSTOR' \
            and 'title' in results[0] and 'title' in results[1] and \
            results[0]['title'][0].lower() == \
            results[1]['title'][0].lower():
        return results[0]

    raise UniqueError('Could not find a positively unique match.')


def write(od, file_handle, delimeter_type, tab_indent):
    # Write header to the output file.
    file_handle.write(
        '%comment{{This file was created with betterbib v{}.}}\n\n'
        .format(__version__)
        )

    # Create the dictionary only once
    dictionary = create_dict()

    # write the data out sequentially to respect ordering
    for bib_id, d in od.items():
        brace_delimeters = delimeter_type == 'braces'
        a = pybtex_to_bibtex_string(
            d, bib_id, brace_delimeters=brace_delimeters,
            tab_indent=tab_indent,
            dictionary=dictionary,
            )
        file_handle.write(a + '\n\n')
    return


def update(entry1, entry2):
    '''Create a merged BibTeX entry with the data from entry2 taking
    precedence.
    '''
    out = entry1
    if entry2 is not None:
        out.type = entry2.type
        out.persons = entry2.persons
        for key, value in entry2.fields.items():
            out.fields[key] = value
    return out
