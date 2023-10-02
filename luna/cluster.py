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
Cluster Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.constant import BOOL_CHOICES, BOOL_META
from luna.utils.message import Message
from luna.utils.arguments import Arguments

class Cluster():
    """
    Cluster Class responsible to show and change information for the Cluster
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "cluster"
        if self.args:
            if self.args["action"] is None:
                self.cluster_info()
            elif self.args["action"] == 'change':
                self.change_cluster()
            else:
                Message().show_warning('Use change as an argument to make an change in cluster.')
        else:
            self.get_arguments(parser, subparsers)

    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Cluster class.
        """
        cluster_menu = subparsers.add_parser('cluster', help='Cluster Information.')
        Arguments().common_list_args(cluster_menu)
        cluster_args = cluster_menu.add_subparsers(dest='action')
        cluster_change = cluster_args.add_parser('change', help='Change Cluster')
        cluster_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        cluster_change.add_argument('-n', '--name', help='New Name For Cluster')
        cluster_change.add_argument('-u', '--user', help='Cluster User')
        cluster_change.add_argument('-ntp', '--ntp_server', metavar='N.N.N.N', help='NTP IP')
        cluster_change.add_argument('-o', '--createnode_ondemand', choices=BOOL_CHOICES,
                                    metavar=BOOL_META, help='On Demand Nodes')
        cluster_change.add_argument('-ns', '--nameserver_ip', help='Name Server IP')
        cluster_change.add_argument('-fs', '--forwardserver_ip', help='Forward Server IP')
        cluster_change.add_argument('-c', '--technical_contacts',  help='Technical Contact')
        cluster_change.add_argument('-pm', '--provision_method', help='Provision Method')
        cluster_change.add_argument('-pf', '--provision_fallback', help='Provision Fallback')
        cluster_change.add_argument('-s', '--security', choices=BOOL_CHOICES,
                                    metavar=BOOL_META, help='Security')
        cluster_change.add_argument('-d', '--debug', choices=BOOL_CHOICES,
                                    metavar=BOOL_META, help='Debug Mode')
        return parser


    def cluster_info(self):
        """
        This method to show the cluster information.
        """
        return Helper().show_data(self.table, self.args)


    def change_cluster(self):
        """
        This method update the luna cluster.
        """
        return Helper().update_record(self.table, self.args)
