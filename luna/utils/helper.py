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
Helper Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.1"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import os
from time import time, sleep
import base64
import binascii
import subprocess
import re
from random import randint
from os import getpid
from multiprocessing import Process
from copy import deepcopy
import urllib3
import hostlist
from termcolor import colored
from nested_lookup import nested_lookup, nested_update, nested_delete, nested_alter
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.presenter import Presenter
from luna.utils.constant import EDITOR_KEYS, BOOL_KEYS, filter_columns, sortby, divider, overrides
from luna.utils.message import Message


class Helper():
    """
    All kind of helper methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.logger = Log.get_logger()


    @staticmethod
    def get_all_names(table):
        """
        Return a sorted list of all names for the given table (e.g. 'node', 'osimage', 'network').
        """
        try:
            get_list = Rest().get_data(table)
            if get_list.status_code == 200:
                content = get_list.content
                if content and "config" in content and table in content["config"]:
                    return sorted(content["config"][table].keys())
        except Exception:
            pass
        return []


    def name_completer(self, kind):
        """
        This method returns a completer function for the given kind of resource.
        """
        def completer(prefix, parsed_args, **kwargs):
            """
            Completer function that returns a list of names starting with the given prefix.
            """
            self.logger.info(f"prefix: {type(prefix)} {prefix}")
            return [n for n in self.get_all_names(kind) if n.startswith(prefix)]
        return completer


    def secret_name_completer(self, kind, entity=None):
        """
        This method returns a completer function for the given kind of resource.
        """
        def completer(prefix, parsed_args, **kwargs):
            """
            Completer function that returns a list of names starting with the given prefix.
            """
            self.logger.info(f"prefix: {type(prefix)} {prefix}")
            self.logger.info(f"parsed_args: {type(parsed_args)} {parsed_args}")
            self.logger.info(f"kind: {type(kind)} {kind}")
            self.logger.info(f"entity: {type(entity)} {entity}")
            entity_name = parsed_args.name
            uri = f'{kind}/{entity}/{entity_name}'
            self.logger.info(uri)
            get_list = Rest().get_data(uri)
            if get_list.status_code == 200:
                self.logger.info(get_list)
                get_list = get_list.content
                self.logger.info(get_list)
                node_secrets = get_list['config']['secrets'][entity][entity_name]
                return [item['name'] for item in node_secrets]
            else:
                self.logger.error(f"Failed to fetch secrets for {entity_name}: {get_list.content}")
                return []
        return completer


    def interface_name_completer(self, kind):
        """
        This method returns a completer function for the given kind of resource.
        """
        def completer(prefix, parsed_args, **kwargs):
            """
            Completer function that returns a list of names starting with the given prefix.
            """
            self.logger.info(f"prefix: {type(prefix)} {prefix}")
            self.logger.info(f"parsed_args: {type(parsed_args)} {parsed_args}")
            self.logger.info(f"kind: {type(kind)} {kind}")
            entity_name = parsed_args.name
            get_list = Rest().get_data(kind, entity_name+'/interfaces')
            self.logger.info(f"entity_name: {type(entity_name)} {entity_name}")
            self.logger.info(f"get_list.status_code: {type(get_list.status_code)} {get_list.status_code}")
            if get_list.status_code == 200:
                get_list = get_list.content
                node_interfaces = get_list['config'][kind][entity_name]['interfaces']
                self.logger.info(node_interfaces)
                return [item['interface'] for item in node_interfaces]
            else:
                self.logger.error(f"Failed to fetch secrets for {entity_name}: {get_list.content}")
                return []
        return completer


    def choice_to_bool(self, raw_data=None):
        """
        This method will convert string choices to
        boolean
        """
        for key in BOOL_KEYS:
            content = nested_lookup(key, raw_data)
            if content:
                if content[0] is not None:
                    if content[0] == '':
                        raw_data = nested_update(raw_data, key=key, value='')
                    elif content[0].lower() in ['y', 'yes', 'true']:
                        raw_data = nested_update(raw_data, key=key, value=True)
                    else:
                        raw_data = nested_update(raw_data, key=key, value=False)
        return raw_data


    def get_correct_option(self, table=None, name=None, interface=None):
        """
        This method will get the correct option value for the interface.
        """
        value = ''
        uri = name+'/interfaces/'+interface
        get_data = Rest().get_data(table, uri)
        if get_data.status_code == 200:
            value = nested_lookup('options', get_data.content)
            value = value[0]
        return value


    def prepare_payload(self, table=None, raw_data=None, local=False):
        """
        This method will prepare the payload.
        if local is true, it allows to edit local, now inherited data
        """
        raw_data = self.choice_to_bool(raw_data)
        payload = {k: v for k, v in raw_data.items() if v is not None}
        for key in EDITOR_KEYS:
            content = nested_lookup(key, payload)
            if content:
                if content[0] is True:
                    if table:
                        get_list = Rest().get_data(table, payload['name'])
                        if get_list.status_code == 200:
                            get_list = get_list.content
                        else:
                            Message().error_exit(get_list.content, get_list.status_code)
                        if get_list:
                            _source = nested_lookup('_'+key+'_source', get_list)
                            if _source:
                                if 'default' in _source:
                                    Message().show_warning(f"WARNING :: {key} contents are 'default'. changes will be set locally")
                                elif table not in _source and not local:
                                    Message().error_exit(f'WARNING :: {key} is currently inherited from parent. use --local to override')
                            if key == 'options':
                                interface = nested_lookup('interface', raw_data)
                                value = self.get_correct_option(table, raw_data['name'], interface[0])
                            else:
                                value = nested_lookup(key, get_list)
                                value = value[0]
                            if isinstance(value, (str, type(None))):
                                content = self.open_editor(key, value, payload)
                                payload = nested_update(payload, key=key, value=content)
                    else:
                        content = self.open_editor(key, None, payload)
                        payload = nested_update(payload, key=key, value=content)
                elif content[0] is False:
                    payload = nested_delete(payload, key)
                elif content[0]:
                    if os.path.exists(content[0]):
                        if os.path.isfile(content[0]):
                            with open(content[0], 'rb') as file_data:
                                content = self.base64_encode(file_data.read())
                                payload = nested_update(payload, key=key, value=content)
                        else:
                            Message().error_exit(f'ERROR :: {content[0]} is a Invalid filepath.')
                    else:
                        content = self.base64_encode(bytes(content[0], 'utf-8'))
                        payload = nested_update(payload, key=key, value=content)
        return payload


    def open_editor(self, key=None, value=None, payload=None):
        """
        This Method will open a default text editor to write the multiline text for keys such as
        comment, prescript, postscript, partscript, content etc. but not limited to them only.
        """
        response = ''
        editor = str(os.path.abspath(__file__)).replace('helper.py', 'editor.sh')
        os.chmod(editor, 0o0755)
        random_path = str(time())+str(randint(1001,9999))+str(getpid())
        tmp_folder = f'/tmp/lunatmp-{random_path}'
        os.mkdir(tmp_folder)
        if key == 'content':
            filename = f'/tmp/lunatmp-{random_path}/{payload["name"]}{key}'
        else:
            filename = f'/tmp/lunatmp-{random_path}/{key}'
        temp_file = open(filename, "x", encoding='utf-8')
        if value:
            value = self.base64_decode(value)
            temp_file.write(value)
            temp_file.close()
        subprocess.check_output(f"sed -i 's/\r$//' {editor}", shell=True)
        subprocess.call([editor, filename])
        subprocess.check_output(f"sed -i 's/\r$//' {filename}", shell=True)
        with open(filename, 'rb') as file_data:
            response = self.base64_encode(file_data.read())
        os.remove(filename)
        os.rmdir(tmp_folder)
        return response


    def get_list(self, table=None, args=None):
        """
        Method to list all switches from Luna Configuration.
        """
        response = False
        fields, rows = [], []
        get_list = Rest().get_data(table)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][table]
            if args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = self.filter_data(table, data)
                # fields = list(map(lambda x: x.replace('tpm_uuid', 'tpm_present'), fields))
                # fields = list(map(lambda x: x.replace('ns_ip', 'nameserver'), fields))
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {table.capitalize()} >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'{table} is not found.')
        return response


    def get_controllers(self, detail=None):
        """
        Method to show a switch in Luna Configuration. Detail True will return the full details.
        """
        # print("--------Detail True---------")
        # print(Helper().get_controllers(detail=True))
        # print("---------Detail False--------")
        # print(Helper().get_controllers(detail=False))
        # print("--------Detail None---------")
        # print(Helper().get_controllers())
        # print("---------END--------")

        response = {'controllers': []} if detail is True else []
        urllib3.disable_warnings()
        check = Rest().daemon_validation(parser=True)
        if check is not True:
            get_list = Rest().get_data('cluster')
            if get_list.status_code == 200:
                get_list = get_list.content
            else:
                Message().error_exit(get_list.content, get_list.status_code)
            self.logger.debug(f'Get List Data from Helper => {get_list}')
            if get_list:
                data = get_list['config']['cluster']
                json_data = Helper().prepare_json(data)
                for key, value in json_data.items():
                    if isinstance(value, dict):
                        response['controllers'].append(json_data[key]) if detail is True else response.append(key) # pylint: disable=W0106
            else:
                response = Message().show_error('Cluster is unavailable at this moment.')
        return response


    def show_data(self, table=None, args=None):
        """
        Method to show a switch in Luna Configuration.
        """
        row_name = None
        if 'name' in args:
            row_name = args['name']
        get_list = Rest().get_data(table, row_name)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            if row_name:
                data = get_list['config'][table][row_name]
            else:
                data = get_list['config'][table]
            json_data = Helper().prepare_json(data)
            if args['raw']:
                response = Presenter().show_json(json_data)
            else:
                div = divider(table)
                limit = True
                if "full_scripts" in args:
                    limit = False if args["full_scripts"] == True else True
                data = Helper().prepare_json(data, limit)
                fields, rows  = self.filter_data_col(table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{table.capitalize()} => {data["name"]}'
                response = Presenter().show_table_col(title, fields, rows, div)
        else:
            response = Message().show_error(f'{args["name"]} is not found in {table}.')
        return response


    def member_record(self, table=None, args=None):
        """
        This method fetch the nodes to the provided entity.
        """
        response = False
        get_list = Rest().get_data(table, args['name']+'/_member')
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][table][args["name"]]['members']
            data = Helper().prepare_json(data)
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                num = 1
                fields = ['#', 'Nodes']
                rows = []
                for member in data:
                    new_row = [num, member]
                    rows.append(new_row)
                    num = num + 1
                title = f'<< {table.capitalize()} {args["name"]} Member Nodes >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'{table} {args["name"]} not have any node.')
        return response


    def reserved_ip(self, args=None):
        """
        This method will fetch all the reserved IP Address for a network.
        """
        response = False
        get_list = Rest().get_data('network', args['name']+'/_member')
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config']['network'][args["name"]]['taken']
            data = Helper().prepare_json(data)
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                num = 1
                fields = ['#', 'IP Address', 'Device Name']
                rows = []
                for each in data:
                    new_row = [num, each['ipaddress'], each['device']]
                    rows.append(new_row)
                    num = num + 1
                title = f'<< Reserved IP Addresses for Network {args["name"]} >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'Network {args["name"]} not have any IP reserved.')
        return response


    def add_record(self, table=None, data=None):
        """
        This method will add a new record.
        """
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        payload = self.prepare_payload(None, data)
        request_data = {'config':{table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        record = Rest().get_data(table, payload['name'])
        if record.status_code == 200:
            message = f'{payload["name"]} already present in {table.capitalize()}'
            Message().error_exit(message, record.status_code)
        else:
            response = Rest().post_data(table, payload['name'], request_data)
            self.logger.debug(f'Response => {response}')
            if response.status_code == 201:
                Message().show_success(response.content)
            else:
                Message().error_exit(response.content, response.status_code)
        return True


    def update_record(self, table=None, data=None, local=False):
        """
        This method will update a record.
        """
        response = None
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        if 'raw' in data:
            data.pop('raw', None)
        payload = self.prepare_payload(table, data, local)
        name = None
        if 'name' in payload:
            name = payload['name']
            request_data = {'config':{table:{name: payload}}}
        else:
            request_data = {'config':{table: payload}}
        if 'cluster' in table:
            request_data = {'config':{table: payload}}
        self.logger.debug(f'Payload => {request_data}')
        if 'cluster' in table:
            response = Rest().post_data(table, None, request_data)
        else:
            record = Rest().get_data(table, payload['name'])
            if record.status_code == 200:
                if len(payload) == 1:
                    Message().error_exit('Kindly choose something to update.')
                else:
                    response = Rest().post_data(table, name, request_data)
            else:
                Message().error_exit(f'Kindly add the {payload["name"]} first', record.status_code)
        self.logger.debug(f'Response => {response}')
        if response:
            if response.status_code == 204:
                if name:
                    Message().show_success(f'{table.capitalize()} {name} is updated.')
                else:
                    Message().show_success(f'{table.capitalize()} is updated.')
            else:
                Message().error_exit(response.content, response.status_code)
        return True


    def compare_data(self, table=None, data=None):
        """
        This method will compare the payload data with the original data.
        """
        check = False
        db_data = Rest().get_data(table, data['name'])
        if db_data.status_code == 200:
            db_data = db_data.content
        else:
            Message().error_exit(db_data.content, db_data.status_code)
        self.logger.debug(f'Get List Data from Helper => {db_data}')
        db_data = db_data['config'][table][data['name']]
        db_data = Helper().prepare_json(db_data)
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        data = {k: v for k, v in data.items() if v is not None}
        for key, value in data.items():
            if key in EDITOR_KEYS:
                if value is False:
                    data = nested_delete(data, key)
        final_data = deepcopy(data)
        for key, value in data.items():
            if key in db_data:
                if db_data[key] != value:
                    self.logger.debug(f"key   {key} value   {db_data[key]} value   {value}")
                    check = True
                del final_data[key]
            else:
                check = True

        if 'interface' in final_data:
            uri = data['name']+'/interfaces/'+final_data['interface']
            interface_data = Rest().get_data(table, uri)
            if interface_data.status_code == 200:
                interface_data = interface_data.content
                if isinstance(interface_data, str):
                    check = True
                else:
                    interface_data = interface_data['config'][table][data["name"]]['interfaces'][0]
                    interface_data = Helper().prepare_json(interface_data)
                    interface_data = self.remove_none(interface_data)
                    for key, value in final_data.items():
                        if key not in interface_data:
                            check = True
                            self.logger.debug(f"-----------------------different~~~~~   {key}")
                        else:
                            if value != interface_data[key]:
                                check = True
                                self.logger.debug(f"-----------------------different   {key}")
            else:
                check = True
        return check


    def remove_none(self, data=None):
        """
        This method will remove the None values recursively from the object.
        """
        if isinstance(data, (list, tuple, set)):
            return type(data)(self.remove_none(x) for x in data if x is not None)
        elif isinstance(data, dict):
            return type(data)((self.remove_none(k), self.remove_none(v))
            for k, v in data.items() if k is not None and v is not None)
        else:
            return data


    def delete_record(self, table=None, data=None):
        """
        This method will delete a record.
        """
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        self.logger.debug(f'Payload => {data}')
        response = Rest().get_delete(table, data['name'])
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Message().show_success(f'{table.capitalize()} {data["name"]} is removed.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def rename_record(self, table=None, data=None, newname=None):
        """
        This method will rename a record.
        """
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        request_data = {'config':{table:{data['name']: data}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(table, data['name'], request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Message().show_success(f'{table.capitalize()} {data["name"]} is renamed to {newname}.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def clone_record(self, table=None, data=None):
        """
        This method will clone a record.
        """
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        payload = self.prepare_payload(table, data)
        request_data = {'config':{table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_clone(table, payload['name'], request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 201:
            Message().show_success(response.content)
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def grab_osimage(self, table=None, data=None):
        """
        Method to grab an osimage for a node.
        """
        process1 = Process(target=Helper().loader, args=("OS Image Grabbing...",))
        process1.start()
        response = False
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        uri = f'config/{table}/{data["name"]}/_osgrab'
        data = self.prepare_payload(table, data)
        request_data = {'config':{table:{data['name']: data}}}
        self.logger.debug(f'Payload => {data}')
        http_response = Rest().post_raw(uri, request_data)
        result = http_response
        if http_response.status_code == 200:
            http_response = http_response.json()
            if 'request_id' in http_response.keys():
                uri = f'config/status/{http_response["request_id"]}'
                def dig_grabbing_status(uri):
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
                        return dig_grabbing_status(uri)
                    else:
                        return False
                response = dig_grabbing_status(uri)
        if response:
            Message().show_success(f'[========] OS Image Grabbed for node {data["name"]}.')
        else:
            Message().error_exit(result.content, result.status_code)
        return True


    def push_osimage(self, table=None, data=None):
        """
        Method to push an osimage for a node or a group.
        """
        process1 = Process(target=Helper().loader, args=("OS Image Pushing...",))
        process1.start()
        response = False
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        uri = f'config/{table}/{data["name"]}/_ospush'
        data = self.prepare_payload(table, data)
        request_data = {'config':{table:{data['name']: data}}}
        self.logger.debug(f'Payload => {data}')
        http_response = Rest().post_raw(uri, request_data)
        result = http_response
        if http_response.status_code == 200:
            http_response = http_response.json()
            if 'request_id' in http_response.keys():
                uri = f'config/status/{http_response["request_id"]}'
                def dig_push_status(uri):
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
                        return dig_push_status(uri)
                    else:
                        return False
                response = dig_push_status(uri)
        if response:
            Message().show_success(f'[========] OS Image Pushed for {table}  {data["name"]}.')
        else:
            Message().error_exit(result.content, result.status_code)
        return True


    def get_hostlist(self, raw_hosts=None):
        """
        This method will perform power option on node.
        """
        response = []
        self.logger.debug(f'Received hostlist: {raw_hosts}.')
        try:
            response = hostlist.expand_hostlist(raw_hosts)
            self.logger.debug(f'Expanded hostlist: {response}.')
        except hostlist.BadHostlist:
            self.logger.debug(f'Hostlist is incorrect: {raw_hosts}.')
        return response


    def luna_hostlist(self, raw_hosts=None):
        """
        This method will perform power option on node.
        """
        response = []
        for each in raw_hosts:
            if '..' in each:
                host_range = re.findall(r'\d+', each)
                if len(host_range) != 2:
                    Message().error_exit(f"Incorrect Hostlist: {each}")
                rectify = each.replace('..', '')
                for raw in host_range:
                    rectify = rectify.replace(raw, '')
                rectify = f'{rectify}[{host_range[0]}-{host_range[1]}]'
                rectify = self.get_hostlist(rectify)
                response = response + rectify
            else:
                response.append(each)
        return response


    def common_list_args(self, parser=None):
        """
        This method will provide the common list and show arguments..
        """
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        parser.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        return parser


    def loader(self, message=None):
        """
        This method is a loader, will run while transactions happens.
        """
        animation = [
        f"[=       ] {message}",
        f"[===     ] {message}",
        f"[====    ] {message}",
        f"[=====   ] {message}",
        f"[======  ] {message}",
        f"[======= ] {message}",
        f"[========] {message}",
        f"[ =======] {message}",
        f"[  ======] {message}",
        f"[   =====] {message}",
        f"[    ====] {message}",
        f"[     ===] {message}",
        f"[      ==] {message}",
        f"[       =] {message}",
        f"[        ] {message}",
        f"[        ] {message}",        ]
        not_complete = True
        i = 0
        try:
            while not_complete:
                print(animation[i % len(animation)], end='\r')
                sleep(.1)
                i += 1
        except KeyboardInterrupt:
            return False
        return True


    def control_print(self, system=None, content=None, count=None):
        """
        This method will parse the data for Control API's.
        """
        result = {}
        possible_cases = ['ok', 'on', 'off']
        if 'failed' in content['control']:
            for key, value in content['control']['failed'].items():
                result[key] = value

        if system in content['control']:
            for case in possible_cases:
                if case in content['control'][system]:
                    for key, value in content['control'][system][case].items():
                        result[key] = case.upper()
        result = dict(sorted(result.items()))

        header = "| #     |     Node Name      |       "
        header += "Status                                              |"
        hr_line = 'X--------------------------------------------'
        hr_line += '--------------------------------------------X'
        rows = []
        for key, value in result.items():
            rows.append([count, key, value])
            count = count + 1

        if rows:
            for row in rows:
                if row[0] == 1:
                    Message().show_success(hr_line)
                    Message().show_success(header)
                    Message().show_success(hr_line)
                row[0] = f'{row[0]}'.ljust(6)
                row[1] = f'{row[1]}'.ljust(19)
                row[2] = f'{row[2]}'.ljust(58)
                line = f'| {row[0]}| {row[1]}| {row[2]}|'
                Message().show_success(line)
        return count


    def dig_control_status(self, request_id=None, count=None, system=None):
        """
        This method will fetch the status of Control API.
        """
        uri = f'control/status/{request_id}'
        sleep(2)
        status = Rest().get_raw(uri)
        status_json = status.json()
        if status.status_code == 200:
            count = Helper().control_print(system, status_json, count)
            return self.dig_control_status(request_id, count, system)
        elif status.status_code == 404:
            hr_line = 'X--------------------------------------------'
            hr_line += '--------------------------------------------X'
            Message().show_success(hr_line)
        else:
            Message().show_error(f"Something Went Wrong {status.status_code}")


    def filter_interface(self, table=None, data=None):
        """
        This method will generate the data as for
        row format from the interface
        """
        
        self.logger.debug(f'table => {table}')
        self.logger.debug(f'data => {data}')
        fields, rows, colored_fields = [], [], []
        fields = filter_columns(table)
        self.logger.debug(f'fields => {fields}')
        for field_key in fields:
            val_row = []
            for ele in data:
                if field_key in list(ele.keys()):
                    if ele[field_key] == 'in progress':
                        val_row.append(colored('in progress', 'green'))
                    elif ele[field_key] == 'queued':
                        val_row.append(colored('queued', 'yellow'))
                    elif ele[field_key] == 1:
                        val_row.append(colored('yes', 'green'))
                    elif ele[field_key] == 0:
                        val_row.append(colored('no', 'yellow'))
                    elif ele[field_key] == 'maintask':
                        val_row.append(colored('Main Task', 'blue'))
                    elif ele[field_key] == 'subtask':
                        val_row.append(colored('Sub Task', 'magenta'))
                    else:
                        val_row.append(ele[field_key])
                else:
                    val_row.append("--NA--")
                self.logger.debug(f'Element => {ele}')
            rows.append(val_row)
            val_row = []
            colored_fields.append(field_key)
        fields = colored_fields
        self.logger.debug(f'Rows before Swapping => {rows}')
        final_rows = []
        for array in range(len(rows[0])) :
            tmp = []
            for element in rows:
                tmp.append(element[array])
            final_rows.append(tmp)
        rows = final_rows
        # Adding Serial Numbers to the dataset
        fields.insert(0, '#')
        num = 1
        for outer in rows:
            outer.insert(0, num)
            num = num + 1
        # Adding Serial Numbers to the dataset
        return fields, rows


    def filter_data(self, table=None, data=None):
        """
        This method will generate the data as for
        row format
        """
        self.logger.debug(f'Table => {table}')
        self.logger.debug(f'Data => {data}')
        fields, rows, colored_fields = [], [], []
        fields = filter_columns(table)
        self.logger.debug(f'Fields => {fields}')
        datacopy=data.copy()
        for ele in datacopy.keys():
            if '_override' in datacopy[ele]:
                if datacopy[ele]['_override'] and 'name' in datacopy[ele]:
                    data[ele]['name'] = f"{data[ele]['name']} *"
                del data[ele]['_override']
                if '_override' in fields:
                    fields.remove('_override')
        for field_key in fields:
            val_row = []
            num = 1
            for ele in data:
                if field_key in list((data[ele].keys())):
                    if isinstance(data[ele][field_key], list):
                        new_list = []
                        for internal in data[ele][field_key]:
                            for internal_val in internal:
                                self.logger.debug(f'Key => {internal_val}')
                                self.logger.debug(f'Value => {internal[internal_val]}')
                                in_key = internal_val
                                in_val = internal[internal_val]
                                new_list.append(f'{in_key} = {in_val} ')
                        new_list = '\n'.join(new_list)
                        val_row.append(new_list)
                        new_list = []
                    elif field_key == 'tpm_uuid':
                        if data[ele][field_key]:
                            val_row.append(True)
                        else:
                            val_row.append(False)
                    else:
                        if table == "network":
                            if field_key == "network":
                                network = data[ele][field_key]
                                if "network_ipv6" in data[ele].keys():
                                    if data[ele]['network_ipv6'] not in ['', None]:
                                        network = f'{data[ele][field_key]}\n{data[ele]["network_ipv6"]}'
                                network = network if num == len(data) else f'{network}\n'
                                val_row.append(network)
                         
                            
                            elif field_key == "dhcp_range_begin":
                                dhcp_range_begin = data[ele][field_key]
                                if "dhcp_range_begin_ipv6" in data[ele].keys():
                                    if data[ele]['network_ipv6'] not in ['', None]:
                                        dhcp_range_begin = f'{data[ele][field_key]}\n{data[ele]["dhcp_range_begin_ipv6"]}'
                                dhcp_range_begin = dhcp_range_begin if num == len(data) else f'{dhcp_range_begin}\n'
                                val_row.append(dhcp_range_begin)
                           
                            
                            elif field_key == "dhcp_range_end":
                                dhcp_range_end = data[ele][field_key]
                                if "dhcp_range_end_ipv6" in data[ele].keys():
                                    if data[ele]['network_ipv6'] not in ['', None]:
                                        dhcp_range_end = f'{data[ele][field_key]}\n{data[ele]["dhcp_range_end_ipv6"]}'
                                dhcp_range_end = dhcp_range_end if num == len(data) else f'{dhcp_range_end}\n'
                                val_row.append(dhcp_range_end)
                            else:
                                val_row.append(data[ele][field_key])
                        else:
                            val_row.append(data[ele][field_key])
                else:
                    val_row.append("--NA--")
                num = num + 1
            rows.append(val_row)
            self.logger.debug(f'Each Row => {val_row}')
            val_row = []
            colored_fields.append(field_key)
        fields = colored_fields
        final_rows = []
        for array in range(len(rows[0])) :
            tmp = []
            for element in rows:
                tmp.append(element[array])
            final_rows.append(tmp)
        rows = final_rows
        # Adding Serial Numbers to the dataset
        fields.insert(0, '#')
        num = 1
        for outer in rows:
            outer.insert(0, num)
            num = num + 1
        # Adding Serial Numbers to the dataset
        return fields, rows


    def base64_encode(self, content=None):
        """
        This method will encode a base 64 string.
        """
        try:
            if content is not None:
                content = base64.b64encode(content).decode("utf-8")
        except binascii.Error:
            self.logger.debug(f'Base64 Encode Error => {content}')
        return content


    def base64_decode(self, content=None):
        """
        This method will decode the base 64 string.
        """
        try:
            if content is not None:
                content = content.replace("\r", "\\r")
                content = base64.b64decode(content, validate=True).decode("utf-8")
        except binascii.Error:
            self.logger.debug(f'Base64 Decode Error => {content}')
        except UnicodeDecodeError:
            self.logger.debug(f'Base64 Unicode Decode Error => {content}')
        return content


    def update_dict(self, data=None):
        """
        Deep Update the Dict
        """
        for key, value in data.items():
            if isinstance(value, str):
                value = None if value == 'None' else value
                if value is not  None:
                    data[key] = self.base64_decode(value)
                    return self.update_dict(data)
            else:
                return self.update_dict(data)
        return data


    def callback(self, value=None):
        """
        This method is a call back method for the nested lookup.
        """
        if isinstance(value, str):
            if value.lower() == 'none':
                value = None
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.lower() == 'null':
                value = None
        response = value
        if value not in  [None, True, False] and isinstance(value, str):
            response = self.base64_decode(value)
        return response


    def nested_dict(self, dictionary=None, limit=False):
        """
        This method will check the nested dictionary.
        """
        for key, value in dictionary.items():
            if isinstance(value, str):
                if key in EDITOR_KEYS:
                    doc = nested_alter({key : value}, key, self.callback)
                    dictionary[key] = self.less_content(doc[key], limit)
                else:
                    dictionary[key] = value
            elif isinstance(value, dict):
                return self.nested_dict(dictionary, limit)
            elif isinstance(value, list):
                return self.nested_list(dictionary, key, value, limit)
        return dictionary


    def nested_list(self, dictionary=None, key=None, value=None, limit=False):
        """
        This method will check the list for a dictionary.
        """
        response = []
        if value:
            for occurrence in value:
                if isinstance(occurrence, str):
                    if key in EDITOR_KEYS:
                        doc = nested_alter({key : occurrence}, key, self.callback)
                        response.append(self.less_content(doc[key], limit))
                    else:
                        response.append(occurrence)
                elif isinstance(occurrence, dict):
                    response.append(self.nested_dict(occurrence, limit))
        dictionary[key] = response
        return dictionary


    def less_content(self, content=None, limit=False):
        """
        This method will reduce the length of the content.
        """
        if limit:
            if content not in  [None, True, False] and isinstance(content, str):
                if len(content) > 60:
                    if "\n" in content:
                        total_lines = content.count('\n')
                        if total_lines-3 > 0:
                            last_line = f"\n{total_lines-3} More lines..."
                            content = content.split('\n', 3)
                            content = '\n'.join(content[:3])
                            content = f"{content}{last_line}"
                    else:
                        content = content[:60]+' ...'
        return content


    def prepare_json(self, json_data=None, limit=False):
        """
        This method will decode the base 64 string.
        """
        self.logger.debug(f'Data Limit => {limit}')
        if isinstance(json_data, list):
            new_json_data=[]
            for list_data in json_data:
                new_json_data.append(self.prepare_json(list_data, limit))
            return new_json_data
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if isinstance(value, str):
                    if key in EDITOR_KEYS:
                        doc = nested_alter({key : value}, key, self.callback)
                        json_data[key] = self.less_content(doc[key], limit)
                    else:
                        json_data[key] = value
                elif isinstance(value, dict):
                    json_data[key] = self.nested_dict(value, limit)
                elif isinstance(value, list):
                    final_list = []
                    if value:
                        for occurrence in value:
                            if isinstance(occurrence, str):
                                doc = nested_alter({key : occurrence}, key, self.callback)
                                final_list.append(self.less_content(doc[key], limit))
                            elif isinstance(occurrence, dict):
                                final_list.append(self.nested_dict(occurrence, limit))
                    json_data[key] = final_list
        return json_data


    def get_secrets(self, table=None, data=None):
        """
        This method will filter data for Secrets
        """
        self.logger.debug(f'Table => {table} and Data => {data}')
        rows, colored_fields = [], []
        fields = filter_columns(table)
        self.logger.debug(f'Fields => {fields}')
        for key in data:
            new_row = []
            for value in data[key]:
                self.logger.debug(f'Key => {key} and Value => {value}')
                new_row.append(key)
                new_row.append(value['name'])
                new_row.append(value['path'])
                content = self.base64_decode(value['content'])
                if content is not None:
                    new_row.append(content[:60]+'...')
                else:
                    new_row.append(content)
                rows.append(new_row)
                new_row = []
        for newfield in fields:
            colored_fields.append(newfield)
        fields = colored_fields
        # Adding Serial Numbers to the dataset
        fields.insert(0, '#')
        num = 1
        for outer in rows:
            outer.insert(0, num)
            num = num + 1
        # Adding Serial Numbers to the dataset
        return fields, rows


    def filter_secret_col(self, table=None, data=None):
        """
        This method will generate the data as for
        row format
        """
        self.logger.debug(f'Table => {table} and Data => {data}')
        rows, colored_fields = [], []
        fields = sortby(table)
        self.logger.debug(f'Fields => {fields}')
        for key in data:
            new_row = []
            for value in data[key]:
                self.logger.debug(f'Key => {key} and Value => {value}')
                new_row.append(key)
                new_row.append(value['name'])
                new_row.append(value['path'])
                content = self.base64_decode(value['content'])
                if content is not None:
                    new_row.append(content[:60]+'...')
                else:
                    new_row.append(content)
                # new_row.append(content)
                rows.append(new_row)
                new_row = []
        for newfield in fields:
            colored_fields.append(newfield)
        fields = colored_fields
        # Adding Serial Numbers to the dataset
        fields.insert(0, '#')
        num = 1
        for outer in rows:
            outer.insert(0, num)
            num = num + 1
        # Adding Serial Numbers to the dataset
        new_fields, new_row = [], []
        for row in rows:
            new_fields = new_fields + fields
            new_row = new_row + row
            new_fields.append("")
            new_row.append("")
        return new_fields, new_row


    def filter_data_col(self, table=None, data=None):
        """
        This method will generate the data as for row format
        """
        # self.table = "network"
        self.logger.debug(f'Table => {table} and Data => {data}')
        defined_keys = sortby(table)
        self.logger.debug(f'Fields => {defined_keys}')
        merge_exception = None
        if table == 'node':
            merge_exception = ["prescript", "partscript", "postscript"]
        data, override = self.merge_source(table, data, merge_exception)
        datacopy=data.copy()
        for key in datacopy.keys():
            if key == '_override':
                if data[key]:
                    data['info'] = "Config differs from parent - local overrides"
                del data[key]
        for new_key in list(data.keys()):
            if new_key not in defined_keys:
                defined_keys.append(new_key)
        index_map = {v: i for i, v in enumerate(defined_keys)}
        data = sorted(data.items(), key=lambda pair: index_map[pair[0]])
        self.logger.debug(f'Sorted Data => {data}')
        fields, rows = [], []
        for key in data:
            key_name = key[0]
            if key_name in override:
                key_name += ' *'
            fields.append(key_name)
            if isinstance(key[1], list):
                new_list = []
                for internal in key[1]:
                    for internal_val in internal:
                        self.logger.debug(f'Key: {internal_val} Value: {internal[internal_val]}')
                        if internal_val == "interface":
                            new_list.append(f'{internal_val} = {internal[internal_val]}')
                        else:
                            new_list.append(f'  {internal_val} = {internal[internal_val]}')
                new_list = '\n'.join(new_list)
                rows.append(new_list)
                new_list = []
            elif isinstance(key[1], dict):
                new_list = []
                num = 1
                for internal in key[1]:
                    self.logger.debug(f'Key => {internal} and Value => {key[1][internal]}')
                    in_key = internal
                    in_val = key[1][internal]
                    new_list.append(f'{in_key} = {in_val} ')
                    num = num + 1
                new_list = '\n'.join(new_list)
                rows.append(new_list)
                new_list = []
            else:
                rows.append(key[1])
            if table == "network":
                if key[0] in ["zone", "dhcp_range_end", "dhcp_range_end_ipv6", "prescript", "partscript", "postscript"]:
                    fields.append('')
                    rows.append('')
        fields = ['source' if item.startswith('_') else item for item in fields]
        return fields, rows


    def merge_source(self, table=None, data=None, exception=None):
        """
        This method will merge *_source field to the real field with braces and remove the
        *_source keys from the output.
        """
        response = deepcopy(data)
        override = overrides(table)
        resp_overrides = []
        for key, value in data.items():
            script = True if 'part' in key or 'post' in key or 'pre' in key else False
            if '_source' in key:
                raw_name = key.replace('_source', '')
                if raw_name[0] == '_':
                    raw_name = raw_name[1:]
                if table == value:
                    if raw_name in override:
                        resp_overrides.append(raw_name)
                if exception and raw_name in exception:
                    default_value = data[key]
                    response[key] = f'({default_value})'
                    default_value = data[raw_name].rstrip()
                    if len(default_value) == 0:
                        response[raw_name] = '<empty>'
                    else:
                        response[raw_name] = default_value
                    continue
                if isinstance(data[raw_name], str):
                    default_value = data[raw_name].rstrip()
                    if len(default_value) == 0:
                        default_value = '<empty>'
                else:
                    default_value = data[raw_name]
                if value in data:
                    if script is True and default_value != '<empty>':
                        response[raw_name] = f'({data[value]}) {default_value}'
                    else:
                        response[raw_name] = f'{default_value} ({data[value]})'
                else:
                    if str(value) == str(table):
                        response[raw_name] = f'{default_value}'
                    else:
                        if script is True and default_value != '<empty>':
                            response[raw_name] = f'({value}) {default_value}'
                        else:
                            response[raw_name] = f'{default_value} ({value})'
                del response[key]
        return response, resp_overrides


    def filter_osimage_col(self, table=None, data=None):
        """
        This method will generate the data as for row format
        """
        self.logger.debug(f'Table => {table} and Data => {data}')
        defined_keys = sortby(table)
        self.logger.debug(f'Fields => {defined_keys}')
        for new_key in list(data.keys()):
            if new_key not in defined_keys:
                defined_keys.append(new_key)
        index_map = {v: i for i, v in enumerate(defined_keys)}
        data = sorted(data.items(), key=lambda pair: index_map[pair[0]])
        self.logger.debug(f'Sorted Data => {data}')
        osimage = ["OS Image\n"]
        fields, rows = ["Tags\n"], ["Details\n"]
        for key in data:
            fields.append(key[0])
            osimage.append(key[1]['osimage'])
            if isinstance(key[1], list):
                new_list = []
                for internal in key[1]:
                    for internal_val in internal:
                        self.logger.debug(f'Key: {internal_val} Value: {internal[internal_val]}')
                        if internal_val == "interface":
                            new_list.append(f'{internal_val} = {internal[internal_val]}')
                        else:
                            new_list.append(f'  {internal_val} = {internal[internal_val]}')
                new_list = '\n'.join(new_list)
                rows.append(new_list)
                new_list = []
            elif isinstance(key[1], dict):
                new_list = []
                num = 1
                for internal in key[1]:
                    self.logger.debug(f'Key => {internal} and Value => {key[1][internal]}')
                    if internal != "name":
                        in_key = internal
                        in_val = key[1][internal]
                        if len(key[1]) == num:
                            new_list.append(f'{in_key} = {in_val} \n')
                        else:
                            new_list.append(f'{in_key} = {in_val} ')
                    num = num + 1
                new_list = '\n'.join(new_list)
                rows.append(new_list)
                new_list = []
            else:
                rows.append(key[1])
        return fields, osimage, rows


    def filter_nodelist_col(self, table=None, data=None):
        """
        This method will generate the data as for
        row format
        """
        self.logger.debug(f'Table => {table}')
        self.logger.debug(f'Data => {data}')
        fields, rows, colored_fields = [], [], []
        fields = filter_columns(table)
        self.logger.debug(f'Fields => {fields}')
        macaddress_row = []
        ipaddress_row = []
        datacopy=data.copy()
        for ele in datacopy.keys():
            if '_override' in datacopy[ele]:
                if datacopy[ele]['_override'] and 'name' in datacopy[ele]:
                    data[ele]['name'] = f"{data[ele]['name']} *"
                del data[ele]['_override']
                if '_override' in fields:
                    fields.remove('_override')
        for field_key in fields:
#            if field_key in ['prescript', 'partscript', 'postscript']:
#               continue
            val_row = []
            num = 1
            for ele in data:
                if field_key in list((data[ele].keys())):
                    if isinstance(data[ele][field_key], list):
                        new_list = []
                        if field_key == 'interfaces':
                            internal_macaddress = []
                            internal_ipaddress = []
                            for internal in data[ele][field_key]:
                                internal_interface, interface_details = None, ''
                                if 'interface' in internal:
                                    internal_interface = internal['interface']
                                if 'macaddress' in internal:
                                    internal_macaddress.append(f"{internal_interface} = {internal['macaddress']}")
                                if internal_interface:
                                    for internal_val in ['ipaddress','ipaddress_ipv6']:
                                        if internal_val in internal and internal[internal_val]:
                                            in_key = internal_val
                                            in_val = internal[internal_val]
                                            interface_details += in_val + ' '
                                    if 'dhcp' in internal and internal['dhcp']:
                                        interface_details += 'dhcp '
                                    internal_ipaddress.append(f'{internal_interface} = {interface_details} ')
                            internal_macaddress = '\n'.join(internal_macaddress)
                            internal_ipaddress = '\n'.join(internal_ipaddress)
                            macaddress_row.append(internal_macaddress)
                            ipaddress_row.append(internal_ipaddress)
                        else:
                            for internal in data[ele][field_key]:
                                for internal_val in internal:
                                    self.logger.debug(f'Key => {internal_val}')
                                    self.logger.debug(f'Value => {internal[internal_val]}')
                                    in_key = internal_val
                                    in_val = internal[internal_val]
                                    new_list.append(f'{in_key} = {in_val} ')
                        new_list = '\n'.join(new_list)
                        val_row.append(new_list)
                        new_list = []
                    else:
                        val_row.append(data[ele][field_key])
                else:
                    val_row.append("--NA--")
                num = num + 1
            rows.append(val_row)
            self.logger.debug(f'Each Row => {val_row}')
            val_row = []
            colored_fields.append(field_key)
        rows.append(macaddress_row)
        rows.append(ipaddress_row)
        colored_fields.append('MAC addresses')
        colored_fields.append('IP addresses')
        # removing the column for interfaces. it's empty at this stage anyways
        index_for_interfaces = colored_fields.index('interfaces')
        del colored_fields[index_for_interfaces]
        del rows[index_for_interfaces]
        fields = colored_fields
        final_rows = []
        for array in range(len(rows[0])) :
            tmp = []
            for element in rows:
                tmp.append(element[array])
            final_rows.append(tmp)
        rows = final_rows
        # Adding Serial Numbers to the dataset
        fields.insert(0, '#')
        num = 1
        for outer in rows:
            outer.insert(0, num)
            num = num + 1
        # Adding Serial Numbers to the dataset
        return fields, rows
