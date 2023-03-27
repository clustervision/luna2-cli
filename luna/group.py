#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Class for the CLI
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
from luna.utils.rest import Rest
from luna.utils.log import Log

class Group():
    """
    Group Class responsible to show, list,
    add, remove information for the Group
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "group"
        self.interface = "groupinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in ["list", "show", "add", "change", "rename", "remove", "clone"]:
                call = methodcaller(f'{self.args["action"]}_group')
                call(self)
            elif self.args["action"] == "interfaces":
                self.list_interfaces()
            elif self.args["action"] == "interface":
                self.show_interface()
            elif self.args["action"] == "changeinterface":
                self.change_interface()
            elif self.args["action"] == "removeinterface":
                self.remove_interface()
            else:
                Helper().show_error("Not a valid option.")
        if parser and subparsers:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Group class.
        """
        group_menu = subparsers.add_parser('group', help='Group operations')
        group_args = group_menu.add_subparsers(dest='action')
        group_list = group_args.add_parser('list', help='List Groups')
        Helper().common_list_args(group_list)
        group_show = group_args.add_parser('show', help='Show Group')
        group_show.add_argument('name', help='Name of the Group')
        Helper().common_list_args(group_show)
        group_add = group_args.add_parser('add', help='Add Group')
        group_add.add_argument('name', help='Name of the Group')
        group_add.add_argument('-b', '--setupbmc', help='BMC Setup')
        group_add.add_argument('-o', '--osimage', help='OS Image Name')
        group_add.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_add.add_argument('-D', '--domain', help='Domain Name')
        group_add.add_argument('-pre', '--prescript', help='Pre Script')
        group_add.add_argument('-part', '--partscript', help='Part Script')
        group_add.add_argument('-post', '--postscript', help='Post Script')
        group_add.add_argument('-pi', '--provision_interface', help='Provision Interface')
        group_add.add_argument('-pm', '--provision_method', help='Provision Method')
        group_add.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        group_add.add_argument('-nb', '--netboot', help='Network Boot')
        group_add.add_argument('-li', '--localinstall', help='Local Install')
        group_add.add_argument('-bm', '--bootmenu', help='Boot Menu')
        group_add.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        group_add.add_argument('-if', '--interface', action='append', help='Interface Name')
        group_add.add_argument('-N', '--network', action='append', help='Interface Network Name')
        group_add.add_argument('-c', '--comment', help='Comment')
        group_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_change = group_args.add_parser('change', help='Change Group')
        group_change.add_argument('name', help='Name of the Group')
        group_change.add_argument('-b', '--setupbmc', help='BMC Setup')
        group_change.add_argument('-o', '--osimage', help='OS Image Name')
        group_change.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_change.add_argument('-D', '--domain', help='Domain Name')
        group_change.add_argument('-pre', '--prescript', help='Pre Script')
        group_change.add_argument('-part', '--partscript', help='Part Script')
        group_change.add_argument('-post', '--postscript', help='Post Script')
        group_change.add_argument('-pi', '--provision_interface', help='Provision Interface')
        group_change.add_argument('-pm', '--provision_method', help='Provision Method')
        group_change.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        group_change.add_argument('-nb', '--netboot', help='Network Boot')
        group_change.add_argument('-li', '--localinstall', help='Local Install')
        group_change.add_argument('-bm', '--bootmenu', help='Boot Menu')
        group_change.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        group_change.add_argument('-if', '--interface', action='append', help='Interface Name')
        group_change.add_argument('-N', '--network', action='append', help='Interface Network Name')
        group_change.add_argument('-c', '--comment', help='Comment')
        group_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_clone = group_args.add_parser('clone', help='Clone Group.')
        group_clone.add_argument('name', help='Name of the Group')
        group_clone.add_argument('newgroupname', help='New Name for the Group')
        group_clone.add_argument('-b', '--setupbmc', help='BMC Setup')
        group_clone.add_argument('-o', '--osimage', help='OS Image Name')
        group_clone.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_clone.add_argument('-D', '--domain', help='Domain Name')
        group_clone.add_argument('-pre', '--prescript', help='Pre Script')
        group_clone.add_argument('-part', '--partscript', help='Part Script')
        group_clone.add_argument('-post', '--postscript', help='Post Script')
        group_clone.add_argument('-pi', '--provision_interface', help='Provision Interface')
        group_clone.add_argument('-pm', '--provision_method', help='Provision Method')
        group_clone.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        group_clone.add_argument('-nb', '--netboot', help='Network Boot')
        group_clone.add_argument('-li', '--localinstall', help='Local Install')
        group_clone.add_argument('-bm', '--bootmenu', help='Boot Menu')
        group_clone.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        group_clone.add_argument('-if', '--interface', action='append', help='Interface Name')
        group_clone.add_argument('-N', '--network', action='append', help='Interface Network Name')
        group_clone.add_argument('-c', '--comment', help='Comment')
        group_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_rename = group_args.add_parser('rename', help='Rename Group.')
        group_rename.add_argument('name', help='Name of the Group')
        group_rename.add_argument('newgroupname', help='New Name for the Group')
        group_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_remove = group_args.add_parser('remove', help='Remove Group')
        group_remove.add_argument('name', help='Name of the Group')
        group_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_interfaces = group_args.add_parser('interfaces', help='List Group Interfaces')
        group_interfaces.add_argument('name', help='Name of the Group')
        Helper().common_list_args(group_interfaces)
        group_interface = group_args.add_parser('interface', help='Show Group Interface')
        group_interface.add_argument('name', help='Name of the Group')
        group_interface.add_argument('interface', help='Name of the Group Interface')
        Helper().common_list_args(group_interface)
        group_changeinterface = group_args.add_parser('changeinterface', help='Change Group Interface')
        group_changeinterface.add_argument('name', help='Name of the Group')
        group_changeinterface.add_argument('interface', help='Group Interface Name')
        group_changeinterface.add_argument('network', help='Network Name')
        group_changeinterface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_removeinterface = group_args.add_parser('removeinterface', help='Remove Group Interface')
        group_removeinterface.add_argument('name', help='Name of the Group')
        group_removeinterface.add_argument('interface', help='Name of the Group Interface')
        group_removeinterface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_group(self):
        """
        Method to list all groups from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_group(self):
        """
        Method to show a network in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_group(self):
        """
        Method to add new group in Luna Configuration.
        """
        error = False
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        iface = [self.args['interface'], self.args['network']]
        ifacecount = sum(x is not None for x in iface)
        if ifacecount:
            if ifacecount == 2:
                if len(self.args['interface']) == len(self.args['network']):
                    interface_data = {'interface': self.args['interface'], 'network': self.args['network']}
                    self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
            else:
                error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
        del self.args['interface']
        del self.args['network']
        if error:
            Helper().show_error('Operation Aborted.')
            payload = {}
        else:
            payload = Helper().prepare_payload(self.args)
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def change_group(self):
        """
        Method to change a group in Luna Configuration.
        """
        payload = {}
        error = False
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        iface = [self.args['interface'], self.args['network']]
        ifacecount = sum(x is not None for x in iface)
        if ifacecount:
            if ifacecount == 2:
                if len(self.args['interface']) == len(self.args['network']):
                    interface_data = {'interface': self.args['interface'], 'network': self.args['network']}
                    self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
            else:
                error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
        del self.args['interface']
        del self.args['network']
        if error:
            Helper().show_error('Operation Aborted.')
            self.args.clear()
        payload = Helper().prepare_payload(self.args)
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
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


    def rename_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newgroupname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def remove_group(self):
        """
        Method to remove a group in Luna Configuration.
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


    def clone_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        iface = [self.args['interface'], self.args['network']]
        ifacecount = sum(x is not None for x in iface)
        if ifacecount:
            if ifacecount == 2:
                if len(self.args['interface']) == len(self.args['network']):
                    interface_data = {'interface': self.args['interface'], 'network': self.args['network']}
                    self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
            else:
                error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
        del self.args['interface']
        del self.args['network']
        if error:
            Helper().show_error('Operation Aborted.')
            self.args.clear()
        payload = Helper().prepare_payload(self.args)
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_clone(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newgroupname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def list_interfaces(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces')
        get_list = Rest().get_data(self.table, self.args['name']+'/interfaces')
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces']
            if self.args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                fields, rows  = Helper().filter_interface(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table.capitalize()} {self.args["name"]} Interfaces >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Helper().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return response


    def show_interface(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces{self.args["interface"]}')
        get_list = Rest().get_data(self.table, self.args['name']+'/interfaces/'+self.args['interface'])
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces'][0]
            if self.args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                fields, rows  = Helper().filter_data_col(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table.capitalize()} [{self.args["name"]}] => Interface {self.args["interface"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'Interface {self.args["interface"]} not found in {self.table} {self.args["name"]} OR {self.args["name"]} is unavailable.')
        return response


    def change_interface(self):
        """
        Method to change a Group interfaces in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        self.args['interfaces'] = {'interface': self.args['interface'], 'network': self.args['network']}
        del self.args['interface']
        del self.args['network']
        payload = Helper().prepare_payload(self.args)
        if payload:
            group_name = payload['name']
            del payload['name']
            request_data = {'config': {self.table: {group_name: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, group_name+'/interfaces', request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'Interfaces updated in {self.table.capitalize()} {group_name}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error('Nothing to update.')
        return response


    def remove_interface(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            self.logger.debug(f"URI {payload['name']}/interfaces/{payload['interface']}")
            response = Rest().get_delete(self.table, payload['name']+'/interfaces/'+payload['interface'])
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'Interface {payload["interface"]} Deleted from {self.table.capitalize()} {payload["name"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return response
