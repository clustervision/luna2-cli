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
                    valrow.append("")
            rows.append(valrow)
            valrow = []
        rows = np.array(rows).T.tolist()
        return fields, rows


    def filter_columns(self, rows=None):
        """
        This method remove the unnessasry fields from
        the dataset.
        """
        static = ['comment', 'dhcp', 'dhcp_range_begin', 'dhcp_range_end', 'gateway', 'name', 'network', 'ns_hostname', 'ns_ip', 'ntps_server']
        pass
        return rows