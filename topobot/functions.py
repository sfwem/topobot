#!/usr/bin/env python3

# Copyright 2014-2018 Clayton Smith
#
# This file is part of bbhn-utils
#
# bbhn-utils is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# bbhn-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bbhn-utils; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import urllib.request
import socket
import os
import shlex
import subprocess
import tempfile

#import dns

import topobot


def get_table(lines, table_name):
    lines = lines[lines.index("Table: " + table_name) + 2:]
    lines = lines[:lines.index("")]
    return [line.split("\t") for line in lines]


def get_host(ip: str, resolver: str = None):
    #resolver = resolver or ip
    #res = dns.resolver.Resolver()
    #res.nameservers = [resolver]
    #dns.resolver.override_system_resolver(res)
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host.replace('.local.mesh', '').replace('-', "-\\n", 1)
    except socket.herror:
        return ip


def get_call(host):
    i = host.find('-')
    if i == -1:
        return host
    else:
        return host[:i].upper()


def round_cost(cost):
    if cost == 'INFINITE':
        return cost
    else:
        cost = float(cost)
        return "{0:.1f}".format(cost)


def print_link(t):
    if t[4] == "0.100":  # Ethernet connection
        print('    "' + t[6] + '" -> "' + t[5] + '" [dir=none, penwidth=3];')
    else:
        if t[4] == 'INFINITE':
            darkness = 0.0
        else:
            darkness = 1.0 / float(t[4])
        gray = "gray" + str(int(65.0 * (1.0 - darkness)))
        print('    "' + t[6] + '" -> "' + t[5] + '" [label="' +
              round_cost(t[4]) + '",color=' + gray + ',fontcolor=' +
              gray + '];')


def prune_topology(nodes, topology):
    ethernetSpanningForest: set = set()
    visited: set = set()

    for node, links in nodes.items():
        if node in visited:
            continue

        spanningTree = []
        toVisit = [(node, None)]

        while len(toVisit) > 0:
            currentNode, link = toVisit.pop()

            if currentNode in visited:
                continue

            visited.add(currentNode)

            if link:
                ethernetSpanningForest.add(tuple(link))

            for link in nodes[currentNode]:
                if link[4] == "0.100":
                    toVisit.append((link[0], link))

    return [t for t in topology if t[4] != "0.100" or tuple(t) in
            ethernetSpanningForest]


def get_olsr(topo_host=topobot.TOPO_HOST, topo_port=topobot.TOPO_PORT):
    topo_url = "http://" + topo_host + ":" + str(topo_port) + "/"
    lines = urllib.request.urlopen(topo_url).readlines()
    lines = [line.decode().strip() for line in lines]
    return lines


def gen_dot():
    dot_data = get_olsr()
    topology = get_table(dot_data, 'Topology')
    hna = get_table(dot_data, 'HNA')

    output = ''

    # Look up DNS names of hosts and create node dictionary
    nodes = {}

    for t in topology:
        t.append(get_host(t[0]))
        t.append(get_host(t[1]))
        nodes.setdefault(t[1], []).append(t)

    topology = prune_topology(nodes, topology)

    groups = {}
    nongroups = []

    for t in topology:
        dstCall = get_call(t[5])
        srcCall = get_call(t[6])
        if dstCall == srcCall:
            if dstCall in groups:
                groups[dstCall].append(t)
            else:
                groups[dstCall] = [t]
        else:
            nongroups.append(t)

    output += "digraph topology {"

    for h in hna:
        if h[0] == "0.0.0.0/0":
            output += '  "' + get_host(h[1]) + '" [fillcolor = yellow]'

    for call, links in groups.items():
        output += "  subgraph cluster_" + call + " {"
        output += "    style=dotted;"

        for t in links:
            if t[4] == "0.100":  # Ethernet connection
                output += '    "' + t[6] + '" -> "' + t[5] + '" [dir=none, penwidth=3];'
            else:
                if t[4] == 'INFINITE':
                    darkness = 0.0
                else:
                    darkness = 1.0 / float(t[4])
                gray = "gray" + str(int(65.0 * (1.0 - darkness)))
                output += (
                    '    "' + t[6] + '" -> "' + t[5] + '" [label="' +
                    round_cost(t[4]) + '",color=' + gray + ',fontcolor=' +
                    gray + '];'
                )


        output += "  }"

    for t in nongroups:
        if t[4] == "0.100":  # Ethernet connection
            output += '    "' + t[6] + '" -> "' + t[5] + '" [dir=none, penwidth=3];'
        else:
            if t[4] == 'INFINITE':
                darkness = 0.0
            else:
                darkness = 1.0 / float(t[4])
            gray = "gray" + str(int(65.0 * (1.0 - darkness)))
            output += (
                '    "' + t[6] + '" -> "' + t[5] + '" [label="' +
                round_cost(t[4]) + '",color=' + gray + ',fontcolor=' +
                gray + '];'
            )

    output += '}'

    return output


def dot2png(dot_data):

    tmp_fd, tmp_file = tempfile.mkstemp()
    os.close(tmp_fd)

    with open(tmp_file, 'w') as ofd:
        ofd.write(dot_data)

    dot_cmd: str = (
        "dot -Tpng -Ncolor=grey -Nstyle=filled -Nfillcolor=white "
        "-Nfontcolor=red -Nwidth=1 -Nfontsize=10 -Efontsize=10 "
        "-Gbgcolor=grey %s -o %s" % (tmp_file, tmp_file + '.1.png')
    )
    dot_args: list = shlex.split(dot_cmd)
    dot_proc = subprocess.Popen(
        dot_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dot_proc.communicate()

    convert_cmd: str = (
        r"convert %s -background \#C0C0C0 -gravity East "
        "-append %s" % (tmp_file + '.1.png', tmp_file + '.2.png')
    )
    convert_args: list = shlex.split(convert_cmd)
    convert_proc = subprocess.Popen(
        convert_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    convert_proc.communicate()

    return tmp_file + '.2.png'
