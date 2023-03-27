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
__status__      = "Production"

from time import sleep
import numpy as np
import base64
import binascii
import hostlist
from termcolor import colored
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.presenter import Presenter
from nested_lookup import nested_lookup, nested_update

class Helper(object):
    """
    All kind of helper methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.logger = Log.get_logger()


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
                fields, rows  = self.filter_data(table, data)
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
        response = False
        fields, rows = [], []
        get_list = Rest().get_data(table, args['name'])
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if get_list:
            data = get_list['config'][table][args["name"]]
            if args['raw']:
                json_data = Helper().prepare_json(data)
                response = Presenter().show_json(json_data)
            else:
                fields, rows  = self.filter_data_col(table, data)
                self.logger.debug(f'Fields => {fields}')
                self.logger.debug(f'Rows => {rows}')
                title = f'{table.capitalize()} => {args["name"]}'
                response = Presenter().show_table_col(title, fields, rows)
        else:
            response = self.show_error(f'{args["name"]} is not found in {table}.')
        return response


    def name_validate(self, count=None, table=None,  name_list=None):
        """
        Recursive method to validate the name.
        """
        if count == 3:
            self.show_error("You have lost all 3 attempts, Please try again.")
        else:
            name = Inquiry().ask_text(f"{table} Name:")
            if name in name_list:
                self.show_error(f'{table} {name} is already present, Kindly use a new name.')
                count = count + 1
                return self.name_validate(count, table, name_list)
            else:
                return name


    def network_list(self):
        """
        This method will return the available network list.
        """
        network = []
        self.get_list = Rest().get_data("network")
        if self.get_list:
            network = list(self.get_list["config"]["network"].keys())
        return network


    def get_hostlist(self, rawhosts=None):
        """
        This method will perform power option on node.
        """
        response = []
        self.logger.debug(f'Received hostlist: {rawhosts}.')
        try:
            response = hostlist.expand_hostlist(rawhosts)
            self.logger.debug(f'Expanded hostlist: {response}.')
        except Exception:
            self.logger.debug(f'Hostlist is incorrect: {rawhosts}.')
        return response


    def common_list_args(self, parser=None):
        """
        This method will provide the common list and show arguments..
        """
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        return parser


    def common_add_args(self, parser=None, name=None):
        """
        This method will provide the common add, update, clone, and rename arguments..
        """
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('-i', '--init', action='store_true', help='Interactive Mode')
        parser.add_argument('-n', '--name', help=f'Name of the {name}')
        return parser


    def common_control_args(self, parser=None):
        """
        This method will provide the control arguments..
        """
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('node', help='Node Name or Node Hostlist')
        return parser


    def common_group_node_args(self, parser=None):
        """
        This method will provide the control arguments..
        """
        parser.add_argument('-pre', '--prescript', help='Pre Script')
        parser.add_argument('-part', '--partscript', help='Part Script')
        parser.add_argument('-post', '--postscript', help='Post Script')
        parser.add_argument('-pi', '--provision_interface', help='Provision Interface')
        parser.add_argument('-pm', '--provision_method', help='Provision Method')
        parser.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        parser.add_argument('-o', '--osimage', help='OS Image Name')
        parser.add_argument('-b', '--setupbmc', action='store_true', help='BMC Setup')
        parser.add_argument('-nb', '--netboot', help='Network Boot')
        parser.add_argument('-li', '--localinstall', help='Local Install')
        parser.add_argument('-bm', '--bootmenu', help='Boot Menu')
        parser.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-if', '--interface', action='append', help='Interface Name')
        parser.add_argument('-N', '--network', action='append', help='Interface Network Name')
        parser.add_argument('-c', '--comment', help='Comment')
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


    def common_switch_device_args(self, parser=None, name=None):
        """
        This method will provide the common add, update and clone aguments
        for switch and otherdevice.
        """
        parser.add_argument('-N', '--network', help=f'Network for {name}')
        parser.add_argument('-ip', '--ipaddress', help=f'IP Address for {name}')
        parser.add_argument('-m', '--macaddress', help=f'MAC Address for {name}')
        parser.add_argument('-c', '--comment', help=f'Comment for {name}')
        return parser


    def control_print(self, num=None, control_data=None):
        """
        This method will perform power option on node.
        """
        header = f"{colored('|', 'yellow')} {colored('S.No.', 'cyan')} {colored('|', 'yellow')}"
        header = f"{header}     {colored('Node Name', 'cyan')}      {colored('|', 'yellow')}       "
        header = f"{header}{colored('Status', 'cyan')}       {colored('|', 'yellow')}"
        hr_line = colored(
            'X-------------------------------------------------X',
            'yellow',
            attrs=['bold']
        )
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
                row[0] = colored(f'{row[0]}'.ljust(6), 'blue')
                row[1] = colored(f'{row[1]}'.ljust(19), 'blue')
                if row[2] in ['Failed', 'Off', 'off']:
                    row[2] = colored(row[2].ljust(19), 'red')
                if row[2] in ['on', 'On']:
                    row[2] = colored(row[2].ljust(19), 'green')
                line = f'| {row[0]}| {row[1]}| {row[2]}|'
                line = line.replace('|', colored('|', 'yellow'))
                print(line)
        return num


    def loader(self, message=None):
        """
        This method is a loader, will run while transactions happens.
        """
        animation = [
        colored(f"[=       ] {message}", 'yellow', attrs=['bold']),
        colored(f"[===     ] {message}", 'yellow', attrs=['bold']),
        colored(f"[====    ] {message}", 'yellow', attrs=['bold']),
        colored(f"[=====   ] {message}", 'yellow', attrs=['bold']),
        colored(f"[======  ] {message}", 'yellow', attrs=['bold']),
        colored(f"[======= ] {message}", 'yellow', attrs=['bold']),
        colored(f"[========] {message}", 'yellow', attrs=['bold']),
        colored(f"[ =======] {message}", 'yellow', attrs=['bold']),
        colored(f"[  ======] {message}", 'yellow', attrs=['bold']),
        colored(f"[   =====] {message}", 'yellow', attrs=['bold']),
        colored(f"[    ====] {message}", 'yellow', attrs=['bold']),
        colored(f"[     ===] {message}", 'yellow', attrs=['bold']),
        colored(f"[      ==] {message}", 'yellow', attrs=['bold']),
        colored(f"[       =] {message}", 'yellow', attrs=['bold']),
        colored(f"[        ] {message}", 'yellow', attrs=['bold']),
        colored(f"[        ] {message}", 'yellow', attrs=['bold'])
        ]
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
                hr_line = colored(
                    'X-------------------------------------------------X',
                    'yellow',
                    attrs=['bold']
                )
                print(hr_line)
                return True
        else:
            Helper().show_error(f"Something Went Wrong {code}")
            return False


    def add_record(self, table=None, data=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        print(table)
        print(data)
        return True


    def delete_record(self, table=None, data=None):
        """
        This method will delete a records from
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        print(table)
        print(data)
        return True


    def update_record(self, table=None, data=None, where=None):
        """
        This method will update a records in
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        print(table)
        print(data)
        print(where)
        return True


    def rename_record(self, table=None, name=None):
        """
        This method will rename a records in
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        print(table)
        print(name)
        return True


    def clone_record(self, table=None, source=None, destination=None, data=None):
        """
        This method will clone a records in
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        print(table)
        print(source)
        print(destination)
        print(data)
        return True


    def show_error(self, message=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Message => {message}')
        print(colored(message, 'red', attrs=['bold']))
        return True


    def show_success(self, message=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Message => {message}')
        print(colored(message, 'green', attrs=['bold']))
        return True


    def show_warning(self, message=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Message => {message}')
        print(colored(message, 'yellow', attrs=['bold']))
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
                    valrow.append(colored(ele[fieldkey], 'blue'))
                else:
                    valrow.append(colored("--NA--", 'red'))
                self.logger.debug(f'Element => {ele}')
            rows.append(valrow)
            valrow = []
            coloredfields.append(colored(fieldkey, 'yellow', attrs=['bold']))
        fields = coloredfields
        self.logger.debug(f'Rows before Swapping => {rows}')
        rows = np.array(rows).T.tolist()
        # Adding Serial Numbers to the dataset
        fields.insert(0, colored('S. No.', 'yellow', attrs=['bold']))
        num = 1
        for outer in rows:
            outer.insert(0, colored(num, 'blue'))
            num = num + 1
        # Adding Serial Numbers to the dataset
        return fields, rows


    def list_to_dict(self, lst):
        """
        This method will iterate the list of strings
        which have colon(:) for split purpose.
        """
        self.logger.debug(f'List to Convert => {lst}')
        response = []
        dictionary = {}
        for keyval in lst:
            if '|' in keyval:
                keyvalspl = keyval.split('|')
                self.logger.debug(f'Length After Split with | => {len(keyvalspl)}')
                if len(keyvalspl) == 4:
                    if keyvalspl[0] != '' and keyvalspl[1] != '' and keyvalspl[2] != '' and keyvalspl[3] != '':
                        dictionary['interface'] = keyvalspl[0]
                        dictionary['network'] = keyvalspl[1]
                        dictionary['ipaddress'] = keyvalspl[2]
                        dictionary['macaddress'] = keyvalspl[3]
                elif len(keyvalspl) == 2:
                    if keyvalspl[0] != '' and keyvalspl[1] != '':
                        dictionary['interface'] = keyvalspl[0]
                        dictionary['network'] = keyvalspl[1]
            if dictionary:
                response.append(dictionary)
                dictionary = {}
        self.logger.debug(f'Dict after Convert => {response}')
        return response


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
                                self.logger.debug(f'Key => {internal_val} and Value => {internal[internal_val]}')
                                inkey = colored(internal_val, 'cyan')
                                inval = colored(internal[internal_val], 'magenta')
                                newlist.append(f'{inkey} = {inval} ')
                        newlist = '\n'.join(newlist)
                        valrow.append(colored(newlist, 'blue'))
                        newlist = []
                    else:
                        if data[ele][fieldkey] is True:
                            valrow.append(colored(data[ele][fieldkey], 'green'))
                        elif data[ele][fieldkey] is False:
                            valrow.append(colored(data[ele][fieldkey], 'red'))
                        else:
                            valrow.append(colored(data[ele][fieldkey], 'blue'))
                else:
                    valrow.append(colored("--NA--", 'red'))
            rows.append(valrow)
            self.logger.debug(f'Each Row => {valrow}')
            valrow = []
            coloredfields.append(colored(fieldkey, 'yellow', attrs=['bold']))
        fields = coloredfields
        rows = np.array(rows).T.tolist()
        # Adding Serial Numbers to the dataset
        fields.insert(0, colored('S. No.', 'yellow', attrs=['bold']))
        num = 1
        for outer in rows:
            outer.insert(0, colored(num, 'blue'))
            num = num + 1
        # Adding Serial Numbers to the dataset
        return fields, rows


    def get_cluster(self, table=None, data=None):
        """
        This method will filter data for cluster
        """
        self.logger.debug(f'Table => {table} and Data => {data}')
        fields, rows, coloredfields = [], [], []
        fields = self.filter_columns(table)
        self.logger.debug(f'Fields => {fields}')
        for key in data:
            if isinstance(data[key], dict):
                newrow = []
                for fieldkey in fields:
                    if fieldkey in data[key]:
                        self.logger.debug(f'Value => {data[key][fieldkey]}')
                        if data[key][fieldkey] is True:
                            newrow.append(colored(data[key][fieldkey], 'green'))
                        elif data[key][fieldkey] is False:
                            newrow.append(colored(data[key][fieldkey], 'red'))
                        else:
                            newrow.append(colored(data[key][fieldkey], 'blue'))
                    elif fieldkey in data:
                        self.logger.debug(f'Value => {data[fieldkey]}')
                        if data[fieldkey] is True:
                            newrow.append(colored(data[fieldkey], 'green'))
                        elif data[fieldkey] is False:
                            newrow.append(colored(data[fieldkey], 'red'))
                        else:
                            newrow.append(colored(data[fieldkey], 'blue'))
                rows.append(newrow)
                newrow = []
        for newfield in fields:
            coloredfields.append(colored(newfield, 'yellow', attrs=['bold']))
        fields = coloredfields
        # # Adding Serial Numbers to the dataset
        fields.insert(0, colored('S. No.', 'yellow', attrs=['bold']))
        num = 1
        for outer in rows:
            outer.insert(0, colored(num, 'blue'))
            num = num + 1
        # Adding Serial Numbers to the dataset
        return fields, rows


    def base64_decode(self, content=None):
        """
        This method will decode the base 64 string.
        """
        try:
            if content is not None:
                content = base64.b64decode(content).decode("utf-8")
        except binascii.Error:
            self.logger.debug(f'Base64 Decode Error => {content}')
        return content


    def prepare_json(self, jsondata=None):
        """
        This method will decode the base 64 string.
        """
        encoded_keys = ['content', 'comment', 'prescript', 'partscript', 'postscript']
        for enkey in encoded_keys:
            content = nested_lookup(enkey, jsondata)
            if content:
                content = self.base64_decode(content[0])
                if content is not None:
                    jsondata = nested_update(jsondata, key=enkey, value=content[:30]+'...')
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
                newrow.append(colored(key, 'blue'))
                newrow.append(colored(value['name'], 'blue'))
                newrow.append(colored(value['path'], 'blue'))
                content = self.base64_decode(value['content'])
                newrow.append(colored(content[:30]+'...', 'blue'))
                rows.append(newrow)
                newrow = []
        for newfield in fields:
            coloredfields.append(colored(newfield, 'yellow', attrs=['bold']))
        fields = coloredfields
        # Adding Serial Numbers to the dataset
        fields.insert(0, colored('S. No.', 'yellow', attrs=['bold']))
        num = 1
        for outer in rows:
            outer.insert(0, colored(num, 'blue'))
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
                newrow.append(colored(key, 'blue'))
                newrow.append(colored(value['name'], 'blue'))
                newrow.append(colored(value['path'], 'blue'))
                content = self.base64_decode(value['content'])
                newrow.append(colored(content[:30]+'...', 'blue'))
                rows.append(newrow)
                newrow = []
        for newfield in fields:
            coloredfields.append(colored(newfield, 'yellow', attrs=['bold']))
        fields = coloredfields
        # Adding Serial Numbers to the dataset
        fields.insert(0, colored('S. No.', 'yellow', attrs=['bold']))
        num = 1
        for outer in rows:
            outer.insert(0, colored(num, 'blue'))
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
            fields.append(colored(key[0], 'yellow', attrs=['bold']))
            if isinstance(key[1], list):
                newlist = []
                for internal in key[1]:
                    for internal_val in internal:
                        self.logger.debug(f'Key => {internal_val} and Value => {internal[internal_val]}')
                        inkey = colored(internal_val, 'cyan')
                        inval = colored(internal[internal_val], 'magenta')
                        newlist.append(f'{inkey} = {inval} ')
                newlist = '\n'.join(newlist)
                rows.append(colored(newlist, 'blue'))
                newlist = []
            elif isinstance(key[1], dict):
                newlist = []
                for internal in key[1]:
                    self.logger.debug(f'Key => {internal} and Value => {key[1][internal]}')
                    inkey = colored(internal, 'cyan')
                    inval = colored(key[1][internal], 'magenta')
                    newlist.append(f'{inkey} = {inval} ')
                newlist = '\n'.join(newlist)
                rows.append(colored(newlist, 'blue'))
                newlist = []
            else:
                if key[1] is True:
                    rows.append(colored(key[1], 'green'))
                elif key[1] is False:
                    rows.append(colored(key[1], 'red'))
                else:
                    rows.append(colored(key[1], 'blue'))
        return fields, rows


    # def filter_keys(self, dictionary=None):
    #     """
    #     This method will arrange all key value into a
    #     single dictionary with a recursive call.
    #     """
    #     response = {}
    #     if dictionary:
    #         def recursive_items(dictionary):
    #             for key, value in dictionary.items():
    #                 if type(value) is dict:
    #                     yield from recursive_items(value)
    #                 else:
    #                     yield (key, value)
    #         for key, value in recursive_items(dictionary):
    #             response[key] = value
    #     return response


    def filter_columns(self, table=None):
        """
        This method remove the unnessasry fields from
        the dataset.
        """
        response = False
        static = {
            'bmcsetup': ['name', 'userid', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users'],
            'cluster': ['name', 'hostname','ipaddress', 'technical_contacts', 'provision_method', 'security'],
            'controller': ['id', 'clusterid', 'hostname', 'status', 'ipaddress', 'serverport'],
            'group': ['name', 'bmcsetup', 'domain', 'provisionfallback', 'interfaces'],
            'groupinterface': ['interfacename', 'network'],
            'groupsecrets': ['Group', 'name', 'path', 'content'],
            'ipaddress': ['id', 'ipaddress', 'subnet', 'network'],
            'monitor': ['id', 'nodeid', 'status', 'state'],
            'network': ['name', 'network', 'ns_ip', 'ns_hostname', 'dhcp'],
            'node': ['name', 'group', 'osimage', 'setupbmc', 'status', 'tpmuuid'],
            'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network'],
            'nodesecrets': ['Node', 'name', 'path', 'content'],
            'osimage': ['name', 'kernelfile', 'path', 'tarball', 'distribution'],
            'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
            'roles': ['id', 'name', 'modules'],
            'switch': ['name', 'network', 'oid', 'read', 'ipaddress'],
            'tracker': ['id', 'infohash', 'peer', 'ipaddress', 'port', 'download', 'upload', 'left', 'updated', 'status'],
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
            'cluster': ['name', 'ns_ip','ntp_server', 'provision_fallback', 'provision_method', 'security', 'technical_contacts', 'user', 'verbose'],
            'controller': ['hostname', 'ipaddress','luna_config', 'srverport', 'status'],
            'node': ['name', 'hostname', 'group', 'osimage', 'interfaces', 'localboot', 'macaddress', 'switch', 'switchport', 'setupbmc', 'status', 'service',
                       'prescript', 'partscript', 'postscript', 'netboot', 'localinstall', 'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback', 'tpmuuid'
                       , 'tpmpubkey', 'tpmsha256',  'unmanaged_bmc_users', 'comment'],
            'group': ['name', 'bmcsetup', 'bmcsetupname', 'domain', 'interfaces', 'osimage', 'prescript', 'partscript', 'postscript', 'netboot', 'localinstall',
                    'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback', 'unmanaged_bmc_users','comment'],
            'bmcsetup': ['name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users', 'comment'],
            'osimage': ['name', 'dracutmodules', 'grab_filesystems', 'grab_exclude', 'initrdfile', 'kernelversion', 'kernelfile', 'kernelmodules', 'kerneloptions',
                        'path', 'tarball', 'torrent', 'distribution', 'comment'],
            'switch': ['name', 'network', 'oid', 'read', 'rw', 'ipaddress', 'comment'],
            'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
            'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network'],
            'groupinterface': ['interfacename', 'network'],
            'groupsecrets': ['Group', 'name', 'path', 'content'],
            'nodesecrets': ['Node', 'name', 'path', 'content'],
            'network': ['name', 'network', 'ns_hostname', 'ns_ip', 'ntp_server', 'gateway','dhcp','dhcp_range_begin','dhcp_range_end','comment']
        }
        response = list(static[table])
        return response


    def default_values(self, table=None, key=None):
        """
        This method will provide the all default
        values for each key of every table from luna
        database. It will be called from the getarguments
        method for the default values.
        """
        response = False
        database = {
            'cluster': {
                'name': True,
                'ns_ip': True,
                'ntp_server': True,
                'provision_fallback': 'http',
                'provision_method': 'torrent',
                'security': 1,
                'technical_contacts': ['root@localhost'],
                'user': True,
                'debug': False
            },
            'controller': {
                'hostname': True,
                'ipaddress': True,
                'luna_config': True,
                'srverport': True,
                'status': True
            },
            'node': {
                'name': True,
                'hostname': True,
                'group': True,
                'osimage': True,
                'interfaces': True,
                'localboot': True,
                'macaddress': True,
                'switch': True,
                'switchport': True,
                'setupbmc': True,
                'status': True,
                'service': True,
                'prescript': True,
                'partscript': True,
                'postscript': True,
                'netboot': True,
                'localinstall': True,
                'bootmenu': True,
                'provisionmethod': True,
                'provisioninterface': True,
                'provisionfallback': True,
                'tpmuuid': True,
                'tpmpubkey': True,
                'tpmsha256': True, 
                'unmanaged_bmc_users': True,
                'comment': True
            },
            'group': {
                'name': True,
                'bmcsetup': True,
                'bmcsetupname': True,
                'domain': True,
                'interfaces': True,
                'osimage': True,
                'prescript': True,
                'partscript': True,
                'postscript': True,
                'netboot': True,
                'localinstall': True,
                'bootmenu': True,
                'provisionmethod': True,
                'provisioninterface': True,
                'provisionfallback': True,
                'unmanaged_bmc_users': True,
                'comment': True
            },
            'bmcsetup': {
                'name': True,
                'userid': True,
                'username': True,
                'password': True,
                'netchannel': True,
                'mgmtchannel': True,
                'unmanaged_bmc_users': True,
                'comment': True
            },
            'osimage': {
                'name': True,
                'dracutmodules': True,
                'grab_filesystems': True,
                'grab_exclude': True,
                'initrdfile': True,
                'kernelversion': True,
                'kernelfile': True,
                'kernelmodules': True,
                'kerneloptions': True,
                'path': True,
                'tarball': True,
                'torrent': True,
                'distribution': True,
                'comment': True
            },
            'switch': {
                'name': True,
                'network': True,
                'oid': True,
                'read': True,
                'rw': True,
                'ipaddress': True,
                'comment': True
            },
            'otherdev': {
                'name': True,
                'network': True,
                'ipaddress': True,
                'macaddress': True,
                'comment': True
            },
            'nodeinterface': {
                'interface': True,
                'ipaddress': True,
                'macaddress': True,
                'network': True
            },
            'groupinterface': {
                'interfacename': True,
                'network': True,
                'ipaddress': True
            },
            'groupsecrets': {
                'Group': True,
                'name': True,
                'path': True,
                'content': True
            },
            'nodesecrets': {
                'Node': True,
                'name': True,
                'path': True,
                'content': True
            },
            'network': {
                'name': True,
                'network': True,
                'ns_hostname': True,
                'ns_ip': True,
                'ntp_server': True,
                'gateway': True,
                'dhcp': True,
                'dhcp_range_begin': True,
                'dhcp_range_end': True,
                'comment': True
            }
        }
        response = database[table][key]
        return response
