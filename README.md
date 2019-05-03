# betterbib

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/betterbib/master.svg)](https://circleci.com/gh/nschloe/betterbib)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/betterbib.svg)](https://codecov.io/gh/nschloe/betterbib)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![awesome](https://img.shields.io/badge/awesome-yes-ff69b4.svg)](https://github.com/nschloe/betterbib)
[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg)](https://pypi.org/project/betterbib)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/betterbib.svg?logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/betterbib)
[![PyPi downloads](https://img.shields.io/pypi/dd/betterbib.svg)](https://pypistats.org/packages/betterbib)

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

### Tools

All of the following tools can read from standard input and write to standard
output, so you can concatenate them to get exactly what you want. For example,
the above `betterbib` command is equivalent to
```
betterbib-sync in.bib | betterbib-journal-abbrev | betterbib-format -b - out.bib
```


#### Sync

betterbib fetches data from

   * [Crossref](http://www.crossref.org/) (default) or
   * [DBLP](http://dblp.uni-trier.de/) (`--source dblp`).

All betterbib-sync command-line options are explained in `betterbib-sync -h`.

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

#### Custom journal abbreviations

To use custom abbrebiations for journal names, create a file as a JSON
dictionary, and provide that as a command line argument with 
`--extra-abbrev-file`. For example, if the file `correct_pnas.json` is:
```json
{"PNAS": "Proc. Natl. Acad. Sci.  U.S.A."}
```
and you call `betterbib-journal-abbrev --extra-abbrev-file=correct_pnas.json`,
this will replace any bibtex entries listed with journal "PNAS" with the
correct abbreviation.

This option is included in the `betterbib` and `betterbib-journal-abbrev`
commands.

When combined with the `--long-journal-names` option, this will override
default options only if both have the same abbreviation.


### Configuration

In BibTeX titles, some words need to be protected by curly brackets such that
they are capitalized correctly, e.g., `{Einstein}`.  betterbib automatically
recognizes some of them (if they are in the default dictionary, like
`Einstein`), but you might want to add some. To this end, create the config
file
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


### Installation

betterbib is [available from the Python Package
Index](https://pypi.org/project/betterbib/), so simply do
```
pip3 install -U betterbib
```
to install or upgrade. Use `sudo -H` to install as root or the `--user` option
of `pip3` to install in `$HOME`.


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
