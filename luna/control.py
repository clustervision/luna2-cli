#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from multiprocessing import Process
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log

class Control():
    """
    Control class is a power control area.
    It is responsible to perform all power related
    operations on the Nodes.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.route = "control"
        self.action = "power"
        if self.args:
            if self.args["power"]:
                if self.args["action"]:
                    self.logger.debug(f'Arguments Supplied => {self.args}')
                    if self.args["action"] == "status":
                        self.power_status()
                    elif self.args["action"] in ["on", "off"]:
                        self.power_toggle()
                    else:
                        Helper().show_error("Not a valid option.")
                else:
                    Helper().show_error("Kindly choose from status, on, or off.")
            else:
                Helper().show_error("Kindly choose 'power' to perform operations.")
        else:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Control Process class.
        """
        control_menu = subparsers.add_parser('control', help='Control Nodes.')
        control_args = control_menu.add_subparsers(dest='power')
        power_parser = control_args.add_parser('power', help='Power Operations')
        power_menu = power_parser.add_subparsers(dest='action')
        status_parser = power_menu.add_parser('status', help='Status of Node(s)')
        Helper().common_control_args(status_parser)
        on_parser = power_menu.add_parser('on', help='Power On Node(s)')
        Helper().common_control_args(on_parser)
        off_parser = power_menu.add_parser('off', help='Power Off Node(s)')
        Helper().common_control_args(off_parser)
        return parser


    def power_status(self):
        """
        This method provide the status of one or more nodes.
        """
        response = False
        hostlist = Helper().get_hostlist(self.args['node'])
        if len(hostlist) == 1:
            uri = f'{self.action}/{self.args["node"]}/{self.args["action"]}'
            result = Rest().get_raw(self.route, uri)
            http_response = result.json()
            if 'control' in http_response.keys():
                title = "<< Power Control Status Of Node >>"
                fields = ["Node Name", "Status"]
                status = http_response['control']['status']
                rows = [self.args['node'], status]
                response = Presenter().show_table_col(title, fields, rows)
            else:
                response = Helper().show_error(http_response['message'])
        elif len(hostlist) > 1:
            process1 = Process(target=Helper().loader, args=("Fetching Nodes Status...",))
            process1.start()
            uri = f'{self.route}/{self.action}'
            payload = {"control":{"power":{self.args["action"]:{"hostlist":self.args['node']}}}}
            result = Rest().post_raw(uri, payload)
            if result.status_code == 200:
                http_response = result.json()
                request_id = http_response['control']['power']['request_id']
                count = 1
                if 'failed' in http_response['control']['power'].keys():
                    count = Helper().control_print(1, http_response)
                check = Helper().dig_data(result.status_code, request_id, count, 0)
                process1.terminate()
                if check:
                    print("[========] Process Completed")
                else:
                    print("[X ERROR X] Try Again!")
        else:
            Helper().show_error("Incorrect host list")
        return response


    def power_toggle(self):
        """
        This method power on or off one or more nodes.
        """
        http_code = 000
        http_response = None
        response = False
        hostlist = Helper().get_hostlist(self.args['node'])
        if len(hostlist) == 1:
            uri = f'{self.action}/{self.args["node"]}/{self.args["action"]}'
            result = Rest().get_raw(self.route, uri)
            http_code = result.status_code
            if http_code == 204:
                title = "<< Power Control Status Of Node >>"
                fields = ["Node Name", "Status"]
                status = self.args["action"]
                rows = [self.args['node'], status]
                response = Presenter().show_table_col(title, fields, rows)
            else:
                http_response = result.json()
                Helper().show_error(http_response['message'])
        elif len(hostlist) > 1:
            process1 = Process(target=Helper().loader, args=("Fetching Nodes Status...",))
            process1.start()
            uri = f'{self.route}/{self.action}'
            payload = {"control":{"power":{self.args["action"]:{"hostlist":self.args['node']}}}}
            Rest().post_raw(uri, payload)
            payload = {"control":{"power":{'status':{"hostlist":self.args['node']}}}}
            result = Rest().post_raw(uri, payload)
            http_response = result.json()

            if result.status_code == 200:
                request_id = http_response['control']['power']['request_id']
                count = 1
                if 'failed' in http_response['control']['power'].keys():
                    count = Helper().control_print(1, http_response)
                check = Helper().dig_data(result.status_code, request_id, count, 0)
                process1.terminate()
                if check:
                    print("[========] Process Completed")
                else:
                    print("[X ERROR X] Try Again!")
        else:
            Helper().show_error("Incorrect host list")
        return response
