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
__version__     = "2.2"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"


from luna.utils.constant import BOOL_CHOICES, BOOL_META
from luna.utils.helper import Helper


class Arguments():
    """
    All kind of common Arguments methods.
    """

    def common_list_args(self, parser, csv=False):
        """
        This method will provide the common list and show arguments.
        """
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        parser.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        if csv:
            parser.add_argument('--csv', metavar='<column>', default=None,
                                help='Output a single column as comma-separated values')
        return parser


    def common_bmcsetup_args(self, parser):
        """
        This method will provide the common bmcsetup arguments.
        """
        parser.add_argument('-i', '--userid', type=int, help='ID to use for the BMC user configuration')
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
    

    def common_cloud_args(self, parser):
        """
        This method will provide the common Cloud arguments.
        """
        parser.add_argument('-t', '--type', help='Type of Cloud Provider')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def common_group_args(self, parser):
        """
        This method will provide the common group arguments.
        """
        parser.add_argument('-e', '--setupbmc', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Enables or disables the use of BMC')
        parser.add_argument('-o', '--osimage', help='Sets the used OSImage for the group').completer = Helper().name_completer("osimage")
        parser.add_argument('-t', '--osimagetag', help='Sets the name of the OSImage Tag to use for booting')
        parser.add_argument('-k', '--kerneloptions', action='store_true', help='Overrides OSImage kernel options')
        parser.add_argument('-qk', '--quick-kerneloptions', dest='kerneloptions',
                                metavar="File-Path OR In-Line", help='Kernel Options File-Path OR In-Line')
        parser.add_argument('-b', '--bmcsetupname', help='BMC Setup Name').completer = Helper().name_completer("bmcsetup")
        parser.add_argument('-d', '--domain', help='Domain Name')
        parser.add_argument('-r', '--roles', help='Sets the roles used for the group. Multiple roles can be supplied comma separated')
        parser.add_argument('-s', '--scripts', help='Sets the scripts used for the group. Multiple scripts can be supplied comma separated')
        parser.add_argument('-rt', '--routes', help='Static routes coupled to the group (comma separated names, "" to clear)')
        parser.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        parser.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        parser.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        parser.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        parser.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        parser.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        parser.add_argument('-i', '--provision_interface', help='Overrides the Cluster provisioning interface')
        parser.add_argument('-p', '--provision_method', help='Overrides Cluster (primary) provisioning method')
        parser.add_argument('-f', '--provision_fallback', help='Overrides Cluster fallback provisioning method')
        parser.add_argument('-n', '--netboot', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Enables or disables network based boots. Disabling allows for local node, e.g. disk boot')
        parser.add_argument('-x', '--ipxe_kernel', help='Sets iPXE kernel used for booting. Supported are "default" and "alternative"')
        parser.add_argument('-m', '--bootmenu', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Cosmetic setting that enables or disables the displaying of the iPXE boot menu')
        parser.add_argument('-U', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-if', '--interface', help='Interface operations, requires a name').completer = Helper().interface_name_completer("group")
        parser.add_argument('-N', '--network', help='Interface Network Name. * Interface is Required.').completer = Helper().name_completer("network")
        parser.add_argument('-L', '--vlanid', help='Interface VLAN ID. * Interface is Required.')
        parser.add_argument('--mtu', help='MTU size * Interface is Required.')
        parser.add_argument('-P', '--vlan_parent', help='Interface VLAN parent interface. * Interface is Required.')
        parser.add_argument('-B', '--bond_mode', help='Interface bonding mode. * Interface is Required.')
        parser.add_argument('-A', '--bond_slaves', help='Interface bonded interface slaves. * Interface is Required.')
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


    def common_node_args(self, parser, required=None):
        """
        This method will provide the common node arguments.
        """
        if required:
            parser.add_argument('-g', '--group', required=True, help='Group Name')
        else:
            parser.add_argument('-g', '--group', help='Group Name').completer = Helper().name_completer("group")
        parser.add_argument('-o', '--osimage', help='Overrides the group configured OSImage').completer = Helper().name_completer("osimage")
        parser.add_argument('-t', '--osimagetag', help='Overrides the group configured OSImage Tag to use for booting')
        parser.add_argument('-k', '--kerneloptions', action='store_true', help='Overrides OSImage and Group kernel options')
        parser.add_argument('-qk', '--quick-kerneloptions', dest='kerneloptions',
                                metavar="File-Path OR In-Line", help='Kernel Options File-Path OR In-Line')
        parser.add_argument('-e', '--setupbmc', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='BMC Setup')
        parser.add_argument('-b', '--bmcsetup', help='BMC Setup')
        parser.add_argument('--switch', help='Sets the switch for the node. Used for port based node detection').completer = Helper().name_completer("switch")
        parser.add_argument('--switchport', help='Sets the switch port for the node. Used for port based node detection')
        parser.add_argument('--cloud', help='Cloud Name').completer = Helper().name_completer("cloud")
        parser.add_argument('-r', '--roles', help='Overrides Group configured roles used. Multiple roles can be supplied comma separated')
        parser.add_argument('-s', '--scripts', help='Overrides Group configured scripts used. Multiple scripts can be supplied comma separated')
        parser.add_argument('-rt', '--routes', help='Static routes coupled to the node (comma separated names, "" to clear)')
        parser.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        parser.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        parser.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        parser.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        parser.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        parser.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        parser.add_argument('-i', '--provision_interface', help='Overrides the Cluster or Group provisioning interface')
        parser.add_argument('-p', '--provision_method', help='Overrides Cluster or Group (primary) provisioning method')
        parser.add_argument('-f', '--provision_fallback', help='Overrides Cluster or Group fallback provisioning method')
        parser.add_argument('-n', '--netboot', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Overrides Group configured network based boots. Disabling allows for local node, e.g. disk boot')
        parser.add_argument('-x', '--ipxe_kernel', help='Sets iPXE kernel used for booting. Supported are "default" and "alternative"')
        parser.add_argument('-m', '--bootmenu', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Overrides Group configured setting that enables or disables the displaying of the iPXE boot menu')
        parser.add_argument('-S', '--service', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Enabling or disabling the Service mode during. Enabled drops the booting node into a shell')
        parser.add_argument('--status', help='Status')
        parser.add_argument('--tpm_uuid', help='TPM UUID')
        parser.add_argument('--tpm_pubkey', help='TPM Public Key')
        parser.add_argument('--tpm_sha256', help='TPM SHA256')
        parser.add_argument('-U', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-if', '--interface', help='Interface operations, requires a name').completer = Helper().interface_name_completer("node")
        parser.add_argument('-N', '--network', help='Interface Network Name. * Interface is Required.').completer = Helper().name_completer("network")
        parser.add_argument('--mtu', help='MTU size * Interface is Required.')
        parser.add_argument('-L', '--vlanid', help='Interface VLAN ID. * Interface is Required.')
        parser.add_argument('-P', '--vlan_parent', help='Interface VLAN parent interface. * Interface is Required.')
        parser.add_argument('-B', '--bond_mode', help='Interface bonding mode. * Interface is Required.')
        parser.add_argument('-A', '--bond_slaves', help='Interface bonded interface slaves. * Interface is Required.')
        parser.add_argument('-I', '--ipaddress', help='Interfaces IP Address. * Interface is Required.')
        parser.add_argument('-M', '--macaddress', help='Interfaces MAC Address. * Interface is Required.')
        parser.add_argument('-O', '--options', action='store_true', help='Interfaces Options. * Interface is Required.')
        parser.add_argument('-D', '--dhcp', choices=BOOL_CHOICES, metavar=BOOL_META, help='Interfaces dhcp toggle. * Interface is Required.')
        parser.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line. * Interface is Required.')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        parser.add_argument('--local', action='store_true', default=None, help='Allow local item changes')
        return parser


    def common_network_args(self, parser, required=None):
        """
        This method will provide the common network arguments.
        """
        if required:
            parser.add_argument('-N', '--network', required=True, help='Network ip-address/cidr')
        else:
            parser.add_argument('-N', '--network', help='Network ip-address/cidr')
            parser.add_argument('-cl', '--clear', metavar=['ipv4', 'ipv6'], help='Clear IPv4 or IPv6 configurations.')
        parser.add_argument('-g', '--gateway', help='Gateway')
        parser.add_argument('-m', '--gateway_metric', type=int, help='Gateway Metric')
        parser.add_argument('-t', '--type', help='Network Type like ethernet or infiniband')
        parser.add_argument('-S', '--nameserver_ip', help='Comma-separated name server IP(s), IPv4 and/or IPv6; sorted by family')
        parser.add_argument('-T', '--ntp_server', help='NTP Server')
        parser.add_argument('-D', '--dhcp', choices=BOOL_CHOICES,
                                 metavar=BOOL_META, help='DHCP')
        parser.add_argument('-b', '--dhcp_range_begin', help='DHCP Range Start. The DHCP range is used for unidentified booting nodes')
        parser.add_argument('-e', '--dhcp_range_end', help='DHCP Range End. The DHCP range is used for unidentified booting nodes')
        parser.add_argument('-p', '--dhcp_nodes_in_pool', choices=BOOL_CHOICES,
                                 metavar=BOOL_META, help='Use IP addresses of the dhcp range for nodes. Uses DDNS to update zones')
        parser.add_argument('-o', '--dhcp_nodes_only', choices=BOOL_CHOICES,
                                 metavar=BOOL_META, help='Only serve IP addresses to known nodes. Static assignments')
        parser.add_argument('-s', '--shared', help='This network will be shared on top of another network. Typically used for mixed node/BMC networks')
        parser.add_argument('-dr', '--dhcp_relay', help='Comma-separated DHCP relay source IP(s) for this subnet, or "" to clear. '
                                 'When set, the subnet is selected by relay source instead of the udhcp pool class')
        parser.add_argument('-dls', '--dhcp_link_subnet', help='Comma-separated link prefix(es) in CIDR form, IPv4 and/or IPv6, for '
                                 'option-82.5 (RFC 3527) link-selection, or "" to clear. Requires --dhcp_relay; each prefix is sorted '
                                 'by family into the v4/v6 anchor. Kea backend')
        parser.add_argument('-rt', '--routes', help='Static routes coupled to the network (comma separated names, "" to clear)')
        parser.add_argument('-z', '--zone', help='Internal or external Network Zone')
        parser.add_argument('-n', '--non_authoritative', choices=BOOL_CHOICES,
                                 metavar=BOOL_META, help='Set this network as non-authoritative for its DNS zone definition')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def common_osimage_args(self, parser):
        """
        This method will provide the common osimage arguments.
        """
        parser.add_argument('-G', '--grab_filesystems', action='store_true', help='File systems or paths to be used during a grab operation')
        parser.add_argument('-qG', '--quick-grab_filesystems', dest='grab_filesystems',
                                metavar="File-Path OR In-Line", help='Grab Filesystems File-Path OR In-Line')
        parser.add_argument('-E', '--grab_exclude', action='store_true', help='Files excluded from a grab operation')
        parser.add_argument('-qE', '--quick-grab_exclude', dest='grab_exclude',
                                metavar="File-Path OR In-Line", help='Grab Excludes File-Path OR In-Line')
        parser.add_argument('-r', '--initrdfile', help='Initrd File')
        parser.add_argument('-f', '--kernelfile', help='Kernel File')
        parser.add_argument('-m', '--kernelmodules', help='Kernel Modules to be included in the Initrd or Ramdisk')
        parser.add_argument('-o', '--kerneloptions', action='store_true', help='Kernel Options used during boot time')
        parser.add_argument('-qo', '--quick-kerneloptions', dest='kerneloptions',
                                metavar="File-Path OR In-Line", help='Kernel Options File-Path OR In-Line')
        parser.add_argument('-k', '--kernelversion', help='Kernel Version')
        parser.add_argument('-p', '--path', help='Path of the image. Location of the image files or root directory structure')
        parser.add_argument('-i', '--imagefile', help='The file name of the packed image file')
        parser.add_argument('-d', '--distribution', help='The distribution e.g. redhat, ubuntu or opensuse')
        parser.add_argument('-l', '--osrelease', help='Distribution release or version')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser
