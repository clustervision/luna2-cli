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
from luna.utils.inquiry import Inquiry

from luna.utils.rest import Rest

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
        related to the BMC Setup class.
        """
        bmcsetup_menu = subparsers.add_parser('bmcsetup', help='BMC Setup operations.')
        bmcsetup_args = bmcsetup_menu.add_subparsers(dest='action')
        ## >>>>>>> BMC Setup Command >>>>>>> list
        cmd = bmcsetup_args.add_parser('list', help='List BMC Setups')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> BMC Setup Command >>>>>>> show
        cmd = bmcsetup_args.add_parser('show', help='Show BMC Setup')
        cmd.add_argument('name', help='Name of the BMC Setup')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> BMC Setup Command >>>>>>> add
        cmd = bmcsetup_args.add_parser('add', help='Add BMC Setup')
        cmd.add_argument('--init', '-i', action='store_true', help='BMC Setup values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the BMC Setup')
        cmd.add_argument('--userid', '-uid', type=int, help='UserID for BMC Setup')
        cmd.add_argument('--username', '-u', help='Username for BMC Setup')
        cmd.add_argument('--password', '-p', help='Password for BMC Setup')
        cmd.add_argument('--netchannel', '-nc', type=int, help='Net Channel for BMC Setup')
        cmd.add_argument('--mgmtchannel', '-mc', type=int, help='MGMT Channel for BMC Setup')
        cmd.add_argument('--unmanaged_bmc_users', '-ubu', help='Unmanaged BMC Users')
        cmd.add_argument('--comment', '-c', help='Comment for BMC Setup')
        ## >>>>>>> BMC Setup Command >>>>>>> update
        cmd = bmcsetup_args.add_parser('update', help='Update a BMC Setup')
        cmd.add_argument('--init', '-i', action='store_true', help='BMC Setup values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the BMC Setup')
        cmd.add_argument('--userid', '-uid', type=int, help='UserID for BMC Setup')
        cmd.add_argument('--username', '-u', help='Username for BMC Setup')
        cmd.add_argument('--password', '-p', help='Password for BMC Setup')
        cmd.add_argument('--netchannel', '-nc', type=int, help='Net Channel for BMC Setup')
        cmd.add_argument('--mgmtchannel', '-mc', type=int, help='MGMT Channel for BMC Setup')
        cmd.add_argument('--unmanaged_bmc_users', '-ubu', help='Unmanaged BMC Users')
        cmd.add_argument('--comment', '-c', help='Comment for BMC Setup')
        ## >>>>>>> BMC Setup Command >>>>>>> clone
        cmd = bmcsetup_args.add_parser('clone', help='Clone BMC Setup')
        cmd.add_argument('--init', '-i', action='store_true', help='BMC Setup values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the BMC Setup')
        cmd.add_argument('--userid', '-uid', type=int, help='UserID for BMC Setup')
        cmd.add_argument('--username', '-u', help='Username for BMC Setup')
        cmd.add_argument('--password', '-p', help='Password for BMC Setup')
        cmd.add_argument('--netchannel', '-nc', type=int, help='Net Channel for BMC Setup')
        cmd.add_argument('--mgmtchannel', '-mc', type=int, help='MGMT Channel for BMC Setup')
        cmd.add_argument('--unmanaged_bmc_users', '-ubu', help='Unmanaged BMC Users')
        cmd.add_argument('--comment', '-c', help='Comment for BMC Setup')
        ## >>>>>>> BMC Setup Command >>>>>>> rename
        cmd = bmcsetup_args.add_parser('rename', help='Rename BMC Setup')
        cmd.add_argument('--init', '-i', action='store_true', help='BMC Setup values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the BMC Setup')
        cmd.add_argument('--newbmcname', '-nn', help='New name of the BMC Setup')
        ## >>>>>>> BMC Setup Command >>>>>>> delete
        cmd = bmcsetup_args.add_parser('delete', help='Delete BMC Setup')
        cmd.add_argument('--init', '-i', action='store_true', help='BMC Setup values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the BMC Setup')
        ## >>>>>>> BMC Setup Commands Ends
        return parser


    def list_bmcsetup(self, args=None):
        """
        Method to list all bmc setups from
        Luna 2 Daemon.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_list(self.table)
        if get_list:
            data = get_list['config']['bmcsetup']
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data(self.table, data)
                response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{self.table} is not found.')
        return response


    def show_bmcsetup(self, args=None):
        """
        Method to show a bmc setup from
        Luna 2 Daemon.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_record(self.table, args['name'])
        if get_list:
            data = get_list['config']['bmcsetup'][args["name"]]
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.table, data)
                title = f'{self.table.capitalize()} => {args["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'{args["name"]} is not found in {self.table}.')
        return response


    def add_bmcsetup(self, args=None):
        """
        Method to add new bmc setup in Luna Configuration.
        """
        payload = {}
        if args['init']:
            payload['name'] = Inquiry().ask_text("Kindly provide BMC Name")
            payload['userid'] = Inquiry().ask_number("Kindly provide BMC User ID")
            payload['username'] = Inquiry().ask_text("Kindly provide BMC Username")
            payload['password'] = Inquiry().ask_secret("Kindly provide BMC Password")
            payload['netchannel'] = Inquiry().ask_number("Kindly provide NET Channel")
            payload['mgmtchannel'] = Inquiry().ask_number("Kindly provide MGMT Channel")
            payload['unmanaged_bmc_users'] = Inquiry().ask_text("Provide Unmanaged BMC Users")
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


    def update_bmcsetup(self, args=None):
        """
        Method to update a bmc setup in Luna Configuration.
        """
        payload = {}
        if args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update", names)
                payload['userid'] = Inquiry().ask_number("Update BMC User ID", True)
                payload['username'] = Inquiry().ask_text("Update BMC Username", True)
                payload['password'] = Inquiry().ask_secret("Update BMC Password", True)
                payload['netchannel'] = Inquiry().ask_number("Update NET Channel", True)
                payload['mgmtchannel'] = Inquiry().ask_number("Update MGMT Channel", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Update Unmanaged BMC Users", True)
                comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                if comment:
                    payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)", True)
                filtered = {k: v for k, v in payload.items() if v != ''}
                payload.clear()
                payload.update(filtered)
                if len(payload) != 1:
                    fields, rows  = Helper().filter_data_col(self.table, payload)
                    title = f'{self.table.capitalize()} Updating => {payload["name"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                    if not confirm:
                        Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
        if len(payload) != 1:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                if payload["name"] in names:
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def rename_bmcsetup(self, args=None):
        """
        Method to rename a bmc setup in Luna Configuration.
        """
        payload = {}
        if args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update", names)
                payload['newbmcname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newbmcname'] = None
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            error = False
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
            if payload['name'] is None:
                error = Helper().show_error('Kindly provide BMC Name.')
            if payload['newbmcname'] is None:
                error = Helper().show_error('Kindly provide New BMC Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newbmcname'] and payload['name']:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                if payload["name"] in names:
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newbmcname"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_bmcsetup(self, args=None):
        """
        Method to delete a bmc setup in Luna Configuration.
        """
        abort = False
        payload = {}
        if args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                payload['name'] = Inquiry().ask_select("Select BMC Setup to update", names)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Deleting => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    abort = Helper().show_error(f'Deletion of {payload["name"]}, {self.table.capitalize()} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide BMC Name.')
        if abort is False:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config']['bmcsetup'].keys())
                if payload["name"] in names:
                    response = Rest().get_delete(self.table, payload['name'])
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def clone_bmcsetup(self, args=None):
        """
        Method to rename a bmc setup in Luna Configuration.
        """
        print(args)
        return True
