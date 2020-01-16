#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TopoBot Commands."""

import argparse
import sys
import logging
import logging.config

from slackbot import settings
from slackbot.bot import Bot  # NOQA pylint: disable=C0413

import topobot

settings.PLUGINS = ['topobot.plugin']
settings.DEBUG = True


__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2020 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def cli() -> None:
    """
    Default Command Line function.
    """
    parser = argparse.ArgumentParser(description='TopoBot')

    parser.add_argument(
        '-p',
        dest='png',
        action='store_true',
        help='Runs a one-off Topology Rendering and returns a PNG.'
    )
    parser.add_argument(
        '-b',
        dest='bot_mode',
        action='store_true',
        help='Runs TopoBot as a Slack Bot.'
    )
    parser.add_argument(
        '-d',
        dest='dot',
        action='store_true',
        help='Runs a one-off Topology Rendering and returns a DOT.'
    )
    args = parser.parse_args()

    if args.png:
        run_png()
    elif args.dot:
        run_dot()
    elif args.bot_mode:
        run_bot()
    else:
        parser.print_help()


def run_png() -> None:
    """
    One-off command that returns path to a PNG file.
    """
    topo_dot = topobot.gen_dot()
    topo_png = topobot.dot2png(topo_dot)
    print(topo_png)


def run_dot() -> None:
    """
    One-off command that returns path to a DOT file.
    """
    topo_dot = topobot.gen_dot()
    topo_dot = topobot.save_dot(topo_dot)
    print(topo_dot)


def run_bot() -> None:
    """
    Runs the Bot.
    """
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
    print('Starting TopoBot as a Slack Bot...')
    bot.run()


if __name__ == '__main__':
    cli()
