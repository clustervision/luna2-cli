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
__status__      = "Production"

from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log

class Cluster():
    """
    Cluster Class responsible to show, list,
    and update information for the Cluster
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "cluster"
        self.get_list = None
        if self.args:
            self.get_list = Rest().get_data(self.table)
            if self.args["action"] is None:
                self.cluster_info()
            elif self.args["action"] == 'change':
                self.change_cluster()
            else:
                Helper().show_error("If you want to update then use update as an argument.")
        if parser and subparsers:
            self.getarguments(parser, subparsers)

    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Cluster class.
        """
        cluster_menu = subparsers.add_parser('cluster', help='Cluster operations.')
        cluster_menu.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        cluster_menu.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        cluster_args = cluster_menu.add_subparsers(dest='action')
        cluster_change = cluster_args.add_parser('change', help='Change Cluster')
        cluster_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        cluster_change.add_argument('-n', '--name', help='New Name For Cluster')
        cluster_change.add_argument('-u', '--user', help='Cluster User')
        cluster_change.add_argument('-ntp', '--ntp_server', metavar='N.N.N.N', help='NTP IP')
        cluster_change.add_argument('-o', '--createnode_ondemand', help='Create Nodes while PXE Boot')
        cluster_change.add_argument('-ns', '--nameserver_ip', help='Name Server IP')
        cluster_change.add_argument('-fs', '--forwardserver_ip', help='Forward Server IP')
        cluster_change.add_argument('-c', '--technical_contacts',  help='Technical Contact')
        cluster_change.add_argument('-pm', '--provision_method', help='Provision Method')
        cluster_change.add_argument('-pf', '--provision_fallback', help='Provision Fallback')
        cluster_change.add_argument('-s', '--security',  help='Security')
        cluster_change.add_argument('-d', '--debug', help='Debug Mode')
        return parser


    def cluster_info(self):
        """
        Method to show a cluster in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Get List Data from Helper => {self.get_list}')
        if self.get_list:
            data = self.get_list['config'][self.table]
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table.capitalize()} => {data["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error('No Cluster Found.')
        return response


    def change_cluster(self):
        """
        Method to update cluster in Luna Configuration.
        """
        payload = {}
        for remove in ['verbose', 'command', 'action', 'raw']:
            self.args.pop(remove, None)
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config': {self.table: payload}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, None, request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 204:
                Helper().show_success(f'{self.table.capitalize()} is updated.')
            else:
                Helper().show_error(f'HTTP Error Code {response.status_code}.')
                Helper().show_error(f'HTTP Error {response.content}.')
        else:
            Helper().show_warning(f'Provide Something to update.')
        return True
