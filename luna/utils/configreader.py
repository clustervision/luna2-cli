#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Config Parser to read INI File Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import sys

class ConfigReader():
    """This Class will read INI file"""

    def __init__(self):
        self.file_data = dict()

    def read_file(self, config_file):
        """ This method will read the file"""
        with open(config_file, 'r', encoding='utf-8') as file:
            file_contents = file.readlines()
        for line in file_contents:
            if line[0]=='#' or line[0]==';':
                continue
            elif line[0]=='[':
                index = line.index(']')
                section = line[1:index]
                self.file_data[section] = dict()
            else:
                value = None
                if '=' in line:
                    name, value = line.split('=')
                elif ':' in line:
                    name, value = line.split(':')
                if value:
                    self.file_data[section][name.strip()] = value.strip()


    def get(self, section=None, option=None):
        """This method will return the value of a specific key"""
        response = None
        if self.has_section(section):
            if self.has_option(section, option):
                response = self.file_data[section][option]
        return response


    def has_section(self, section=None):
        """This method will check the section in INI file data"""
        response = None
        if section in self.file_data:
            response = True
        return response


    def has_option(self, section=None, option=None):
        """This method will check the section in INI file data"""
        response = None
        if section in self.file_data:
            if option in self.file_data[section]:
                response = True
        return response
    