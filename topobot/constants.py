#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TopoBot Constants."""

import logging
import os

__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter(
    ('%(asctime)s topobot %(levelname)s %(name)s.%(funcName)s:%(lineno)d - '
     '%(message)s'))

TOPO_HOST = os.environ.get('TOPO_HOST', 'TOPO_HOST')
TOPO_PORT = int(os.environ.get('TOPO_PORT', 2006))

HELP_CMDS = """
Available Commands:

    * help
    * current - Gets Current Topography

"""
