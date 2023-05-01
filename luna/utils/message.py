#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            sys.stderr.write(f'HTTP ERROR :: {code}\n')
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
