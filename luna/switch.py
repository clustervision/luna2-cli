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
__status__      = "Development"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.constant import actions

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
                Helper().show_error(f"Kindly choose from {self.actions}.")
        else:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Switch class.
        """
        # import pathlib
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
        switch_add.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_add.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_change = switch_args.add_parser('change', help='Change Switch')
        switch_change.add_argument('name', help='Switch Name')
        switch_change.add_argument('-N', '--network', help='Network')
        switch_change.add_argument('-ip', '--ipaddress', help='IP Address')
        switch_change.add_argument('-m', '--macaddress', help='MAC Address')
        switch_change.add_argument('-r', '--read', help='Read community')
        switch_change.add_argument('-w', '--rw', help='Write community')
        switch_change.add_argument('-o', '--oid', help='OID')
        switch_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_change.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_clone = switch_args.add_parser('clone', help='Clone Switch')
        switch_clone.add_argument('name', help='Switch Name')
        switch_clone.add_argument('newswitchname', help='New Switch Name')
        switch_clone.add_argument('-N', '--network', help='Network')
        switch_clone.add_argument('-ip', '--ipaddress', help='IP Address')
        switch_clone.add_argument('-m', '--macaddress', help='MAC Address')
        switch_clone.add_argument('-r', '--read', help='Read community')
        switch_clone.add_argument('-w', '--rw', help='Write community')
        switch_clone.add_argument('-o', '--oid', help='OID')
        switch_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        switch_clone.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        switch_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_rename = switch_args.add_parser('rename', help='Rename Switch')
        switch_rename.add_argument('name', help='Switch Name')
        switch_rename.add_argument('newswitchname', help='New Switch Name')
        switch_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        switch_remove = switch_args.add_parser('remove', help='Remove Switch')
        switch_remove.add_argument('name', help='Switch Name')
        switch_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_switch(self):
        """
        This method list all switchs.
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
        return Helper().update_record(self.table, self.args)


    def clone_switch(self):
        """
        This method clone a switch.
        """
        return Helper().clone_record(self.table, self.args, self.args["newswitchname"])


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
