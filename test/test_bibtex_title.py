# -*- coding: utf-8 -*-
#
import betterbib


def test():
    assert betterbib.bibtex._translate_title(
        'The Magnus expansion and some of its applications'
        ) == \
        'The {Magnus} expansion and some of its applications'

    assert betterbib.bibtex._translate_title(
        'VODE: a variable-coefficient ODE solver'
        ) == \
        '{VODE:} {A} variable-coefficient {ODE} solver'

    assert betterbib.bibtex._translate_title(
        'Peano\'s kernel theorem for vector-valued functions'
        ) == \
        '{Peano\'s} kernel theorem for vector-valued functions'

    assert betterbib.bibtex._translate_title(
        'Exponential Runge-Kutta methods for parabolic problems'
        ) == \
        'Exponential {Runge}-{Kutta} methods for parabolic problems'

    assert betterbib.bibtex._translate_title(
        'GMRES: A generalized minimal residual algorithm'
        ) == \
        '{GMRES:} {A} generalized minimal residual algorithm'

    assert betterbib.bibtex._translate_title(
        'On generalized averaged Gaussian formulas, II'
        ) == \
        'On generalized averaged {Gaussian} formulas, {II}'

    assert betterbib.bibtex._translate_title(
        'Gaussian Hermitian Jacobian'
        ) == \
        '{Gaussian} {Hermitian} {Jacobian}'
    return
