import pytest

import betterbib


@pytest.mark.parametrize(
    "string,ref",
    [
        (
            "The Magnus expansion and some of its applications",
            "The {Magnus} expansion and some of its applications",
        ),
        (
            "On generalized averaged Gaussian formulas, II",
            "On generalized averaged {Gaussian} formulas, {II}",
        ),
        ("Gaussian Hermitian Jacobian", "{Gaussian} {Hermitian} {Jacobian}"),
        (
            "VODE: a variable-coefficient ODE solver",
            "{VODE:} {A} variable-coefficient {ODE} solver",
        ),
        (
            "GMRES: A generalized minimal residual algorithm",
            "{GMRES:} {A} generalized minimal residual algorithm",
        ),
        (
            "Peano's kernel theorem for vector-valued functions",
            "{Peano's} kernel theorem for vector-valued functions",
        ),
        (
            "Exponential Runge-Kutta methods for parabolic problems",
            "Exponential {Runge}-{Kutta} methods for parabolic problems",
        ),
        (
            "Dash-Dash Double--Dash Triple---Dash",
            "Dash-Dash Double--Dash Triple---Dash",
        ),
        ("x: {X}", "x: {X}"),
        (
            "{Aaa ${\\text{Pt/Co/AlO}}_{x}$ aaa bbb}",
            "{Aaa {${\\text{Pt/Co/AlO}}_{x}$} aaa bbb}",
        ),
        ("z*", "z*"),
    ],
)
def test_translate_title(string, ref):
    assert betterbib.tools._translate_title(string) == ref
