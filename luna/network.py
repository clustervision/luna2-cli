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
from luna.utils.log import Log

class Network(object):
    """
    Network Class responsible to show, list,
    add, remove information for the networks
    """

    def __init__(self, args=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "network"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] == "list":
                self.list_network()
            elif self.args["action"] == "show":
                self.show_network()
            elif self.args["action"] == "add":
                self.add_network()
            elif self.args["action"] == "update":
                self.update_network()
            elif self.args["action"] == "rename":
                self.rename_network()
            elif self.args["action"] == "delete":
                self.delete_network()
            elif self.args["action"] == "clone":
                self.clone_network()
            elif self.args["action"] == "ipinfo":
                self.ipinfo_network()
            elif self.args["action"] == "nextip":
                self.nextip_network()
            else:
                Helper().show_error("Not a valid option.")
        else:
            Helper().show_error("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Network class.
        """
        network_menu = subparsers.add_parser('network', help='Node operations.')
        network_args = network_menu.add_subparsers(dest='action')
        ## >>>>>>> Network Command >>>>>>> list
        network_list = network_args.add_parser('list', help='List Networks')
        network_list.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_list.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Command >>>>>>> show
        network_show = network_args.add_parser('show', help='Show Network')
        network_show.add_argument('name', help='Name of the Network')
        network_show.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_show.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Command >>>>>>> add
        network_add = network_args.add_parser('add', help='Add Network')
        network_add.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_add.add_argument('-i', '--init', action='store_true', help='Network Interactive Mode')
        network_add.add_argument('-n', '--name', help='Name of the Network')
        network_add.add_argument('-N', '--network', help='Network')
        network_add.add_argument('-g', '--gateway', help='Gateway of the Network')
        network_add.add_argument('-ni', '--ns_ip', metavar='N.N.N.N', help='Name server IP Address of the Network')
        network_add.add_argument('-nh', '--ns_hostname', help='Name server Hostname of the Network')
        network_add.add_argument('-ntp', '--ntp_server', help='NTP Server of the Network')
        network_add.add_argument('-ds', '--dhcp_range_begin', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        network_add.add_argument('-de', '--dhcp_range_end', metavar='N.N.N.N', help='DHCP Range End for the Network')
        network_add.add_argument('-c', '--comment', help='Comment for Network')
        ## >>>>>>> Network Command >>>>>>> update
        network_update = network_args.add_parser('update', help='Update Network')
        network_update.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_update.add_argument('-i', '--init', action='store_true', help='Network Interactive Mode')
        network_update.add_argument('-n', '--name', help='Name of the Network')
        network_update.add_argument('-N', '--network', help='Network')
        network_update.add_argument('-g', '--gateway', help='Gateway of the Network')
        network_update.add_argument('-ni', '--ns_ip', metavar='N.N.N.N', help='Name server IP Address of the Network')
        network_update.add_argument('-nh', '--ns_hostname', help='Name server Hostname of the Network')
        network_update.add_argument('-ntp', '--ntp_server', help='NTP Server of the Network')
        network_update.add_argument('-dh', '--dhcp', help='DHCP of the Network')
        network_update.add_argument('-ds', '--dhcp_range_begin', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        network_update.add_argument('-de', '--dhcp_range_end', metavar='N.N.N.N', help='DHCP Range End for the Network')
        network_update.add_argument('-c', '--comment', help='Comment for Network')
        ## >>>>>>> Network Command >>>>>>> clone
        network_clone = network_args.add_parser('clone', help='Clone Network')
        network_clone.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_clone.add_argument('-i', '--init', action='store_true', help='Network Interactive Mode')
        network_clone.add_argument('-n', '--name', help='Name of the Network')
        network_clone.add_argument('-nn', '--newnetname', help='New name of the Network')
        network_clone.add_argument('-N', '--network', help='Network')
        network_clone.add_argument('-g', '--gateway', help='Gateway of the Network')
        network_clone.add_argument('-ni', '--ns_ip', metavar='N.N.N.N', help='Name server IP Address of the Network')
        network_clone.add_argument('-nh', '--ns_hostname', help='Name server Hostname of the Network')
        network_clone.add_argument('-ntp', '--ntp_server', help='NTP Server of the Network')
        network_clone.add_argument('-dh', '--dhcp', help='DHCP of the Network')
        network_clone.add_argument('-ds', '--dhcp_range_begin', metavar='N.N.N.N', help='DHCP Range Start for the Network')
        network_clone.add_argument('-de', '--dhcp_range_end', metavar='N.N.N.N', help='DHCP Range End for the Network')
        network_clone.add_argument('-c', '--comment', help='Comment for Network')
        ## >>>>>>> Network Command >>>>>>> rename
        network_rename = network_args.add_parser('rename', help='Rename Network')
        network_rename.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_rename.add_argument('-i', '--init', action='store_true', help='Network Interactive Mode')
        network_rename.add_argument('-n', '--name', help='Name of the Network')
        network_rename.add_argument('-nn', '--newnetname', help='New name of the Network')
        ## >>>>>>> Network Command >>>>>>> delete
        network_delete = network_args.add_parser('delete', help='Delete Network')
        network_delete.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_delete.add_argument('-i', '--init', action='store_true', help='Network Interactive Mode')
        network_delete.add_argument('-n', '--name', help='Name of the Network')
        ## >>>>>>> Network Command >>>>>>> ipinfo
        network_ipinfo = network_args.add_parser('ipinfo', help='Show Network IP Information')
        network_ipinfo.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_ipinfo.add_argument('name', help='Name of the Network')
        network_ipinfo.add_argument('ipaddress', help='IP Address from the Network')
        ## >>>>>>> Network Command >>>>>>> nextip
        network_nextip = network_args.add_parser('nextip', help='Show Next Available IP Address on the Network')
        network_nextip.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        network_nextip.add_argument('name', help='Name of the Network')
        ## >>>>>>> Network Commands Ends
        return parser


    def list_network(self):
        """
        Method to list all networks from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_network(self):
        """
        Method to add new network in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            if self.args['dhcp_range_begin'] and self.args['dhcp_range_end']:
                self.args['dhcp'] = True
            else:
                del self.args['dhcp_range_begin']
                del self.args['dhcp_range_end']
            payload = self.args
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
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            elif response == 204:
                Helper().show_warning(f'{payload["name"]} present already.')
            else:
                Helper().show_error(f'{self.table.capitalize()}, {payload["name"]} is not created.')
        return True


    def update_network(self):
        """
        Method to update a network in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            if self.args['dhcp_range_begin'] and self.args['dhcp_range_end']:
                self.args['dhcp'] = True
            else:
                del self.args['dhcp_range_begin']
                del self.args['dhcp_range_end']
            payload = self.args
            filtered = {k: v for k, v in payload.items() if v is not None}
            payload.clear()
            payload.update(filtered)
        if (len(payload) != 1) and ('name' in payload):
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error('Nothing to update.')
        return True


    def rename_network(self):
        """
        Method to rename a network in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            payload = self.args
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
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newnetname"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_network(self):
        """
        Method to delete a network in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            payload = self.args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide Network Name.')
        if abort is False:
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {payload}')
                    response = Rest().get_delete(self.table, payload['name'])
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def clone_network(self):
        """
        Method to rename a network in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
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
                get_record = Rest().get_data(self.table, payload['name'])
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            if self.args['dhcp_range_begin'] and self.args['dhcp_range_end']:
                self.args['dhcp'] = True
            else:
                del self.args['dhcp_range_begin']
                del self.args['dhcp_range_end']
            payload = self.args
            get_record = Rest().get_data(self.table, payload['name'])
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
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    if payload["newnetname"] in names:
                        Helper().show_error(f'{payload["newnetname"]} is already present in {self.table.capitalize()}.')
                    else:
                        self.logger.debug(f'Payload => {request_data}')
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        self.logger.debug(f'Response => {response}')
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


    def ipinfo_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        response = False
        uri = f'{self.args["name"]}/{self.args["ipaddress"]}'
        self.logger.debug(f'IPinfo URI => {uri}')
        ipinfo = Rest().get_data(self.table, uri)
        self.logger.debug(f'IPinfo Response => {ipinfo}')
        if ipinfo:
            status = ipinfo['config']['network'][self.args["ipaddress"]]['status']
            if 'free' in status:
                response = Helper().show_success(f'{self.args["ipaddress"]} is {status.capitalize()}.')
            else:
                response = Helper().show_warning(f'{self.args["ipaddress"]} is {status.capitalize()}.')
        return response


    def nextip_network(self):
        """
        Method to show a network in Luna Configuration.
        """
        response = False
        uri = f'{self.args["name"]}/_nextfreeip'
        self.logger.debug(f'NextIP URI => {uri}')
        nextip = Rest().get_data(self.table, uri)
        self.logger.debug(f'NextIP Response => {nextip}')
        if nextip:
            ipaddr = nextip['config']['network'][self.args["name"]]['nextip']
            if ipaddr:
                response = Helper().show_success(f'Next Available IP Address is {ipaddr}.')
            else:
                response = Helper().show_warning(f'No More IP Address available on network {self.args["ipaddress"]}.')
        return response
