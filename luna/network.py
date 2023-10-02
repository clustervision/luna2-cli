#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
#This code is part of the TrinityX software suite
#Copyright (C) 2023  ClusterVision Solutions b.v.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>

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

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import actions
from luna.utils.message import Message
from luna.utils.arguments import Arguments

class Network():
    """
    Network Class responsible to show, list,
    add, remove Information
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "network"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_network')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Network class.
        """
        network_menu = subparsers.add_parser('network', help='Network operations.')
        network_args = network_menu.add_subparsers(dest='action')
        network_list = network_args.add_parser('list', help='List Networks')
        Arguments().common_list_args(network_list)
        network_show = network_args.add_parser('show', help='Show Network')
        network_show.add_argument('name', help='Network Name')
        Arguments().common_list_args(network_show)
        network_add = network_args.add_parser('add', help='Add Network')
        Arguments().common_network_args(network_add, True)
        network_change = network_args.add_parser('change', help='Change Network')
        Arguments().common_network_args(network_change)
        network_rename = network_args.add_parser('rename', help='Rename Network')
        network_rename.add_argument('name', help='Network Name')
        network_rename.add_argument('newnetname', help='New Network Name')
        network_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_remove = network_args.add_parser('remove', help='Remove Network')
        network_remove.add_argument('name', help='Network Name')
        network_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_taken = network_args.add_parser('reserve', help='List Reserved IP\'s for Network')
        network_taken.add_argument('name', help='Network Name')
        network_taken.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        network_taken.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_ipinfo = network_args.add_parser('ipinfo', help='Show Network IP Information')
        network_ipinfo.add_argument('name', help='Network Name')
        network_ipinfo.add_argument('ipaddress', help='IP Address from the Network')
        network_ipinfo.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_nextip = network_args.add_parser('nextip', help='Show Next Available IP Address')
        network_nextip.add_argument('name', help='Network Name')
        network_nextip.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_network(self):
        """
        This method list all networks.
        """
        return Helper().get_list(self.table, self.args)


    def show_network(self):
        """
        This method show a specific network.
        """
        return Helper().show_data(self.table, self.args)


    def add_network(self):
        """
        This method add a network.
        """
        return Helper().add_record(self.table, self.args)


    def change_network(self):
        """
        This method update a network.
        """
        return Helper().update_record(self.table, self.args)


    def rename_network(self):
        """
        This method rename a network.
        """
        return Helper().rename_record(self.table, self.args, self.args["newnetname"])


    def remove_network(self):
        """
        This method remove a network.
        """
        return Helper().delete_record(self.table, self.args)


    def reserve_network(self):
        """
        This method will show all Nodes boots with the OSimage.
        """
        return Helper().reserved_ip(self.args)


    def ipinfo_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        response = False
        uri = f'{self.args["name"]}/{self.args["ipaddress"]}'
        self.logger.debug(f'IPinfo URI => {uri}')
        ipinfo = Rest().get_data(self.table, uri)
        if ipinfo.status_code == 200:
            ipinfo = ipinfo.content
        else:
            Message().error_exit(ipinfo.content, ipinfo.status_code)
        self.logger.debug(f'IPinfo Response => {ipinfo}')
        if ipinfo:
            status = ipinfo['config']['network'][self.args["ipaddress"]]['status']
            status = f'{self.args["ipaddress"]} is {status.capitalize()}.'
            if 'free' in status:
                response = Message().show_success(status)
            else:
                response = Message().show_warning(status)
        return response


    def nextip_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        response = False
        uri = f'{self.args["name"]}/_nextfreeip'
        self.logger.debug(f'NextIP URI => {uri}')
        nextip = Rest().get_data(self.table, uri)
        if nextip.status_code == 200:
            nextip = nextip.content
        else:
            Message().error_exit(nextip.content, nextip.status_code)
        self.logger.debug(f'NextIP Response => {nextip}')
        if nextip:
            ipaddress = nextip['config']['network'][self.args["name"]]['nextip']
            if ipaddress:
                response = Message().show_success(f'Next Available IP Address is {ipaddress}.')
            else:
                response = Message().show_warning(f'IP not available on {self.args["ipaddress"]}.')
        return response
