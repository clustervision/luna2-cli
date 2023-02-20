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

class Cluster(object):
    """
    Cluster Class responsible to show, list,
    and update information for the Cluster
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "cluster"
        self.version = None
        self.clusterid = None
        if self.args:
            if self.args["action"] == "list":
                self.list_cluster(self.args)
            elif self.args["action"] == "show":
                self.show_cluster(self.args)
            elif self.args["action"] == "update":
                self.update_cluster(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Cluster class.
        """
        cluster_menu = subparsers.add_parser('cluster', help='Cluster operations.')
        cluster_args = cluster_menu.add_subparsers(dest='action')
        ## >>>>>>> Cluster Command >>>>>>> list
        cmd = cluster_args.add_parser('list', help='List Cluster')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Cluster Command >>>>>>> show
        cmd = cluster_args.add_parser('show', help='Show Cluster')
        cmd.add_argument('name', help='Name of the Cluster')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Cluster Command >>>>>>> add
        cmd = cluster_args.add_parser('update', help='Update Cluster')
        cmd.add_argument('name', help='Name of the Cluster')
        cmd.add_argument('--name', '-n', help='New Cluster Name')
        cmd.add_argument('--user', '-u', help='Cluster User')
        cmd.add_argument('--ntp_server', '-ntp', metavar='N.N.N.N', help='Cluster NTP Server')
        cmd.add_argument('--clusterdebug', '-cd', help='Debug Mode')
        cmd.add_argument('--technical_contacts', '-c', help='Technical Contact')
        cmd.add_argument('--provision_method', '-pm', help='Provision Method')
        cmd.add_argument('--provision_fallback', '-fb', help='Provision Fallback')
        return parser


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
