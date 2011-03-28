#!/usr/bin/env python

from data_gc_ca_api.__version__ import version
try:
        from setuptools import setup, find_packages
except ImportError:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup, find_packages


setup(name='data-gc-ca-api',
    version='0.1',
    license="'GPL3' or 'Apache 2'",
    description='Utility for Accessing Environment Canada Data',
    author='Ian Gable',
    author_email='ian@gable.ca',
    url='https://github.com/igable',
    scripts=['weatherca'],
    packages=['data_gc_ca_api'],
)
