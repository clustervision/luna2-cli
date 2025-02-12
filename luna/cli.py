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
Main Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.1"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import sys
import urllib3
try:
    import os
    from pathlib import Path
    from textwrap import dedent
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    from luna.utils.constant import TOOL_DESCRIPTION, TOOL_EPILOG, LOG_DIR, VERSION_FILE
    # from luna.utils.presenter import Presenter
    from luna.utils.log import Log
    from luna.network import Network
    from luna.group import Group
    from luna.osimage import OSImage
    from luna.cluster import Cluster
    from luna.cloud import Cloud
    from luna.bmcsetup import BMCSetup
    from luna.node import Node
    from luna.switch import Switch
    from luna.otherdev import OtherDev
    from luna.secrets import Secrets
    from luna.service import Service
    from luna.control import Control
    from luna.monitor import Monitor
    from luna.utils.message import Message
    from luna.utils.rest import Rest
    from luna.utils.message import Message
    classes = [
        Cluster,
        Cloud,
        Network,
        OSImage,
        BMCSetup,
        Switch,
        OtherDev,
        Group,
        Node,
        Secrets,
        Service,
        Control,
        Monitor
    ]

except KeyboardInterrupt:
    sys.stderr.write("\nKeyboard Interrupted.\n")
    sys.exit(1)


class Cli():
    """
    Cli class use arguments to navigate further.
    """

    def __init__(self):
        self.logger = None
        self.parser = None
        self.subparsers = None
        self.args = None
        Message()
        # Presenter().show_banner()

    def get_parser(self):
        """
        using shtab from parent directory: shtab --shell=bash luna.cli.get_parser
        """
        ver = self.get_version()
        self.parser = ArgumentParser(
            prog = 'luna',
            formatter_class = RawDescriptionHelpFormatter,
            description = dedent(TOOL_DESCRIPTION),
            epilog = TOOL_EPILOG
        )
        self.parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {ver}')
        self.parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        self.subparsers = self.parser.add_subparsers(dest="command", help='See Details by --help')
        for cls in classes:
            cls(parser=self.parser, subparsers =self.subparsers)
        print(f"{self.parser}")
        return self.parser

    def main(self):
        """
        Main method to fetch and provide the arguments for each class.
        """
        self.log_checker()
        ver = self.get_version()
        self.parser = ArgumentParser(
            prog = 'luna',
            formatter_class = RawDescriptionHelpFormatter,
            description = dedent(TOOL_DESCRIPTION),
            epilog = TOOL_EPILOG
        )
        self.parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {ver}')
        self.parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        self.subparsers = self.parser.add_subparsers(dest="command", help='See Details by --help')
        for cls in classes:
            cls(parser=self.parser, subparsers =self.subparsers)
        self.args = vars(self.parser.parse_args())
        self.call_class()
        return True


    def call_class(self):
        """
        Method to call the class for further operations.
        """
        if self.args["verbose"]:
            self.logger = Log.init_log('debug')
        else:
            self.logger = Log.init_log('info')
        command = sys.argv
        command[0] = 'luna'
        command = ' '.join(command)
        self.logger.info(f'Command Supplied => {command}')
        try:
            if self.args["command"]:
                if self.args["command"] == "osimage":
                    call = globals()["OSImage"]
                elif self.args["command"] == "bmcsetup":
                    call = globals()["BMCSetup"]
                elif self.args["command"] == "otherdev":
                    call = globals()["OtherDev"]
                else:
                    call = globals()[self.args["command"].capitalize()]
                urllib3.disable_warnings()
                Rest().daemon_validation()
                call(self.args, self.parser, self.subparsers)
            else:
                self.parser.print_help(sys.stdout)
                sys.exit(0)
        except KeyboardInterrupt:
            sys.stderr.write("\nKeyboard Interrupted\n")
            sys.exit(1)


    def get_version(self):
        """
        This Method will fetch the current version of Luna CLI from VERSION File.
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if 'luna' not in sys.argv[0]:
            current_dir = str(Path(current_dir).parent)
        version_file = f'{current_dir}/{VERSION_FILE}'
        with open(version_file, 'r', encoding='utf-8') as ver:
            version = ver.read()
        return version


    def log_checker(self):
        """
        This method will check if the log file is in place or not.
        If not then will create it.
        """
        if os.path.exists(LOG_DIR) is False:
            try:
                os.makedirs(LOG_DIR)
                Message().show_success(f'PASS :: {LOG_DIR} is created.')
            except PermissionError:
                Message().error_exit('ERROR :: Install this tool as a super user.')


def run_tool():
    """
    This method initiate the main method of CLI class.
    """
    try:
        Cli().main()
    except KeyboardInterrupt:
        sys.stderr.write("\nKeyboard Interrupted.\n")
        sys.exit(1)

def get_parser():
    return Cli().get_parser()
 
