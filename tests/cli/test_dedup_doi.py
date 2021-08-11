# import os
# import tempfile
# from pathlib import Path
#
# import betterbib
#
# ref_test_cli_dedup_doi_in = (
#     "@article{foobar,\n" "doi={foobar},\n" "url = {https://doi.org/foobar}\n" "}"
# )
#
# ref_test_cli_dedup_doi_out = (
#     f"%comment{{This file was created with betterbib v{betterbib.__version__}.}}\n"
#     "\n"
#     "\n"
#     "@article{foobar,\n"
#     " url = {https://doi.org/foobar},\n"
#     "}\n"
# )
#
#
# def test_cli_dedup_doi():
#     infile = tempfile.NamedTemporaryFile().name
#     with open(infile, "w") as f:
#         f.write(ref_test_cli_dedup_doi_in)
#
#     betterbib.cli.dedup_doi(["--in-place", infile])
#     with open(infile) as f:
#         assert f.read() == (ref_test_cli_dedup_doi_out)
#     os.remove(infile)
#
#
# def test_cli_dedup_doi_stdout(capsys):
#     infile = tempfile.NamedTemporaryFile().name
#     with open(infile, "w") as f:
#         f.write(ref_test_cli_dedup_doi_in)
#
#     betterbib.cli.dedup_doi([infile])
#     captured = capsys.readouterr()
#
#     assert captured.out == "".join(ref_test_cli_dedup_doi_out)
#     os.remove(infile)
