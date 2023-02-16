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


from luna.utils.helper import Helper
from luna.utils.rest import Rest

class Service(object):
    """
    Service Class responsible to perform service
    based actions for predefined services.
    """

    def __init__(self, args=None):
        self.args = args
        self.route = "service"
        if self.args["service"] and self.args["action"]:
            self.service_action(self.args)
        else:
            print("Select a service and action to be performed, See with -h.")


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
        dhcp_parser.add_parser('stop', help='Stop DHCP Service')
        dhcp_parser.add_parser('start', help='Start DHCP Service')
        dhcp_parser.add_parser('restart', help='Restart DHCP Service')
        ## >>>>>>> Service Command >>>>>>> dns
        dns = service_args.add_parser('dns', help='DNS Service')
        dns_parser = dns.add_subparsers(dest='action')
        dns_parser.add_parser('stop', help='Stop DNS Service')
        dns_parser.add_parser('start', help='Start DNS Service')
        dns_parser.add_parser('restart', help='Restart DNS Service')
        ## >>>>>>> Service Command >>>>>>> luna2
        daemon = service_args.add_parser('luna2', help='Luna Daemon Service')
        daemon_parser = daemon.add_subparsers(dest='action')
        daemon_parser.add_parser('stop', help='Stop Luna Daemon Service')
        daemon_parser.add_parser('start', help='Start Luna Daemon Service')
        daemon_parser.add_parser('restart', help='Restart Luna Daemon Service')
        return parser


    def service_action(self, args=None):
        """
        Method to will perform the action on
        the desired service via Luna Daemon
        with it's REST API.
        """
        response = False
        uri = f'{args["service"]}/{args["action"]}'
        result = Rest().get_raw(self.route, uri)
        if result:
            http_code = result.status_code
            result = result.json()
            result = result['service'][args["service"]]
            if http_code == 200:
                response = Helper().show_success(f'{args["action"]} performed on {args["service"]}')
                Helper().show_success(f'{result}')
            else:
                Helper().show_error(f'HTTP error code is: {http_code} ')
                Helper().show_error(f'{result}')
        return response
