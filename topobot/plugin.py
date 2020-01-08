#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TopoBot Plugin."""

import re

import slackbot

import topobot

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2020 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


@slackbot.bot.default_reply
def default_handler(message: str) -> None:
    message.reply(topobot.HELP_CMDS)


@slackbot.bot.respond_to('current', re.IGNORECASE)
def current_topography(message: str) -> None:
    topo_dot = topobot.gen_dot()
    topo_png = topobot.dot2png(topo_dot)
    message.channel.upload_file('Topography', topo_png)

@slackbot.bot.respond_to('current2', re.IGNORECASE)
def current2_topography(message: str) -> None:
    topo_dot = topobot.gen_dot(span=2)
    topo_png = topobot.dot2png(topo_dot)
    message.channel.upload_file('Topography', topo_png)
