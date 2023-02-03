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
        data_list = Rest().get_data(table, None)
        if data_list:
            response = data_list
        return response


    def get_record(self, table=None, name=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        ## Call Rest API Class method
        return True


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


    def filter_data(self, table=None, data=None, filter=None):
        """
        This method will generate the data as for
        row format
        """
        fields, rows, coloredfields = [], [], []
        fields = self.filter_columns(table, filter)
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


    def filter_data_col(self, table=None, data=None):
        """
        This method will generate the data as for
        row format
        """
        fields, rows  = self.filter_data(table, data)
        rows.insert(0, fields)
        rows = np.array(rows).T.tolist()
        return rows


    def filter_columns(self, table=None, filter=None):
        """
        This method remove the unnessasry fields from
        the dataset.
        """
        response = False
        if filter:
            static = {
                'bmcsetup': ['id', 'name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel', 'comment', 'unmanaged_bmc_users'],
                'cluster': ['id', 'name', 'user', 'ns_ip', 'ntp_server', 'technical_contacts', 'provision_method', 'provision_fallback', 'security', 'debug'],
                'controller': ['id', 'clusterid', 'hostname', 'status', 'ipaddr', 'serverport'],
                'group': ['id', 'name', 'bmcsetupid', 'bmcsetup', 'osimageid', 'domain', 'prescript', 'partscript', 'postscript', 'netboot', 'localinstall', 'bootmenu', 'comment', 'provisioninterface', 'provisionfallback', 'provisionmethod', 'unmanaged_bmc_users'],
                'groupinterface': ['id', 'groupid', 'interfacename', 'networkid'],
                'groupsecrets': ['id', 'groupid', 'name', 'content', 'path'],
                'ipaddress': ['id', 'ipaddress', 'subnet', 'network'],
                'monitor': ['id', 'nodeid', 'status', 'state'],
                'network': ['name', 'network', 'subnet', 'gateway', 'ns_ip', 'ns_hostname', 'ntp_server', 'dhcp', 'dhcp_range_begin', 'dhcp_range_end', 'comment'],
                'node': ['id', 'name', 'hostname', 'groupid', 'localboot', 'macaddr', 'osimageid', 'switchport', 'service', 'bmcsetupid', 'setupbmc', 'status', 'switchid', 'comment', 'prescript', 'partscript', 'postscript', 'netboot', 'localinstall', 'bootmenu', 'provisioninterface', 'provisionfallback', 'provisionmethod', 'tpmuuid', 'tpmpubkey', 'tpmsha256', 'unmanaged_bmc_users'],
                'nodeinterface': ['id', 'nodeid', 'networkid', 'ipaddress', 'macaddress', 'interface'],
                'nodesecrets': ['id', 'nodeid', 'name', 'content', 'path'],
                'osimage': ['id', 'name', 'dracutmodules', 'grab_filesystems', 'grab_exclude', 'initrdfile', 'kernelfile', 'kernelmodules', 'kerneloptions', 'kernelversion', 'path', 'tarball', 'torrent', 'distribution', 'comment'],
                'otherdevices': ['id', 'name', 'network', 'ipaddress', 'macaddr', 'comment'],
                'roles': ['id', 'name', 'modules'],
                'switch': ['id', 'name', 'network', 'oid', 'read', 'rw', 'ipaddress', 'comment'],
                'tracker': ['id', 'infohash', 'peer', 'ipaddress', 'port', 'download', 'upload', 'left', 'updated', 'status'],
                'user': ['id', 'username', 'password', 'roleid', 'createdby', 'lastlogin', 'created']
            }
        else:
            static = {
                'bmcsetup': ['name', 'userid', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users'],
                'cluster': ['name', 'ntp_server', 'technical_contacts', 'provision_method', 'security'],
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
                'otherdevices': ['name', 'network', 'ipaddress', 'macaddr', 'comment'],
                'roles': ['id', 'name', 'modules'],
                'switch': ['name', 'network', 'oid', 'read', 'ipaddress'],
                'tracker': ['id', 'infohash', 'peer', 'ipaddress', 'port', 'download', 'upload', 'left', 'updated', 'status'],
                'user': ['id', 'username', 'password', 'roleid', 'createdby', 'lastlogin', 'created']
            }
        response = list(static[table])
        return response