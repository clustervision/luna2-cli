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
__version__     = "2.2"
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
    'setupredfish',
    'netboot',
    'bootmenu',
    'service'
]
EDITOR_KEYS = [
    'options', 'content', 'comment', 'prescript', 'partscript', 'postscript', 'grab_filesystems',
    'grab_exclude', 'kerneloptions', 'ztpconfig', 'disklayout', 'osimage_filter'
]
# Free-text fields where a Word/Outlook paste can land a lookalike character (TRIX-1868).
# content is excluded: it is a byte-preserving path for binary secrets/profile files.
NORMALIZE_KEYS = ['comment', 'prescript', 'partscript', 'postscript']
# Rich-text (Word/Outlook/browser) punctuation mapped to its plain ASCII equivalent.
TYPOGRAPHIC_LOOKALIKES = {
    '‘': "'",   # LEFT SINGLE QUOTATION MARK
    '’': "'",   # RIGHT SINGLE QUOTATION MARK
    '‚': "'",   # SINGLE LOW-9 QUOTATION MARK
    '‛': "'",   # SINGLE HIGH-REVERSED-9 QUOTATION MARK
    '′': "'",   # PRIME
    '“': '"',   # LEFT DOUBLE QUOTATION MARK
    '”': '"',   # RIGHT DOUBLE QUOTATION MARK
    '„': '"',   # DOUBLE LOW-9 QUOTATION MARK
    '‟': '"',   # DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    '″': '"',   # DOUBLE PRIME
    '‐': '-',   # HYPHEN
    '‑': '-',   # NON-BREAKING HYPHEN
    '‒': '-',   # FIGURE DASH
    '–': '-',   # EN DASH
    '—': '-',   # EM DASH
    '―': '-',   # HORIZONTAL BAR
    ' ': ' ',   # NO-BREAK SPACE
    ' ': ' ',   # FIGURE SPACE
    ' ': ' ',   # THIN SPACE
    '​': '',    # ZERO WIDTH SPACE
    '­': '',    # SOFT HYPHEN
    '…': '...'  # HORIZONTAL ELLIPSIS
}
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
        "redfishsetup": {
            "help": "Redfish Setup operations.",
            "description":  '''\
                Luna redfishsetup manages how Luna reaches a BMC over Redfish -
                the scheme, the port and whether the certificate is verified -
                together with the accounts it logs in with. A node picks one up
                from its group unless it names one of its own.
            '''
        },
        "biosconfig": {
            "help": "BIOS Configuration operations.",
            "description":  '''\
                Luna biosconfig manages BIOS settings grabbed off a golden node,
                to be pushed to other nodes of the same hardware. A configuration
                is created by 'luna node biosgrab' rather than by hand, and holds
                only what the node's own attribute registry says may be carried
                to another machine. Its exclude list can be changed here, and a
                clone of it becomes a profile once entries are changed on it
                by concept (--set hyperthreading=off). Assign a configuration to
                a node or a group (--biosconfig) and 'biospush' with no name
                pushes what is assigned.
            '''
        },
        "firmwarecatalog": {
            "help": "Firmware Catalogue operations.",
            "description":  '''\
                Luna firmwarecatalog holds the version each firmware component
                should be running, per kind of hardware, and the image that
                carries it. It is keyed on the manufacturer and model a board
                reports and never on a group, because one group routinely holds
                more than one platform. An entry is written here rather than
                grabbed from a machine: it is desired state, so it has to be
                stated. Apply it with 'luna node firmwarepush'.
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
                Luna secrets stores data for the cluster, groups and nodes in an encrypted
                way. Secrets is typically used to store keytabs, certificates or other
                sensitive information that would otherwise be stored inside the osimage.
                Secrets stack: a node receives the cluster secrets, its group secrets and
                its own, all of them.
            '''
        },
        "boot" : {
            "help": "Where nodes are in a (re)boot cycle.",
            "description":  '''\
                Luna boot summarises where the cluster is in a boot: how many nodes are
                waiting to be handed their installer, how many are fetching their image,
                how many are configuring, and how many are done. Grouped by group and by
                the osimage each node will actually boot.
            '''
        },
        "profile" : {
            "help": "Profile operations.",
            "description":  '''\
                Luna profile bundles configuration files with a service to act on, and
                assigns that bundle to groups and nodes. The files are written into the
                node during install and the service is enabled or disabled accordingly.
                Profiles stack: a node applies the profiles of its group plus its own.
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
    inventory_actions = ["listinventory", "showinventory", "refreshinventory"]
    disklayout_actions = ["showdisklayout"]
    member_action = ["member"]
    static = {
        "cloud" : network_actions,
        "group": common_actions + member_action + ["ospush", "biospush", "firmwarepush"] + interface_actions + disklayout_actions,
        "node": common_actions + ["osgrab", "ospush", "biosgrab", "biospush", "firmwarepush"] + interface_actions + inventory_actions + disklayout_actions,
        "boot": ["status"],
        "profile": common_actions + member_action + ["status", "addfile", "changefile", "removefile"],
        "network": network_actions + ["reserve", "ipinfo", "nextip", "dns", "route"],
        "osimage": common_actions + member_action + ["pack", "cancel", "kernel", "tag", "updatecerts"],
        "bmcsetup": common_actions + member_action,
        "redfishsetup": common_actions + member_action + ["addaccount", "changeaccount", "removeaccount"],
        # no add: a configuration comes into existence by being grabbed off a
        # node, never by being typed in. A clone of that grab is a profile
        "biosconfig": ["list", "show", "change", "clone", "rename", "remove", "status"],
        # an entry is desired state, written by hand, so unlike biosconfig it has
        # an add. There is no clone: two entries differing in one field is how a
        # catalogue starts disagreeing with itself about the same hardware
        "firmwarecatalog": ["list", "show", "add", "change", "rename", "remove", "status"],
        "otherdev": common_actions,
        "switch" : common_actions + ["listinterface", "showinterface", "changeinterface", "removeinterface", "renameinterface"],
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
        'redfishsetup': ['name', 'scheme', 'port', 'verify', 'accounts'],
        'biosconfig': ['name', 'manufacturer', 'model', 'biosversion', 'grabbedfrom', 'settings'],
        'firmwarecatalog': ['name', 'manufacturer', 'model', 'component', 'version', 'imagefile'],
        'group': ['name', 'bmcsetupname', 'osimage', 'roles', 'interfaces'],
        'groupinterface': ['interface', 'network', 'options', 'vlanid', 'vlan_parent',
                           'bond_mode', 'bond_slaves', 'dhcp', 'mtu'],
        'groupsecrets': ['Group', 'name', 'path', 'owner', 'mode', 'content'],
        'clustersecrets': ['name', 'path', 'owner', 'mode', 'content'],
        'profile': ['name', 'scope', 'service', 'action', 'files'],
        'profilefile': ['name', 'path', 'owner', 'mode', 'content'],
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
        'switchinterface': ['interface', 'mgmt', 'ipaddress', 'ipaddress_ipv6', 'macaddress', 'network'],
        'nodesecrets': ['Node', 'name', 'path', 'owner', 'mode', 'content'],
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
            'osimage', 'osimagetag', 'kerneloptions', 'setupbmc', 'bmcsetup', 'redfishsetup', 'biosconfig', 'netboot', 'ipxe_kernel',
            'bootmenu', 'roles', 'scripts', 'prescript', 'partscript', 'postscript',
            'install_mode', 'disklayout', 'osimage_filter',
            'provision_interface', 'provision_method', 'provision_fallback', 'routes',
            'unmanaged_bmc_users'
        ],
        'group': [
            'provision_method', 'provision_interface', 'provision_fallback', 'kerneloptions',
            'osimagetag', 'install_mode', 'routes',
            'ipxe_kernel', 'bootmenu', 'unmanaged_bmc_users'
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
            'install_mode',
            'nameserver_ip', 'forwardserver_ip', 'domain_search', 'bind_legacy', 'dnssec_enable',
            'dnssec_validation', 'ntp_server', 'security',
            'nextnode_discover', 'createnode_ondemand', 'createnode_macashost', 'packing_bootpause',
            'user', 'debug'
        ],
        'cloud': ['name', 'type'],
        # grouped, and the groups are what the dividers below draw a rule between:
        # identity, then where the machine is, then how we reach its BMC, then how
        # it boots, then what is layered onto it, then how it is installed, then the
        # scripts, then provisioning. A field that is not listed here still appears -
        # it is appended at the end - so adding one to the schema and forgetting this
        # list is untidy rather than invisible.
        'node': [
            'info',
            'name', 'hostname', 'status', 'vendor', 'assettag', 'group', 'osimage', 'osimagetag',
            'interfaces', 'routes', 'position', 'switch', 'switchport', 'cloud',
            'setupbmc', 'setupredfish', 'bmcsetup', 'redfishsetup', 'unmanaged_bmc_users',
            'netboot', 'ipxe_kernel', 'kerneloptions', 'biosconfig', 'bootmenu', 'service',
            'roles', 'scripts', 'profiles', 'profiles_digest',
            'install_mode', '_disklayout_source', 'disklayout',
            '_osimage_filter_source', 'osimage_filter',
            '_prescript_source', 'prescript',
            '_partscript_source', 'partscript',
            '_postscript_source', 'postscript',
            'provision_interface', 'provision_method', 'provision_fallback', 'tpm_uuid',
            'tpm_pubkey', 'tpm_sha256', 'comment', 'macaddress'
        ],
        # the same blocks as 'node' above, in the same order, minus the fields a
        # group does not have. Reading one after the other should not feel like
        # two different tools.
        'group': [
            'info',
            'name', 'domain', 'osimage', 'osimagetag',
            'interfaces', 'routes',
            'setupbmc', 'setupredfish', 'bmcsetupname', 'redfishsetupname',
            'unmanaged_bmc_users',
            'netboot', 'ipxe_kernel', 'kerneloptions', 'biosconfig', 'bootmenu',
            'roles', 'scripts', 'profiles',
            'install_mode', 'disklayout', 'osimage_filter',
            'prescript', 'partscript', 'postscript',
            'provision_interface', 'provision_method', 'provision_fallback', 'comment'
        ],
        'bmcsetup': [
            'name', 'userid', 'username', 'password', 'netchannel', 'mgmtchannel',
            'unmanaged_bmc_users', 'comment'
        ],
        'redfishsetup': ['name', 'scheme', 'port', 'verify', 'accounts', 'comment'],
        'biosconfig': ['name', 'manufacturer', 'model', 'biosversion', 'grabbedfrom', 'settings',
                       'grab_exclude', 'updated', 'comment'],
        'firmwarecatalog': ['name', 'manufacturer', 'model', 'component', 'version', 'imagefile',
                            'updated', 'comment'],
        'osimage': [
            'name', 'grab_filesystems', 'grab_exclude', 'initrdfile',
            'kernelversion', 'kernelfile', 'kernelmodules', 'kerneloptions', 'path', 'imagefile',
            'distribution', 'osrelease', 'comment'
        ],
        'switch': ['name', 'vendor', 'ostype', 'mgmt_interface', 'network', 'ipaddress', 'ipaddress_ipv6', 'macaddress',
                   'oid', 'read', 'rw', 'uplinkports',
                   'netboot', 'default_url', 'bootfile', 'ztpformat', 'ztpconfig',
                   'url_protocol', 'url_server', 'tftp_enable', 'comment'],
        'otherdev': ['name', 'network', 'ipaddress', 'macaddress', 'comment'],
        'nodeinterface': ['interface', 'ipaddress', 'macaddress', 'network', 'mtu', 'vlanid',
                          'vlan_parent', 'bond_mode', 'bond_slaves'],
        'switchinterface': ['interface', 'mgmt', 'ipaddress', 'ipaddress_ipv6', 'macaddress', 'network'],
        'groupinterface': [
            'interfacename', 'network', 'vlanid', 'vlan_parent', 'bond_mode', 'bond_slaves'
        ],
        'groupsecrets': ['Group', 'name', 'path', 'owner', 'mode', 'content'],
        'nodesecrets': ['Node', 'name', 'path', 'owner', 'mode', 'content'],
        'clustersecrets': ['name', 'path', 'owner', 'mode', 'content'],
        'profile': ['name', 'scope', 'service', 'action', 'files'],
        'profilefile': ['name', 'path', 'owner', 'mode', 'content'],
        'network': [
            'name', 'type', 'zone', 'non_authoritative', 'dhcp',
            'network', 'gateway', 'nameserver_ip', 'dhcp_range_begin', 'dhcp_range_end',
            'network_ipv6', 'gateway_ipv6', 'nameserver_ip_ipv6',
            'dhcp_range_begin_ipv6', 'dhcp_range_end_ipv6', 'ntp_server',
            'gateway_metric', 'routes', 'dhcp_nodes_in_pool', 'dhcp_nodes_only', 'shared', 'dhcp_relay',
            'dhcp_link_subnet', 'comment'
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
    # the LAST field of each block in sortby() above. Both spellings of every one:
    # a field that deviates from its parent renders as '<name> *' (helper.py adds
    # the marker), and the rule is matched on what is rendered - so listing only
    # the bare name loses the divider exactly when a node overrides that field.
    node_blocks = ['info', 'osimagetag', 'cloud', 'unmanaged_bmc_users', 'service',
                   'profiles_digest', 'osimage_filter', 'prescript', 'partscript',
                   'postscript', 'comment']
    group_blocks = ['info', 'osimagetag', 'routes', 'unmanaged_bmc_users', 'bootmenu',
                    'profiles', 'osimage_filter', 'prescript', 'partscript', 'postscript',
                    'comment']
    static = {
        'node': node_blocks + [f'{field} *' for field in node_blocks],
        'group': group_blocks + [f'{field} *' for field in group_blocks]
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
