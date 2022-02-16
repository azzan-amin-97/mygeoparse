#!/usr/bin/env python
import os
from setuptools import find_packages, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mygeoparse",
    version="0.0.9",
    description='Malaysia Address Parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/azzan-amin-97/tlo-my-address-parser.git',
    download_url='https://github.com/azzan-amin-97/tlo-my-address-parser/archive/refs/heads/master.zip',
    author="Azzan Amin",
    author_email='ibnuamin97@thelorry.com',
    packages=["mygeoparse"],
    keywords=['address', 'parser', 'ner'],
    license='MIT',
    install_requires=['spacy>=2.3.2', 'pandas'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ]
)
