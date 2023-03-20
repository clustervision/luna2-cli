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

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.inquiry import Inquiry
from luna.utils.rest import Rest
from luna.utils.log import Log

class Group():
    """
    Group Class responsible to show, list,
    add, remove information for the Group
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "group"
        self.interface = "groupinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in ["update", "rename", "delete", "clone"]:
                self.get_list = Rest().get_data(self.table)
            if self.args["action"] in ["list", "show", "add", "update", "rename", "delete", "clone"]:
                call = methodcaller(f'{self.args["action"]}_group')
                call(self)
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
        if parser and subparsers:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Group class.
        """
        group_menu = subparsers.add_parser('group', help='Group operations')
        group_args = group_menu.add_subparsers(dest='action')
        group_list = group_args.add_parser('list', help='List Groups')
        Helper().common_list_args(group_list)
        group_show = group_args.add_parser('show', help='Show Group')
        group_show.add_argument('name', help='Name of the Group')
        Helper().common_list_args(group_show)
        group_add = group_args.add_parser('add', help='Add Group')
        Helper().common_add_args(group_add, 'Group')
        Helper().common_group_node_args(group_add)
        group_add.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_add.add_argument('-D', '--domain', help='Domain Name')
        group_update = group_args.add_parser('update', help='Update Group')
        Helper().common_add_args(group_update, 'Group')
        Helper().common_group_node_args(group_update)
        group_update.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_update.add_argument('-D', '--domain', help='Domain Name')
        group_clone = group_args.add_parser('clone', help='Clone Group.')
        Helper().common_add_args(group_clone, 'Group')
        Helper().common_group_node_args(group_clone)
        group_clone.add_argument('-nn', '--newgroupname', help='New Name for the Group')
        group_clone.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        group_clone.add_argument('-D', '--domain', help='Domain Name')
        group_rename = group_args.add_parser('rename', help='Rename Group.')
        Helper().common_add_args(group_rename, 'Group')
        group_rename.add_argument('-nn', '--newgroupname', help='New Name for the Group')
        group_delete = group_args.add_parser('delete', help='Delete Group')
        Helper().common_add_args(group_delete, 'Group')
        group_interfaces = group_args.add_parser('interfaces', help='List Group Interfaces')
        group_interfaces.add_argument('name', help='Name of the Group')
        Helper().common_list_args(group_interfaces)
        group_interface = group_args.add_parser('interface', help='Show Group Interface')
        group_interface.add_argument('name', help='Name of the Group')
        group_interface.add_argument('interface', help='Name of the Group Interface')
        Helper().common_list_args(group_interface)
        group_updateinterface = group_args.add_parser('updateinterface', help='Update Group Interface')
        Helper().common_add_args(group_updateinterface, 'Group')
        group_updateinterface.add_argument('-if', '--interface', action='append', help='Group Interface')
        group_updateinterface.add_argument('-N', '--network', action='append', help='Network Name')
        group_deleteinterface = group_args.add_parser('deleteinterface', help='Delete Group Interface')
        Helper().common_add_args(group_deleteinterface, 'Group')
        group_deleteinterface.add_argument('-if', '--interface', help='Name of the Group Interface')
        return parser


    def list_group(self):
        """
        Method to list all groups from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_group(self):
        """
        Method to show a network in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_group(self):
        """
        Method to add new group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            payload['name'] = Inquiry().ask_text("Write Name Of Group")
            payload['setupbmc'] = Inquiry().ask_text("BMC Setup True or False", True)
            payload['bmcsetupname'] = Inquiry().ask_text("Write BMC Setup Name", True)
            payload['domain'] = Inquiry().ask_text("Write Domain Name", True)
            payload['osimage'] = Inquiry().ask_text("Write OSImage Name", True)
            payload['prescript'] = Inquiry().ask_text("Write Pre-Script", True)
            payload['partscript'] = Inquiry().ask_text("Write Part-Script", True)
            payload['postscript'] = Inquiry().ask_text("Write Post-Script", True)
            payload['netboot'] = Inquiry().ask_text("Network Boot", True)
            payload['localinstall'] = Inquiry().ask_file("Local Install", True)
            payload['bootmenu'] = Inquiry().ask_text("Boot Menu", True)
            payload['provision_method'] = Inquiry().ask_text("Provision Method", True)
            payload['provision_fallback'] = Inquiry().ask_text("Provision Fallback", True)
            payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users", True)
            def interfaces(interfc):
                if len(interfc):
                    confirm_text = "Add one more Interface?"
                else:
                    confirm_text = "Add Interface?"
                ifc = Inquiry().ask_confirm(confirm_text)
                if ifc:
                    interface_name = Inquiry().ask_text("Write Interface Name")
                    networkn_name = Inquiry().ask_text("Write Interface Network Name")
                    if interface_name and networkn_name:
                        interfc.append({'interface': interface_name, 'network': networkn_name})
                    return interfaces(interfc)
                else:
                    return interfc
            payload['interfaces'] = interfaces([])
            comment = Inquiry().ask_confirm("Do you want to provide a comment?")
            if comment:
                payload['comment'] = Inquiry().ask_text("Kindly provide comment(if any)")
            fields, rows  = Helper().filter_data_col(self.table, payload)
            title = f'{self.table.capitalize()} Adding => {payload["name"]}'
            Presenter().show_table_col(title, fields, rows)
            confirm = Inquiry().ask_confirm(f'Add {payload["name"]} in {self.table.capitalize()}?')
            if not confirm:
                Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                payload = {}
        else:
            error = False
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            iface = [self.args['interface'], self.args['network']]
            ifacecount = sum(x is not None for x in iface)
            if ifacecount:
                if ifacecount == 2:
                    if len(self.args['interface']) == len(self.args['network']):
                        interface_data = {'interface': self.args['interface'], 'network': self.args['network']}
                        self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                    else:
                        error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
            del self.args['interface']
            del self.args['network']
            if error:
                Helper().show_error('Operation Aborted.')
                self.args.clear()
            else:
                payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config': {self.table: {payload['name']: payload}}}
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


    def update_group(self):
        """
        Method to update a group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group", names)
                payload['setupbmc'] = Inquiry().ask_text("BMC Setup True or False", True)
                payload['bmcsetupname'] = Inquiry().ask_text("Write BMC Setup Name", True)
                payload['domain'] = Inquiry().ask_text("Write Domain Name", True)
                payload['osimage'] = Inquiry().ask_text("Write OSImage Name", True)
                payload['prescript'] = Inquiry().ask_text("Write Pre-Script", True)
                payload['partscript'] = Inquiry().ask_text("Write Part-Script", True)
                payload['postscript'] = Inquiry().ask_text("Write Post-Script", True)
                payload['netboot'] = Inquiry().ask_text("Network Boot", True)
                payload['localinstall'] = Inquiry().ask_file("Local Install", True)
                payload['bootmenu'] = Inquiry().ask_text("Boot Menu", True)
                payload['provision_method'] = Inquiry().ask_text("Provision Method", True)
                payload['provision_fallback'] = Inquiry().ask_text("Provision Fallback", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users", True)
                def interfaces(interfc):
                    if len(interfc):
                        confirm_text = "Add one more Interface?"
                    else:
                        confirm_text = "Add Interface?"
                    ifc = Inquiry().ask_confirm(confirm_text)
                    if ifc:
                        interface_name = Inquiry().ask_text("Write Interface Name")
                        networkn_name = Inquiry().ask_text("Write Interface Network Name")
                        if interface_name and networkn_name:
                            interfc.append({'interface': interface_name, 'network': networkn_name})
                        return interfaces(interfc)
                    else:
                        return interfc
                payload['interfaces'] = interfaces([])
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
            error = False
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            iface = [self.args['interface'], self.args['network']]
            ifacecount = sum(x is not None for x in iface)
            if ifacecount:
                if ifacecount == 2:
                    if len(self.args['interface']) == len(self.args['network']):
                        interface_data = {'interface': self.args['interface'], 'network': self.args['network']}
                        self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                    else:
                        error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
            del self.args['interface']
            del self.args['network']
            if error:
                Helper().show_error('Operation Aborted.')
                self.args.clear()
            payload = {k: v for k, v in self.args.items() if v is not None}
        if (len(payload) != 1) and ('name' in payload):
            request_data = {'config': {self.table: {payload['name']: payload}}}
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
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


    def rename_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group to rename", names)
                payload['newgroupname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Rename {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newgroupname'] = None
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            error = False
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            if payload['name'] is None:
                error = Helper().show_error('Kindly provide Group Name.')
            if payload['newgroupname'] is None:
                error = Helper().show_error('Kindly provide New Group Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newgroupname'] and payload['name']:
            request_data = {'config': {self.table: {payload['name']: payload}}}
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                if payload["name"] in names:
                    self.logger.debug(f'Payload => {request_data}')
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    self.logger.debug(f'Response => {response}')
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newgroupname"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_group(self):
        """
        Method to delete a group in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group to delete", names)
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Deleting => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Delete {payload["name"]} from {self.table.capitalize()}?')
                if not confirm:
                    abort = Helper().show_error(f'Deletion of {payload["name"]}, {self.table.capitalize()} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide Group Name.')
        if abort is False:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
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


    def clone_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group", names)
                payload['newgroupname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['setupbmc'] = Inquiry().ask_text("BMC Setup True or False", True)
                payload['bmcsetupname'] = Inquiry().ask_text("Write BMC Setup Name", True)
                payload['domain'] = Inquiry().ask_text("Write Domain Name", True)
                payload['osimage'] = Inquiry().ask_text("Write OSImage Name", True)
                payload['prescript'] = Inquiry().ask_text("Write Pre-Script", True)
                payload['partscript'] = Inquiry().ask_text("Write Part-Script", True)
                payload['postscript'] = Inquiry().ask_text("Write Post-Script", True)
                payload['netboot'] = Inquiry().ask_text("Network Boot", True)
                payload['localinstall'] = Inquiry().ask_file("Local Install", True)
                payload['bootmenu'] = Inquiry().ask_text("Boot Menu", True)
                payload['provision_method'] = Inquiry().ask_text("Provision Method", True)
                payload['provision_fallback'] = Inquiry().ask_text("Provision Fallback", True)
                payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users", True)
                def interfaces(interfc):
                    if len(interfc):
                        confirm_text = "Add one more Interface?"
                    else:
                        confirm_text = "Add Interface?"
                    ifc = Inquiry().ask_confirm(confirm_text)
                    if ifc:
                        interface_name = Inquiry().ask_text("Write Interface Name")
                        networkn_name = Inquiry().ask_text("Write Interface Network Name")
                        if interface_name and networkn_name:
                            interfc.append({'interface': interface_name, 'network': networkn_name})
                        return interfaces(interfc)
                    else:
                        return interfc
                interfc = []
                payload['interfaces'] = interfaces(interfc)
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
                    title = f'{self.table.capitalize()} Cloning : {payload["name"]} => {payload["newgroupname"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newgroupname"]}?')
                    if not confirm:
                        Helper().show_error(f'Cloning of {payload["newgroupname"]} is Aborted')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            error =  False
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            iface = [self.args['interface'], self.args['network']]
            ifacecount = sum(x is not None for x in iface)
            if ifacecount:
                if ifacecount == 2:
                    if len(self.args['interface']) == len(self.args['network']):
                        interface_data = {'interface': self.args['interface'], 'network': self.args['network']}
                        self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                    else:
                        error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
            del self.args['interface']
            del self.args['network']
            if error:
                Helper().show_error('Operation Aborted.')
                self.args.clear()
            payload = {k: v for k, v in self.args.items() if v is not None}
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
            request_data = {'config': {self.table: {payload['name']: payload}}}
            if self.get_list:
                names = list(self.get_list['config'][self.table].keys())
                if payload["name"] in names:
                    if payload["newgroupname"] in names:
                        Helper().show_error(f'{payload["newgroupname"]} is already present in {self.table.capitalize()}.')
                    else:
                        self.logger.debug(f'Payload => {request_data}')
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        self.logger.debug(f'Response => {response}')
                        if response == 201:
                            Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newgroupname"]}.')
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
        Method to list a Group interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces')
        get_list = Rest().get_data(self.table, self.args['name']+'/interfaces')
        self.logger.debug(f'List Interfaces => {get_list}')
        if get_list:
            data = get_list['config'][self.table][self.args["name"]]['interfaces']
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                fields, rows  = Helper().filter_interface(self.interface, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {self.table.capitalize()} {self.args["name"]} Interfaces >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Helper().show_error(f'{self.args["name"]} is not found in {self.table}.')
        return response


    def show_interface(self):
        """
        Method to list a Group interfaces in Luna Configuration.
        """
        response = False
        fields, rows = [], []
        self.logger.debug(f'Table => {self.table} and URI => {self.args["name"]}/interfaces{self.args["interface"]}')
        get_list = Rest().get_data(self.table, self.args['name']+'/interfaces/'+self.args['interface'])
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
        Method to list a Group interfaces in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group", names)
                def interfaces(interfc):
                    if len(interfc):
                        confirm_text = "Add one more Interface?"
                    else:
                        confirm_text = "Add Interface?"
                    ifc = Inquiry().ask_confirm(confirm_text)
                    if ifc:
                        interface_name = Inquiry().ask_text("Write Interface Name")
                        networkn_name = Inquiry().ask_text("Write Interface Network Name")
                        if interface_name and networkn_name:
                            interfc.append({
                                'interface': interface_name,
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
            error = False
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            iface = [self.args['interface'], self.args['network']]
            ifacecount = sum(x is not None for x in iface)
            if ifacecount:
                if ifacecount == 2:
                    if len(self.args['interface']) == len(self.args['network']):
                        interface_data = {'interface': self.args['interface'], 'network': self.args['network']}
                        self.args['interfaces'] = [{key : value[i] for key, value in interface_data.items()} for i in range(len(interface_data['interface']))]
                    else:
                        error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
                else:
                    error = Helper().show_warning('Each Interface should have Interface Name and Network Name.')
            del self.args['interface']
            del self.args['network']
            if error:
                Helper().show_error('Operation Aborted.')
                self.args.clear()
            payload = {k: v for k, v in self.args.items() if v is not None}
        if (len(payload) != 1) and ('name' in payload):
            node_name = payload['name']
            del payload['name']
            request_data = {'config': {self.table: {node_name: payload}}}
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
        Method to list a Group interfaces in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            get_list = Rest().get_data(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group to delete Interface", names)
                record = Rest().get_data(self.table, payload['name'])
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
            for remove in ['debug', 'command', 'action', 'init']:
                self.args.pop(remove, None)
            payload = self.args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide Group Name.')
            if payload['interface'] is None:
                abort = Helper().show_error('Kindly provide Interface Name.')
        if abort is False:
            self.logger.debug(f"URI {payload['name']}/interfaces/{payload['interface']}")
            response = Rest().get_delete(self.table, payload['name']+'/interfaces/'+payload['interface'])
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'Interface {payload["interface"]} Deleted from {self.table.capitalize()} {payload["name"]}.')
            else:
                Helper().show_error(f'HTTP Error Code: {response}.')
        return response
