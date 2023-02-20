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
from luna.network import Network
from luna.group import Group
from luna.osimage import OSImage
from luna.cluster import Cluster
from luna.bmcsetup import BMCSetup
from luna.node import Node
from luna.switch import Switch
from luna.otherdevices import OtherDevices
from luna.secrets import Secrets
from luna.service import Service
from luna.control import Control


class Cli(object):
    """
    Cli class use arguments to navigate further.
    """

    def __init__(self):
        Presenter().show_banner()

    def main(self):
        """
        Main method to fetch and provide the arguments
        for each class.
        """
        parser = ArgumentParser(prog='luna', description='Manage Luna Cluster')
        parser.add_argument('--debug', '-d', action='store_true', help='Show debug information')
        subparsers = parser.add_subparsers(dest="command", help='See Details by --help')
        Cluster.getarguments(self, parser, subparsers)
        Network.getarguments(self, parser, subparsers)
        OSImage.getarguments(self, parser, subparsers)
        BMCSetup.getarguments(self, parser, subparsers)
        Switch.getarguments(self, parser, subparsers)
        OtherDevices.getarguments(self, parser, subparsers)
        Group.getarguments(self, parser, subparsers)
        Node.getarguments(self, parser, subparsers)
        Secrets.getarguments(self, parser, subparsers)
        Service.getarguments(self, parser, subparsers)
        Control.getarguments(self, parser, subparsers)

        args = vars(parser.parse_args())
        self.callclass(args)
        return True


    def callclass(self, args):
        """
        Method to call the class for further
        operations.
        """
        if args:
            if args["command"] == "cluster":
                Cluster(args)
            elif args["command"] == "network":
                Network(args)
            elif args["command"] == "osimage":
                OSImage(args)
            elif args["command"] == "bmcsetup":
                BMCSetup(args)
            elif args["command"] == "switch":
                Switch(args)
            elif args["command"] == "otherdevices":
                OtherDevices(args)
            elif args["command"] == "group":
                Group(args)
            elif args["command"] == "node":
                Node(args)
            elif args["command"] == "secrets":
                Secrets(args)
            elif args["command"] == "service":
                Service(args)
            elif args["command"] == "control":
                Control(args)
        else:
            print("Please pass -h to see help menu.")


def run_tool():
    """
    This method initiate the main method of
    CLI class.
    """
    Cli().main()
