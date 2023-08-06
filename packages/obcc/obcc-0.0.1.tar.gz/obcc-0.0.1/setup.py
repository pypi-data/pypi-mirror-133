# -*- coding: utf-8 -*-
"""
    Author: Lorenzo
    Email : zetatez@icloud.com
    """

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="obcc",
    version="0.0.1",
    author="Lorenzo",
    author_email="zetatez@icloud.com",
    description="ocean base data consistency check.",
    url='https://github.com/zetatez/obcc',
    packages=setuptools.find_packages(),
    install_requires=[
        "dbutils", "loguru", "mysql-connector-python", "protobuf"
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.1',
)
# python setup.py sdist bdist_wheel
# twine upload dist/*
