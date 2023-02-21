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

class Group(object):
    """
    Group Class responsible to show, list,
    add, remove information for the Group
    """

    def __init__(self, args=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "group"
        self.interface = "groupinterface"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] == "list":
                self.list_group()
            elif self.args["action"] == "show":
                self.show_group()
            elif self.args["action"] == "add":
                self.add_group()
            elif self.args["action"] == "update":
                self.update_group()
            elif self.args["action"] == "rename":
                self.rename_group()
            elif self.args["action"] == "delete":
                self.delete_group()
            
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
        related to the Group class.
        """
        group_menu = subparsers.add_parser('group', help='Group operations')
        group_args = group_menu.add_subparsers(dest='action')
        ## >>>>>>> Group Command >>>>>>> list
        cmd = group_args.add_parser('list', help='List Groups')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Group Command >>>>>>> show
        cmd = group_args.add_parser('show', help='Show Group')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the Group')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Group Command >>>>>>> add
        cmd = group_args.add_parser('add', help='Add Group')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Group values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Group')
        cmd.add_argument('-b', '--bmcsetup', action='store_true', help='BMC Setup')
        cmd.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        cmd.add_argument('-D', '--domain', help='Domain Name')
        cmd.add_argument('-o', '--osimage', help='OS Image Name')
        cmd.add_argument('-pre', '--prescript', help='Pre Script')
        cmd.add_argument('-part', '--partscript', help='Part Script')
        cmd.add_argument('-post', '--postscript', help='Post Script')
        cmd.add_argument('-nb', '--netboot', help='Network Boot')
        cmd.add_argument('-li', '--localinstall', help='Local Install')
        cmd.add_argument('-bm', '--bootmenu', help='Boot Menu')
        cmd.add_argument('-pm', '--provision_method', help='Provision Method')
        cmd.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        cmd.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        cmd.add_argument('-if', '--interfaces', action='append', help='Group Interfaces interfacename|networkname')
        cmd.add_argument('-c', '--comment', help='Comment for Group')
        ## >>>>>>> Group Command >>>>>>> udpate
        cmd = group_args.add_parser('udpate', help='Update Group')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Group values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Group')
        cmd.add_argument('-b', '--bmcsetup', action='store_true', help='BMC Setup True/False')
        cmd.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        cmd.add_argument('-D', '--domain', help='Domain Name')
        cmd.add_argument('-o', '--osimage', help='OS Image Name')
        cmd.add_argument('-pre', '--prescript', help='Pre Script')
        cmd.add_argument('-part', '--partscript', help='Part Script')
        cmd.add_argument('-post', '--postscript', help='Post Script')
        cmd.add_argument('-nb', '--netboot', help='Network Boot')
        cmd.add_argument('-li', '--localinstall', help='Local Install')
        cmd.add_argument('-bm', '--bootmenu', help='Boot Menu')
        cmd.add_argument('-pm', '--provision_method', help='Provision Method')
        cmd.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        cmd.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        cmd.add_argument('-if', '--interfaces', action='append', help='Group Interfaces interfacename|networkname')
        cmd.add_argument('-c', '--comment', help='Comment for Group')
        ## >>>>>>> Group Command >>>>>>> clone
        cmd = group_args.add_parser('clone', help='Clone Group.')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Group values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Group')
        cmd.add_argument('-nn', '--newgroupname', help='New Name for the Group')
        cmd.add_argument('-b', '--bmcsetup', action='store_true', help='BMC Setup True/False')
        cmd.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        cmd.add_argument('-D', '--domain', help='Domain Name')
        cmd.add_argument('-o', '--osimage', help='OS Image Name')
        cmd.add_argument('-pre', '--prescript', help='Pre Script')
        cmd.add_argument('-part', '--partscript', help='Part Script')
        cmd.add_argument('-post', '--postscript', help='Post Script')
        cmd.add_argument('-nb', '--netboot', help='Network Boot')
        cmd.add_argument('-li', '--localinstall', help='Local Install')
        cmd.add_argument('-bm', '--bootmenu', help='Boot Menu')
        cmd.add_argument('-pm', '--provision_method', help='Provision Method')
        cmd.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        cmd.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        cmd.add_argument('-if', '--interfaces', action='append', help='Group Interfaces interfacename|networkname')
        cmd.add_argument('-c', '--comment', help='Comment for Group')
        ## >>>>>>> Group Command >>>>>>> rename
        cmd = group_args.add_parser('rename', help='Rename Group.')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Group values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Group')
        cmd.add_argument('-nn', '--newgroupname', help='New Name for the Group')
        ## >>>>>>> Group Command >>>>>>> delete
        cmd = group_args.add_parser('delete', help='Delete Group')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Group values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Group')
        ## >>>>>>> Group Commands Ends
        ## >>>>>>> Group Interface Command >>>>>>> interfaces
        cmd = group_args.add_parser('interfaces', help='List Group Interfaces')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the Group')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Group Interface Command >>>>>>> interfaces
        cmd = group_args.add_parser('interface', help='Show Group Interface')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the Group')
        cmd.add_argument('interface', help='Name of the Group Interface')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> Group Interface Command >>>>>>> delete
        cmd = group_args.add_parser('updateinterface', help='Update Group Interface')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Group values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Group')
        cmd.add_argument('-if', '--interface', action='append', help='Group Interface')
        cmd.add_argument('-N', '--network', action='append', help='Network Name')
        ## >>>>>>> Group Interface Command >>>>>>> delete
        cmd = group_args.add_parser('deleteinterface', help='Delete Group Interface')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='Group values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the Group')
        cmd.add_argument('-if', '--interface', help='Name of the Group Interface')
        return parser


    def list_group(self):
        """
        Method to list all groups from Luna Configuration.
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


    def show_group(self):
        """
        Method to show a network in Luna Configuration.
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


    def add_group(self):
        """
        Method to add new group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            payload['name'] = Inquiry().ask_text("Write Name Of Group")
            payload['bmcsetup'] = Inquiry().ask_text("BMC Setup True or False")
            payload['bmcsetupname'] = Inquiry().ask_text("Write BMC Setup Name")
            payload['domain'] = Inquiry().ask_text("Write Domain Name")
            payload['osimage'] = Inquiry().ask_text("Write OSImage Name")
            payload['prescript'] = Inquiry().ask_text("Write Pre-Script")
            payload['partscript'] = Inquiry().ask_text("Write Part-Script")
            payload['postscript'] = Inquiry().ask_text("Write Post-Script")
            payload['netboot'] = Inquiry().ask_text("Network Boot")
            payload['localinstall'] = Inquiry().ask_file("Local Install")
            payload['bootmenu'] = Inquiry().ask_text("Boot Menu")
            payload['provision_method'] = Inquiry().ask_text("Provision Method")
            payload['provision_fallback'] = Inquiry().ask_text("Provision Fallback")
            payload['unmanaged_bmc_users'] = Inquiry().ask_text("Unmanaged BMC Users")
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


    def update_group(self):
        """
        Method to update a group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group", names)
                payload['bmcsetup'] = Inquiry().ask_text("BMC Setup True or False", True)
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


    def rename_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            payload = self.args
            if payload['name'] is None:
                error = Helper().show_error('Kindly provide Group Name.')
            if payload['newgroupname'] is None:
                error = Helper().show_error('Kindly provide New Group Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newgroupname'] and payload['name']:
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
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            payload = self.args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide Group Name.')
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


    def clone_group(self):
        """
        Method to rename a group in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group", names)
                payload['newgroupname'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['bmcsetup'] = Inquiry().ask_text("BMC Setup True or False", True)
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
        Method to list a Group interfaces in Luna Configuration.
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
        Method to list a Group interfaces in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
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
            del self.args['debug']
            del self.args['command']
            del self.args['action']
            del self.args['init']
            if len(self.args['interface']) == len(self.args['network']):
                self.args['interfaces'] = []
                temp_dict = {}
                for ifc, nwk in zip(self.args['interface'], self.args['network']):
                    temp_dict['interface'] = ifc
                    temp_dict['network'] = nwk
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
        Method to list a Group interfaces in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select Group to delete Interface", names)
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
