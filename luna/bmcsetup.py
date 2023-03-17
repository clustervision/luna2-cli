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

    def __init__(self, args=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "bmcsetup"
        self.get_list = None
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in ["update", "rename", "delete", "clone"]:
                self.get_list = Rest().get_data(self.table)
            call = methodcaller(f'{self.args["action"]}_bmcsetup')
            call(self)


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
            payload['name'] = Inquiry().ask_text("BMC Setup Name:")
            payload['userid'] = Inquiry().ask_number("User ID:", True)
            payload['username'] = Inquiry().ask_text("Username:", True)
            payload['password'] = Inquiry().ask_secret("Password:", True)
            payload['netchannel'] = Inquiry().ask_number("Network Channel:", True)
            payload['mgmtchannel'] = Inquiry().ask_number("Management Channel:", True)
            payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users:", True)
            comment = Inquiry().ask_confirm("Do you want to provide a comment?")
            if comment:
                payload['comment'] = Inquiry().ask_text("Comment:", True)
            fields, rows  = Helper().filter_data_col(self.table, payload)
            title = f'{self.table.capitalize()} Adding => {payload["name"]}'
            Presenter().show_table_col(title, fields, rows)
            confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
            if not confirm:
                Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
        else:
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            if not self.args["name"]:
                payload = {}
                Helper().show_error('BMC Setup name is a Mandatory Key.')
            else:
                payload = self.args
                payload = {k: v for k, v in self.args.items() if v is not None}
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


    def update_bmcsetup(self):
        """
        Method to update a bmc setup in Luna Configuration.
        """
        payload = {}
        if self.get_list:
            bmc_names = list(self.get_list['config']['bmcsetup'].keys())
            if self.args['init']:
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update:", bmc_names)
                payload['userid'] = Inquiry().ask_number("Update User ID", True)
                payload['username'] = Inquiry().ask_text("Update Username", True)
                payload['password'] = Inquiry().ask_secret("Update Password", True)
                payload['netchannel'] = Inquiry().ask_number("Update Network Channel", True)
                payload['mgmtchannel'] = Inquiry().ask_number("Update Management Channel", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Update Unmanaged BMC Users", True)
                comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                if comment:
                    payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)", True)
                filtered = {k: v for k, v in payload.items() if v != ''}
                payload.clear()
                payload.update(filtered)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Updating => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload = {}
            else:
                for remove in ['debug', 'command', 'action', 'init']:
                    self.args.pop(remove, None)
                if not self.args["name"]:
                    Helper().show_error('BMC Setup name is a Mandatory Key.')
                else:
                    if self.args["name"] not in bmc_names:
                        Helper().show_error(f'{self.args["name"]} Not found in {self.table.capitalize()}.')
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
        if self.args['init']:
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update", names)
                payload['newbmcname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newbmcname'] = None
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            if self.args['name'] is None:
                Helper().show_error('Kindly provide BMC Name.')
            if self.args['newbmcname'] is None:
                Helper().show_error('Kindly provide New BMC Name.')
            payload = self.args
        if payload['newbmcname'] and payload['name']:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newbmcname"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_bmcsetup(self):
        """
        Method to delete a bmc setup in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select BMC Setup to delete", names)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Deleting => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Delete {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    abort = Helper().show_error(f'Deletion of {payload["name"]}, {self.table.capitalize()} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            payload = self.args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide BMC Name.')
        if abort is False:
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    response = Rest().get_delete(self.table, payload['name'])
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def clone_bmcsetup(self):
        """
        Method to rename a bmc setup in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update", names)
                payload['newbmcname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['userid'] = Inquiry().ask_number("Update BMC User ID", True)
                payload['username'] = Inquiry().ask_text("Update BMC Username", True)
                payload['password'] = Inquiry().ask_secret("Update BMC Password", True)
                payload['netchannel'] = Inquiry().ask_number("Update NET Channel", True)
                payload['mgmtchannel'] = Inquiry().ask_number("Update MGMT Channel", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Update Unmanaged BMC Users", True)
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
                    title = f'{self.table.capitalize()} Cloning : {payload["name"]} => {payload["newbmcname"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newbmcname"]}?')
                    if not confirm:
                        Helper().show_error(f'Cloning of {payload["newbmcname"]} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
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
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    if payload["newbmcname"] in names:
                        Helper().show_error(f'{payload["newbmcname"]} is already present in {self.table.capitalize()}.')
                    else:
                        self.logger.debug(f'Payload => {request_data}')
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        self.logger.debug(f'Response => {response}')
                        if response == 201:
                            Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newbmcname"]}.')
                        else:
                            Helper().show_error(f'HTTP Error {response}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True
