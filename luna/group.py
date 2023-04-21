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
__status__      = "Development"

import sys
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
        self.table_cap = self.table.capitalize()
        self.interface = "groupinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "member", "add", "change", "rename", "remove", "clone",
                       "listinterface", "showinterface", "changeinterface", "removeinterface"]
            if self.args["action"] in actions:
                if 'interface' in self.args["action"]:
                    call = methodcaller(f'{self.args["action"]}')
                else:
                    call = methodcaller(f'{self.args["action"]}_group')
                call(self)
            else:
                Helper().show_error(f"Kindly choose from {actions}.")
        else:
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
        group_member = group_args.add_parser('member', help='Group Used by Nodes')
        group_member.add_argument('name', help='Name of the Group')
        Helper().common_list_args(group_member)
        group_add = group_args.add_parser('add', help='Add Group')
        group_add.add_argument('name', help='Name of the Group')
        group_add.add_argument('-b', '--setupbmc', choices=Helper().boolean(),
                               metavar="{y,yes,n,no,''}", help='BMC Setup')
        group_add.add_argument('-o', '--osimage', help='OS Image Name')
        group_add.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_add.add_argument('-D', '--domain', help='Domain Name')
        group_add.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        group_add.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        group_add.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        group_add.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        group_add.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        group_add.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        group_add.add_argument('-pi', '--provision_interface', help='Provision Interface')
        group_add.add_argument('-pm', '--provision_method', help='Provision Method')
        group_add.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        group_add.add_argument('-nb', '--netboot', choices=Helper().boolean(),
                               metavar="{y,yes,n,no,''}", help='Network Boot')
        group_add.add_argument('-li', '--localinstall', choices=Helper().boolean(),
                               metavar="{y,yes,n,no,''}", help='Local Install')
        group_add.add_argument('-bm', '--bootmenu', choices=Helper().boolean(),
                               metavar="{y,yes,n,no,''}", help='Boot Menu')
        group_add.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        group_add.add_argument('-if', '--interface', help='Interface Name')
        group_add.add_argument('-N', '--network', help='Interface Network Name')
        group_add.add_argument('-O', '--options', action='store_true', help='Interfaces Options')
        group_add.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        group_add.add_argument('-c', '--comment', action='store_true', help='Comment')
        group_add.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        group_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_change = group_args.add_parser('change', help='Change Group')
        group_change.add_argument('name', help='Name of the Group')
        group_change.add_argument('-b', '--setupbmc', choices=Helper().boolean(),
                                  metavar="{y,yes,n,no,''}", help='BMC Setup')
        group_change.add_argument('-o', '--osimage', help='OS Image Name')
        group_change.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_change.add_argument('-D', '--domain', help='Domain Name')
        group_change.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        group_change.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        group_change.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        group_change.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        group_change.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        group_change.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        group_change.add_argument('-pi', '--provision_interface', help='Provision Interface')
        group_change.add_argument('-pm', '--provision_method', help='Provision Method')
        group_change.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        group_change.add_argument('-nb', '--netboot', choices=Helper().boolean(),
                                  metavar="{y,yes,n,no,''}", help='Network Boot')
        group_change.add_argument('-li', '--localinstall', choices=Helper().boolean(),
                                  metavar="{y,yes,n,no,''}", help='Local Install')
        group_change.add_argument('-bm', '--bootmenu', choices=Helper().boolean(),
                                  metavar="{y,yes,n,no,''}", help='Boot Menu')
        group_change.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        group_change.add_argument('-if', '--interface', help='Interface Name')
        group_change.add_argument('-N', '--network', help='Interface Network Name')
        group_change.add_argument('-O', '--options', action='store_true', help='Interfaces Options')
        group_change.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        group_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        group_change.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        group_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_clone = group_args.add_parser('clone', help='Clone Group.')
        group_clone.add_argument('name', help='Name of the Group')
        group_clone.add_argument('newgroupname', help='New Name for the Group')
        group_clone.add_argument('-b', '--setupbmc', choices=Helper().boolean(),
                                 metavar="{y,yes,n,no,''}", help='BMC Setup')
        group_clone.add_argument('-o', '--osimage', help='OS Image Name')
        group_clone.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_clone.add_argument('-D', '--domain', help='Domain Name')
        group_clone.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        group_clone.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        group_clone.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        group_clone.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        group_clone.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        group_clone.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        group_clone.add_argument('-pi', '--provision_interface', help='Provision Interface')
        group_clone.add_argument('-pm', '--provision_method', help='Provision Method')
        group_clone.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        group_clone.add_argument('-nb', '--netboot', help='Network Boot')
        group_clone.add_argument('-li', '--localinstall', help='Local Install')
        group_clone.add_argument('-bm', '--bootmenu', help='Boot Menu')
        group_clone.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        group_clone.add_argument('-if', '--interface', help='Interface Name')
        group_clone.add_argument('-N', '--network', help='Interface Network Name')
        group_clone.add_argument('-O', '--options', action='store_true', help='Interfaces Options')
        group_clone.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        group_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        group_clone.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        group_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_rename = group_args.add_parser('rename', help='Rename Group.')
        group_rename.add_argument('name', help='Name of the Group')
        group_rename.add_argument('newgroupname', help='New Name for the Group')
        group_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_remove = group_args.add_parser('remove', help='Remove Group')
        group_remove.add_argument('name', help='Name of the Group')
        group_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        group_interfaces = group_args.add_parser('listinterface', help='List Group Interfaces')
        group_interfaces.add_argument('name', help='Name of the Group')
        Helper().common_list_args(group_interfaces)
        group_interface = group_args.add_parser('showinterface', help='Show Group Interface')
        group_interface.add_argument('name', help='Name of the Group')
        group_interface.add_argument('interface', help='Name of the Group Interface')
        Helper().common_list_args(group_interface)
        change_interface = group_args.add_parser('changeinterface', help='Change Group Interface')
        change_interface.add_argument('name', help='Name of the Group')
        change_interface.add_argument('interface', help='Group Interface Name')
        change_interface.add_argument('-N', '--network', help='Network Name')
        change_interface.add_argument('-O', '--options', action='store_true',
                                      help='Interfaces Options')
        change_interface.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        change_interface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        remove_interface = group_args.add_parser('removeinterface', help='Remove Group Interface')
        remove_interface.add_argument('name', help='Name of the Group')
        remove_interface.add_argument('interface', help='Name of the Group Interface')
        remove_interface.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_group(self):
        """
        Method to list all groups from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


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
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options']:
                self.args.pop(remove, None)
        return Helper().add_record(self.table, self.args)


    def change_group(self):
        """
        Method to change a group in Luna Configuration.
        """
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options']:
                self.args.pop(remove, None)
        return Helper().update_record(self.table, self.args)


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


    def clone_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        interface = {}
        if self.args['interface']:
            interface['interface'] = self.args['interface']
            if self.args['network']:
                interface['network'] = self.args['network']
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options']:
                self.args.pop(remove, None)
        return Helper().clone_record(self.table, self.args, self.args["newgroupname"])


    def listinterface(self):
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
                data = Helper().prepare_json(data, True)
                fields, rows  = Helper().filter_interface(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table_cap} {self.args["name"]} Interfaces >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Helper().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return response


    def showinterface(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        response = False
        uri = self.args['name']+'/interfaces/'+self.args['interface']
        self.logger.debug(f'Table => {self.table} and URI => {uri}')
        get_list = Rest().get_data(self.table, uri)
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
            response = Helper().show_error(msg)
        return response


    def changeinterface(self):
        """
        Method to change a Group interfaces in Luna Configuration.
        """
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
            if self.args['options']:
                interface['options'] = self.args['options']
            elif self.args['options'] == '':
                interface['options'] = self.args['options']
        if interface:
            self.args['interfaces'] = [interface]
            for remove in ['interface', 'network', 'options']:
                self.args.pop(remove, None)
        payload = Helper().prepare_payload(uri, self.args)
        if payload:
            del payload['name']
            request_data = {'config': {self.table: {group_name: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, group_name+'/interfaces', request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'Interfaces updated in {self.table_cap} {group_name}.')
            else:
                sys.stderr.write(f'HTTP Error Code {response.status_code}.\n')
                sys.stderr.write(f'HTTP Error {response.content}.\n')
                sys.exit(1)
        else:
            Helper().show_error('Nothing to update.')
        return response


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
                msg = f'{payload["interface"]} removed from {self.table_cap} {payload["name"]}.'
                Helper().show_success(msg)
            else:
                sys.stderr.write(f'HTTP Error Code {response.status_code}.\n')
                sys.stderr.write(f'HTTP Error {response.content}.\n')
                sys.exit(1)
        return response
