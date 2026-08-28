#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.
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
Firmware Catalogue Class for the CLI
"""
__author__      = "Antoine Schonewille"
__copyright__   = "Copyright 2026, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.2"
__maintainer__  = "Antoine Schonewille"
__email__       = "antoine.schonewille@clustervision.com"
__status__      = "Development"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import actions
from luna.utils.presenter import Presenter
from luna.utils.message import Message
from luna.utils.arguments import Arguments


class FirmwareCatalog():
    """
    Firmware Catalogue Class, responsible to list, show, add, change, rename and
    remove a catalogue entry, and to say what became of the updates that were
    asked for.

    An entry is written by hand and not grabbed off a machine, which is the
    opposite of a BIOS configuration and the reason this carries an add where
    biosconfig deliberately does not: it is desired state, so it has to be
    stated. Nothing here is derived from a node - a node only ever selects an
    entry, by the hardware it reported.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "firmwarecatalog"
        self.route = "firmwarecatalog"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_firmwarecatalog')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Firmware Catalogue class.
        """
        firmware_menu = Helper().get_help_message(subparsers, self.table)
        firmware_args = firmware_menu.add_subparsers(dest='action', title='commands', description='Available firmwarecatalog operations')
        firmware_list = firmware_args.add_parser('list', help='List Firmware Catalogue Entries')
        Arguments().common_list_args(firmware_list, True)
        firmware_show = firmware_args.add_parser('show', help='Show a Firmware Catalogue Entry')
        firmware_show.add_argument('name', help='Firmware Catalogue Entry Name').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(firmware_show)
        firmware_add = firmware_args.add_parser('add', help='Add a Firmware Catalogue Entry')
        firmware_add.add_argument('name', help='Firmware Catalogue Entry Name')
        Arguments().common_firmwarecatalog_args(firmware_add)
        firmware_change = firmware_args.add_parser('change', help='Change a Firmware Catalogue Entry')
        firmware_change.add_argument('name', help='Firmware Catalogue Entry Name').completer = Helper().name_completer(self.table)
        Arguments().common_firmwarecatalog_args(firmware_change)
        firmware_rename = firmware_args.add_parser('rename', help='Rename a Firmware Catalogue Entry')
        firmware_rename.add_argument('name', help='Firmware Catalogue Entry Name').completer = Helper().name_completer(self.table)
        firmware_rename.add_argument('newfirmwarename', help='New Firmware Catalogue Entry Name')
        firmware_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        firmware_status = firmware_args.add_parser('status', help='What became of the firmware updates that were asked for')
        firmware_status.add_argument('name', nargs='?',
                                     help='Name of a single Node').completer = Helper().name_completer('node')
        firmware_status.add_argument('-g', '--group',
                                     help='Only the nodes of this Group').completer = Helper().name_completer('group')
        firmware_status.add_argument('-a', '--all', action='store_true', default=None,
                                     help='Every node, not only the ones worth looking at')
        firmware_status.add_argument('-R', '--raw', action='store_true', default=None,
                                     help='Raw JSON output')
        firmware_status.add_argument('-v', '--verbose', action='store_true', default=None,
                                     help='Verbose Mode')
        firmware_remove = firmware_args.add_parser('remove', help='Remove a Firmware Catalogue Entry')
        firmware_remove.add_argument('name', help='Firmware Catalogue Entry Name').completer = Helper().name_completer(self.table)
        firmware_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_firmwarecatalog(self):
        """
        This method list all firmware catalogue entries.
        """
        return Helper().get_list(self.table, self.args)


    def show_firmwarecatalog(self):
        """
        This method shows one firmware catalogue entry.
        """
        return Helper().show_data(self.table, self.args)


    def add_firmwarecatalog(self):
        """
        This method adds a firmware catalogue entry.
        """
        return Helper().add_record(self.table, self.args)


    def change_firmwarecatalog(self):
        """
        This method updates a firmware catalogue entry.
        """
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')


    def rename_firmwarecatalog(self):
        """
        This method renames a firmware catalogue entry.
        """
        return Helper().rename_record(self.table, self.args, self.args["newfirmwarename"])


    def remove_firmwarecatalog(self):
        """
        This method removes a firmware catalogue entry.
        """
        return Helper().delete_record(self.table, self.args)


    def status_firmwarecatalog(self):
        """
        Method to show what became of the firmware updates that were asked for.

        This is not what a node is running - 'luna node firmwarepush --dry-run'
        answers that from inventory. This answers the other question, which is
        what somebody asked for and how it ended, and the two are worth keeping
        apart: a push that never ran and a node that is already up to date look
        identical if they are reported in one column.

        Counts first and rows only for what needs action, like every status view
        here. A line per node is useful on a rack and useless on four thousand,
        where the handful still running or failed are exactly what gets buried.
        """
        uri = f'{self.route}/status'
        if self.args.get('name'):
            uri = f'{uri}/{self.args["name"]}'
        elif self.args.get('group'):
            uri = f'{uri}/group/{self.args["group"]}'
        get_list = Rest().get_data(uri)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        if not get_list:
            return Message().show_error('No firmware status available.')
        data = get_list['config'][self.table]['status']
        summary = get_list['config'][self.table].get('summary') or {}
        if self.args['raw']:
            return Presenter().show_json(Helper().prepare_json(get_list['config'][self.table]))

        if not self.args.get('name'):
            counts = [[state, summary[state]] for state in sorted(summary)]
            Presenter().show_table(' << Firmware Status >>', ['state', 'nodes'], counts)

        show_all = self.args.get('all') or self.args.get('name')
        rows, num = [], 1
        for node in sorted(data):
            row = data[node]
            if not show_all and row['state'] == 'done':
                continue
            rows.append([num, node, row.get('group') or '-', row['component'] or 'all',
                         row['state'], row['since'] or '-', row['message'] or '-'])
            num += 1
        if rows:
            Presenter().show_table(
                ' << Firmware Status >>',
                ['#', 'node', 'group', 'component', 'state', 'since', 'message'], rows)
        elif not show_all:
            Message().show_success('Nothing needs attention.')
        return True


def firmware_push(table=None, args=None):
    """
    'luna node firmwarepush' and 'luna group firmwarepush', which differ only in
    what they are aimed at.

    Written once and imported by both, rather than a copy in each: the two verbs
    are the same request with a different word in the URI, and a pair of copies is
    how the one that gets fixed stops being the one that gets called.

    A dry run asks the daemon what a push would do and does not record anything.
    It contacts no BMC either - every input is stored inventory - so it answers
    for a rack that is powered off, and it is affordable to ask about a whole
    cluster before deciding.
    """
    name = args['name']
    if args.get('dry_run'):
        return firmware_preview(table, name, args)
    record = {}
    if args.get('component'):
        record['component'] = args['component']
    payload = {'config': {table: {name: record}}}
    response = Rest().post_raw(f'config/{table}/{name}/_firmwarepush', payload)
    content = response.json() if response.content else {}
    message = content.get('message', response.content)
    if response.status_code not in (200, 201, 204):
        return Message().error_exit(message, response.status_code)
    Message().show_success(f'{message}')
    Message().show_success('Watch it with: luna firmwarecatalog status')
    return response


def firmware_preview(table=None, name=None, args=None):
    """
    What a firmware push would do, and why it would not.

    The skips are grouped by cause rather than listed per node. At four thousand
    nodes they share a handful of reasons, and a line each is a wall that buries
    the nodes which would actually change.
    """
    get_list = Rest().get_data(f'{table}/{name}/firmware/_preview')
    if get_list.status_code != 200:
        Message().error_exit(get_list.content, get_list.status_code)
    answer = get_list.content['config']['firmware']['preview']
    if args.get('raw'):
        return Presenter().show_json(Helper().prepare_json(answer))
    component = args.get('component')
    rows, num = [], 1
    for plan in answer.get('ready') or []:
        for item in plan['differs']:
            if component and item['component'] != component:
                continue
            rows.append([num, plan['node'], item['component'],
                         item['running'] or 'unknown', item['wanted'],
                         item['entry'], item['imagefile'] or '-'])
            num += 1
    if rows:
        Presenter().show_table(' << Firmware Push Preview >>',
                               ['#', 'node', 'component', 'running', 'would become',
                                'entry', 'image'], rows)
    for reason, nodes in sorted((answer.get('skipped') or {}).items()):
        Message().show_warning(f'{len(nodes)} node(s) skipped: {reason}')
    for line in answer.get('summary') or []:
        Message().show_success(line)
    if not rows:
        Message().show_success('Nothing would change.')
    return True
