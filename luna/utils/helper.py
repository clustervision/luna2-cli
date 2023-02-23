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

import numpy as np
from termcolor import colored
from luna.utils.rest import Rest
from luna.utils.log import Log

class Helper(object):
    """
    All kind of helper methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.logger = Log.get_logger()


    def get_list(self, table=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        response = False
        self.logger.debug(f'Helper List => {table}')
        data_list = Rest().get_data(table, None, None)
        self.logger.debug(f'Response => {data_list}')
        if data_list:
            response = data_list
        return response


    def get_record(self, table=None, name=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        response = False
        self.logger.debug(f'Table => {table} and Name => {name}')
        data_list = Rest().get_data(table, name, None)
        self.logger.debug(f'Response => {data_list}')
        if data_list:
            response = data_list
        return response


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
                newrow.append(colored(value['content'], 'blue'))
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
                newrow.append(colored(value['content'], 'blue'))
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
            'cluster': ['name', 'hostname','ipaddr', 'technical_contacts', 'provision_method', 'security'],
            'controller': ['id', 'clusterid', 'hostname', 'status', 'ipaddr', 'serverport'],
            'group': ['name', 'bmcsetup', 'domain', 'provisionfallback', 'interfaces'],
            'groupinterface': ['interfacename', 'network'],
            'groupsecrets': ['Group', 'name', 'path', 'content'],
            'ipaddress': ['id', 'ipaddress', 'subnet', 'network'],
            'monitor': ['id', 'nodeid', 'status', 'state'],
            'network': ['name', 'network', 'ns_ip', 'ns_hostname', 'dhcp'],
            'node': ['name', 'hostname', 'setupbmc', 'status', 'tpmuuid'],
            'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network'],
            'nodesecrets': ['Node', 'name', 'path', 'content'],
            'osimage': ['name', 'kernelfile', 'path', 'tarball', 'distribution'],
            'otherdev': ['name', 'network', 'ipaddress', 'macaddr', 'comment'],
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
            'cluster': ['name', 'ns_ip','ntp_server', 'provision_fallback', 'provision_method', 'security', 'technical_contacts', 'user', 'debug'],
            'controller': ['hostname', 'ipaddr','luna_config', 'srverport', 'status'],
            'node': ['name', 'hostname', 'group', 'osimage', 'interfaces', 'localboot', 'macaddr', 'switch', 'switchport', 'setupbmc', 'status', 'service',
                       'prescript', 'partscript', 'postscript', 'netboot', 'localinstall', 'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback', 'tpmuuid'
                       , 'tpmpubkey', 'tpmsha256',  'unmanaged_bmc_users', 'comment'],
            'group': ['name', 'bmcsetup', 'bmcsetupname', 'domain', 'interfaces', 'osimage', 'prescript', 'partscript', 'postscript', 'netboot', 'localinstall',
                    'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback', 'unmanaged_bmc_users','comment'],
            'bmcsetup': ['name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users', 'comment'],
            'osimage': ['name', 'dracutmodules', 'grab_filesystems', 'grab_exclude', 'initrdfile', 'kernelversion', 'kernelfile', 'kernelmodules', 'kerneloptions',
                        'path', 'tarball', 'torrent', 'distribution', 'comment'],
            'switch': ['name', 'network', 'oid', 'read', 'rw', 'ipaddress', 'comment'],
            'otherdev': ['name', 'network', 'ipaddress', 'macaddr', 'comment'],
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
                'ipaddr': True,
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
                'macaddr': True,
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
                'macaddr': True,
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
