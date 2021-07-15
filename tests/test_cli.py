import os
import tempfile

import betterbib


def test_cli_dedup_doi():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar}\n"
            "}"
        )

    betterbib.cli.dedup_doi(["--in-place", infile])
    with open(infile) as f:
        assert f.read() == (
            f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
            "\n"
            "\n"
            "@article{foobar,\n"
            " url = {https://doi.org/foobar},\n"
            "}\n"
        )
    os.remove(infile)


def test_cli_dedup_doi_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar}\n"
            "}"
        )

    betterbib.cli.dedup_doi([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{foobar,\n"
        " url = {https://doi.org/foobar},\n"
        "}\n"
    )
    os.remove(infile)


def test_cli_format():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar}\n"
            "}"
        )

    betterbib.cli.format(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == (
            f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
            "\n"
            "\n"
            "@article{foobar,\n"
            " doi = {foobar},\n"
            " url = {https://doi.org/foobar},\n"
            "}\n"
        )

    os.remove(infile)


def test_cli_format_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar}\n"
            "}"
        )

    betterbib.cli.format([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{foobar,\n"
        " doi = {foobar},\n"
        " url = {https://doi.org/foobar},\n"
        "}\n"
    )

    os.remove(infile)


def test_cli_journal_abbrev():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write("@article{foobar,\njournal={SIAM Journal on Scientific Computing}\n}")

    betterbib.cli.journal_abbrev(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == (
            f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
            "\n"
            "\n"
            "@article{foobar,\n"
            " journal = {SIAM J. Sci. Comput.},\n"
            "}\n"
        )

    os.remove(infile)


def test_cli_journal_abbrev_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write("@article{foobar,\njournal={SIAM Journal on Scientific Computing}\n}")

    betterbib.cli.journal_abbrev([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{foobar,\n"
        " journal = {SIAM J. Sci. Comput.},\n"
        "}\n"
    )

    os.remove(infile)


def test_cli_sync():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{stockman,\n"
            " author = {Stockman},\n"
            "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
            "}"
        )

    betterbib.cli.sync(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == (
            f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
            "\n"
            "\n"
            "@article{stockman,\n"
            " author = {Stockman, J.A.},\n"
            " title = {A New Equation to Estimate Glomerular Filtration Rate},\n"
            " doi = {10.1016/s0084-3954(09)79550-8},\n"
            " pages = {193-194},\n"
            " source = {Crossref},\n"
            " url = {http://dx.doi.org/10.1016/s0084-3954(09)79550-8},\n"
            " volume = {2011},\n"
            " journal = {Yearbook of Pediatrics},\n"
            " publisher = {Elsevier BV},\n"
            " issn = {0084-3954},\n"
            " year = {2011},\n"
            " month = jan,\n"
            "}\n"
        )
    os.remove(infile)


def test_cli_sync_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{stockman,\n"
            " author = {Stockman},\n"
            "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
            "}"
        )

    betterbib.cli.sync([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{stockman,\n"
        " author = {Stockman, J.A.},\n"
        " title = {A New Equation to Estimate Glomerular Filtration Rate},\n"
        " doi = {10.1016/s0084-3954(09)79550-8},\n"
        " pages = {193-194},\n"
        " source = {Crossref},\n"
        " url = {http://dx.doi.org/10.1016/s0084-3954(09)79550-8},\n"
        " volume = {2011},\n"
        " journal = {Yearbook of Pediatrics},\n"
        " publisher = {Elsevier BV},\n"
        " issn = {0084-3954},\n"
        " year = {2011},\n"
        " month = jan,\n"
        "}\n"
    )
    os.remove(infile)


def test_cli_doi2bibtex(capsys):
    betterbib.cli.doi2bibtex(["10.1016/s0084-3954(09)79550-8"])
    captured = capsys.readouterr()
    assert captured.out == "".join(
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{stockman2011,\n"
        " author = {Stockman, J.A.},\n"
        " doi = {10.1016/s0084-3954(09)79550-8},\n"
        " pages = {193-194},\n"
        " source = {Crossref},\n"
        " url = {http://dx.doi.org/10.1016/s0084-3954(09)79550-8},\n"
        " volume = {2011},\n"
        " journal = {Yearbook of Pediatrics},\n"
        " publisher = {Elsevier BV},\n"
        " title = {A New Equation to Estimate Glomerular Filtration Rate},\n"
        " issn = {0084-3954},\n"
        " year = {2011},\n"
        " month = jan,\n"
        "}\n"
    )


def test_cli_full():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{stockman,\n"
            " author = {Stockman},\n"
            "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
            "}"
        )

    betterbib.cli.full(["--in-place", infile])

    ref = (
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{stockman,\n"
        " author = {Stockman, J.A.},\n"
        " title = {A New Equation to Estimate Glomerular Filtration Rate},\n"
        " doi = {10.1016/s0084-3954(09)79550-8},\n"
        " pages = {193-194},\n"
        " source = {Crossref},\n"
        " url = {https://doi.org/10.1016/s0084-3954(09)79550-8},\n"
        " volume = {2011},\n"
        " journal = {Yearbook of Pediatrics},\n"
        " publisher = {Elsevier BV},\n"
        " issn = {0084-3954},\n"
        " year = {2011},\n"
        " month = jan,\n"
        "}\n"
    )

    with open(infile) as f:
        data = f.read()
        assert data == ref

    os.remove(infile)


def test_cli_full_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{stockman,\n"
            " author = {Stockman},\n"
            "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
            "}"
        )

    betterbib.cli.full([infile])
    captured = capsys.readouterr()

    ref = (
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{stockman,\n"
        " author = {Stockman, J.A.},\n"
        " title = {A New Equation to Estimate Glomerular Filtration Rate},\n"
        " doi = {10.1016/s0084-3954(09)79550-8},\n"
        " pages = {193-194},\n"
        " source = {Crossref},\n"
        " url = {https://doi.org/10.1016/s0084-3954(09)79550-8},\n"
        " volume = {2011},\n"
        " journal = {Yearbook of Pediatrics},\n"
        " publisher = {Elsevier BV},\n"
        " issn = {0084-3954},\n"
        " year = {2011},\n"
        " month = jan,\n"
        "}\n"
    )

    assert captured.out == "".join(ref)

    os.remove(infile)
