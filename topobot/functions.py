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


import shlex
import socket
import subprocess
import tempfile
import typing
import urllib.request

import topobot


def get_table(lines: typing.List, table_name: str) -> typing.List:
    """
    Gets the given Table from OLSR data.

    :param lines:
    :param table_name:
    :return:
    """
    lines = lines[lines.index("Table: " + table_name) + 2:]
    lines = lines[:lines.index("")]
    return [line.split("\t") for line in lines]


def get_host(ip: str) -> str:
    """
    Resolves IP to Hostname.

    :param ip:
    :return:
    """
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host.replace('.local.mesh', '').upper()#.replace('-', "-\\n", 1)
    except socket.herror:
        return ip


def get_call(host: str, span: int = 1) -> str:
    """
    Gets the Callsign from the Hostname.
    Given a Span, will extract that many sections of the callsign.

    For example:
    - span=1 would extract 'W2GMD' from W2GMD-SUNSET-5G-1
    - span=2 would extract 'W2GMD-SUNSET' from W2GMD-SUNSET-5G-1

    :param host: Hostname from which to extract callsign.
    :param span: Number of sections of callsign to extract.
    :return:
    """
    if '-' in host:
        segments = host.split('-')
        if len(segments) >= 1:
            if span == 0:
                return segments[0].upper()
            else:
                return ''.join(segments[:span]).upper()
        else:
            return host.upper()
    else:
        return host.upper()


def round_cost(cost: str) -> str:
    if cost == 'INFINITE':
        return cost
    else:
        cost = float(cost)
        return "{0:.1f}".format(cost)


def prune_topology(nodes, topology) -> typing.List:
    ethernet_spanning_forest: typing.Set = set()
    visited: typing.Set = set()

    for node, links in nodes.items():
        if node in visited:
            continue

        spanning_tree = []
        to_visit = [(node, None)]

        while len(to_visit) > 0:
            current_node, link = to_visit.pop()

            if current_node in visited:
                continue

            visited.add(current_node)

            if link:
                ethernet_spanning_forest.add(tuple(link))

            for link in nodes[current_node]:
                if link[4] == "0.100":
                    to_visit.append((link[0], link))

    return [t for t in topology if t[4] != "0.100" or tuple(t) in
            ethernet_spanning_forest]


def get_olsr(topo_host: str = topobot.TOPO_HOST,
             topo_port: int = topobot.TOPO_PORT) -> typing.List:
    """
    Gets OLSR routing table from Topo Host and returns as a List.

    :param topo_host: OLSR (AREDN Mesh) Host.
    :param topo_port: OLSR Port
    :return: list
    """
    topo_url = f"http://{topo_host}:{str(topo_port)}/"
    olsr_data: typing.List[str] = urllib.request.urlopen(topo_url).readlines()
    lines = [line.decode().strip() for line in olsr_data]
    return lines


def gen_dot(span: int = 1) -> str:
    """
    Generates Dot file for GraphViz.

    :return:
    """
    output: str = ""
    nodes: typing.Dict = {}
    groups: typing.Dict = {}
    nongroups: typing.List = []

    olsr_data: typing.List[str] = get_olsr()

    topology = get_table(olsr_data, 'Topology')
    hna = get_table(olsr_data, 'HNA')

    # Look up DNS names of hosts and create node dictionary
    for t in topology:
        t.append(get_host(t[0]))
        t.append(get_host(t[1]))
        nodes.setdefault(t[1], []).append(t)

    topology = prune_topology(nodes, topology)

    for t in topology:
        dst_call = get_call(t[5], span)
        src_call = get_call(t[6], span)
        if dst_call == src_call:
            if dst_call in groups:
                groups[dst_call].append(t)
            else:
                groups[dst_call] = [t]
        else:
            nongroups.append(t)

    output = "\n".join([output, "digraph topology {"])

    for h in hna:
        if h[0] == "0.0.0.0/0":
            output = "\n".join([
                output,
                f"  \"{get_host(h[1])}\" [fillcolor = yellow]"
            ])

    for call, links in groups.items():
        output = "\n".join([output, f"  subgraph cluster_{call} {{"])
        output = "\n".join([output, "    style=dotted;"])

        for t in links:
            if t[4] == "0.100":  # Ethernet connection
                output = "\n".join([
                    output,
                    '    "' + t[6] + '" -> "' + t[5] + '" [dir=none, penwidth=3];'
                ])
            else:
                if t[4] == 'INFINITE':
                    darkness = 0.0
                else:
                    darkness = 1.0 / float(t[4])

                gray = f"gray{str(int(65.0 * (1.0 - darkness)))}"

                output = "\n".join([
                    output,
                    (
                        '    "' + t[6] + '" -> "' + t[5] + '" [label="' +
                        round_cost(t[4]) + '",color=' + gray + ',fontcolor=' +
                        gray + '];'
                    )
                ])

        output = "\n".join([output, "  }"])

    for t in nongroups:
        if t[4] == "0.100":  # Ethernet connection
            output = "\n".join([
                output,
                '    "' + t[6] + '" -> "' + t[5] + '" [dir=none, penwidth=3];'
            ])
        else:
            if t[4] == 'INFINITE':
                darkness = 0.0
            else:
                darkness = 1.0 / float(t[4])

            gray = f"gray{str(int(65.0 * (1.0 - darkness)))}"

            output = "\n".join([
                output,
                (
                    '    "' + t[6] + '" -> "' + t[5] + '" [label="' +
                    round_cost(t[4]) + '",color=' + gray + ',fontcolor=' +
                    gray + '];'
                )
            ])

    output = "\n".join([output, '}'])

    return output


def save_dot(dot_data: str) -> str:
    """
    Saves the Dot file.

    :param dot_data:
    :return:
    """
    with tempfile.NamedTemporaryFile(suffix='.dot', delete=False) as dot_fd:
        dot_fd.write(dot_data.encode())
        dot_file = dot_fd.name
        return dot_file


def dot2png(dot_data: str) -> str:
    """
    Renders a PNG from a Dot file.

    :param dot_data:
    :return:
    """
    with tempfile.NamedTemporaryFile(suffix='.dot') as dot_fd:
        dot_fd.write(dot_data.encode())
        dot_file = dot_fd.name

        with tempfile.NamedTemporaryFile(suffix='.png') as png1_fd:
            png1_file = png1_fd.name

            dot_cmd: str = (
                f"dot -Tpng -Ncolor=grey -Nstyle=filled -Nfillcolor=white "
                f"-Nfontcolor=red -Nwidth=1 -Nfontsize=10 -Efontsize=10 "
                f"-Gbgcolor=grey {dot_file} -o {png1_file}"
            )

            dot_args: typing.List[str] = shlex.split(dot_cmd)
            dot_proc = subprocess.Popen(
                dot_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            dot_proc.communicate()

            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) \
                    as png2_fd:
                png2_file = png2_fd.name

                convert_cmd: str = (
                    f"convert {png1_file} -background \\#C0C0C0 -gravity East "
                    f"-append {png2_file}"
                )

                convert_args: typing.List[str] = shlex.split(convert_cmd)
                convert_proc = subprocess.Popen(
                    convert_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                convert_proc.communicate()

                return png2_file
