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
Switch Class for the CLI
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
from luna.utils.log import Log
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.constant import actions, BOOL_CHOICES, BOOL_META
from luna.utils.message import Message

class Switch():
    """
    Switch Class responsible to show, list, add, change,
    remove, rename and clone information for the Switch.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "switch"
        self.table_cap = self.table.capitalize()
        self.interface = "switchinterface"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_switch')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Switch class.
        """
        switch_menu = Helper().get_help_message(subparsers, self.table)
        switch_args = switch_menu.add_subparsers(dest='action', title='commands', description='Available switch operations')
        switch_list = switch_args.add_parser('list', help='List Switch')
        Helper().common_list_args(switch_list, True)
        switch_show = switch_args.add_parser('show', help='Show Switch')
        switch_show.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        Helper().common_list_args(switch_show)
        switch_add = switch_args.add_parser('add', help='Add Switch')
        switch_add.add_argument('name', help='Switch Name')
        switch_add.add_argument('--vendor', help='Add Switch Vendor Name')
        switch_add.add_argument('-ot', '--ostype', choices=['nvos', 'cumulus', 'generic', ''],
                                metavar="{nvos,cumulus,generic}",
                                help='Switch OS type; gates ZTP options (cumulus adds option 239)')
        switch_add.add_argument('-N', '--network', help='Network').completer = Helper().name_completer("network")
        switch_add.add_argument('-I', '--ipaddress', help='IP Address')
        switch_add.add_argument('-M', '--macaddress', help='MAC Address')
        switch_add.add_argument('-r', '--read', help='Read community')
        switch_add.add_argument('-w', '--rw', help='Write community')
        switch_add.add_argument('-o', '--oid', help='OID')
        switch_add.add_argument('-u', '--uplinkports', help='Write community')
        # TRIX-1908: switch zero-touch provisioning (ZTP) fields
        switch_add.add_argument('-nb', '--netboot', choices=BOOL_CHOICES, metavar=BOOL_META,
                                help='Toggle ZTP netboot DHCP options for the switch')
        switch_add.add_argument('-du', '--default-url',
                                help='ZTP boot image path, controller-relative (e.g. files/<image>.bin)')
        switch_add.add_argument('-bf', '--bootfile',
                                help='ZTP recipe path, controller-relative (e.g. boot/switch/<name>)')
        switch_add.add_argument('-zc', '--ztpconfig', action='store_true',
                                help='Config served by ZTP (opens an editor)')
        switch_add.add_argument('-qz', '--quick-ztpconfig', dest='ztpconfig',
                                metavar="File-Path OR In-Line", help='ZTP config File-Path OR In-Line')
        switch_add.add_argument('-zf', '--ztpformat', choices=['commands', 'yaml'],
                                help='ZTP config format served by the recipe')
        switch_add.add_argument('-up', '--url_protocol', choices=['secure', 'plain', ''],
                                metavar="{secure,plain}",
                                help='ZTP URL scheme: secure (API/https) or plain (webserver/http); default auto')
        switch_add.add_argument('-us', '--url_server',
                                help='ZTP URL host override (IP or hostname); default the known controller')
        switch_add.add_argument('-te', '--tftp_enable', choices=BOOL_CHOICES, metavar=BOOL_META,
                                help='Enable TFTP (option 66) for the switch, e.g. ONIE/TFTP install; default off')
        switch_add.add_argument('--nonetwork', action='store_true', default=None, help='No network verification')
        switch_add.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_add.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_add.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_change = switch_args.add_parser('change', help='Change Switch')
        switch_change.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_change.add_argument('--vendor', help='Change Switch Vendor Name')
        switch_change.add_argument('-ot', '--ostype', choices=['nvos', 'cumulus', 'generic', ''],
                                   metavar="{nvos,cumulus,generic}",
                                   help='Switch OS type; gates ZTP options (cumulus adds option 239)')
        switch_change.add_argument('-N', '--network', help='Network').completer = Helper().name_completer("network")
        switch_change.add_argument('-I', '--ipaddress', help='IP Address')
        switch_change.add_argument('-M', '--macaddress', help='MAC Address')
        switch_change.add_argument('-r', '--read', help='Read community')
        switch_change.add_argument('-w', '--rw', help='Write community')
        switch_change.add_argument('-o', '--oid', help='OID')
        switch_change.add_argument('-u', '--uplinkports', help='Write community')
        # TRIX-1908: switch zero-touch provisioning (ZTP) fields
        switch_change.add_argument('-nb', '--netboot', choices=BOOL_CHOICES, metavar=BOOL_META,
                                   help='Toggle ZTP netboot DHCP options for the switch')
        switch_change.add_argument('-du', '--default-url',
                                   help='ZTP boot image path, controller-relative (e.g. files/<image>.bin)')
        switch_change.add_argument('-bf', '--bootfile',
                                   help='ZTP recipe path, controller-relative (e.g. boot/switch/<name>)')
        switch_change.add_argument('-zc', '--ztpconfig', action='store_true',
                                   help='Config served by ZTP (opens an editor)')
        switch_change.add_argument('-qz', '--quick-ztpconfig', dest='ztpconfig',
                                   metavar="File-Path OR In-Line", help='ZTP config File-Path OR In-Line')
        switch_change.add_argument('-zf', '--ztpformat', choices=['commands', 'yaml'],
                                   help='ZTP config format served by the recipe')
        switch_change.add_argument('-up', '--url_protocol', choices=['secure', 'plain', ''],
                                   metavar="{secure,plain}",
                                   help='ZTP URL scheme: secure (API/https) or plain (webserver/http); default auto')
        switch_change.add_argument('-us', '--url_server',
                                   help='ZTP URL host override (IP or hostname); default the known controller')
        switch_change.add_argument('-te', '--tftp_enable', choices=BOOL_CHOICES, metavar=BOOL_META,
                                   help='Enable TFTP (option 66) for the switch, e.g. ONIE/TFTP install; default off')
        switch_change.add_argument('--nonetwork', action='store_true', default=None, help='No network verification')
        switch_change.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_change.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_clone = switch_args.add_parser('clone', help='Clone Switch')
        switch_clone.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_clone.add_argument('newswitchname', help='New Switch Name')
        switch_clone.add_argument('--vendor', help='Clone Switch Vendor Name')
        switch_clone.add_argument('-ot', '--ostype', choices=['nvos', 'cumulus', 'generic', ''],
                                  metavar="{nvos,cumulus,generic}",
                                  help='Switch OS type; gates ZTP options (cumulus adds option 239)')
        switch_clone.add_argument('-N', '--network', help='Network').completer = Helper().name_completer("network")
        switch_clone.add_argument('-I', '--ipaddress', help='IP Address')
        switch_clone.add_argument('-M', '--macaddress', help='MAC Address')
        switch_clone.add_argument('-r', '--read', help='Read community')
        switch_clone.add_argument('-w', '--rw', help='Write community')
        switch_clone.add_argument('-o', '--oid', help='OID')
        switch_clone.add_argument('-u', '--uplinkports', help='Write community')
        # TRIX-1908: switch zero-touch provisioning (ZTP) fields
        switch_clone.add_argument('-nb', '--netboot', choices=BOOL_CHOICES, metavar=BOOL_META,
                                  help='Toggle ZTP netboot DHCP options for the switch')
        switch_clone.add_argument('-du', '--default-url',
                                  help='ZTP boot image path, controller-relative (e.g. files/<image>.bin)')
        switch_clone.add_argument('-bf', '--bootfile',
                                  help='ZTP recipe path, controller-relative (e.g. boot/switch/<name>)')
        switch_clone.add_argument('-zc', '--ztpconfig', action='store_true',
                                  help='Config served by ZTP (opens an editor)')
        switch_clone.add_argument('-qz', '--quick-ztpconfig', dest='ztpconfig',
                                  metavar="File-Path OR In-Line", help='ZTP config File-Path OR In-Line')
        switch_clone.add_argument('-zf', '--ztpformat', choices=['commands', 'yaml'],
                                  help='ZTP config format served by the recipe')
        switch_clone.add_argument('-up', '--url_protocol', choices=['secure', 'plain', ''],
                                  metavar="{secure,plain}",
                                  help='ZTP URL scheme: secure (API/https) or plain (webserver/http); default auto')
        switch_clone.add_argument('-us', '--url_server',
                                  help='ZTP URL host override (IP or hostname); default the known controller')
        switch_clone.add_argument('-te', '--tftp_enable', choices=BOOL_CHOICES, metavar=BOOL_META,
                                  help='Enable TFTP (option 66) for the switch, e.g. ONIE/TFTP install; default off')
        switch_clone.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_clone.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_rename = switch_args.add_parser('rename', help='Rename Switch')
        switch_rename.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_rename.add_argument('newswitchname', help='New Switch Name')
        switch_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_remove = switch_args.add_parser('remove', help='Remove Switch')
        switch_remove.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        # TRIX-1880: switch interfaces (lighter than node interfaces: name + mac + ip + network)
        switch_listif = switch_args.add_parser('listinterface', help='List Switch Interfaces')
        switch_listif.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_listif.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        switch_showif = switch_args.add_parser('showinterface', help="Show a Switch Interface")
        switch_showif.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_showif.add_argument('interface', help='Interface Name')
        switch_showif.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        switch_changeif = switch_args.add_parser('changeinterface', help='Add or change a Switch Interface')
        switch_changeif.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_changeif.add_argument('interface', help='Interface Name (e.g. eth0, swp1)')
        switch_changeif.add_argument('-N', '--network', help='Network Name').completer = Helper().name_completer("network")
        switch_changeif.add_argument('-I', '--ipaddress', help='IP Address')
        switch_changeif.add_argument('-M', '--macaddress', help='MAC Address')
        switch_changeif.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_removeif = switch_args.add_parser('removeinterface', help='Remove a Switch Interface')
        switch_removeif.add_argument('name', help='Switch Name').completer = Helper().name_completer(self.table)
        switch_removeif.add_argument('interface', help='Interface Name')
        switch_removeif.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_switch(self):
        """
        This method list all switches.
        """
        return Helper().get_list(self.table, self.args)


    def show_switch(self):
        """
        This method show a specific switch.
        """
        return Helper().show_data(self.table, self.args)


    def add_switch(self):
        """
        This method add a switch.
        """
        return Helper().add_record(self.table, self.args)


    def change_switch(self):
        """
        This method update a switch.
        """
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')
        # return Helper().update_record(self.table, self.args)


    def clone_switch(self):
        """
        This method clone a switch.
        """
        return Helper().clone_record(self.table, self.args)


    def rename_switch(self):
        """
        This method rename a switch.
        """
        return Helper().rename_record(self.table, self.args, self.args["newswitchname"])


    def remove_switch(self):
        """
        This method remove a switch.
        """
        return Helper().delete_record(self.table, self.args)


    def listinterface_switch(self):
        """List the interfaces of a switch (table by default, JSON with -R/--raw)."""
        response = Rest().get_data(self.table, self.args['name'] + '/interfaces')
        if response.status_code != 200:
            Message().error_exit(response.content, response.status_code)
        data = response.content['config'][self.table][self.args['name']]['interfaces']
        if self.args['raw']:
            Presenter().show_json(Helper().prepare_json(data))
        else:
            data = Helper().prepare_json(data, True)
            fields, rows = Helper().filter_interface(self.interface, data)
            title = f' << {self.table_cap} {self.args["name"]} Interfaces >>'
            Presenter().show_table(title, fields, rows)
        return True


    def showinterface_switch(self):
        """Show one interface of a switch (columns by default, JSON with -R/--raw)."""
        uri = self.args['name'] + '/interfaces/' + self.args['interface']
        response = Rest().get_data(self.table, uri)
        if response.status_code != 200:
            Message().error_exit(response.content, response.status_code)
        data = response.content['config'][self.table][self.args['name']]['interfaces'][0]
        if self.args['raw']:
            Presenter().show_json(Helper().prepare_json(data))
        else:
            data = Helper().prepare_json(data, True)
            fields, rows = Helper().filter_data_col(self.interface, data)
            title = f'{self.table_cap} {self.args["name"]} Interface [{self.args["interface"]}]'
            Presenter().show_table_col(title, fields, rows)
        return True


    def changeinterface_switch(self):
        """Add or change one interface of a switch."""
        name = self.args['name']
        interface = {'interface': self.args['interface']}
        for key in ('network', 'ipaddress', 'macaddress'):
            if self.args.get(key) is not None:
                interface[key] = self.args[key]
        request_data = {'config': {self.table: {name: {'interfaces': [interface]}}}}
        response = Rest().post_data(self.table, name + '/interfaces', request_data)
        if response.status_code in (200, 201, 204):
            Message().show_success(f'Switch {name} interface {self.args["interface"]} updated.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def removeinterface_switch(self):
        """Remove one interface of a switch."""
        name, interface = self.args['name'], self.args['interface']
        response = Rest().get_delete(self.table, name + '/interfaces/' + interface)
        if response.status_code == 204:
            Message().show_success(f'Switch {name} interface {interface} removed.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True
