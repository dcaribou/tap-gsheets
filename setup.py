#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-gsheets",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_gsheets"],
    install_requires=[
        "singer-python>=5.0.12",
        "gspread",
        "oauth2client",
        "pyhocon",
        "genson",
        "inflection"
    ],
    entry_points="""
    [console_scripts]
    tap-gsheets=tap_gsheets:main
    """,
    packages=["tap_gsheets"],
    package_data = {
        "schemas": ["tap_gsheets/schemas/*.json"]
    },
    include_package_data=True,
)
