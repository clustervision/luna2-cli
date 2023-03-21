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
from luna.utils.presenter import Presenter
from luna.utils.inquiry import Inquiry
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
        self.get_list = None
        self.name_list = []
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "update", "rename", "delete", "clone"]
            if self.args["action"] in actions:
                self.get_list = Rest().get_data(self.table)
                if self.get_list:
                    self.name_list = list(self.get_list['config'][self.table].keys())
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
        Helper().common_add_args(bmcsetup_add, 'BMC Setup')
        bmcsetup_add.add_argument('-id', '--userid', type=int, help='UserID for BMC Setup')
        bmcsetup_add.add_argument('-u', '--username', help='Username for BMC Setup')
        bmcsetup_add.add_argument('-p', '--password', help='Password for BMC Setup')
        bmcsetup_add.add_argument('-nt', '--netchannel', type=int, help='Network Channel')
        bmcsetup_add.add_argument('-mt', '--mgmtchannel', type=int, help='Management Channel')
        bmcsetup_add.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        bmcsetup_add.add_argument('-c', '--comment', help='Comment for BMC Setup')
        bmcsetup_update = bmcsetup_args.add_parser('update', help='Update a BMC Setup')
        Helper().common_add_args(bmcsetup_update, 'BMC Setup')
        bmcsetup_update.add_argument('-id', '--userid', type=int, help='UserID for BMC Setup')
        bmcsetup_update.add_argument('-u', '--username', help='Username for BMC Setup')
        bmcsetup_update.add_argument('-p', '--password', help='Password for BMC Setup')
        bmcsetup_update.add_argument('-nt', '--netchannel', type=int, help='Network Channel')
        bmcsetup_update.add_argument('-mt', '--mgmtchannel', type=int, help='Management Channel')
        bmcsetup_update.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        bmcsetup_update.add_argument('-c', '--comment', help='Comment for BMC Setup')
        bmcsetup_clone = bmcsetup_args.add_parser('clone', help='Clone BMC Setup')
        Helper().common_add_args(bmcsetup_clone, 'BMC Setup')
        bmcsetup_clone.add_argument('-nn', '--newbmcname', help='New name of the BMC Setup')
        bmcsetup_clone.add_argument('-id', '--userid', type=int, help='UserID for BMC Setup')
        bmcsetup_clone.add_argument('-u', '--username', help='Username for BMC Setup')
        bmcsetup_clone.add_argument('-p', '--password', help='Password for BMC Setup')
        bmcsetup_clone.add_argument('-nt', '--netchannel', type=int, help='Network Channel')
        bmcsetup_clone.add_argument('-mt', '--mgmtchannel', type=int, help='Management Channel')
        bmcsetup_clone.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        bmcsetup_clone.add_argument('-c', '--comment', help='Comment for BMC Setup')
        bmcsetup_rename = bmcsetup_args.add_parser('rename', help='Rename BMC Setup')
        Helper().common_add_args(bmcsetup_rename, 'BMC Setup')
        bmcsetup_rename.add_argument('-nn', '--newbmcname', help='New name of the BMC Setup')
        bmcsetup_delete = bmcsetup_args.add_parser('delete', help='Delete BMC Setup')
        Helper().common_add_args(bmcsetup_delete, 'BMC Setup')
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
        if self.args['init']:
            payload['name'] = Helper().name_validate(0, 'BMC Setup', self.name_list)
            if payload['name']:
                payload['userid'] = Inquiry().ask_number(f"User ID for {payload['name']}:", True)
                payload['username'] = Inquiry().ask_text(f"Username for {payload['name']}:", True)
                payload['password'] = Inquiry().ask_secret(f"Password for {payload['name']}:", True)
                payload['netchannel'] = Inquiry().ask_number(f"Network Channel for {payload['name']}:", True)
                payload['mgmtchannel'] = Inquiry().ask_number(f"Management Channel for {payload['name']}:", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text(f"Unmanaged BMC Users for {payload['name']}:", True)
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
                payload = {}
        else:
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            if not self.args["name"]:
                Helper().show_error('BMC Setup name is a Mandatory Key.')
            elif self.args["name"] in self.name_list:
                Helper().show_warning(f'BMC Setup {self.args["name"]} present already.')
            else:
                payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            else:
                Helper().show_error(f'{self.table.capitalize()}, {payload["name"]} is not created.')
        return True


    def update_bmcsetup(self):
        """
        Method to update a bmc setup in Luna Configuration.
        """
        payload = {}
        if self.get_list:
            if self.args['init']:
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update:", self.name_list)
                payload['userid'] = Inquiry().ask_number(f"User ID for {payload['name']}:", True)
                payload['username'] = Inquiry().ask_text(f"Username for {payload['name']}:", True)
                payload['password'] = Inquiry().ask_secret(f"Password for {payload['name']}:", True)
                payload['netchannel'] = Inquiry().ask_number(f"Network Channel for {payload['name']}:", True)
                payload['mgmtchannel'] = Inquiry().ask_number(f"Management Channel for {payload['name']}:", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text(f"Unmanaged BMC Users for {payload['name']}:", True)
                comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                if comment:
                    payload['comment'] = Inquiry().ask_text(f"Comment for {payload['name']}:", True)
                filtered = {k: v for k, v in payload.items() if v != ''}
                payload.clear()
                payload.update(filtered)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Updating => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                msg = f'Update {payload["name"]} in {self.table.capitalize()}'
                confirm = Inquiry().ask_confirm(f'{msg}?')
                if not confirm:
                    Helper().show_error(f'{msg} is Aborted')
                    payload = {}
            else:
                for remove in ['debug', 'command', 'action', 'init']:
                    self.args.pop(remove, None)
                if not self.args["name"]:
                    Helper().show_error('BMC Setup name is a Mandatory Key.')
                elif self.args["name"] in self.name_list:
                    Helper().show_warning(f'BMC Setup {self.args["name"]} present already.')
                else:
                    payload = {k: v for k, v in self.args.items() if v is not None}
        else:
            Helper().show_error(f'No {self.table.capitalize()} is available.')
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
        return True


    def rename_bmcsetup(self):
        """
        Method to rename a bmc setup in Luna Configuration.
        """
        payload = {}
        if self.get_list:
            bmc_names = list(self.get_list['config']['bmcsetup'].keys())
            if self.args['init']:
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update", bmc_names)
                payload['newbmcname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                msg = f'Rename {payload["name"]} to {payload["newbmcname"]}'
                confirm = Inquiry().ask_confirm(f'{msg}?')
                if not confirm:
                    Helper().show_error(f'{msg} is Aborted.')
                    payload = {}
            else:
                for remove in ['debug', 'command', 'action', 'init']:
                    self.args.pop(remove, None)
                if self.args['name'] is None or self.args['newbmcname'] is None:
                    Helper().show_error('BMC Name and New BMC name both are required.')
                else:
                    if self.args["name"] not in bmc_names:
                        msg = f'{self.args["name"]} Not found in {self.table.capitalize()}.'
                        Helper().show_error(msg)
                    else:
                        payload = self.args
        else:
            response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                msg = f'{payload["name"]} is renamed to {payload["newbmcname"]}'
                Helper().show_success(f'{msg} in {self.table.capitalize()}.')
        return True


    def delete_bmcsetup(self):
        """
        Method to delete a bmc setup in Luna Configuration.
        """
        payload = {}
        if self.get_list:
            bmc_names = list(self.get_list['config']['bmcsetup'].keys())
            if self.args['init']:
                payload['name'] = Inquiry().ask_select("Select BMC Setup to delete", bmc_names)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Deleting => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                msg = f'Delete {payload["name"]} from {self.table.capitalize()}'
                confirm = Inquiry().ask_confirm(f'{msg}?')
                if not confirm:
                    Helper().show_error(f'{msg} is Aborted')
                    payload = {}
            else:
                for remove in ['debug', 'command', 'action', 'init']:
                    self.args.pop(remove, None)
                if self.args['name'] is None:
                    Helper().show_error('Kindly provide BMC Name or use -i.')
                else:
                    if self.args["name"] not in bmc_names:
                        msg = f'{self.args["name"]} Not found in {self.table.capitalize()}.'
                        Helper().show_error(msg)
                    else:
                        payload = self.args
        else:
            response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        if payload:
            response = Rest().get_delete(self.table, payload['name'])
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
        return True


    def clone_bmcsetup(self):
        """
        Method to rename a bmc setup in Luna Configuration.
        """
        payload = {}
        if self.get_list:
            bmc_names = list(self.get_list['config']['bmcsetup'].keys())
            if self.args['init']:
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update", bmc_names)
                payload['newbmcname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['userid'] = Inquiry().ask_number("Update BMC User ID", True)
                payload['username'] = Inquiry().ask_text("Update BMC Username", True)
                payload['password'] = Inquiry().ask_secret("Update BMC Password", True)
                payload['netchannel'] = Inquiry().ask_number("Update NET Channel", True)
                payload['mgmtchannel'] = Inquiry().ask_number("Update MGMT Channel", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users", True)
                comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                if comment:
                    payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)", True)

                data = self.get_list['config'][self.table][payload["name"]]
                for key, value in payload.items():
                    if value == '' and key in data:
                        payload[key] = data[key]
                filtered = {k: v for k, v in payload.items() if v is not None}
                payload.clear()
                payload.update(filtered)

                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'Clone {self.table.capitalize()} {payload["name"]} => {payload["newbmcname"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newbmcname"]}?')
                if not confirm:
                    Helper().show_error(f'Cloning of {payload["newbmcname"]} is Aborted')
                    payload = {}
            else:
                for remove in ['debug', 'command', 'action', 'init']:
                    self.args.pop(remove, None)
                if None not in [self.args["name"], self.args["newbmcname"]]:
                    payload = self.args
                    if payload["name"] in bmc_names:
                        data = self.get_list['config'][self.table][payload["name"]]
                        for key, value in payload.items():
                            if (value == '' or value is None) and key in data:
                                payload[key] = data[key]
                        filtered = {k: v for k, v in payload.items() if v is not None}
                        payload.clear()
                        payload.update(filtered)
                    else:
                        Helper().show_error(f'{payload["name"]} is not recognized.')
                        payload = {}
                else:
                    Helper().show_error('Source & Destination BMC names are required.')
                    payload = {}
        else:
            Helper().show_error(f'No {self.table.capitalize()} is available.')
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            if payload["newbmcname"] in bmc_names:
                Helper().show_error(f'{payload["newbmcname"]} is already present in {self.table.capitalize()}.')
            else:
                self.logger.debug(f'Payload => {request_data}')
                response = Rest().post_clone(self.table, payload['name'], request_data)
                self.logger.debug(f'Response => {response}')
                if response == 201:
                    Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloned as {payload["newbmcname"]}.')
                else:
                    Helper().show_error(f'HTTP Error {response}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True
