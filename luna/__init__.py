#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Init method for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"


import os
import sys
from shutil import copy2

INI_FILE = '/trinity/local/luna/cli/config/luna.ini'
LOG_FOLDER = '/var/log/luna'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def create_dir(path=None):
    """This method will create required directories"""
    if os.path.exists(path) is False:
        try:
            os.makedirs(path, mode=0o777, exist_ok=False)
            sys.stdout.write(f'PASS :: {path} is created.\n')
        except PermissionError:
            sys.stderr.write('ERROR :: Install this tool as a super user.\n')
            sys.exit(1)

if False in [os.path.exists(LOG_FOLDER), os.path.exists(INI_FILE)]:
    create_dir(path=LOG_FOLDER)
    create_dir(path="/trinity/local/luna/config")
    copy2(f'{CURRENT_DIR}/luna.ini', INI_FILE)
