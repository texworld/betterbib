import os
import codecs

from setuptools import setup, find_packages

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "betterbib", "__about__.py"), "rb") as f:
    exec(f.read(), about)


def read(fname):
    return codecs.open(os.path.join(base_dir, fname), encoding="utf-8").read()


setup(
    name="betterbib",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    packages=find_packages(),
    package_data={"betterbib": ["data/journals.json"]},
    description="Better BibTeX data",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url=about["__website__"],
    license=about["__license__"],
    platforms="any",
    install_requires=[
        "latexcodec",
        "pybtex >= 0.19.0",
        "pyenchant",
        "requests",
        "requests_cache",
        "tqdm",
    ],
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "betterbib = betterbib.cli.full:main",
            "betterbib-dedup-doi = betterbib.cli.dedup_doi:main",
            "betterbib-doi2bibtex = betterbib.cli.doi2bibtex:main",
            "betterbib-format = betterbib.cli.format:main",
            "betterbib-journal-abbrev = betterbib.cli.journal_abbrev:main",
            "betterbib-sync = betterbib.cli.sync:main",
        ]
    },
)
