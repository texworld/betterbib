# -*- coding: utf-8 -*-
#
import os
from setuptools import setup
import codecs

from betterbib import __version__, __author__, __author_email__


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
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    packages=['betterbib'],
    description='y meshes, Voronoi regions',
    long_description=read('README.rst'),
    url='https://github.com/nschloe/betterbib',
    download_url='https://pypi.python.org/pypi/matplotlib2tikz',
    license='License :: OSI Approved :: MIT License',
    platforms='any',
    requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
        ],
    )
