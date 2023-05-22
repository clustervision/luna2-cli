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
from luna.utils.log import Log
from luna.utils.message import Message
from  luna.utils.TableIt import *
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


    def print_results_table(self, data, teams_list):
        str_l = max(len(t) for t in teams_list)
        print(" ".join(['{:>{length}s}'.format(t, length = str_l) for t in [" "] + teams_list]))
        for t, row in zip(teams_list, data):
            # print(" ".join(['{:>{length}s}'.format(str(x), length = str_l) for x in [t] + row]))
            print(" ".join(['{:>{length}s}'.format(str(x), length = str_l) for x in [t] + row]))


    def show_table(self, title=None, fields=None, rows=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        self.print_results_table(rows, fields)
        # # header = "| S.No. |     Node Name      |       Status       |"
        # header = "|S.No.|"
        # # header = "| S.No. |     Node Name      |       Status       |"
        # # hr_line = 'X-------------------------------------------------X'
        # hr_line = ''
        # newrows = ''
        # num = 0

        # for head in fields:
        #     if num != 0:
        #         header = f"{header}     {head}      |"
        #     num = num +1

        # for line in range(len(header)-2):
        #     hr_line = f'{hr_line}-'
        # hr_line = f'+{hr_line}+'

        # num, inner = 0, 1
        # for row in rows:
        #     for element in row:
        #         print(f'asdasd {num} dasdasd {len(rows)}')
        #         if inner == 1:
        #             newrows = f'{newrows}|  {element}  |'
        #             inner = inner +1
        #         elif inner == len(row):
        #             newrows = f'{newrows}     {element}      |\n'
        #             inner = 1
        #         else:
        #             newrows = f'{newrows}     {element}      |'
        #             inner = inner +1
                
        # #     num = num +1
        # # # print(newrows)
        # newrows = newrows[:-1]
        # print(hr_line)
        # print(header)
        # print(hr_line)
        # print(newrows)
        # print(hr_line)
        # print("\n\n\n")

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
