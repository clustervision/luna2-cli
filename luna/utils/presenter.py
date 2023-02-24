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

import json
from prettytable import PrettyTable
from rich import print_json
import pyfiglet
from termcolor import colored
from luna.utils.log import Log

class Presenter(object):
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
        banner = pyfiglet.figlet_format('Luna 2 CLI', font = "digital")
        banner = colored(banner, 'green', attrs=['bold'])
        print(banner)
        return True


    def show_json(self, jsondata=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Jason Data => {jsondata}')
        pretty = json.dumps(jsondata, indent=4)
        print_json(pretty)
        return True



    def show_table(self, title=None, fields=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Fields => {fields}')
        self.logger.debug(f'Rows => {rows}')
        self.table.title = colored(title, 'cyan', attrs=['bold'])
        self.table.field_names = fields
        if '\\n' in str(rows):
            self.table.align = "l"
        self.table.add_rows(rows)
        print(self.table)
        return True


    def show_table_col(self, title=None, field=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.logger.debug(f'Fields => {field}')
        self.logger.debug(f'Rows => {rows}')
        self.table.title = colored(title, 'cyan', attrs=['bold'])
        self.table.add_column("Field", field)
        self.table.add_column("Values", rows)
        self.table.header = False
        self.table.align = "l"
        print(self.table)
        return True
