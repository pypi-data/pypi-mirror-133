#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name='opia',
    version='1.0.2',
    description='Opia Package',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Melih Colpan',
    author_email='melihcolpan1@gmail.com',
    url='https://github.com/melihcolpan/opia',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "pandas", "scipy"
    ],
    packages=find_packages(include=["opia", "opia.*"], exclude=('tests', 'docs'))
)
