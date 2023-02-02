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

from prettytable import PrettyTable, FRAME, HEADER, NONE
import json
from pygments import highlight, lexers, formatters

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
        formatted_json = json.dumps(jsondata, sort_keys=True, indent=4)
        colorful = highlight(
            formatted_json,
            lexers.JsonLexer(),
            formatters.Terminal256Formatter())
        print(colorful)
        return True


    def show_table(self, fields=None, rows=None, filter=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.table.field_names = fields
        self.table.add_rows(rows)
        if filter:
            print(self.table.get_string(fields=filter))
        else:
            print(self.table)
        return True
