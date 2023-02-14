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
from luna.utils.inquiry import Inquiry
from luna.utils.rest import Rest

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
            elif self.args["action"] == "clone":
                self.clone_network(self.args)
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
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Command >>>>>>> show
        cmd = network_args.add_parser('show', help='Show Network')
        cmd.add_argument('name', help='Name of the Network')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Command >>>>>>> add
        cmd = network_args.add_parser('add', help='Add Network')
        cmd.add_argument('--init', '-i', action='store_true', help='Network values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Network')
        cmd.add_argument('--network', '-N', help='Network')
        cmd.add_argument('--gateway', '-g', help='Gateway of the Network')
        cmd.add_argument('--ns_ip', '-ni', metavar='N.N.N.N', help='Name server IP Address of the Network')
        cmd.add_argument('--ns_hostname', '-nh', help='Name server Hostname of the Network')
        cmd.add_argument('--ntp_server', '-ntp', help='NTP Server of the Network')
        cmd.add_argument('--dhcp_range_begin', '-ds', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        cmd.add_argument('--dhcp_range_end', '-de', metavar='N.N.N.N', help='DHCP Range End for the Network')
        cmd.add_argument('--comment', '-c', help='Comment for Network')
        ## >>>>>>> Network Command >>>>>>> update
        cmd = network_args.add_parser('update', help='Update Network')
        cmd.add_argument('--init', '-i', action='store_true', help='Network values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Network')
        cmd.add_argument('--network', '-N', help='Network')
        cmd.add_argument('--gateway', '-g', help='Gateway of the Network')
        cmd.add_argument('--ns_ip', '-ni', metavar='N.N.N.N', help='Name server IP Address of the Network')
        cmd.add_argument('--ns_hostname', '-nh', help='Name server Hostname of the Network')
        cmd.add_argument('--ntp_server', '-ntp', help='NTP Server of the Network')
        cmd.add_argument('--dhcp', '-d', help='DHCP of the Network')
        cmd.add_argument('--dhcp_range_begin', '-ds', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        cmd.add_argument('--dhcp_range_end', '-de', metavar='N.N.N.N', help='DHCP Range End for the Network')
        cmd.add_argument('--comment', '-c', help='Comment for Network')
        ## >>>>>>> Network Command >>>>>>> clone
        cmd = network_args.add_parser('clone', help='Clone Network')
        cmd.add_argument('--init', '-i', action='store_true', help='Network values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Network')
        cmd.add_argument('--network', '-N', help='Network')
        cmd.add_argument('--gateway', '-g', help='Gateway of the Network')
        cmd.add_argument('--ns_ip', '-ni', metavar='N.N.N.N', help='Name server IP Address of the Network')
        cmd.add_argument('--ns_hostname', '-nh', help='Name server Hostname of the Network')
        cmd.add_argument('--ntp_server', '-ntp', help='NTP Server of the Network')
        cmd.add_argument('--dhcp', '-d', help='DHCP of the Network')
        cmd.add_argument('--dhcp_range_begin', '-ds', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        cmd.add_argument('--dhcp_range_end', '-de', metavar='N.N.N.N', help='DHCP Range End for the Network')
        cmd.add_argument('--comment', '-c', help='Comment for Network')
        ## >>>>>>> Network Command >>>>>>> rename
        cmd = network_args.add_parser('rename', help='Rename Network')
        cmd.add_argument('--init', '-i', action='store_true', help='Network values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Network')
        cmd.add_argument('--newnetname', '-nn', help='New name of the Network')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = network_args.add_parser('delete', help='Delete Network')
        cmd.add_argument('--init', '-i', action='store_true', help='Network values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Network')
        ## >>>>>>> Network Commands Ends
        return parser


    def list_network(self, args=None):
        """
        Method to list all networks from Luna Configuration.
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


    def show_network(self, args=None):
        """
        Method to show a network in Luna Configuration.
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


    def add_network(self, args=None):
        """
        Method to add new network in Luna Configuration.
        """
        payload = {}
        if args['init']:
            payload['name'] = Inquiry().ask_text("Kindly provide Network Name")
            payload['network'] = Inquiry().ask_text("Kindly provide Network")
            payload['gateway'] = Inquiry().ask_text("Kindly provide Gateway for the Network")
            payload['ns_ip'] = Inquiry().ask_text("Kindly provide Name Server IP Address")
            payload['ns_hostname'] = Inquiry().ask_text("Kindly provide Name Server Hostname")
            payload['ntp_server'] = Inquiry().ask_text("Kindly provide NTP Server")
            payload['dhcp'] = Inquiry().ask_confirm("DHCP is Enabled?")
            if payload['dhcp']:
                payload['dhcp_range_begin'] = Inquiry().ask_text("DHCP Range Starts From")
                payload['dhcp_range_end'] = Inquiry().ask_text("DHCP Range Ends To:")
            else:
                del payload['dhcp']
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
            if args['dhcp_range_begin'] and args['dhcp_range_end']:
                args['dhcp'] = True
            else:
                del args['dhcp_range_begin']
                del args['dhcp_range_end']
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


    def update_network(self, args=None):
        """
        Method to update a network in Luna Configuration.
        """
        payload = {}
        if args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Network to update", names)
                payload['network'] = Inquiry().ask_text("Kindly provide Network", True)
                payload['gateway'] = Inquiry().ask_text("Kindly provide Gateway for the Network", True)
                payload['ns_ip'] = Inquiry().ask_text("Kindly provide Name Server IP Address", True)
                payload['ns_hostname'] = Inquiry().ask_text("Kindly provide Name Server Hostname", True)
                payload['ntp_server'] = Inquiry().ask_text("Kindly provide NTP Server", True)
                payload['dhcp'] = Inquiry().ask_confirm("DHCP is Enabled?")
                if payload['dhcp']:
                    payload['dhcp_range_begin'] = Inquiry().ask_text("DHCP Range Starts From", True)
                    payload['dhcp_range_end'] = Inquiry().ask_text("DHCP Range Ends To:", True)
                else:
                    del payload['dhcp']
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
                    confirm = Inquiry().ask_confirm(f'update {payload["name"]} in {self.table.capitalize()}?')
                    if not confirm:
                        Helper().show_error(f'update {payload["name"]} into {self.table.capitalize()} Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            if args['dhcp_range_begin'] and args['dhcp_range_end']:
                args['dhcp'] = True
            else:
                del args['dhcp_range_begin']
                del args['dhcp_range_end']
            payload = args
            filtered = {k: v for k, v in payload.items() if v is not None}
            payload.clear()
            payload.update(filtered)
        if (len(payload) != 1) and ('name' in payload):
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error('Nothing to update.')
        return True


    def rename_network(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        payload = {}
        if args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Network to rename", names)
                payload['newnetname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Rename {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newnetname'] = None
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
                error = Helper().show_error('Kindly provide Network Name.')
            if payload['newnetname'] is None:
                error = Helper().show_error('Kindly provide New Network Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newnetname'] and payload['name']:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newnetname"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_network(self, args=None):
        """
        Method to delete a network in Luna Configuration.
        """
        abort = False
        payload = {}
        if args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Network to delete", names)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Deleting => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Delete {payload["name"]} from {self.table.capitalize()}?')
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
                abort = Helper().show_error('Kindly provide Network Name.')
        if abort is False:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    response = Rest().get_delete(self.table, payload['name'])
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def clone_network(self, args=None):
        """
        Method to rename a network in Luna Configuration.
        """
        payload = {}
        if args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Network to clone", names)
                payload['newnetname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['network'] = Inquiry().ask_text("Kindly provide Network", True)
                payload['gateway'] = Inquiry().ask_text("Kindly provide Gateway for the Network", True)
                payload['ns_ip'] = Inquiry().ask_text("Kindly provide Name Server IP Address", True)
                payload['ns_hostname'] = Inquiry().ask_text("Kindly provide Name Server Hostname", True)
                payload['ntp_server'] = Inquiry().ask_text("Kindly provide NTP Server", True)
                payload['dhcp'] = Inquiry().ask_confirm("DHCP is Enabled?")
                if payload['dhcp']:
                    payload['dhcp_range_begin'] = Inquiry().ask_text("DHCP Range Starts From", True)
                    payload['dhcp_range_end'] = Inquiry().ask_text("DHCP Range Ends To:", True)
                else:
                    del payload['dhcp']
                comment = Inquiry().ask_confirm("Do you want to provide a comment?")
                if comment:
                    payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)", True)
                get_record = Helper().get_record(self.table, payload['name'])
                if get_record:
                    data = get_record['config'][self.table][payload["name"]]
                    for key, value in payload.items():
                        if value == '' and key in data:
                            payload[key] = data[key]
                    filtered = {k: v for k, v in payload.items() if v is not None}
                    payload.clear()
                    payload.update(filtered)

                if len(payload) != 1:
                    fields, rows  = Helper().filter_data_col(self.table, payload)
                    title = f'{self.table.capitalize()} Cloning : {payload["name"]} => {payload["newnetname"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newnetname"]}?')
                    if not confirm:
                        Helper().show_error(f'Cloning of {payload["newnetname"]} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            if args['dhcp_range_begin'] and args['dhcp_range_end']:
                args['dhcp'] = True
            else:
                del args['dhcp_range_begin']
                del args['dhcp_range_end']
            payload = args
            get_record = Helper().get_record(self.table, payload['name'])
            if get_record:
                data = get_record['config'][self.table][payload["name"]]
                for key, value in payload.items():
                    if (value == '' or value is None) and key in data:
                        payload[key] = data[key]
                filtered = {k: v for k, v in payload.items() if v is not None}
                payload.clear()
                payload.update(filtered)
        if len(payload) != 1:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    if payload["newnetname"] in names:
                        Helper().show_error(f'{payload["newnetname"]} is already present in {self.table.capitalize()}.')
                    else:
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        if response == 201:
                            Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newnetname"]}.')
                        else:
                            Helper().show_error(f'HTTP Error {response}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True
