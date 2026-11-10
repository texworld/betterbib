<p align="center">
  <img alt="betterbib" src="https://raw.githubusercontent.com/texworld/betterbib/main/images/betterbib.svg" width="60%">
</p>

[![PyPi Version](https://img.shields.io/pypi/v/betterbib.svg?style=flat-square)](https://pypi.org/project/betterbib)
[![GitHub stars](https://img.shields.io/github/stars/texworld/betterbib.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/texworld/betterbib)

> [!NOTE]
> betterbib requires an active [TeX World](https://mondaytech.com/texworld/) license. See
> [Licensing](#licensing) below.

Bibliography files are notoriously hard to work with. betterbib is a fast,
single-binary command-line tool that helps:

- [`betterbib sync`](#sync) enriches your bibliography entries with data from online
  sources, e.g.,

  - [Crossref](https://www.crossref.org/)
  - [DBLP](https://dblp.uni-trier.de/)
  - [PubMed](https://pubmed.ncbi.nlm.nih.gov/)

- [`betterbib format`](#format) normalizes the cosmetic style of your bibliography
  files (key case, value alignment, field order, indentation).

- [`betterbib check`](#check) lints bibliography files for common mistakes
  (malformed DOIs, duplicate keys, missing fields, inconsistent name/journal
  abbreviations, ...) and can auto-fix most of them.

- [`betterbib convert`](#convert) converts between bibliography formats, e.g.

  - [BibTeX](https://www.bibtex.org/Format/)
  - [BibLaTeX](https://ctan.org/pkg/biblatex)
  - [RIS](<https://en.wikipedia.org/wiki/RIS_(file_format)>)
  - [CSL-JSON](https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html)

- [`betterbib doi-to`](#dereference-dois) turns a DOI into a bibliography entry.

### Installation

Install betterbib [from PyPI](https://pypi.org/project/betterbib/) with

```sh
pip install betterbib
```

### Licensing

betterbib checks for a TeX World license on startup. If none is found and
you're running interactively, you'll be prompted to enter a license key,
start a free trial, or buy a license online.

For non-interactive use (CI, scripts), set the license key via one of the
following environment variables:

```sh
export TEXWORLD_LIC=<your-license-key>
```

For commercial licensing, contact <texworld@mondaytech.com>.

#### Sync

Simply run

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
  title     = {Modular Elliptic Curves and Fermat's Last Theorem},
  journal   = {The Annals of Mathematics},
  volume    = {141},
  number    = {3},
  pages     = {443},
  publisher = {JSTOR},
  issn      = {0003-486X},
  url       = {https://doi.org/10.2307/2118559},
  doi       = {10.2307/2118559},
  source    = {Crossref},
}
```

```
Usage: betterbib sync [OPTIONS] <INPUT_FILE>

Arguments:
  <INPUT_FILE>  input bibliography file

Options:
      --stdout   Write output to stdout instead of modifying the file in place
      --check    Don't write any changes; report per-entry updates/no-matches and exit with non-zero status if any occurred
  -q, --quiet    Don't show progress info
  -v, --verbose  Print a line per entry showing which source matched, or why it didn't
  -h, --help     Print help
```

`--check` is useful in CI: it exits non-zero if any entry would change,
without touching the file. Combine with `--stdout` to inspect the would-be
result without writing it.

In `--check` mode, betterbib also prints one line per entry that needs
attention, so you can grep/postprocess the output:

```
wiles: would update (via Crossref)
unfindable: no match found
in.bib: would update 1 entry
in.bib: 1 entry has no match
```

`no match found` means none of the configured sources could resolve the
entry (e.g. a DOI that doesn't exist); these entries are not modified
either way, but `--check` still exits non-zero so the case isn't missed
silently.

Outside of `--check`, pass `-v`/`--verbose` to get the same kind of detail
for an actual (writing) sync run:

```
$ betterbib sync in.bib --verbose
skipped: skipped (betterbib-skip)
wiles: updated (via Crossref)
unfindable: no match found
```

`--verbose` and `--quiet` are mutually exclusive.

To exclude a single entry from `sync` (e.g. because you've edited it by hand),
add a `betterbib-skip` field to it:

```bibtex
@article{wiles,
  title          = {Fermat Last Theorem},
  doi            = {10.2307/2118559},
  betterbib-skip = {true},
}
```

Any value other than `false` skips the entry; it's left completely
untouched (and doesn't count towards `--check`'s change count).

By default, betterbib tries OpenAlex, then the DOI resolver (for entries that
already have a DOI), then Crossref, DBLP and PubMed, stopping at the first
source that returns a confident, unique match. You can restrict or
reorder sources, and tune match confidence, via `betterbib.toml`:

```toml
[sync]
sources = ["crossref", "dblp"]  # default: ["openalex", "doi", "crossref", "dblp", "pubmed"]
minimum-score = 0.0             # minimum match score to accept a result
num-concurrent-requests = 5     # concurrent HTTPS requests
cache-ttl-s = 2592000            # how long API responses are cached (30 days)
timeout-s = 120                  # per-request timeout
```

#### Format

```sh
betterbib format in.bib
```

normalizes the cosmetic style of a bibliography file: key case, field
alignment, field order, and indentation. It does not change field content
(for that, see [`check --fix`](#check)).

```
Usage: betterbib format [OPTIONS] <INPUT_FILE>

Arguments:
  <INPUT_FILE>  File to format

Options:
      --check  Avoid writing any formatted files back; instead, exit with a non-zero status code if any files would have been modified, and zero otherwise
  -h, --help   Print help
```

Configure the style via `betterbib.toml`:

```toml
[format]
keyword-case = "lower"      # "lower" or "upper"
align-values = true
field-order = "standard"    # "standard", "alphabetical", or "unchanged"
indentation = "  "
```

#### Check

```sh
betterbib check in.bib
```

lints a bibliography file for common mistakes. For example:

```
BIB09 [*] Expected abbreviated given names, got 'Andrew'
 --> in.bib:2:23
  |
1 | @article{wiles,
2 |   author    = {Wiles, Andrew},
  |                       ^^^^^^
3 |   title     = {Modular Elliptic Curves and Fermat's Last Theorem},
  |
help: Replace with `A.`

BIB15 [*] Unprotected word `Fermat`
 --> in.bib:3:44
  |
2 |   author    = {Wiles, Andrew},
3 |   title     = {Modular Elliptic Curves and Fermat's Last Theorem},
  |                                            ^^^^^^
4 |   journal   = {The Annals of Mathematics},
  |
help: Protect with braces: `{Fermat}`

Found 2 errors.
[*] 2 fixable with the `--fix` option.
```

Pass `--fix` to apply the auto-fixable ones in place:

```
Usage: betterbib check [OPTIONS] <INPUT_FILE>

Arguments:
  <INPUT_FILE>  File to check

Options:
      --fix   Apply fixes to resolve lint violations
  -h, --help  Print help
```

| Rule  | Checks for |
| ----- | ---------- |
| BIB01 | Fields valid only in BibLaTeX used in a BibTeX file |
| BIB02 | Entry types valid only in BibLaTeX used in a BibTeX file |
| BIB04 | Consecutive whitespace in field values |
| BIB05 | Malformed DOIs |
| BIB07 | Duplicate fields within an entry |
| BIB08 | Duplicate citation keys |
| BIB09 | Given names not matching the configured abbreviation style |
| BIB10 | Journal names not matching the configured abbreviation style |
| BIB12 | Inconsistent `location`/`address` style (with/without US state) |
| BIB13 | Incorrectly formatted `month` field |
| BIB14 | Wrong page-range separator |
| BIB15 | Unprotected capitalized words in titles |
| BIB16 | Missing fields required for the entry type |
| BIB17 | Problematic/non-normalized Unicode |
| BIB18 | Old-style DOI URLs |
| BIB19 | Malformed ISBN/ISSN |
| BIB22 | `title`/`chapter`/`booktitle`/`series` holding the same text |
| BIB23 | Two-person eponyms (e.g. `Cauchy-Riemann`) spelled with a hyphen instead of an en dash |
| BIB24 | Unescaped TeX-reserved characters (`&`, `%`, `#`) |
| BIB25 | BibLaTeX `pages` holding a publisher article number instead of a page range |
| BIB26 | Undecoded XML/HTML entities (e.g. `&amp;`) |

Configure rule behavior, or disable individual rules, via `betterbib.toml`:

```toml
[lint]
journal-abbreviation = "abbreviated"  # "abbreviated" or "full"
given-name-style = "abbreviated"      # "abbreviated" or "full"
page-range-separator = "--"
location-style = "with-state"         # "with-state" or "without-state"
ignore = ["BIB12", "BIB16"]
```

#### Convert

```sh
betterbib convert in.bib out.ris
```

converts between BibTeX, BibLaTeX, RIS, and CSL-JSON. The format is inferred
from each file's extension; for `.bib` files specifically, a filename ending
in `-biblatex` (e.g. `library-biblatex.bib`) is treated as BibLaTeX, anything
else as plain BibTeX. This same rule decides the dialect for `sync` and
`check` as well — it isn't configurable.

```
Usage: betterbib convert <INPUT_FILE> <OUTPUT_FILE>

Arguments:
  <INPUT_FILE>   input file
  <OUTPUT_FILE>  output file

Options:
  -h, --help  Print help
```

#### Dereference DOIs

Given a DOI, generate a bibliography entry for it directly, without an input
file:

```sh
betterbib doi-to ris 10.1002/andp.19053221004
```

```ris
TY - JOUR
TI - Zur Elektrodynamik Bewegter Körper
JF - Annalen der Physik
VO - 322
IS - 10
SP - 891
EP - 921
PB - Wiley
SN - 0003-3804, 1521-3889
UR - https://doi.org/10.1002/andp.19053221004
DI - 10.1002/andp.19053221004
DS - Crossref
```

```
Usage: betterbib doi-to [OPTIONS] <OUTPUT_FORMAT> <DOI>

Arguments:
  <OUTPUT_FORMAT>  output format [possible values: biblatex, bibtex, csl-json, ris]
  <DOI>            doi

Options:
      --source <SOURCE>  Data source [default: crossref] [possible values: crossref, dblp]
  -h, --help             Print help
```

#### Cache

`sync` and `doi-to` cache online responses locally.

```sh
betterbib cache dir    # show the cache directory
betterbib cache clear  # clear the cache
```

### Configuration

betterbib looks for a `betterbib.toml` file in the current directory or any
parent directory. All options shown above (`[sync]`, `[format]`, `[lint]`)
live in this single file; see the snippets above for the available keys and
their defaults.

You can also override config for a single file by adding a header comment
block starting with `// betterbib:`:

```bibtex
// betterbib: format.keyword-case = "upper"
// sync.sources = ["crossref"]

@article{...}
```
