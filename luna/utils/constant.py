#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Constant File for the CLI.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

INI_FILE = '/trinity/local/luna/config/luna.ini'
TOKEN_FILE = '/tmp/token.txt'
VERSION_FILE = 'VERSION.txt'
LOG_DIR = '/var/log/luna'
LOG_FILE = '/var/log/luna/luna2-cli.log'
BOOL_CHOICES = ['y', 'yes', 'n', 'no', '']
BOOL_META = "{y,yes,n,no,''}"
BOOL_KEYS = [
    'debug',
    'security',
    'createnode_ondemand',
    'dhcp',
    'setupbmc',
    'netboot',
    'localinstall',
    'bootmenu',
    'localboot',
    'service'
]
EDITOR_KEYS = ['options', 'content', 'comment', 'prescript', 'partscript', 'postscript']
SERVICE_ACTIONS = ['start', 'stop', 'restart', 'reload', 'status']
SERVICES = ['dhcp', 'dns', 'luna2']

BANNER_NAME = 'Luna 2 CLI'
BANNER_STYLE= "digital"
TOOL_DESCRIPTION = '''\
    Manage Luna Cluster
    --------------------------------
        - This tool will be helpful to communicate with the luna daemon.
        - use -h or --help at any point where you are not sure what to use.
'''
TOOL_EPILOG = '© 2023 ClusterVision'


def actions(table=None):
    """This method provide the actions for the class."""
    response = False
    common_actions = ["list", "show", "add", "change", "rename", "clone", "remove"]
    interface_actions = ["listinterface", "showinterface", "changeinterface", "removeinterface"]
    member_action = ["member"]
    static = {
        "group": common_actions + member_action + interface_actions,
        "node": common_actions + interface_actions,
        "network": common_actions + ["ipinfo", "nextip"],
        "osimage": common_actions + member_action + ["pack", "kernel"],
        "bmcsetup": common_actions + member_action,
        "otherdev": common_actions,
        "switch" : common_actions
    }
    response = list(static[table])
    return response


def filter_columns(table=None):
    """
    This method remove the unnecessary fields from
    the dataset.
    """
    response = False
    static = {
        'bmcsetup': ['name', 'userid', 'netchannel', 'mgmtchannel', 'unmanaged_bmc_users'],
        'cluster': ['name', 'hostname','ipaddress', 'technical_contacts', 'provision_method',
                    'security'],
        'controller': ['id', 'clusterid', 'hostname', 'status', 'ipaddress', 'serverport'],
        'group': ['name', 'bmcsetupname', 'osimage', 'provision_fallback', 'interfaces'],
        'groupinterface': ['interface', 'network', 'options'],
        'groupsecrets': ['Group', 'name', 'path', 'content'],
        'ipaddress': ['id', 'ipaddress', 'subnet', 'network'],
        'monitor': ['id', 'nodeid', 'status', 'state'],
        'network': ['name', 'network', 'ns_ip', 'dhcp', 'dhcp_range_begin', 'dhcp_range_end'],
        'node': ['name', 'group', 'osimage', 'setupbmc', 'bmcsetup', 'status', 'tpm_uuid'],
        'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network', 'options'],
        'nodesecrets': ['Node', 'name', 'path', 'content'],
        'osimage': ['name', 'kernelfile', 'path', 'tarball', 'distribution'],
        'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
        'roles': ['id', 'name', 'modules'],
        'switch': ['name', 'network', 'oid', 'read', 'ipaddress'],
        'tracker': ['infohash', 'peer', 'ipaddress', 'port', 'status'],
        'user': ['id', 'username', 'password', 'roleid', 'createdby', 'lastlogin', 'created']
    }
    response = list(static[table])
    return response


def sortby(table=None):
    """
    This method remove the unnecessary fields from
    the dataset.
    """
    response = False
    static = {
        'cluster': ['name', 'ns_ip','ntp_server', 'provision_fallback', 'provision_method',
                    'security', 'technical_contacts', 'user', 'debug'],
        'controller': ['hostname', 'ipaddress','luna_config', 'serverport', 'status'],
        'node': ['name', 'hostname', 'group', 'osimage', 'interfaces', 'localboot',
                    'macaddress', 'switch', 'switchport', 'setupbmc', 'status', 'service',
                    'prescript', 'partscript', 'postscript', 'netboot', 'localinstall',
                    'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback',
                    'tpmuuid', 'tpmpubkey', 'tpmsha256', 'unmanaged_bmc_users', 'comment'],
        'group': ['name', 'bmcsetup', 'bmcsetupname', 'domain', 'interfaces', 'osimage',
                    'prescript', 'partscript', 'postscript', 'netboot', 'localinstall',
                    'bootmenu', 'provisionmethod', 'provisioninterface', 'provisionfallback',
                    'unmanaged_bmc_users','comment'],
        'bmcsetup': ['name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel',
                        'unmanaged_bmc_users', 'comment'],
        'osimage': ['name', 'dracutmodules', 'grab_filesystems', 'grab_exclude', 'initrdfile',
                    'kernelversion', 'kernelfile', 'kernelmodules', 'kerneloptions', 'path',
                    'tarball', 'torrent', 'distribution', 'comment'],
        'switch': ['name', 'network', 'oid', 'read', 'rw', 'ipaddress', 'comment'],
        'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
        'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network'],
        'groupinterface': ['interfacename', 'network'],
        'groupsecrets': ['Group', 'name', 'path', 'content'],
        'nodesecrets': ['Node', 'name', 'path', 'content'],
        'network': ['name', 'network', 'ns_hostname', 'ns_ip', 'ntp_server', 'gateway', 'dhcp',
                    'dhcp_range_begin', 'dhcp_range_end', 'comment']
    }
    response = list(static[table])
    return response
