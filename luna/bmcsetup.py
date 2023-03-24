#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BMC Setup Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log

class BMCSetup():
    """
    BMC Setup Class responsible to show, list,
    add, remove information for the BMC Setup
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "bmcsetup"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "change", "rename", "clone", "remove"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_bmcsetup')
                call(self)
            else:
                Helper().show_error(f"Kindly choose from {actions}.")
        if parser and subparsers:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the BMC Setup class.
        """
        bmcsetup_menu = subparsers.add_parser('bmcsetup', help='BMC Setup operations.')
        bmcsetup_args = bmcsetup_menu.add_subparsers(dest='action')
        bmcsetup_list = bmcsetup_args.add_parser('list', help='List BMC Setups')
        Helper().common_list_args(bmcsetup_list)
        bmcsetup_show = bmcsetup_args.add_parser('show', help='Show BMC Setup')
        bmcsetup_show.add_argument('name', help='Name of the BMC Setup')
        Helper().common_list_args(bmcsetup_show)
        bmcsetup_add = bmcsetup_args.add_parser('add', help='Add BMC Setup')
        bmcsetup_add.add_argument('name', help='Name of the BMC Setup')
        bmcsetup_add.add_argument('-uid', '--userid', type=int, help='UserID for BMC Setup')
        bmcsetup_add.add_argument('-u', '--username', help='Username for BMC Setup')
        bmcsetup_add.add_argument('-p', '--password', help='Password for BMC Setup')
        bmcsetup_add.add_argument('-nt', '--netchannel', type=int, help='Network Channel')
        bmcsetup_add.add_argument('-mt', '--mgmtchannel', type=int, help='Management Channel')
        bmcsetup_add.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        bmcsetup_add.add_argument('-c', '--comment', help='Comment for BMC Setup')
        bmcsetup_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        bmcsetup_change = bmcsetup_args.add_parser('change', help='Change a BMC Setup')
        bmcsetup_change.add_argument('name', help='Name of the BMC Setup')
        bmcsetup_change.add_argument('-uid', '--userid', type=int, help='UserID for BMC Setup')
        bmcsetup_change.add_argument('-u', '--username', help='Username for BMC Setup')
        bmcsetup_change.add_argument('-p', '--password', help='Password for BMC Setup')
        bmcsetup_change.add_argument('-nt', '--netchannel', type=int, help='Network Channel')
        bmcsetup_change.add_argument('-mt', '--mgmtchannel', type=int, help='Management Channel')
        bmcsetup_change.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        bmcsetup_change.add_argument('-c', '--comment', help='Comment for BMC Setup')
        bmcsetup_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        bmcsetup_clone = bmcsetup_args.add_parser('clone', help='Clone BMC Setup')
        bmcsetup_clone.add_argument('name', help='Name of the BMC Setup')
        bmcsetup_clone.add_argument('newbmcname', help='New Name for BMC Setup')
        bmcsetup_clone.add_argument('-uid', '--userid', type=int, help='UserID for BMC Setup')
        bmcsetup_clone.add_argument('-u', '--username', help='Username for BMC Setup')
        bmcsetup_clone.add_argument('-p', '--password', help='Password for BMC Setup')
        bmcsetup_clone.add_argument('-nt', '--netchannel', type=int, help='Network Channel')
        bmcsetup_clone.add_argument('-mt', '--mgmtchannel', type=int, help='Management Channel')
        bmcsetup_clone.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        bmcsetup_clone.add_argument('-c', '--comment', help='Comment for BMC Setup')
        bmcsetup_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        bmcsetup_rename = bmcsetup_args.add_parser('rename', help='Rename BMC Setup')
        bmcsetup_rename.add_argument('name', help='Name of the BMC Setup')
        bmcsetup_rename.add_argument('newbmcname', help='New name of the BMC Setup')
        bmcsetup_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        bmcsetup_remove = bmcsetup_args.add_parser('remove', help='Remove BMC Setup')
        bmcsetup_remove.add_argument('name', help='Name of the BMC Setup')
        bmcsetup_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_bmcsetup(self):
        """
        Method to list all bmc setups from
        Luna 2 Daemon.
        """
        return Helper().get_list(self.table, self.args)


    def show_bmcsetup(self):
        """
        Method to show a bmc setup from
        Luna 2 Daemon.
        """
        return Helper().show_data(self.table, self.args)


    def add_bmcsetup(self):
        """
        Method to add new bmc setup in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
            payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def change_bmcsetup(self):
        """
        Method to update a bmc setup in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
            payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def clone_bmcsetup(self):
        """
        Method to rename a bmc setup in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_clone(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloned as {payload["newbmcname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def rename_bmcsetup(self):
        """
        Method to rename a bmc setup in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                msg = f'{payload["name"]} is renamed to {payload["newbmcname"]}'
                Helper().show_success(f'{msg} in {self.table.capitalize()}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def remove_bmcsetup(self):
        """
        Method to remove a bmc setup in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            response = Rest().get_delete(self.table, payload['name'])
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True
