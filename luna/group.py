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


from luna.utils.helper import Helper
from luna.utils.presenter import Presenter

class Group(object):
    """
    Group Class responsible to show, list,
    add, remove information for the Group
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "group"
        self.version = None
        self.clusterid = None
        if self.args:
            if self.args["action"] == "list":
                self.list_group(self.args)
            elif self.args["action"] == "show":
                self.show_group(self.args)
            elif self.args["action"] == "add":
                self.add_group(self.args)
            elif self.args["action"] == "update":
                self.update_group(self.args)
            elif self.args["action"] == "rename":
                self.rename_group(self.args)
            elif self.args["action"] == "delete":
                self.delete_group(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Network class.
        """
        group_menu = subparsers.add_parser('group', help='Group operations')
        group_args = group_menu.add_subparsers(dest='action')
        ## >>>>>>> Group Command >>>>>>> list
        cmd = group_args.add_parser('list', help='List Groups')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        cmd.add_argument('--all', '-A', action='store_true', help='All Data output')
        ## >>>>>>> Group Command >>>>>>> show
        cmd = group_args.add_parser('show', help='Show Group')
        cmd.add_argument('name', help='Name of the Group')
        cmd_group = cmd.add_mutually_exclusive_group()
        cmd_group.add_argument('--raw', '-R', action='store_true', help='JSON output')
        cmd_group.add_argument('--osimage', '-o', action='store_true', help='Show osimage assigned to Group.')
        cmd_group.add_argument('--prescript', '--pre', action='store_true', help='Show prescript')
        cmd_group.add_argument('--postscript', '--post', action='store_true', help='Show postscript.')
        cmd_group.add_argument('--partscript', '--part', action='store_true', help='Show partition script.')
        cmd_group.add_argument('--bmcsetup', '-b', action='store_true', help='BMCSetup assigned to Group.')
        cmd_group.add_argument('--interface', '-i', help='Interface')
        cmd_group.add_argument('--comment', '-C', action='store_true', help='Print comment')
        ## >>>>>>> Group Command >>>>>>> add
        cmd = group_args.add_parser('add', help='Add Group')
        cmd.add_argument('--name', '-n', required=True, help='Name of the Group')
        cmd.add_argument('--osimage', '-o', required=True, help='Osimage assigned to Group')
        cmd.add_argument('--bmcsetup', '-b', help='BMCSetup assigned to Group')
        cmd.add_argument('--bmcnetwork', '-bn', help='Network for BMC interface')
        cmd.add_argument('--network', '-N', required=True, help='Network for boot interface')
        ## >>>>>>> Group Command >>>>>>> change
        cmd = group_args.add_parser('change', help='Change Group')
        cmd.add_argument('name', help='Name of the Group')
        cmd.add_argument('--osimage', '-o', help='Osimage assigned to Group')
        cmd.add_argument('--domain', '-d', help='Domain')
        cmd.add_argument('--prescript', '--pre', action='store_true', help='Set prescript')
        cmd.add_argument('--postscript', '--post', action='store_true', help='Set postscript.')
        cmd.add_argument('--partscript', '--part', action='store_true', help='Set partition script. Localdisk should be mounted under /sysimage')
        cmd.add_argument('--bmcsetup', '-b', help='BMCSetup assigned to Group')
        cmd.add_argument('--torrent_if', '--ti', help='High-speed interface')
        cmd.add_argument('--interface', '-i', help='Interface')
        cmd.add_argument('--add', '-A', action='store_true', help='Add interface')
        cmd.add_argument('--delete', '-D', action='store_true', help='Delete interface')
        cmd.add_argument('--setnet', '--sn', metavar='NETWORK', help='Set Network for interface or for BMC')
        cmd.add_argument('--delnet', '--dn', action='store', nargs='?', default=False, const=True, help='Delete Network for interface or for BMC')
        cmd.add_argument('--edit', '-e', action='store_true', help='Edit interface parameters or edit scripts')
        cmd.add_argument('--rename', '--nn', metavar='NEW_NAME', help='Rename interface')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Group Command >>>>>>> clone
        cmd = group_args.add_parser('clone', help='Clone Group.')
        cmd.add_argument('name', help='Name of the Group')
        cmd.add_argument('--to', '-t', required=True, help='Name of the clone group')
        ## >>>>>>> Group Command >>>>>>> rename
        cmd = group_args.add_parser('rename', help='Rename Group.')
        cmd.add_argument('name', help='Name of the Group')
        cmd.add_argument('--newname', '--nn', required=True, help='New name')
        ## >>>>>>> Group Command >>>>>>> delete
        cmd = group_args.add_parser('delete', help='Delete Group')
        cmd.add_argument('name', help='Name of the Group')
        ## >>>>>>> Group Commands Ends
        return parser



    def list_group(self, args=None):
        """
        Method to list all groups from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = dict(Helper().get_list(self.table))
        data = get_list['config']['group']
        if args['raw']:
            response = Presenter().show_json(data)
        elif args['all']:
            fields, rows  = Helper().filter_data(self.table, data, args['all'])
            response = Presenter().show_table(fields, rows)
        else:
            fields, rows  = Helper().filter_data(self.table, data, None)
            response = Presenter().show_table(fields, rows)
        return response


    def show_group(self, args=None):
        """
        Method to show a network in Luna Configuration.
        """
        return True


    def add_group(self, args=None):
        """
        Method to add new network in Luna Configuration.
        """
        return True


    def delete_group(self, args=None):
        """
        Method to delete a network in Luna Configuration.
        """
        return True


    def update_group(self, args=None):
        """
        Method to update a network in Luna Configuration.
        """
        return True


    def rename_group(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True


    def clone_group(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True
