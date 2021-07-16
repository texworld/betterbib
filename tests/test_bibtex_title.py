import betterbib


def test_translate_title_capitalized():
    assert (
        betterbib.tools._translate_title(
            "The Magnus expansion and some of its applications"
        )
        == "The {Magnus} expansion and some of its applications"
    )

    assert (
        betterbib.tools._translate_title(
            "On generalized averaged Gaussian formulas, II"
        )
        == "On generalized averaged {Gaussian} formulas, {II}"
    )

    assert (
        betterbib.tools._translate_title("Gaussian Hermitian Jacobian")
        == "{Gaussian} {Hermitian} {Jacobian}"
    )


def test_translate_title_ACRONYM():
    assert (
        betterbib.tools._translate_title("VODE: a variable-coefficient ODE solver")
        == "{VODE:} {A} variable-coefficient {ODE} solver"
    )

    assert (
        betterbib.tools._translate_title(
            "GMRES: A generalized minimal residual algorithm"
        )
        == "{GMRES:} {A} generalized minimal residual algorithm"
    )


def test_translate_title_apostrophe():
    assert (
        betterbib.tools._translate_title(
            "Peano's kernel theorem for vector-valued functions"
        )
        == "{Peano's} kernel theorem for vector-valued functions"
    )


def test_translate_title_dashed_names():
    assert (
        betterbib.tools._translate_title(
            "Exponential Runge-Kutta methods for parabolic problems"
        )
        == "Exponential {Runge}-{Kutta} methods for parabolic problems"
    )


def test_translate_title_dashes():
    assert (
        betterbib.tools._translate_title("Dash-Dash Double--Dash Triple---Dash")
        == "Dash-Dash Double--Dash Triple---Dash"
    )


def test_translate_title_variable():
    assert betterbib.tools._translate_title("x: {X}") == "x: {X}"


def test_translate_title_escape_dollar():
    assert (
        betterbib.tools._translate_title("{Aaa ${\\text{Pt/Co/AlO}}_{x}$ aaa bbb}")
        == "{Aaa {${\\text{Pt/Co/AlO}}_{x}$} aaa bbb}"
    )


def test_translate_title_star():
    assert betterbib.tools._translate_title("z*") == "z*"
