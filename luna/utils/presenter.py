#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2023  ClusterVision Solutions b.v.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>


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
        This method will fetch all records from the Luna 2 Daemon Database
        """
        self.logger.debug(f'Jason Data => {json_data}')
        pretty = json.dumps(json_data, indent=2)
        Message().show_success(pretty)
        return True


    def show_table(self, title=None, fields=None, rows=None):
        """
        This method will fetch a records from the Luna 2 Daemon Database
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
        This method will fetch a records from the Luna 2 Daemon Database
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


    def show_table_col_more_fields(self, title=None, field=None, newfield=None, rows=None):
        """
        This method will fetch a records from the Luna 2 Daemon Database
        """
        self.logger.debug(f'Fields => {field}')
        self.logger.debug(f'Rows => {rows}')
        self.table.title = title
        self.table.add_column("Field", field)
        self.table.add_column("Field", newfield)
        self.table.add_column("Values", rows)
        self.table.header = False
        self.table.align = "l"
        Message().show_success(self.table)
        return True


    def table_only_rows(self, fields=None, rows=None):
        """
        This method will fetch a records from the Luna 2 Daemon Database
        """
        self.logger.debug(f'Rows => {rows}')
        self.table.field_names = fields
        self.table.add_rows(rows)
        Message().show_success(self.table)
        return True
