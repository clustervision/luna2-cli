#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2023  ClusterVision Solutions b.v.
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
Control Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from textwrap import wrap
from multiprocessing import Process
from argparse import FileType
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import actions
from luna.utils.message import Message

class Control():
    """
    Control class is a power control area.
    It is responsible to perform all power related operations on the Nodes.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.route = "control"
        self.system = actions(self.route)
        if self.args:
            if self.args["system"]:
                if self.args["action"]:
                    self.logger.debug(f'Arguments Supplied => {self.args}')
                    self.action_status()
                else:
                    Message().show_warning(f'Kindly choose from {actions(self.args["system"])}')
            else:
                Message().show_warning(f'Kindly choose from {self.system}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Control Process class.
        """
        control_menu = subparsers.add_parser('control', help='Control Nodes.')
        control_args = control_menu.add_subparsers(dest='system')
        power_parser = control_args.add_parser('power', help='Power Operations')
        power_menu = power_parser.add_subparsers(dest='action')
        for action in actions('power'):
            action_parser = power_menu.add_parser(action, help=f'Node(s) {action.capitalize()}', usage='%(prog)s [-h] [-v] [node|hostlist]')
            action_parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
            action_parser.add_argument('node', help='Node Name or Node Hostlist')
        sel_parser = control_args.add_parser('sel', help='Sel Operations')
        sel_menu = sel_parser.add_subparsers(dest='action')
        for action in actions('sel'):
            action_parser = sel_menu.add_parser(action, help=f'Node(s) {action.capitalize()}', usage='%(prog)s [-h] [-v] [node|hostlist]')
            action_parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
            action_parser.add_argument('node', help='Node Name or Node Hostlist')
        chassis_parser = control_args.add_parser('chassis', help='Chassis Operations')
        chassis_menu = chassis_parser.add_subparsers(dest='action')
        for action in actions('chassis'):
            action_parser = chassis_menu.add_parser(action, help=f'Node(s) {action.capitalize()}', usage='%(prog)s [-h] [-v] [node|hostlist]')
            action_parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
            action_parser.add_argument('node', help='Node Name or Node Hostlist')
        redfish_parser = control_args.add_parser('redfish', help='RedFish Operations')
        redfish_menu = redfish_parser.add_subparsers(dest='action')
        for action in actions('redfish'):
            action_parser = redfish_menu.add_parser(action, help=f'Node(s) {action.capitalize()}', usage='%(prog)s [-h] [-v] [node|hostlist]')
            action_parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
            action_parser.add_argument('node', help='Node Name or Node Hostlist')
            action_parser.add_argument('-f', '--file', type=FileType('r'), help='File Path')
        return parser


    def action_status(self):
        """
        This method provide the status of one or more nodes.
        """
        message = ''
        response = False
        hostlist = Helper().get_hostlist(self.args['node'])
        if len(hostlist) == 1:
            uri = f'{self.route}/action/{self.args["system"]}'
            uri = f'{uri}/{self.args["node"]}/_{self.args["action"]}'
            self.logger.debug(f'URI => {uri}')
            if 'file' in self.args:
                if self.args['file']:
                    print('<<<<<========== File Data [Under Development]==========>>>>>')
                    print(self.args["file"].read())
                    print('<<<<<========== File Data [Under Development]==========>>>>>')
            response = Rest().get_raw(uri)
            self.logger.debug(f'HTTP STATUS => {response.status_code}')
            self.logger.debug(f'HTTP Response => {response.content}')
            # status = True if response.status_code == [200, 204] else False
            if response.content:
                content = response.json()
                if 'control' in content.keys():
                    message = content['control'][self.args['system']]
                elif 'message' in content.keys():
                    message = content['message']
                else:
                    message = 'NO message received'
            else:
                message = self.args['action']
            if len(message) >= 50:
                message = '\n'.join(wrap(message, width=50))

            title = f"<< Control {self.args['system']} Node {self.args['action']} >>".title()
            fields = ["Node Name", "Status"]
            rows = [self.args['node'], message]
            response = Presenter().show_table_col(title, fields, rows)

        elif len(hostlist) > 1:
            control_process = Process(target=Helper().loader, args=("Fetching Nodes Status...",))
            control_process.start()
            request_id = None
            uri = f'{self.route}/action/{self.args["system"]}/_{self.args["action"]}'
            payload = {
                'control':{
                    self.args['system']:{
                        self.args['action']:{
                            'hostlist':self.args['node']
                        }
                    }
                }
            }
            response = Rest().post_raw(uri, payload)
            self.logger.debug(f'HTTP STATUS => {response.status_code}')
            self.logger.debug(f'HTTP Response => {response.content}')
            if response.status_code == 200:
                content = response.json()
                if 'control' in content:
                    request_id = content['request_id'] if 'request_id' in content else None
                    count = Helper().control_print(self.args['system'], content ,1)
                    if request_id:
                        Helper().dig_control_status(request_id, count, self.args['system'])
                        control_process.terminate()
        return response
