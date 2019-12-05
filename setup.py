#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the TopoBot.

Source:: https://github.com/ampledata/topobot
"""

import os
import sys
import setuptools

__title__ = 'topobot'
__version__ = '1.0.0b1'
__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2019 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='TopoBot - Mesh Topography Bot.',
    author='Greg Albrecht',
    author_email='oss@undef.net',
    packages=['topobot'],
    package_data={'': ['LICENSE']},
    package_dir={'topobot': 'topobot'},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/topobot',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests',
        'slackbot',
        'dnspython'
    ],
    entry_points={'console_scripts': ['topobot = topobot.cmd:cli']}
)
