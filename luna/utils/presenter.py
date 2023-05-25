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
from luna.utils.log import Log
from luna.utils.message import Message
from  luna.utils.consoletable import ConsoleTable
class Presenter():
    """
    All kind of display methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.logger = Log.get_logger()
        self.table = ConsoleTable()


    def show_banner(self):
        """
        This method will show the banner
        """
        banner = "\n+-+-+-+-+ +-+-+-+\n|L|u|n|a| |C|L|I|\n+-+-+-+-+ +-+-+-+\n"
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
        rows.insert(0, fields)
        self.table.print_table(title, rows, True)
        return True


    def show_table_col(self, title=None, data=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.table.print_table(title, data)
        return True
