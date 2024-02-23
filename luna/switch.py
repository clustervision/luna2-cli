#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2023  ClusterVision Solutions b.v.
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
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.constant import actions
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
        switch_menu = subparsers.add_parser('switch', help='Switch operations.')
        switch_args = switch_menu.add_subparsers(dest='action')
        switch_list = switch_args.add_parser('list', help='List Switch')
        Helper().common_list_args(switch_list)
        switch_show = switch_args.add_parser('show', help='Show Switch')
        switch_show.add_argument('name', help='Switch Name')
        Helper().common_list_args(switch_show)
        switch_add = switch_args.add_parser('add', help='Add Switch')
        switch_add.add_argument('name', help='Switch Name')
        switch_add.add_argument('-N', '--network', help='Network')
        switch_add.add_argument('-ip', '--ipaddress', help='IP Address')
        switch_add.add_argument('-m', '--macaddress', help='MAC Address')
        switch_add.add_argument('-r', '--read', help='Read community')
        switch_add.add_argument('-w', '--rw', help='Write community')
        switch_add.add_argument('-o', '--oid', help='OID')
        switch_add.add_argument('-u', '--uplinkports', help='Write community')
        switch_add.add_argument('-vd', '--vendor', help='Add Switch Vendor Name')
        switch_add.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_add.add_argument('-nn', '--nonetwork', action='store_true', default=None, help='No network verification')
        switch_add.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_add.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_change = switch_args.add_parser('change', help='Change Switch')
        switch_change.add_argument('name', help='Switch Name')
        switch_change.add_argument('-N', '--network', help='Network')
        switch_change.add_argument('-ip', '--ipaddress', help='IP Address')
        switch_change.add_argument('-m', '--macaddress', help='MAC Address')
        switch_change.add_argument('-r', '--read', help='Read community')
        switch_change.add_argument('-w', '--rw', help='Write community')
        switch_change.add_argument('-o', '--oid', help='OID')
        switch_change.add_argument('-u', '--uplinkports', help='Write community')
        switch_change.add_argument('-vd', '--vendor', help='Change Switch Vendor Name')
        switch_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_change.add_argument('-nn', '--nonetwork', action='store_true', default=None, help='No network verification')
        switch_change.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_change.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_clone = switch_args.add_parser('clone', help='Clone Switch')
        switch_clone.add_argument('name', help='Switch Name')
        switch_clone.add_argument('newswitchname', help='New Switch Name')
        switch_clone.add_argument('-N', '--network', help='Network')
        switch_clone.add_argument('-ip', '--ipaddress', help='IP Address')
        switch_clone.add_argument('-m', '--macaddress', help='MAC Address')
        switch_clone.add_argument('-r', '--read', help='Read community')
        switch_clone.add_argument('-w', '--rw', help='Write community')
        switch_clone.add_argument('-o', '--oid', help='OID')
        switch_clone.add_argument('-u', '--uplinkports', help='Write community')
        switch_clone.add_argument('-vd', '--vendor', help='Clone Switch Vendor Name')
        switch_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_clone.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_clone.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_rename = switch_args.add_parser('rename', help='Rename Switch')
        switch_rename.add_argument('name', help='Switch Name')
        switch_rename.add_argument('newswitchname', help='New Switch Name')
        switch_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        switch_remove = switch_args.add_parser('remove', help='Remove Switch')
        switch_remove.add_argument('name', help='Switch Name')
        switch_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
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
