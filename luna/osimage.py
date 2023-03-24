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
from time import sleep
from multiprocessing import Process
from termcolor import colored
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log

class OSImage():
    """
    OSImage Class responsible to show, list,
    add, remove information for the osimage
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "osimage"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "change", "rename", "clone", "remove", "pack", "kernel"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_osimage')
                call(self)
            else:
                Helper().show_error("Not a valid option.")
        if parser and subparsers:
            self.getarguments(parser, subparsers)


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the OSImage class.
        """
        osimage_menu = subparsers.add_parser('osimage', help='OSImage operations.')
        osimage_args = osimage_menu.add_subparsers(dest='action')
        osimage_list = osimage_args.add_parser('list', help='List OSImages')
        Helper().common_list_args(osimage_list)
        osimage_show = osimage_args.add_parser('show', help='Show a OSImage')
        osimage_show.add_argument('name', help='Name of the OSImage')
        Helper().common_list_args(osimage_show)
        osimage_add = osimage_args.add_parser('add', help='Add OSImage')
        osimage_add.add_argument('name', help='Name of the OSImage')
        osimage_add.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        osimage_add.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        osimage_add.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        osimage_add.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_add.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_add.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        osimage_add.add_argument('-o', '--kerneloptions', help='Kernel Options')
        osimage_add.add_argument('-v', '--kernelversion', help='Kernel Version')
        osimage_add.add_argument('-p', '--path', required=True, help='Path of image')
        osimage_add.add_argument('-tar', '--tarball', help='Tarball UUID')
        osimage_add.add_argument('-t', '--torrent', help='Torrent UUID')
        osimage_add.add_argument('-D', '--distribution', help='Distribution From')
        osimage_add.add_argument('-c', '--comment', help='Comment for OSImage')
        osimage_add.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        osimage_change = osimage_args.add_parser('change', help='Change OSImage')
        osimage_change.add_argument('name', help='Name of the OSImage')
        osimage_change.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        osimage_change.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        osimage_change.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        osimage_change.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_change.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_change.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        osimage_change.add_argument('-o', '--kerneloptions', help='Kernel Options')
        osimage_change.add_argument('-v', '--kernelversion', help='Kernel Version')
        osimage_change.add_argument('-p', '--path', help='Path of image')
        osimage_change.add_argument('-tar', '--tarball', help='Tarball UUID')
        osimage_change.add_argument('-t', '--torrent', help='Torrent UUID')
        osimage_change.add_argument('-D', '--distribution', default='redhat', help='Distribution From')
        osimage_change.add_argument('-c', '--comment', help='Comment for OSImage')
        osimage_change.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        osimage_clone = osimage_args.add_parser('clone', help='Clone OSImage')
        osimage_clone.add_argument('name', help='Name of the OSImage')
        osimage_clone.add_argument('-nn', '--newosimage', help='New Name of the OSImage')
        osimage_clone.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        osimage_clone.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        osimage_clone.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        osimage_clone.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_clone.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_clone.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        osimage_clone.add_argument('-o', '--kerneloptions', help='Kernel Options')
        osimage_clone.add_argument('-v', '--kernelversion', help='Kernel Version')
        osimage_clone.add_argument('-p', '--path', required=True, help='Path of image')
        osimage_clone.add_argument('-tar', '--tarball', help='Tarball UUID')
        osimage_clone.add_argument('-t', '--torrent', help='Torrent UUID')
        osimage_clone.add_argument('-D', '--distribution', help='Distribution From')
        osimage_clone.add_argument('-c', '--comment', help='Comment for OSImage')
        osimage_clone.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        osimage_rename = osimage_args.add_parser('rename', help='Rename OSImage')
        osimage_rename.add_argument('name', help='Name of the OSImage')
        osimage_rename.add_argument('newosimage', help='New Name of the OSImage')
        osimage_rename.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        osimage_remove = osimage_args.add_parser('remove', help='Remove OSImage')
        osimage_remove.add_argument('name', help='Name of the OS Image')
        osimage_remove.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        osimage_pack = osimage_args.add_parser('pack', help='Pack OSImage')
        osimage_pack.add_argument('name', help='Name of the OS Image')
        osimage_pack.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        osimage_kernel = osimage_args.add_parser('kernel', help='Chnage Kernel Version in OS Image')
        osimage_kernel.add_argument('name', help='Name of the OS Image')
        osimage_kernel.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_kernel.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_kernel.add_argument('-v', '--kernelversion', help='Kernel Version')
        osimage_kernel.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        return parser


    def list_osimage(self):
        """
        Method to list all osimages from Luna Configuration.
        """
        return Helper().get_list(self.table, self.args)


    def show_osimage(self):
        """
        Method to show a osimage in Luna Configuration.
        """
        return Helper().show_data(self.table, self.args)


    def add_osimage(self):
        """
        Method to add new osimage in Luna Configuration.
        """
        payload = {}
        for remove in ['debug', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 201:
                Helper().show_success(f'New {self.table.capitalize()}, {payload["name"]} created.')
            else:
                Helper().show_error(f'HTTP Error {response}.')
        return True


    def change_osimage(self):
        """
        Method to change a osimage in Luna Configuration.
        """
        payload = {}
        for remove in ['debug', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} updated.')
            else:
                Helper().show_error(f'HTTP Error {response}.')
        else:
            Helper().show_error('Nothing to update.')
        return True


    def rename_osimage(self):
        """
        Method to rename a osimage in Luna Configuration.
        """
        for remove in ['debug', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_data(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} renamed to {payload["newosimage"]}.')
            else:
                Helper().show_error(f'HTTP Error {response}.')
        return True


    def remove_osimage(self):
        """
        Method to remove a osimage in Luna Configuration.
        """
        for remove in ['debug', 'command', 'action']:
            self.args.pop(remove, None)
        payload = self.args
        if payload:
            self.logger.debug(f'Payload => {payload}')
            response = Rest().get_delete(self.table, payload['name'])
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} is deleted.')
            else:
                Helper().show_error(f'HTTP Error {response}.')
        return True


    def clone_osimage(self):
        """
        Method to rename a osimage in Luna Configuration.
        """
        payload = {}
        for remove in ['debug', 'command', 'action']:
            self.args.pop(remove, None)
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            response = Rest().post_clone(self.table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response == 201:
                Helper().show_success(f'{self.table.capitalize()}, {payload["name"]} cloneed as {payload["newosimage"]}.')
            else:
                Helper().show_error(f'HTTP Error {response}.')
        else:
            Helper().show_error(f'Nothing to update in {payload["name"]}.')
        return True


    def pack_osimage(self):
        """
        Method to pack the OS Image
        """
        process1 = Process(target=Helper().loader, args=("OS Image Packing...",))
        process1.start()
        response = False
        uri = f'config/{self.table}/{self.args["name"]}/_pack'
        result = Rest().get_raw(uri)
        if result.status_code == 200:
            http_response = result.json()
            if 'request_id' in http_response.keys():
                uri = f'config/status/{http_response["request_id"]}'
                def dig_packing_status(uri):
                    result = Rest().get_raw(uri)
                    if result.status_code == 400:
                        process1.terminate()
                        return True
                    elif result.status_code == 200:
                        http_response = result.json()
                        if http_response['message']:
                            message = http_response['message'].split(';;')
                            for msg in message:
                                sleep(2)
                                print(colored(msg, 'yellow', attrs=['bold']))
                        sleep(2)
                        return dig_packing_status(uri)
                    else:
                        return False
                response = dig_packing_status(uri)
        if response:
            print(colored(f'[========] OS Image {self.args["name"]} Packed.', 'green', attrs=['bold']))
        else:
            print(colored("[X ERROR X] Try Again!", 'red', attrs=['bold']))
        return response


    def kernel_osimage(self):
        """
        Method to change kernel version from an
        OS Image
        """
        payload = {}
        for remove in ['debug', 'command', 'action']:
            self.args.pop(remove, None)
        payload = {k: v for k, v in self.args.items() if v is not None}
        if payload:
            request_data = {'config':{self.table:{payload['name']: payload}}}
            self.logger.debug(f'Payload => {request_data}')
            self.logger.debug(f'Change Kernel URI => {payload["name"]}/_kernel')
            response = Rest().post_data(self.table, payload['name']+'/_kernel', request_data)
            self.logger.debug(f'Response => {response}')
            if response == 204:
                Helper().show_success(f'OS Image {self.args["name"]} Kernel updated.')
            else:
                Helper().show_error(f'HTTP Error Code: {response}.')
        return True
