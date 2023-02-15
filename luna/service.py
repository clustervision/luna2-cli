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
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest

class Service(object):
    """
    Service Class responsible to perform service
    based actions for predefined services.
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "cluster"
        self.version = None
        self.clusterid = None
        print(self.args)
        # if self.args:
        #     if self.args["service"] == "dhcp":
        #         self.dhcp(self.args)
        #     elif self.args["action"] == "dns":
        #         self.dns(self.args)
        #     elif self.args["action"] == "luna-daemon":
        #         self.daemon(self.args)
        #     else:
        #         print("Not a valid option.")
        # else:
        #     print("Please pass -h to see help menu.")


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
        dhcp_parser.add_parser('status', help='Status Of DHCP Service')
        ## >>>>>>> Service Command >>>>>>> dns
        dns = service_args.add_parser('dns', help='DNS Service')
        dns_parser = dns.add_subparsers(dest='action')
        dns_parser.add_parser('stop', help='Stop DNS Service')
        dns_parser.add_parser('start', help='Start DNS Service')
        dns_parser.add_parser('restart', help='Restart DNS Service')
        dns_parser.add_parser('status', help='Status Of DNS Service')
        ## >>>>>>> Service Command >>>>>>> luna-daemon
        daemon = service_args.add_parser('daemon', help='Luna Daemon Service')
        daemon_parser = daemon.add_subparsers(dest='action')
        daemon_parser.add_parser('stop', help='Stop Luna Daemon Service')
        daemon_parser.add_parser('start', help='Start Luna Daemon Service')
        daemon_parser.add_parser('restart', help='Restart Luna Daemon Service')
        daemon_parser.add_parser('status', help='Status Of Luna Daemon Service')
        return parser


    def dhcp(self, args=None):
        """
        Method to list all cluster from Luna Configuration.
        """
        print(args)


    def dns(self, args=None):
        """
        Method to list all cluster from Luna Configuration.
        """
        print(args)


    def daemon(self, args=None):
        """
        Method to list all cluster from Luna Configuration.
        """
        print(args)
    def list_cluster(self, args=None):
        """
        Method to list all cluster from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_list(self.table)
        if get_list:
            data = get_list['config']['cluster']
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().get_cluster(self.table, data)
                response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{self.table} is not found.')
        return response


    def show_cluster(self, args=None):
        """
        Method to show a cluster in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_list(self.table)
        if get_list:
            data = get_list['config']['cluster']
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.table, data)
                title = f'{self.table.capitalize()} => {data["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'{args["name"]} is not found in {self.table}.')
        return response


    def update_cluster(self, args=None):
        """
        Method to update cluster in Luna Configuration.
        """
        payload = {}
        del args['debug']
        del args['command']
        del args['action']
        payload = args
        filtered = {k: v for k, v in args.items() if v is not None}
        payload.clear()
        payload.update(filtered)
        if payload['clusterdebug']:
            payload['debug'] = True
        del payload['clusterdebug']
        if payload:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = payload
            response = Rest().post_data(self.table, None, request_data)
            if response == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
            else:
                Helper().show_error(f'HTTP error code is: {response} ')
        return True
