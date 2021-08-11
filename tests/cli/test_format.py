import tempfile
from pathlib import Path

import betterbib


def test_cli_format(capsys):
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
    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"

        with open(infile, "w") as f:
            f.write(ref_test_cli_format_in)

        betterbib.cli.main(["format", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == ref_test_cli_format_out

        betterbib.cli.main(["format", "--in-place", str(infile)])
        with open(infile) as f:
            assert f.read() == ref_test_cli_format_out


def test_cli_format_escape_ampersand(capsys):
    ref_in = (
        "@article{foobar,\n"
        "doi={foobar},\n"
        "url = {https://doi.org/foobar},\n"
        r"title = {Foo & Bar}," + "\n"
        "}"
    )
    ref_out = (
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{foobar,\n"
        " doi = {foobar},\n"
        " url = {https://doi.org/foobar},\n"
        r" title = {Foo \& Bar}," + "\n"
        "}\n"
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"

        with open(infile, "w") as f:
            f.write(ref_in)

        betterbib.cli.main(["format", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == "".join(ref_out)

        for _ in range(5):
            betterbib.cli.main(["format", "--in-place", str(infile)])
            with open(infile) as f:
                assert f.read() == ref_out


def test_cli_format_escape_command(capsys):
    ref_in = (
        "@article{foobar,\n"
        "doi={foobar},\n"
        "url = {https://doi.org/foobar},\n"
        r"title = {Foo on \LaTeX}," + "\n"
        "}"
    )
    ref_out = (
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{foobar,\n"
        " doi = {foobar},\n"
        " url = {https://doi.org/foobar},\n"
        r" title = {Foo on \LaTeX}," + "\n"
        "}\n"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"

        with open(infile, "w") as f:
            f.write(ref_in)

        betterbib.cli.main(["f", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == ref_out

        for _ in range(5):
            betterbib.cli.main(["f", "--in-place", str(infile)])
            with open(infile) as f:
                assert f.read() == ref_out


def test_cli_format_escape(capsys):
    ref_in = (
        "@article{foobar,\n"
        "doi={foobar},\n"
        "url = {https://doi.org/foobar},\n"
        r"title = {Foo & Bar on \LaTeX\ @TheBridge}," + "\n"
        "}"
    )
    ref_out = (
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{foobar,\n"
        " doi = {foobar},\n"
        " url = {https://doi.org/foobar},\n"
        r" title = {Foo \& Bar on \LaTeX @TheBridge}," + "\n"
        "}\n"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"

        with open(infile, "w") as f:
            f.write(ref_in)

        betterbib.cli.main(["f", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == ref_out

        for _ in range(5):
            betterbib.cli.main(["format", "--in-place", str(infile)])
            with open(infile) as f:
                assert f.read() == ref_out
