#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BMC Setup Class for the CLI
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
from luna.utils.arguments import Arguments

class BMCSetup():
    """
    BMC Setup Class responsible to show, list, add, change,
    remove, rename and clone information for the BMC Setup.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "bmcsetup"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_bmcsetup')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the BMC Setup class.
        """
        bmcsetup_menu = subparsers.add_parser('bmcsetup', help='BMC Setup operations.')
        bmcsetup_args = bmcsetup_menu.add_subparsers(dest='action')
        bmcsetup_list = bmcsetup_args.add_parser('list', help='List BMC Setups')
        Arguments().common_list_args(bmcsetup_list)
        bmcsetup_show = bmcsetup_args.add_parser('show', help='Show BMC Setup')
        bmcsetup_show.add_argument('name', help='BMC Setup Name')
        Arguments().common_list_args(bmcsetup_show)
        bmcsetup_member = bmcsetup_args.add_parser('member', help='OS Image Used by Nodes')
        bmcsetup_member.add_argument('name', help='BMC Setup Name')
        Arguments().common_list_args(bmcsetup_member)
        bmcsetup_add = bmcsetup_args.add_parser('add', help='Add BMC Setup')
        Arguments().common_bmcsetup_args(bmcsetup_add)
        bmcsetup_change = bmcsetup_args.add_parser('change', help='Change a BMC Setup')
        Arguments().common_bmcsetup_args(bmcsetup_change)
        bmcsetup_clone = bmcsetup_args.add_parser('clone', help='Clone BMC Setup')
        Arguments().common_bmcsetup_args(bmcsetup_clone)
        bmcsetup_clone.add_argument('newbmcname', help='New BMC Setup Name')
        bmcsetup_rename = bmcsetup_args.add_parser('rename', help='Rename BMC Setup')
        bmcsetup_rename.add_argument('name', help='BMC Setup Name')
        bmcsetup_rename.add_argument('newbmcname', help='New BMC Setup Name')
        bmcsetup_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        bmcsetup_remove = bmcsetup_args.add_parser('remove', help='Remove BMC Setup')
        bmcsetup_remove.add_argument('name', help='BMC Setup Name')
        bmcsetup_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_bmcsetup(self):
        """
        This method list all bmcsetup.
        """
        return Helper().get_list(self.table, self.args)


    def show_bmcsetup(self):
        """
        This method show a specific bmcsetup.
        """
        return Helper().show_data(self.table, self.args)


    def member_bmcsetup(self):
        """
        This method will show all Nodes boots with the BMC Setup.
        """
        return Helper().member_record(self.table, self.args)


    def add_bmcsetup(self):
        """
        This method add a bmcsetup.
        """
        return Helper().add_record(self.table, self.args)


    def change_bmcsetup(self):
        """
        This method update a bmcsetup.
        """
        return Helper().update_record(self.table, self.args)


    def clone_bmcsetup(self):
        """
        This method clone a bmcsetup.
        """
        return Helper().clone_record(self.table, self.args)


    def rename_bmcsetup(self):
        """
        This method rename a bmcsetup.
        """
        return Helper().rename_record(self.table, self.args, self.args["newbmcname"])


    def remove_bmcsetup(self):
        """
        This method remove a bmcsetup.
        """
        return Helper().delete_record(self.table, self.args)
