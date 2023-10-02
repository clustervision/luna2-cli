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
Message Class for the CLI to show stdout, stderr
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import sys
from luna.utils.log import Log


class Message():
    """
    All kind of Message methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.logger = Log.get_logger()
        if self.logger is None:
            self.logger = Log.init_log('info')


    def error_exit(self, message=None, code=None):
        """
        This method will print the standard error and exit from program.
        """
        sys.stdout.write(f'{message}.\n')
        self.logger.debug(f'Message => {message}')
        if code:
            # sys.stderr.write(f'HTTP ERROR :: {code}\n')
            self.logger.debug(f'HTTP ERROR :: {code}')
        sys.exit(1)


    def show_error(self, message=None):
        """
        This method will print the standard error.
        """
        sys.stdout.write(f'{message}\n')
        self.logger.debug(f'Message => {message}')
        return True


    def show_success(self, message=None):
        """
        This method will print the standard output.
        """
        sys.stdout.write(f'{message}\n')
        self.logger.debug(f'Message => {message}')
        return True


    def show_warning(self, message=None):
        """
        This method will print the standard output.
        """
        sys.stdout.write(f'{message}\n')
        self.logger.debug(f'Message => {message}')
        return True
