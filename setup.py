#!/usr/bin/env python

from distutils.core import setup

setup(
    version='0.11',
    name="runnable",
    description="Runnable django forms",
    author="Wouter van Atteveldt",
    author_email="wouter@vanatteveldt.com",
    packages=["runnable"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "django"
    ],
)
