#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch Class for the CLI
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

class Switch():
    """
    Switch Class responsible to show, list,
    add, remove information for the Switch
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "switch"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "change", "rename", "clone", "remove"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_switch')
                call(self)
            else:
                Helper().show_error(f"Kindly choose from {actions}.")
        if parser and subparsers:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Switch class.
        """
        switch_menu = subparsers.add_parser('switch', help='Switch operations.')
        switch_args = switch_menu.add_subparsers(dest='action')
        switch_list = switch_args.add_parser('list', help='List Switch')
        Helper().common_list_args(switch_list)
        switch_show = switch_args.add_parser('show', help='Show Switch')
        switch_show.add_argument('name', help='Name of the Switch')
        Helper().common_list_args(switch_show)
        switch_add = switch_args.add_parser('add', help='Add Switch')
        switch_add.add_argument('name', help='Name of the Switch')
        switch_add.add_argument('-N', '--network', required=True, help='Network for Switch')
        switch_add.add_argument('-ip', '--ipaddress', required=True, help='IP Address for Switch')
        switch_add.add_argument('-m', '--macaddress', help='MAC Address for Switch')
        switch_add.add_argument('-r', '--read', help='Read community')
        switch_add.add_argument('-w', '--rw', help='Write community')
        switch_add.add_argument('-o', '--oid', help='OID of the Switch')
        switch_add.add_argument('-c', '--comment', help='Comment for Switch')
        switch_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_change = switch_args.add_parser('change', help='Change Switch')
        switch_change.add_argument('name', help='Name of the Switch')
        switch_change.add_argument('-N', '--network', help='Network for Switch')
        switch_change.add_argument('-ip', '--ipaddress', help='IP Address for Switch')
        switch_change.add_argument('-m', '--macaddress', help='MAC Address for Switch')
        switch_change.add_argument('-r', '--read', help='Read community')
        switch_change.add_argument('-w', '--rw', help='Write community')
        switch_change.add_argument('-o', '--oid', help='OID of the Switch')
        switch_change.add_argument('-c', '--comment', help='Comment for Switch')
        switch_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_clone = switch_args.add_parser('clone', help='Clone Switch')
        switch_clone.add_argument('name', help='Name of the Switch')
        switch_clone.add_argument('newswitchname', help='New name of the Switch')
        switch_clone.add_argument('-N', '--network', required=True, help='Network for Switch')
        switch_clone.add_argument('-ip', '--ipaddress', required=True, help='IP Address for Switch')
        switch_clone.add_argument('-m', '--macaddress', help='MAC Address for Switch')
        switch_clone.add_argument('-r', '--read', help='Read community')
        switch_clone.add_argument('-w', '--rw', help='Write community')
        switch_clone.add_argument('-o', '--oid', help='OID of the Switch')
        switch_clone.add_argument('-c', '--comment', help='Comment for Switch')
        switch_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_rename = switch_args.add_parser('rename', help='Rename Switch')
        switch_rename.add_argument('name', help='Name of the Switch')
        switch_rename.add_argument('newswitchname', help='New name of the Switch')
        switch_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_remove = switch_args.add_parser('remove', help='Remove Switch')
        switch_remove.add_argument('name', help='Name of the Switch')
        switch_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_switch(self):
        """
        Method to list all switchs from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_switch(self):
        """
        Method to show a switch in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_switch(self):
        """
        Method to add new switch in Luna Configuration.
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


    def change_switch(self):
        """
        Method to change a switch in Luna Configuration.
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
        else:
            Helper().show_error('Nothing to update.')
        return True

    def clone_switch(self):
        """
        Method to rename a switch in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_clone(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newswitchname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def rename_switch(self):
        """
        Method to rename a switch in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newswitchname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def remove_switch(self):
        """
        Method to remove a switch in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            self.logger.debug(f'Payload => {payload}')
            response = Rest().get_delete(self.table, payload['name'])
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True
