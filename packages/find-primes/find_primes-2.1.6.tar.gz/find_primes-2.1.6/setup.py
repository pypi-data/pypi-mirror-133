from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'find_primes',
    version = '2.1.6',
    author = 'JamesJ',
    author_email = 'GGJamesQQ@yeah.net',
    description = 'A module for finding primes and finding factors of big numbers.',
    install_requires = ['numpy', 'rsa'],
    python_requires = '>=3.6.0',
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    url = 'https://github.com/git4robot/pypi_find_primes',
    packages = ['find_primes'],
    scripts = ['bin/find_primes.py'],
    long_description = long_description,
    long_description_content_type = 'text/markdown',
)