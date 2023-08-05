#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from setuptools import setup
import versioneer

# pull in some definitions from the package's __init__.py file
import punx


verbose = 1


setup(
    name=punx.__package_name__,  # punx
    license=punx.__license__,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=punx.__description__,
    long_description=punx.__long_description__,
    author=punx.__author_name__,
    author_email=punx.__author_email__,
    url=punx.__url__,
    # download_url     = punx.__download_url__,
    keywords=punx.__keywords__,
    platforms="any",
    install_requires=punx.__install_requires__,
    package_dir={"": "."},
    packages=["punx", "punx/validations"],
    # packages=find_packages(),
    package_data={
        "punx": [
            "cache/*.p",
            "cache/*.ini",
            "cache/*.zip",
            "cache/*/*.json",
            "cache/*/*.xsd",
            "cache/*/*/*.xml",
            "cache/*/*/*.xsl",
            "data/writer_*.hdf5",
            "LICENSE.txt",
        ],
    },
    classifiers=punx.__classifiers__,
    entry_points={
        # create & install scripts in <python>/bin
        "console_scripts": ["punx=punx.main:main", ],
        # 'gui_scripts': [],
    },
    test_suite="punx/tests",
)
