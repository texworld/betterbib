import tempfile
from pathlib import Path

import pytest

import betterbib

version_line = (
    f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
)


@pytest.mark.parametrize(
    "ref_in,ref_out",
    [
        (
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar}\n"
            "}",
            version_line + "\n"
            "\n"
            "@article{foobar,\n"
            " doi = {foobar},\n"
            " url = {https://doi.org/foobar},\n"
            "}\n",
        ),
        # escape ampersand:
        (
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar},\n"
            r"title = {Foo & Bar}," + "\n"
            "}",
            version_line + "\n"
            "\n"
            "@article{foobar,\n"
            " doi = {foobar},\n"
            " url = {https://doi.org/foobar},\n"
            r" title = {Foo \& Bar}," + "\n"
            "}\n",
        ),
        # escape command:
        (
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar},\n"
            r"title = {Foo on \LaTeX}," + "\n"
            "}",
            version_line + "\n"
            "\n"
            "@article{foobar,\n"
            " doi = {foobar},\n"
            " url = {https://doi.org/foobar},\n"
            r" title = {Foo on \LaTeX}," + "\n"
            "}\n",
        ),
        # more escape:
        (
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar},\n"
            r"title = {Foo & Bar on \LaTeX\ @TheBridge}," + "\n"
            "}",
            version_line + "\n"
            "\n"
            "@article{foobar,\n"
            " doi = {foobar},\n"
            " url = {https://doi.org/foobar},\n"
            r" title = {Foo \& Bar on \LaTeX @TheBridge}," + "\n"
            "}\n",
        ),
    ],
)
def test_cli_format(ref_in, ref_out, capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"

        with open(infile, "w") as f:
            f.write(ref_in)

        betterbib.cli.main(["format", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == ref_out

        betterbib.cli.main(["format", "--in-place", str(infile)])
        with open(infile) as f:
            assert f.read() == ref_out
