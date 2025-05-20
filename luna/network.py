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
Main Class for the CLI
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
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import actions
from luna.utils.message import Message
from luna.utils.arguments import Arguments
from luna.utils.presenter import Presenter

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
        dns_action = ''
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                if self.args["action"] == "dns":
                    if self.args["dns"]:
                        dns_action = f'_{self.args["dns"]}'
                    call = methodcaller(f'network_{self.args["action"]}{dns_action}')
                else:
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
        controllers = Helper().get_controllers()
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
        for controller in controllers:
            network_change.add_argument(f"--{controller}", metavar='<IP Address>', help=f"Changing the IP address for Controller {controller}")
        Arguments().common_network_args(network_change)
        network_rename = network_args.add_parser('rename', help='Rename Network')
        network_rename.add_argument('name', help='Network Name')
        network_rename.add_argument('newnetname', help='New Network Name')
        network_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        network_remove = network_args.add_parser('remove', help='Remove Network')
        network_remove.add_argument('name', help='Network Name')
        network_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        network_taken = network_args.add_parser('reserve', help='List Reserved IP\'s for Network')
        network_taken.add_argument('name', help='Network Name')
        network_taken.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        network_taken.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        network_ipinfo = network_args.add_parser('ipinfo', help='Show Network IP Information')
        network_ipinfo.add_argument('name', help='Network Name')
        network_ipinfo.add_argument('ipaddress', help='IP Address from the Network')
        network_ipinfo.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        network_nextip = network_args.add_parser('nextip', help='Show Next Available IP Address')
        network_nextip.add_argument('name', help='Network Name')
        network_nextip.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        network_dns = network_args.add_parser('dns', help='Show DNS List for a Network')
        network_dns.add_argument('name', help='Network Name')
        Arguments().common_list_args(network_dns)
        network_dns_args = network_dns.add_subparsers(dest='dns')
        network_dns_add = network_dns_args.add_parser('add', help='Add DNS Entry')
        # network_dns_add.add_argument('name', help='Network Name')
        network_dns_add.add_argument('host', help='Host Name')
        network_dns_add.add_argument('ipaddress', help='IP Address')
        network_dns_add.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        network_dns_change = network_dns_args.add_parser('change', help='Change DNS Entry')
        # network_dns_change.add_argument('name', help='Network Name')
        network_dns_change.add_argument('host', help='Host Name')
        network_dns_change.add_argument('ipaddress', help='IP Address')
        network_dns_change.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        network_dns_remove = network_dns_args.add_parser('remove', help='Remove DNS Entry')
        # network_dns_remove.add_argument('name', help='Network Name')
        network_dns_remove.add_argument('host', help='Host Name')
        network_dns_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
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
        change = Helper().compare_data(self.table, self.args)
        if change is True:
            Helper().update_record(self.table, self.args)
        else:
            Message().show_error('Nothing is changed, Kindly change something to update')
        # return Helper().update_record(self.table, self.args)


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

    def network_dns(self):
        """
        This method list all DNS entries.
        """
        response = False
        fields, rows = [], []
        get_list = Rest().get_data(f'dns/{self.args["name"]}')
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if isinstance(get_list.content, dict):
        # if get_list.status_code == 200: ### ==>> Status code should be 404, if no dns entries.
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
            get_list = None
        if get_list:
            data = get_list['config']['dns'][self.args['name']]
            if self.args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = Helper().filter_interface('dns', data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << DNS Entries For Network {self.args["name"]} >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'{self.args["name"]} is not found.')
        return response


    def network_dns_add(self):
        """
        This method add a DNS entry.
        """
        request_data = {'config': {'dns': {self.args['name']: [{'host': self.args['host'], 'ipaddress':self.args['ipaddress']}]}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data('dns', self.args['name'], request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 201:
            Message().show_success(response.content)
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def network_dns_change(self):
        """
        This method update a DNS entry.
        """
        request_data = {'config': {'dns': {self.args['name']: [{'host': self.args['host'], 'ipaddress':self.args['ipaddress']}]}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data('dns', self.args['name'], request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 201:
            Message().show_success(response.content)
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def network_dns_remove(self):
        """
        This method remove a DNS entry.
        """
        name = f"{self.args['name']}/{self.args['host']}"
        response = Rest().get_delete('dns', name)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Message().show_success(f'Network {self.args["name"]} DNS entry {self.args["host"]} is removed.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True
