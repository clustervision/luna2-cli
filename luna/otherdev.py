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
__status__      = "Development"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log

class OtherDev():
    """
    OtherDev Class responsible to show, list, add, change,
    remove, rename and clone information for the OtherDev.
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
                Helper().show_error(f"Kindly choose from {actions}.")
        else:
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
        otherdev_show.add_argument('name', help='Other Device Name')
        Helper().common_list_args(otherdev_show)
        otherdev_add = otherdev_args.add_parser('add', help='Add Other Devices')
        otherdev_add.add_argument('name', help='Other Device Name')
        otherdev_add.add_argument('-N', '--network', required=True, help='Network Name')
        otherdev_add.add_argument('-ip', '--ipaddress', required=True, help='IP Address')
        otherdev_add.add_argument('-m', '--macaddress', help='MAC Address')
        otherdev_add.add_argument('-c', '--comment', action='store_true', help='Comment')
        otherdev_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_change = otherdev_args.add_parser('change', help='Change Other Devices')
        otherdev_change.add_argument('name', help='Other Device Name')
        otherdev_change.add_argument('-N', '--network', help='Network')
        otherdev_change.add_argument('-ip', '--ipaddress', help='IP Address')
        otherdev_change.add_argument('-m', '--macaddress', help='MAC Address')
        otherdev_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        otherdev_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_clone = otherdev_args.add_parser('clone', help='Clone Other Devices')
        otherdev_clone.add_argument('name', help='Other Device Name')
        otherdev_clone.add_argument('newotherdevname', help='New Other Device Name')
        otherdev_clone.add_argument('-N', '--network', required=True, help='Network')
        otherdev_clone.add_argument('-ip', '--ipaddress', required=True, help='IP Address')
        otherdev_clone.add_argument('-m', '--macaddress', help='MAC Address')
        otherdev_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        otherdev_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_rename = otherdev_args.add_parser('rename', help='Rename Other Devices')
        otherdev_rename.add_argument('name', help='Other Device Name')
        otherdev_rename.add_argument('newotherdevname', help='New Other Device Name')
        otherdev_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        otherdev_remove = otherdev_args.add_parser('remove', help='Remove Other Devices')
        otherdev_remove.add_argument('name', help='Other Device Name')
        otherdev_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_otherdev(self):
        """
        This method list all other devices.
        """
        return Helper().get_list(self.table, self.args)


    def show_otherdev(self):
        """
        This method show a specific other device.
        """
        return Helper().show_data(self.table, self.args)


    def add_otherdev(self):
        """
        This method add a other device.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
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
        This method update a other device.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
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


    def clone_otherdev(self):
        """
        This method clone a other device.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
        request_data = {'config':{self.table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_clone(self.table, payload['name'], request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 201:
            Helper().show_success(f'{payload["name"]} clone as {payload["newotherdevname"]}.')
        else:
            Helper().show_error(f'HTTP Error Code {response.status_code}.')
            Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def rename_otherdev(self):
        """
        This method rename a other device.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        request_data = {'config':{self.table:{self.args['name']: self.args}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(self.table, self.args['name'], request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Helper().show_success(f'{self.args["name"]} renamed to {self.args["newotherdevname"]}.')
        else:
            Helper().show_error(f'HTTP Error Code {response.status_code}.')
            Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def remove_otherdev(self):
        """
        This method remove a other device.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        self.logger.debug(f'Payload => {self.args}')
        response = Rest().get_delete(self.table, self.args['name'])
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Helper().show_success(f'{self.table.capitalize()}, {self.args["name"]} is deleted.')
        else:
            Helper().show_error(f'HTTP Error Code {response.status_code}.')
            Helper().show_error(f'HTTP Error {response.content}.')
        return True
