# BetterBib

[![Code Health](https://landscape.io/github/nschloe/betterbib/master/landscape.png)](https://landscape.io/github/nschloe/betterbib/master)

Update BibTeX file with info from online sources, e.g.,
http://www.ams.org/mathscinet/.

### Requirements

BetterBib requires a few Python modules to run, notably

* [requests](http://docs.python-requests.org/en/latest/),
* [Pybtex](http://pybtex.sourceforge.net/).


### Usage
```
$ ./betterbib mybibliography.bib out.bib
```
Download http://www.w3.org/Math/characters/unicode.xml to the directory where
the script resides.

### License

BetterBib is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
