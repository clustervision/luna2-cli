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

class OSImage(object):
    """
    OSImage Class responsible to show, list,
    add, remove information for the osimage
    """

    def __init__(self, args=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "osimage"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] == "list":
                self.list_osimage()
            elif self.args["action"] == "show":
                self.show_osimage()
            elif self.args["action"] == "add":
                self.add_osimage()
            elif self.args["action"] == "update":
                self.update_osimage()
            elif self.args["action"] == "rename":
                self.rename_osimage()
            elif self.args["action"] == "delete":
                self.delete_osimage()
            elif self.args["action"] == "clone":
                self.clone_osimage()
            elif self.args["action"] == "pack":
                self.pack_osimage()
            elif self.args["action"] == "kernel":
                self.kernel_osimage()
            else:
                Helper().show_error("Not a valid option.")
        else:
            Helper().show_error("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the OSImage class.
        """
        osimage_menu = subparsers.add_parser('osimage', help='OSImage operations.')
        osimage_args = osimage_menu.add_subparsers(dest='action')
        ## >>>>>>> OSImage Command >>>>>>> list
        cmd = osimage_args.add_parser('list', help='List OSImages')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> OSImage Command >>>>>>> show
        cmd = osimage_args.add_parser('show', help='Show a OSImage')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the OSImage')
        cmd.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        ## >>>>>>> OSImage Command >>>>>>> add
        cmd = osimage_args.add_parser('add', help='Add OSImage')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the OSImage')
        cmd.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        cmd.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        cmd.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        cmd.add_argument('-rd', '--initrdfile', help='INIT RD File')
        cmd.add_argument('-k', '--kernelfile', help='Kernel File')
        cmd.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        cmd.add_argument('-o', '--kerneloptions', help='Kernel Options')
        cmd.add_argument('-v', '--kernelversion', help='Kernel Version')
        cmd.add_argument('-p', '--path', help='Path of image')
        cmd.add_argument('-tar', '--tarball', help='Tarball UUID')
        cmd.add_argument('-t', '--torrent', help='Torrent UUID')
        cmd.add_argument('-D', '--distribution', help='Distribution From')
        cmd.add_argument('-c', '--comment', help='Comment for OSImage')
        ## >>>>>>> OSImage Command >>>>>>> update
        cmd = osimage_args.add_parser('update', help='Update OSImage')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the OSImage')
        cmd.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        cmd.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        cmd.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        cmd.add_argument('-rd', '--initrdfile', help='INIT RD File')
        cmd.add_argument('-k', '--kernelfile', help='Kernel File')
        cmd.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        cmd.add_argument('-o', '--kerneloptions', help='Kernel Options')
        cmd.add_argument('-v', '--kernelversion', help='Kernel Version')
        cmd.add_argument('-p', '--path', help='Path of image')
        cmd.add_argument('-tar', '--tarball', help='Tarball UUID')
        cmd.add_argument('-t', '--torrent', help='Torrent UUID')
        cmd.add_argument('-D', '--distribution', help='Distribution From')
        cmd.add_argument('-c', '--comment', help='Comment for OSImage')
        ## >>>>>>> OSImage Command >>>>>>> clone
        cmd = osimage_args.add_parser('clone', help='Clone OSImage')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the OSImage')
        cmd.add_argument('-nn', '--newosimage', help='New Name of the OSImage')
        cmd.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        cmd.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        cmd.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        cmd.add_argument('-rd', '--initrdfile', help='INIT RD File')
        cmd.add_argument('-k', '--kernelfile', help='Kernel File')
        cmd.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        cmd.add_argument('-o', '--kerneloptions', help='Kernel Options')
        cmd.add_argument('-v', '--kernelversion', help='Kernel Version')
        cmd.add_argument('-p', '--path', help='Path of image')
        cmd.add_argument('-tar', '--tarball', help='Tarball UUID')
        cmd.add_argument('-t', '--torrent', help='Torrent UUID')
        cmd.add_argument('-D', '--distribution', help='Distribution From')
        cmd.add_argument('-c', '--comment', help='Comment for OSImage')
        ## >>>>>>> OSImage Command >>>>>>> rename
        cmd = osimage_args.add_parser('rename', help='Rename OSImage')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the OSImage')
        cmd.add_argument('-nn', '--newosimage', help='New Name of the OSImage')
        ## >>>>>>> OSImage Command >>>>>>> delete
        cmd = osimage_args.add_parser('delete', help='Delete OSImage')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the OSImage')
        ## >>>>>>> OSImage Command >>>>>>> pack
        cmd = osimage_args.add_parser('pack', help='Pack OSImage')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('name', help='Name of the OS Image')
        ## >>>>>>> OSImage Command >>>>>>> kernel
        cmd = osimage_args.add_parser('kernel', help='Chnage Kernel Version in OS Image')
        cmd.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        cmd.add_argument('-i', '--init', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('-n', '--name', help='Name of the OSImage')
        cmd.add_argument('-rd', '--initrdfile', help='INIT RD File')
        cmd.add_argument('-k', '--kernelfile', help='Kernel File')
        cmd.add_argument('-v', '--kernelversion', help='Kernel Version')
        ## >>>>>>> OSImage Commands Ends
        return parser


    def list_osimage(self):
        """
        Method to list all osimages from Luna Configuration.
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


    def show_osimage(self):
        """
        Method to show a osimage in Luna Configuration.
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


    def add_osimage(self):
        """
        Method to add new osimage in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            payload['name'] = Inquiry().ask_text("Write Name Of OSImage")
            payload['dracutmodules'] = Inquiry().ask_text("Write Dracut Modules")
            payload['grab_filesystems'] = Inquiry().ask_text("Write Grab Filesystems")
            payload['grab_exclude'] = Inquiry().ask_text("Write Grab Excludes")
            payload['initrdfile'] = Inquiry().ask_text("Write INIT RD File")
            payload['kernelfile'] = Inquiry().ask_text("Write Kernel File")
            payload['kernelmodules'] = Inquiry().ask_text("Write Kernel Modules")
            payload['kerneloptions'] = Inquiry().ask_text("Write Kernel Options")
            payload['kernelversion'] = Inquiry().ask_text("Write Kernel Version")
            payload['path'] = Inquiry().ask_file("Write Path of image")
            payload['tarball'] = Inquiry().ask_text("Write Tarball UUID")
            payload['torrent'] = Inquiry().ask_text("Write Torrent UUID")
            payload['distribution'] = Inquiry().ask_text("Write Distribution")
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


    def update_osimage(self):
        """
        Method to update a osimage in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select OSImage", names)
                payload['dracutmodules'] = Inquiry().ask_text("Write Dracut Modules", True)
                payload['grab_filesystems'] = Inquiry().ask_text("Write Grab Filesystems", True)
                payload['grab_exclude'] = Inquiry().ask_text("Write Grab Excludes", True)
                payload['initrdfile'] = Inquiry().ask_text("Write INIT RD File", True)
                payload['kernelfile'] = Inquiry().ask_text("Write Kernel File", True)
                payload['kernelmodules'] = Inquiry().ask_text("Write Kernel Modules", True)
                payload['kerneloptions'] = Inquiry().ask_text("Write Kernel Options", True)
                payload['kernelversion'] = Inquiry().ask_text("Write Kernel Version", True)
                payload['path'] = Inquiry().ask_file("Write Path of image", True)
                payload['tarball'] = Inquiry().ask_text("Write Tarball UUID", True)
                payload['torrent'] = Inquiry().ask_text("Write Torrent UUID", True)
                payload['distribution'] = Inquiry().ask_text("Write Distribution", True)
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


    def rename_osimage(self):
        """
        Method to rename a osimage in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select OSImage to rename", names)
                payload['newosimage'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                fields, rows  = Helper().filter_data_col(self.table, payload)
                title = f'{self.table.capitalize()} Renaming => {payload["name"]}'
                Presenter().show_table_col(title, fields, rows)
                confirm = Inquiry().ask_confirm(f'Rename {payload["name"]} in {self.table.capitalize()}?')
                if not confirm:
                    Helper().show_error(f'Add {payload["name"]} into {self.table.capitalize()} Aborted')
                    payload['newosimage'] = None
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
                error = Helper().show_error('Kindly provide OSImage Name.')
            if payload['newosimage'] is None:
                error = Helper().show_error('Kindly provide New OSImage Name.')
            if error:
                Helper().show_error(f'Renaming {payload["name"]} in {self.table.capitalize()} Abort.')
        if payload['newosimage'] and payload['name']:
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
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newosimage"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_osimage(self):
        """
        Method to delete a osimage in Luna Configuration.
        """
        abort = False
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select OSImage to delete", names)
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
                abort = Helper().show_error('Kindly provide OSImage Name.')
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


    def clone_osimage(self):
        """
        Method to rename a osimage in Luna Configuration.
        """
        payload = {}
        if self.args['init']:
            get_list = Helper().get_list(self.table)
            if get_list:
                names = list(get_list['config'][self.table].keys())
                payload['name'] = Inquiry().ask_select("Select OSImage", names)
                payload['newosimage'] = Inquiry().ask_text(f'Write new name for {payload["name"]}')
                payload['dracutmodules'] = Inquiry().ask_text("Write Dracut Modules", True)
                payload['grab_filesystems'] = Inquiry().ask_text("Write Grab Filesystems", True)
                payload['grab_exclude'] = Inquiry().ask_text("Write Grab Excludes", True)
                payload['initrdfile'] = Inquiry().ask_text("Write INIT RD File", True)
                payload['kernelfile'] = Inquiry().ask_text("Write Kernel File", True)
                payload['kernelmodules'] = Inquiry().ask_text("Write Kernel Modules", True)
                payload['kerneloptions'] = Inquiry().ask_text("Write Kernel Options", True)
                payload['kernelversion'] = Inquiry().ask_text("Write Kernel Version", True)
                payload['path'] = Inquiry().ask_file("Write Path of image", True)
                payload['tarball'] = Inquiry().ask_text("Write Tarball UUID", True)
                payload['torrent'] = Inquiry().ask_text("Write Torrent UUID", True)
                payload['distribution'] = Inquiry().ask_text("Write Distribution", True)
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
                    title = f'{self.table.capitalize()} Cloning : {payload["name"]} => {payload["newosimage"]}'
                    Presenter().show_table_col(title, fields, rows)
                    confirm = Inquiry().ask_confirm(f'Clone {payload["name"]} as {payload["newosimage"]}?')
                    if not confirm:
                        Helper().show_error(f'Cloning of {payload["newosimage"]} is Aborted')
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
                    if payload["newosimage"] in names:
                        Helper().show_error(f'{payload["newosimage"]} is already present in {self.table.capitalize()}.')
                    else:
                        self.logger.debug(f'Payload => {request_data}')
                        response = Rest().post_clone(self.table, payload['name'], request_data)
                        self.logger.debug(f'Response => {response}')
                        if response == 201:
                            Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newosimage"]}.')
                        else:
                            Helper().show_error(f'HTTP Error {response}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                Helper().show_error(f'No {self.table.capitalize()} is available.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def pack_osimage(self):
        """
        Method to pack the OS Image
        """
        uri = self.args['name']+'/_pack'
        self.logger.debug(f'OS Image Pack URI => {uri}')
        response = Rest().get_status(self.table, uri)
        self.logger.debug(f'Response => {response}')
        if response == 204:
            Helper().show_success(f'OS Image {self.args["name"]} Packed.')
        else:
            Helper().show_error(f'HTTP Error Code: {response}.')
        return response


    def kernel_osimage(self):
        """
        Method to change kernel version from an
        OS Image
        """
        payload = {}
        if self.args['init']:
            payload['name'] = Inquiry().ask_text("Write Name Of OSImage")
            payload['initrdfile'] = Inquiry().ask_text("Write INIT RD File")
            payload['kernelfile'] = Inquiry().ask_text("Write Kernel File")
            payload['kernelversion'] = Inquiry().ask_text("Write Kernel Version")
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
            self.logger.debug(f'Change Kernel URI => {payload["name"]}/_kernel')
            response = Rest().post_data(self.table, payload['name']+'/_kernel', request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'OS Image {self.args["name"]} Kernel updated.')
            else:
                Helper().show_error(f'HTTP Error Code: {response}.')
        return error
