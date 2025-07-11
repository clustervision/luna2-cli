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
Other Devices Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.1"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.constant import actions
from luna.utils.message import Message

class OtherDev():
    """
    OtherDev Class responsible to show, list, add, change,
    remove, rename and clone information for the OtherDev.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "otherdev"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_otherdev')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the OtherDev class.
        """
        otherdev_menu = subparsers.add_parser('otherdev', help='Other Devices operations.')
        otherdev_args = otherdev_menu.add_subparsers(dest='action')
        otherdev_list = otherdev_args.add_parser('list', help='List Other Devices')
        Helper().common_list_args(otherdev_list)
        otherdev_show = otherdev_args.add_parser('show', help='Show Other Devices')
        otherdev_show.add_argument('name', help='Other Device Name').completer = Helper().name_completer(self.table)
        Helper().common_list_args(otherdev_show)
        otherdev_add = otherdev_args.add_parser('add', help='Add Other Devices')
        otherdev_add.add_argument('name', help='Other Device Name')
        otherdev_add.add_argument('-N', '--network', help='Network Name').completer = Helper().name_completer("network")
        otherdev_add.add_argument('-I', '--ipaddress', help='IP Address')
        otherdev_add.add_argument('-M', '--macaddress', help='MAC Address')
        otherdev_add.add_argument('--vendor', help='Add Other Device Vendor Name')
        otherdev_add.add_argument('-c', '--comment', action='store_true', help='Comment')
        otherdev_add.add_argument('--nonetwork', action='store_true', default=None, help='No network verification')
        otherdev_add.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        otherdev_add.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        otherdev_change = otherdev_args.add_parser('change', help='Change Other Devices')
        otherdev_change.add_argument('name', help='Other Device Name').completer = Helper().name_completer(self.table)
        otherdev_change.add_argument('-N', '--network', help='Network').completer = Helper().name_completer("network")
        otherdev_change.add_argument('-I', '--ipaddress', help='IP Address')
        otherdev_change.add_argument('-M', '--macaddress', help='MAC Address')
        otherdev_change.add_argument('--vendor', help='Change Other Device Vendor Name')
        otherdev_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        otherdev_change.add_argument('--nonetwork', action='store_true', default=None, help='No network verification')
        otherdev_change.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        otherdev_change.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        otherdev_clone = otherdev_args.add_parser('clone', help='Clone Other Devices')
        otherdev_clone.add_argument('name', help='Other Device Name').completer = Helper().name_completer(self.table)
        otherdev_clone.add_argument('newotherdevname', help='New Other Device Name')
        otherdev_clone.add_argument('-N', '--network', help='Network').completer = Helper().name_completer("network")
        otherdev_clone.add_argument('-I', '--ipaddress', help='IP Address')
        otherdev_clone.add_argument('-M', '--macaddress', help='MAC Address')
        otherdev_clone.add_argument('--vendor', help='Clone Other Device Vendor Name')
        otherdev_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        otherdev_clone.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        otherdev_clone.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        otherdev_rename = otherdev_args.add_parser('rename', help='Rename Other Devices')
        otherdev_rename.add_argument('name', help='Other Device Name').completer = Helper().name_completer(self.table)
        otherdev_rename.add_argument('newotherdevname', help='New Other Device Name')
        otherdev_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        otherdev_remove = otherdev_args.add_parser('remove', help='Remove Other Devices')
        otherdev_remove.add_argument('name', help='Other Device Name').completer = Helper().name_completer(self.table)
        otherdev_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_otherdev(self):
        """
        This method list all other devices.
        """
        return Helper().get_list(self.table, self.args)


    def show_otherdev(self):
        """
        This method show a specific other device.
        """
        return Helper().show_data(self.table, self.args)


    def add_otherdev(self):
        """
        This method add a other device.
        """
        return Helper().add_record(self.table, self.args)


    def change_otherdev(self):
        """
        This method update a other device.
        """
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')
        # return Helper().update_record(self.table, self.args)

    def clone_otherdev(self):
        """
        This method clone a other device.
        """
        return Helper().clone_record(self.table, self.args)


    def rename_otherdev(self):
        """
        This method rename a other device.
        """
        return Helper().rename_record(self.table, self.args, self.args["newotherdevname"])


    def remove_otherdev(self):
        """
        This method remove a other device.
        """
        return Helper().delete_record(self.table, self.args)
