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
Cloud Class for the CLI to support cloud providers.
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
from luna.utils.arguments import Arguments

class Cloud():
    """
    Cloud Class responsible to show, list, add, change, remove, rename information for the Cloud.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "cloud"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_cloud')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Cloud Provider class.
        """
        cloud_menu = subparsers.add_parser('cloud', help='Cloud Operations.')
        cloud_args = cloud_menu.add_subparsers(dest='action')
        cloud_list = cloud_args.add_parser('list', help='List All Cloud Providers')
        Arguments().common_list_args(cloud_list)
        cloud_show = cloud_args.add_parser('show', help='Show Cloud Providers')
        cloud_show.add_argument('name', help='Cloud Provider Name')
        Arguments().common_list_args(cloud_show)
        cloud_add = cloud_args.add_parser('add', help='Add Cloud Provider')
        Arguments().common_cloud_args(cloud_add)
        cloud_change = cloud_args.add_parser('change', help='Change a Cloud Provider')
        Arguments().common_cloud_args(cloud_change)
        cloud_remove = cloud_args.add_parser('remove', help='Remove Cloud Provider')
        cloud_remove.add_argument('name', help='Cloud Provider Name')
        cloud_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def list_cloud(self):
        """
        This method list all cloud.
        """
        return Helper().get_list(self.table, self.args)


    def show_cloud(self):
        """
        This method show a specific cloud.
        """
        return Helper().show_data(self.table, self.args)


    def add_cloud(self):
        """
        This method add a cloud.
        """
        return Helper().add_record(self.table, self.args)


    def change_cloud(self):
        """
        This method update a cloud.
        """
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')


    def remove_cloud(self):
        """
        This method remove a cloud.
        """
        return Helper().delete_record(self.table, self.args)
