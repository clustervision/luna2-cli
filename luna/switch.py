#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch Class for the CLI
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

class Switch(object):
    """
    Switch Class responsible to show, list,
    add, remove information for the Switch
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "switch"
        self.version = None
        self.clusterid = None
        if self.args:
            if self.args["action"] == "list":
                self.list_switch(self.args)
            elif self.args["action"] == "show":
                self.show_switch(self.args)
            elif self.args["action"] == "add":
                self.add_switch(self.args)
            elif self.args["action"] == "update":
                self.update_switch(self.args)
            elif self.args["action"] == "rename":
                self.rename_switch(self.args)
            elif self.args["action"] == "delete":
                self.delete_switch(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Switch class.
        """
        switch_menu = subparsers.add_parser('switch', help='Switch operations.')
        switch_args = switch_menu.add_subparsers(dest='action')
        ## >>>>>>> Network Command >>>>>>> list
        cmd = switch_args.add_parser('list', help='List Switch')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Command >>>>>>> show
        cmd = switch_args.add_parser('show', help='Show Switch')
        cmd.add_argument('name', help='Name of the Switch')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Command >>>>>>> add
        cmd = switch_args.add_parser('add', help='Add Switch')
        cmd.add_argument('--init', '-i', action='store_true', help='Switch values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Switch')
        cmd.add_argument('--network', '-N', help='Network Switch belongs to')
        cmd.add_argument('--ipaddress', '-ip', help='IP of the Switch')
        cmd.add_argument('--read', '-r', default='public', help='Read community')
        cmd.add_argument('--rw', '-w', default='private', help='Write community')
        cmd.add_argument('--oid', '-o', default='.1.3.6.1.2.1.17.7.1.2.2.1.2', help='OID of the Switch')
        cmd.add_argument('--comment', '-c', help='Comment for Switch')
        ## >>>>>>> Network Command >>>>>>> update
        cmd = switch_args.add_parser('update', help='Update Switch')
        cmd.add_argument('name', help='Name of the Switch')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Switch')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> clone
        cmd = switch_args.add_parser('clone', help='Clone Switch')
        cmd.add_argument('name', help='Name of the Switch')
        cmd.add_argument('--network', '-N', metavar='N.N.N.N', help='Switchs')
        cmd.add_argument('--prefix', '-P', metavar='PP', type=int, help='Prefix')
        cmd.add_argument('--reserve', '-R', metavar='X.X.X.X', help='Reserve IP')
        cmd.add_argument('--release', metavar='X.X.X.X', help='Release IP')
        cmd.add_argument('--nshostname', help='Name server for zone file')
        cmd.add_argument('--nsipaddress', metavar='N.N.N.N', help='Name server\'s IP for zone file')
        cmd.add_argument('--include', action='store_true', help='Include data for zone file')
        cmd.add_argument('--rev_include', action='store_true', help='Include data for reverse zone file')
        cmd.add_argument('--comment', '-C', action='store_true', help='Add comment')
        ## >>>>>>> Network Command >>>>>>> rename
        cmd = switch_args.add_parser('rename', help='Rename Switch')
        cmd.add_argument('name', help='Name of the Switch')
        cmd.add_argument('--newname', '--nn', required=True, help='New name of the Switch')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = switch_args.add_parser('delete', help='Delete Switch')
        cmd.add_argument('name', help='Name of the Switch')
        ## >>>>>>> Network Commands Ends
        return parser


    def list_switch(self, args=None):
        """
        Method to list all switchs from Luna Configuration.
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


    def show_switch(self, args=None):
        """
        Method to show a switch in Luna Configuration.
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


    def add_switch(self, args=None):
        """
        Method to add new switch in Luna Configuration.
        """
        payload = {}
        if args['init']:
            payload['name'] = Inquiry().ask_text("Kindly provide Switch Name")
            payload['network'] = Inquiry().ask_text("Kindly provide Switch Network")
            payload['ipaddress'] = Inquiry().ask_text("Kindly provide Switch IP Address")
            payload['oid'] = Inquiry().ask_text("Kindly provide Switch OID")
            payload['read'] = Inquiry().ask_text("Kindly provide Read community")
            payload['rw'] = Inquiry().ask_text("Kindly provide Write community")
            comment = Inquiry().ask_confirm("Do you want to provide a comment?")
            if comment:
                payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)")
            fields, rows  = Helper().filter_data_col(self.table, payload)
            title = f'{self.table.capitalize()} Adding => {payload["name"]}'
            Presenter().show_table_col(title, fields, rows)
            confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
            if not confirm:
                Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
        else:
            error = False
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
            for key in payload:
                if payload[key] is None:
                    error = Helper().show_error(f'Kindly provide {key}.')
            if error:
                Helper().show_error(f'Adding {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            response = Rest().post_data(self.table, payload['name'], request_data)
            if response == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            elif response == 204:
                Helper().show_warning(f'{payload["name"]} present already.')
            else:
                Helper().show_error(f'{self.table.capitalize()}, {payload["name"]} is not created.')
        return True


    def delete_switch(self, args=None):
        """
        Method to delete a network in Luna Configuration.
        """
        return True


    def update_switch(self, args=None):
        """
        Method to update a network in Luna Configuration.
        """
        return True


    def rename_switch(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True


    def clone_switch(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        return True
