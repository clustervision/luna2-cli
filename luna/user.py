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
User Class for the CLI: the identities that hold a Luna token. Not the cluster's OS
accounts, which obol manages.
"""
__author__      = "Antoine Schonewille"
__copyright__   = "Copyright 2026, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.2"
__maintainer__  = "Antoine Schonewille"
__email__       = "antoine.schonewille@clustervision.com"
__status__      = "Development"

from getpass import getpass
from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.constant import actions, BOOL_CHOICES, BOOL_META
from luna.utils.message import Message
from luna.utils.arguments import Arguments
from luna.utils.rest import Rest
from luna.utils.presenter import Presenter
from luna.access import _message


class User():
    """
    User Class responsible to show, list, add, change, rename, remove Luna users.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "user"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_user')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the User class.
        """
        user_menu = Helper().get_help_message(subparsers, self.table)
        user_args = user_menu.add_subparsers(dest='action', title='commands', description='Available user operations')
        user_list = user_args.add_parser('list', help='List Users')
        Arguments().common_list_args(user_list, True)
        user_show = user_args.add_parser('show', help='Show a User')
        user_show.add_argument('name', help='Username').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(user_show)
        user_access = user_args.add_parser('access', help='What a User holds, per kind of object')
        user_access.add_argument('name', help='Username').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(user_access)
        user_add = user_args.add_parser('add', help='Add a User')
        user_add.add_argument('name', help='Username')
        self.user_args(user_add)
        user_change = user_args.add_parser('change', help='Change a User')
        user_change.add_argument('name', help='Username').completer = Helper().name_completer(self.table)
        self.user_args(user_change)
        user_rename = user_args.add_parser('rename', help='Rename a User')
        user_rename.add_argument('name', help='Username').completer = Helper().name_completer(self.table)
        user_rename.add_argument('newusername', help='New Username')
        user_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        user_remove = user_args.add_parser('remove', help='Remove a User and its memberships')
        user_remove.add_argument('name', help='Username').completer = Helper().name_completer(self.table)
        user_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def user_args(self, sub_parser):
        """
        The fields of a user. A password is asked on the terminal, never given as an argument.
        """
        sub_parser.add_argument('-p', '--password', action='store_true', default=None,
                                help='Set a Luna password (asked on the terminal)')
        sub_parser.add_argument('-s', '--source', help='Where the user authenticates: local, pam, ldap')
        sub_parser.add_argument('-e', '--enabled', choices=BOOL_CHOICES, metavar=BOOL_META, help='Enabled')
        sub_parser.add_argument('-a', '--admin', choices=BOOL_CHOICES, metavar=BOOL_META,
                                help='Cluster-wide admin flag: everything, everywhere')
        sub_parser.add_argument('-d', '--delegate', choices=BOOL_CHOICES, metavar=BOOL_META,
                                help='May obtain a token on behalf of another user (the portal)')
        sub_parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return sub_parser


    def _ask_password(self):
        """
        Replace the --password flag with the password itself, asked twice on the terminal.
        """
        if self.args.get('password'):
            first = getpass('Luna password: ')
            second = getpass('Again: ')
            if first != second:
                Message().error_exit('ERROR :: the two passwords differ')
            self.args['password'] = first
        elif 'password' in self.args:
            del self.args['password']


    def list_user(self):
        """
        This method lists all users.
        """
        return Helper().get_list(self.table, self.args)


    def show_user(self):
        """
        This method shows one user.
        """
        return Helper().show_data(self.table, self.args)


    def access_user(self):
        """
        What the user holds: every object it reaches, with the mode in words beside the letters.
        """
        name = self.args['name']
        response = Rest().get_raw(f'config/user/{name}/_access')
        if response.status_code != 200:
            Message().error_exit(_message(response), response.status_code)
        held = response.json()['config']['user'][name]['access']
        if self.args.get('raw'):
            return Presenter().show_json(held)
        rows = [[kind, obj, Helper().access_triplet_in_words(mode)] for kind in sorted(held) for obj, mode in sorted(held[kind].items())]
        if not rows:
            return Message().show_success(f'{name} holds nothing.')
        return Presenter().show_table(f'What {name} holds', ['kind', 'object', 'access'], rows)


    def add_user(self):
        """
        This method adds a user.
        """
        self._ask_password()
        return Helper().add_record(self.table, self.args)


    def change_user(self):
        """
        This method changes a user.
        """
        self._ask_password()
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')


    def rename_user(self):
        """
        This method renames a user.
        """
        return Helper().rename_record(self.table, self.args, self.args["newusername"])


    def remove_user(self):
        """
        This method removes a user.
        """
        return Helper().delete_record(self.table, self.args)
