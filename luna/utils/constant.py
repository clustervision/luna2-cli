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
Constant File for the CLI.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.1"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

INI_FILE = '/trinity/local/luna/cli/config/luna.ini'
TOKEN_FILE = '/trinity/local/luna/cli/config/token.txt'
VERSION_FILE = 'VERSION.txt'
LOG_DIR = '/var/log/luna'
LOG_FILE = '/var/log/luna/luna2-cli.log'
BOOL_CHOICES = ['y', 'yes', 'n', 'no', '']
BOOL_META = "{y,yes,n,no,''}"
BOOL_KEYS = [
    'debug',
    'security',
    'createnode_ondemand',
    'createnode_macashost',
    'nextnode_discover',
    'dhcp',
    'setupbmc',
    'netboot',
    'bootmenu',
    'service'
]
EDITOR_KEYS = ['options', 'content', 'comment', 'prescript', 'partscript', 'postscript', 'grab_filesystems', 'grab_exclude', 'kerneloptions']
SERVICE_ACTIONS = ['start', 'stop', 'restart', 'reload', 'status']
SERVICES = ['dhcp', 'dns', 'luna2']
TOOL_DESCRIPTION = '''\
    Manage Luna Cluster
    --------------------------------
        - This tool will be helpful to communicate with the luna daemon.
        - use -h or --help at any point where you are not sure what to use.
'''
# TOOL_EPILOG = '© 2025 ClusterVision'
TOOL_EPILOG = ''


def actions(table=None):
    """
    This method provide the actions for the class.
    """
    response = False
    common_actions = ["list", "show", "add", "change", "rename", "clone", "remove"]
    network_actions = ["list", "show", "add", "change", "rename", "remove"]
    interface_actions = ["listinterface", "showinterface", "changeinterface", "removeinterface"]
    member_action = ["member"]
    static = {
        "cloud" : network_actions,
        "group": common_actions + member_action + ["ospush"] + interface_actions,
        "node": common_actions + ["osgrab", "ospush"] + interface_actions,
        "network": network_actions + ["reserve", "ipinfo", "nextip", "dns"],
        "osimage": common_actions + member_action + ["pack", "kernel", "tag"],
        "bmcsetup": common_actions + member_action,
        "otherdev": common_actions,
        "switch" : common_actions,
        "control" : ["power", "sel", "chassis", "redfish"],
        "power" : ["on", "off", "status", "reset"],
        "sel" : ["list", "clear"],
        "chassis" : ["identify", "noidentify"],
        "redfish" : ["upload", "setting"],
        "tag_osimage" : ["change", "remove"]
    }
    response = list(static[table])
    return response


def filter_columns(table=None):
    """
    This method remove the unnecessary fields from the dataset.
    """
    response = False
    static = {
        'cloud': ['name', 'type'],
        'bmcsetup': ['name', 'userid', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users'],
        'group': ['name', 'bmcsetupname', 'osimage', 'roles', 'interfaces'],
        'groupinterface': ['interface', 'network', 'options', 'vlanid', 'vlan_parent',
                           'bond_mode', 'bond_slaves', 'dhcp'],
        'groupsecrets': ['Group', 'name', 'path', 'content'],
        'network': ['name', 'network', 'type', 'dhcp', 'dhcp_range_begin', 'dhcp_range_end',
                    'dhcp_nodes_in_pool'],
        'dns': ['host', 'ipaddress'],
        'node': ['name', 'group', 'osimage', 'setupbmc', 'bmcsetup', 'status', 'tpm_present', 'interfaces'],
        'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network', 'options',
                          'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp'],
        'nodesecrets': ['Node', 'name', 'path', 'content'],
        'osimage': ['name', 'kernelversion', 'path', 'distribution', 'osrelease'],
        'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
        'switch': ['name', 'network', 'oid', 'read', 'ipaddress'],
        'osimagetag': ['osimage', 'name', 'kernelfile', 'initrdfile', 'imagefile', 'path', 'nodes',
                       'groups'],
        'status': ['username_initiator', 'request_id', 'read', 'message', 'created'],
        'queue': ['username_initiator', 'request_id', 'level', 'status', 'subsystem', 'task', 'created']
    }
    response = list(static[table])
    return response


def overrides(table=None):
    """
    This method has information regarding what could be an override for what table: node, group, cluster, etc
    """
    response = False
    static = {
        'node': [
            'osimage', 'osimagetag', 'kerneloptions', 'setupbmc', 'bmcsetup', 'netboot', 'bootmenu',
            'roles', 'scripts', 'prescript', 'partscript', 'postscript', 'provision_interface',
            'provision_method', 'provision_fallback'
        ],
        'group': [
            'provision_method', 'provision_interface', 'provision_fallback', 'kerneloptions', 'osimagetag'
        ]
    }
    if table and table in static:
        response = list(static[table])
    return response


def sortby(table=None):
    """
    This method remove the unnecessary fields from the dataset.
    """
    response = False
    static = {
        'cluster': [
            'name', 'controller', 'technical_contacts', 'provision_method', 'provision_fallback',
            'nameserver_ip', 'forwardserver_ip', 'domain_search', 'ntp_server', 'security',
            'nextnode_discover', 'createnode_ondemand', 'createnode_macashost', 'packing_bootpause',
            'user', 'debug'
        ],
        'cloud': ['name', 'type'],
        'node': [
            'info', 'name', 'hostname', 'group', 'osimage', 'osimagetag', 'kerneloptions',
            'interfaces', 'status', 'vendor', 'assettag', 'position', 'switch', 'switchport',
            'cloud', 'setupbmc', 'bmcsetup', 'unmanaged_bmc_users', 'netboot', 'bootmenu',
            'service', 'roles', 'scripts', '_prescript_source', 'prescript', '_partscript_source',
            'partscript', '_postscript_source', 'postscript', 'provision_interface',
            'provision_method', 'provision_fallback', 'tpm_uuid', 'tpm_pubkey', 'tpm_sha256',
            'comment',  'macaddress'
        ],
        'group': [
            'info', 'name', 'domain', 'osimage', 'osimagetag', 'kerneloptions', 'interfaces', 'setupbmc',
            'bmcsetupname', 'unmanaged_bmc_users', 'netboot', 'bootmenu', 'roles', 'scripts',
            'prescript', 'partscript', 'postscript', 'provision_interface', 'provision_method',
            'provision_fallback', 'comment'
        ],
        'bmcsetup': [
            'name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel',
            'unmanaged_bmc_users', 'comment'
        ],
        'osimage': [
            'name', 'grab_filesystems', 'grab_exclude', 'initrdfile',
            'kernelversion', 'kernelfile', 'kernelmodules', 'kerneloptions', 'path', 'imagefile',
            'distribution', 'osrelease', 'comment'
        ],
        'switch': ['name', 'network', 'oid', 'read', 'rw', 'ipaddress', 'comment'],
        'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
        'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network', 'vlanid',
                          'vlan_parent', 'bond_mode', 'bond_slaves'],
        'groupinterface': ['interfacename', 'network', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves'],
        'groupsecrets': ['Group', 'name', 'path', 'content'],
        'nodesecrets': ['Node', 'name', 'path', 'content'],
        'network': [
            'name', 'type', 'zone','network', 'gateway', 'nameserver_ip', 'dhcp_range_begin',
            'dhcp_range_end', 'network_ipv6', 'gateway_ipv6', 'nameserver_ip_ipv6',
            'dhcp_range_begin_ipv6', 'dhcp_range_end_ipv6', 'dhcp', 'gateway_metric', 'ntp_server',
            'shared', 'comment'
        ],
        'osimagetag': [
            'osimage', 'name', 'kernelfile', 'initrdfile', 'imagefile', 'path', 'nodes', 'groups'
        ]
    }
    response = list(static[table])
    return response


def divider(table=None):
    """
    This method returns when a divider after what field is desired for a table
    """
    response = False
    static = {
        'node': ['info','scripts', 'prescript', 'partscript', 'postscript',
                 'scripts *', 'prescript *', 'partscript *', 'postscript *'],
        'group': ['info','scripts', 'prescript', 'partscript', 'postscript']
    }
    if table in static:
        response = list(static[table])
    return response
