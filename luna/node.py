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
Node Class for the CLI
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


class Node():
    """
    Node Class responsible to show, list, add, remove information for the Node
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "node"
        self.actions = actions(self.table)
        self.table_cap = self.table.capitalize()
        self.interface = "nodeinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                if 'interface' in self.args["action"]:
                    call = methodcaller(f'{self.args["action"]}')
                else:
                    call = methodcaller(f'{self.args["action"]}_node')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Node class.
        """
        node_menu = subparsers.add_parser('node', help='Compute Node operations.')
        node_args = node_menu.add_subparsers(dest='action')
        node_list = node_args.add_parser('list', help='List All Nodes')
        Arguments().common_list_args(node_list)
        node_show = node_args.add_parser('show', help='Show A Node')
        node_show.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(node_show)
        node_show.add_argument('-f', '--full-scripts', action='store_true', default=None, help='Show the Full Scripts')
        node_add = node_args.add_parser('add', help='Add A Node')
        node_add.add_argument('name', help='Name of the Node')
        Arguments().common_node_args(node_add, True)
        node_change = node_args.add_parser('change', help='Make Changes Into a Node')
        node_change.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        Arguments().common_node_args(node_change)
        node_clone = node_args.add_parser('clone', help='Clone A Node')
        node_clone.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        Arguments().common_node_args(node_clone)
        node_clone.add_argument('newnodename', help='New Name for the Node')
        node_rename = node_args.add_parser('rename', help='Rename A Node')
        node_rename.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        node_rename.add_argument('newnodename', help='New Name for the Node')
        node_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        node_remove = node_args.add_parser('remove', help='Remove A Node')
        node_remove.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        node_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        node_osgrab = node_args.add_parser('osgrab', help='Gran an OS Image for a Node')
        node_osgrab.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        node_osgrab.add_argument('-o', '--osimage', help='OS Image Name').completer = Helper().name_completer("osimage")
        node_osgrab.add_argument('-b', '--bare', action='store_true', default=None, help='Bare OS Image(Exclude Packing)')
        node_osgrab.add_argument('--nodry', action='store_true', default=None,
                                 help='No Dry flag to avoid dry run')
        node_osgrab.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        node_ospush = node_args.add_parser('ospush', help='Push an OS Image for a Node')
        node_ospush.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        node_ospush.add_argument('-o', '--osimage', help='OS Image Name').completer = Helper().name_completer("osimage")
        node_ospush.add_argument('--nodry', action='store_true', default=None,
                                 help='No Dry flag to avoid dry run')
        node_ospush.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        node_interfaces = node_args.add_parser('listinterface', help='List Node Interfaces')
        node_interfaces.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        Arguments().common_list_args(node_interfaces)
        node_interface = node_args.add_parser('showinterface', help='Show Node Interface')
        node_interface.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        node_interface.add_argument('interface', help='Name of the Node Interface').completer = Helper().interface_name_completer(self.table)
        Arguments().common_list_args(node_interface)
        change_interface = node_args.add_parser('changeinterface', help='Change Node Interface')
        change_interface.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        change_interface.add_argument('interface', help='Name of the Node Interface').completer = Helper().interface_name_completer(self.table)
        change_interface.add_argument('-N', '--network', help='Network Name').completer = Helper().name_completer("network")
        change_interface.add_argument('--mtu', help='MTU size')
        change_interface.add_argument('-L', '--vlanid', help='VLAN ID')
        change_interface.add_argument('-P', '--vlan_parent', help='VLAN parent interface')
        change_interface.add_argument('-B', '--bond_mode', help='Bonding mode')
        change_interface.add_argument('-A', '--bond_slaves', help='Bonding interface slaves')
        change_interface.add_argument('-I', '--ipaddress', help='IP Address')
        change_interface.add_argument('-M', '--macaddress', help='MAC Address')
        change_interface.add_argument('-D', '--dhcp', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='toggle dhcp')
        change_interface.add_argument('-O', '--options', action='store_true',
                                      help='Interfaces Options')
        change_interface.add_argument('-qO', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        change_interface.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        remove_interface = node_args.add_parser('removeinterface', help='Remove Node Interface')
        remove_interface.add_argument('name', help='Name of the Node').completer = Helper().name_completer(self.table)
        remove_interface.add_argument('interface', help='Name of the Node Interface').completer = Helper().interface_name_completer(self.table)
        remove_interface.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_node(self):
        """
        Method to list all nodes from Luna Configuration.
        """
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
                fields, rows  = Helper().filter_nodelist_col(self.table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table.capitalize()} >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'{self.table} is not found.')
        return response


    def show_node(self):
        """
        Method to show a node in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_node(self):
        """
        Method to add new node in Luna Configuration.
        """
        hostlist = Helper().get_hostlist(self.args['name'])
        hostlist = Helper().luna_hostlist(hostlist)
        if self.args['interface'] is None and (self.args['network'] or self.args['ipaddress'] or self.args['macaddress'] or self.args['options']):
            Message().error_exit("ERROR :: Kindly supply the interface in order to use the network, ipaddress, macaddress or options.")
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
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress'] or self.args['macaddress'] == '':
                interface['macaddress'] = self.args['macaddress']
            if self.args['options'] or self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['mtu'] or self.args['mtu'] == '':
                interface['mtu'] = self.args['mtu']
            if self.args['dhcp']:
                interface['dhcp'] = self.args['dhcp']

        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options', 'mtu', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
            if len(hostlist) > 1 and ('ipaddress' in interface or 'macaddress' in interface):
                Message().error_exit('Interface IP Address or MAC Address can not be use with the hostlist, Kindly provide the single node or remove the IP Address and MAC Address.')
        record = Rest().get_data(self.table)
        if record.status_code == 200:
            if 'config' in record.content:
                if self.table in record.content['config']:
                    records = list(record.content['config'][self.table].keys())
                    if any(x in records for x in hostlist) is False:
                        if hostlist:
                            for each in hostlist:
                                if each not in records:
                                    self.args['name'] = each
                                    Helper().add_record(self.table, self.args)
                        else:
                            Message().error_exit(f'Node Hostlist is: {hostlist}')
                    else:
                        for each in hostlist:
                            if each in records:
                                Message().show_error(f'Node already present in database: {each}')

                else:
                    Message().error_exit('Node are not available at this moment.')
            elif 'message' in record.content:
                Message().error_exit(record.content['message'])
            else:
                Message().error_exit('Node are not available at this moment.')
        else:
            for each in hostlist:
                self.args['name'] = each
                Helper().add_record(self.table, self.args)
        return True



    def change_node(self):
        """
        Method to change a node in Luna Configuration.
        """
        local = False
        if 'local' in self.args:
            local = self.args['local']
            del self.args['local']
        real_args = deepcopy(self.args)
        hostlist = Helper().get_hostlist(self.args['name'])
        hostlist = Helper().luna_hostlist(hostlist)
        if self.args['interface'] is None and (self.args['network'] or self.args['ipaddress'] or self.args['macaddress'] or self.args['options']):
            Message().error_exit("ERROR :: Kindly supply the interface in order to use the network, ipaddress, macaddress or options.")
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
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress'] or self.args['macaddress'] == '':
                interface['macaddress'] = self.args['macaddress']
            if self.args['options'] or self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['mtu'] or self.args['mtu'] == '':
                interface['mtu'] = self.args['mtu']
            if self.args['dhcp']:
                interface['dhcp'] = self.args['dhcp']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options', 'mtu', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
            if len(hostlist) > 1 and ('ipaddress' in interface or 'macaddress' in interface):
                Message().error_exit('Interface IP Address or MAC Address can not be use with the hostlist, Kindly provide the single node or remove the IP Address and MAC Address.')
        record = Rest().get_data(self.table)
        if record.status_code == 200:
            if 'config' in record.content:
                if self.table in record.content['config']:
                    records = list(record.content['config'][self.table].keys())
                    if all(x in records for x in hostlist) is True:
                        if hostlist:
                            for each in hostlist:
                                if each in records:
                                    self.args['name'] = each
                                    real_args['name'] = each
                                    change = Helper().compare_data(self.table, real_args)
                                    if change is True:
                                        Helper().update_record(self.table, self.args, local)
                                    else:
                                        Message().show_error('Nothing is changed, Kindly change something to update')
                        else:
                            Message().error_exit(f'Node Hostlist is: {hostlist}')
                    else:
                        for each in hostlist:
                            if each  not in records:
                                Message().show_error(f'Node is not present in database: {each}')

                else:
                    Message().error_exit('Node are not available at this moment.')
            elif 'message' in record.content:
                Message().error_exit(record.content['message'])
            else:
                Message().error_exit('Node are not available at this moment.')
        else:
            Message().error_exit('Node are not available at this moment.')
        # return Helper().update_record(self.table, self.args)


    def rename_node(self):
        """
        Method to rename a node in Luna Configuration.
        """
        return Helper().rename_record(self.table, self.args, self.args["newnodename"])


    def remove_node(self):
        """
        Method to remove a node in Luna Configuration.
        """
        hostlist = Helper().get_hostlist(self.args['name'])
        hostlist = Helper().luna_hostlist(hostlist)
        record = Rest().get_data(self.table)
        if record.status_code == 200:
            if 'config' in record.content:
                if self.table in record.content['config']:
                    records = list(record.content['config'][self.table].keys())
                    if all(x in records for x in hostlist) is True:
                        if hostlist:
                            for each in hostlist:
                                if each in records:
                                    self.args['name'] = each
                                    Helper().delete_record(self.table, self.args)
                        else:
                            Message().error_exit(f'Node Hostlist is: {hostlist}')
                    else:
                        for each in hostlist:
                            if each  not in records:
                                Message().show_error(f'Node is not present in database: {each}')

                else:
                    Message().error_exit('Node are not available at this moment.')
            elif 'message' in record.content:
                Message().error_exit(record.content['message'])
            else:
                Message().error_exit('Node are not available at this moment.')
        else:
            Message().error_exit('Node are not available at this moment.')
        # return Helper().delete_record(self.table, self.args)


    def osgrab_node(self):
        """
        Method to grab an osimage to a node.
        """
        hostlist = Helper().get_hostlist(self.args['name'])
        hostlist = Helper().luna_hostlist(hostlist)
        record = Rest().get_data(self.table)
        if record.status_code == 200:
            if 'config' in record.content:
                if self.table in record.content['config']:
                    records = list(record.content['config'][self.table].keys())
                    if all(x in records for x in hostlist) is True:
                        if hostlist:
                            for each in hostlist:
                                if each in records:
                                    self.args['name'] = each
                                    Helper().grab_osimage(self.table, self.args)
                        else:
                            Message().error_exit(f'Node Hostlist is: {hostlist}')
                    else:
                        for each in hostlist:
                            if each  not in records:
                                Message().show_error(f'Node is not present in database: {each}')

                else:
                    Message().error_exit('Node are not available at this moment.')
            elif 'message' in record.content:
                Message().error_exit(record.content['message'])
            else:
                Message().error_exit('Node are not available at this moment.')
        else:
            Message().error_exit('Node are not available at this moment.')

        # return Helper().grab_osimage(self.table, self.args)


    def ospush_node(self):
        """
        Method to push an osimage to a node.
        """
        hostlist = Helper().get_hostlist(self.args['name'])
        hostlist = Helper().luna_hostlist(hostlist)
        record = Rest().get_data(self.table)
        if record.status_code == 200:
            if 'config' in record.content:
                if self.table in record.content['config']:
                    records = list(record.content['config'][self.table].keys())
                    if all(x in records for x in hostlist) is True:
                        if hostlist:
                            for each in hostlist:
                                if each in records:
                                    self.args['name'] = each
                                    Helper().push_osimage(self.table, self.args)
                        else:
                            Message().error_exit(f'Node Hostlist is: {hostlist}')
                    else:
                        for each in hostlist:
                            if each  not in records:
                                Message().show_error(f'Node is not present in database: {each}')

                else:
                    Message().error_exit('Node are not available at this moment.')
            elif 'message' in record.content:
                Message().error_exit(record.content['message'])
            else:
                Message().error_exit('Node are not available at this moment.')
        else:
            Message().error_exit('Node are not available at this moment.')
        # return Helper().push_osimage(self.table, self.args)


    def clone_node(self):
        """
        Method to rename a node in Luna Configuration.
        """
        hostlist = Helper().get_hostlist(self.args['newnodename'])
        hostlist = Helper().luna_hostlist(hostlist)
        if self.args['interface'] is None and (self.args['network'] or self.args['ipaddress'] or self.args['macaddress'] or self.args['options']):
            Message().error_exit("ERROR :: Kindly supply the interface in order to use the network, ipaddress, macaddress or options.")
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
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress'] or self.args['macaddress'] == '':
                interface['macaddress'] = self.args['macaddress']
            if self.args['options'] or self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['mtu'] or self.args['mtu'] == '':
                interface['mtu'] = self.args['mtu']
            if self.args['dhcp'] == '':
                interface['dhcp'] = self.args['dhcp']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options', 'mtu', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
            if len(hostlist) > 1 and ('ipaddress' in interface or 'macaddress' in interface):
                Message().error_exit('Interface IP Address or MAC Address can not be use with the hostlist, Kindly provide the single node or remove the IP Address and MAC Address.')
        record = Rest().get_data(self.table)
        if record.status_code == 200:
            if 'config' in record.content:
                if self.table in record.content['config']:
                    records = list(record.content['config'][self.table].keys())
                    if all(x in records for x in hostlist) is False:
                        if hostlist:
                            for each in hostlist:
                                if each not in records:
                                    self.args['newnodename'] = each
                                    Helper().clone_record(self.table, self.args)
                        else:
                            Message().error_exit(f'Node Hostlist is: {hostlist}')
                    else:
                        for each in hostlist:
                            if each in records:
                                Message().show_error(f'Node already present in database: {each}')

                else:
                    Message().error_exit('Node are not available at this moment.')
            elif 'message' in record.content:
                Message().error_exit(record.content['message'])
            else:
                Message().error_exit('Node are not available at this moment.')
        else:
            Message().error_exit('Node are not available at this moment.')
        # return Helper().clone_record(self.table, self.args)


    def listinterface(self):
        """
        Method to list a node interfaces in Luna Configuration.
        """
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
                Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = Helper().filter_interface(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table_cap} {self.args["name"]} Interfaces >>'
                Presenter().show_table(title, fields, rows)
        else:
            Message().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return True


    def showinterface(self):
        """
        Method to show a node interfaces in Luna Configuration.
        """
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
                Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = Helper().filter_data_col(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table_cap} {self.args["name"]} Interface [{self.args["interface"]}]'
                Presenter().show_table_col(title, fields, rows)
        else:
            msg = f'{self.args["interface"]} not found in {self.table} {self.args["name"]}'
            msg = f'{msg} OR {self.args["name"]} is unavailable.'
            Message().show_error(msg)
        return True


    def changeinterface(self):
        """
        Method to change a node interfaces in Luna Configuration.
        """
        real_args = deepcopy(self.args)
        # uri = self.table+'/'+self.args['name']+'/interfaces/'+self.args['interface']
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
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress'] or self.args['macaddress'] == '':
                interface['macaddress'] = self.args['macaddress']
            if self.args['options'] or self.args['options'] == '':
                interface['options'] = self.args['options']
            if self.args['mtu'] or self.args['mtu'] == '':
                interface['mtu'] = self.args['mtu']
            if self.args['dhcp']:
                interface['dhcp'] = self.args['dhcp']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options', 'mtu', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp']:
                self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.table, self.args)
        # payload = Helper().prepare_payload(uri, self.args)
        if payload:
            node_name = payload['name']
            del payload['name']
            request_data = {'config': {self.table: {node_name: payload}}}
            self.logger.debug(f'Payload => {request_data}')

            change = Helper().compare_data(self.table, real_args)
            if change is True:
                response = Rest().post_data(self.table, node_name+'/interfaces', request_data)
                self.logger.debug(f'Response => {response}')
                if response.status_code == 204:
                    Message().show_success(f'Node {node_name} Interface {interface["interface"]} is updated.')
                else:
                    Message().error_exit(response.content, response.status_code)
            else:
                Message().show_error('Nothing is changed, Kindly change something to update')

        else:
            Message().show_error('Nothing to update.')
        return True


    def removeinterface(self):
        """
        Method to remove a node interfaces in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            self.logger.debug(f'Payload => {payload}')
            uri = payload['name']+'/interfaces/'+payload['interface']
            response = Rest().get_delete(self.table, uri)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                msg = f'Node {payload["name"]} Interface {payload["interface"]} is removed.'
                Message().show_success(msg)
            else:
                Message().error_exit(response.content, response.status_code)
        return True
