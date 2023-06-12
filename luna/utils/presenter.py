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
__status__      = "Development"

import json
from prettytable import PrettyTable
import pyfiglet
from luna.utils.log import Log
from luna.utils.constant import BANNER_NAME, BANNER_STYLE
from luna.utils.message import Message

class Presenter():
    """
    All kind of display methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.logger = Log.get_logger()
        self.table = PrettyTable()


    def show_banner(self):
        """
        This method will show the banner
        """
        banner = pyfiglet.figlet_format(BANNER_NAME, font=BANNER_STYLE)
        Message().show_success(banner)
        return True


    def show_json(self, json_data=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Jason Data => {json_data}')
        pretty = json.dumps(json_data, indent=2)
        Message().show_success(pretty)
        return True


    def show_table(self, title=None, fields=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Fields => {fields}')
        self.logger.debug(f'Rows => {rows}')
        self.table.title = title
        self.table.field_names = fields
        if '\\n' in str(rows):
            self.table.align = "l"
        self.table.add_rows(rows)
        Message().show_success(self.table)
        return True


    def show_table_col(self, title=None, field=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Fields => {field}')
        self.logger.debug(f'Rows => {rows}')
        self.table.title = title
        self.table.add_column("Field", field)
        self.table.add_column("Values", rows)
        self.table.header = False
        self.table.align = "l"
        Message().show_success(self.table)
        return True


    def table_only_rows(self, fields=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Rows => {rows}')
        self.table.field_names = fields
        self.table.add_rows(rows)
        Message().show_success(self.table)
        return True
