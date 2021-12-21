import tempfile
from pathlib import Path

import pytest

import betterbib

this_dir = Path(__file__).resolve().parent
data_file_exists = Path(this_dir / "../../src/betterbib/data/journals.json").is_file()


@pytest.mark.skipif(not data_file_exists, reason="Data file missing")
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
        " source = {Crossref},\n"
        " url = {https://doi.org/10.1016/s0084-3954(09)79550-8},\n"
        " volume = {2011},\n"
        " journal = {Yearbook of Pediatrics},\n"
        " publisher = {Elsevier BV},\n"
        " issn = {0084-3954},\n"
        " pages = {193--194},\n"
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
        assert captured.out == "\n" + ref_out

        betterbib.cli.main(["up", "--in-place", str(infile)])
        with open(infile) as f:
            fcontent = f.read()
        assert fcontent == ref_out
