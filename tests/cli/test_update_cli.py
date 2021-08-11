import tempfile
from pathlib import Path

import betterbib


def test_cli_update(capsys):
    ref_in = (
        "@article{stockman,\n"
        " author = {Stockman},\n"
        "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
        "}"
    )
    ref_out = (
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
    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"
        with open(infile, "w") as f:
            f.write(ref_in)

        betterbib.cli.main(["update", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == ref_out

        betterbib.cli.main(["up", "--in-place", str(infile)])
        with open(infile) as f:
            assert f.read() == ref_out
