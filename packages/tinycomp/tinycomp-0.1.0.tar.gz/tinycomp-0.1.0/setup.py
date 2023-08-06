#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'numpy'
]

setup_requirements = requirements.copy()
test_requirements = [ ]

setup(
    author="Julian Lehrer",
    author_email='jmlehrer@ucsc.edu',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
  description=" A Python library for doing computations on small subsets of a DataFrame too large to fit in memory.",
    install_requires=requirements,
    license="MIT license",
    long_description="TinyComp is a Python library for doing computations on small subsets of a numeric .csv data file too large to fit entirely in memory. The library follows similarly to the Pandas API. Originally developed for my research at the UCSC Genomics Insitute with massive single-cell datasets, this library serves to be a minimal and quick tool for analysis on large datasets.",
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='tinycomp',
    name='tinycomp',
    packages=find_packages(include=['tinycomp', 'tinycomp.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jlehrer1/tinycomp',
    version='0.1.0',
)
