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

import types

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
EDITOR_KEYS = [
    'options', 'content', 'comment', 'prescript', 'partscript', 'postscript', 'grab_filesystems',
    'grab_exclude', 'kerneloptions', 'ztpconfig'
]
SERVICE_ACTIONS = ['start', 'stop', 'restart', 'reload', 'status']
SERVICES = ['dhcp', 'dns']
TOOL_DESCRIPTION = '''\
    Manage Luna Cluster
    --------------------------------
        - This tool will be helpful to communicate with the luna daemon.
        - use -h or --help at any point where you are not sure what to use.
'''
# TOOL_EPILOG = '© 2025 ClusterVision'
TOOL_EPILOG = ''


def parser_doc(table: str) -> types.SimpleNamespace:
    """
    This method provide the documentation for the subparsers.
    """
    response = types.SimpleNamespace()
    static = {
        "cluster" : {
            "help": "Cluster Information.",
            "description":  '''\
                Luna cluster shows and alters cluster level configuration
                like DNS forwarders, provisioning method etc.
            '''
        },
        "cloud": {
            "help": "Cloud Operations.",
            "description":  '''\
                This refers to anything related to external cloud provider(s)
                and making changes to those within trinityX.
            '''
        },
        "network": {
            "help": "Network operations.",
            "description":  '''\
                Luna network manages the networks. Changed values will also
                automatically be reflected in depended components like groups
                and nodes where respective interfaces are member of the
                altered network.
            '''
        },
        "osimage": {
            "help": "OSImage operations.",
            "description":  '''\
                This refers to changes and management of supported osimages
                within trinityX and to boot worker nodes.
            '''
        },
        "bmcsetup": {
            "help": "BMC Setup operations.",
            "description":  '''\
                Luna bmcsetup manages bmc or ipmi configurations through
                profiles. In here netchannels and passwords can be configured.
            '''
        },
        "switch": {
            "help": "Switch operations.",
            "description":  '''\
                Luna switch manages the optional switches. Switches configured
                with an IP address and OID will be scanned on interval to aid in
                switch port based node detection.
            '''
        },
        "otherdev": {
            "help": "Other Devices operations.",
            "description":  '''\
                Luna otherdev(ices) allows to add, change and remove devices like
                cameras, PDU-s and UPS-es. These devices will not be probed or
                accessed are primarily there to complete a rack layout (pun) or
                cluster interal DNS zone information.
            '''
        },
        "group" : {
            "help": "Group operations.",
            "description":  '''\
                Luna group manages the groups or categories of nodes. Nodes are
                typically member of a group where equal configuration can be done
                on a higher level. Good examples are to use a group for nodes where
                these boot the same osimage. It is common practice to have separate
                groups for a function or category like a compute node category,
                storage servers and login nodes.
            '''
        },
        "node" : {
            "help": "Compute Node operations.",
            "description":  '''\
                Luna node manages the nodes. All inheritable configuration from the
                group or cluster can be overridden here. This offers a great range of
                freedom where a set of nodes being nearly identical except for e.g.
                the bmcsetup can be setup without having duplicate configuration.
                The alternative bmcsetup profile can be simply set for just that node.
            '''
        },
        "secrets" : {
            "help": "Secrets operations.",
            "description":  '''\
                Luna secrets stores data for groups and nodes in an encrypted way.
                Secrets is typically used to store keytabs, certificates or other
                sensitive information that would otherwise be stored inside the osimage.
            '''
        },
        "service" : {
            "help": "Service operations.",
            "description":  '''\
                Luna service allows to manually stop, start, restart and status services
                like dns and dhcp.
            '''
        },
        "control" : {
            "help": "Control Nodes.",
            "description":  '''\
                This is a Luna tool fully supporting the APIs. A separate tool named lpower
                also controls the nodes the same way as luna control.
            '''
        },
        "monitor" : {
            "help": "Get Monitor Status.",
            "description":  '''\
                This relates to monitoring luna status messages and queues.
            '''
        }
    }
    response.help = static[table]["help"]
    response.description = static[table]["description"]
    return response


def actions(table: str) -> list:
    """
    This method provide the actions for the class.
    """
    response = False
    common_actions = ["list", "show", "add", "change", "rename", "clone", "remove"]
    network_actions = ["list", "show", "add", "change", "rename", "remove"]
    interface_actions = ["listinterface", "showinterface", "changeinterface", "removeinterface", "renameinterface"]
    member_action = ["member"]
    static = {
        "cloud" : network_actions,
        "group": common_actions + member_action + ["ospush"] + interface_actions,
        "node": common_actions + ["osgrab", "ospush"] + interface_actions,
        "network": network_actions + ["reserve", "ipinfo", "nextip", "dns", "route"],
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


def filter_columns(table: str) -> list:
    """
    This method remove the unnecessary fields from the dataset.
    """
    response = False
    static = {
        'cloud': ['name', 'type'],
        'bmcsetup': ['name', 'userid', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users'],
        'group': ['name', 'bmcsetupname', 'osimage', 'roles', 'interfaces'],
        'groupinterface': ['interface', 'network', 'options', 'vlanid', 'vlan_parent',
                           'bond_mode', 'bond_slaves', 'dhcp', 'mtu'],
        'groupsecrets': ['Group', 'name', 'path', 'content'],
        'network': ['name', 'network', 'type', 'zone', 'dhcp', 'dhcp_range_begin', 'dhcp_range_end',
                    'shared', 'dhcp_mode'],
        'dns': ['host', 'ipaddress'],
        'route': ['name', 'destination', 'gateway', 'metric', 'device', 'assigned'],
        'node': [
            'name', 'group', 'osimage', 'setupbmc', 'bmcsetup', 'status', 'tpm_present',
            'interfaces'
        ],
        'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network', 'options', 'mtu',
                          'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves', 'dhcp'],
        'nodesecrets': ['Node', 'name', 'path', 'content'],
        'osimage': ['name', 'kernelversion', 'path', 'distribution', 'osrelease'],
        'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
        'switch': ['name', 'network', 'oid', 'read', 'ipaddress', 'netboot'],
        'osimagetag': ['osimage', 'name', 'kernelfile', 'initrdfile', 'imagefile', 'path', 'nodes',
                       'groups'],
        'status': ['username_initiator', 'request_id', 'read', 'message', 'created'],
        'queue': [
            'username_initiator', 'queue_id', 'request_id', 'level', 'status', 'subsystem', 'task', 'created'
        ]
    }
    response = list(static[table])
    return response


def overrides(table=None):
    """
    This method has information regarding what could be an override for what table: node, group,
    cluster, etc
    """
    response = False
    static = {
        'node': [
            'osimage', 'osimagetag', 'kerneloptions', 'setupbmc', 'bmcsetup', 'netboot', 'ipxe_kernel',
            'bootmenu', 'roles', 'scripts', 'prescript', 'partscript', 'postscript',
            'provision_interface', 'provision_method', 'provision_fallback', 'routes'
        ],
        'group': [
            'provision_method', 'provision_interface', 'provision_fallback', 'kerneloptions',
            'osimagetag', 'routes'
        ]
    }
    if table and table in static:
        response = list(static[table])
    return response


def sortby(table: str) -> list:
    """
    This method remove the unnecessary fields from the dataset.
    """
    response = False
    static = {
        'cluster': [
            'name', 'controller', 'technical_contacts', 'provision_method', 'provision_fallback',
            'nameserver_ip', 'forwardserver_ip', 'domain_search', 'bind_legacy', 'dnssec_enable',
            'dnssec_validation', 'ntp_server', 'security',
            'nextnode_discover', 'createnode_ondemand', 'createnode_macashost', 'packing_bootpause',
            'user', 'debug'
        ],
        'cloud': ['name', 'type'],
        'node': [
            'info', 'name', 'hostname', 'group', 'osimage', 'osimagetag', 'kerneloptions',
            'interfaces', 'routes', 'status', 'vendor', 'assettag', 'position', 'switch', 'switchport',
            'cloud', 'setupbmc', 'bmcsetup', 'unmanaged_bmc_users', 'netboot', 'ipxe_kernel',
            'bootmenu', 'service', 'roles', 'scripts', '_prescript_source', 'prescript',
            '_partscript_source', 'partscript', '_postscript_source', 'postscript',
            'provision_interface', 'provision_method', 'provision_fallback', 'tpm_uuid',
            'tpm_pubkey', 'tpm_sha256', 'comment',  'macaddress'
        ],
        'group': [
            'info', 'name', 'domain', 'osimage', 'osimagetag', 'kerneloptions', 'interfaces',
            'routes', 'setupbmc', 'bmcsetupname', 'unmanaged_bmc_users', 'netboot', 'ipxe_kernel',
            'bootmenu', 'roles', 'scripts', 'prescript', 'partscript', 'postscript',
            'provision_interface', 'provision_method', 'provision_fallback', 'comment'
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
        'switch': ['name', 'network', 'oid', 'read', 'rw', 'ipaddress', 'netboot',
                   'default_url', 'bootfile', 'ztpformat', 'ztpconfig', 'comment'],
        'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
        'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network', 'mtu', 'vlanid',
                          'vlan_parent', 'bond_mode', 'bond_slaves'],
        'groupinterface': [
            'interfacename', 'network', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves'
        ],
        'groupsecrets': ['Group', 'name', 'path', 'content'],
        'nodesecrets': ['Node', 'name', 'path', 'content'],
        'network': [
            'name', 'type', 'zone', 'non_authoritative', 'dhcp',
            'network', 'gateway', 'nameserver_ip', 'dhcp_range_begin', 'dhcp_range_end',
            'network_ipv6', 'gateway_ipv6', 'nameserver_ip_ipv6',
            'dhcp_range_begin_ipv6', 'dhcp_range_end_ipv6', 'ntp_server',
            'gateway_metric', 'routes', 'dhcp_nodes_in_pool', 'dhcp_nodes_only', 'shared', 'comment'
        ],
        'osimagetag': [
            'osimage', 'name', 'kernelfile', 'initrdfile', 'imagefile', 'path', 'nodes', 'groups'
        ],
        'route': ['name', 'destination', 'gateway', 'metric', 'device', 'comment', 'assigned']
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


def spacer(table=None):
    """
    This method returns when an extra space to be added after what field is desired for a table
    """
    response = False
    static = {
        'network': [
            'dhcp', 'dhcp_range_end', 'dhcp_range_end_ipv6', 'prescript', 'partscript', 'postscript'
        ]
    }
    if table in static:
        response = list(static[table])
    return response
