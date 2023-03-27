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
__status__      = "Production"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log

class Network():
    """
    Network Class responsible to show, list,
    add, remove information for the networks
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "network"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "change", "rename", "clone", "remove", "ipinfo", "nextip"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_network')
                call(self)
            else:
                Helper().show_error("Not a valid option.")
        if parser and subparsers:
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
        network_show.add_argument('name', help='Name of the Network')
        Helper().common_list_args(network_show)
        network_add = network_args.add_parser('add', help='Add Network')
        network_add.add_argument('name', help='Name of the Network')
        network_add.add_argument('-N', '--network', required=True, help='Network')
        network_add.add_argument('-g', '--gateway', help='Gateway of the Network')
        network_add.add_argument('-nsip', '--nameserver_ip', metavar='N.N.N.N', help='Name server IP')
        network_add.add_argument('-ntp', '--ntp_server', help='NTP Server of the Network')
        network_add.add_argument('-dhcp', '--dhcp', help='DHCP')
        network_add.add_argument('-ds', '--dhcp_range_begin', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        network_add.add_argument('-de', '--dhcp_range_end', metavar='N.N.N.N', help='DHCP Range End for the Network')
        network_add.add_argument('-c', '--comment', help='Comment for Network')
        network_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_change = network_args.add_parser('change', help='Change Network')
        network_change.add_argument('name', help='Name of the Network')
        network_change.add_argument('-N', '--network', help='Network')
        network_change.add_argument('-g', '--gateway', help='Gateway of the Network')
        network_change.add_argument('-nsip', '--nameserver_ip', metavar='N.N.N.N', help='Name server IP')
        network_change.add_argument('-ntp', '--ntp_server', help='NTP Server of the Network')
        network_change.add_argument('-dhcp', '--dhcp', help='DHCP')
        network_change.add_argument('-ds', '--dhcp_range_begin', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        network_change.add_argument('-de', '--dhcp_range_end', metavar='N.N.N.N', help='DHCP Range End for the Network')
        network_change.add_argument('-c', '--comment', help='Comment for Network')
        network_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_clone = network_args.add_parser('clone', help='Clone Network')
        network_clone.add_argument('name', help='Name of the Network')
        network_clone.add_argument('newnetname', help='New name of the Network')
        network_clone.add_argument('-N', '--network', required=True, help='Network')
        network_clone.add_argument('-g', '--gateway', help='Gateway of the Network')
        network_clone.add_argument('-nsip', '--nameserver_ip', metavar='N.N.N.N', help='Name server IP')
        network_clone.add_argument('-ntp', '--ntp_server', help='NTP Server of the Network')
        network_clone.add_argument('-dhcp', '--dhcp', help='DHCP')
        network_clone.add_argument('-ds', '--dhcp_range_begin', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        network_clone.add_argument('-de', '--dhcp_range_end', metavar='N.N.N.N', help='DHCP Range End for the Network')
        network_clone.add_argument('-c', '--comment', help='Comment for Network')
        network_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_rename = network_args.add_parser('rename', help='Rename Network')
        network_rename.add_argument('name', help='Name of the Network')
        network_rename.add_argument('newnetname', help='New name of the Network')
        network_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_remove = network_args.add_parser('remove', help='Remove Network')
        network_remove.add_argument('name', help='Name of the Network')
        network_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_ipinfo = network_args.add_parser('ipinfo', help='Show Network IP Information')
        network_ipinfo.add_argument('name', help='Name of the Network')
        network_ipinfo.add_argument('ipaddress', help='IP Address from the Network')
        network_ipinfo.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        network_nextip = network_args.add_parser('nextip', help='Show Next Available IP Address on the Network')
        network_nextip.add_argument('name', help='Name of the Network')
        network_nextip.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_network(self):
        """
        Method to list all networks from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_network(self):
        """
        Method to add new network in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def change_network(self):
        """
        Method to change a network in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error('Nothing to update.')
        return True


    def rename_network(self):
        """
        Method to rename a network in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newnetname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        return True


    def remove_network(self):
        """
        Method to remove a network in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            self.logger.debug(f'Payload => {payload}')
            response = Rest().get_delete(self.table, payload['name'])
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')        
        return True


    def clone_network(self):
        """
        Method to rename a network in Luna Configuration.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_clone(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newnetname"]}.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


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
            if 'free' in status:
                response = Helper().show_success(f'{self.args["ipaddress"]} is {status.capitalize()}.')
            else:
                response = Helper().show_warning(f'{self.args["ipaddress"]} is {status.capitalize()}.')
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
                response = Helper().show_warning(f'No More IP Address available on network {self.args["ipaddress"]}.')
        return response
