#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arguments Class for the CLI for common arguments.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from luna.utils.constant import BOOL_CHOICES, BOOL_META

class Arguments():
    """
    All kind of common Arguments methods.
    """

    def common_list_args(self, parser=None):
        """
        This method will provide the common list and show arguments.
        """
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        parser.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        return parser


    def common_bmcsetup_args(self, parser=None):
        """
        This method will provide the common bmcsetup arguments.
        """
        parser.add_argument('name', help='BMC Setup Name')
        parser.add_argument('-uid', '--userid', type=int, help='UserID')
        parser.add_argument('-u', '--username', help='Username')
        parser.add_argument('-p', '--password', help='Password')
        parser.add_argument('-nt', '--netchannel', type=int, help='Network Channel')
        parser.add_argument('-mt', '--mgmtchannel', type=int, help='Management Channel')
        parser.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def common_group_args(self, parser=None):
        """
        This method will provide the common group arguments.
        """
        parser.add_argument('name', help='Name of the Group')
        parser.add_argument('-b', '--setupbmc', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='BMC Setup')
        parser.add_argument('-o', '--osimage', help='OS Image Name')
        parser.add_argument('-bmc', '--bmcsetupname', help='BMC Setup Name')
        parser.add_argument('-D', '--domain', help='Domain Name')
        parser.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        parser.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        parser.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        parser.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        parser.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        parser.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        parser.add_argument('-pi', '--provision_interface', help='Provision Interface')
        parser.add_argument('-pm', '--provision_method', help='Provision Method')
        parser.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        parser.add_argument('-nb', '--netboot', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Network Boot')
        parser.add_argument('-li', '--localinstall', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Local Install')
        parser.add_argument('-bm', '--bootmenu', choices=BOOL_CHOICES,
                               metavar=BOOL_META, help='Boot Menu')
        parser.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-if', '--interface', help='Interface Name')
        parser.add_argument('-N', '--network', help='Interface Network Name')
        parser.add_argument('-O', '--options', action='store_true', help='Interfaces Options')
        parser.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def common_node_args(self, parser=None, required=None):
        """
        This method will provide the common node arguments.
        """
        parser.add_argument('name', help='Name of the Node')
        parser.add_argument('-host', '--hostname',help='Hostname')
        if required:
            parser.add_argument('-g', '--group', required=True, help='Group Name')
        else:
            parser.add_argument('-g', '--group', help='Group Name')
        parser.add_argument('-o', '--osimage', help='OS Image Name')
        parser.add_argument('-b', '--setupbmc', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='BMC Setup')
        parser.add_argument('-bmc', '--bmcsetup', help='BMC Setup')
        parser.add_argument('-sw', '--switch', help='Switch Name')
        parser.add_argument('-sp', '--switchport', help='Switch Port')
        parser.add_argument('-pre', '--prescript', action='store_true', help='Pre Script')
        parser.add_argument('-qpre', '--quick-prescript', dest='prescript',
                        metavar="File-Path OR In-Line", help='Pre Script File-Path OR In-Line')
        parser.add_argument('-part', '--partscript', action='store_true', help='Part Script')
        parser.add_argument('-qpart', '--quick-partscript', dest='partscript',
                        metavar="File-Path OR In-Line", help='Part Script File-Path OR In-Line')
        parser.add_argument('-post', '--postscript', action='store_true', help='Post Script')
        parser.add_argument('-qpost', '--quick-postscript', dest='postscript',
                        metavar="File-Path OR In-Line", help='Post Script File-Path OR In-Line')
        parser.add_argument('-pi', '--provision_interface', help='Provision Interface')
        parser.add_argument('-pm', '--provision_method', help='Provision Method')
        parser.add_argument('-fb', '--provision_fallback', help='Provision Fallback')
        parser.add_argument('-nb', '--netboot', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Network Boot')
        parser.add_argument('-li', '--localinstall', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Local Install')
        parser.add_argument('-bm', '--bootmenu', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Boot Menu')
        # parser.add_argument('-lb', '--localboot', choices=BOOL_CHOICES,
                            #   metavar=BOOL_META, help='Local Boot')
        parser.add_argument('-ser', '--service', choices=BOOL_CHOICES,
                              metavar=BOOL_META, help='Service')
        parser.add_argument('-s', '--status', help='Status')
        parser.add_argument('-tid', '--tpm_uuid', help='TPM UUID')
        parser.add_argument('-tkey', '--tpm_pubkey', help='TPM Public Key')
        parser.add_argument('-tsha', '--tpm_sha256', help='TPM SHA256')
        parser.add_argument('-ubu', '--unmanaged_bmc_users', help='Unmanaged BMC Users')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-if', '--interface', help='Interface Name')
        parser.add_argument('-N', '--network', help='Interface Network Name')
        parser.add_argument('-I', '--ipaddress', help='Interfaces IP Address')
        parser.add_argument('-M', '--macaddress', help='Interfaces MAC Address')
        parser.add_argument('-O', '--options', action='store_true', help='Interfaces Options')
        parser.add_argument('-qo', '--quick-options', dest='options',
                                metavar="File-Path OR In-Line", help='Options File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def common_network_args(self, parser=None, required=None):
        """
        This method will provide the common network arguments.
        """
        parser.add_argument('name', help='Network Name')
        if required:
            parser.add_argument('-N', '--network', required=True, help='Network')
        else:
            parser.add_argument('-N', '--network', help='Network')
        parser.add_argument('-g', '--gateway', help='Gateway')
        parser.add_argument('-nsip', '--nameserver_ip', help='NameServer IP')
        parser.add_argument('-ntp', '--ntp_server', help='NTP Server')
        parser.add_argument('-dhcp', '--dhcp', choices=BOOL_CHOICES,
                                 metavar=BOOL_META, help='DHCP')
        parser.add_argument('-ds', '--dhcp_range_begin', help='DHCP Range Start')
        parser.add_argument('-de', '--dhcp_range_end', help='DHCP Range End')
        parser.add_argument('-z', '--zone', help='Internal OR External Network Zone')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def common_osimage_args(self, parser=None, required=None):
        """
        This method will provide the common osimage arguments.
        """
        parser.add_argument('name', help='OSImage Name')
        parser.add_argument('-dm', '--dracutmodules', help='Dracut Modules')
        parser.add_argument('-gf', '--grab_filesystems', help='Grab Filesystems')
        parser.add_argument('-ge', '--grab_exclude', help='Grab Excludes')
        parser.add_argument('-rd', '--initrdfile', help='INIT RD File')
        parser.add_argument('-k', '--kernelfile', help='Kernel File')
        parser.add_argument('-m', '--kernelmodules', help='Kernel Modules')
        parser.add_argument('-o', '--kerneloptions', help='Kernel Options')
        parser.add_argument('-ver', '--kernelversion', help='Kernel Version')
        if required:
            parser.add_argument('-p', '--path', required=True, help='Path of image')
        else:
            parser.add_argument('-p', '--path', help='Path of image')
        parser.add_argument('-img', '--imagefile', help='Imagefile UUID')
        parser.add_argument('-D', '--distribution', help='Distribution')
        parser.add_argument('-R', '--osrelease', help='OS release or version')
        parser.add_argument('-sys', '--systemroot', help='System Root for OS Image')
        parser.add_argument('-c', '--comment', action='store_true', help='Comment')
        parser.add_argument('-qc', '--quick-comment', dest='comment',
                                metavar="File-Path OR In-Line", help='Comment File-Path OR In-Line')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser
