import os
import tempfile

import betterbib

ref_test_cli_dedup_doi_in = (
    "@article{foobar,\n" "doi={foobar},\n" "url = {https://doi.org/foobar}\n" "}"
)

ref_test_cli_dedup_doi_out = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
    "\n"
    "\n"
    "@article{foobar,\n"
    " url = {https://doi.org/foobar},\n"
    "}\n"
)


def test_cli_dedup_doi():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_dedup_doi_in)

    betterbib.cli.dedup_doi(["--in-place", infile])
    with open(infile) as f:
        assert f.read() == (ref_test_cli_dedup_doi_out)
    os.remove(infile)


def test_cli_dedup_doi_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_dedup_doi_in)

    betterbib.cli.dedup_doi([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_dedup_doi_out)
    os.remove(infile)


ref_test_cli_format_in = (
    "@article{foobar,\n" "doi={foobar},\n" "url = {https://doi.org/foobar}\n" "}"
)


ref_test_cli_format_out = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
    "\n"
    "\n"
    "@article{foobar,\n"
    " doi = {foobar},\n"
    " url = {https://doi.org/foobar},\n"
    "}\n"
)


def test_cli_format():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_in)

    betterbib.cli.format(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == ref_test_cli_format_out

    os.remove(infile)


def test_cli_format_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_in)

    betterbib.cli.format([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_format_out)

    os.remove(infile)


ref_test_cli_format_escape_ampersand_in = (
    "@article{foobar,\n"
    "doi={foobar},\n"
    "url = {https://doi.org/foobar},\n"
    r"title = {Foo & Bar}," + "\n"
    "}"
)


ref_test_cli_format_escape_ampersand_out = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
    "\n"
    "\n"
    "@article{foobar,\n"
    " doi = {foobar},\n"
    " url = {https://doi.org/foobar},\n"
    r" title = {Foo \& Bar}," + "\n"
    "}\n"
)


def test_cli_format_escape_ampersand():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_ampersand_in)

    betterbib.cli.format(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == ref_test_cli_format_escape_ampersand_out

    os.remove(infile)


def test_cli_format_escape_ampersand_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_ampersand_in)

    betterbib.cli.format([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_format_escape_ampersand_out)

    os.remove(infile)


def test_cli_format_escape_ampersand_repeated():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_ampersand_in)

    for i in range(10):
        betterbib.cli.format(["--in-place", infile])

        with open(infile) as f:
            assert f.read() == ref_test_cli_format_escape_ampersand_out

    os.remove(infile)


def test_cli_format_escape_ampersand_repeated_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_ampersand_in)

    for i in range(10):
        betterbib.cli.format(["--in-place", infile])
        betterbib.cli.format([infile])
        captured = capsys.readouterr()

        assert captured.out == "".join(ref_test_cli_format_escape_ampersand_out)

    os.remove(infile)


ref_test_cli_format_escape_command_in = (
    "@article{foobar,\n"
    "doi={foobar},\n"
    "url = {https://doi.org/foobar},\n"
    r"title = {Foo on \LaTeX}," + "\n"
    "}"
)


ref_test_cli_format_escape_command_out = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
    "\n"
    "\n"
    "@article{foobar,\n"
    " doi = {foobar},\n"
    " url = {https://doi.org/foobar},\n"
    r" title = {Foo on \LaTeX}," + "\n"
    "}\n"
)


def test_cli_format_escape_command():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_command_in)

    betterbib.cli.format(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == ref_test_cli_format_escape_command_out

    os.remove(infile)


def test_cli_format_escape_command_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_command_in)

    betterbib.cli.format([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_format_escape_command_out)

    os.remove(infile)


def test_cli_format_escape_command_repeated():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_command_in)

    for i in range(10):
        betterbib.cli.format(["--in-place", infile])

        with open(infile) as f:
            assert f.read() == ref_test_cli_format_escape_command_out

    os.remove(infile)


def test_cli_format_escape_command_repeated_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_command_in)

    for i in range(10):
        betterbib.cli.format(["--in-place", infile])
        betterbib.cli.format([infile])
        captured = capsys.readouterr()

        assert captured.out == "".join(ref_test_cli_format_escape_command_out)

    os.remove(infile)


ref_test_cli_format_escape_in = (
    "@article{foobar,\n"
    "doi={foobar},\n"
    "url = {https://doi.org/foobar},\n"
    r"title = {Foo & Bar on \LaTeX\ @TheBridge}," + "\n"
    "}"
)


ref_test_cli_format_escape_out = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
    "\n"
    "\n"
    "@article{foobar,\n"
    " doi = {foobar},\n"
    " url = {https://doi.org/foobar},\n"
    r" title = {Foo \& Bar on \LaTeX @TheBridge}," + "\n"
    "}\n"
)


def test_cli_format_escape():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_in)

    betterbib.cli.format(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == ref_test_cli_format_escape_out

    os.remove(infile)


def test_cli_format_escape_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_in)

    betterbib.cli.format([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_format_escape_out)

    os.remove(infile)


def test_cli_format_escape_repeated():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_in)

    for i in range(10):
        betterbib.cli.format(["--in-place", infile])

        with open(infile) as f:
            assert f.read() == ref_test_cli_format_escape_out

    os.remove(infile)


def test_cli_format_escape_repeated_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_format_escape_in)

    for i in range(10):
        betterbib.cli.format(["--in-place", infile])
        betterbib.cli.format([infile])
        captured = capsys.readouterr()

        assert captured.out == "".join(ref_test_cli_format_escape_out)

    os.remove(infile)


ref_test_cli_journal_abbrev_in = (
    "@article{foobar,\n" "journal={SIAM Journal on Scientific Computing}\n" "}"
)

ref_test_cli_journal_abbrev_out = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
    "\n"
    "\n"
    "@article{foobar,\n"
    " journal = {SIAM J. Sci. Comput.},\n"
    "}\n"
)


def test_cli_journal_abbrev():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_journal_abbrev_in)

    betterbib.cli.journal_abbrev(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == (ref_test_cli_journal_abbrev_out)

    os.remove(infile)


def test_cli_journal_abbrev_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_journal_abbrev_in)

    betterbib.cli.journal_abbrev([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_journal_abbrev_out)

    os.remove(infile)


ref_test_cli_sync_in = (
    "@article{stockman,\n"
    " author = {Stockman},\n"
    "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
    "}"
)

ref_test_cli_sync_out = (
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


def test_cli_sync():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_sync_in)

    betterbib.cli.sync(["--in-place", infile])

    with open(infile) as f:
        assert f.read() == (ref_test_cli_sync_out)
    os.remove(infile)


def test_cli_sync_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_sync_in)

    betterbib.cli.sync([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_sync_out)
    os.remove(infile)


ref_test_cli_doi2bibtex_args = ["10.1016/s0084-3954(09)79550-8"]

ref_test_cli_doi2bibtex_out = (
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


def test_cli_doi2bibtex(capsys):
    betterbib.cli.doi2bibtex(ref_test_cli_doi2bibtex_args)

    captured = capsys.readouterr()
    assert captured.out == "".join(ref_test_cli_doi2bibtex_out)


ref_test_cli_full_in = (
    "@article{stockman,\n"
    " author = {Stockman},\n"
    "title = {A New Equation to Estimate Glomerular Filtration Rate}\n"
    "}"
)

ref_test_cli_full_out = (
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


def test_cli_full():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_full_in)

    betterbib.cli.full(["--in-place", infile])

    with open(infile) as f:
        data = f.read()
        assert data == ref_test_cli_full_out

    os.remove(infile)


def test_cli_full_stdout(capsys):
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(ref_test_cli_full_in)

    betterbib.cli.full([infile])
    captured = capsys.readouterr()

    assert captured.out == "".join(ref_test_cli_full_out)

    os.remove(infile)
