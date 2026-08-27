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
BIOS Configuration Class for the CLI
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


class BiosConfig():
    """
    BIOS Configuration Class, responsible to list, show, change, rename and
    remove a stored BIOS configuration.

    There is deliberately no add: a configuration comes into existence by being
    grabbed off a node - see 'luna node biosgrab' - because a set of BIOS
    settings nobody's hardware ever reported is exactly what a golden node is
    there to avoid.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "biosconfig"
        self.route = "biosconfig"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_biosconfig')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the BIOS Configuration class.
        """
        biosconfig_menu = Helper().get_help_message(subparsers, self.table)
        biosconfig_args = biosconfig_menu.add_subparsers(dest='action', title='commands', description='Available biosconfig operations')
        biosconfig_list = biosconfig_args.add_parser('list', help='List BIOS Configurations')
        Arguments().common_list_args(biosconfig_list, True)
        biosconfig_show = biosconfig_args.add_parser('show', help='Show a BIOS Configuration and its settings')
        biosconfig_show.add_argument('name', help='BIOS Configuration Name').completer = Helper().name_completer(self.table)
        biosconfig_show.add_argument('-s', '--settings', action='store_true', default=None, help='Also list every stored setting')
        Arguments().common_list_args(biosconfig_show)
        biosconfig_change = biosconfig_args.add_parser('change', help='Change a BIOS Configuration')
        biosconfig_change.add_argument('name', help='BIOS Configuration Name').completer = Helper().name_completer(self.table)
        Arguments().common_biosconfig_args(biosconfig_change)
        biosconfig_rename = biosconfig_args.add_parser('rename', help='Rename a BIOS Configuration')
        biosconfig_rename.add_argument('name', help='BIOS Configuration Name').completer = Helper().name_completer(self.table)
        biosconfig_rename.add_argument('newbiosname', help='New BIOS Configuration Name')
        biosconfig_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        biosconfig_status = biosconfig_args.add_parser('status', help='What every node was last seen holding')
        biosconfig_status.add_argument('name', nargs='?',
                                       help='Name of a single Node').completer = Helper().name_completer('node')
        biosconfig_status.add_argument('-g', '--group',
                                       help='Only the nodes of this Group').completer = Helper().name_completer('group')
        biosconfig_status.add_argument('-a', '--all', action='store_true', default=None,
                                       help='Every node, not only the ones worth looking at')
        biosconfig_status.add_argument('-R', '--raw', action='store_true', default=None,
                                       help='Raw JSON output')
        biosconfig_status.add_argument('-v', '--verbose', action='store_true', default=None,
                                       help='Verbose Mode')
        biosconfig_remove = biosconfig_args.add_parser('remove', help='Remove a BIOS Configuration')
        biosconfig_remove.add_argument('name', help='BIOS Configuration Name').completer = Helper().name_completer(self.table)
        biosconfig_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_biosconfig(self):
        """
        This method list all BIOS configurations.
        """
        return Helper().get_list(self.table, self.args)


    def show_biosconfig(self):
        """
        This method shows one BIOS configuration.

        The settings are behind a flag rather than shown by default: a grab off a
        real machine brings back hundreds of them, and burying the four fields
        that decide whether it can be pushed anywhere under that list makes the
        command useless for the question it is usually asked.
        """
        name = self.args['name']
        get_list = Rest().get_data(self.table, name)
        if get_list.status_code != 200:
            Message().error_exit(get_list.content, get_list.status_code)
        detail = get_list.content['config'][self.table][name]
        settings = detail.pop('attributes', {}) or {}
        if self.args['raw']:
            Presenter().show_json(Helper().prepare_json(dict(detail, attributes=settings)))
            return True
        # the same decode every other show does: grab_exclude and comment are
        # editor keys, so they travel base64 and are read back for display here.
        # Rendering the record straight printed both of them as base64.
        detail = Helper().prepare_json(detail)
        fields = list(detail.keys())
        rows = [detail[key] for key in fields]
        Presenter().show_table_col(f'BIOS Configuration :: {name}', fields, rows)
        if self.args['settings']:
            if not settings:
                Message().show_warning(f'BIOS configuration {name} carries no settings.')
                return True
            rows = [[key, settings[key]] for key in sorted(settings)]
            Presenter().show_table(f' << {name} Settings >>', ['Attribute', 'Value'], rows)
        return True


    def status_biosconfig(self):
        """
        Method to show what every node was last seen holding.

        Read entirely from stored inventory: no BMC is contacted, so this answers
        for machines that are switched off, and it answers in one query rather
        than one connection per node. The price of that is that it is a record of
        the last time we looked, never of this moment - which is why every row
        carries when that was, and why it does not pretend to say how many stages
        a node still needs. Ask the machine for that, with 'luna node biospush'.
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
            return Message().show_error('No BIOS status available.')
        data = get_list['config'][self.table]['status']
        summary = get_list['config'][self.table].get('summary') or {}
        if self.args['raw']:
            return Presenter().show_json(Helper().prepare_json(get_list['config'][self.table]))

        # the counts answer 'is it fine'; the rows are only what is not. A line per
        # node is useful on a rack and useless on a cluster, and the handful that
        # need action are exactly what gets buried
        if not self.args.get('name'):
            counts = [[state, summary[state]] for state in sorted(summary)]
            Presenter().show_table(' << BIOS Status >>', ['state', 'nodes'], counts)

        show_all = self.args.get('all') or self.args.get('name')
        rows, num = [], 1
        for node in sorted(data):
            row = data[node]
            if not show_all and row['state'] in ('matched', 'unknown'):
                continue
            rows.append([num, node, row.get('group') or '-', row['config'] or '-',
                         row['state'], row['bios_version'] or '-',
                         row['digest'] or '-', row['since'] or '-'])
            num += 1
        if rows:
            Presenter().show_table(
                ' << BIOS Status >>',
                ['#', 'node', 'group', 'config', 'state', 'bios', 'digest',
                 'last seen'], rows)
        elif not show_all:
            Message().show_success('Nothing needs attention.')
        return True


    def change_biosconfig(self):
        """
        This method updates what an administrator owns on a BIOS configuration.
        """
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')


    def rename_biosconfig(self):
        """
        This method renames a BIOS configuration.
        """
        return Helper().rename_record(self.table, self.args, self.args["newbiosname"])


    def remove_biosconfig(self):
        """
        This method removes a BIOS configuration.
        """
        return Helper().delete_record(self.table, self.args)
