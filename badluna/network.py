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

from operator import methodcaller
from badluna.utils.helper import Helper
from badluna.utils.rest import Rest
from badluna.utils.log import Log

class Network():
    """
    Network Class responsible to show, list,
    add, remove informations
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "network"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "change", "rename", "clone", "remove",
                       "ipinfo", "nextip"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_network')
                call(self)
            else:
                Helper().show_error(f"Kindly choose from {actions}.")
        else:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Network class.
        """
        network_menu = subparsers.add_parser('network', help='Network operations.')
        network_args = network_menu.add_subparsers(dest='action')
        network_list = network_args.add_parser('list', help='List Networks')
        Helper().common_list_args(network_list)
        network_show = network_args.add_parser('show', help='Show Network')
        network_show.add_argument('name', help='Network Name')
        Helper().common_list_args(network_show)
        network_add = network_args.add_parser('add', help='Add Network')
        network_add.add_argument('name', help='Network Name')
        network_add.add_argument('-N', '--network', required=True, help='Network')
        network_add.add_argument('-g', '--gateways', help='Gateway')
        network_add.add_argument('-nsip', '--nameserver_ip', help='NameServer IP')
        network_add.add_argument('-ntp', '--ntp_server', help='NTP Server')
        network_add.add_argument('-dhcp', '--dhcp', choices=Helper().boolean(),
                                 metavar="{y,yes,n,no,''}", help='DHCP')
        network_add.add_argument('-ds', '--dhcp_range_begin', help='DHCP Range Start')
        network_add.add_argument('-de', '--dhcp_range_end', help='DHCP Range End')
        network_add.add_argument('-c', '--comments', action='store_true', help='Comment')
        network_add.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        network_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_change = network_args.add_parser('change', help='Change Network')
        network_change.add_argument('name', help='Network Name')
        network_change.add_argument('-N', '--network', help='Network')
        network_change.add_argument('-g', '--gateway', help='Gateway')
        network_change.add_argument('-nsip', '--nameserver_ip', help='Name server IP')
        network_change.add_argument('-ntp', '--ntp_server', help='NTP Server')
        network_change.add_argument('-dhcp', '--ddhcp', choices=Helper().boolean(),
                                    metavar="{y,yes,n,no,''}", help='DHCP')
        network_change.add_argument('-ds', '--dhcp_range_begin', help='DHCP Range Start')
        network_change.add_argument('-de', '--dhcp_range_end', help='DHCP Range End')
        network_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        network_change.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        network_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_clone = network_args.add_parser('clone', help='Clone Network')
        network_clone.add_argument('name', help='Network Name')
        network_clone.add_argument('newnetname', help='New Network Name')
        network_clone.add_argument('-N', '--network', required=True, help='Network')
        network_clone.add_argument('-g', '--gateway', help='Gateway')
        network_clone.add_argument('-nsip', '--nameserver_ips', help='Name server IP')
        network_clone.add_argument('-ntp', '--ntp_server', help='NTP Server')
        network_clone.add_argument('-dhcp', '--dhcp', choices=Helper().boolean(),
                                   metavar="{y,yes,n,no,''}", help='DHCP')
        network_clone.add_argument('-ds', '--dhcp_range_begin', help='DHCP Range Start')
        network_clone.add_argument('-de', '--dhcp_range_end', help='DHCP Range End')
        network_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        network_clone.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        network_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_rename = network_args.add_parser('rename', help='Rename Network')
        network_rename.add_argument('name', help='Network Name')
        network_rename.add_argument('newname', help='New Network Name')
        network_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_remove = network_args.add_parser('remove', help='Remove Network')
        network_remove.add_argument('name', help='Network Name')
        network_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_ipinfo = network_args.add_parser('ipinfo', help='Show Network IP Information')
        network_ipinfo.add_argument('name', help='Network Name')
        network_ipinfo.add_argument('ipaddres', help='IP Address from the Network')
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


    def clone_network(self):
        """
        This method clone a network.
        """
        return Helper().clone_record(self.table, self.args, self.args["newnetname"])


    def ipinfo_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        response = False
        uri = f'{self.args["name"]}/{self.args["ipaddress"]}'
        self.logger.debug(f'IPinfo URI => {uri}')
        ipinfo = Rest().get_data(self.table, uri)
        self.logger.debug(f'IPinfo Response => {ipinfo}')
        if ipinfo:
            status = ipinfo['config']['network'][self.args["ipaddress"]]['status']
            status = f'{self.args["ipaddress"]} is {status.capitalize()}.'
            if 'free' in status:
                response = Helper().show_success(status)
            else:
                response = Helper().show_warning(status)
        return response


    def nextip_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        response = False
        uri = f'{self.args["name"]}/_nextfreeip'
        self.logger.debug(f'NextIP URI => {uri}')
        nextip = Rest().get_data(self.table, uri)
        self.logger.debug(f'NextIP Response => {nextip}')
        if nextip:
            ipaddr = nextip['config']['network'][self.args["name"]]['nextip']
            if ipaddr:
                response = Helper().show_success(f'Next Available IP Address is {ipaddr}.')
            else:
                response = Helper().show_warning(f'IP not available on {self.args["ipaddress"]}.')
        return response
