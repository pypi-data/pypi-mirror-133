import os
import setuptools
from setuptools import find_packages, setup


setuptools.setup(
    name="atsocatest",
    version="0.0.4",
    packages=['atsocatest'],
    author="Carlos Acosta",
    author_email="atsoca.c@gmail.com",
    description="An easy and funny example of a Python package",
    long_description="My_own_Python_package contains a simple sum",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)