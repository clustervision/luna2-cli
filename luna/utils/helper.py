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


    def rowwise(self, data=None):
        """
        This method will generate the data as for
        row format
        """
        fields, rows = [], []
        for ele in data:
            keys = list(data[ele].keys())
            for key in keys:
                if key not in fields:
                    fields.append(key)
        for fieldkey in fields:
            valrow = []
            for ele in data:
                if fieldkey in list((data[ele].keys())):
                    valrow.append(data[ele][fieldkey])
                else:
                    valrow.append("--NA--")
            rows.append(valrow)
            valrow = []
        rows = np.array(rows).T.tolist()
        return fields, rows


    def filter_data(self, table=None, data=None):
        """"""
        fields, rows = [], []
        fields = self.filter_columns(table)
        # for x in filtered:
        #     newdata[x] = {}
        # rows = []
        for fieldkey in fields:
            valrow = []
            for ele in data:
                if fieldkey in list((data[ele].keys())):
                    valrow.append(data[ele][fieldkey])
                else:
                    valrow.append("--NA--")
            rows.append(valrow)
            valrow = []
        rows = np.array(rows).T.tolist()
        # print(rows)
        return fields, rows


    def filter_columns(self, table=None):
        """
        This method remove the unnessasry fields from
        the dataset.
        """
        response = False
        static = {
            'bmcsetup': ['id', 'name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel', 'comment', 'unmanaged_bmc_users'],
            'cluster': ['id', 'name', 'user', 'ns_ip', 'ntp_server', 'technical_contacts', 'provision_method', 'provision_fallback', 'security', 'debug'],
            'controller': ['id', 'clusterid', 'hostname', 'status', 'ipaddr', 'serverport'],
            'group': ['id', 'name', 'bmcsetupid', 'bmcsetup', 'osimageid', 'domain', 'prescript', 'partscript', 'postscript', 'netboot', 'localinstall', 'bootmenu', 'comment', 'provisioninterface', 'provisionfallback', 'provisionmethod', 'unmanaged_bmc_users'],
            'groupinterface': ['id', 'groupid', 'interfacename', 'networkid'],
            'groupsecrets': ['id', 'groupid', 'name', 'content', 'path'],
            'ipaddress': ['id', 'ipaddress', 'subnet', 'network'],
            'monitor': ['id', 'nodeid', 'status', 'state'],
            # 'network': ['id', 'name', 'network', 'subnet', 'gateway', 'ns_ip', 'ns_hostname', 'ntp_server', 'dhcp', 'dhcp_range_begin', 'dhcp_range_end', 'comment'],
            'network': ['name', 'network', 'ns_ip', 'ns_hostname', 'ntp_server', 'dhcp'],
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
        response = list(static[table])
        return response