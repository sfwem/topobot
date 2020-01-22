TopoBot - AREDN Mesh Network Topology Bot
=========================================

TopoBot is a command-line tool to generate topology graphs of AREDN Mesh
Networks.

From VE3IRR\'s \"bbhn-tools\":

> Each mesh node appears in an oval. Arrows between nodes indicate the
> link cost (i.e. expected number of transmissions required per packet).
> Solid lines between nodes indicate Ethernet links. Nodes beginning
> with the same call sign are grouped together.

Additionally, TopBot can be run as a Slack bot and will respond to
queries in a Slack group.

::: {.contents depth="2"}
:::

Usage
-----

There are two modes in which you can use TopBot:

:   1.  Command Line
    2.  Slack Bot

### Command Line Usage

Generate a PNG of the Mesh Network Topology from the command line:

    $ topobot -p
    /var/folders/nl/7nqyxlfn05dgqlmvfyc13jc00000gn/T/tmp8txp7udf.png
    $ open -a preview  /var/folders/nl/7nqyxlfn05dgqlmvfyc13jc00000gn/T/tmp8txp7udf.png

Generate a GraphViz DOT of the Mesh Network Topology from the command
line:

    $ topobot -p
    /var/folders/nl/7nqyxlfn05dgqlmvfyc13jc00000gn/T/tmp8txp7udf.dot

### Slack Bot Usage

To run TopoBot as a Slack bot:

    $ export SLACKBOT_API_TOKEN='xoxb-XXXX-XXXX'
    $ topobot -s

Once TopoBot is running as a Slack bot, you can message the bot with the
phrase **current**, and the bot will reply with a PNG of the current
AREDN Mesh Network Topology.

Environment
-----------

TopoBot uses between 0 and 2 environment variables:

-   `TOPO_HOST`: (optional) AREDN Mesh Network host running OLSR from
    which to query topology data. By default uses
    `localnode.local.mesh`.
-   `SLACKBOT_API_TOKEN`: (optional) Slack Bot API Token.

Installation
------------

On most Debian or Ubuntu-based Linux systems you\'ll need the
**graphviz** and **imagemagick** packages installed:

    $ sudo apt-get install graphviz imagemagick -y

Then install TopoBot from PyPI:

    $ pip install topobot

Source
------

Github: <https://github.com/ampledata/topobot>

Authors
-------

-   [Greg Albrecht W2GMD (\@ampledata)](https://github.com/ampledata):
    TopoBot Slack Bot & Command Line Client.
-   [Clayton Smith VE3IRR (\@argilo)](https://github.com/argilo):
    [topology.py]{.title-ref}, the basis for [functions.py]{.title-ref}.

Copyright
---------

-   TopoBot Slack Bot & Command Line Client: Copyright 2020 Greg
    Albrecht
-   bbhn-utils: Copyright 2014-2018 Clayton Smith

License
-------

-   TopoBot Slack Bot & Command Line Client: Apache License, Version 2.0
-   bbhn-utils: GNU General Public License 3
