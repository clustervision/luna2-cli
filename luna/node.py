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
from luna.utils.log import Log

class Node(object):
    """
    Node Class responsible to show, list,
    add, remove information for the Node
    """

    def __init__(self, args=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "node"
        self.interface = "nodeinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] == "list":
                self.list_node()
            elif self.args["action"] == "show":
                self.show_node()
            elif self.args["action"] == "add":
                self.add_node()
            elif self.args["action"] == "update":
                self.update_node()
            elif self.args["action"] == "rename":
                self.rename_node()
            elif self.args["action"] == "delete":
                self.delete_node()
            elif self.args["action"] == "clone":
                self.clone_node()
            
            elif self.args["action"] == "interfaces":
                self.list_interfaces()
            elif self.args["action"] == "interface":
                self.show_interface()
            elif self.args["action"] == "updateinterface":
                self.update_interface()
            elif self.args["action"] == "deleteinterface":
                self.delete_interface()
            else:
                Helper().show_error("Not a valid option.")
        else:
            Helper().show_error("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Node class.
        """
        node_menu = subparsers.add_parser('node', help='Node operations.')
        node_args = node_menu.add_subparsers(dest='action')
        ## >>>>>>> Node Command >>>>>>> list
        cmd = node_args.add_parser('list', help='List Node')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Node Command >>>>>>> show
        cmd = node_args.add_parser('show', help='Show Node')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Node Command >>>>>>> add
        cmd = node_args.add_parser('add', help='Add Node')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Node values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Node')
        cmd.add_argument('-host', '--hostname',help='Hostname')
        cmd.add_argument('-g', '--group', help='Group Name')
        cmd.add_argument('-lb', '--localboot', help='Local Boot')
        cmd.add_argument('-m', '--macaddr', help='MAC Address')
        cmd.add_argument('-o', '--osimage', help='OS Image Name')
        cmd.add_argument('-sw', '--switch', help='Switch Name')
        cmd.add_argument('-sp', '--switchport', help='Switch Port')
        cmd.add_argument('-ser', '--service', action='store_true', help='Service')
        cmd.add_argument('-b', '--setupbmc', action='store_true', help='BMC Setup')
        cmd.add_argument('-s', '--status', help='Status')
        cmd.add_argument('-pre', '--prescript', help='Pre Script')
        cmd.add_argument('-part', '--partscript', help='Part Script')
        cmd.add_argument('-post', '--postscript', help='Post Script')
        cmd.add_argument('-nb', '--netboot', help='Network Boot')
        cmd.add_argument('-li', '--localinstall', help='Local Install')
        cmd.add_argument('-bm', '--bootmenu', help='Boot Menu')
        cmd.add_argument('-pi', '--provision_interface', help='Provision Interface')
        cmd.add_argument('-pm', '--provision_method', help='Provision Method')
        cmd.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        cmd.add_argument('-tid', '--tpm_uuid', action='store_true', help='TPM UUID')
        cmd.add_argument('-tkey', '--tpm_pubkey', help='TPM Public Key')
        cmd.add_argument('-tsha', '--tpm_sha256', help='TPM SHA256')
        cmd.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        cmd.add_argument('-if', '--interfaces', action='append', help='Node Interfaces interfacename|networkname|ipaddress|macaddress')
        cmd.add_argument('-c', '--comment', help='Comment for Node')
        ## >>>>>>> Node Command >>>>>>> update
        cmd = node_args.add_parser('update', help='Update Node')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Node values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Node')
        cmd.add_argument('-host', '--hostname',help='Hostname')
        cmd.add_argument('-g', '--group', help='Group Name')
        cmd.add_argument('-lb', '--localboot', help='Local Boot')
        cmd.add_argument('-m', '--macaddr', help='MAC Address')
        cmd.add_argument('-o', '--osimage', help='OS Image Name')
        cmd.add_argument('-sw', '--switch', help='Switch Name')
        cmd.add_argument('-sp', '--switchport', help='Switch Port')
        cmd.add_argument('-ser', '--service', action='store_true', help='Service')
        cmd.add_argument('-b', '--setupbmc', action='store_true', help='BMC Setup')
        cmd.add_argument('-s', '--status', help='Status')
        cmd.add_argument('-pre', '--prescript', help='Pre Script')
        cmd.add_argument('-part', '--partscript', help='Part Script')
        cmd.add_argument('-post', '--postscript', help='Post Script')
        cmd.add_argument('-nb', '--netboot', help='Network Boot')
        cmd.add_argument('-li', '--localinstall', help='Local Install')
        cmd.add_argument('-bm', '--bootmenu', help='Boot Menu')
        cmd.add_argument('-pi', '--provision_interface', help='Provision Interface')
        cmd.add_argument('-pm', '--provision_method', help='Provision Method')
        cmd.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        cmd.add_argument('-tid', '--tpm_uuid', action='store_true', help='TPM UUID')
        cmd.add_argument('-tkey', '--tpm_pubkey', help='TPM Public Key')
        cmd.add_argument('-tsha', '--tpm_sha256', help='TPM SHA256')
        cmd.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        cmd.add_argument('-if', '--interfaces', action='append', help='Node Interfaces interfacename|networkname|ipaddress|macaddress')
        cmd.add_argument('-c', '--comment', help='Comment for Node')
        ## >>>>>>> Node Command >>>>>>> clone
        cmd = node_args.add_parser('clone', help='Clone Node')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Node values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Node')
        cmd.add_argument('-nn', '--newnodename', help='New Name for the Node')
        cmd.add_argument('-host', '--hostname',help='Hostname')
        cmd.add_argument('-g', '--group', help='Group Name')
        cmd.add_argument('-lb', '--localboot', help='Local Boot')
        cmd.add_argument('-m', '--macaddr', help='MAC Address')
        cmd.add_argument('-o', '--osimage', help='OS Image Name')
        cmd.add_argument('-sw', '--switch', help='Switch Name')
        cmd.add_argument('-sp', '--switchport', help='Switch Port')
        cmd.add_argument('-ser', '--service', action='store_true', help='Service')
        cmd.add_argument('-b', '--setupbmc', action='store_true', help='BMC Setup')
        cmd.add_argument('-s', '--status', help='Status')
        cmd.add_argument('-pre', '--prescript', help='Pre Script')
        cmd.add_argument('-part', '--partscript', help='Part Script')
        cmd.add_argument('-post', '--postscript', help='Post Script')
        cmd.add_argument('-nb', '--netboot', help='Network Boot')
        cmd.add_argument('-li', '--localinstall', help='Local Install')
        cmd.add_argument('-bm', '--bootmenu', help='Boot Menu')
        cmd.add_argument('-pi', '--provision_interface', help='Provision Interface')
        cmd.add_argument('-pm', '--provision_method', help='Provision Method')
        cmd.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        cmd.add_argument('-tid', '--tpm_uuid', action='store_true', help='TPM UUID')
        cmd.add_argument('-tkey', '--tpm_pubkey', help='TPM Public Key')
        cmd.add_argument('-tsha', '--tpm_sha256', help='TPM SHA256')
        cmd.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        cmd.add_argument('-if', '--interfaces', action='append', help='Node Interfaces interfacename|networkname|ipaddress|macaddress')
        cmd.add_argument('-c', '--comment', help='Comment for Node')
        ## >>>>>>> Node Command >>>>>>> rename
        cmd = node_args.add_parser('rename', help='Rename Node')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Node values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Node')
        cmd.add_argument('-nn', '--newnodename', help='New Name for the Node')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = node_args.add_parser('delete', help='Delete Node')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Node values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Node')
        ## >>>>>>> Node Commands Ends
        ## >>>>>>> Node Interface Command >>>>>>> interfaces
        cmd = node_args.add_parser('interfaces', help='List Node Interfaces')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Node Interface Command >>>>>>> interfaces
        cmd = node_args.add_parser('interface', help='Show Node Interface')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('interface', help='Name of the Node Interface')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Interface Command >>>>>>> delete
        cmd = node_args.add_parser('updateinterface', help='Update Node Interface')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Node values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Node')
        cmd.add_argument('-if', '--interface', action='append', help='Node Interface')
        cmd.add_argument('-N', '--network', action='append', help='Network Name')
        cmd.add_argument('-ip', '--ipaddress', action='append', help='IP Address')
        cmd.add_argument('-m', '--macaddress', action='append', help='MAC Address')
        ## >>>>>>> Network Interface Command >>>>>>> delete
        cmd = node_args.add_parser('deleteinterface', help='Delete Node Interface')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Node values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Node')
        cmd.add_argument('-if', '--interface', help='Name of the Node Interface')
        return parser


    def list_node(self):
        """
        Method to list all nodes from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_list(self.table)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][self.table]
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data(self.table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{self.table} is not found.')
        return response


    def show_node(self):
        """
        Method to show a node in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_record(self.table, self.args['name'])
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table.capitalize()} => {self.args["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return response


    def add_node(self):
        """
        Method to add new node in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            payload['name'] = Inquiry().ask_text("Write Name Of Node")
            payload['hostname'] = Inquiry().ask_text("Node's Hostname")
            payload['group'] = Inquiry().ask_text("Group Name")
            payload['localboot'] = Inquiry().ask_text("Local Boot")
            payload['macaddr'] = Inquiry().ask_text("MAC Address")
            payload['osimage'] = Inquiry().ask_text("OS Image")
            payload['switch'] = Inquiry().ask_text("Write Switch Name")
            payload['switchport'] = Inquiry().ask_text("Write Switch Port")
            payload['service'] = Inquiry().ask_text("Service")
            payload['setupbmc'] = Inquiry().ask_text("Setup BMC")
            payload['status'] = Inquiry().ask_text("Status")
            payload['prescript'] = Inquiry().ask_text("Pre-Script")
            payload['partscript'] = Inquiry().ask_text("Part-Script")
            payload['postscript'] = Inquiry().ask_text("Post-Script")
            payload['netboot'] = Inquiry().ask_text("Network Boot")
            payload['localinstall'] = Inquiry().ask_text("Local Install")
            payload['bootmenu'] = Inquiry().ask_text("Boot Menu")
            payload['provision_interface'] = Inquiry().ask_text("Provision Interface")
            payload['provision_method'] = Inquiry().ask_text("Provision Method")
            payload['provision_fallback'] = Inquiry().ask_text("Provision Fallback")
            payload['tpm_uuid'] = Inquiry().ask_text("TPM UUID")
            payload['tpm_pubkey'] = Inquiry().ask_text("TPM Public Key")
            payload['tpm_sha256'] = Inquiry().ask_text("TPM SHA-256")
            payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users")
            def interfaces(interfc):
                if len(interfc):
                    confirm_text = "Add one more Interface?"
                else:
                    confirm_text = "Add Interface?"
                ifc = Inquiry().ask_confirm(confirm_text)
                if ifc:
                    interface_name = Inquiry().ask_text("Write Interface Name")
                    interface_ip = Inquiry().ask_text("Write Interface IP Address")
                    interface_mac = Inquiry().ask_text("Write Interface MAC Address")
                    networkn_name = Inquiry().ask_text("Write Interface Network Name")
                    if interface_name and interface_ip and interface_mac and networkn_name:
                        interfc.append({
                            'interface': interface_name,
                            'ipaddress': interface_ip,
                            'macaddress': interface_mac,
                            'network': networkn_name})
                    return interfaces(interfc)
                else:
                    return interfc
            interfc = []
            payload['interfaces'] = interfaces(interfc)
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
            if self.args['interfaces']:
                self.args['interfaces'] = Helper().list_to_dict(self.args['interfaces'])
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


    def update_node(self):
        """
        Method to update a node in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Node", names)
                payload['hostname'] = Inquiry().ask_text("Node's Hostname", True)
                payload['group'] = Inquiry().ask_text("Group Name", True)
                payload['localboot'] = Inquiry().ask_text("Local Boot", True)
                payload['macaddr'] = Inquiry().ask_text("MAC Address", True)
                payload['osimage'] = Inquiry().ask_text("OS Image", True)
                payload['switch'] = Inquiry().ask_text("Write Switch Name", True)
                payload['switchport'] = Inquiry().ask_text("Write Switch Port", True)
                payload['service'] = Inquiry().ask_text("Service", True)
                payload['setupbmc'] = Inquiry().ask_text("Setup BMC", True)
                payload['status'] = Inquiry().ask_text("Status", True)
                payload['prescript'] = Inquiry().ask_text("Pre-Script", True)
                payload['partscript'] = Inquiry().ask_text("Part-Script", True)
                payload['postscript'] = Inquiry().ask_text("Post-Script", True)
                payload['netboot'] = Inquiry().ask_text("Network Boot", True)
                payload['localinstall'] = Inquiry().ask_text("Local Install", True)
                payload['bootmenu'] = Inquiry().ask_text("Boot Menu", True)
                payload['provision_interface'] = Inquiry().ask_text("Provision Interface", True)
                payload['provision_method'] = Inquiry().ask_text("Provision Method", True)
                payload['provision_fallback'] = Inquiry().ask_text("Provision Fallback", True)
                payload['tpm_uuid'] = Inquiry().ask_text("TPM UUID", True)
                payload['tpm_pubkey'] = Inquiry().ask_text("TPM Public Key", True)
                payload['tpm_sha256'] = Inquiry().ask_text("TPM SHA-256", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users", True)
                def interfaces(interfc):
                    if len(interfc):
                        confirm_text = "Add one more Interface?"
                    else:
                        confirm_text = "Add Interface?"
                    ifc = Inquiry().ask_confirm(confirm_text)
                    if ifc:
                        interface_name = Inquiry().ask_text("Write Interface Name")
                        interface_ip = Inquiry().ask_text("Write Interface IP Address")
                        interface_mac = Inquiry().ask_text("Write Interface MAC Address")
                        networkn_name = Inquiry().ask_text("Write Interface Network Name")
                        if interface_name and interface_ip and interface_mac and networkn_name:
                            interfc.append({
                                'interface': interface_name,
                                'ipaddress': interface_ip,
                                'macaddress': interface_mac,
                                'network': networkn_name})
                        return interfaces(interfc)
                    else:
                        return interfc
                interfc = []
                payload['interfaces'] = interfaces(interfc)
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
            if self.args['interfaces']:
                self.args['interfaces'] = Helper().list_to_dict(self.args['interfaces'])
            payload = self.args
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


    def rename_node(self):
        """
        Method to rename a node in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Node to rename", names)
                payload['newnodename'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Rename {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newnodename'] = None
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
                error = Helper().show_error('Kindly provide Node Name.')
            if payload['newnodename'] is None:
                error = Helper().show_error('Kindly provide New Node Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newnodename'] and payload['name']:
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][payload['name']] = payload
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newnodename"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_node(self):
        """
        Method to delete a node in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Node to delete", names)
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
                abort = Helper().show_error('Kindly provide Node Name.')
        if abort is False:
            get_list = Helper().get_list(self.table)
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


    def clone_node(self):
        """
        Method to rename a node in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Node", names)
                payload['newnodename'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['hostname'] = Inquiry().ask_text("Node's Hostname", True)
                payload['group'] = Inquiry().ask_text("Group Name", True)
                payload['localboot'] = Inquiry().ask_text("Local Boot", True)
                payload['macaddr'] = Inquiry().ask_text("MAC Address", True)
                payload['osimage'] = Inquiry().ask_text("OS Image", True)
                payload['switch'] = Inquiry().ask_text("Write Switch Name", True)
                payload['switchport'] = Inquiry().ask_text("Write Switch Port", True)
                payload['service'] = Inquiry().ask_text("Service", True)
                payload['setupbmc'] = Inquiry().ask_text("Setup BMC", True)
                payload['status'] = Inquiry().ask_text("Status", True)
                payload['prescript'] = Inquiry().ask_text("Pre-Script", True)
                payload['partscript'] = Inquiry().ask_text("Part-Script", True)
                payload['postscript'] = Inquiry().ask_text("Post-Script", True)
                payload['netboot'] = Inquiry().ask_text("Network Boot", True)
                payload['localinstall'] = Inquiry().ask_text("Local Install", True)
                payload['bootmenu'] = Inquiry().ask_text("Boot Menu", True)
                payload['provision_interface'] = Inquiry().ask_text("Provision Interface", True)
                payload['provision_method'] = Inquiry().ask_text("Provision Method", True)
                payload['provision_fallback'] = Inquiry().ask_text("Provision Fallback", True)
                payload['tpm_uuid'] = Inquiry().ask_text("TPM UUID", True)
                payload['tpm_pubkey'] = Inquiry().ask_text("TPM Public Key", True)
                payload['tpm_sha256'] = Inquiry().ask_text("TPM SHA-256", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users", True)
                def interfaces(interfc):
                    if len(interfc):
                        confirm_text = "Add one more Interface?"
                    else:
                        confirm_text = "Add Interface?"
                    ifc = Inquiry().ask_confirm(confirm_text)
                    if ifc:
                        interface_name = Inquiry().ask_text("Write Interface Name")
                        interface_ip = Inquiry().ask_text("Write Interface IP Address")
                        interface_mac = Inquiry().ask_text("Write Interface MAC Address")
                        networkn_name = Inquiry().ask_text("Write Interface Network Name")
                        if interface_name and interface_ip and interface_mac and networkn_name:
                            interfc.append({
                                'interface': interface_name,
                                'ipaddress': interface_ip,
                                'macaddress': interface_mac,
                                'network': networkn_name})
                        return interfaces(interfc)
                    else:
                        return interfc
                interfc = []
                payload['interfaces'] = interfaces(interfc)
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
                    title = f'{self.table.capitalize()} Cloning : {payload["name"]} => {payload["newgroupname"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newgroupname"]}?')
                    if not confirm:
                        Helper().show_error(f'Cloning of {payload["newgroupname"]} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            payload = self.args
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
                    if payload["newnodename"] in names:
                        Helper().show_error(f'{payload["newnodename"]} is already present in {self.table.capitalize()}.')
                    else:
                        self.logger.debug(f'Payload => {request_data}')
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        self.logger.debug(f'Response => {response}')
                        if response == 201:
                            Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newnodename"]}.')
                        else:
                            Helper().show_error(f'HTTP Error {response}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def list_interfaces(self):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces')
        get_list = Helper().get_record(self.table, self.args['name']+'/interfaces')
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces']
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_interface(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return response


    def show_interface(self):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces{self.args["interface"]}')
        get_list = Helper().get_record(self.table, self.args['name']+'/interfaces/'+self.args['interface'])
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces'][0]
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{self.table.capitalize()} [{self.args["name"]}] => Interface {self.args["interface"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'Interface {self.args["interface"]} not found in {self.table} {self.args["name"]} OR {self.args["name"]} is unavailable.')
        return response


    def update_interface(self):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Node", names)
                def interfaces(interfc):
                    if len(interfc):
                        confirm_text = "Add one more Interface?"
                    else:
                        confirm_text = "Add Interface?"
                    ifc = Inquiry().ask_confirm(confirm_text)
                    if ifc:
                        interface_name = Inquiry().ask_text("Write Interface Name")
                        interface_ip = Inquiry().ask_text("Write Interface IP Address")
                        interface_mac = Inquiry().ask_text("Write Interface MAC Address")
                        networkn_name = Inquiry().ask_text("Write Interface Network Name")
                        if interface_name and interface_ip and interface_mac and networkn_name:
                            interfc.append({
                                'interface': interface_name,
                                'ipaddress': interface_ip,
                                'macaddress': interface_mac,
                                'network': networkn_name})
                        return interfaces(interfc)
                    else:
                        return interfc
                interfc = []
                payload['interfaces'] = interfaces(interfc)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Updating => {payload["name"]} Interfaces'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'update Interfaces in {self.table.capitalize()} {payload["name"]}?')
                if not confirm:
                    Helper().show_error(f'update Interfaces in {self.table.capitalize()} {payload["name"]} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            if len(self.args['interface']) == len(self.args['network']) == len(self.args['ipaddress']) == len(self.args['macaddress']):
                self.args['interfaces'] = []
                temp_dict = {}
                for ifc, nwk, ip, mac in zip(self.args['interface'], self.args['network'], self.args['ipaddress'], self.args['macaddress']):
                    temp_dict['interface'] = ifc
                    temp_dict['network'] = nwk
                    temp_dict['ipaddress'] = ip
                    temp_dict['macaddress'] = mac
                    self.args['interfaces'].append(temp_dict)
                    temp_dict = {}
                del self.args['interface']
                del self.args['network']
                del self.args['ipaddress']
                del self.args['macaddress']
            else:
                response = Helper().show_error('Each Interface should have Interface Name, Network, IP Address and MAC Address')
            payload = self.args
            filtered = {k: v for k, v in payload.items() if v is not None}
            payload.clear()
            payload.update(filtered)
        if (len(payload) != 1) and ('name' in payload):
            node_name = payload['name']
            del payload['name']
            request_data = {}
            request_data['config'] = {}
            request_data['config'][self.table] = {}
            request_data['config'][self.table][node_name] = payload
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, node_name+'/interfaces', request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'Interfaces updated in {self.table.capitalize()} {node_name}.')
            else:
                Helper().show_error(f'HTTP Error Code {response}.')
        else:
            Helper().show_error('Nothing to update.')
        return response


    def delete_interface(self):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Node to delete Interface", names)
                record = Helper().get_record(self.table, payload['name'])
                all_interface = record['config'][self.table][payload['name']]['interfaces']
                ifc_list = []
                for ifc in all_interface:
                    ifc_list.append(ifc['interface'])
                payload['interface'] = Inquiry().ask_select("Select Interface to delete", ifc_list)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Deleting Interface [{payload["interface"]}] => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Delete Interface {payload["interface"]} from {self.table.capitalize()} {payload["name"]}?')
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
                abort = Helper().show_error('Kindly provide Node Name.')
            if payload['interface'] is None:
                abort = Helper().show_error('Kindly provide Interface Name.')
        if abort is False:
            self.logger.debug(f'Payload => {payload}')
            response = Rest().get_delete(self.table, payload['name']+'/interfaces/'+payload['interface'])
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'Interface {payload["interface"]} Deleted from {self.table.capitalize()} {payload["name"]}.')
            else:
                Helper().show_error(f'HTTP Error Code: {response}.')
        return response
