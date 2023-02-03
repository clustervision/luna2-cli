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
from rich import print_json
import pyfiglet
from termcolor import colored

class Presenter(object):
    """
    All kind of display methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.table = PrettyTable()


    def show_banner(self):
        """
        This method will show the banner
        """
        banner = pyfiglet.figlet_format('Luna 2 CLI', font = "digital")
        banner= colored(banner, 'green', attrs=['bold'])
        print(banner)
        return True


    def show_json(self, jsondata=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        pretty = json.dumps(jsondata, indent=4)
        print_json(pretty)
        return True



    def show_table(self, fields=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.table.field_names = fields
        if '\\n' in str(rows):
            self.table.align = "l"
        self.table.add_rows(rows)
        print(self.table)
        return True
