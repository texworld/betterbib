# -*- coding: utf-8 -*-
#
import betterbib


# pylint: disable=protected-access
def test():
    assert betterbib.tools._translate_title(
        'The Magnus expansion and some of its applications'
        ) == \
        'The {Magnus} expansion and some of its applications'

    assert betterbib.tools._translate_title(
        'VODE: a variable-coefficient ODE solver'
        ) == \
        '{VODE:} {A} variable-coefficient {ODE} solver'

    assert betterbib.tools._translate_title(
        'Peano\'s kernel theorem for vector-valued functions'
        ) == \
        '{Peano\'s} kernel theorem for vector-valued functions'

    assert betterbib.tools._translate_title(
        'Exponential Runge-Kutta methods for parabolic problems'
        ) == \
        'Exponential {Runge}-{Kutta} methods for parabolic problems'

    assert betterbib.tools._translate_title(
        'GMRES: A generalized minimal residual algorithm'
        ) == \
        '{GMRES:} {A} generalized minimal residual algorithm'

    assert betterbib.tools._translate_title(
        'On generalized averaged Gaussian formulas, II'
        ) == \
        'On generalized averaged {Gaussian} formulas, {II}'

    assert betterbib.tools._translate_title(
        'Gaussian Hermitian Jacobian'
        ) == \
        '{Gaussian} {Hermitian} {Jacobian}'

    assert betterbib.tools._translate_title(
        'Dash-Dash Double--Dash Triple---Dash'
        ) == \
        'Dash-Dash Double--Dash Triple---Dash'

    assert betterbib.tools._translate_title(
        'x: {X}'
        ) == \
        'x: {X}'
    return


def test_brackets():
    title = '{Aaa ${\\text{Pt/Co/AlO}}_{x}$ aaa bbb}'
    ref = '{Aaa {${\\text{Pt/Co/AlO}}_{x}$} aaa bbb}'
    out = betterbib.tools._translate_title(title)
    assert out == ref
    return
