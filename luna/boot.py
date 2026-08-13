#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

"""
Where the cluster is in a boot.

Nothing here is new information - it is the state each node already reports, folded
into something an operator watching a thousand nodes come up can read at a glance.

Deliberately its own command rather than an action on a node: what it answers is a
question about the cluster, not about any one machine. That also leaves room for the
things that boot but are not nodes - switches being provisioned through ZTP have
their own progress, and they belong in this view rather than in a second one.
"""

__author__      = 'Antoine Schonewille'
__copyright__   = 'Copyright 2025, Luna2 Project'
__license__     = 'GPL'
__version__     = '2.2'
__maintainer__  = 'Antoine Schonewille'
__email__       = 'antoine.schonewille@clustervision.com'
__status__      = 'Development'

from operator import methodcaller
from luna.utils.constant import actions
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.message import Message


class Boot():
    """
    Boot Class responsible to show where nodes are in a boot cycle.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "boot"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_boot')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Boot class.
        """
        boot_menu = Helper().get_help_message(subparsers, self.table)
        boot_args = boot_menu.add_subparsers(dest='action', title='commands',
                                             description='Available boot operations')
        boot_show = boot_args.add_parser('status', help='Where the cluster is in a (re)boot cycle')
        boot_show.add_argument('-g', '--group', help='Only this group').completer = Helper().name_completer("group")
        boot_show.add_argument('-R', '--raw', action='store_true', default=None,
                               help='Raw JSON output')
        boot_show.add_argument('-v', '--verbose', action='store_true', default=None,
                               help='Verbose Mode')
        return parser


    # Where a node is in its boot cycle, from the state it last reported. Three phases
    # rather than the full step list: an operator watching a cluster come up wants to
    # know how many are still fetching and how many are configuring, not which of the
    # dozen post-install steps node417 is on.
    BOOT_PHASES = [
        ('ipxe', ('rendered',)),
        ('download', ('download', 'unpack')),
        ('done', ('success', 'booted')),
    ]

    # How much of a boot is behind a node reporting a given step. The three phases are
    # not equal work: getting handed an installer is quick, fetching and unpacking the
    # image is most of the wait, and the steps after it are short. Roughly a fifth,
    # three fifths, a fifth - with unpack weighted above download inside that middle
    # stretch because it is the part that takes the longest.
    #
    # These are estimates of effort, not measurements, and they are here so a number can
    # be read at a glance rather than counted across five columns.
    STEP_PROGRESS = [
        ('booted', 100), ('success', 100),
        ('unpack', 65), ('download', 35), ('rendered', 20),
    ]
    CONFIG_PROGRESS = 85

    def boot_phase(self, status=None):
        """
        The phase a reported state belongs to. Matching is on the step rather than the
        whole string, so a change to how the daemon words it does not silently drop
        every node into 'unknown'.
        """
        if not status or status in ('None', 'none'):
            return 'unknown'
        lowered = str(status).lower()
        for phase, steps in self.BOOT_PHASES:
            if any(step in lowered for step in steps):
                return phase
        if 'installer' in lowered or 'install.' in lowered:
            return 'config'
        return 'unknown'

    def step_progress(self, status=None):
        """How far through a boot a node is, as a percentage."""
        phase = self.boot_phase(status)
        if phase == 'unknown':
            return 0
        lowered = str(status).lower()
        for step, progress in self.STEP_PROGRESS:
            if step in lowered:
                return progress
        return self.CONFIG_PROGRESS

    def status_boot(self):
        """
        Method to summarise where nodes are in a (re)boot cycle, by group and the
        osimage they will actually boot - which is the node's own when it overrides
        its group's.
        """
        get_list = Rest().get_data('node')
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        if not get_list:
            return Message().show_error('No nodes are available.')
        nodes = get_list['config']['node']

        phases = [phase for phase, _ in self.BOOT_PHASES if phase != 'done']
        phases = phases + ['config', 'done', 'unknown']
        buckets, progress = {}, {}
        for name in sorted(nodes):
            node = nodes[name]
            if self.args.get('group') and node.get('group') != self.args['group']:
                continue
            key = (node.get('group') or '-', node.get('osimage') or '-')
            counts = buckets.setdefault(key, dict.fromkeys(phases, 0))
            counts[self.boot_phase(node.get('status'))] += 1
            progress.setdefault(key, []).append(self.step_progress(node.get('status')))

        if not buckets:
            return Message().show_error('No nodes matched.')
        if self.args['raw']:
            data = {}
            for (group, osimage), counts in buckets.items():
                done = progress[(group, osimage)]
                entry = dict(counts)
                entry['total'] = sum(counts.values())
                entry['progress'] = int(round(sum(done) / len(done))) if done else 0
                data[f'{group}/{osimage}'] = entry
            return Presenter().show_json(Helper().prepare_json(data))

        fields = ['#', 'group', 'osimage'] + phases + ['total', 'progress']
        rows, num = [], 1
        for (group, osimage) in sorted(buckets):
            counts = buckets[(group, osimage)]
            done = progress[(group, osimage)]
            percent = int(round(sum(done) / len(done))) if done else 0
            bar = '#' * (percent // 10) + '.' * (10 - percent // 10)
            rows.append([num, group, osimage] + [counts[phase] or '' for phase in phases]
                        + [sum(counts.values()), f'{bar} {percent}%'])
            num = num + 1
        return Presenter().show_table(' << Boot Overview >>', fields, rows)

