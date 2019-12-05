#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TopoBot Commands."""

import argparse
import os
import sys
import logging
import logging.config

import topobot

from slackbot import settings

settings.PLUGINS = ['topobot.plugin']
settings.ERRORS_TO = os.environ.get('SLACK_ERRORS_TO', 'gba')
settings.DEBUG = True

from slackbot.bot import Bot  # NOQA pylint: disable=C0413


__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def cli():
    parser = argparse.ArgumentParser(description='TopoBot')
    parser.add_argument('-c', dest='cron', action='store_true')
    args = parser.parse_args()

    if args.cron:
        run_cron()
    else:
        run_bot()

def run_cron():
    topo_dot = topobot.gen_dot()
    topo_png = topobot.dot2png(topo_dot)
    # TODO

def run_bot():
    lkw = {
        'format': (
            '%(asctime)s topobot %(levelname)s '
            '%(name)s.%(funcName)s:%(lineno)d - %(message)s'
        ),
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**lkw)
    logging.getLogger(
        'requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)

    bot = Bot()
    print('Starting TopoBot...')
    bot.run()


if __name__ == '__main__':
    cli()
