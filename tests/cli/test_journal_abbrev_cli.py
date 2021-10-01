import tempfile
from pathlib import Path

import pytest

import betterbib

this_dir = Path(__file__).resolve().parent
data_file_exists = Path(this_dir / "../../src/betterbib/data/journals.json").is_file()


@pytest.mark.skipif(not data_file_exists, reason="Data file missing")
def test_cli_journal_abbrev(capsys):
    ref_in = "@article{foobar,\n" "journal={SIAM Journal on Scientific Computing}\n" "}"
    ref_out = (
        f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
        "\n"
        "\n"
        "@article{foobar,\n"
        " journal = {SIAM J. Sci. Comput.},\n"
        "}\n"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"

        with open(infile, "w") as f:
            f.write(ref_in)

        betterbib.cli.main(["aj", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == ref_out

        betterbib.cli.main(["aj", "--in-place", str(infile)])
        with open(infile) as f:
            assert f.read() == ref_out
