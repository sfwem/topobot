TopoBot - AREDN Topography Bot for Slack
****************************************

Topo(graphy) Bot is a Slack bot to query and display AREDN OLSR topography information.

Usage
=====

From Slack `/msg @topobot current` to receive a PNG image of the latest topography.

Running
=======

Ensure the host running this bot has an AREDN node as a Name resolver.

Run the bot::

    export TOPO_HOST='172.17.0.1'
    export SLACKBOT_API_TOKEN='xoxb-XXXX-XXXX'
    topobot


Installation
============

You'll need to create a Slack Bot and create a Slack Bot API Token, then::

    $ sudo apt-get install graphviz
    $ sudo apt-get install imagemagick -y
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
