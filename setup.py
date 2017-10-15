# -*- coding: utf-8 -*-
#
import os
from setuptools import setup
import codecs

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'betterbib', '__about__.py'), 'rb') as f:
    exec(f.read(), about)


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content


setup(
    name='betterbib',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=['betterbib'],
    description='Better BibTeX data',
    long_description=read('README.rst'),
    url='https://github.com/nschloe/betterbib',
    download_url='https://pypi.python.org/pypi/betterbib',
    license=about['__license__'],
    platforms='any',
    install_requires=[
        'pipdate',
        'pybtex >= 0.19.0',
        'pypandoc',
        'requests',
        'tqdm',
        ],
    classifiers=[
        about['__status__'],
        about['__license__'],
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities'
        ],
    scripts=[
        'tools/betterbib',
        'tools/doi2bibtex'
        ]
    )
