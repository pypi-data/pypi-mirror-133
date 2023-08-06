#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import shutil
import subprocess
import re

from setuptools import find_packages
from setuptools import setup

setup(
    name='argoap',
    version='1.0.0',
    license='MIT',
    description='test version',
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    package_data={
      'argoap': ['*','*/*','bin/*/*', 'example/*/*'],
    },
    # install_requires=requirements,
    entry_points={
        'console_scripts': [
            'argoap = argoap.argoap:main',
        ]
    }
)
