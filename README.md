<p align="center">
  <img alt="betterbib" src="https://nschloe.github.io/betterbib/betterbib.svg" width="60%">
</p>

[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg?style=flat-square)](https://pypi.org/project/betterbib)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/betterbib.svg?style=flat-square)](https://pypi.org/pypi/betterbib/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/betterbib.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/betterbib)
[![PyPi downloads](https://img.shields.io/pypi/dm/betterbib.svg?style=flat-square)](https://pypistats.org/packages/betterbib)

[![Discord](https://img.shields.io/static/v1?logo=discord&label=chat&message=on%20discord&color=7289da&style=flat-square)](https://discord.gg/hnTJ5MRX2Y)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/betterbib/ci?style=flat-square)](https://github.com/nschloe/betterbib/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/betterbib.svg?style=flat-square)](https://codecov.io/gh/nschloe/betterbib)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/betterbib.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/betterbib)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

BibTeX files are typically manually maintained and thus often contain inconsistencies,
mistakes, or are missing information. betterbib helps maintaining your BibTeX files by
comparing them with online sources and correcting whatever entries are faulty.

Install with

```
pip install betterbib
```

and run simply run

```
betterbib update in.bib   # or short `betterbib up`
```

to improve your BibTeX file with default settings. For example, the input BibTeX

```
@article {krylov,
  author = {Liesen and Gaul and Nabben},
  title = {Framework Deflation Krylov Augmented}
}
```

is converted to

```
@article{krylov,
 author = {Gaul, André and Gutknecht, Martin H. and Liesen, Jörg and Nabben, Reinhard},
 title = {A Framework for Deflated and Augmented {Krylov} Subspace Methods},
 doi = {10.1137/110820713},
 number = {2},
 pages = {495-518},
 source = {Crossref},
 url = {https://doi.org/10.1137/110820713},
 volume = {34},
 journal = {SIAM J. Matrix Anal. \& Appl.},
 publisher = {Society for Industrial \& Applied Mathematics (SIAM)},
 issn = {0895-4798, 1095-7162},
 year = {2013},
 month = jan,
}
```

Use `-i`/`--in-place` to modify the input file in place. Use `-h`/`--help` to see all
options.

#### Sync

betterbib fetches data from

- [Crossref](http://www.crossref.org/) (default) or
- [DBLP](http://dblp.uni-trier.de/) (`--source dblp`).

All betterbib-sync command-line options are explained in `betterbib-sync -h`.

#### Format

The tool

```sh
betterbib format in.bib
```

allows you to apply consistent formatting to you BibTeX file. See `-h`/`--help` for
options.

#### (Un)abbreviate journal names

The tool

```
betterbib abbreviate-journal-names in.bib
```

allows you to apply consistent abbreviation of journal names. See `-h`/`--help` for
options.

To use custom abbrebiations for journal names, create a file as a JSON dictionary, and
provide that as a command line argument with `--extra-abbrev-file`. For example, if the
file `correct_pnas.json` is:

```json
{ "PNAS": "Proc. Natl. Acad. Sci.  U.S.A." }
```

and you call `betterbib-journal-abbrev --extra-abbrev-file=correct_pnas.json`, this will
replace any bibtex entries listed with journal "PNAS" with the correct abbreviation.

This option is included in the `betterbib` and `betterbib-journal-abbrev` commands.

When combined with the `--long-journal-names` option, this will override default options
only if both have the same abbreviation.

### Configuration

In BibTeX titles, some words need to be protected by curly brackets such that they are
capitalized correctly, e.g., `{Einstein}`. betterbib automatically recognizes some of
them (if they are in the default dictionary, like `Einstein`), but you might want to add
some. To this end, create the config file

```
~/.config/betterbib/config.ini
```

and fill it with, e.g.,

```
[DICTIONARY]
add=Arnoldi,
    Bernstein,
    Boolean,
    Chebyshev,
    Hermitian

remove=hermitian,
   boolean
```

### Similar software

- [bibcure](https://github.com/bibcure/bibcure)
