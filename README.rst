TopoBot - AREDN Mesh Network Topology Bot
*****************************************

TopoBot is a command-line tool to generate topology graphs of AREDN Mesh Networks.

Additionally, TopBot can be run as a Slack bot and will respond to queries in a Slack group.

Usage
=====

There are two modes in which you can use TopBot:
    1. Command Line
    2. Slack Bot

Command Line Usage
==================

Generate a PNG of the Mesh Network Topology from the command line::

    $ export TOPO_HOST=127.17.0.1
    $ topobot -p
    /var/folders/nl/7nqyxlfn05dgqlmvfyc13jc00000gn/T/tmp8txp7udf.png
    $ open -a preview  /var/folders/nl/7nqyxlfn05dgqlmvfyc13jc00000gn/T/tmp8txp7udf.png

Generate a GraphViz DOT of the Mesh Network Topology from the command line::

    $ export TOPO_HOST=127.17.0.1
    $ topobot -p
    /var/folders/nl/7nqyxlfn05dgqlmvfyc13jc00000gn/T/tmp8txp7udf.dot

Slack Bot Usage
===============

To run TopoBot as a Slack bot::

    $ export TOPO_HOST=127.17.0.1
    $ export SLACKBOT_API_TOKEN='xoxb-XXXX-XXXX'
    $ topobot -s

Once TopoBot is running as a Slack bot, you can message the bot with the phrase **current**, and the bot will reply with
a PNG of the current AREDN Mesh Network Topology.

Installation
============

On most Debian or Ubuntu-based Linux systems you'll need the **graphviz** and **imagemagick** packages installed::

    $ sudo apt-get install graphviz imagemagick -y

Then install TopoBot from PyPI::

    $ pip install topobot


Source
======
Github: https://github.com/ampledata/topobot

Author
======
Greg Albrecht W2GMD oss@undef.net

http://ampledata.org/

Copyright
=========
Copyright 2020 Greg Albrecht

bbhn-utils is Copyright 2014-2018 Clayton Smith

License
=======
Apache License, Version 2.0. See LICENSE for details.

bbhn-utils is licensed GNU General Public License 3
