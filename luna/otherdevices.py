#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other Devices Class for the CLI
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

class OtherDevices(object):
    """
    OtherDevice Class responsible to show, list,
    add, remove information for the OtherDevices
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "otherdev"
        self.version = None
        self.clusterid = None
        if self.args:
            if self.args["action"] == "list":
                self.list_otherdevices(self.args)
            elif self.args["action"] == "show":
                self.show_otherdevices(self.args)
            elif self.args["action"] == "add":
                self.add_otherdevices(self.args)
            elif self.args["action"] == "update":
                self.update_otherdevices(self.args)
            elif self.args["action"] == "rename":
                self.rename_otherdevices(self.args)
            elif self.args["action"] == "delete":
                self.delete_otherdevices(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Network class.
        """
        otherdevice_menu = subparsers.add_parser('otherdevices', help='Other Devices operations.')
        otherdevice_args = otherdevice_menu.add_subparsers(dest='action')
        ## >>>>>>> Network Command >>>>>>> list
        cmd = otherdevice_args.add_parser('list', help='List Other Devices')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Command >>>>>>> show
        cmd = otherdevice_args.add_parser('show', help='Show Other Devices')
        cmd.add_argument('name', help='Name of the Other Devices')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        cmd.add_argument('--reservedips', '-r', action='store_true', help='List reserved IPs')
        cmd.add_argument('--comment', '-C', action='store_true', help='Print comment')
        ## >>>>>>> Network Command >>>>>>> add
        cmd = otherdevice_args.add_parser('add', help='Add Other Devices')
        cmd.add_argument('--name', '-n', required=True, help='Name of the Other Devices')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', required=True, help='Other Devices')
        cmd.add_argument('--prefix', '-P', metavar='PP', required=True, type=int, help='Prefix')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        ## >>>>>>> Network Command >>>>>>> update
        cmd = otherdevice_args.add_parser('update', help='Update Other Devices')
        cmd.add_argument('name', help='Name of the Other Devices')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Other Devices')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> clone
        cmd = otherdevice_args.add_parser('clone', help='Clone Other Devices')
        cmd.add_argument('name', help='Name of the Other Devices')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Other Devices')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> rename
        cmd = otherdevice_args.add_parser('rename', help='Rename Other Devices')
        cmd.add_argument('name', help='Name of the Other Devices')
        cmd.add_argument('--newname', '--nn', required=True, help='New name of the Other Devices')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = otherdevice_args.add_parser('delete', help='Delete Other Devices')
        cmd.add_argument('name', help='Name of the Other Devices')
        ## >>>>>>> Network Commands Ends
        return parser


    def list_otherdevices(self, args=None):
        """
        Method to list all networks from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = dict(Helper().get_list(self.table))
        data = get_list['config'][self.table]
        if args['raw']:
            response = Presenter().show_json(data)
        else:
            fields, rows  = Helper().filter_data(self.table, data)
            response = Presenter().show_table(fields, rows)
        return response


    def show_otherdevices(self, args=None):
        """
        Method to show a network in Luna Configuration.
        """
        return True


    def add_otherdevices(self, args=None):
        """
        Method to add new network in Luna Configuration.
        """
        return True


    def delete_otherdevices(self, args=None):
        """
        Method to delete a network in Luna Configuration.
        """
        return True


    def update_otherdevices(self, args=None):
        """
        Method to update a network in Luna Configuration.
        """
        return True


    def rename_otherdevices(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True


    def clone_otherdevices(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True
