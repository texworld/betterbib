<p align="center">
  <img alt="betterbib" src="https://nschloe.github.io/betterbib/betterbib.svg" width="60%">
</p>

[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg?style=flat-square)](https://pypi.org/project/betterbib)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/betterbib.svg?style=flat-square)](https://pypi.org/pypi/betterbib/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/betterbib.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/betterbib)
[![Downloads](https://pepy.tech/badge/betterbib/month?style=flat-square)](https://pepy.tech/project/betterbib)
<!--[![PyPi downloads](https://img.shields.io/pypi/dm/betterbib.svg?style=flat-square)](https://pypistats.org/packages/betterbib)-->

[![Discord](https://img.shields.io/static/v1?logo=discord&logoColor=white&label=chat&message=on%20discord&color=7289da&style=flat-square)](https://discord.gg/hnTJ5MRX2Y)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/betterbib/ci?style=flat-square)](https://github.com/nschloe/betterbib/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/betterbib.svg?style=flat-square)](https://codecov.io/gh/nschloe/betterbib)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/betterbib.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/betterbib)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

BibTeX files are typically manually maintained and thus often contain inconsistencies,
mistakes, or are missing information. betterbib helps maintaining your BibTeX files by
comparing them with online sources and correcting whatever entries are faulty.

Install with

<!--pytest-codeblocks:skip-->

```sh
pip install betterbib
```

and simply run

<!--pytest-codeblocks:skip-->

```sh
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

<!--pytest-codeblocks:skipif(sys.version_info >= (3, 10))-->

```sh
betterbib up -h
```

<!--pytest-codeblocks:expected-output-->

```
usage: betterbib update [-h] [-i] [-b] [-t] [-d {braces,quotes}]
                        [-u {unchanged,new,short}] [-p PAGE_RANGE_SEPARATOR]
                        [-s {crossref,dblp}] [-l]
                        [--extra-abbrev-file EXTRA_ABBREV_FILE] [-c N] [-a]
                        infiles [infiles ...]

positional arguments:
  infiles               input BibTeX files (default: stdin)

optional arguments:
  -h, --help            show this help message and exit
  -i, --in-place        modify infile in place
  -s {crossref,dblp}, --source {crossref,dblp}
                        data source (default: crossref)
  -l, --long-journal-names
                        prefer long journal names (default: false)
  --extra-abbrev-file EXTRA_ABBREV_FILE
                        custom journal abbreviations, as JSON file
  -c N, --num-concurrent-requests N
                        number of concurrent HTTPS requests (default: 10)
  -a, --latex-output    force LaTeX output (default: unicode)

Formatting:
  -b, --sort-by-bibkey  sort entries by BibTeX key (default: false)
  -t, --tab-indent      use tabs for indentation (default: false)
  -d {braces,quotes}, --delimiter-type {braces,quotes}
                        which delimiters to use in the output file (default:
                        braces {...})
  -u {unchanged,new,short}, --doi-url-type {unchanged,new,short}
                        DOI URL (new: https://doi.org/<DOI> (default), short:
                        https://doi.org/abcde)
  -p PAGE_RANGE_SEPARATOR, --page-range-separator PAGE_RANGE_SEPARATOR
                        page range separator (default: --)
```

betterbib fetches data from

- [Crossref](http://www.crossref.org/) (default) or
- [DBLP](http://dblp.uni-trier.de/) (`--source dblp`).

#### Format

The tool

<!--pytest-codeblocks:skip-->

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
~/.config/betterbib/config.toml
```

and fill it with, e.g.,

```toml
[DICTIONARY]
add=["Abrikosov", "Arnoldi", "Bergman", "Bernstein",
"Bruijn", "Chebyshev", "Danilewski", "Darboux", "Galerkin",
"Ginzburg", "Goldbach", "Hermite", "Hermitian", "Hopf",
"Hopfield", "Hölder", "Jacobi", "Jacobian", "Kolmogorov",
"Kronrod", "Krylov", "Kuratowski", "Kutta", "Lanczos",
"Liouville", "Lyapunov", "Magnus", "Manin", "Minkowski",
"Navier", "Peano", "Pell", "Pezzo", "Pitaevskii", "Pólya",
"Ramanujan", "Ricatti", "Runge", "Scholz", "Schur", "Siebeck",
"Sommerfeld", "Stieltjes", "Tausworthe", "Tchebycheff",
"Toeplitz", "Voronoi", "Voronoï", "Wieland", "Wronski",
"Wronskian"]

remove=["hermitian", "boolean" ]
```

### Similar software

- [bibcure](https://github.com/bibcure/bibcure)
