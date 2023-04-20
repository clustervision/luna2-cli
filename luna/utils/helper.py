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
import sys
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


class Helper():
    """
    All kind of helper methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.logger = Log.get_logger()


    def boolean(self):
        """
        This method will provide boolean choices
        for argument parser.
        """
        choices = ['y', 'yes', 'n', 'no', '']
        return choices


    def choice_to_bool(self, raw_data=None):
        """
        This method will convert string choices to
        boolean
        """
        bool_keys = [
            'debug',
            'security',
            'createnode_ondemand',
            'dhcp',
            'setupbmc',
            'netboot',
            'localinstall',
            'bootmenu',
            'localboot',
            'service'
        ]
        for enkey in bool_keys:
            content = nested_lookup(enkey, raw_data)
            if content:
                if content[0] is not None:
                    if content[0] == '':
                        raw_data = nested_update(raw_data, key=enkey, value='')
                    elif content[0].lower() in ['y', 'yes', 'true']:
                        raw_data = nested_update(raw_data, key=enkey, value=True)
                    else:
                        raw_data = nested_update(raw_data, key=enkey, value=False)
        return raw_data

    def prepare_payload(self, table=None, raw_data=None):
        """
        This method will prepare the payload.
        """
        raw_data = self.choice_to_bool(raw_data)
        payload = {k: v for k, v in raw_data.items() if v is not None}
        editor_keys = ['options', 'content', 'comment', 'prescript', 'partscript', 'postscript']
        for enkey in editor_keys:
            content = nested_lookup(enkey, payload)
            if content:
                if content[0] is True:
                    if table:
                        get_list = Rest().get_data(table, payload['name'])
                        if get_list:
                            keydata = nested_lookup(enkey, get_list)
                            if keydata:
                                content = self.open_editor(enkey, keydata[0], payload)
                                payload = nested_update(payload, key=enkey, value=content)
                    else:
                        content = self.open_editor(enkey, None, payload)
                        payload = nested_update(payload, key=enkey, value=content)
                elif content[0] is False:
                    payload = nested_delete(payload, enkey)
                elif content[0]:
                    if os.path.exists(content[0]):
                        if os.path.isfile(content[0]):
                            with open(content[0], 'rb') as file_data:
                                content = self.base64_encode(file_data.read())
                                payload = nested_update(payload, key=enkey, value=content)
                        else:
                            sys.stderr.write(f"ERROR :: {content[0]} is a Invalid filepath.")
                            sys.exit(1)
                    else:
                        content = self.base64_encode(bytes(content[0], 'utf-8'))
                        payload = nested_update(payload, key=enkey, value=content)
        return payload


    def open_editor(self, key=None, keydata=None, payload=None):
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
        if keydata:
            keydata = self.base64_decode(keydata)
            temp_file.write(keydata)
            temp_file.close()
        subprocess.call([editor, filename])
        with open(filename, 'rb') as file_data:
            response = self.base64_encode(file_data.read())
        os.remove(filename)
        os.rmdir(tmp_folder)
        return response


    def get_list(self, table=None, args=None):
        """
        Method to list all switchs from Luna Configuration.
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
            response = self.show_error(f'{table} is not found.')
        return response


    def show_data(self, table=None, args=None):
        """
        Method to show a switch in Luna Configuration.
        """
        rowname = None
        if 'name' in args:
            rowname = args['name']
        get_list = Rest().get_data(table, rowname)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            if rowname:
                data = get_list['config'][table][rowname]
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
            response = self.show_error(f'{args["name"]} is not found in {table}.')
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
                    newrow = [num, member]
                    rows.append(newrow)
                    num = num + 1
                title = f'<< {table.capitalize()} {args["name"]} Member Nodes >>'
                response = Presenter().show_table(title, fields, rows)
        else:
            response = self.show_error(f'{table} {args["name"]} not have any node.')
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
            self.show_success(f'New {table.capitalize()}, {payload["name"]} created.')
        else:
            sys.stderr.write(f'HTTP Error Code {response.status_code}.')
            sys.stderr.write(f'HTTP Error {response.content}.')
            sys.exit(1)
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
                self.show_success(f'{table.capitalize()}, {name} updated.')
            else:
                self.show_success(f'{table.capitalize()} updated.')
        else:
            sys.stderr.write(f'HTTP Error Code {response.status_code}.')
            sys.stderr.write(f'HTTP Error {response.content}.')
            sys.exit(1)
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
            self.show_success(f'{table.capitalize()}, {data["name"]} is deleted.')
        else:
            sys.stderr.write(f'HTTP Error Code {response.status_code}.')
            sys.stderr.write(f'HTTP Error {response.content}.')
            sys.exit(1)
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
            self.show_success(f'{data["name"]} renamed to {newname}.')
        else:
            sys.stderr.write(f'HTTP Error Code {response.status_code}.')
            sys.stderr.write(f'HTTP Error {response.content}.')
            sys.exit(1)
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
            self.show_success(f'{payload["name"]} cloneed as {newname}.')
        else:
            sys.stderr.write(f'HTTP Error Code {response.status_code}.')
            sys.stderr.write(f'HTTP Error {response.content}.')
            sys.exit(1)
        return True


    def get_hostlist(self, rawhosts=None):
        """
        This method will perform power option on node.
        """
        response = []
        self.logger.debug(f'Received hostlist: {rawhosts}.')
        try:
            response = hostlist.expand_hostlist(rawhosts)
            self.logger.debug(f'Expanded hostlist: {response}.')
        except hostlist.BadHostlist:
            self.logger.debug(f'Hostlist is incorrect: {rawhosts}.')
        return response


    def common_list_args(self, parser=None):
        """
        This method will provide the common list and show arguments..
        """
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        return parser


    def common_control_args(self, parser=None):
        """
        This method will provide the control arguments..
        """
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('node', help='Node Name or Node Hostlist')
        return parser


    def common_service_args(self, parser=None, service=None):
        """
        This method will return all common actions and arguments
        parser for service module.
        """
        actions = ['start', 'stop', 'restart', 'reload', 'status']
        for act in actions:
            parser_args = parser.add_parser(act, help=f'{act.capitalize()} {service} Service')
            parser_args.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
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
                    print(hr_line)
                    print(header)
                    print(hr_line)
                row[0] = f'{row[0]}'.ljust(6)
                row[1] = f'{row[1]}'.ljust(19)
                if row[2] in ['Failed', 'Off', 'off']:
                    row[2] = row[2].ljust(19)
                if row[2] in ['on', 'On']:
                    row[2] = row[2].ljust(19)
                line = f'| {row[0]}| {row[1]}| {row[2]}|'
                # line = line.replace('|', colored('|', 'yellow'))
                print(line)
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
        notcomplete = True
        i = 0
        while notcomplete:
            print(animation[i % len(animation)], end='\r')
            sleep(.1)
            i += 1
        return True


    def dig_data(self, code=None, request_id=None, count=None, bad_count=None):
        """
        Data Digger for Control API's.
        """
        uri = f'control/status/{request_id}'
        response = Rest().get_raw(uri)
        code = response.status_code
        http_response = response.json()
        if code == 200:
            count = Helper().control_print(count, http_response)
            return self.dig_data(code, request_id, count, bad_count)
        elif code == 400:
            bad_count = bad_count + 1
            if bad_count < 10:
                count = Helper().control_print(count, http_response)
                return self.dig_data(code, request_id, count, bad_count)
            elif bad_count > 10:
                Helper().show_error("Too Many Bad Response, Try Again!")
            else:
                print('X-------------------------------------------------X')
                return True
        else:
            Helper().show_error(f"Something Went Wrong {code}")
            return False


    def show_error(self, message=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Message => {message}')
        print(message)
        return True


    def show_success(self, message=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Message => {message}')
        print(message)
        return True


    def show_warning(self, message=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Message => {message}')
        print(message)
        return True


    def filter_interface(self, table=None, data=None):
        """
        This method will generate the data as for
        row format from the interface
        """
        self.logger.debug(f'table => {table}')
        self.logger.debug(f'data => {data}')
        fields, rows, coloredfields = [], [], []
        fields = self.filter_columns(table)
        self.logger.debug(f'fields => {fields}')
        for fieldkey in fields:
            valrow = []
            for ele in data:
                if fieldkey in list(ele.keys()):
                    valrow.append(ele[fieldkey])
                else:
                    valrow.append("--NA--")
                self.logger.debug(f'Element => {ele}')
            rows.append(valrow)
            valrow = []
            coloredfields.append(fieldkey)
        fields = coloredfields
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
        fields, rows, coloredfields = [], [], []
        fields = self.filter_columns(table)
        self.logger.debug(f'Fields => {fields}')
        for fieldkey in fields:
            valrow = []
            for ele in data:
                if fieldkey in list((data[ele].keys())):
                    if isinstance(data[ele][fieldkey], list):
                        newlist = []
                        for internal in data[ele][fieldkey]:
                            for internal_val in internal:
                                self.logger.debug(f'Key => {internal_val}')
                                self.logger.debug(f'Value => {internal[internal_val]}')
                                inkey = internal_val
                                inval = internal[internal_val]
                                newlist.append(f'{inkey} = {inval} ')
                        newlist = '\n'.join(newlist)
                        valrow.append(newlist)
                        newlist = []
                    elif fieldkey == 'tpm_uuid':
                        if data[ele][fieldkey]:
                            valrow.append(True)
                        else:
                            valrow.append(False)
                    else:
                        valrow.append(data[ele][fieldkey])
                else:
                    valrow.append("--NA--")
            rows.append(valrow)
            self.logger.debug(f'Each Row => {valrow}')
            valrow = []
            coloredfields.append(fieldkey)
        fields = coloredfields
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


    def prepare_json(self, jsondata=None, limit=False):
        """
        This method will decode the base 64 string.
        """
        encoded_keys = ['options', 'content', 'comment', 'prescript', 'partscript', 'postscript']
        for enkey in encoded_keys:
            content = nested_lookup(enkey, jsondata)
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
                        jsondata = nested_update(jsondata, key=enkey, value=content)
                    except TypeError:
                        self.logger.debug(f"Without any reason {content} is coming from api.")
        return jsondata


    def get_secrets(self, table=None, data=None):
        """
        This method will filter data for Secrets
        """
        self.logger.debug(f'Table => {table} and Data => {data}')
        rows, coloredfields = [], []
        fields = self.filter_columns(table)
        self.logger.debug(f'Fields => {fields}')
        for key in data:
            newrow = []
            for value in data[key]:
                self.logger.debug(f'Key => {key} and Value => {value}')
                newrow.append(key)
                newrow.append(value['name'])
                newrow.append(value['path'])
                content = self.base64_decode(value['content'])
                newrow.append(content[:60]+'...')
                rows.append(newrow)
                newrow = []
        for newfield in fields:
            coloredfields.append(newfield)
        fields = coloredfields
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
        rows, coloredfields = [], []
        fields = self.sortby(table)
        self.logger.debug(f'Fields => {fields}')
        for key in data:
            newrow = []
            for value in data[key]:
                self.logger.debug(f'Key => {key} and Value => {value}')
                newrow.append(key)
                newrow.append(value['name'])
                newrow.append(value['path'])
                content = self.base64_decode(value['content'])
                newrow.append(content)
                rows.append(newrow)
                newrow = []
        for newfield in fields:
            coloredfields.append(newfield)
        fields = coloredfields
        # Adding Serial Numbers to the dataset
        fields.insert(0, 'S. No.')
        num = 1
        for outer in rows:
            outer.insert(0, num)
            num = num + 1
        # Adding Serial Numbers to the dataset
        newfiels, newrows = [], []
        for row in rows:
            newfiels = newfiels + fields
            newrows = newrows + row
            newfiels.append("")
            newrows.append("")
        return newfiels, newrows


    def filter_data_col(self, table=None, data=None):
        """
        This method will generate the data as for
        row format
        """
        self.logger.debug(f'Table => {table} and Data => {data}')
        definedkeys = self.sortby(table)
        self.logger.debug(f'Fields => {definedkeys}')
        for newkey in list(data.keys()):
            if newkey not in definedkeys:
                definedkeys.append(newkey)
        index_map = {v: i for i, v in enumerate(definedkeys)}
        data = sorted(data.items(), key=lambda pair: index_map[pair[0]])
        self.logger.debug(f'Sorted Data => {data}')
        fields, rows = [], []
        for key in data:
            fields.append(key[0])
            if isinstance(key[1], list):
                newlist = []
                for internal in key[1]:
                    for internal_val in internal:
                        self.logger.debug(f'Key: {internal_val} Value: {internal[internal_val]}')
                        if internal_val == "interface":
                            newlist.append(f'{internal_val} = {internal[internal_val]}')
                        else:
                            newlist.append(f'  {internal_val} = {internal[internal_val]}')
                newlist = '\n'.join(newlist)
                rows.append(newlist)
                newlist = []
            elif isinstance(key[1], dict):
                newlist = []
                for internal in key[1]:
                    self.logger.debug(f'Key => {internal} and Value => {key[1][internal]}')
                    inkey = internal
                    inval = key[1][internal]
                    newlist.append(f'{inkey} = {inval} ')
                newlist = '\n'.join(newlist)
                rows.append(newlist)
                newlist = []
            else:
                rows.append(key[1])
        return fields, rows


    def filter_columns(self, table=None):
        """
        This method remove the unnessasry fields from
        the dataset.
        """
        response = False
        static = {
            'bmcsetup': ['name', 'userid', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users'],
            'cluster': ['name', 'hostname','ipaddress', 'technical_contacts', 'provision_method',
                        'security'],
            'controller': ['id', 'clusterid', 'hostname', 'status', 'ipaddress', 'serverport'],
            'group': ['name', 'bmcsetupname', 'osimage', 'provision_fallback', 'interfaces'],
            'groupinterface': ['interface', 'network', 'options'],
            'groupsecrets': ['Group', 'name', 'path', 'content'],
            'ipaddress': ['id', 'ipaddress', 'subnet', 'network'],
            'monitor': ['id', 'nodeid', 'status', 'state'],
            'network': ['name', 'network', 'ns_ip', 'dhcp', 'dhcp_range_begin', 'dhcp_range_end'],
            'node': ['name', 'group', 'osimage', 'setupbmc', 'bmcsetup', 'status', 'tpm_uuid'],
            'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network', 'options'],
            'nodesecrets': ['Node', 'name', 'path', 'content'],
            'osimage': ['name', 'kernelfile', 'path', 'tarball', 'distribution'],
            'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
            'roles': ['id', 'name', 'modules'],
            'switch': ['name', 'network', 'oid', 'read', 'ipaddress'],
            'tracker': ['infohash', 'peer', 'ipaddress', 'port', 'status'],
            'user': ['id', 'username', 'password', 'roleid', 'createdby', 'lastlogin', 'created']
        }
        response = list(static[table])
        return response


    def sortby(self, table=None):
        """
        This method remove the unnessasry fields from
        the dataset.
        """
        response = False
        static = {
            'cluster': ['name', 'ns_ip','ntp_server', 'provision_fallback', 'provision_method',
                        'security', 'technical_contacts', 'user', 'debug'],
            'controller': ['hostname', 'ipaddress','luna_config', 'srverport', 'status'],
            'node': ['name', 'hostname', 'group', 'osimage', 'interfaces', 'localboot',
                     'macaddress', 'switch', 'switchport', 'setupbmc', 'status', 'service',
                     'prescript', 'partscript', 'postscript', 'netboot', 'localinstall',
                     'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback',
                     'tpmuuid', 'tpmpubkey', 'tpmsha256', 'unmanaged_bmc_users', 'comment'],
            'group': ['name', 'bmcsetup', 'bmcsetupname', 'domain', 'interfaces', 'osimage',
                      'prescript', 'partscript', 'postscript', 'netboot', 'localinstall',
                      'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback',
                      'unmanaged_bmc_users','comment'],
            'bmcsetup': ['name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel',
                         'unmanaged_bmc_users', 'comment'],
            'osimage': ['name', 'dracutmodules', 'grab_filesystems', 'grab_exclude', 'initrdfile',
                        'kernelversion', 'kernelfile', 'kernelmodules', 'kerneloptions', 'path',
                        'tarball', 'torrent', 'distribution', 'comment'],
            'switch': ['name', 'network', 'oid', 'read', 'rw', 'ipaddress', 'comment'],
            'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
            'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network'],
            'groupinterface': ['interfacename', 'network'],
            'groupsecrets': ['Group', 'name', 'path', 'content'],
            'nodesecrets': ['Node', 'name', 'path', 'content'],
            'network': ['name', 'network', 'ns_hostname', 'ns_ip', 'ntp_server', 'gateway', 'dhcp',
                        'dhcp_range_begin', 'dhcp_range_end', 'comment']
        }
        response = list(static[table])
        return response
