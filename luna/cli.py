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
__status__      = "Production"

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


class Cli(object):
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
        self.parser.add_argument('-d', '--debug', action='store_true', help='Show debug information')
        self.subparsers = self.parser.add_subparsers(dest="command", help='See Details by --help')
        Cluster.getarguments(self, self.parser, self.subparsers)
        Network.getarguments(self, self.parser, self.subparsers)
        OSImage.getarguments(self, self.parser, self.subparsers)
        BMCSetup.getarguments(self, self.parser, self.subparsers)
        Switch.getarguments(self, self.parser, self.subparsers)
        OtherDev.getarguments(self, self.parser, self.subparsers)
        Group.getarguments(self, self.parser, self.subparsers)
        Node.getarguments(self, self.parser, self.subparsers)
        Secrets.getarguments(self, self.parser, self.subparsers)
        Service.getarguments(self, self.parser, self.subparsers)
        Control.getarguments(self, self.parser, self.subparsers)

        self.args = vars(self.parser.parse_args())
        self.callclass()
        return True


    def callclass(self):
        """
        Method to call the class for further
        operations.
        """
        if self.args["debug"]:
            self.logger = Log.init_log('debug')
        else:
            self.logger = Log.init_log('info')
        if self.args:
            if self.args["command"] == "cluster":
                Cluster(self.args)
            elif self.args["command"] == "network":
                Network(self.args)
            elif self.args["command"] == "osimage":
                OSImage(self.args)
            elif self.args["command"] == "bmcsetup":
                BMCSetup(self.args)
            elif self.args["command"] == "switch":
                Switch(self.args)
            elif self.args["command"] == "otherdev":
                OtherDev(self.args)
            elif self.args["command"] == "group":
                Group(self.args)
            elif self.args["command"] == "node":
                Node(self.args)
            elif self.args["command"] == "secrets":
                Secrets(self.args)
            elif self.args["command"] == "service":
                Service(self.args)
            elif self.args["command"] == "control":
                Control(self.args)
        else:
            print("Please pass -h to see help menu.")


def run_tool():
    """
    This method initiate the main method of
    CLI class.
    """
    Cli().main()
