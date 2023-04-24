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

import sys
from time import sleep
from multiprocessing import Process
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import SERVICES, SERVICE_ACTIONS

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
            if self.args["service"]:
                if self.args["action"]:
                    self.logger.debug(f'Arguments Supplied => {self.args}')
                    self.service_action()
                else:
                    Helper().show_error(f"Kindly choose action from {SERVICE_ACTIONS}.")
            else:
                Helper().show_error(f"Kindly choose service {SERVICES}.")
        else:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Service class.
        """
        service_menu = subparsers.add_parser('service', help='Service operations.')
        service_args = service_menu.add_subparsers(dest='service')
        for name in SERVICES:
            service = service_args.add_parser(name, help=f'{name.upper()} Service')
            service_parser = service.add_subparsers(dest='action')
            for action in SERVICE_ACTIONS:
                action_help = f'{action.capitalize()} {name.upper()} Service'
                action_args = service_parser.add_parser(action, help=action_help)
                action_args.add_argument('-v', '--verbose', action='store_true',
                                         help='Verbose Mode')
        return parser


    def service_action(self):
        """
        Method to will perform the action on the desired service by Luna Daemon's API.
        """
        response = False
        uri = f'{self.args["service"]}/{self.args["action"]}'
        self.logger.debug(f'Service URL => {uri}')
        response = Rest().get_raw(self.route, uri)
        self.logger.debug(f'Response => {response}')
        content = response.json()
        status_code = response.status_code
        if self.args["action"] == 'status':
            if status_code == 200:
                if 'info' in content:
                    print(content['info'])
                else:
                    service_name = list(content['monitor']['Service'].keys())
                    service_status = content['monitor']['Service'][service_name[0]]
                    print(service_status)
            elif status_code == 500:
                service_name = list(content['monitor']['Service'].keys())
                service_status = content['monitor']['Service'][service_name[0]]
                sys.stderr.write(f'{service_status}\n')
                sys.exit(1)
            else:
                sys.stderr.write(f'HTTP ERROR ::{status_code}\n')
                sys.stderr.write(f'RESPONSE  :: {content}\n')
                sys.exit(1)
        else:
            fetch_msg = f"{self.args['service']} {self.args['action']}..."
            process1 = Process(target=Helper().loader, args=(fetch_msg,))
            process1.start()
            if 'request_id' in content:
                uri = f'service/status/{content["request_id"]}'
                def dig_service_status(uri):
                    result = Rest().get_raw(uri)
                    if result.status_code == 404:
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
        return response
