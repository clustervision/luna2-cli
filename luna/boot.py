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

import json
from datetime import datetime
from textwrap import wrap
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
        boot_show.add_argument('-a', '--all', action='store_true', default=None,
                               help='Every node in scope, not only the ones in this boot')
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

    # The steps a node reports, in the order the installer runs them, folded into the
    # stretches somebody watching a cluster come up actually distinguishes between.
    #
    # lpart reports three phases of its own, and they are not the operator's pre, part
    # and post scripts: pre prepares lpart's runtime, part carries the partitioning
    # together with the image download and extract, post finalises the bootloader. They
    # sit in the same stretches of the flow as the classic steps around them, so they
    # fold into the same stages and the ladder is the same shape whichever installer the
    # node ran. install.lpart_unavailable is deliberately absent: it is a warning, the
    # node carries on down the classic path and reports download and unpack from there.
    #
    # The percentage is how much of a boot is behind a node reporting that stage. The
    # stretches are not equal work - being handed an installer is quick, fetching and
    # unpacking the image is most of the wait - and these are estimates of effort rather
    # than measurements, here so a number can be read at a glance.
    BOOT_STAGES = [
        ('discovered', ('discovered',), 5),
        ('rendered', ('rendered',), 10),
        ('prepare', ('scripts', 'prescript', 'lpart.pre', 'setupbmc', 'partscript',
                     'started'), 20),
        ('download', ('download', 'downloaded'), 45),
        ('unpack', ('unpack', 'lpart.part'), 70),
        ('configure', ('setnet', 'secrets', 'postscript', 'lpart.post', 'roles',
                       'profiles', 'image', 'finalizing'), 85),
        ('success', ('success', 'completed'), 95),
        ('booted', ('booted',), 100),
    ]

    # Each bar answers one question: how many of this boot have got past here. So a
    # milestone names the stage a node has to have *reached* to count as having passed
    # it - a node reporting prescript is in the prepare stretch, not through it. The
    # counts therefore descend, and the bar that has stopped moving is where the cluster
    # is being held.
    BOOT_MILESTONES = [
        ('discovered', 0, 'ipxe asked for a boot'),
        ('rendered', 1, 'installer handed out'),
        ('prepared', 3, 'scripts, prescript, bmc, partscript'),
        ('downloaded', 4, 'image fetched'),
        ('unpacked', 5, 'unpack, or the lpart part phase'),
        ('configured', 6, 'setnet, secrets, postscript, roles, profiles'),
        ('booted', 7, 'up and reported in'),
    ]
    BAR_WIDTH = 20

    # A node that has not reported for this long, and has not booted, is not slow: it
    # has stopped. An hour is a judgement rather than a measurement - a large image over
    # a slow link genuinely takes a while - but nothing healthy sits in one step for an
    # hour, and a threshold that never fires is worth less than one occasionally argued
    # with. It is the timestamp's real job: the anchor tells you which boot, this tells
    # you which nodes are not coming.
    STUCK_MINUTES = 60

    # How many stuck nodes are named before the rest become a count. A boot does not go
    # wrong for one node, it goes wrong for a rack or a switch at a time, and five
    # hundred names in a table cell tell an operator less than the count does. What
    # identifies the fault at that scale is the stage they all stopped in, so that is
    # summarised first and always, and the names are the detail behind it.
    STUCK_LISTED = 12

    # Nothing in this block is allowed past this, wrapped across rows if it has to be.
    # Every count here is bounded, but a node name is not: names run to a rack and a
    # position on real clusters, so a fixed number of them is not a fixed width.
    ROW_WIDTH = 96

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


    def node_stage(self, status=None):
        """
        Which stage of the ladder a reported state belongs to, as an index, or None for
        a node that has not reported one. Matching is on the step rather than the whole
        string, so a change to how the daemon words it does not silently drop a node.
        """
        if not status or status in ('None', 'none'):
            return None
        lowered = str(status).lower()
        for index, (_, steps, _) in enumerate(self.BOOT_STAGES):
            if any(step in lowered for step in steps):
                return index
        return None


    def step_progress(self, status=None):
        """How far through a boot a node is, as a percentage."""
        stage = self.node_stage(status)
        if stage is None:
            return 0
        return self.BOOT_STAGES[stage][2]


    def progress_bar(self, percent=None):
        """A percentage as something the eye reads before the number does."""
        filled = int(round(percent * self.BAR_WIDTH / 100))
        return '[' + ('#' * filled) + ('.' * (self.BAR_WIDTH - filled)) + ']'


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
        buckets, progress, scope = {}, {}, []
        for name in sorted(nodes):
            node = nodes[name]
            if self.args.get('group') and node.get('group') != self.args['group']:
                continue
            scope.append(name)
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
            # every other key here is group/osimage and carries a slash, so this one
            # cannot collide with them and anything already reading this output keeps
            # finding exactly what it found before
            data['progress'] = self.boot_progress(scope)
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
        Presenter().show_table(' << Boot Overview >>', fields, rows)
        return self.show_progress(scope)


    def node_states(self):
        """
        What every node last reported, and when. The monitor route is a three column
        join where the node route is the whole record for every node, which at a few
        thousand nodes is the difference worth one extra call. The state comes back
        prefixed with the node's own name, and that prefix is stripped here rather than
        matched around: a node called download01 would otherwise read as a node
        downloading.
        """
        states = {}
        get_list = Rest().get_raw('monitor/node')
        if not (get_list and get_list.content):
            return states
        try:
            data = json.loads(get_list.content.decode('utf-8'))
        except ValueError as error:
            self.logger.debug(f'Monitor node states unreadable => {error}')
            return states
        for name, entry in (data.get('monitor', {}).get('status', {}).get('node', {})).items():
            state = str(entry.get('state') or '')
            if state.startswith(f'{name} '):
                state = state[len(name) + 1:]
            states[name] = {'state': state, 'updated': entry.get('updated')}
        return states


    def boot_cohort(self, states=None, scope=None):
        """
        Which nodes are in the boot happening now, which is the number every bar divides
        by. It cannot be read from the state alone: a node that finishes reports booted
        and is then indistinguishable from one that booted a month ago, so a set defined
        that way would shrink as nodes succeed and the bars would never fill.

        So it is anchored on the nodes still in flight - the oldest report among them is
        when this boot started, and everything that has reported since belongs to it.
        No window to configure and no interval to guess at.

        A node stuck for days is still in flight and drags that anchor back with it,
        which widens the cohort to whatever has reported since. That is a dilution and
        not a distortion: the extra nodes are ones that finished, they sit at the top of
        every bar, and the shape of the progression is unchanged. The floor of the
        degradation is every node in scope, which is what --all asks for outright and
        what an older daemon that does not stamp the row leaves us with anyway. The node
        holding the anchor back is named in the view, so it is never a mystery.
        """
        known = [name for name in scope if states.get(name, {}).get('state')]
        last = len(self.BOOT_STAGES) - 1
        inflight = [name for name in known if self.node_stage(states[name]['state']) != last]
        if self.args.get('all') or not inflight:
            return known, False
        stamps = [states[name]['updated'] for name in inflight if states[name].get('updated')]
        if not stamps:
            return known, False
        oldest = min(stamps)
        return [name for name in known
                if str(states[name].get('updated') or '') >= oldest], True


    def age(self, minutes=None):
        """Minutes as something an operator reads without counting zeroes."""
        if minutes < 60:
            return f'{minutes}m'
        return f'{minutes // 60}h{minutes % 60:02d}m'


    def stuck_nodes(self, states=None, scope=None):
        """
        Nodes that went quiet mid-install: not booted, and nothing heard from them for
        longer than a boot takes. Worst first.

        A boot has always had these and never shown them. They are also what drags the
        cohort anchor back - a node stuck since last week is still in flight - so the
        same line explains the stragglers and why the cohort is the size it is.
        """
        last = len(self.BOOT_STAGES) - 1
        now = datetime.utcnow()
        stuck = []
        for name in scope:
            entry = states.get(name) or {}
            stage = self.node_stage(entry.get('state'))
            if stage is None or stage == last or not entry.get('updated'):
                continue
            try:
                since = datetime.strptime(str(entry['updated']), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue
            minutes = int((now - since).total_seconds() // 60)
            if minutes >= self.STUCK_MINUTES:
                stuck.append({'node': name, 'minutes': minutes,
                              'stage': self.BOOT_STAGES[stage][0]})
        return sorted(stuck, key=lambda node: -node['minutes'])


    def boot_progress(self, scope=None):
        """
        Where the nodes in scope are on the ladder. One entry per milestone, counting
        every node that has reached it or gone past it.
        """
        states = self.node_states()
        cohort, anchored = self.boot_cohort(states, scope)
        if not cohort:
            return None
        reported = [self.node_stage(states[name]['state']) for name in cohort]
        reported = [stage for stage in reported if stage is not None]
        data = {
            'nodes': len(cohort),
            'anchored': anchored,
            'stuck': self.stuck_nodes(states, cohort),
            'total': int(round(sum(self.BOOT_STAGES[stage][2] for stage in reported)
                               / len(cohort))) if reported else 0,
            'milestones': []
        }
        for label, threshold, note in self.BOOT_MILESTONES:
            count = len([stage for stage in reported if stage >= threshold])
            data['milestones'].append({
                'milestone': label, 'nodes': count, 'note': note,
                'progress': int(round(count * 100 / len(cohort)))})
        return data


    def show_progress(self, scope=None):
        """
        The same boot read node by node rather than by group: one bar per milestone,
        under each other, so the bar that has stopped is the one being waited on.
        """
        data = self.boot_progress(scope)
        if not data:
            return Message().show_warning('No node has reported a boot state.')
        counted = 'nodes in this boot' if data['anchored'] else 'nodes, no boot in progress'
        fields = ['total']
        rows = [f"{self.progress_bar(data['total'])} {data['total']:3d}%"
                f"   {data['nodes']} {counted}"]
        for entry in data['milestones']:
            fields.append(entry['milestone'])
            rows.append(f"{self.progress_bar(entry['progress'])} {entry['progress']:3d}%"
                        f"   {entry['nodes']:>4}/{data['nodes']}   {entry['note']}")
        divider = ['total']
        if data['stuck']:
            stuck, worst = data['stuck'], data['stuck'][0]
            divider.append(fields[-1])
            by_stage = {}
            for node in stuck:
                by_stage[node['stage']] = by_stage.get(node['stage'], 0) + 1
            # one entry per stage, so this line is the same length for five nodes as
            # for five hundred - and at five hundred the stage is the diagnosis
            ranked = sorted(by_stage.items(), key=lambda item: -item[1])
            where = ', '.join(f'{count} in {stage}' for stage, count in ranked[:3])
            if len(ranked) > 3:
                where = f'{where}, {sum(count for _, count in ranked[3:])} elsewhere'
            fields.append('stuck')
            rows.append(f"{len(stuck)} silent for over {self.age(self.STUCK_MINUTES)}"
                        f"   {where}   worst {worst['node']} "
                        f"{self.age(worst['minutes'])}")
            if self.args.get('verbose'):
                named = [node['node'] for node in stuck[:self.STUCK_LISTED]]
                if len(stuck) > self.STUCK_LISTED:
                    named.append(f'and {len(stuck) - self.STUCK_LISTED} more')
                for line in wrap(', '.join(named), self.ROW_WIDTH) or ['']:
                    fields.append('')
                    rows.append(line)
        return Presenter().show_table_col(' << Boot Progress >> ', fields, rows,
                                          divider=divider)

