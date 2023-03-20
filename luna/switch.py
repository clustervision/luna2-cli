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
from luna.utils.presenter import Presenter
from luna.utils.inquiry import Inquiry
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
        self.get_list = None
        self.name_list = []
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "update", "rename", "clone", "delete"]
            if self.args["action"] in actions:
                self.get_list = Rest().get_data(self.table)
                if self.get_list:
                    self.name_list = list(self.get_list['config'][self.table].keys())
                call = methodcaller(f'{self.args["action"]}_switch')
                call(self)
            else:
                print("Not a valid option.")
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
        Helper().common_add_args(switch_add, 'Switch')
        switch_add.add_argument('-N', '--network', help='Network Switch belongs to')
        switch_add.add_argument('-ip', '--ipaddress', help='IP of the Switch')
        switch_add.add_argument('-r', '--read', default='public', help='Read community')
        switch_add.add_argument('-w', '--rw', default='private', help='Write community')
        switch_add.add_argument('-o', '--oid', default='.1.3.6.1.2.1.17.7.1.2.2.1.2', help='OID of the Switch')
        switch_add.add_argument('-c', '--comment', help='Comment for Switch')
        switch_update = switch_args.add_parser('update', help='Update Switch')
        Helper().common_add_args(switch_update, 'Switch')
        switch_update.add_argument('-N', '--network', help='Network Switch belongs to')
        switch_update.add_argument('-ip', '--ipaddress', help='IP of the Switch')
        switch_update.add_argument('-r', '--read', help='Read community')
        switch_update.add_argument('-w', '--rw', help='Write community')
        switch_update.add_argument('-o', '--oid', help='OID of the Switch')
        switch_update.add_argument('-c', '--comment', help='Comment for Switch')
        switch_clone = switch_args.add_parser('clone', help='Clone Switch')
        Helper().common_add_args(switch_clone, 'Switch')
        switch_clone.add_argument('-nn', '--newswitchname', help='New name of the Switch')
        switch_clone.add_argument('-N', '--network', help='Network Switch belongs to')
        switch_clone.add_argument('-ip', '--ipaddress', help='IP of the Switch')
        switch_clone.add_argument('-r', '--read', help='Read community')
        switch_clone.add_argument('-w', '--rw', help='Write community')
        switch_clone.add_argument('-o', '--oid', help='OID of the Switch')
        switch_clone.add_argument('-c', '--comment', help='Comment for Switch')
        switch_rename = switch_args.add_parser('rename', help='Rename Switch')
        Helper().common_add_args(switch_rename, 'Switch')
        switch_rename.add_argument('-nn', '--newswitchname', help='New name of the Switch')
        switch_delete = switch_args.add_parser('delete', help='Delete Switch')
        Helper().common_add_args(switch_delete, 'Switch')
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
        payload = {'oid': '.1.3.6.1.2.1.17.7.1.2.2.1.2', 'read': 'public', 'rw': 'private'}
        if self.args['init']:
            payload['name'] = Helper().name_validate(0, 'Switch', self.name_list)
            if payload['name']:
                payload['network'] = Inquiry().ask_text(f"Network for {payload['name']}:")
                payload['ipaddress'] = Inquiry().ask_text(f"IP Address for {payload['name']}:")
                payload['oid'] = Inquiry().ask_text(f"OID for {payload['name']}:", True)
                payload['read'] = Inquiry().ask_text(f"Read community for {payload['name']}:", True)
                payload['rw'] = Inquiry().ask_text(f"Write community for {payload['name']}:", True)
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
            if None in [self.args['name'], self.args['network'], self.args['ipaddress']]:
                Helper().show_error('Switch name, network name and IP address are mandatory.')
                payload = {}
            else:
                if self.args["name"] in self.name_list:
                    Helper().show_warning(f'Switch {self.args["name"]} present already.')
                    payload = {}
                else:
                    payload = {k: v for k, v in self.args.items() if v != None}
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


    def update_switch(self):
        """
        Method to update a switch in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Switch to update", names)
                payload['network'] = Inquiry().ask_text("Kindly provide Switch Network", True)
                payload['ipaddress'] = Inquiry().ask_text("Kindly provide Switch IP Address", True)
                payload['oid'] = Inquiry().ask_text("Kindly provide Switch OID", True)
                payload['read'] = Inquiry().ask_text("Kindly provide Read community", True)
                payload['rw'] = Inquiry().ask_text("Kindly provide Write community", True)
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
                    confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                    if not confirm:
                        Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
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


    def rename_switch(self):
        """
        Method to rename a switch in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Switch to rename", names)
                payload['newswitchname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newswitchname'] = None
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            error = False
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            if payload['name'] is None:
                error = Helper().show_error('Kindly provide Switch Name.')
            if payload['newswitchname'] is None:
                error = Helper().show_error('Kindly provide New Switch Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newswitchname'] and payload['name']:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newswitchname"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_switch(self):
        """
        Method to delete a switch in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Switch to delete", names)
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
                abort = Helper().show_error('Kindly provide Switch Name.')
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


    def clone_switch(self):
        """
        Method to rename a switch in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Switch to update", names)
                payload['newswitchname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['network'] = Inquiry().ask_text("Kindly provide Switch Network", True)
                payload['ipaddress'] = Inquiry().ask_text("Kindly provide Switch IP Address", True)
                payload['oid'] = Inquiry().ask_text("Kindly provide Switch OID", True)
                payload['read'] = Inquiry().ask_text("Kindly provide Read community", True)
                payload['rw'] = Inquiry().ask_text("Kindly provide Write community", True)
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
                    title = f'{self.table.capitalize()} Cloning : {payload["name"]} => {payload["newswitchname"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newswitchname"]}?')
                    if not confirm:
                        Helper().show_error(f'Cloning of {payload["newswitchname"]} is Aborted')
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
                    if payload["newswitchname"] in names:
                        Helper().show_error(f'{payload["newswitchname"]} is already present in {self.table.capitalize()}.')
                    else:
                        self.logger.debug(f'Payload => {request_data}')
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        self.logger.debug(f'Response => {response}')
                        if response == 201:
                            Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newswitchname"]}.')
                        else:
                            Helper().show_error(f'HTTP Error {response}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True
