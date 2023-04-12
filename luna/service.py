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
__status__      = "Development"

from time import sleep
from multiprocessing import Process
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log

class Service():
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
        else:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Service class.
        """
        service_menu = subparsers.add_parser('service', help='Service operations.')
        service_args = service_menu.add_subparsers(dest='service')
        dhcp = service_args.add_parser('dhcp', help='DHCP Service')
        dhcp_parser = dhcp.add_subparsers(dest='action')
        Helper().common_service_args(dhcp_parser, 'DHCP')
        dns = service_args.add_parser('dns', help='DNS Service')
        dns_parser = dns.add_subparsers(dest='action')
        Helper().common_service_args(dns_parser, 'DNS')
        daemon = service_args.add_parser('luna2', help='Luna Daemon Service')
        daemon_parser = daemon.add_subparsers(dest='action')
        Helper().common_service_args(daemon_parser, 'Luna Daemon')
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
        http_code = result.status_code
        result = result.json()
        if http_code == 200:
            if self.args["action"] == 'status':
                print(f'HTTP CODE :: {http_code}')
                print(f'RESPONSE  :: {result}')
                ## TODO ->
                ## Need to parse it, when daemon side is done
                # result = result['service'][self.args["service"]]
                # response = Helper().show_success(f'{self.args["action"]} {self.args["service"]}')
                # Helper().show_success(f'{result}')
            else:
                fetch_msg = f"{self.args['service']} {self.args['action']}..."
                process1 = Process(target=Helper().loader, args=(fetch_msg,))
                process1.start()
                if 'request_id' in result.keys():
                    uri = f'service/status/{result["request_id"]}'
                    def dig_service_status(uri):
                        result = Rest().get_raw(uri)
                        if result.status_code == 400:
                            process1.terminate()
                            return True
                        elif result.status_code == 200:
                            http_response = result.json()
                            if http_response['message']:
                                message = http_response['message'].split(';;')
                                for msg in message:
                                    sleep(1)
                                    if 'error' in msg.lower() or 'fail' in msg.lower():
                                        print(f'[X ERROR X] {msg}')
                                    else:
                                        print(f'[========] {msg}')
                            sleep(1)
                            return dig_service_status(uri)
                        else:
                            return False
                    response = dig_service_status(uri)
                    if response:
                        service = self.args['service']
                        action = self.args['action']
                        msg = f"[========] Service {service} {action} is finish."
                        print(msg)
                    else:
                        print("[X ERROR X] Try Again!")
                else:
                    process1.terminate()
                    print("[X ERROR X] Something is Wrong with Daemon.")
        else:
            Helper().show_error(f'HTTP error code is: {http_code} ')
            Helper().show_error(f'{result}')
        return response
