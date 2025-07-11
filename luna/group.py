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
Main Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.1"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from operator import methodcaller
from copy import deepcopy
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import actions, BOOL_CHOICES, BOOL_META
from luna.utils.message import Message
from luna.utils.arguments import Arguments

class Group():
    """
    Group Class responsible to show, list, add, remove information for the Group
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "group"
        self.actions = actions(self.table)
        self.table_cap = self.table.capitalize()
        self.interface = "groupinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                if 'interface' in self.args["action"]:
                    call = methodcaller(f'{self.args["action"]}')
                else:
                    call = methodcaller(f'{self.args["action"]}_group')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Group class.
        """
        group_menu = subparsers.add_parser('group', help='Group operations')
        group_args = group_menu.add_subparsers(dest='action')
        group_list = group_args.add_parser('list', help='List Groups')
        Arguments().common_list_args(group_list)
        group_show = group_args.add_parser('show', help='Show Group')
        group_show.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(group_show)
        group_show.add_argument('-f', '--full-scripts', action='store_true', default=None, help='Show the Full Scripts')
        group_member = group_args.add_parser('member', help='Group Used by Nodes')
        group_member.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(group_member)
        group_add = group_args.add_parser('add', help='Add Group')
        group_add.add_argument('name', help='Name of the Group')
        Arguments().common_group_args(group_add)
        group_change = group_args.add_parser('change', help='Change Group')
        group_change.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        Arguments().common_group_args(group_change)
        group_clone = group_args.add_parser('clone', help='Clone Group.')
        group_clone.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        Arguments().common_group_args(group_clone)
        group_clone.add_argument('newgroupname', help='New Name for the Group')
        group_rename = group_args.add_parser('rename', help='Rename Group.')
        group_rename.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        group_rename.add_argument('newgroupname', help='New Name for the Group')
        group_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        group_remove = group_args.add_parser('remove', help='Remove Group')
        group_remove.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        group_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        group_ospush = group_args.add_parser('ospush', help='Push an OS Image for a Group')
        group_ospush.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        group_ospush.add_argument('-o', '--osimage', help='OS Image Name').completer = Helper().name_completer("osimage")
        group_ospush.add_argument('--nodry', action='store_true', default=None,
                                  help='No Dry flag to avoid dry run')
        group_ospush.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        group_interfaces = group_args.add_parser('listinterface', help='List Group Interfaces')
        group_interfaces.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(group_interfaces)
        group_interface = group_args.add_parser('showinterface', help='Show Group Interface')
        group_interface.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        group_interface.add_argument('interface', help='Name of the Group Interface').completer = Helper().interface_name_completer(self.table)
        Arguments().common_list_args(group_interface)
        change_interface = group_args.add_parser('changeinterface', help='Change Group Interface')
        change_interface.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        change_interface.add_argument('interface', help='Group Interface Name').completer = Helper().interface_name_completer(self.table)
        change_interface.add_argument('-N', '--network', help='Network Name').completer = Helper().name_completer("network")
        change_interface.add_argument('-L', '--vlanid', help='VLAN ID')
        change_interface.add_argument('-P', '--vlan_parent', help='VLAN parent interface')
        change_interface.add_argument('-B', '--bond_mode', help='Bonding mode')
        change_interface.add_argument('-A', '--bond_slaves', help='Bonding interface slaves')
        change_interface.add_argument('-D', '--dhcp', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='toggle dhcp')
        change_interface.add_argument('-O', '--options', action='store_true',
                                      help='Interfaces Options')
        change_interface.add_argument('-qO', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        change_interface.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        remove_interface = group_args.add_parser('removeinterface', help='Remove Group Interface')
        remove_interface.add_argument('name', help='Name of the Group').completer = Helper().name_completer(self.table)
        remove_interface.add_argument('interface', help='Name of the Group Interface').completer = Helper().interface_name_completer(self.table)
        remove_interface.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_group(self):
        """
        Method to list all groups from Luna Configuration.
        """
        #return Helper().get_list(self.table, self.args)
        response = False
        fields, rows = [], []
        get_list = Rest().get_data(self.table)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][self.table]
            if 'raw' in self.args and self.args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = Helper().filter_data(self.table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table.capitalize()} >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'{self.table} is not found.')
        return response



    def show_group(self):
        """
        Method to show a group in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def member_group(self):
        """
        This method will show all Nodes tied with the group.
        """
        return Helper().member_record(self.table, self.args)


    def add_group(self):
        """
        Method to add new group in Luna Configuration.
        """
        if self.args['interface'] is None and (self.args['network'] or self.args['options']):
            Message().error_exit("ERROR :: Kindly supply the interface in order to use the network or options.")
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['vlanid']:
                interface['vlanid'] = self.args['vlanid']
            if self.args['vlan_parent']:
                interface['vlan_parent'] = self.args['vlan_parent']
            if self.args['bond_mode']:
                interface['bond_mode'] = self.args['bond_mode']
            if self.args['bond_slaves']:
                interface['bond_slaves'] = self.args['bond_slaves']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['dhcp']:
                interface['dhcp'] = self.args['dhcp']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
        return Helper().add_record(self.table, self.args)


    def change_group(self):
        """
        Method to change a group in Luna Configuration.
        """
        local = False
        if 'local' in self.args:
            local = self.args['local']
            del self.args['local']
        real_args = deepcopy(self.args)
        if self.args['interface'] is None and (self.args['network'] or self.args['options']):
            Message().error_exit("ERROR :: Kindly supply the interface in order to use the network or options.")
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['vlanid']:
                interface['vlanid'] = self.args['vlanid']
            if self.args['vlan_parent']:
                interface['vlan_parent'] = self.args['vlan_parent']
            if self.args['bond_mode']:
                interface['bond_mode'] = self.args['bond_mode']
            if self.args['bond_slaves']:
                interface['bond_slaves'] = self.args['bond_slaves']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['dhcp']:
                interface['dhcp'] = self.args['dhcp']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
        change = Helper().compare_data(self.table, real_args)
        if change is True:
            Helper().update_record(self.table, self.args, local)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')
        # return Helper().update_record(self.table, self.args)


    def rename_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        return Helper().rename_record(self.table, self.args, self.args["newgroupname"])


    def remove_group(self):
        """
        Method to remove a group in Luna Configuration.
        """
        return Helper().delete_record(self.table, self.args)


    def ospush_group(self):
        """
        Method to push an osimage to a group.
        """
        return Helper().push_osimage(self.table, self.args)


    def clone_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        if self.args['interface'] is None and (self.args['network'] or self.args['options']):
            Message().error_exit("ERROR :: Kindly supply the interface in order to use the network or options.")
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['vlanid']:
                interface['vlanid'] = self.args['vlanid']
            if self.args['vlan_parent']:
                interface['vlan_parent'] = self.args['vlan_parent']
            if self.args['bond_mode']:
                interface['bond_mode'] = self.args['bond_mode']
            if self.args['bond_slaves']:
                interface['bond_slaves'] = self.args['bond_slaves']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['dhcp']:
                interface['dhcp'] = self.args['dhcp']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
        return Helper().clone_record(self.table, self.args)


    def listinterface(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces')
        get_list = Rest().get_data(self.table, self.args['name']+'/interfaces')
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces']
            if self.args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = Helper().filter_interface(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table_cap} {self.args["name"]} Interfaces >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return response


    def showinterface(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        response = False
        uri = self.args['name']+'/interfaces/'+self.args['interface']
        self.logger.debug(f'Table => {self.table} and URI => {uri}')
        get_list = Rest().get_data(self.table, uri)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces'][0]
            if self.args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = Helper().filter_data_col(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table_cap} {self.args["name"]} Interface [{self.args["interface"]}]'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            msg = f'{self.args["interface"]} not found in {self.table} {self.args["name"]}'
            msg = f'{msg} OR {self.args["name"]} is unavailable.'
            response = Message().show_error(msg)
        return response


    def changeinterface(self):
        """
        Method to change a Group interfaces in Luna Configuration.
        """
        real_args = deepcopy(self.args)
        uri = self.table+'/'+self.args['name']+'/interfaces'
        group_name = self.args['name']
        self.args['name'] = self.args['interface']
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['vlanid']:
                interface['vlanid'] = self.args['vlanid']
            if self.args['vlan_parent']:
                interface['vlan_parent'] = self.args['vlan_parent']
            if self.args['bond_mode']:
                interface['bond_mode'] = self.args['bond_mode']
            if self.args['bond_slaves']:
                interface['bond_slaves'] = self.args['bond_slaves']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['dhcp']:
                interface['dhcp'] = self.args['dhcp']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
        payload = Helper().prepare_payload(uri, self.args)
        if payload:
            del payload['name']
            request_data = {'config': {self.table: {group_name: payload}}}
            self.logger.debug(f'Payload => {request_data}')

            change = Helper().compare_data(self.table, real_args)
            if change is True:
                response = Rest().post_data(self.table, group_name+'/interfaces', request_data)
                self.logger.debug(f'Response => {response}')
                if response.status_code == 204:
                    Message().show_success(f'Group {group_name} Interface {interface["interface"]} is updated.')
                else:
                    Message().error_exit(response.content, response.status_code)
            else:
                Message().show_error('Nothing is changed, Kindly change something to update')

        else:
            Message().show_error('Nothing to update.')
        return True


    def removeinterface(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            uri = payload['name']+'/interfaces/'+payload['interface']
            self.logger.debug(f"URI {uri}")
            response = Rest().get_delete(self.table, uri)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                msg = f'Group {payload["name"]} Interface {payload["interface"]} is removed.'
                Message().show_success(msg)
            else:
                Message().error_exit(response.content, response.status_code)
        return response
