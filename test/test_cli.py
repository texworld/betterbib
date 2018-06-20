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

    betterbib.cli.dedup_doi([infile, outfile])
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


def test_cli_format():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{foobar,\n"
            "doi={foobar},\n"
            "url = {https://doi.org/foobar}\n"
            "}"
        )

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.format([infile, outfile])

    with open(outfile, "r") as f:
        assert f.read() == (
            (
                "%comment{{This file was created with betterbib v{}.}}\n"
                "\n"
                "\n"
                "\n"
                "@article{{foobar,\n"
                " doi = {{foobar}},\n"
                " url = {{https://doi.org/foobar}},\n"
                "}}\n"
            ).format(betterbib.__version__)
        )

    os.remove(infile)
    os.remove(outfile)
    return


def test_cli_journal_abbrev():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{foobar,\n"
            "journal={SIAM Journal on Scientific Computing}\n"
            "}"
        )

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.journal_abbrev([infile, outfile])

    with open(outfile, "r") as f:
        assert f.read() == (
            (
                "%comment{{This file was created with betterbib v{}.}}\n"
                "\n"
                "\n"
                "\n"
                "@article{{foobar,\n"
                " journal = {{SIAM J. Sci. Comput.}},\n"
                "}}\n"
            ).format(betterbib.__version__)
        )

    os.remove(infile)
    os.remove(outfile)
    return


def test_cli_sync():
    infile = tempfile.NamedTemporaryFile().name
    with open(infile, "w") as f:
        f.write(
            "@article{krylov,\n"
            " author = {Liesen and Gaul and Nabben},\n"
            "title = {Framework Deflation Krylov Augmented}\n"
            "}"
        )

    outfile = tempfile.NamedTemporaryFile().name

    betterbib.cli.sync([infile, outfile])

    with open(outfile, "r") as f:
        assert f.read() == (
            (
                "%comment{{This file was created with betterbib v{}.}}\n"
                "\n"
                "\n"
                "\n"
                "@article{{krylov,\n"
                " author = {{Gaul, André and Gutknecht, Martin H. and Liesen, Jörg and Nabben, Reinhard}},\n"
                " title = {{A Framework for Deflated and Augmented {{Krylov}} Subspace Methods}},\n"
                " doi = {{10.1137/110820713}},\n"
                " number = {{2}},\n"
                " pages = {{495-518}},\n"
                " source = {{Crossref}},\n"
                " url = {{http://dx.doi.org/10.1137/110820713}},\n"
                " volume = {{34}},\n"
                " journal = {{SIAM J. Matrix Anal. \& Appl.}},\n"
                " publisher = {{Society for Industrial \& Applied Mathematics (SIAM)}},\n"
                " issn = {{0895-4798, 1095-7162}},\n"
                " year = {{2013}},\n"
                " month = jan,\n"
                "}}\n"
            ).format(betterbib.__version__)
        )

    os.remove(infile)
    os.remove(outfile)
    return
