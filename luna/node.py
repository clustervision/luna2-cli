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
__status__      = "Production"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log

class Node():
    """
    Node Class responsible to show, list,
    add, remove information for the Node
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "node"
        self.interface = "nodeinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in ["list", "show", "add", "change", "rename", "remove", "clone"]:
                call = methodcaller(f'{self.args["action"]}_node')
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
        related to the Node class.
        """
        node_menu = subparsers.add_parser('node', help='Node operations.')
        node_args = node_menu.add_subparsers(dest='action')
        ## >>>>>>> Node Command >>>>>>> list
        node_list = node_args.add_parser('list', help='List Node')
        Helper().common_list_args(node_list)
        node_show = node_args.add_parser('show', help='Show Node')
        node_show.add_argument('name', help='Name of the Node')
        Helper().common_list_args(node_show)
        node_add = node_args.add_parser('add', help='Add Node')
        node_add.add_argument('name', help='Name of the Node')
        node_add.add_argument('-host', '--hostname',help='Hostname')
        node_add.add_argument('-g', '--group', required=True, help='Group Name')
        node_add.add_argument('-o', '--osimage', help='OS Image Name')
        node_add.add_argument('-b', '--setupbmc', help='BMC Setup')
        node_add.add_argument('-bmc', '--bmcsetup', help='BMC Setup')
        node_add.add_argument('-sw', '--switch', help='Switch Name')
        node_add.add_argument('-sp', '--switchport', help='Switch Port')
        node_add.add_argument('-pre', '--prescript', help='Pre Script')
        node_add.add_argument('-part', '--partscript', help='Part Script')
        node_add.add_argument('-post', '--postscript', help='Post Script')
        node_add.add_argument('-pi', '--provision_interface', help='Provision Interface')
        node_add.add_argument('-pm', '--provision_method', help='Provision Method')
        node_add.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        node_add.add_argument('-nb', '--netboot', help='Network Boot')
        node_add.add_argument('-li', '--localinstall', help='Local Install')
        node_add.add_argument('-bm', '--bootmenu', help='Boot Menu')
        node_add.add_argument('-lb', '--localboot', help='Local Boot')
        node_add.add_argument('-ser', '--service', help='Service')
        node_add.add_argument('-s', '--status', help='Status')
        node_add.add_argument('-tid', '--tpm_uuid', help='TPM UUID')
        node_add.add_argument('-tkey', '--tpm_pubkey', help='TPM Public Key')
        node_add.add_argument('-tsha', '--tpm_sha256', help='TPM SHA256')
        node_add.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        node_add.add_argument('-c', '--comment', help='Comment')
        node_add.add_argument('-if', '--interface', action='append', help='Interface Name')
        node_add.add_argument('-N', '--network', action='append', help='Interface Network Name')
        node_add.add_argument('-I', '--ipaddress', action='append', help='Interfaces IP Address')
        node_add.add_argument('-M', '--macaddress', action='append', help='Interfaces MAC Address')
        node_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_change = node_args.add_parser('change', help='Change Node')
        node_change.add_argument('name', help='Name of the Node')
        node_change.add_argument('-host', '--hostname',help='Hostname')
        node_change.add_argument('-g', '--group', help='Group Name')
        node_change.add_argument('-o', '--osimage', help='OS Image Name')
        node_change.add_argument('-b', '--setupbmc', help='BMC Setup')
        node_change.add_argument('-bmc', '--bmcsetup', help='BMC Setup')
        node_change.add_argument('-sw', '--switch', help='Switch Name')
        node_change.add_argument('-sp', '--switchport', help='Switch Port')
        node_change.add_argument('-pre', '--prescript', help='Pre Script')
        node_change.add_argument('-part', '--partscript', help='Part Script')
        node_change.add_argument('-post', '--postscript', help='Post Script')
        node_change.add_argument('-pi', '--provision_interface', help='Provision Interface')
        node_change.add_argument('-pm', '--provision_method', help='Provision Method')
        node_change.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        node_change.add_argument('-nb', '--netboot', help='Network Boot')
        node_change.add_argument('-li', '--localinstall', help='Local Install')
        node_change.add_argument('-bm', '--bootmenu', help='Boot Menu')
        node_change.add_argument('-lb', '--localboot', help='Local Boot')
        node_change.add_argument('-ser', '--service', help='Service')
        node_change.add_argument('-s', '--status', help='Status')
        node_change.add_argument('-tid', '--tpm_uuid', help='TPM UUID')
        node_change.add_argument('-tkey', '--tpm_pubkey', help='TPM Public Key')
        node_change.add_argument('-tsha', '--tpm_sha256', help='TPM SHA256')
        node_change.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        node_change.add_argument('-c', '--comment', help='Comment')
        node_change.add_argument('-if', '--interface', action='append', help='Interface Name')
        node_change.add_argument('-N', '--network', action='append', help='Interface Network Name')
        node_change.add_argument('-I', '--ipaddress', action='append', help='Interfaces IP Address')
        node_change.add_argument('-M', '--macaddress', action='append', help='Interfaces MAC Address')
        node_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        ## >>>>>>> Node Command >>>>>>> clone
        node_clone = node_args.add_parser('clone', help='Clone Node')
        node_clone.add_argument('name', help='Name of the Node')
        node_clone.add_argument('newnodename', help='New Name for the Node')
        node_clone.add_argument('-host', '--hostname',help='Hostname')
        node_clone.add_argument('-g', '--group', help='Group Name')
        node_clone.add_argument('-o', '--osimage', help='OS Image Name')
        node_clone.add_argument('-b', '--setupbmc', help='BMC Setup')
        node_clone.add_argument('-bmc', '--bmcsetup', help='BMC Setup')
        node_clone.add_argument('-sw', '--switch', help='Switch Name')
        node_clone.add_argument('-sp', '--switchport', help='Switch Port')
        node_clone.add_argument('-pre', '--prescript', help='Pre Script')
        node_clone.add_argument('-part', '--partscript', help='Part Script')
        node_clone.add_argument('-post', '--postscript', help='Post Script')
        node_clone.add_argument('-pi', '--provision_interface', help='Provision Interface')
        node_clone.add_argument('-pm', '--provision_method', help='Provision Method')
        node_clone.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        node_clone.add_argument('-nb', '--netboot', help='Network Boot')
        node_clone.add_argument('-li', '--localinstall', help='Local Install')
        node_clone.add_argument('-bm', '--bootmenu', help='Boot Menu')
        node_clone.add_argument('-lb', '--localboot', help='Local Boot')
        node_clone.add_argument('-ser', '--service', help='Service')
        node_clone.add_argument('-s', '--status', help='Status')
        node_clone.add_argument('-tid', '--tpm_uuid', help='TPM UUID')
        node_clone.add_argument('-tkey', '--tpm_pubkey', help='TPM Public Key')
        node_clone.add_argument('-tsha', '--tpm_sha256', help='TPM SHA256')
        node_clone.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        node_clone.add_argument('-c', '--comment', help='Comment')
        node_clone.add_argument('-if', '--interface', action='append', help='Interface Name')
        node_clone.add_argument('-N', '--network', action='append', help='Interface Network Name')
        node_clone.add_argument('-I', '--ipaddress', action='append', help='Interfaces IP Address')
        node_clone.add_argument('-M', '--macaddress', action='append', help='Interfaces MAC Address')
        node_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_rename = node_args.add_parser('rename', help='Rename Node')
        node_rename.add_argument('name', help='Name of the Node')
        node_rename.add_argument('newnodename', help='New Name for the Node')
        node_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_remove = node_args.add_parser('remove', help='Remove Node')
        node_remove.add_argument('name', help='Name of the Node')
        node_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_interfaces = node_args.add_parser('interfaces', help='List Node Interfaces')
        node_interfaces.add_argument('name', help='Name of the Node')
        Helper().common_list_args(node_interfaces)
        node_interface = node_args.add_parser('interface', help='Show Node Interface')
        node_interface.add_argument('name', help='Name of the Node')
        node_interface.add_argument('interface', help='Name of the Node Interface')
        Helper().common_list_args(node_interface)
        node_changeinterface = node_args.add_parser('changeinterface', help='Change Node Interface')
        node_changeinterface.add_argument('name', help='Name of the Node')
        node_changeinterface.add_argument('interface', help='Name of the Node Interface')
        node_changeinterface.add_argument('network', action='append', help='Network Name')
        node_changeinterface.add_argument('ipaddress', action='append', help='IP Address')
        node_changeinterface.add_argument('macaddress', action='append', help='MAC Address')
        node_changeinterface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        node_removeinterface = node_args.add_parser('removeinterface', help='Remove Node Interface')
        node_removeinterface.add_argument('name', help='Name of the Node')
        node_removeinterface.add_argument('interface', help='Name of the Node Interface')
        node_removeinterface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
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
        error = False
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        iface = [self.args['interface'], self.args['network'], self.args['ipaddress'], self.args['macaddress']]
        ifacecount = sum(x is not None for x in iface)
        if ifacecount:
            if ifacecount == 4:
                if len(self.args['interface']) == len(self.args['network']) == len(self.args['ipaddress']) == len(self.args['macaddress']):
                    interface_data = {'interface': self.args['interface'], 'network': self.args['network'], 'ipaddress': self.args['ipaddress'], 'macaddress': self.args['macaddress']}
                    self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name, Network Name, IP Address, and MAC Address.')
            else:
                error = Helper().show_warning('Each Interface should have Interface Name, Network Name, IP Address, and MAC Address.')
        for remove in ['interface', 'network', 'ipaddress', 'macaddress']:
            self.args.pop(remove, None)
        if error:
            Helper().show_error('Operation Aborted.')
            self.args.clear()
        payload = {k: v for k, v in self.args.items() if v is not None}
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


    def change_node(self):
        """
        Method to chagne a node in Luna Configuration.
        """
        error = False
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        iface = [self.args['interface'], self.args['network'], self.args['ipaddress'], self.args['macaddress']]
        ifacecount = sum(x is not None for x in iface)
        if ifacecount:
            if ifacecount == 4:
                if len(self.args['interface']) == len(self.args['network']) == len(self.args['ipaddress']) == len(self.args['macaddress']):
                    interface_data = {'interface': self.args['interface'], 'network': self.args['network'], 'ipaddress': self.args['ipaddress'], 'macaddress': self.args['macaddress']}
                    self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name, Network Name, IP Address, and MAC Address.')
            else:
                error = Helper().show_warning('Each Interface should have Interface Name, Network Name, IP Address, and MAC Address.')
        for remove in ['interface', 'network', 'ipaddress', 'macaddress']:
            self.args.pop(remove, None)
        if error:
            Helper().show_error('Operation Aborted.')
            self.args.clear()
        payload = {k: v for k, v in self.args.items() if v is not None}
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


    def rename_node(self):
        """
        Method to rename a node in Luna Configuration.
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
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newnodename"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def remove_node(self):
        """
        Method to remove a node in Luna Configuration.
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


    def clone_node(self):
        """
        Method to rename a node in Luna Configuration.
        """
        
        error = False
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        iface = [self.args['interface'], self.args['network'], self.args['ipaddress'], self.args['macaddress']]
        ifacecount = sum(x is not None for x in iface)
        if ifacecount:
            if ifacecount == 4:
                if len(self.args['interface']) == len(self.args['network']) == len(self.args['ipaddress']) == len(self.args['macaddress']):
                    interface_data = {'interface': self.args['interface'], 'network': self.args['network'], 'ipaddress': self.args['ipaddress'], 'macaddress': self.args['macaddress']}
                    self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name, Network Name, IP Address, and MAC Address.')
            else:
                error = Helper().show_warning('Each Interface should have Interface Name, Network Name, IP Address, and MAC Address.')
        for remove in ['interface', 'network', 'ipaddress', 'macaddress']:
            self.args.pop(remove, None)
        if error:
            Helper().show_error('Operation Aborted.')
            self.args.clear()
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_clone(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newnodename"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def list_interfaces(self):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces')
        get_list = Rest().get_data(self.table, self.args['name']+'/interfaces')
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces']
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_interface(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table.capitalize()} {self.args["name"]} Interfaces >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Helper().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return True


    def show_interface(self):
        """
        Method to show a node interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces{self.args["interface"]}')
        get_list = Rest().get_data(self.table, self.args['name']+'/interfaces/'+self.args['interface'])
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces'][0]
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table.capitalize()} [{self.args["name"]}] => Interface {self.args["interface"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'Interface {self.args["interface"]} not found in {self.table} {self.args["name"]} OR {self.args["name"]} is unavailable.')
        return True


    def change_interface(self):
        """
        Method to change a node interfaces in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        self.args['interfaces'] = {'interface': self.args['interface'], 'network': self.args['network'], 'ipaddress': self.args['ipaddress'], 'macaddress': self.args['macaddress']}
        for remove in ['interface', 'network', 'ipaddress', 'macaddress']:
            self.args.pop(remove, None)
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            node_name = payload['name']
            del payload['name']
            request_data = {'config': {self.table: {node_name: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, node_name+'/interfaces', request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'Interfaces updated in {self.table.capitalize()} {payload["name"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response}.')
        else:
            Helper().show_error('Nothing to update.')
        return True


    def remove_interface(self):
        """
        Method to remove a node interfaces in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload is False:
            self.logger.debug(f'Payload => {payload}')
            response = Rest().get_delete(self.table, payload['name']+'/interfaces/'+payload['interface'])
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'Interface {payload["interface"]} Deleted from {self.table.capitalize()} {payload["name"]}.')
            else:
                Helper().show_error(f'HTTP Error Code: {response}.')
        return True
