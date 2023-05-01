#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Helper Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import os
from time import time, sleep
import base64
import binascii
import subprocess
from random import randint
from os import getpid
import numpy as np
import hostlist
from nested_lookup import nested_lookup, nested_update, nested_delete
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.presenter import Presenter
from luna.utils.constant import EDITOR_KEYS, BOOL_KEYS, filter_columns, sortby
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


    def prepare_payload(self, table=None, raw_data=None):
        """
        This method will prepare the payload.
        """
        raw_data = self.choice_to_bool(raw_data)
        payload = {k: v for k, v in raw_data.items() if v is not None}
        for key in EDITOR_KEYS:
            content = nested_lookup(key, payload)
            if content:
                if content[0] is True:
                    if table:
                        get_list = Rest().get_data(table, payload['name'])
                        if get_list:
                            value = nested_lookup(key, get_list)
                            if value:
                                content = self.open_editor(key, value[0], payload)
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
        This Method will open a default text editor to
        write the multiline text for keys such as comment,
        prescript, postscript, partscript, content etc. but
        not limited to them only.
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
        subprocess.call([editor, filename])
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
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][table]
            if args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                data = Helper().prepare_json(data, True)
                fields, rows  = self.filter_data(table, data)
                fields = list(map(lambda x: x.replace('tpm_uuid', 'tpm_present'), fields))
                fields = list(map(lambda x: x.replace('ns_ip', 'nameserver'), fields))
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f' << {table.capitalize()} >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = Message().show_error(f'{table} is not found.')
        return response


    def show_data(self, table=None, args=None):
        """
        Method to show a switch in Luna Configuration.
        """
        row_name = None
        if 'name' in args:
            row_name = args['name']
        get_list = Rest().get_data(table, row_name)
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
                data = Helper().prepare_json(data, True)
                fields, rows  = self.filter_data_col(table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{table.capitalize()} => {data["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Message().show_error(f'{args["name"]} is not found in {table}.')
        return response


    def member_record(self, table=None, args=None):
        """
        This method fetch the nodes to the provided entity.
        """
        response = False
        get_list = Rest().get_data(table, args['name']+'/_list')
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][table][args["name"]]['members']
            data = Helper().prepare_json(data)
            if args['raw']:
                response = Presenter().show_json(data)
            else:
                num = 1
                fields = ['S.No.', 'Nodes']
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


    def add_record(self, table=None, data=None):
        """
        This method will add a new record.
        """
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        payload = self.prepare_payload(None, data)
        request_data = {'config':{table:{payload['name']: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(table, payload['name'], request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 201:
            Message().show_success(f'New {table.capitalize()}, {payload["name"]} created.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def update_record(self, table=None, data=None):
        """
        This method will update a record.
        """
        for remove in ['verbose', 'command', 'action']:
            data.pop(remove, None)
        if 'raw' in data:
            data.pop('raw', None)
        payload = self.prepare_payload(table, data)
        name = None
        if 'name' in payload:
            name = payload['name']
            request_data = {'config':{table:{name: payload}}}
        else:
            request_data = {'config':{table: payload}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(table, name, request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            if name:
                Message().show_success(f'{table.capitalize()}, {name} updated.')
            else:
                Message().show_success(f'{table.capitalize()} updated.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True


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
            Message().show_success(f'{table.capitalize()}, {data["name"]} is deleted.')
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
            Message().show_success(f'{data["name"]} renamed to {newname}.')
        else:
            Message().error_exit(response.content, response.status_code)
        return True


    def clone_record(self, table=None, data=None, newname=None):
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
            Message().show_success(f'{payload["name"]} cloned as {newname}.')
        else:
            Message().error_exit(response.content, response.status_code)
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


    def common_list_args(self, parser=None):
        """
        This method will provide the common list and show arguments..
        """
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        return parser


    def control_print(self, num=None, control_data=None):
        """
        This method will perform power option on node.
        """
        header = "| S.No. |     Node Name      |       Status       |"
        hr_line = 'X-------------------------------------------------X'
        rows = []
        power_status = ['failed', 'off', 'on']
        if 'control' in control_data:
            if 'power' in control_data['control']:
                for state in power_status:
                    if control_data['control']['power'][state]['hostlist']:
                        host_list = control_data['control']['power'][state]['hostlist'].split(',')
                        for node in host_list:
                            rows.append([num, node, state.capitalize()])
                            num = num + 1

        if rows:
            for row in rows:
                if row[0] == 1:
                    Message().show_success(hr_line)
                    Message().show_success(header)
                    Message().show_success(hr_line)
                row[0] = f'{row[0]}'.ljust(6)
                row[1] = f'{row[1]}'.ljust(19)
                if row[2] in ['Failed', 'Off', 'off']:
                    row[2] = row[2].ljust(19)
                if row[2] in ['on', 'On']:
                    row[2] = row[2].ljust(19)
                line = f'| {row[0]}| {row[1]}| {row[2]}|'
                Message().show_success(line)
        return num


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
        while not_complete:
            print(animation[i % len(animation)], end='\r')
            sleep(.1)
            i += 1
        return True


    def dig_data(self, code=None, request_id=None, count=None):
        """
        Data Digger for Control API's.
        """
        sleep(2)
        uri = f'control/status/{request_id}'
        response = Rest().get_raw(uri)
        code = response.status_code
        http_response = response.json()
        if code == 200:
            count = Helper().control_print(count, http_response)
            return self.dig_data(code, request_id, count)
        elif code == 404:
            Message().show_success('X-------------------------------------------------X')
            return True
        else:
            Message().show_error(f"Something Went Wrong {code}")
            return False


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
                    val_row.append(ele[field_key])
                else:
                    val_row.append("--NA--")
                self.logger.debug(f'Element => {ele}')
            rows.append(val_row)
            val_row = []
            colored_fields.append(field_key)
        fields = colored_fields
        self.logger.debug(f'Rows before Swapping => {rows}')
        rows = np.array(rows).T.tolist()
        # Adding Serial Numbers to the dataset
        fields.insert(0, 'S. No.')
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
        for field_key in fields:
            val_row = []
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
                        val_row.append(data[ele][field_key])
                else:
                    val_row.append("--NA--")
            rows.append(val_row)
            self.logger.debug(f'Each Row => {val_row}')
            val_row = []
            colored_fields.append(field_key)
        fields = colored_fields
        rows = np.array(rows).T.tolist()
        # Adding Serial Numbers to the dataset
        fields.insert(0, 'S. No.')
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
                content = base64.b64decode(content)
                content = content.decode("utf-8")
        except binascii.Error:
            self.logger.debug(f'Base64 Decode Error => {content}')
        except UnicodeDecodeError:
            self.logger.debug(f'Base64 Unicode Decode Error => {content}')
        return content


    def prepare_json(self, json_data=None, limit=False):
        """
        This method will decode the base 64 string.
        """
        for key in EDITOR_KEYS:
            content = nested_lookup(key, json_data)
            if content:
                if content[0] is not None:
                    try:
                        content = self.base64_decode(content[0])
                        if limit:
                            if len(content) and '<empty>' not in content:
                                content = content[:60]
                                if '\n' in content:
                                    content = content.removesuffix('\n')
                                content = f'{content}...'
                        json_data = nested_update(json_data, key=key, value=content)
                    except TypeError:
                        self.logger.debug(f"Without any reason {content} is coming from api.")
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
                new_row.append(content[:60]+'...')
                rows.append(new_row)
                new_row = []
        for newfield in fields:
            colored_fields.append(newfield)
        fields = colored_fields
        # Adding Serial Numbers to the dataset
        fields.insert(0, 'S. No.')
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
                new_row.append(content)
                rows.append(new_row)
                new_row = []
        for newfield in fields:
            colored_fields.append(newfield)
        fields = colored_fields
        # Adding Serial Numbers to the dataset
        fields.insert(0, 'S. No.')
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
        This method will generate the data as for
        row format
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
        fields, rows = [], []
        for key in data:
            fields.append(key[0])
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
                for internal in key[1]:
                    self.logger.debug(f'Key => {internal} and Value => {key[1][internal]}')
                    in_key = internal
                    in_val = key[1][internal]
                    new_list.append(f'{in_key} = {in_val} ')
                new_list = '\n'.join(new_list)
                rows.append(new_list)
                new_list = []
            else:
                rows.append(key[1])
        return fields, rows
