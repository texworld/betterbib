# betterbib

[![Build Status](https://travis-ci.org/nschloe/betterbib.svg?branch=master)](https://travis-ci.org/nschloe/betterbib)
[![codecov](https://codecov.io/gh/nschloe/betterbib/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/betterbib)
[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg)](https://pypi.python.org/pypi/betterbib)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg)](https://img.shields.io/badge/awesome-yes-brightgreen.svg)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/betterbib.svg?style=social&label=Stars&maxAge=2592000)](https://github.com/nschloe/betterbib)

BibTeX files are typically manually maintained and thus often contain
inconsistencies, mistakes, or are missing information. betterbib helps
maintaining your BibTeX files by comparing them with online sources and
correcting whatever entries are found faulty.

Simply run
```
betterbib in.bib out.bib
```
to improve your BibTeX file with default settings. For example,
the input BibTeX
```
@article {krylov,
  author = {Liesen and Gaul and Nabben},
  title = {Framework Deflation Krylov Augmented}
}
```
is converted into
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
 journal = {SIAM J. Matrix Anal. & Appl.},
 publisher = {Society for Industrial & Applied Mathematics (SIAM)},
 issn = {0895-4798, 1095-7162},
 year = {2013},
 month = jan,
}
```

### Tools

All of the following tools can read from standard input and write to standard
output, so you can concatenate them to get exactly what you want. For example,
the above `betterbib` command is short for
```
betterbib-sync in.bib | betterbib-journal-abbrev | betterbib-format -b - out.bib
```


#### Sync


betterbib fetches data from

   * [Crossref](http://www.crossref.org/) (default) or
   * [DBLP](http://dblp.uni-trier.de/) (`--source dblp`).

All betterbib command-line options are explained in `betterbib -h`.

#### Format

The tool
```
betterbib-format in.bib out.bib
```
allows you to apply consistent formatting to you BibTeX file. See `-h`/`--help`
for options.

#### (Un)abbreviate journal names

The tool
```
betterbib-journal-abbrev in.bib out.bib
```
allows you to apply consistent abbreviation of journal names. See `-h`/`--help`
for options.

### Installation

#### Python Package Index

betterbib is [available from the Python Package
Index](https://pypi.python.org/pypi/betterbib/), so simply type
```
pip install -U betterbib
```
to install or upgrade. Use `sudo -H` to install as root or the `--user` option
of `pip` to install in `$HOME`.


### Requirements

betterbib requires

* [enchant](https://abiword.github.io/enchant/) and
* [pandoc](https://pandoc.org/)

to be installed.


### Testing

To run the betterbib unit tests, check out this repository and type
```
pytest
```

### Distribution
To create a new release

1. bump the `__version__` number,

2. publish to PyPi and tag on GitHub:
    ```
    $ make publish
    ```

### License

betterbib is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
