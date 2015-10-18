# BetterBib

[![Build Status](https://travis-ci.org/nschloe/betterbib.svg?branch=master)](https://travis-ci.org/nschloe/betterbib)
[![Code Health](https://landscape.io/github/nschloe/betterbib/master/landscape.png)](https://landscape.io/github/nschloe/betterbib/master)
[![Coverage Status](https://coveralls.io/repos/nschloe/betterbib/badge.svg?branch=master&service=github)](https://coveralls.io/github/nschloe/betterbib?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg)](https://pypi.python.org/pypi/betterbib)
[![PyPi Downloads](https://img.shields.io/pypi/dm/betterbib.svg)](https://pypi.python.org/pypi/betterbib)

BibTeX files are typically manually maintained and thus often contain
inconsistencies, mistakes, or are missing information. BetterBib helps
maintaining your BibTeX files by comparing them with online sources and
correcting whatever entries are found faulty. For example, with
```
$ betterbib in.bib out.bib
```
the input BibTex
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

At the moment, BetterBib fetches from one of two data sources:

 * [MRef](http://www.ams.org/mref) and
 * [MathSciNet](http://www.ams.org/mathscinet/).

The former is free and open, so it is the default. If you have access, you may
however find the MathSciNet source faster. All BetterBib command-line options
are explained in `betterbib -h`.


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

* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
* [requests](http://docs.python-requests.org/en/latest/),
* [Pybtex](http://pybtex.sourceforge.net/).


### Usage
```
$ ./betterbib mybibliography.bib out.bib
```

### Testing

To run the BetterBib unit tests, check out this repository and type
```
nosetests
```
or
```
nose2 -s test
```



### Distribution
To create a new release

1. bump the `__version__` number,

2. create a Git tag,
    ```
    $ git tag -a v0.3.1
    $ git push --tags
    ```
    and

3. upload to PyPi:
    ```
    $ make upload
    ```

### License

BetterBib is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
