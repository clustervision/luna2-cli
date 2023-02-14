#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Node Class for the CLI
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
from luna.utils.inquiry import Inquiry
from luna.utils.rest import Rest

class Node(object):
    """
    Node Class responsible to show, list,
    add, remove information for the Node
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "node"
        self.version = None
        self.clusterid = None
        if self.args:
            if self.args["action"] == "list":
                self.list_node(self.args)
            elif self.args["action"] == "show":
                self.show_node(self.args)
            elif self.args["action"] == "add":
                self.add_node(self.args)
            elif self.args["action"] == "update":
                self.update_node(self.args)
            elif self.args["action"] == "rename":
                self.rename_node(self.args)
            elif self.args["action"] == "delete":
                self.delete_node(self.args)
            elif self.args["action"] == "clone":
                self.clone_node(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Node class.
        """
        node_menu = subparsers.add_parser('node', help='Node operations.')
        node_args = node_menu.add_subparsers(dest='action')
        ## >>>>>>> Node Command >>>>>>> list
        cmd = node_args.add_parser('list', help='List Node')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Node Command >>>>>>> show
        cmd = node_args.add_parser('show', help='Show Node')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Node Command >>>>>>> add
        cmd = node_args.add_parser('add', help='Add Node')
        cmd.add_argument('--init', '-i', action='store_true', help='Node values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Node')
        cmd.add_argument('--hostname', '-host',help='Hostname')
        cmd.add_argument('--group', '-g', help='Group Name')
        cmd.add_argument('--localboot', '-lb', help='Local Boot')
        cmd.add_argument('--macaddr', '-m', help='MAC Address')
        cmd.add_argument('--osimage', '-o', help='OS Image Name')
        cmd.add_argument('--switch', '-sw', help='Switch Name')
        cmd.add_argument('--switchport', '-sp', help='Switch Port')
        cmd.add_argument('--service', '-ser', action='store_true', help='Service')
        cmd.add_argument('--setupbmc', '-b', action='store_true', help='BMC Setup')
        cmd.add_argument('--status', '-s', help='Status')
        cmd.add_argument('--prescript', '-pre', help='Pre Script')
        cmd.add_argument('--partscript', '-part', help='Part Script')
        cmd.add_argument('--postscript', '-post', help='Post Script')
        cmd.add_argument('--netboot', '-nb', help='Network Boot')
        cmd.add_argument('--localinstall', '-li', help='Local Install')
        cmd.add_argument('--bootmenu', '-bm', help='Boot Menu')
        cmd.add_argument('--provision_interface', '-pi', help='Provision Interface')
        cmd.add_argument('--provision_method', '-pm', help='Provision Method')
        cmd.add_argument('--provision_fallback', '-fb', help='Provision Fallback')
        cmd.add_argument('--tpm_uuid', '-tid', action='store_true', help='TPM UUID')
        cmd.add_argument('--tpm_pubkey', '-tkey', help='TPM Public Key')
        cmd.add_argument('--tpm_sha256', '-tsha', help='TPM SHA256')
        cmd.add_argument('--unmanaged_bmc_users', '-ubu', help='Unmanaged BMC Users')
        cmd.add_argument('--interfaces', '-if', action='append', help='Node Interfaces interfacename:networkname:ipaddress')
        cmd.add_argument('--comment', '-c', help='Comment for Node')
        ## >>>>>>> Node Command >>>>>>> update
        cmd = node_args.add_parser('update', help='Update Node')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Node')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Node Command >>>>>>> clone
        cmd = node_args.add_parser('clone', help='Clone Node')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Node')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Node Command >>>>>>> rename
        cmd = node_args.add_parser('rename', help='Rename Node')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('--newname', '--nn', required=True, help='New name of the Node')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = node_args.add_parser('delete', help='Delete Node')
        cmd.add_argument('name', help='Name of the Node')
        ## >>>>>>> Node Commands Ends
        return parser


    def list_node(self, args=None):
        """
        Method to list all nodes from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_list(self.table)
        if get_list:
            data = get_list['config'][self.table]
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data(self.table, data)
                response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{self.table} is not found.')
        return response


    def show_node(self, args=None):
        """
        Method to show a node in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_record(self.table, args['name'])
        if get_list:
            data = get_list['config'][self.table][args["name"]]
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.table, data)
                title = f'{self.table.capitalize()} => {args["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'{args["name"]} is not found in {self.table}.')
        return response


    def add_node(self, args=None):
        """
        Method to add new node in Luna Configuration.
        """
        return True


    def update_node(self, args=None):
        """
        Method to update a node in Luna Configuration.
        """
        return True


    def rename_node(self, args=None):
        """
        Method to rename a node in Luna Configuration.
        """
        return True


    def delete_node(self, args=None):
        """
        Method to delete a node in Luna Configuration.
        """
        return True


    def clone_node(self, args=None):
        """
        Method to rename a node in Luna Configuration.
        """
        return True
