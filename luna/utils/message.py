#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.
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
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.2"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import json
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


    @staticmethod
    def answer_message(answer=None, code=None):
        """
        Read a daemon answer without letting error reporting raise another error.
        A 500 with an unusable body still says Server Error; only a JSON detail
        is added beneath it, never a proxy's HTML page or an arbitrary body.
        """
        fallback = 'Server Error'
        try:
            # A string already supplied by a command is its message, not a raw body.
            strict = code == 500 and not isinstance(answer, str)
            content = getattr(answer, 'content', answer)
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='replace')
            body = content
            if isinstance(content, str):
                try:
                    body = json.loads(content)
                except ValueError:
                    return fallback if strict else content
            if isinstance(body, dict):
                message = body.get('message', fallback if code == 500 else content)
                if not isinstance(message, str):
                    if code == 500:
                        message = fallback
                    else:
                        return str(message)
                detail = body.get('detail')
                if isinstance(detail, str):
                    detail = ' '.join(''.join(char if char.isprintable() else ' '
                                              for char in detail).split())
                    if detail:
                        return f'{message}\n    {detail}'
                return message
            if strict or content is None:
                return fallback
            return str(content)
        except Exception:
            # A broken response or exception string must not hide the original 500.
            return fallback


    def error_exit(self, message=None, code=None):
        """
        This method will print the standard error and exit from program.
        """
        message = self.answer_message(message, code)
        if code == 500:
            message = f'HTTP ERROR :: 500 {message}'
        suffix = '' if '\n' in message else '.'
        line = f'{message}{suffix}\n'
        try:
            try:
                sys.stderr.write(line)
            except UnicodeEncodeError:
                # Older terminals may not support the characters in an exception.
                sys.stderr.write(line.encode('ascii', errors='backslashreplace').decode('ascii'))
        except Exception:
            # An unavailable stderr still means failure, not a secondary traceback.
            pass
        try:
            self.logger.debug(f'Message => {message}')
            if code:
                self.logger.debug(f'HTTP ERROR :: {code}')
        except Exception:
            # Logging the failure must not prevent the nonzero exit either.
            pass
        sys.exit(1)


    def show_failed_exit(self, message=None):
        """
        This method will print the standard error.
        """
        message = self.answer_message(message)
        sys.stderr.write(f'{message}\n')
        self.logger.debug(f'Message => {message}')
        sys.exit(1)


    def show_error(self, message=None, code=None):
        """
        This method will print the standard error.
        """
        message = self.answer_message(message, code)
        if code == 500:
            message = f'HTTP ERROR :: 500 {message}'
        sys.stderr.write(f'{message}\n')
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
