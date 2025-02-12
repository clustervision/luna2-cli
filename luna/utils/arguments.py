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
Arguments Class for the CLI for common arguments.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.1"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

import argparse
from luna.utils.constant import BOOL_CHOICES, BOOL_META

class Arguments():
    """
    All kind of common Arguments methods.
    """

    def common_list_args(self, parser=None):
        """
        This method will provide the common list and show arguments.
        """
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        parser.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        return parser


    def common_bmcsetup_args(self, parser=None):
        """
        This method will provide the common bmcsetup arguments.
        """
        parser.add_argument('name', help='BMC Setup Name')
        parser.add_argument('-i', '--userid', type=int, help='UserID')
        parser.add_argument('-u', '--username', help='Username')
        parser.add_argument('-p', '--password', help='Password')
        parser.add_argument('-n', '--netchannel', type=int, help='Network Channel')
        parser.add_argument('-m', '--mgmtchannel', type=int, help='Management Channel')
        parser.add_argument('-U', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser
    

    def common_cloud_args(self, parser=None):
        """
        This method will provide the common Cloud arguments.
        """
        parser.add_argument('name', help='Cloud Provider Name')
        parser.add_argument('-t', '--type', help='Type of Cloud Provider')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def common_group_args(self, parser=None):
        """
        This method will provide the common group arguments.
        """
        parser.add_argument('name', help='Name of the Group')
        parser.add_argument('-e', '--setupbmc', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='BMC Setup')
        parser.add_argument('-o', '--osimage', help='OS Image Name')
        parser.add_argument('-t', '--osimagetag', help='OS Image Tag')
        parser.add_argument('-k', '--kerneloptions', action='store_true', help='Kernel Options')
        parser.add_argument('-qk', '--quick-kerneloptions', dest='kerneloptions',
                                metavar="File-Path OR In-Line", help='Kernel Options File-Path OR In-Line')
        parser.add_argument('-b', '--bmcsetupname', help='BMC Setup Name')
        parser.add_argument('-d', '--domain', help='Domain Name')
        parser.add_argument('-r', '--roles', help='Roles')
        parser.add_argument('-s', '--scripts', help='Scripts')
        parser.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        parser.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        parser.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        parser.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        parser.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        parser.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        parser.add_argument('-i', '--provision_interface', help='Provision Interface')
        parser.add_argument('-p', '--provision_method', help='Provision Method')
        parser.add_argument('-f', '--provision_fallback', help='Provision Fallback')
        parser.add_argument('-n', '--netboot', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Network Boot')
        parser.add_argument('-m', '--bootmenu', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Boot Menu')
        parser.add_argument('-U', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-if', '--interface', help='Interface Name')
        parser.add_argument('-N', '--network', help='Interface Network Name. * Interface is Required.')
        parser.add_argument('-L', '--vlanid', help='Interface VLAN ID. * Interface is Required.')
        parser.add_argument('-O', '--options', action='store_true', help='Interfaces Options. * Interface is Required.')
        parser.add_argument('-D', '--dhcp', choices=BOOL_CHOICES, metavar=BOOL_META, help='Interfaces dhcp toggle. * Interface is Required.')
        parser.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line. * Interface is Required.')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('--local', action='store_true', default=None, help='Allow local item changes')
        return parser


    def common_node_args(self, parser=None, required=None):
        """
        This method will provide the common node arguments.
        """
        parser.add_argument('name', help='Name of the Node')
        if required:
            parser.add_argument('-g', '--group', required=True, help='Group Name')
        else:
            parser.add_argument('-g', '--group', help='Group Name')
        parser.add_argument('-o', '--osimage', help='OS Image Name')
        parser.add_argument('-t', '--osimagetag', help='OS Image Tag')
        parser.add_argument('-k', '--kerneloptions', action='store_true', help='Kernel Options')
        parser.add_argument('-qk', '--quick-kerneloptions', dest='kerneloptions',
                                metavar="File-Path OR In-Line", help='Kernel Options File-Path OR In-Line')
        parser.add_argument('-e', '--setupbmc', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='BMC Setup')
        parser.add_argument('-b', '--bmcsetup', help='BMC Setup')
        parser.add_argument('--switch', help='Switch Name')
        parser.add_argument('--switchport', help='Switch Port')
        parser.add_argument('--cloud', help='Cloud Name')
        parser.add_argument('-r', '--roles', help='Roles')
        parser.add_argument('-s', '--scripts', help='Scripts')
        parser.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        parser.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        parser.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        parser.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        parser.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        parser.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        parser.add_argument('-i', '--provision_interface', help='Provision Interface')
        parser.add_argument('-p', '--provision_method', help='Provision Method')
        parser.add_argument('-f', '--provision_fallback', help='Provision Fallback')
        parser.add_argument('-n', '--netboot', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Network Boot')
        parser.add_argument('-m', '--bootmenu', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Boot Menu')
        parser.add_argument('-S', '--service', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Service')
        parser.add_argument('--status', help='Status')
        parser.add_argument('--tpm_uuid', help='TPM UUID')
        parser.add_argument('--tpm_pubkey', help='TPM Public Key')
        parser.add_argument('--tpm_sha256', help='TPM SHA256')
        parser.add_argument('-U', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-if', '--interface', help='Interface Name')
        parser.add_argument('-N', '--network', help='Interface Network Name. * Interface is Required.')
        parser.add_argument('-L', '--vlanid', help='Interface VLAN ID. * Interface is Required.')
        parser.add_argument('-I', '--ipaddress', help='Interfaces IP Address. * Interface is Required.')
        parser.add_argument('-M', '--macaddress', help='Interfaces MAC Address. * Interface is Required.')
        parser.add_argument('-O', '--options', action='store_true', help='Interfaces Options. * Interface is Required.')
        parser.add_argument('-D', '--dhcp', choices=BOOL_CHOICES, metavar=BOOL_META, help='Interfaces dhcp toggle. * Interface is Required.')
        parser.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line. * Interface is Required.')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        parser.add_argument('--local', action='store_true', default=None, help='Allow local item changes')
        return parser


    def common_network_args(self, parser=None, required=None):
        """
        This method will provide the common network arguments.
        """
        parser.add_argument('name', help='Network Name')
        if required:
            parser.add_argument('-N', '--network', required=True, help='Network ip-address/cidr')
        else:
            parser.add_argument('-N', '--network', help='Network ip-address/cidr')
            parser.add_argument('-cl', '--clear', metavar=['ipv4', 'ipv6'], help='Clear IPv4 or IPv6 configurations.')
        parser.add_argument('-g', '--gateway', help='Gateway')
        parser.add_argument('-m', '--gateway_metric', type=int, help='Gateway Metric')
        parser.add_argument('-t', '--type', help='Network Type like ethernet or infiniband')
        parser.add_argument('-S', '--nameserver_ip', help='NameServer IP')
        parser.add_argument('-T', '--ntp_server', help='NTP Server')
        parser.add_argument('-D', '--dhcp', choices=BOOL_CHOICES,
                                 metavar=BOOL_META, help='DHCP')
        parser.add_argument('-b', '--dhcp_range_begin', help='DHCP Range Start')
        parser.add_argument('-e', '--dhcp_range_end', help='DHCP Range End')
        parser.add_argument('-p', '--dhcp_nodes_in_pool', choices=BOOL_CHOICES,
                                 metavar=BOOL_META, help='Use IP addresses of the dhcp range for nodes. Uses DDNS to update zones')
        parser.add_argument('-s', '--shared', help='Network Shared')
        parser.add_argument('-z', '--zone', help='Internal or external Network Zone')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def common_osimage_args(self, parser=None):
        """
        This method will provide the common osimage arguments.
        """
        parser.add_argument('name', help='OSImage Name')
        parser.add_argument('-G', '--grab_filesystems', action='store_true', help='Grab Filesystems')
        parser.add_argument('-qG', '--quick-grab_filesystems', dest='grab_filesystems',
                                metavar="File-Path OR In-Line", help='Grab Filesystems File-Path OR In-Line')
        parser.add_argument('-E', '--grab_exclude', action='store_true', help='Grab Excludes')
        parser.add_argument('-qE', '--quick-grab_exclude', dest='grab_exclude',
                                metavar="File-Path OR In-Line", help='Grab Excludes File-Path OR In-Line')
        parser.add_argument('-r', '--initrdfile', help='INIT RD File')
        parser.add_argument('-f', '--kernelfile', help='Kernel File')
        parser.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        parser.add_argument('-o', '--kerneloptions', action='store_true', help='Kernel Options')
        parser.add_argument('-qo', '--quick-kerneloptions', dest='kerneloptions',
                                metavar="File-Path OR In-Line", help='Kernel Options File-Path OR In-Line')
        parser.add_argument('-k', '--kernelversion', help='Kernel Version')
        parser.add_argument('-p', '--path', help='Path of image')
        parser.add_argument('-i', '--imagefile', help='Imagefile UUID')
        parser.add_argument('-d', '--distribution', help='Distribution')
        parser.add_argument('-l', '--osrelease', help='OS release or version')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser
