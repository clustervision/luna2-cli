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
from luna.utils.presenter import Presenter
from luna.utils.inquiry import Inquiry
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
        self.get_list = None
        self.name_list = []
        self.networks = None
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "update", "rename", "clone", "delete"]
            if self.args["action"] in actions:
                self.get_list = Rest().get_data(self.table)
                self.networks = Helper().network_list()
                if self.get_list:
                    self.name_list = list(self.get_list['config'][self.table].keys())
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
        Helper().common_add_args(otherdev_add, 'Other Device')
        Helper().common_switch_device_args(otherdev_add, 'Other Device')
        otherdev_update = otherdev_args.add_parser('update', help='Update Other Devices')
        Helper().common_add_args(otherdev_update, 'Other Device')
        Helper().common_switch_device_args(otherdev_update, 'Other Device')
        otherdev_clone = otherdev_args.add_parser('clone', help='Clone Other Devices')
        otherdev_clone.add_argument('-nn', '--newotherdevname', help='New name of the Other Device')
        Helper().common_add_args(otherdev_clone, 'Other Device')
        Helper().common_switch_device_args(otherdev_clone, 'Other Device')
        otherdev_rename = otherdev_args.add_parser('rename', help='Rename Other Devices')
        Helper().common_add_args(otherdev_rename, 'Other Device')
        otherdev_rename.add_argument('-nn', '--newotherdevname', help='New name of the Other Devices')
        otherdev_delete = otherdev_args.add_parser('delete', help='Delete Other Devices')
        Helper().common_add_args(otherdev_delete, 'Other Device')
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
        if self.networks:
            payload = {}
            if self.args['init']:
                payload['name'] = Helper().name_validate(0, 'Other Device', self.name_list)
                if payload['name']:
                    payload['network'] = Inquiry().ask_select(f"Network for {payload['name']}:", self.networks)
                    payload['ipaddress'] = Inquiry().ask_text(f"IP Address for {payload['name']}:")
                    payload['macaddress'] = Inquiry().ask_text(f"MAC Address for {payload['name']}:", True)
                    comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                    if comment:
                        payload['comment'] = Inquiry().ask_text(f"Comment for {payload['name']}:", True)
                    fields, rows  = Helper().filter_data_col(self.table, payload)
                    title = f'{self.table.capitalize()} Adding => {payload["name"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                    if not confirm:
                        Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    else:
                        filtered = {k: v for k, v in payload.items() if v != ''}
                        payload.clear()
                        payload.update(filtered)
            else:
                for remove in ['debug', 'command', 'action', 'init']:
                    self.args.pop(remove, None)
                if None in [self.args['name'], self.args['network'], self.args['ipaddress']]:
                    Helper().show_error('Other Device name, network name and IP address are mandatory.')
                    payload = {}
                elif self.args["name"] in self.name_list:
                    Helper().show_warning(f'Device {self.args["name"]} present already.')
                    payload = {}
                elif self.args["network"] not in self.networks:
                    Helper().show_warning(f'Network {self.args["network"]} is undefined.')
                    payload = {}
                else:
                    payload = {k: v for k, v in self.args.items() if v is not None}
        else:
            payload = {}
            Helper().show_error('Kindly create a network first.')
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            elif response == 204:
                Helper().show_warning(f'{payload["name"]} present already.')
            else:
                Helper().show_error(f'{self.table.capitalize()}, {payload["name"]} is not created.')
        return True


    def update_otherdev(self):
        """
        Method to update a other devices in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Device to update", names)
                payload['network'] = Inquiry().ask_text("Kindly provide Device Network", True)
                payload['ipaddress'] = Inquiry().ask_text("Kindly provide Device IP Address", True)
                payload['macaddress'] = Inquiry().ask_text("Kindly provide MAC Address", True)
                comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                if comment:
                    payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)", True)
                filtered = {k: v for k, v in payload.items() if v != ''}
                payload.clear()
                payload.update(filtered)
                if len(payload) != 1:
                    fields, rows  = Helper().filter_data_col(self.table, payload)
                    title = f'{self.table.capitalize()} Updating => {payload["name"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'update {payload["name"]} in {self.table.capitalize()}?')
                    if not confirm:
                        Helper().show_error(f'update {payload["name"]} into {self.table.capitalize()} Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            filtered = {k: v for k, v in payload.items() if v is not None}
            payload.clear()
            payload.update(filtered)
        if (len(payload) != 1) and ('name' in payload):
            request_data = {'config':{self.table:{payload['name']: payload}}}
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error('Nothing to update.')
        return True


    def rename_otherdev(self):
        """
        Method to rename a other devices in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Device to rename", names)
                payload['newotherdevname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Rename {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newotherdevname'] = None
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            error = False
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            if payload['name'] is None:
                error = Helper().show_error('Kindly provide Device Name.')
            if payload['newotherdevname'] is None:
                error = Helper().show_error('Kindly provide New Device Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newotherdevname'] and payload['name']:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newotherdevname"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_otherdev(self):
        """
        Method to delete a other devices in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Device to delete", names)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Deleting => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Delete {payload["name"]} from {self.table.capitalize()}?')
                if not confirm:
                    abort = Helper().show_error(f'Deletion of {payload["name"]}, {self.table.capitalize()} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide Device Name.')
        if abort is False:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {payload}')
                    response = Rest().get_delete(self.table, payload['name'])
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def clone_otherdev(self):
        """
        Method to rename a other devices in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Device to clone", names)
                payload['newotherdevname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['network'] = Inquiry().ask_text("Kindly provide Device Network", True)
                payload['ipaddress'] = Inquiry().ask_text("Kindly provide Device IP Address", True)
                payload['macaddress'] = Inquiry().ask_text("Kindly provide MAC Address", True)
                comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                if comment:
                    payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)", True)
                get_record = Rest().get_data(self.table, payload['name'])
                if get_record:
                    data = get_record['config'][self.table][payload["name"]]
                    for key, value in payload.items():
                        if value == '' and key in data:
                            payload[key] = data[key]
                    filtered = {k: v for k, v in payload.items() if v is not None}
                    payload.clear()
                    payload.update(filtered)

                if len(payload) != 1:
                    fields, rows  = Helper().filter_data_col(self.table, payload)
                    title = f'{self.table.capitalize()} Cloning : {payload["name"]} => {payload["newotherdevname"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newotherdevname"]}?')
                    if not confirm:
                        Helper().show_error(f'Cloning of {payload["newotherdevname"]} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            get_record = Rest().get_data(self.table, payload['name'])
            if get_record:
                data = get_record['config'][self.table][payload["name"]]
                for key, value in payload.items():
                    if (value == '' or value is None) and key in data:
                        payload[key] = data[key]
                filtered = {k: v for k, v in payload.items() if v is not None}
                payload.clear()
                payload.update(filtered)
        if len(payload) != 1:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                if payload["name"] in names:
                    if payload["newotherdevname"] in names:
                        Helper().show_error(f'{payload["newotherdevname"]} is already present in {self.table.capitalize()}.')
                    else:
                        self.logger.debug(f'Payload => {request_data}')
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        self.logger.debug(f'Response => {response}')
                        if response == 201:
                            Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newotherdevname"]}.')
                        else:
                            Helper().show_error(f'HTTP Error {response}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True
