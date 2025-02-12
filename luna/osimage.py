#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>


"""
Main Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.1"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from operator import methodcaller
from time import sleep
from multiprocessing import Process
from luna.utils.helper import Helper
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.constant import actions
from luna.utils.message import Message
from luna.utils.arguments import Arguments
from luna.utils.presenter import Presenter

class OSImage():
    """
    OSImage Class responsible to show, list, add, change,
    remove, rename, clone, pack and kernel update for the OSImage.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "osimage"
        self.actions = actions(self.table)
        self.tag_actions = actions("tag_osimage")
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                if self.args["action"] == 'tag':
                    if self.args["tag_action"] is None:
                        call = methodcaller('list_tag')
                        call(self)
                    else:
                        call = methodcaller(f'{self.args["tag_action"]}_tag')
                        call(self)
                else:
                    call = methodcaller(f'{self.args["action"]}_osimage')
                    call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the OSImage class.
        """
        osimage_menu = subparsers.add_parser('osimage', help='OSImage operations.')
        osimage_args = osimage_menu.add_subparsers(dest='action')
        osimage_list = osimage_args.add_parser('list', help='List OSImages')
        Arguments().common_list_args(osimage_list)
        osimage_show = osimage_args.add_parser('show', help='Show a OSImage')
        osimage_show.add_argument('name', help='OSImage Name')
        Arguments().common_list_args(osimage_show)
        osimage_member = osimage_args.add_parser('member', help='OS Image Used by Nodes')
        osimage_member.add_argument('name', help='OS Image Name')
        Arguments().common_list_args(osimage_member)
        osimage_add = osimage_args.add_parser('add', help='Add OSImage')
        Arguments().common_osimage_args(osimage_add)
        osimage_change = osimage_args.add_parser('change', help='Change OSImage')
        Arguments().common_osimage_args(osimage_change)
        osimage_change.add_argument('-t', '--tag', help='OS Image Tag')
        osimage_clone = osimage_args.add_parser('clone', help='Clone OSImage')
        Arguments().common_osimage_args(osimage_clone)
        osimage_clone.add_argument('-t', '--tag', help='OS Image Tag')
        osimage_clone.add_argument('--nocopy', action='store_true', default=None, help='No Copy OS Image')
        osimage_clone.add_argument('-b', '--bare', action='store_true', default=None, help='Bare OS Image(Exclude Packing)')
        osimage_clone.add_argument('newosimage', help='New OSImage Name')
        osimage_rename = osimage_args.add_parser('rename', help='Rename OSImage')
        osimage_rename.add_argument('name', help='OSImage Name')
        osimage_rename.add_argument('newosimage', help='New OSImage Name')
        osimage_rename.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        osimage_remove = osimage_args.add_parser('remove', help='Remove OSImage')
        osimage_remove.add_argument('name', help='Name of the OS Image')
        osimage_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        osimage_pack = osimage_args.add_parser('pack', help='Pack OSImage')
        osimage_pack.add_argument('name', help='Name of the OS Image')
        osimage_pack.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        osimage_kernel = osimage_args.add_parser('kernel', help='Change Kernel Version in OS Image')
        osimage_kernel.add_argument('name', help='Name of the OS Image')
        osimage_kernel.add_argument('-r', '--initrdfile', help='INIT RD File')
        osimage_kernel.add_argument('-f', '--kernelfile', help='Kernel File')
        osimage_kernel.add_argument('-k', '--kernelversion', help='Kernel Version')
        osimage_kernel.add_argument('-b', '--bare', action='store_true', default=None,
                                    help='Bare OS Image(Exclude Packing)')
        osimage_kernel.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')

        tag_menu = osimage_args.add_parser('tag', help='Tag OS Image')
        tag_menu.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        tag_menu.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        tag_args = tag_menu.add_subparsers(dest='tag_action')

        tag_show = tag_args.add_parser('show', help='Show a OS Image Tag')
        tag_show.add_argument('name', help='OSImage Name')
        Arguments().common_list_args(tag_show)

        tag_change = tag_args.add_parser('change', help='Change a OS Image Tag')
        tag_change.add_argument('name', help='OSImage Name')
        tag_change.add_argument('tag', help='OS Image Tag Name')
        tag_change.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')

        tag_remove = tag_args.add_parser('remove', help='Delete a OS Image Tag')
        tag_remove.add_argument('name', help='OSImage Name')
        tag_remove.add_argument('tag', help='OS Image Tag Name')
        tag_remove.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')


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
        payload = Helper().prepare_payload(self.table, self.args)
        request_data = {'config':{self.table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        result = Rest().post_clone(self.table, payload['name'], request_data)
        if result.status_code == 200:
            http_response = result.content
            if 'request_id' in http_response.keys():
                process1 = Process(target=Helper().loader, args=("OS Image Cloning...",))
                process1.start()
                uri = f'config/status/{http_response["request_id"]}'
                def dig_packing_status(uri):
                    result = Rest().get_raw(uri)
                    if result.status_code == 404:
                        process1.terminate()
                        return True
                    elif result.status_code == 200:
                        http_response = result.json()
                        if http_response['message']:
                            message = http_response['message'].split(';;')
                            for msg in message:
                                sleep(2)
                                Message().show_success(f'{msg}')
                        sleep(2)
                        return dig_packing_status(uri)
                    else:
                        return False

                response = dig_packing_status(uri)
        if response:
            Message().show_success(f'[========] OS Image {self.args["newosimage"]} Cloned.')
        else:
            Message().error_exit(result.content, result.status_code)
        return response


    def pack_osimage(self):
        """
        This method pack a osimage.
        """
        response = False
        uri = f'config/{self.table}/{self.args["name"]}/_pack'
        result = Rest().get_raw(uri)
        if result.status_code == 200:
            http_response = result.json()
            if http_response['message']:
                if len(http_response['message']) > 5:
                    message = http_response['message'].split(';;')
                    for msg in message:
                        sleep(2)
                        Message().show_success(f'{msg}')
                else:
                    Message().show_success(f'{http_response["message"]}')

            if 'request_id' in http_response.keys():
                process1 = Process(target=Helper().loader, args=("OS Image Packing...",))
                process1.start()
                uri = f'config/status/{http_response["request_id"]}'

                def dig_packing_status(uri):
                    sleep(2)
                    result = Rest().get_raw(uri)
                    if result.status_code == 404:
                        process1.terminate()
                        return True
                    elif result.status_code == 200:
                        http_response = result.json()
                        if http_response['message']:
                            if len(http_response['message']) > 5:
                                message = http_response['message'].split(';;')
                                for msg in message:
                                    sleep(2)
                                    Message().show_success(f'{msg}')
                            else:
                                Message().show_success(f'{http_response["message"]}')
                        return dig_packing_status(uri)
                    else:
                        return False
                response = dig_packing_status(uri)
        if response:
            Message().show_success(f'[========] Image {self.args["name"]} Packed.')
        else:
            Message().error_exit(result.content, result.status_code)
        return response


    def kernel_osimage(self):
        """
        This method change kernel version and pack a osimage again.
        """
        for remove in ['verbose', 'command', 'action']:
            self.args.pop(remove, None)
        payload = Helper().prepare_payload(self.table, self.args)
        request_data = {'config':{self.table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        self.logger.debug(f'Change Kernel URI => {payload["name"]}/kernel')
        result = Rest().post_data(self.table, payload['name']+'/kernel', request_data)
        if result.status_code == 204:
            Message().show_success(f'OS Image {self.args["name"]} Kernel is updated.')
        elif result.status_code == 200:
            response = False
            http_response = result.content
            if http_response['message']:
                if len(http_response['message']) > 5:
                    message = http_response['message'].split(';;')
                    for msg in message:
                        sleep(2)
                        Message().show_success(f'{msg}')
                else:
                    Message().show_success(f'{http_response["message"]}')

            if 'request_id' in http_response.keys():
                process1 = Process(target=Helper().loader, args=("OS Image Kernel Updating...",))
                process1.start()
                uri = f'config/status/{http_response["request_id"]}'
                def dig_packing_status(uri):
                    sleep(2)
                    result = Rest().get_raw(uri)
                    if result.status_code == 404:
                        process1.terminate()
                        return True
                    elif result.status_code == 200:
                        http_response = result.json()
                        if http_response['message']:
                            message = http_response['message'].split(';;')
                            for msg in message:
                                sleep(2)
                                Message().show_success(f'{msg}')
                        return dig_packing_status(uri)
                    else:
                        return False
                response = dig_packing_status(uri)
            if response:
                Message().show_success(f'[========] Image {self.args["name"]} Packed.')
            else:
                Message().error_exit(result.content, result.status_code)
        else:
            Message().error_exit(f'{result.content}', result.status_code)
        return True


    def list_tag(self):
        """
        This method list all osimage Tags.
        """
        return Helper().get_list("osimagetag", self.args)


    def show_tag(self):
        """
        This method show a specific osimage tag.
        """
        get_list = Rest().get_data("osimagetag", self.args['name'])
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config']["osimagetag"]
            if self.args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                # fields, rows  = Helper().filter_data("osimagetag", data)
                fields, osimage, rows  = Helper().filter_osimage_col("osimagetag", data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << OS Image Tags for {self.args["name"]} >>'
                # response = Presenter().show_table(title, fields, rows)
                # response = Presenter().show_table_col(title, fields, rows)
                response = Presenter().show_table_col_more_fields(title, fields, osimage, rows)
        else:
            response = Message().show_error(f'OS Image Tags is not found for {self.args["name"]}.')
        return response


    def change_tag(self):
        """
        This method update a osimage tag.
        """
        for remove in ['verbose', 'command', 'action', 'raw', 'tag_action']:
            self.args.pop(remove, None)
        request_data = {'config': {self.table: {self.args['name']: {'tag': self.args['tag']}}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(self.table, f"{self.args['name']}/tag", request_data)
        if response.status_code == 204:
            Message().show_success(f'OS Image {self.args["name"]} Tag {self.args["tag"]} is Updated.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def remove_tag(self):
        """
        This method remove a osimage tag.
        """
        route = f'/config/{self.table}/{self.args["name"]}/osimagetag/{self.args["tag"]}/_delete'
        response = Rest().get_raw(route)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Message().show_success(f'OS Image {self.args["name"]} Tag {self.args["tag"]} is removed.')
        else:
            if response.content:
                message = response.json()
                Message().error_exit(message["message"], response.status_code)
            else:
                Message().error_exit(
                    f'Tag {self.args["tag"]} is deleted for {self.args["name"]}.',
                    response.status_code
                )
        return True
