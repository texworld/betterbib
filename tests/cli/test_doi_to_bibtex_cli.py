import betterbib


def test_cli_doi_to_bibtex(capsys):
    doi = "10.1016/s0084-3954(09)79550-8"

    ref_out = (
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{stockman2011,\n"
        " author = {Stockman, J.A.},\n"
        " doi = {10.1016/s0084-3954(09)79550-8},\n"
        " source = {Crossref},\n"
        " url = {http://dx.doi.org/10.1016/s0084-3954(09)79550-8},\n"
        " volume = {2011},\n"
        " journal = {Yearbook of Pediatrics},\n"
        " publisher = {Elsevier BV},\n"
        " title = {A New Equation to Estimate Glomerular Filtration Rate},\n"
        " issn = {0084-3954},\n"
        " pages = {193--194},\n"
        " year = {2011},\n"
        " month = jan,\n"
        "}\n"
    )

    betterbib.cli.main(["doi-to-bibtex", doi])

    captured = capsys.readouterr()
    assert captured.out == ref_out
