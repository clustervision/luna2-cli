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
__status__      = "Development"

from operator import methodcaller
from time import sleep
from multiprocessing import Process
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log

class OSImage():
    """
    OSImage Class responsible to show, list, add, change,
    remove, rename, clone, pack and kernel update for the OSImage.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "osimage"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "member", "add", "change", "rename", "clone", "remove",
                       "pack", "kernel"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_osimage')
                call(self)
            else:
                Helper().show_error(f"Kindly choose from {actions}.")
        else:
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
        osimage_show.add_argument('name', help='OSImage Name')
        Helper().common_list_args(osimage_show)
        osimage_member = osimage_args.add_parser('member', help='OS Image Used by Nodes')
        osimage_member.add_argument('name', help='OS Image Name')
        Helper().common_list_args(osimage_member)
        osimage_add = osimage_args.add_parser('add', help='Add OSImage')
        osimage_add.add_argument('name', help='OSImage Name')
        osimage_add.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        osimage_add.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        osimage_add.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        osimage_add.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_add.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_add.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        osimage_add.add_argument('-o', '--kerneloptions', help='Kernel Options')
        osimage_add.add_argument('-ver', '--kernelversion', help='Kernel Version')
        osimage_add.add_argument('-p', '--path', required=True, help='Path of image')
        osimage_add.add_argument('-tar', '--tarball', help='Tarball UUID')
        osimage_add.add_argument('-t', '--torrent', help='Torrent UUID')
        osimage_add.add_argument('-D', '--distribution', help='Distribution')
        osimage_add.add_argument('-c', '--comment', action='store_true', help='Comment')
        osimage_add.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        osimage_add.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        osimage_change = osimage_args.add_parser('change', help='Change OSImage')
        osimage_change.add_argument('name', help='OSImage Name')
        osimage_change.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        osimage_change.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        osimage_change.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        osimage_change.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_change.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_change.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        osimage_change.add_argument('-o', '--kerneloptions', help='Kernel Options')
        osimage_change.add_argument('-ver', '--kernelversion', help='Kernel Version')
        osimage_change.add_argument('-p', '--path', help='Path of image')
        osimage_change.add_argument('-tar', '--tarball', help='Tarball UUID')
        osimage_change.add_argument('-t', '--torrent', help='Torrent UUID')
        osimage_change.add_argument('-D', '--distribution', help='Distribution')
        osimage_change.add_argument('-c', '--comment', action='store_true', help='Comment')
        osimage_change.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        osimage_change.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        osimage_clone = osimage_args.add_parser('clone', help='Clone OSImage')
        osimage_clone.add_argument('name', help='OSImage Name')
        osimage_clone.add_argument('newosimage', help='New OSImage Name')
        osimage_clone.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        osimage_clone.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        osimage_clone.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        osimage_clone.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_clone.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_clone.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        osimage_clone.add_argument('-o', '--kerneloptions', help='Kernel Options')
        osimage_clone.add_argument('-ver', '--kernelversion', help='Kernel Version')
        osimage_clone.add_argument('-p', '--path', required=True, help='Path of image')
        osimage_clone.add_argument('-tar', '--tarball', help='Tarball UUID')
        osimage_clone.add_argument('-t', '--torrent', help='Torrent UUID')
        osimage_clone.add_argument('-D', '--distribution', help='Distribution')
        osimage_clone.add_argument('-c', '--comment', action='store_true', help='Comment')
        osimage_clone.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        osimage_clone.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        osimage_rename = osimage_args.add_parser('rename', help='Rename OSImage')
        osimage_rename.add_argument('name', help='OSImage Name')
        osimage_rename.add_argument('newosimage', help='New OSImage Name')
        osimage_rename.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        osimage_remove = osimage_args.add_parser('remove', help='Remove OSImage')
        osimage_remove.add_argument('name', help='Name of the OS Image')
        osimage_remove.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        osimage_pack = osimage_args.add_parser('pack', help='Pack OSImage')
        osimage_pack.add_argument('name', help='Name of the OS Image')
        osimage_pack.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        osimage_kernel = osimage_args.add_parser('kernel', help='Chnage Kernel Version in OS Image')
        osimage_kernel.add_argument('name', help='Name of the OS Image')
        osimage_kernel.add_argument('-rd', '--initrdfile', help='INIT RD File')
        osimage_kernel.add_argument('-k', '--kernelfile', help='Kernel File')
        osimage_kernel.add_argument('-ver', '--kernelversion', help='Kernel Version')
        osimage_kernel.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_osimage(self):
        """
        This method list all osimages.
        """
        return Helper().get_list(self.table, self.args)


    def show_osimage(self):
        """
        This method show a specific osimage.
        """
        return Helper().show_data(self.table, self.args)


    def member_osimage(self):
        """
        This method will show all Nodes boots with the OSimage.
        """
        return Helper().member_record(self.table, self.args)


    def add_osimage(self):
        """
        This method add a osimage.
        """
        return Helper().add_record(self.table, self.args)


    def change_osimage(self):
        """
        This method update a osimage.
        """
        return Helper().update_record(self.table, self.args)


    def rename_osimage(self):
        """
        This method rename a osimage.
        """
        return Helper().rename_record(self.table, self.args, self.args["newosimage"])


    def remove_osimage(self):
        """
        This method remove a osimage.
        """
        return Helper().delete_record(self.table, self.args)


    def clone_osimage(self):
        """
        This method clone a osimage.
        """
        response = False
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
        request_data = {'config':{self.table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        result = Rest().post_clone(self.table, payload['name'], request_data)
        if result.status_code == 200:
            process1 = Process(target=Helper().loader, args=("OS Image Cloning...",))
            process1.start()
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
                                print(msg)
                        sleep(2)
                        return dig_packing_status(uri)
                    else:
                        return False

                response = dig_packing_status(uri)
        if response:
            print(f'[========] OS Image {self.args["newosimage"]} Cloned.')
        else:
            print("[X ERROR X] Try Again!")
        return response


    def pack_osimage(self):
        """
        This method pack a osimage.
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
                                print(msg)
                        sleep(2)
                        return dig_packing_status(uri)
                    else:
                        return False
                response = dig_packing_status(uri)
        if response:
            print(f'[========] Image {self.args["name"]} Packed.')
        else:
            print("[X ERROR X] Try Again!")
        return response


    def kernel_osimage(self):
        """
        This method change kernel version and pack
        a osimage again.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.args)
        request_data = {'config':{self.table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        self.logger.debug(f'Change Kernel URI => {payload["name"]}/_kernel')
        response = Rest().post_data(self.table, payload['name']+'/_kernel', request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Helper().show_success(f'OS Image {self.args["name"]} Kernel updated.')
        else:
            Helper().show_error(f'HTTP Error Code {response.status_code}.')
            Helper().show_error(f'HTTP Error {response.content}.')
        return True
