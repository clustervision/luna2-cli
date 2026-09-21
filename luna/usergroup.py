#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2023  ClusterVision Solutions b.v.
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
UserGroup Class for the CLI: organisations, departments and teams of Luna users, the
role each member holds, and the map from a directory group onto a usergroup. Not a
node group, and not an OS group.
"""
__author__      = "Antoine Schonewille"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.2"
__maintainer__  = "Antoine Schonewille"
__email__       = "antoine.schonewille@clustervision.com"
__status__      = "Development"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.rest import Rest
from luna.utils.constant import actions, BOOL_CHOICES, BOOL_META
from luna.utils.message import Message
from luna.utils.arguments import Arguments
from luna.utils.presenter import Presenter

ROLES = ['admin', 'manager', 'operator', 'reader']


class UserGroup():
    """
    UserGroup Class responsible to show, list, add, change, rename, remove usergroups,
    to add and remove members with a role, and to keep the directory group map.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "usergroup"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_usergroup')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the UserGroup class.
        """
        menu = Helper().get_help_message(subparsers, self.table)
        args = menu.add_subparsers(dest='action', title='commands', description='Available usergroup operations')
        ug_list = args.add_parser('list', help='List Usergroups')
        Arguments().common_list_args(ug_list, True)
        ug_show = args.add_parser('show', help='Show a Usergroup and its members')
        ug_show.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(ug_show)
        ug_add = args.add_parser('add', help='Add a Usergroup')
        ug_add.add_argument('name', help='Usergroup Name')
        self.usergroup_args(ug_add)
        ug_change = args.add_parser('change', help='Change a Usergroup')
        ug_change.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        self.usergroup_args(ug_change)
        ug_rename = args.add_parser('rename', help='Rename a Usergroup')
        ug_rename.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        ug_rename.add_argument('newusergroupname', help='New Usergroup Name')
        ug_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        ug_remove = args.add_parser('remove', help='Remove a Usergroup, its memberships and its map entries')
        ug_remove.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        ug_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        ug_member = args.add_parser('member', help='List the members of a Usergroup with their roles')
        ug_member.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(ug_member)
        ug_addmember = args.add_parser('addmember', help='Add a member with a role, or change the role')
        ug_addmember.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        ug_addmember.add_argument('username', help='Username').completer = Helper().name_completer('user')
        ug_addmember.add_argument('-r', '--role', required=True, choices=ROLES,
                                  help='The membership role: admin, manager, operator or reader (not a boot role)')
        ug_addmember.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        ug_removemember = args.add_parser('removemember', help='Remove a member')
        ug_removemember.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        ug_removemember.add_argument('username', help='Username').completer = Helper().name_completer('user')
        ug_removemember.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        ug_map = args.add_parser('map', help='List the directory group map: external group, usergroup, role')
        Arguments().common_list_args(ug_map, True)
        ug_addmap = args.add_parser('addmap', help='Map a directory group onto a Usergroup with a role')
        ug_addmap.add_argument('name', help='Usergroup Name').completer = Helper().name_completer(self.table)
        ug_addmap.add_argument('-s', '--source', required=True, help='The source of the group: pam, ldap')
        ug_addmap.add_argument('-g', '--external_group', required=True,
                               help='The group as the source names it (an OS group name, or a directory DN)')
        ug_addmap.add_argument('-r', '--role', required=True, choices=ROLES, help='The membership role it grants')
        ug_addmap.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        ug_removemap = args.add_parser('removemap', help='Remove a map entry')
        ug_removemap.add_argument('-s', '--source', required=True, help='The source of the group')
        ug_removemap.add_argument('-g', '--external_group', required=True, help='The group as the source names it')
        ug_removemap.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def usergroup_args(self, sub_parser):
        """
        The fields of a usergroup. Members are added one at a time, never as a list here.
        """
        sub_parser.add_argument('-c', '--comment', help='Comment')
        sub_parser.add_argument('-H', '--hardware', choices=BOOL_CHOICES, metavar=BOOL_META,
                                help='Its admins and managers may create nodes and hardware setups (set by rootus)')
        sub_parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return sub_parser


    def list_usergroup(self):
        return Helper().get_list(self.table, self.args)

    def show_usergroup(self):
        return Helper().show_data(self.table, self.args)

    def add_usergroup(self):
        return Helper().add_record(self.table, self.args)

    def change_usergroup(self):
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')

    def rename_usergroup(self):
        return Helper().rename_record(self.table, self.args, self.args["newusergroupname"])

    def remove_usergroup(self):
        return Helper().delete_record(self.table, self.args)


    def _done(self, response):
        """
        A create answers 201 with its message, an update 204 with none: say what was done.
        """
        if response.status_code == 201:
            Message().show_success(response.content)
        elif response.status_code == 204:
            Message().show_success(f"usergroup {self.args.get('name') or ''}: {self.args['action']} done.".replace('  ', ' '))
        else:
            Message().error_exit(response.content, response.status_code)


    def member_usergroup(self):
        """
        The members of a usergroup, with the role each holds.
        """
        name = self.args['name']
        response = Rest().get_raw(f'config/usergroup/{name}/members')
        if response.status_code != 200:
            Message().error_exit(response.content, response.status_code)
        members = response.json()['config']['usergroup'][name]['members']
        if self.args.get('raw'):
            return Presenter().show_json(members)
        rows = [[username, role] for username, role in sorted(members.items())]
        return Presenter().show_table(f'Members of {name}', ['username', 'role'], rows)


    def addmember_usergroup(self):
        """
        Add one member with a role, or change the role of one.
        """
        name = self.args['name']
        body = {'config': {'usergroup': {name: {'username': self.args['username'], 'role': self.args['role']}}}}
        response = Rest().post_raw(f'config/usergroup/{name}/members', body)
        self._done(response)


    def removemember_usergroup(self):
        """
        Remove one member.
        """
        name = self.args['name']
        body = {'config': {'usergroup': {name: {'username': self.args['username']}}}}
        response = Rest().post_raw(f'config/usergroup/{name}/members/_remove', body)
        self._done(response)


    def map_usergroup(self):
        """
        The directory group map.
        """
        response = Rest().get_raw('config/usergroupmap')
        if response.status_code != 200:
            Message().error_exit(response.content, response.status_code)
        entries = response.json()['config']['usergroupmap']
        if self.args.get('raw'):
            return Presenter().show_json(entries)
        rows = [[e['source'], e['external_group'], e['usergroup'], e['role']] for e in entries]
        return Presenter().show_table('Usergroup map', ['source', 'external group', 'usergroup', 'role'], rows)


    def addmap_usergroup(self):
        """
        Map one directory group onto a usergroup with a role, or change where it lands.
        """
        body = {'config': {'usergroupmap': {'source': self.args['source'], 'external_group': self.args['external_group'],
                                            'usergroup': self.args['name'], 'role': self.args['role']}}}
        response = Rest().post_raw('config/usergroupmap', body)
        self._done(response)


    def removemap_usergroup(self):
        """
        Remove one map entry, by source and external group.
        """
        body = {'config': {'usergroupmap': {'source': self.args['source'], 'external_group': self.args['external_group']}}}
        response = Rest().post_raw('config/usergroupmap/_remove', body)
        self._done(response)
