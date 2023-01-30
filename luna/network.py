#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"


# import luna

class Network(object):
    """
    Network Class responsible to show, list,
    add, remove information for the networks
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "network"
        self.version = None
        self.clusterid = None
        print(self.args)
        if self.args:
            if self.args["action"] == "list":
                self.list_network(self.args)
            elif self.args["action"] == "show":
                self.show_network(self.args)
            elif self.args["action"] == "add":
                self.add_network(self.args)
            elif self.args["action"] == "update":
                self.update_network(self.args)
            elif self.args["action"] == "rename":
                self.rename_network(self.args)
            elif self.args["action"] == "delete":
                self.delete_network(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Network class.
        """
        network_menu = subparsers.add_parser('network', help='Node operations.')
        network_args = network_menu.add_subparsers(dest='action')
        ## >>>>>>> Network Command >>>>>>> list
        cmd = network_args.add_parser('list', help='List Networks')
        ## >>>>>>> Network Command >>>>>>> show
        cmd = network_args.add_parser('show', help='Show Network')
        cmd.add_argument('name', help='Name of the Network')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        cmd.add_argument('--reservedips', '-r', action='store_true', help='List reserved IPs')
        cmd.add_argument('--comment', '-C', action='store_true', help='Print comment')
        ## >>>>>>> Network Command >>>>>>> add
        cmd = network_args.add_parser('add', help='Add Network')
        cmd.add_argument('--name', '-n', required=True, help='Name of the Network')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', required=True, help='Network')
        cmd.add_argument('--prefix', '-P', metavar='PP', required=True, type=int, help='Prefix')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        ## >>>>>>> Network Command >>>>>>> update
        cmd = network_args.add_parser('update', help='Update Network')
        cmd.add_argument('name', help='Name of the Network')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Network')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> clone
        cmd = network_args.add_parser('clone', help='Clone Network')
        cmd.add_argument('name', help='Name of the Network')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Network')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> rename
        cmd = network_args.add_parser('rename', help='Rename Network')
        cmd.add_argument('name', help='Name of the Network')
        cmd.add_argument('--newname', '--nn', required=True, help='New name of the Network')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = network_args.add_parser('delete', help='Delete Network')
        cmd.add_argument('name', help='Name of the Network')
        ## >>>>>>> Network Commands Ends
        return parser


    def list_network(self, args=None):
        """
        Method to list all networks from Luna Configuration.
        """
        print(args)
        return True


    def show_network(self, args=None):
        """
        Method to show a network in Luna Configuration.
        """
        return True


    def add_network(self, args=None):
        """
        Method to add new network in Luna Configuration.
        """
        return True


    def delete_network(self, args=None):
        """
        Method to delete a network in Luna Configuration.
        """
        return True


    def update_network(self, args=None):
        """
        Method to update a network in Luna Configuration.
        """
        return True


    def rename_network(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True


    def clone_network(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True
