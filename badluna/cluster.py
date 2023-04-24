#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from badluna.utils.helper import Helper
from badluna.utils.log import Log

class Cluster():
    """
    Cluster Class responsible to show and change
    information for the Cluster
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
                Helper().show_error("If you want to change then use change as an argument.")
        else:
            self.getarguments(parser, subparsers)

    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Cluster class.
        """
        cluster_menu = subparsers.add_parser('cluster', help='Cluster Information.')
        cluster_menu.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        cluster_menu.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        cluster_args = cluster_menu.add_subparsers(dest='action')
        cluster_change = cluster_args.add_parser('change', help='Change Cluster')
        cluster_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        cluster_change.add_argument('-n', '--name', help='New Name For Cluster')
        cluster_change.add_argument('-u', '--user', help='Cluster User')
        cluster_change.add_argument('-ntp', '--ntp_server', metavar='N.N.N.N', help='NTP IP')
        cluster_change.add_argument('-o', '--createnode_ondemand', choices=Helper().boolean(),
                                    metavar="{y,yes,n,no,''}", help='On Demand Nodes')
        cluster_change.add_argument('-ns', '--nameserver_ip', help='Name Server IP')
        cluster_change.add_argument('-fs', '--forwardserver_ips', help='Forward Server IP')
        cluster_change.add_argument('-c', '--technical_contacts',  help='Technical Contact')
        cluster_change.add_argument('-pm', '--provision_method', help='Provision Method')
        cluster_change.add_argument('-pf', '--provision_fallback', help='Provision Fallback')
        cluster_change.add_argument('-s', '--security', choices=Helper().boolean(),
                                    metavar="{y,yes,n,no,''}", help='Security')
        cluster_change.add_argument('-d', '--debug', choices=Helper().boolean(),
                                    metavar="{y,yes,n,no,''}", help='Debug Mode')
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
