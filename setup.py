#!/usr/bin/env python
import sys

from data_gc_ca_api.__version__ import version
try:
        from setuptools import setup, find_packages
except ImportError:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup, find_packages

if float(sys.version[:3]) >= 2.7:
    required_packages = []
else:
    required_packages = ["elementtree>=1.2.7"]
 


setup(name='data-gc-ca-api',
    version = version,
    license = "'GPL3' or 'Apache 2'",
    description = 'Utility for Accessing Environment Canada Data',
    author = 'Ian Gable',
    author_email = 'ian@gable.ca',
    url = 'https://github.com/igable/data-gc-ca-api',
    scripts=['weatherca'],
    packages = ['data_gc_ca_api'],
    install_requires = required_packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],
    
)
