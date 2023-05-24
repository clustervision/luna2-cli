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

import re

class ConsoleTable():
    """
    This Class is responsible to generate a clean and beautiful console table.
    """


    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.rows = 0
        self.cols = 0
        self.row_length = None
        self.matrix_new = []
        self.table = []
        self.element_length = []
        self.title = None
        self.matrix = []
        self.header = False


    def largest_column_length_list(self):
        """
        This method will make a list of largest columns length.
        """
        column_length = []
        for col in range(self.cols):
            for row in range(self.rows):
                column_length.append(len(str(self.matrix[row][col])))
            column_length.sort()
            element_length = column_length[-1]
            self.element_length.append(element_length)
            column_length = []
        return True


    def create_matrix(self):
        """
        This method will Create a new data set.
        """
        for row in range(self.rows):
            self.matrix_new.append([])
            for col in range(self.cols):
                self.matrix_new[row].append(str(self.matrix[row][col]))
        return True


    def nested_rows(self, current_row, element, element_split, col):
        """
        This method will parse rows with new lines.
        """
        temp_element = ""
        if len(element_split) >= 2:
            num = 1
            for each in element_split:
                calculate_length = " " * (self.element_length[col] - len(each) + 1)
                if num == 1:
                    temp_element = "|" + current_row + each + calculate_length + " |"
                else:
                    blank_row = re.sub('[a-zA-Z0-9./`~!@#$%]', ' ', current_row)
                    if num == len(element_split):
                        temp_element = "|"+blank_row+" " + each + calculate_length + "|"
                    else:
                        temp_element = "|"+blank_row+" " + each + calculate_length + "|"
                num = num +1
                self.table.append(temp_element)
        else:
            element = element + " " *(self.element_length[col] - len(element) + 2) + "|"
            current_row += element
            self.table.append("|" + current_row)
        return True


    def create_table(self):
        """
        This method will create table rows and format accordingly.
        """
        for row in range(self.rows):
            current_row = ""
            for col in range(self.cols):
                element = " " + self.matrix_new[row][col]
                if '\n' in element:
                    element = element[:-1]
                    element_split = element.split('\n')
                    self.nested_rows(current_row, element, element_split, col)
                    current_row = ""
                elif '\\n' in element:
                    element = element[:-1]
                    element_split = element.split('\\n')
                    self.nested_rows(current_row, element, element_split, col)
                    self.element_length[col] = self.element_length[col] - len(element_split) - 1
                    current_row = ""
                elif self.element_length[col] != len(self.matrix_new[row][col]):
                    element = element + " " *(self.element_length[col] - len(element) + 2) + "|"
                    current_row += element
                else:
                    element = element + " " + "|"
                    current_row += element
            if current_row:
                self.table.append("|" + current_row)
            self.row_length = len(current_row)
        return True


    def trim_table(self):
        """
        This method will reduce the extra white space from the table.
        """
        table_trim = []
        check_list = []
        check = False
        for each in self.table:
            last_from_string = each[-5:-1]
            check = last_from_string.isspace()
            check_list.append(check)
        if all(check_list):
            for each in self.table:
                line = each[:-5]+"|"
                table_trim.append(line)
                row_length = len(line)
            self.table = table_trim
            self.row_length = row_length
            return self.trim_table()
        self.row_length = len(self.table[0])
        return True


    def wrap_table(self):
        """
        This method will wrap the table.
        """
        row_wrap = ""
        for _ in range(self.row_length - 2):
            row_wrap += "-"
        row_wrap = "+" + row_wrap
        row_wrap += "+"
        self.table.insert(0, row_wrap)
        self.table.append(row_wrap)
        return True


    def wrap_header(self):
        """
        This method will wrap the field header.
        """
        line = ""
        for col in range(self.cols):
            element = "+"
            element = element + "-" * (self.element_length[col] + 2)
            line += element
        line += "+"
        self.table.insert(2, line)
        return True


    def add_title(self, title):
        """
        This method will add title in center of row for the table.
        """
        title_row = " "
        index = len(self.table[0])
        title_len = len(title)
        index = index+1 - title_len
        reminder = index % 2
        place = (index // 2)-1
        if reminder:
            title_row = f'{title_row * place}{title}{title_row * place}'
        else:
            place_reduced = place-1
            title_row = f'{title_row * place}{title}{title_row * place_reduced}'
        title_row = f'|{title_row}|'
        blank_line = self.table[0]
        self.table.insert(0, title_row)
        self.table.insert(0, blank_line)
        return True


    def console_print(self):
        """
        This is final method to print the table into console.
        """
        for row in self.table:
            print(row)
        return True


    def print_table(self, title, matrix, header=False):
        """
        This method will be called from outside to create and print table into console.
        """
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.largest_column_length_list()
        self.create_matrix()
        self.create_table()
        self.trim_table()
        self.wrap_table()
        if header:
            self.wrap_header()
        if title:
            self.add_title(title)
        self.console_print()
        return True
