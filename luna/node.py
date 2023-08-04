#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Node Class for the CLI
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
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import actions
from luna.utils.message import Message
from luna.utils.arguments import Arguments


class Node():
    """
    Node Class responsible to show, list,
    add, remove information for the Node
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
        Method will provide all the arguments
        related to the Node class.
        """
        node_menu = subparsers.add_parser('node', help='Compute Node operations.')
        node_args = node_menu.add_subparsers(dest='action')
        node_list = node_args.add_parser('list', help='List All Nodes')
        Arguments().common_list_args(node_list)
        node_show = node_args.add_parser('show', help='Show A Node')
        node_show.add_argument('name', help='Name of the Node')
        Arguments().common_list_args(node_show)
        node_add = node_args.add_parser('add', help='Add A Node')
        Arguments().common_node_args(node_add, True)
        node_change = node_args.add_parser('change', help='Make Changes Into a Node')
        Arguments().common_node_args(node_change)
        node_clone = node_args.add_parser('clone', help='Clone A Node')
        Arguments().common_node_args(node_clone)
        node_clone.add_argument('newnodename', help='New Name for the Node')
        node_rename = node_args.add_parser('rename', help='Rename A Node')
        node_rename.add_argument('name', help='Name of the Node')
        node_rename.add_argument('newnodename', help='New Name for the Node')
        node_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_remove = node_args.add_parser('remove', help='Remove A Node')
        node_remove.add_argument('name', help='Name of the Node')
        node_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_osgrab = node_args.add_parser('osgrab', help='Gran an OS Image for a Node')
        node_osgrab.add_argument('name', help='Name of the Node')
        node_osgrab.add_argument('-o', '--osimage', help='OS Image Name')
        node_osgrab.add_argument('-b', '--bare', action='store_true', help='Bare OS Image')
        node_osgrab.add_argument('-no', '--nodry', action='store_true', help='No Dry flag to avoid dry run')
        node_osgrab.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_ospush = node_args.add_parser('ospush', help='Push an OS Image for a Node')
        node_ospush.add_argument('name', help='Name of the Node')
        node_ospush.add_argument('-o', '--osimage', help='OS Image Name')
        node_ospush.add_argument('-no', '--nodry', action='store_true', help='No Dry flag to avoid dry run')
        node_ospush.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_interfaces = node_args.add_parser('listinterface', help='List Node Interfaces')
        node_interfaces.add_argument('name', help='Name of the Node')
        Arguments().common_list_args(node_interfaces)
        node_interface = node_args.add_parser('showinterface', help='Show Node Interface')
        node_interface.add_argument('name', help='Name of the Node')
        node_interface.add_argument('interface', help='Name of the Node Interface')
        Arguments().common_list_args(node_interface)
        change_interface = node_args.add_parser('changeinterface', help='Change Node Interface')
        change_interface.add_argument('name', help='Name of the Node')
        change_interface.add_argument('interface', help='Name of the Node Interface')
        change_interface.add_argument('-N', '--network', help='Network Name')
        change_interface.add_argument('-I', '--ipaddress', help='IP Address')
        change_interface.add_argument('-M', '--macaddress', help='MAC Address')
        change_interface.add_argument('-O', '--options', action='store_true',
                                      help='Interfaces Options')
        change_interface.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        change_interface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        remove_interface = node_args.add_parser('removeinterface', help='Remove Node Interface')
        remove_interface.add_argument('name', help='Name of the Node')
        remove_interface.add_argument('interface', help='Name of the Node Interface')
        remove_interface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_node(self):
        """
        Method to list all nodes from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_node(self):
        """
        Method to show a node in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_node(self):
        """
        Method to add new node in Luna Configuration.
        """
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress']:
                interface['macaddress'] = self.args['macaddress']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options']:
                self.args.pop(remove, None)
        return Helper().add_record(self.table, self.args)


    def change_node(self):
        """
        Method to change a node in Luna Configuration.
        """
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress']:
                interface['macaddress'] = self.args['macaddress']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options']:
                self.args.pop(remove, None)
        return Helper().update_record(self.table, self.args)


    def rename_node(self):
        """
        Method to rename a node in Luna Configuration.
        """
        return Helper().rename_record(self.table, self.args, self.args["newnodename"])


    def remove_node(self):
        """
        Method to remove a node in Luna Configuration.
        """
        return Helper().delete_record(self.table, self.args)


    def osgrab_node(self):
        """
        Method to grab an osimage to a node.
        """
        return Helper().grab_osimage(self.table, self.args)


    def ospush_node(self):
        """
        Method to push an osimage to a node.
        """
        return Helper().push_osimage(self.table, self.args)


    def clone_node(self):
        """
        Method to rename a node in Luna Configuration.
        """
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress']:
                interface['macaddress'] = self.args['macaddress']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options']:
                self.args.pop(remove, None)
        return Helper().clone_record(self.table, self.args, self.args["newnodename"])


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
        uri = self.table+'/'+self.args['name']+'/interfaces'
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['ipaddress']:
                interface['ipaddress'] = self.args['ipaddress']
            if self.args['macaddress']:
                interface['macaddress'] = self.args['macaddress']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'ipaddress', 'macaddress', 'options']:
                self.args.pop(remove, None)
        payload = Helper().prepare_payload(uri, self.args)
        if payload:
            node_name = payload['name']
            del payload['name']
            request_data = {'config': {self.table: {node_name: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, node_name+'/interfaces', request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Message().show_success(f'Interfaces updated in {self.table_cap} {node_name}.')
            else:
                Message().error_exit(response.content, response.status_code)
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
                msg = f'{payload["interface"]} Deleted from {self.table_cap} {payload["name"]}.'
                Message().show_success(msg)
            else:
                Message().error_exit(response.content, response.status_code)
        return True
