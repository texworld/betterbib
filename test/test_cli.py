# -*- coding: utf-8 -*-
#
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

    betterbib.cli.dedup_doi.main([infile, outfile])
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
    return
