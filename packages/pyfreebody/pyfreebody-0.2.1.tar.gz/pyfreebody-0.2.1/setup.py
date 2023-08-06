#!/usr/bin/env python3
from setuptools import setup, find_packages
setup(
    name='pyfreebody',
    version='0.2.1',
    author="Daniel Rosel",
    url="https://github.com/danalves24com/pyfreebody",
    description=("Pyfreebody is an easy tool to create free-body diagrams. See how to use at https://github.com/danalves24com/pyfreebody/blob/main/docs.org"),
    packages=find_packages(include=['pyfreebody']),
        install_requires=[
            "Pillow"
        ]

)
