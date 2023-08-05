#!/usr/bin/env python
######################################################################
#                                                                    #
#              Copyright Arun Goud Akkala 2021.                      #
#  Distributed under the Boost Software License, Version 1.0.        #
#          (See accompanying LICENSE file or copy at                 #
#            https://www.boost.org/LICENSE_1_0.txt)                  #
#                                                                    #
######################################################################

from setuptools import find_packages, setup


def get_version_and_cmdclass(package_name):
    """Load version.py module without importing the whole package.

    Version picked up comes from git tag.
    """
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("version", os.path.join(package_name, "_version.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


version, cmdclass = get_version_and_cmdclass("gdschamfer")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gdschamfer",
    version=version,
    cmdclass=cmdclass,
    python_requires=">=3.8",
    description=("Python add-on module for gdspy that can perform chamfering operation on GDSII files."),
    url="https://github.com/arun-goud/gdschamfer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=("arun-goud"),
    author_email="72409952+arun-goud@users.noreply.github.com",
    license="Boost Software License - Version 1.0",
    install_requires=["gdspy"],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    zip_safe=False,
)