# BetterBib

[![Build Status](https://travis-ci.org/nschloe/betterbib.svg?branch=master)](https://travis-ci.org/nschloe/betterbib)
[![Code Health](https://landscape.io/github/nschloe/betterbib/master/landscape.png)](https://landscape.io/github/nschloe/betterbib/master)
[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg)](https://pypi.python.org/pypi/betterbib)
[![PyPi Downloads](https://img.shields.io/pypi/dm/betterbib.svg)](https://pypi.python.org/pypi/betterbib)

BibTeX files are typically manually maintained and thus often contain
inconsistences, mistakes, or are missing information. BetterBib helps
maintaining your BibTeX files by comparing them with online sources and
correctiing whatever entries were found faulty. For example, the BibTeX entry
```
@article {krylov,
  author = {Liesen and Strakoš},
  title = {Krylov subspace methods}
}
```
is converted into
```
@book{krylov,
    AUTHOR = {Liesen, J{\"o}rg and Strako{\v{s}}, Zden{\v{e}}k},
     TITLE = {Krylov subspace methods},
    SERIES = {Numerical Mathematics and Scientific Computation},
      NOTE = {Principles and analysis},
 PUBLISHER = {Oxford University Press, Oxford},
      YEAR = {2013},
     PAGES = {xvi+391},
      ISBN = {978-0-19-965541-0},
   MRCLASS = {65F10 (65F15)},
  MRNUMBER = {3024841},
MRREVIEWER = {Melina A. Freitag},
}
```
by simply calling
```
betterbib in.bib out.bib
```

At the moment, the only BetterBib backend is the
[MathSciNet](http://www.ams.org/mathscinet/) service, so you'll have to be in a
university network for it to work.


### Installation

#### Python Package Index

BetterBib is [available from the Python Package
Index](https://pypi.python.org/pypi/betterbib/), so simply type
```
pip install betterbib
```
to install or
```
pip install betterbib -U
```
to upgrade.

#### Manual installation

Download BetterBib from [GitHub](https://github.com/nschloe/betterbib) and install it
with
```
python setup.py install
```

### Requirements

BetterBib requires a few Python modules to run, notably

* [requests](http://docs.python-requests.org/en/latest/),
* [Pybtex](http://pybtex.sourceforge.net/).


### Usage
```
$ ./betterbib mybibliography.bib out.bib
```

### License

BetterBib is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
