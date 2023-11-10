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
Monitor status class for the Luna CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import json
from luna.utils.rest import Rest
from luna.utils.presenter import Presenter
from luna.utils.log import Log
from luna.utils.message import Message

class Monitor():
    """
    Monitor Class responsible to show status and queue status.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "monitor"
        if self.args:
            if self.args["action"] is None:
                Message().show_warning('Use status or queue to see the status of monitor service.')
            elif self.args["action"] == 'status':
                self.status_monitor()
            elif self.args["action"] == 'queue':
                self.queue_monitor()
            else:
                Message().show_warning('Use status or queue to see the status of monitor service.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Monitor class.
        """
        monitor = subparsers.add_parser('monitor', help='Get Monitor Status.')
        monitor.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        monitor_menu = monitor.add_subparsers(dest='action')
        monitor_status = monitor_menu.add_parser('status', help='Get Monitor Status.')
        monitor_status.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        monitor_queue = monitor_menu.add_parser('queue', help='Get Monitor Queue Status.')
        monitor_queue.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def status_monitor(self):
        """
        This method to show the monitor status.
        """
        response = False
        route = 'monitor/status'
        data = Rest().get_raw(route)
        if data.content:
            data = data.content.decode("utf-8")
            data = json.loads(data)
            response = Presenter().show_json(data)
        else:
            Message().show_error('Monitor Status is Empty.')
        return response


    def queue_monitor(self):
        """
        This method to show the monitor queue status.
        """
        response = False
        route = 'monitor/queue'
        data = Rest().get_raw(route)
        if data.content:
            data = data.content.decode("utf-8")
            data = json.loads(data)
            response = Presenter().show_json(data)
        else:
            Message().show_error('Monitor Queue is Empty.')
        return response
