import tempfile
from pathlib import Path

import betterbib

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


def test_cli_journal_abbrev(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        infile = Path(tmpdir) / "test.bib"

        with open(infile, "w") as f:
            f.write(ref_test_cli_journal_abbrev_in)

        betterbib.cli.main(["aj", str(infile)])
        captured = capsys.readouterr()
        assert captured.out == ref_test_cli_journal_abbrev_out

        betterbib.cli.main(["aj", "--in-place", str(infile)])
        with open(infile) as f:
            assert f.read() == ref_test_cli_journal_abbrev_out
