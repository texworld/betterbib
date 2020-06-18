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

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.dedup_doi([infile, outfile])
    with open(outfile, "r") as f:
        assert f.read() == (
            (
                "%comment{{This file was created with betterbib v{}.}}\n"
                "\n"
                "@article{{foobar,\n"
                " url = {{https://doi.org/foobar}},\n"
                "}}\n"
                "\n"
            ).format(betterbib.__version__)
        )
    os.remove(infile)
    os.remove(outfile)


def test_cli_format():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar}\n"
            "}"
        )

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.format([infile, outfile])

    with open(outfile, "r") as f:
        assert f.read() == (
            (
                "%comment{{This file was created with betterbib v{}.}}\n"
                "\n"
                "\n"
                "@article{{foobar,\n"
                " doi = {{foobar}},\n"
                " url = {{https://doi.org/foobar}},\n"
                "}}\n"
            ).format(betterbib.__version__)
        )

    os.remove(infile)
    os.remove(outfile)


def test_cli_journal_abbrev():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write("@article{foobar,\njournal={SIAM Journal on Scientific Computing}\n}")

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.journal_abbrev([infile, outfile])

    with open(outfile, "r") as f:
        assert f.read() == (
            (
                "%comment{{This file was created with betterbib v{}.}}\n"
                "\n"
                "\n"
                "@article{{foobar,\n"
                " journal = {{SIAM J. Sci. Comput.}},\n"
                "}}\n"
            ).format(betterbib.__version__)
        )

    os.remove(infile)
    os.remove(outfile)


def test_cli_sync():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{stockman,\n"
            " author = {Stockman},\n"
            "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
            "}"
        )

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.sync([infile, outfile])

    with open(outfile, "r") as f:
        assert f.read() == (
            (
                "%comment{{This file was created with betterbib v{}.}}\n"
                "\n"
                "\n"
                "@article{{stockman,\n"
                " author = {{Stockman, J.A.}},\n"
                " title = {{A New Equation to Estimate Glomerular Filtration Rate}},\n"
                " doi = {{10.1016/s0084-3954(09)79550-8}},\n"
                " pages = {{193-194}},\n"
                " source = {{Crossref}},\n"
                " url = {{http://dx.doi.org/10.1016/s0084-3954(09)79550-8}},\n"
                " volume = {{2011}},\n"
                " journal = {{Yearbook of Pediatrics}},\n"
                " publisher = {{Elsevier BV}},\n"
                " issn = {{0084-3954}},\n"
                " year = {{2011}},\n"
                " month = jan,\n"
                "}}\n"
            ).format(betterbib.__version__)
        )
    os.remove(infile)
    os.remove(outfile)


def test_cli_doit2bibtex():
    outfile = tempfile.NamedTemporaryFile().name
    betterbib.cli.doi2bibtex(["10.1016/s0084-3954(09)79550-8", outfile])
    with open(outfile, "r") as f:
        assert f.read() == (
            "@article{key,\n"
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
            "}"
        )
    os.remove(outfile)


def test_cli_full():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{stockman,\n"
            " author = {Stockman},\n"
            "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
            "}"
        )

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.full([infile, outfile])

    ref = (
        "%comment{{This file was created with betterbib v{}.}}\n"
        "\n"
        "\n"
        "@article{{stockman,\n"
        " author = {{Stockman, J.A.}},\n"
        " title = {{A New Equation to Estimate Glomerular Filtration Rate}},\n"
        " doi = {{10.1016/s0084-3954(09)79550-8}},\n"
        " pages = {{193-194}},\n"
        " source = {{Crossref}},\n"
        " url = {{https://doi.org/10.1016/s0084-3954(09)79550-8}},\n"
        " volume = {{2011}},\n"
        " journal = {{Yearbook of Pediatrics}},\n"
        " publisher = {{Elsevier BV}},\n"
        " issn = {{0084-3954}},\n"
        " year = {{2011}},\n"
        " month = jan,\n"
        "}}\n"
    ).format(betterbib.__version__)

    with open(outfile, "r") as f:
        data = f.read()
        assert data == ref

    os.remove(infile)
    os.remove(outfile)
