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
Redfish Setup Class for the CLI
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
from luna.utils.message import Message
from luna.utils.arguments import Arguments

class RedfishSetup():
    """
    Redfish Setup Class responsible to show, list, add, change, remove, rename and
    clone a redfish setup, and to manage the accounts underneath it.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "redfishsetup"
        self.route = "redfishsetup"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_redfishsetup')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Redfish Setup class.
        """
        redfishsetup_menu = Helper().get_help_message(subparsers, self.table)
        redfishsetup_args = redfishsetup_menu.add_subparsers(dest='action', title='commands', description='Available redfishsetup operations')
        redfishsetup_list = redfishsetup_args.add_parser('list', help='List Redfish Setups')
        Arguments().common_list_args(redfishsetup_list, True)
        redfishsetup_show = redfishsetup_args.add_parser('show', help='Show Redfish Setup')
        redfishsetup_show.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(redfishsetup_show)
        redfishsetup_member = redfishsetup_args.add_parser('member', help='Nodes and Groups Using the Redfish Setup')
        redfishsetup_member.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(redfishsetup_member)
        redfishsetup_add = redfishsetup_args.add_parser('add', help='Add Redfish Setup')
        redfishsetup_add.add_argument('name', help='Redfish Setup Name')
        Arguments().common_redfishsetup_args(redfishsetup_add)
        redfishsetup_change = redfishsetup_args.add_parser('change', help='Change a Redfish Setup')
        redfishsetup_change.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        Arguments().common_redfishsetup_args(redfishsetup_change)
        redfishsetup_clone = redfishsetup_args.add_parser('clone', help='Clone Redfish Setup')
        redfishsetup_clone.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        Arguments().common_redfishsetup_args(redfishsetup_clone)
        redfishsetup_clone.add_argument('newredfishsetupname', help='New Redfish Setup Name')
        redfishsetup_rename = redfishsetup_args.add_parser('rename', help='Rename Redfish Setup')
        redfishsetup_rename.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        redfishsetup_rename.add_argument('newredfishsetupname', help='New Redfish Setup Name')
        redfishsetup_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        redfishsetup_remove = redfishsetup_args.add_parser('remove', help='Remove Redfish Setup')
        redfishsetup_remove.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        redfishsetup_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        redfishsetup_addaccount = redfishsetup_args.add_parser('addaccount', help='Add an Account to a Redfish Setup')
        redfishsetup_addaccount.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        redfishsetup_addaccount.add_argument('account', help='Account Name')
        Arguments().common_redfishaccount_args(redfishsetup_addaccount)
        redfishsetup_changeaccount = redfishsetup_args.add_parser('changeaccount', help='Change an Account of a Redfish Setup')
        redfishsetup_changeaccount.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        redfishsetup_changeaccount.add_argument('account', help='Account Name')
        Arguments().common_redfishaccount_args(redfishsetup_changeaccount)
        redfishsetup_removeaccount = redfishsetup_args.add_parser('removeaccount', help='Remove an Account from a Redfish Setup')
        redfishsetup_removeaccount.add_argument('name', help='Redfish Setup Name').completer = Helper().name_completer(self.table)
        redfishsetup_removeaccount.add_argument('account', help='Account Name')
        redfishsetup_removeaccount.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_redfishsetup(self):
        """
        This method list all redfishsetup.
        """
        return Helper().get_list(self.table, self.args)


    def show_redfishsetup(self):
        """
        This method show a specific redfishsetup.
        """
        return Helper().show_data(self.table, self.args)


    def member_redfishsetup(self):
        """
        This method will show the nodes and groups using the Redfish Setup.
        """
        return Helper().member_record(self.table, self.args)


    def add_redfishsetup(self):
        """
        This method add a redfishsetup.
        """
        return Helper().add_record(self.table, self.args)


    def change_redfishsetup(self):
        """
        This method update a redfishsetup.
        """
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')


    def clone_redfishsetup(self):
        """
        This method clone a redfishsetup.
        """
        return Helper().clone_record(self.table, self.args)


    def rename_redfishsetup(self):
        """
        This method rename a redfishsetup.
        """
        return Helper().rename_record(self.table, self.args, self.args["newredfishsetupname"])


    def remove_redfishsetup(self):
        """
        This method remove a redfishsetup.
        """
        return Helper().delete_record(self.table, self.args)


    def redfishsetup_account(self, name=None, account=None):
        """
        One account of a redfishsetup as it stands, or None.
        """
        get_list = Rest().get_data(f'{self.route}/{name}')
        if get_list.status_code != 200:
            return None
        detail = get_list.content['config'][self.table].get(name) or {}
        for entry in detail.get('accounts') or []:
            if entry.get('name') == account:
                return entry
        return None


    def account_payload(self):
        """
        The body for one account. Only what was supplied is sent: a change that
        gives an account the Operator role says nothing about its password, and
        demanding one would make the operator retype a password to leave it alone.
        """
        payload = {'name': self.args['account']}
        for field in ['username', 'password', 'role']:
            if self.args.get(field) is not None:
                payload[field] = self.args[field]
        comment = self.args.get('comment')
        if comment is True:
            payload['comment'] = Helper().open_editor(
                'comment', None, {'name': self.args['account']})
        elif comment:
            payload['comment'] = comment
        return payload


    def post_account(self, payload=None):
        """
        Send one account to the redfishsetup it belongs to.
        """
        name = self.args['name']
        request_data = {'config': {self.table: {name: {'accounts': [payload]}}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(self.route, name, request_data)
        self.logger.debug(f'Response => {response}')
        return response


    def addaccount_redfishsetup(self):
        """
        Method to add an account to a Redfish Setup.
        """
        name, account = self.args['name'], self.args['account']
        if Rest().get_data(f'{self.route}/{name}').status_code != 200:
            Message().error_exit(f'Redfish Setup {name} is not available', 404)
        if self.redfishsetup_account(name, account):
            Message().error_exit(f'Account {account} is already in redfishsetup {name}', 400)
        payload = self.account_payload()
        for required in ['username', 'password']:
            if not payload.get(required):
                return Message().show_error(f'An account needs a {required}: '
                                            f'supply -u and -p')
        response = self.post_account(payload)
        if response.status_code in (200, 201, 204):
            Message().show_success(f'Account {account} is added to redfishsetup {name}.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def changeaccount_redfishsetup(self):
        """
        Method to change an account of a Redfish Setup. What is not supplied keeps
        the value it already has.
        """
        name, account = self.args['name'], self.args['account']
        if not self.redfishsetup_account(name, account):
            Message().error_exit(f'Account {account} is not in redfishsetup {name}. '
                                 f'Use addaccount to create it', 404)
        payload = self.account_payload()
        if list(payload.keys()) == ['name']:
            return Message().show_error('Nothing to change: supply a username, password '
                                        'or role')
        response = self.post_account(payload)
        if response.status_code in (200, 201, 204):
            Message().show_success(f'Account {account} in redfishsetup {name} is updated.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def removeaccount_redfishsetup(self):
        """
        Method to remove one account from a Redfish Setup.
        """
        name, account = self.args['name'], self.args['account']
        response = Rest().get_delete(self.route, f'{name}/{account}')
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Message().show_success(f'Account {account} is removed from redfishsetup {name}.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response
