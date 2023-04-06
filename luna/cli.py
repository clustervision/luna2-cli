#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import sys
from argparse import ArgumentParser
from luna.utils.presenter import Presenter
from luna.utils.log import Log
from luna.network import Network
from luna.group import Group
from luna.osimage import OSImage
from luna.cluster import Cluster
from luna.bmcsetup import BMCSetup
from luna.node import Node
from luna.switch import Switch
from luna.otherdev import OtherDev
from luna.secrets import Secrets
from luna.service import Service
from luna.control import Control
classes = [
    Cluster,
    Network,
    OSImage,
    BMCSetup,
    Switch,
    OtherDev,
    Group,
    Node,
    Secrets,
    Service,
    Control
]

class Cli():
    """
    Cli class use arguments to navigate further.
    """

    def __init__(self):
        self.logger = None
        self.parser = None
        self.subparsers = None
        self.args = None
        Presenter().show_banner()


    def main(self):
        """
        Main method to fetch and provide the arguments
        for each class.
        """
        self.parser = ArgumentParser(prog='luna', description='Manage Luna Cluster')
        self.parser.add_argument('-V', '--version', action='version', version='%(prog)s 2.0')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        self.subparsers = self.parser.add_subparsers(dest="command", help='See Details by --help')
        for clss in classes:
            clss(parser=self.parser, subparsers =self.subparsers)
        self.args = vars(self.parser.parse_args())
        self.call_class()
        return True


    def call_class(self):
        """
        Method to call the class for further
        operations.
        """
        if self.args["verbose"]:
            self.logger = Log.init_log('debug')
        else:
            self.logger = Log.init_log('info')
        command = sys.argv
        command[0] = 'luna'
        command = ' '.join(command)
        self.logger.info(f'Command Supplied => {command}')
        if self.args["command"]:
            if self.args["command"] == "osimage":
                call = globals()["OSImage"]
            elif self.args["command"] == "bmcsetup":
                call = globals()["BMCSetup"]
            elif self.args["command"] == "otherdev":
                call = globals()["OtherDev"]
            else:
                call = globals()[self.args["command"].capitalize()]
            call(self.args, self.parser, self.subparsers)
        else:
            self.parser.print_help(sys.stderr)
            sys.exit(1)


def run_tool():
    """
    This method initiate the main method of
    CLI class.
    """
    Cli().main()
