from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'MinMaxScaler for AI'
LONG_DESCRIPTION = 'A package that allows to make a list smaller by keeping the proportion. Source code: '

# Setting up
setup(
    name="WhatScaler",
    version=VERSION,
    author="GodZilo (Ido Barel)",
    author_email="<vikbarel5@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'AI', 'Scaler', 'MinMaxScaler', 'numpy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)