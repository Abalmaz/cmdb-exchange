#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(name='Cmdb Exchange Library',
      version='1.0',
      description='Python library for CMDB and IPRM',
      packages=find_packages(where="src"),
      package_dir={"": "src"},
     )
