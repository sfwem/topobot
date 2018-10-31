#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TopoBot Plugin."""

import re

import slackbot

import topobot

__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


@slackbot.bot.default_reply
def default_handler(message):
    message.reply(topobot.HELP_CMDS)


@slackbot.bot.respond_to('current', re.IGNORECASE)
def current_topography(message):
    topo_dot = topobot.gen_dot()
    topo_png = topobot.dot2png(topo_dot)
    message.channel.upload_file('Topography', topo_png)
