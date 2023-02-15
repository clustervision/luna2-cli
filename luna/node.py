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
        self.interface = "nodeinterface"
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
            
            elif self.args["action"] == "interfaces":
                self.list_interfaces(self.args)
            elif self.args["action"] == "interface":
                self.show_interface(self.args)
            elif self.args["action"] == "updateinterface":
                self.update_interface(self.args)
            elif self.args["action"] == "deleteinterface":
                self.delete_interface(self.args)
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
        cmd.add_argument('--interfaces', '-if', action='append', help='Node Interfaces interfacename|networkname|ipaddress|macaddress')
        cmd.add_argument('--comment', '-c', help='Comment for Node')
        ## >>>>>>> Node Command >>>>>>> update
        cmd = node_args.add_parser('update', help='Update Node')
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
        cmd.add_argument('--interfaces', '-if', action='append', help='Node Interfaces interfacename|networkname|ipaddress|macaddress')
        cmd.add_argument('--comment', '-c', help='Comment for Node')
        ## >>>>>>> Node Command >>>>>>> clone
        cmd = node_args.add_parser('clone', help='Clone Node')
        cmd.add_argument('--init', '-i', action='store_true', help='Node values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Node')
        cmd.add_argument('--newnodename', '-nn', help='New Name for the Node')
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
        cmd.add_argument('--interfaces', '-if', action='append', help='Node Interfaces interfacename|networkname|ipaddress|macaddress')
        cmd.add_argument('--comment', '-c', help='Comment for Node')
        ## >>>>>>> Node Command >>>>>>> rename
        cmd = node_args.add_parser('rename', help='Rename Node')
        cmd.add_argument('--init', '-i', action='store_true', help='Node values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Node')
        cmd.add_argument('--newnodename', '-nn', help='New Name for the Node')
        ## >>>>>>> Network Command >>>>>>> delete
        cmd = node_args.add_parser('delete', help='Delete Node')
        cmd.add_argument('--init', '-i', action='store_true', help='Node values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Node')
        ## >>>>>>> Node Commands Ends
        ## >>>>>>> Node Interface Command >>>>>>> interfaces
        cmd = node_args.add_parser('interfaces', help='List Node Interfaces')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Node Interface Command >>>>>>> interfaces
        cmd = node_args.add_parser('interface', help='Show Node Interface')
        cmd.add_argument('name', help='Name of the Node')
        cmd.add_argument('interface', help='Name of the Node Interface')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Network Interface Command >>>>>>> delete
        cmd = node_args.add_parser('updateinterface', help='Update Node Interface')
        cmd.add_argument('--init', '-i', action='store_true', help='Node values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Node')
        cmd.add_argument('--interface', '-if', action='append', help='Node Interface')
        cmd.add_argument('--network', '-N', action='append', help='Network Name')
        cmd.add_argument('--ipaddress', '-ip', action='append', help='IP Address')
        cmd.add_argument('--macaddress', '-m', action='append', help='MAC Address')
        ## >>>>>>> Network Interface Command >>>>>>> delete
        cmd = node_args.add_parser('deleteinterface', help='Delete Node Interface')
        cmd.add_argument('--init', '-i', action='store_true', help='Node values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the Node')
        cmd.add_argument('--interface', '-if', help='Name of the Node Interface')
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
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            if args['interfaces']:
                args['interfaces'] = Helper().list_to_dict(args['interfaces'])
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


    def update_node(self, args=None):
        """
        Method to update a node in Luna Configuration.
        """
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            if args['interfaces']:
                args['interfaces'] = Helper().list_to_dict(args['interfaces'])
            payload = args
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


    def rename_node(self, args=None):
        """
        Method to rename a node in Luna Configuration.
        """
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
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
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newnodename"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_node(self, args=None):
        """
        Method to delete a node in Luna Configuration.
        """
        abort = False
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide Node Name.')
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


    def clone_node(self, args=None):
        """
        Method to rename a node in Luna Configuration.
        """
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
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
                    if payload["newnodename"] in names:
                        Helper().show_error(f'{payload["newnodename"]} is already present in {self.table.capitalize()}.')
                    else:
                        response = Rest().post_clone(self.table, payload['name'], request_data)
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


    def list_interfaces(self, args=None):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_record(self.table, args['name']+'/interfaces')
        if get_list:
            data = get_list['config'][self.table][args["name"]]['interfaces']
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_interface(self.interface, data)
                response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{args["name"]} is not found in {self.table}.')
        return response


    def show_interface(self, args=None):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Helper().get_record(self.table, args['name']+'/interfaces/'+args['interface'])
        if get_list:
            data = get_list['config'][self.table][args["name"]]['interfaces'][0]
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_data_col(self.interface, data)
                title = f'{self.table.capitalize()} [{args["name"]}] => Interface {args["interface"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error(f'Interface {args["interface"]} not found in {self.table} {args["name"]} OR {args["name"]} is unavailable.')
        return response


    def update_interface(self, args=None):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            if len(args['interface']) == len(args['network']) == len(args['ipaddress']) == len(args['macaddress']):
                args['interfaces'] = []
                temp_dict = {}
                for ifc, nwk, ip, mac in zip(args['interface'], args['network'], args['ipaddress'], args['macaddress']):
                    temp_dict['interface'] = ifc
                    temp_dict['network'] = nwk
                    temp_dict['ipaddress'] = ip
                    temp_dict['macaddress'] = mac
                    args['interfaces'].append(temp_dict)
                    temp_dict = {}
                del args['interface']
                del args['network']
                del args['ipaddress']
                del args['macaddress']
            else:
                response = Helper().show_error('Each Interface should have Interface Name, Network, IP Address and MAC Address')
            payload = args
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
            response = Rest().post_data(self.table, node_name+'/interfaces', request_data)
            if response == 204:
                Helper().show_success(f'Interfaces updated in {self.table.capitalize()} {node_name}.')
            else:
                Helper().show_error(f'HTTP Error Code {response}.')
        else:
            Helper().show_error('Nothing to update.')
        return response


    def delete_interface(self, args=None):
        """
        Method to list a node interfaces in Luna Configuration.
        """
        abort = False
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide Node Name.')
            if payload['interface'] is None:
                abort = Helper().show_error('Kindly provide Interface Name.')
        if abort is False:
            response = Rest().get_delete(self.table, payload['name']+'/interfaces/'+payload['interface'])
            if response == 204:
                Helper().show_success(f'Interface {payload["interface"]} Deleted from {self.table.capitalize()} {payload["name"]}.')
            else:
                Helper().show_error(f'HTTP Error Code: {response}.')
        return response
