#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Presenter Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"

from prettytable import PrettyTable

class Presenter(object):
    """
    All kind of display methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.table = PrettyTable()


    def show_json(self, jsondata=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        response = False
        return response


    def show_table(self, fields=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.table.field_names = fields
        self.table.add_rows(rows)
        print(self.table)
        return True


    def show_table_as_column(self, data=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        print(data)
        for key in data:
            self.table.add_column(key, data[key])
        print(self.table)
        return True
