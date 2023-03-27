#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other Devices Class for the CLI
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

class OtherDev():
    """
    Other Devices Class responsible to show, list,
    add, remove information for the Other Devices
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "otherdev"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "change", "rename", "clone", "remove"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_otherdev')
                call(self)
            else:
                Helper().show_error("Not a valid option.")
        if parser and subparsers:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the OtherDev class.
        """
        otherdev_menu = subparsers.add_parser('otherdev', help='Other Devices operations.')
        otherdev_args = otherdev_menu.add_subparsers(dest='action')
        otherdev_list = otherdev_args.add_parser('list', help='List Other Devices')
        Helper().common_list_args(otherdev_list)
        otherdev_show = otherdev_args.add_parser('show', help='Show Other Devices')
        otherdev_show.add_argument('name', help='Name of the Other Devices')
        Helper().common_list_args(otherdev_show)
        otherdev_add = otherdev_args.add_parser('add', help='Add Other Devices')
        otherdev_add.add_argument('name', help='Name of the Other Device')
        otherdev_add.add_argument('-N', '--network', required=True, help='Network for Other Device')
        otherdev_add.add_argument('-ip', '--ipaddress', required=True, help='IP Address for Other Device')
        otherdev_add.add_argument('-m', '--macaddress', help='MAC Address for Other Device')
        otherdev_add.add_argument('-c', '--comment', action='store_true', help='Comment for Other Device')
        otherdev_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_change = otherdev_args.add_parser('change', help='Change Other Devices')
        otherdev_change.add_argument('name', help='Name of the Other Device')
        otherdev_change.add_argument('-N', '--network', help='Network for Other Device')
        otherdev_change.add_argument('-ip', '--ipaddress', help='IP Address for Other Device')
        otherdev_change.add_argument('-m', '--macaddress', help='MAC Address for Other Device')
        otherdev_change.add_argument('-c', '--comment', action='store_true', help='Comment for Other Device')
        otherdev_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_clone = otherdev_args.add_parser('clone', help='Clone Other Devices')
        otherdev_clone.add_argument('name', help='Name of the Other Device')
        otherdev_clone.add_argument('newotherdevname', help='New name of the Other Device')
        otherdev_clone.add_argument('-N', '--network', required=True, help='Network for Other Device')
        otherdev_clone.add_argument('-ip', '--ipaddress', required=True, help='IP Address for Other Device')
        otherdev_clone.add_argument('-m', '--macaddress', help='MAC Address for Other Device')
        otherdev_clone.add_argument('-c', '--comment', action='store_true', help='Comment for Other Device')
        otherdev_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_rename = otherdev_args.add_parser('rename', help='Rename Other Devices')
        otherdev_rename.add_argument('name', help='Name of the Other Device')
        otherdev_rename.add_argument('newotherdevname', help='New name of the Other Devices')
        otherdev_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_remove = otherdev_args.add_parser('remove', help='Remove Other Devices')
        otherdev_remove.add_argument('name', help='Name of the Other Device')
        otherdev_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_otherdev(self):
        """
        Method to list all other devices from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_otherdev(self):
        """
        Method to show a other devices in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_otherdev(self):
        """
        Method to add new other devices in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
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


    def change_otherdev(self):
        """
        Method to change a other devices in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
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


    def clone_otherdev(self):
        """
        Method to rename a other devices in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_clone(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newotherdevname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def rename_otherdev(self):
        """
        Method to rename a other devices in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newotherdevname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def remove_otherdev(self):
        """
        Method to remove a other devices in Luna Configuration.
        """
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
