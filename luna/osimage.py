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

class OSImage(object):
    """
    OSImage Class responsible to show, list,
    add, remove information for the osimage
    """

    def __init__(self, args=None):
        self.args = args
        self.table = "osimage"
        self.version = None
        self.clusterid = None
        if self.args:
            if self.args["action"] == "list":
                self.list_osimage(self.args)
            elif self.args["action"] == "show":
                self.show_osimage(self.args)
            elif self.args["action"] == "add":
                self.add_osimage(self.args)
            elif self.args["action"] == "update":
                self.update_osimage(self.args)
            elif self.args["action"] == "rename":
                self.rename_osimage(self.args)
            elif self.args["action"] == "delete":
                self.delete_osimage(self.args)
            elif self.args["action"] == "clone":
                self.clone_osimage(self.args)
            elif self.args["action"] == "pack":
                self.pack_osimage(self.args)
            elif self.args["action"] == "kernel":
                self.kernel_osimage(self.args)
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the OSImage class.
        """
        osimage_menu = subparsers.add_parser('osimage', help='OSImage operations.')
        osimage_args = osimage_menu.add_subparsers(dest='action')
        ## >>>>>>> OSImage Command >>>>>>> list
        cmd = osimage_args.add_parser('list', help='List OSImages')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> OSImage Command >>>>>>> show
        cmd = osimage_args.add_parser('show', help='Show a OSImage')
        cmd.add_argument('name', help='Name of the OSImage')
        cmd.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> OSImage Command >>>>>>> add
        cmd = osimage_args.add_parser('add', help='Add OSImage')
        cmd.add_argument('--init', '-i', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the OSImage')
        cmd.add_argument('--dracutmodules', '-dm', help='Dracut Modules')
        cmd.add_argument('--grab_filesystems', '-gf', help='Grab Filesystems')
        cmd.add_argument('--grab_exclude', '-ge', help='Grab Excludes')
        cmd.add_argument('--initrdfile', '-rd', help='INIT RD File')
        cmd.add_argument('--kernelfile', '-k', help='Kernel File')
        cmd.add_argument('--kernelmodules', '-m', help='Kernel Modules')
        cmd.add_argument('--kerneloptions', '-o', help='Kernel Options')
        cmd.add_argument('--kernelversion', '-v', help='Kernel Version')
        cmd.add_argument('--path', '-p', help='Path of image')
        cmd.add_argument('--tarball', '-tar', help='Tarball UUID')
        cmd.add_argument('--torrent', '-t', help='Torrent UUID')
        cmd.add_argument('--distribution', '-d', help='Distribution From')
        cmd.add_argument('--comment', '-c', help='Comment for OSImage')
        ## >>>>>>> OSImage Command >>>>>>> update
        cmd = osimage_args.add_parser('update', help='Update OSImage')
        cmd.add_argument('--init', '-i', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the OSImage')
        cmd.add_argument('--dracutmodules', '-dm', help='Dracut Modules')
        cmd.add_argument('--grab_filesystems', '-gf', help='Grab Filesystems')
        cmd.add_argument('--grab_exclude', '-ge', help='Grab Excludes')
        cmd.add_argument('--initrdfile', '-rd', help='INIT RD File')
        cmd.add_argument('--kernelfile', '-k', help='Kernel File')
        cmd.add_argument('--kernelmodules', '-m', help='Kernel Modules')
        cmd.add_argument('--kerneloptions', '-o', help='Kernel Options')
        cmd.add_argument('--kernelversion', '-v', help='Kernel Version')
        cmd.add_argument('--path', '-p', help='Path of image')
        cmd.add_argument('--tarball', '-tar', help='Tarball UUID')
        cmd.add_argument('--torrent', '-t', help='Torrent UUID')
        cmd.add_argument('--distribution', '-d', help='Distribution From')
        cmd.add_argument('--comment', '-c', help='Comment for OSImage')
        ## >>>>>>> OSImage Command >>>>>>> clone
        cmd = osimage_args.add_parser('clone', help='Clone OSImage')
        cmd.add_argument('--init', '-i', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the OSImage')
        cmd.add_argument('--newosimage', '-nn', help='New Name of the OSImage')
        cmd.add_argument('--dracutmodules', '-dm', help='Dracut Modules')
        cmd.add_argument('--grab_filesystems', '-gf', help='Grab Filesystems')
        cmd.add_argument('--grab_exclude', '-ge', help='Grab Excludes')
        cmd.add_argument('--initrdfile', '-rd', help='INIT RD File')
        cmd.add_argument('--kernelfile', '-k', help='Kernel File')
        cmd.add_argument('--kernelmodules', '-m', help='Kernel Modules')
        cmd.add_argument('--kerneloptions', '-o', help='Kernel Options')
        cmd.add_argument('--kernelversion', '-v', help='Kernel Version')
        cmd.add_argument('--path', '-p', help='Path of image')
        cmd.add_argument('--tarball', '-tar', help='Tarball UUID')
        cmd.add_argument('--torrent', '-t', help='Torrent UUID')
        cmd.add_argument('--distribution', '-d', help='Distribution From')
        cmd.add_argument('--comment', '-c', help='Comment for OSImage')
        ## >>>>>>> OSImage Command >>>>>>> rename
        cmd = osimage_args.add_parser('rename', help='Rename OSImage')
        cmd.add_argument('--init', '-i', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the OSImage')
        cmd.add_argument('--newosimage', '-nn', help='New Name of the OSImage')
        ## >>>>>>> OSImage Command >>>>>>> delete
        cmd = osimage_args.add_parser('delete', help='Delete OSImage')
        cmd.add_argument('--init', '-i', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the OSImage')
        ## >>>>>>> OSImage Command >>>>>>> pack
        cmd = osimage_args.add_parser('pack', help='Pack OSImage')
        cmd.add_argument('name', help='Name of the OS Image')
        ## >>>>>>> OSImage Command >>>>>>> kernel
        cmd = osimage_args.add_parser('kernel', help='Chnage Kernel Version in OS Image')
        cmd.add_argument('--init', '-i', action='store_true', help='OSImage values one-by-one')
        cmd.add_argument('--name', '-n', help='Name of the OSImage')
        cmd.add_argument('--initrdfile', '-rd', help='INIT RD File')
        cmd.add_argument('--kernelfile', '-k', help='Kernel File')
        cmd.add_argument('--kernelversion', '-v', help='Kernel Version')
        ## >>>>>>> OSImage Commands Ends
        return parser


    def list_osimage(self, args=None):
        """
        Method to list all osimages from Luna Configuration.
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


    def show_osimage(self, args=None):
        """
        Method to show a osimage in Luna Configuration.
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


    def add_osimage(self, args=None):
        """
        Method to add new osimage in Luna Configuration.
        """
        payload = {}
        if args['init']:
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


    def update_osimage(self, args=None):
        """
        Method to update a osimage in Luna Configuration.
        """
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
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


    def rename_osimage(self, args=None):
        """
        Method to rename a osimage in Luna Configuration.
        """
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
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
                    response = Rest().post_data(self.table, payload['name'], request_data)
                    if response == 204:
                        Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newosimage"]}.')
                else:
                    Helper().show_error(f'{payload["name"]} Not found in {self.table.capitalize()}.')
            else:
                response = Helper().show_error(f'No {self.table.capitalize()} is available.')
        return True


    def delete_osimage(self, args=None):
        """
        Method to delete a osimage in Luna Configuration.
        """
        abort = False
        payload = {}
        if args['init']:
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
            del args['debug']
            del args['command']
            del args['action']
            del args['init']
            payload = args
            if payload['name'] is None:
                abort = Helper().show_error('Kindly provide OSImage Name.')
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


    def clone_osimage(self, args=None):
        """
        Method to rename a osimage in Luna Configuration.
        """
        payload = {}
        if args['init']:
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
                    if payload["newosimage"] in names:
                        Helper().show_error(f'{payload["newosimage"]} is already present in {self.table.capitalize()}.')
                    else:
                        response = Rest().post_clone(self.table, payload['name'], request_data)
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


    def pack_osimage(self, args=None):
        """
        Method to pack the OS Image
        """
        response = Rest().get_status(self.table, args['name']+'/_pack')
        if response == 204:
            Helper().show_success(f'OS Image {args["name"]} Packed.')
        else:
            Helper().show_error(f'HTTP Error Code: {response}.')
        return response


    def kernel_osimage(self, args=None):
        """
        Method to change kernel version from an
        OS Image
        """
        payload = {}
        if args['init']:
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
            response = Rest().post_data(self.table, payload['name']+'/_kernel', request_data)
            if response == 204:
                Helper().show_success(f'OS Image {args["name"]} Kernel updated.')
            else:
                Helper().show_error(f'HTTP Error Code: {response}.')
        return error
