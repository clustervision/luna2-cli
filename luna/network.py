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


import luna

class Network(object):
    
    
    def __init__(self, args=None):
        self.args = args
        self.nsipaddress = None
        self.version = None
        self.clusterid = None
        print(self.args)
        if self.args:
            if self.args["action"] == "add":
                self.add_network(self.args)
            # elif self.args["action"] == "remove":
            #     self.addnetwork(self.args)
            else:
                pass
                # Cluster.init(self)
        else:
            print("Please pass -h to see help menu.")
        # luna.common()


    def getarguments(self, parser, subparsers):
        ## >>>>>>> Network Commands Begins
        NetworkMenu = subparsers.add_parser('network', help='Node operations.')
        NetworkArgs = NetworkMenu.add_subparsers(dest='action')
        ## >>>>>>> Network Command >>>>>>> list
        cmd = NetworkArgs.add_parser('list', help='List Networks')
        ## >>>>>>> Network Command >>>>>>> show
        cmd = NetworkArgs.add_parser('show', help='Show Network')
        cmd.add_argument('name', help='Name of the Network')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        cmd.add_argument('--reservedips', '-r', action='store_true', help='List reserved IPs')
        cmd.add_argument('--comment', '-C', action='store_true', help='Print comment')
        ## >>>>>>> Network Command >>>>>>> add
        cmd = NetworkArgs.add_parser('add', help='Add Network')
        cmd.add_argument('--name', '-n', required=True, help='Name of the Network')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', required=True, help='Network')
        cmd.add_argument('--prefix', '-P', metavar='PP', required=True, type=int, help='Prefix')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        ## >>>>>>> Network Command >>>>>>> change
        cmd = NetworkArgs.add_parser('change', help='Change Network')
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
        cmd = NetworkArgs.add_parser('rename', help='Rename Network')
        cmd.add_argument('name', help='Name of the Network')
        cmd.add_argument('--newname', '--nn', required=True, help='New name of the Network')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = NetworkArgs.add_parser('delete', help='Delete Network')
        cmd.add_argument('name', help='Name of the Network')
        ## >>>>>>> Network Commands Ends
        return parser

    def add_network(self, args=None):
        table = "network"
        return None

