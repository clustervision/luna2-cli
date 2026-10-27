#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Optional field groups in governed list and show output.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2026, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.2"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import os
import sys
from configparser import RawConfigParser, Error
from functools import lru_cache

from luna.utils.constant import FILTER_FIELDS, GOVERNED_TABLES, INI_FILE, USER_INI_FILE


class Display():
    """
    Read display preferences and filter rendered fields without changing API data.
    """

    @staticmethod
    def warning(message):
        """
        A display preference warning must not prevent the requested command.
        """
        try:
            sys.stderr.write(f'WARNING :: {message}\n')
        except Exception:
            pass

    @staticmethod
    @lru_cache(maxsize=1)
    def preferences():
        """
        Read once per CLI process: personal values override controller values.
        Missing values default to enabled, independently of credential selection.
        """
        preferences = dict.fromkeys(FILTER_FIELDS, True)
        pending = set(preferences)
        for filename in (os.path.expanduser(USER_INI_FILE), INI_FILE):
            if not pending:
                break
            parser = RawConfigParser()
            try:
                # Missing or unreadable files are optional for display preferences.
                if not parser.read(filename, encoding='utf-8'):
                    continue
            except (Error, UnicodeError, OSError):
                Display.warning(f'Cannot read display preferences from {filename}; using defaults or the next file.')
                continue
            for option in sorted(pending):
                if not parser.has_option('DISPLAY', option):
                    continue
                try:
                    preferences[option] = parser.getboolean('DISPLAY', option)
                except ValueError:
                    Display.warning(f'Invalid [DISPLAY] {option} in {filename}; using yes.')
                pending.remove(option)
        return preferences

    @staticmethod
    def filter_fields(table, fields, rows, column=False):
        """
        Keep fields and their values together in list rows or a vertical show.
        Only governed views opt in; access reports and raw JSON do not use this.
        """
        if table not in GOVERNED_TABLES:
            return fields, rows
        preferences = Display.preferences()
        hidden = {field for option, group in FILTER_FIELDS.items()
                  if not preferences[option] for field in group}
        if not hidden:
            return fields, rows
        # An overridden show field has a trailing marker added by Helper.
        kept = [index for index, field in enumerate(fields)
                if field.removesuffix(' *') not in hidden]
        if len(kept) == len(fields):
            return fields, rows
        filtered = [fields[index] for index in kept]
        if column:
            return filtered, [rows[index] for index in kept]
        return filtered, [[row[index] for index in kept] for row in rows]
