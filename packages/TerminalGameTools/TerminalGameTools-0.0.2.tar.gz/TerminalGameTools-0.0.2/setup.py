#!/usr/bin/env python3
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="TerminalGameTools",
    version='0.0.2',
    author="KermitPurple (Shane McDonough)",
    description='A package to allow for terminal text-based games to be easier to create',
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=['TerminalGameTools'],
    package_dir={'': 'src'},
    install_requires=['colorama', 'getch'],
)
