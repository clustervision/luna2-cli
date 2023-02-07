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

from luna.utils.rest import Rest
import numpy as np
import pandas as pd
from termcolor import colored

class Helper(object):
    """
    All kind of helper methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """


    def get_list(self, table=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        response = False
        data_list = Rest().get_data(table, None, None)
        if data_list:
            response = data_list
        return response


    def get_record(self, table=None, name=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        response = False
        data_list = Rest().get_data(table, name, None)
        if data_list:
            response = data_list
        return response


    def add_record(self, table=None, data=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        return True


    def delete_record(self, table=None, data=None):
        """
        This method will delete a records from
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        return True


    def update_record(self, table=None, data=None, where=None):
        """
        This method will update a records in
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        return True


    def rename_record(self, table=None, name=None):
        """
        This method will rename a records in
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        return True


    def clone_record(self, table=None, source=None, destination=None, data=None):
        """
        This method will clone a records in
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        return True


    def show_error(self, message=None):
        """
        This method will add a new records into
        the Luna 2 Daemon Database
        """
        print(colored(message, 'red', attrs=['bold']))
        return True


    def filter_data(self, table=None, data=None):
        """
        This method will generate the data as for
        row format
        """
        fields, rows, coloredfields = [], [], []
        fields = self.filter_columns(table)
        for fieldkey in fields:
            valrow = []
            for ele in data:
                if fieldkey in list((data[ele].keys())):
                    if isinstance(data[ele][fieldkey], list):
                        newlist = []
                        for internal in data[ele][fieldkey]:
                            for internal_val in internal:
                                inkey = colored(internal_val, 'cyan')
                                inval = colored(internal[internal_val], 'magenta')
                                newlist.append(f'{inkey} = {inval} ')
                        newlist = '\n'.join(newlist)
                        valrow.append(colored(newlist, 'blue'))
                        newlist = []
                    else:
                        if data[ele][fieldkey] == True:
                            valrow.append(colored(data[ele][fieldkey], 'green'))
                        elif data[ele][fieldkey] == False:
                            valrow.append(colored(data[ele][fieldkey], 'red'))
                        else:
                            valrow.append(colored(data[ele][fieldkey], 'blue'))
                else:
                    valrow.append(colored("--NA--", 'red'))
            rows.append(valrow)
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
        fields, rows, coloredfields = [], [], []
        fields = self.filter_columns(table)
        for key in data:
            if type(data[key]) is dict:
                newrow = []
                for fieldkey in fields:
                    if fieldkey in data[key]:
                        if data[key][fieldkey] == True:
                            newrow.append(colored(data[key][fieldkey], 'green'))
                        elif data[key][fieldkey] == False:
                            newrow.append(colored(data[key][fieldkey], 'red'))
                        else:
                            newrow.append(colored(data[key][fieldkey], 'blue'))
                    elif fieldkey in data:
                        if data[fieldkey] == True:
                            newrow.append(colored(data[fieldkey], 'green'))
                        elif data[fieldkey] == False:
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



    def filter_data_col(self, table=None, data=None):
        """
        This method will generate the data as for
        row format
        """
        index_map = {v: i for i, v in enumerate(self.sortby(table))}
        data = sorted(data.items(), key=lambda pair: index_map[pair[0]])
        fields, rows = [], []
        for key in data:
            fields.append(colored(key[0], 'yellow', attrs=['bold']))
            if isinstance(key[1], list):
                newlist = []
                for internal in key[1]:
                    for internal_val in internal:
                        inkey = colored(internal_val, 'cyan')
                        inval = colored(internal[internal_val], 'magenta')
                        newlist.append(f'{inkey} = {inval} ')
                newlist = '\n'.join(newlist)
                rows.append(colored(newlist, 'blue'))
                newlist = []
            else:
                if key[1] == True:
                    rows.append(colored(key[1], 'green'))
                elif key[1] == False:
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
            'groupinterface': ['id', 'groupid', 'interfacename', 'networkid'],
            'groupsecrets': ['id', 'groupid', 'name', 'content', 'path'],
            'ipaddress': ['id', 'ipaddress', 'subnet', 'network'],
            'monitor': ['id', 'nodeid', 'status', 'state'],
            'network': ['name', 'network', 'ns_ip', 'ns_hostname', 'dhcp'],
            'node': ['name', 'hostname', 'setupbmc', 'status', 'tpmuuid'],
            'nodeinterface': ['id', 'nodeid', 'networkid', 'ipaddress', 'macaddress', 'interface'],
            'nodesecrets': ['id', 'nodeid', 'name', 'content', 'path'],
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
            'node': ['name', 'hostname', 'group', 'osimage', 'interfaces', 'localboot', 'macaddr', 'switch', 'switchport', 'setupbmc', 'status', 'service',
                       'prescript', 'partscript', 'postscript', 'netboot', 'localinstall', 'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback', 'tpmuuid'
                       , 'tpmpubkey', 'tpmsha256',  'unmanaged_bmc_users', 'comment'],
            'group': ['name', 'bmcsetup', 'bmcsetupname', 'domain', 'interfaces', 'osimage', 'prescript', 'partscript', 'postscript', 'netboot', 'localinstall',
                    'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback', 'unmanaged_bmc_users','comment'],
            'bmcsetup': ['name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users', 'comment'],
            'osimage': ['name', 'dracutmodules', 'grab_filesystems', 'grab_exclude', 'initrdfile', 'kernelversion', 'kernelfile', 'kernelmodules', 'kerneloptions',
                        'path', 'tarball', 'torrent', 'distribution', 'comment'],
            'network': ['name', 'network', 'ns_hostname', 'ns_ip', 'ntp_server', 'gateway','dhcp','dhcp_range_begin','dhcp_range_end','comment']
        }
        response = list(static[table])
        return response