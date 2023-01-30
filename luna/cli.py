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


# import sys
from argparse import ArgumentParser

from luna.network import Network


class Cli(object):
    """
    Cli class use arguments to navigate further.
    """

    def __init__(self):
        pass
    
    def main(self):
        parser = ArgumentParser(prog='luna', description='Manage Luna Cluster')
        parser.add_argument('--debug', '-d', action='store_true', help='Show debug information')
        subparsers = parser.add_subparsers(dest="command", help='See Details by --help')
        Networkparser = Network.getarguments(self, parser, subparsers)

        args = vars(parser.parse_args())
        self.callclass(args)
        return True


    def callclass(self, args):
        if args:
            # print(args)
            # sys.exit(0)
            if args["command"] == "network":
                Network(args)
        else:
            print("Please pass -h to see help menu.")


def run_tool():
    """
    This method initiate the main method of
    CLI class.
    """
    Cli().main()
