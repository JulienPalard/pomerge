#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="pomerge",
    version="0.1.2",
    description="Merge known translations between .po files.",
    long_description=readme,
    author="Julien Palard",
    author_email="julien@palard.fr",
    url="https://github.com/JulienPalard/pomerge",
    packages=["pomerge"],
    package_dir={"pomerge": "pomerge"},
    entry_points={"console_scripts": ["pomerge=pomerge.pomerge:main"]},
    include_package_data=True,
    install_requires=["tqdm", "polib"],
    extras_require={"dev": ["pylint", "flake8", "black", "mypy"]},
    license="MIT license",
    zip_safe=False,
    keywords="pomerge",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
