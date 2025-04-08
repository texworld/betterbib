<p align="center">
  <img alt="betterbib" src="https://raw.githubusercontent.com/texworld/betterbib/assets/betterbib.svg" width="60%">
</p>

[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg?style=flat-square)](https://pypi.org/project/betterbib)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/betterbib.svg?style=flat-square)](https://pypi.org/pypi/betterbib/)
[![GitHub stars](https://img.shields.io/github/stars/texworld/betterbib.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/texworld/betterbib)

<!-- [![Downloads](https://pepy.tech/badge/betterbib/month?style=flat-square)](https://pepy.tech/project/betterbib) -->
<!--[![PyPi downloads](https://img.shields.io/pypi/dm/betterbib.svg?style=flat-square)](https://pypistats.org/packages/betterbib)-->

[![Discord](https://img.shields.io/static/v1?logo=discord&logoColor=white&label=chat&message=on%20discord&color=7289da&style=flat-square)](https://discord.gg/hnTJ5MRX2Y)

> [!NOTE]
> See [here](https://github.com/texworld) for licensing information.

Bibliography files are notoriously hard to work with. Betterbib contains
a number of easy-to-use command-line tools to help.

- [`betterbib convert`](#convert) converts between different bibliography formats, e.g.

  - [BibTeX](https://www.bibtex.org/Format/)
  - [BibLaTeX](https://ctan.org/pkg/biblatex)
  - [RIS](<https://en.wikipedia.org/wiki/RIS_(file_format)>)
  - [CSL-JSON](https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html)

- [`betterbib sync`](#sync) syncs bibliography data with a number of online sources, e.g.,

  - [Crossref](https://www.crossref.org/)
  - [DBLP](https://dblp.uni-trier.de/)
  - [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
  - [arXiv](https://arxiv.org/)
  - [Zenodo](https://zenodo.org/)

- [`betterbib format`](#format) formats your bibliography files to your liking.
  Can also (un)abbreviate author and journal names.

- [`betterbib doi-to`](#dereference-dois) converts a DOI or DOI URL to a bibliography entry.

### Installation

Install betterbib [from PyPI](https://pypi.org/project/betterbib/) with

<!--pytest.mark.skip-->

```
pip install betterbib
```

#### Convert

#### Sync

Simply run

<!--pytest.mark.skip-->

```sh
betterbib sync in.bib
```

to sync your bibliography file with online sources. For example, the input

```bibtex
@article{wiles,
title={Fermat Last Theorem},
doi={10.2307/2118559},
}
```

is converted to

```bibtex
@article{wiles,
  number = {3},
  doi = {10.2307/2118559},
  pages = {443},
  source = {Crossref},
  volume = {141},
  author = {Wiles, Andrew},
  year = {1995},
  month = may,
  url = {https://doi.org/10.2307/2118559},
  issn = {0003-486X},
  journal = {The Annals of Mathematics},
  publisher = {JSTOR},
  title = {Modular Elliptic Curves and Fermat's Last Theorem},
}
```

See `-h`/`--help` for all options.

<!--pytest.mark.skipif(sys.version_info < (3, 11), reason="Need Python 3.11+")-->

```sh
betterbib sync -h
```

<!--pytest-codeblocks: expected-output-ignore-whitespace-->

```
Usage: betterbib sync [-h] [-i] [-c N] [-s SRC] [-m MINIMUM_SCORE] [-q] [--debug]
                      [--output-format {bibtex,biblatex,csl-json,ris}]
                      infiles [infiles ...]

Positional Arguments:
  infiles               input bibliography files

Options:
  -h, --help            show this help message and exit
  -i, --in-place        modify infile in place
  -c, --num-concurrent-requests N
                        number of concurrent HTTPS requests (default: 1)
  -s, --sources SRC     sources to try (comma-separated, with order; default:
                        crossref,dblp,pubmed)
  -m, --minimum-score MINIMUM_SCORE
                        minimum score to count as a match (default: 0.0)
  -q, --quiet           don't show progress info (default: show)
  --debug               some debug output (default: false)
  --output-format {bibtex,biblatex,csl-json,ris}
                        force output format (default: same as input)
```

#### Format

After that, you can for example run

```
betterbib format in.bib --sort-fields --align-values --journal-names short --abbrev-first-names
```

to get

```bibtex
@article{wiles,
  author    = {Wiles, A.},
  doi       = {10.2307/2118559},
  issn      = {0003-486X},
  journal   = {Ann. Math.},
  month     = may,
  number    = {3},
  pages     = {443},
  publisher = {JSTOR},
  source    = {Crossref},
  title     = {Modular Elliptic Curves and Fermat's Last Theorem},
  url       = {https://doi.org/10.2307/2118559},
  volume    = {141},
  year      = {1995},
}
```

```sh
betterbib format -h
```

<!--pytest.mark.skipif(sys.version_info < (3, 11), reason="Need Python 3.11+")-->

```
Usage: betterbib format [-h] [-i] [--drop DROP] [--journal-names {long,short,unchanged}] [--abbrev-first-names]
                        [--sort-entries] [--sort-fields] [--doi-url-type {unchanged,old,new,short}]
                        [--page-range-separator PAGE_RANGE_SEPARATOR] [--protect-title-capitalization]
                        [--indent [INDENT]] [--align-values]
                        infiles [infiles ...]

Positional Arguments:
  infiles               input BibTeX files

Options:
  -h, --help            show this help message and exit
  -i, --in-place        modify infile in place
  --drop DROP           drop fields from entries (can be passed multiple times)
  --journal-names {long,short,unchanged}
                        force full or abbreviated journal names (default: unchanged)
  --abbrev-first-names  abbreviate first names in author lists etc. (default: false)
  --sort-entries        sort entries alphabetically by BibTeX key (default: false)
  --sort-fields         sort fields alphabetically (default: false)
  --doi-url-type {unchanged,old,new,short}
                        DOI URL (new: https://doi.org/<DOI>, short: https://doi.org/abcde) (default: new)
  --page-range-separator PAGE_RANGE_SEPARATOR
                        page range separator (int or string, default: unchanged)
  --protect-title-capitalization
                        brace-protect names in titles (e.g., {Newton}; default: false)
  --indent [INDENT]     indentation (int or string; default: 1)
  --align-values        align field values (default: false)
```

#### Dereference DOIs

Given a DOI or a DOI URL, it's often useful to generate a bibliography entry for it. `betterbib doi-to` does just that.

```sh
betterbib doi-to ris 10.1002/andp.19053221004
```

<!--pytest-codeblocks: expected-output-ignore-whitespace-->

```ris
TY  - JOUR
IS  - 10
DO  - 10.1002/andp.19053221004
SP  - 891
EP  - 921
DS  - Crossref
VL  - 322
AU  - Einstein, A.
DA  - 1905/01
UR  - https://doi.org/10.1002/andp.19053221004
SN  - 0003-3804
SN  - 1521-3889
JF  - Annalen der Physik
JO  - Ann. Phys.
PB  - Wiley
TI  - Zur Elektrodynamik bewegter Körper
ER  -
```
