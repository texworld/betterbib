# betterbib

[![Build Status](https://travis-ci.org/nschloe/betterbib.svg?branch=master)](https://travis-ci.org/nschloe/betterbib)
[![codecov](https://codecov.io/gh/nschloe/betterbib/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/betterbib)
[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg)](https://pypi.python.org/pypi/betterbib)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg)](https://img.shields.io/badge/awesome-yes-brightgreen.svg)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/betterbib.svg?style=social&label=Stars&maxAge=2592000)](https://github.com/nschloe/betterbib)

BibTeX files are typically manually maintained and thus often contain
inconsistencies, mistakes, or are missing information. betterbib helps
maintaining your BibTeX files by comparing them with online sources and
correcting whatever entries are found faulty. For example, with
```
$ betterbib in.bib out.bib
```
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
  publisher = {Society for Industrial & Applied Mathematics (SIAM)},
  doi = {10.1137/110820713},
  title = {A Framework for Deflated and Augmented {Krylov} Subspace Methods},
  url = {https://doi.org/10.1137/110820713},
  journal = {SIAM J. Matrix Anal. & Appl.},
  number = {2},
  month = jan,
  volume = {34},
  source = {Crossref},
  year = {2013},
  pages = {495-518}
}
```
(If you prefer long journal names, add the option `--long-journal-name`/`-l`.)

betterbib fetches data from

   * [Crossref](http://www.crossref.org/) (default) or
   * [DBLP](http://dblp.uni-trier.de/) (`--source dblp`).

All betterbib command-line options are explained in `betterbib -h`.


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


### Usage
```
$ betterbib mybibliography.bib out.bib
```

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
