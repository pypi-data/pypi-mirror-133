#!/usr/bin/env python

# Standard library modules.
import os

# Third party modules.
from setuptools import setup, find_packages

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASEDIR, "README.md"), "r") as fp:
    LONG_DESCRIPTION = fp.read()

PACKAGES = find_packages()
PACKAGE_DATA = {}

penepmadir = os.path.join(BASEDIR, "pymontecarlo_penepma", "penepma")
for root, _dirnames, filenames in os.walk(penepmadir):
    dirpath = os.path.join("penepma", root[len(penepmadir) + 1 :])
    for filename in filenames:
        relpath = os.path.join(dirpath, filename)
        PACKAGE_DATA.setdefault("pymontecarlo_penepma", []).append(relpath)

with open(os.path.join(BASEDIR, "requirements.txt"), "r") as fp:
    INSTALL_REQUIRES = fp.read().splitlines()

EXTRAS_REQUIRE = {}

CMDCLASS = versioneer.get_cmdclass()

ENTRY_POINTS = {}

setup(
    name="pyMonteCarlo-PENEPMA",
    version=versioneer.get_version(),
    url="https://github.com/pymontecarlo",
    description="Interface of Monte Carlo simulation program PENEPMA with pyMonteCarlo",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Hendrix Demers and Philippe T. Pinard",
    author_email="philippe.pinard@gmail.com",
    license="Apache License version 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    cmdclass=CMDCLASS,
    entry_points=ENTRY_POINTS,
)
