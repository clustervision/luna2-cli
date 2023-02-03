#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BMC Setup Class for the CLI
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

class BMCSetup(object):
    """
    BMC Setup Class responsible to show, list,
    add, remove information for the BMC Setup
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "bmcsetup"
        self.version = None
        self.clusterid = None
        if self.args:
            if self.args["action"] == "list":
                self.list_bmcsetup(self.args)
            elif self.args["action"] == "show":
                self.show_bmcsetup(self.args)
            elif self.args["action"] == "add":
                self.add_bmcsetup(self.args)
            elif self.args["action"] == "update":
                self.update_bmcsetup(self.args)
            elif self.args["action"] == "rename":
                self.rename_bmcsetup(self.args)
            elif self.args["action"] == "delete":
                self.delete_bmcsetup(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Network class.
        """
        bmcsetup_menu = subparsers.add_parser('bmcsetup', help='BMC Setup operations.')
        bmcsetup_args = bmcsetup_menu.add_subparsers(dest='action')
        ## >>>>>>> Network Command >>>>>>> list
        cmd = bmcsetup_args.add_parser('list', help='List BMC Setups')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        cmd.add_argument('--all', '-A', action='store_true', help='All Data output')
        ## >>>>>>> Network Command >>>>>>> show
        cmd = bmcsetup_args.add_parser('show', help='Show BMC Setup')
        cmd.add_argument('name', help='Name of the BMC Setup')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        cmd.add_argument('--reservedips', '-r', action='store_true', help='List reserved IPs')
        cmd.add_argument('--comment', '-C', action='store_true', help='Print comment')
        ## >>>>>>> Network Command >>>>>>> add
        cmd = bmcsetup_args.add_parser('add', help='Add BMC Setup')
        cmd.add_argument('--name', '-n', required=True, help='Name of the BMC Setup')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', required=True, help='BMC Setup')
        cmd.add_argument('--prefix', '-P', metavar='PP', required=True, type=int, help='Prefix')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        ## >>>>>>> Network Command >>>>>>> update
        cmd = bmcsetup_args.add_parser('update', help='Update BMC Setup')
        cmd.add_argument('name', help='Name of the BMC Setup')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='BMC Setup')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> clone
        cmd = bmcsetup_args.add_parser('clone', help='Clone BMC Setup')
        cmd.add_argument('name', help='Name of the BMC Setup')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='BMC Setup')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> rename
        cmd = bmcsetup_args.add_parser('rename', help='Rename BMC Setup')
        cmd.add_argument('name', help='Name of the BMC Setup')
        cmd.add_argument('--newname', '--nn', required=True, help='New name of the BMC Setup')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = bmcsetup_args.add_parser('delete', help='Delete BMC Setup')
        cmd.add_argument('name', help='Name of the BMC Setup')
        ## >>>>>>> Network Commands Ends
        return parser


    def list_bmcsetup(self, args=None):
        """
        Method to list all networks from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = dict(Helper().get_list(self.table))
        data = get_list['config']['bmcsetup']
        if args['raw']:
            response = Presenter().show_json(data)
        elif args['all']:
            fields, rows  = Helper().filter_data(self.table, data, args['all'])
            response = Presenter().show_table(fields, rows)
        else:
            fields, rows  = Helper().filter_data(self.table, data, None)
            response = Presenter().show_table(fields, rows)
        return response


    def show_bmcsetup(self, args=None):
        """
        Method to show a network in Luna Configuration.
        """
        return True


    def add_bmcsetup(self, args=None):
        """
        Method to add new network in Luna Configuration.
        """
        return True


    def delete_bmcsetup(self, args=None):
        """
        Method to delete a network in Luna Configuration.
        """
        return True


    def update_bmcsetup(self, args=None):
        """
        Method to update a network in Luna Configuration.
        """
        return True


    def rename_bmcsetup(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True


    def clone_bmcsetup(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True
