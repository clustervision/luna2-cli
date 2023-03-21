#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Service Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"

from time import sleep
from multiprocessing import Process
from termcolor import colored
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log

class Service(object):
    """
    Service Class responsible to perform service
    based actions for predefined services.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.route = "service"
        if self.args:
            if self.args["service"] and self.args["action"]:
                self.logger.debug(f'Arguments Supplied => {self.args}')
                self.service_action()
        if parser and subparsers:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Service class.
        """
        service_menu = subparsers.add_parser('service', help='Service operations.')
        service_args = service_menu.add_subparsers(dest='service')
        ## >>>>>>> Service Command >>>>>>> dhcp
        dhcp = service_args.add_parser('dhcp', help='DHCP Service')
        dhcp_parser = dhcp.add_subparsers(dest='action')
        dhcp_stop = dhcp_parser.add_parser('stop', help='Stop DHCP Service')
        dhcp_stop.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dhcp_start = dhcp_parser.add_parser('start', help='Start DHCP Service')
        dhcp_start.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dhcp_restart = dhcp_parser.add_parser('restart', help='Restart DHCP Service')
        dhcp_restart.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dhcp_reload = dhcp_parser.add_parser('reload', help='Reload DHCP Service')
        dhcp_reload.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dhcp_status = dhcp_parser.add_parser('status', help='Status Of DHCP Service')
        dhcp_status.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        ## >>>>>>> Service Command >>>>>>> dns
        dns = service_args.add_parser('dns', help='DNS Service')
        dns_parser = dns.add_subparsers(dest='action')
        dns_stop = dns_parser.add_parser('stop', help='Stop DNS Service')
        dns_stop.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dns_start = dns_parser.add_parser('start', help='Start DNS Service')
        dns_start.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dns_restart = dns_parser.add_parser('restart', help='Restart DNS Service')
        dns_restart.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dns_reload = dns_parser.add_parser('reload', help='Reload DNS Service')
        dns_reload.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        dns_status = dns_parser.add_parser('status', help='Status Of DNS Service')
        dns_status.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        ## >>>>>>> Service Command >>>>>>> luna2
        daemon = service_args.add_parser('luna2', help='Luna Daemon Service')
        daemon_parser = daemon.add_subparsers(dest='action')
        daemon_stop = daemon_parser.add_parser('stop', help='Stop Luna Daemon Service')
        daemon_stop.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        daemon_start = daemon_parser.add_parser('start', help='Start Luna Daemon Service')
        daemon_start.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        daemon_restart = daemon_parser.add_parser('restart', help='Restart Luna Daemon Service')
        daemon_restart.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        daemon_reload = daemon_parser.add_parser('reload', help='Reload Luna Daemon Service')
        daemon_reload.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        daemon_status = daemon_parser.add_parser('status', help='Status Of Luna Daemon Service')
        daemon_status.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        return parser


    def service_action(self):
        """
        Method to will perform the action on
        the desired service via Luna Daemon
        with it's REST API.
        """
        response = False
        uri = f'{self.args["service"]}/{self.args["action"]}'
        self.logger.debug(f'Service URL => {uri}')
        result = Rest().get_raw(self.route, uri)
        self.logger.debug(f'Response => {result}')
        if result:
            http_code = result.status_code
            result = result.json()
            result = result['service'][self.args["service"]]
            print(result)
        #     if http_code == 200:
        #         response = Helper().show_success(f'{self.args["action"]} performed on {self.args["service"]}')
        #         Helper().show_success(f'{result}')
        #     else:
        #         Helper().show_error(f'HTTP error code is: {http_code} ')
        #         Helper().show_error(f'{result}')
        # return response
