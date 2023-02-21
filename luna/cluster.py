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

class Cluster(object):
    """
    Cluster Class responsible to show, list,
    and update information for the Cluster
    """

    def __init__(self, args=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "cluster"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] == "list":
                self.list_cluster()
            elif self.args["action"] == "show":
                self.show_cluster()
            elif self.args["action"] == "update":
                self.update_cluster()
            else:
                Helper().show_error("Not a valid option.")
        else:
            Helper().show_error("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Cluster class.
        """
        cluster_menu = subparsers.add_parser('cluster', help='Cluster operations.')
        cluster_args = cluster_menu.add_subparsers(dest='action')
        ## >>>>>>> Cluster Command >>>>>>> list
        cmd = cluster_args.add_parser('list', help='List Cluster')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Cluster Command >>>>>>> show
        cmd = cluster_args.add_parser('show', help='Show Cluster')
        cmd.add_argument('name', help='Name of the Cluster')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Cluster Command >>>>>>> add
        cmd = cluster_args.add_parser('update', help='Update Cluster')
        cmd.add_argument('name', help='Name of the Cluster')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-n', '--name', help='New Cluster Name')
        cmd.add_argument('-u', '--user', help='Cluster User')
        cmd.add_argument('-ntp', '--ntp_server', metavar='N.N.N.N', help='Cluster NTP Server')
        cmd.add_argument('-cd', '--clusterdebug', help='Debug Mode')
        cmd.add_argument('-c', '--technical_contacts', help='Technical Contact')
        cmd.add_argument('-pm', '--provision_method', help='Provision Method')
        cmd.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        return parser


    def list_cluster(self):
        """
        Method to list all cluster from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_list(self.table)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][self.table]
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().get_cluster(self.table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{self.table} is not found.')
        return response


    def show_cluster(self):
        """
        Method to show a cluster in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_list(self.table)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][self.table]
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table.capitalize()} => {data["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return response


    def update_cluster(self):
        """
        Method to update cluster in Luna Configuration.
        """
        payload = {}
        del self.args['debug']
        del self.args['command']
        del self.args['action']
        if self.args['clusterdebug']:
            self.args['debug'] = True
        del self.args['clusterdebug']
        payload = self.args
        filtered = {k: v for k, v in self.args.items() if v is not None}
        payload.clear()
        payload.update(filtered)
        if payload:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = payload
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, None, request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
            else:
                Helper().show_error(f'HTTP error code is: {response} ')
        return True
